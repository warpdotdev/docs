#!/usr/bin/env python3
"""Sync the public OpenAPI spec from warp-server into the docs repo.

The canonical OpenAPI spec lives in `warp-server/public_api/openapi.yaml`.
The Scalar API reference at `docs.warp.dev/api` renders from
`docs/developers/agent-api-openapi.yaml`, which is a curated subset.

This script generates the docs subset deterministically:
  * operations marked ``x-internal: true`` are removed, and a path whose
    every operation is internal is dropped entirely
  * tags listed in EXCLUDED_TAGS are removed (and their paths/schemas)
  * paths listed in EXCLUDED_PATHS are removed
  * every section in PRUNABLE_COMPONENT_SECTIONS (schemas, responses,
    parameters, ...) is pruned to only the entries reachable from the
    surviving paths via $ref walking
  * every key in STRIP_FLAGS (implementation-only extensions such as
    ``x-go-type`` and ``x-stainless-naming``) is removed recursively from
    whatever survives the filtering above, wherever it appears in the tree
  * the regenerated spec is validated for unresolved $refs before
    being written; apply will refuse to write a broken spec

``x-internal`` is warp-server's own public/private marker: its
``public_api/public-openapi-filter.yaml`` strips those operations when the
release pipeline publishes the spec. Honoring the same marker here keeps this
script from publishing a surface the server team has explicitly marked private,
instead of relying only on a hand-maintained tag allowlist that goes stale
whenever a new private tag appears. STRIP_FLAGS mirrors that same filter's
``stripFlags`` list, so implementation-only extensions never reach the
published docs copy either.

Modes:
  diff       Print structural drift between source and target. Exits 1
             if drift is found.
  apply      Rewrite target with the regenerated docs subset. Exits 3
             if any $ref in the output is unresolved.
  self-test  Runs a small in-memory test to validate $ref walking and
             output ref resolution.

Usage:
  python3 sync_openapi.py --mode diff
  python3 sync_openapi.py --mode apply
  python3 sync_openapi.py --mode self-test
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

import yaml

# Tags whose paths and tag entry should be removed entirely.
# `memory_stores` / `memory` back Agent Memory, which is a research preview.
# `harness-support` is the worker-to-server contract — not a public API.
# `factory` is Oz Factory, which has not shipped publicly.
# These are belt-and-braces on top of the `x-internal` filter below: a tag can
# be private even when individual operations aren't marked internal yet.
EXCLUDED_TAGS: frozenset[str] = frozenset(
    {"memory_stores", "memory", "harness-support", "factory"}
)

# OpenAPI extension warp-server uses to mark an operation private. Mirrors
# `flagValues: [x-internal: true]` in warp-server/public_api/public-openapi-filter.yaml.
INTERNAL_MARKER = "x-internal"

# Implementation-only OpenAPI extensions that must never reach the published
# docs copy. Mirrors `stripFlags` in
# warp-server/public_api/public-openapi-filter.yaml: these keys are useful for
# server/SDK code generation (oapi-codegen, Stainless) but are stripped
# unconditionally from every remaining object, not just top-level operations.
STRIP_FLAGS: frozenset[str] = frozenset(
    {
        "x-internal",
        "x-enum-varnames",
        "x-go-type",
        "x-go-type-import",
        "x-go-type-skip-optional-pointer",
        "x-oapi-codegen-extra-tags",
        "x-stainless-deprecation-message",
        "x-stainless-naming",
    }
)

# Path-item keys that are HTTP operations rather than shared path metadata.
HTTP_METHODS: frozenset[str] = frozenset(
    {"get", "put", "post", "delete", "options", "head", "patch", "trace"}
)

# Component sections pruned down to entries reachable from the surviving
# paths. Mirrors `unusedComponents` in
# warp-server/public_api/public-openapi-filter.yaml. Sections outside this set
# (notably `securitySchemes`, which nothing $refs) are copied verbatim.
PRUNABLE_COMPONENT_SECTIONS: frozenset[str] = frozenset(
    {
        "schemas",
        "parameters",
        "examples",
        "headers",
        "requestBodies",
        "responses",
        "mediaTypes",
    }
)

# Specific paths under otherwise-public tags that should be hidden from
# the public API reference. Keep in sync with references/sync-policy.md.
EXCLUDED_PATHS: frozenset[str] = frozenset(
    {
        "/agent/runs/{runId}/handoff/attachments",
        "/agent/handoff/upload-snapshot",
        "/agent/conversations/{conversation_id}/fork",
        "/agent/conversations/{conversationId}/redirect",
    }
)

# Path prefixes that are private no matter how the operation is tagged. Tag
# checks alone are not enough here: some Factory operations are tagged `agent`
# upstream (for example `GET /factory/scorers/{scorer_id}/results`), so a
# tags-only rule would leak them into the public reference.
EXCLUDED_PATH_PREFIXES: tuple[str, ...] = ("/factory",)

# Default checkout layout: docs/ and warp-server/ as siblings.
DEFAULT_SOURCE = Path("../warp-server/public_api/openapi.yaml")
DEFAULT_TARGET = Path("developers/agent-api-openapi.yaml")


# ---------------------------------------------------------------------------
# YAML helpers
# ---------------------------------------------------------------------------


class _PreserveStringDumper(yaml.SafeDumper):
    """SafeDumper that emits multiline strings as block literals (|).

    Without this, descriptions that contain newlines round-trip through
    PyYAML as ugly quoted strings with explicit ``\\n`` escapes, which is
    both unreadable and a noisy diff against the hand-edited source.
    """


def _str_representer(dumper: yaml.SafeDumper, data: str) -> Any:
    if "\n" in data:
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
    return dumper.represent_scalar("tag:yaml.org,2002:str", data)


_PreserveStringDumper.add_representer(str, _str_representer)


def _load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    if not isinstance(data, dict):
        raise SystemExit(f"{path}: expected a YAML mapping at the document root")
    return data


def _dump_yaml(data: dict[str, Any], path: Path) -> None:
    with path.open("w", encoding="utf-8") as fh:
        yaml.dump(
            data,
            fh,
            Dumper=_PreserveStringDumper,
            sort_keys=False,
            default_flow_style=False,
            allow_unicode=True,
            width=10**6,  # avoid line wrapping
        )


# ---------------------------------------------------------------------------
# Filtering & schema-pruning
# ---------------------------------------------------------------------------


def _operation_tags(operation: dict[str, Any]) -> list[str]:
    tags = operation.get("tags") or []
    return [t for t in tags if isinstance(t, str)]


def _path_tags(path_item: dict[str, Any]) -> set[str]:
    """Union of tags across all HTTP operations on a path item."""
    tags: set[str] = set()
    for key, op in path_item.items():
        # OpenAPI methods + a few path-level fields. We only care about
        # method entries (objects with `operationId`/`tags`).
        if isinstance(op, dict) and ("tags" in op or "operationId" in op):
            tags.update(_operation_tags(op))
    return tags


def _is_internal_operation(operation: Any) -> bool:
    """Whether an operation carries warp-server's ``x-internal: true`` marker."""
    return isinstance(operation, dict) and operation.get(INTERNAL_MARKER) is True


def _prune_internal(node: Any) -> Any:
    """Recursively drop any object marked ``x-internal: true``, then recurse
    into whatever remains.

    Mirrors openapi-format's ``flagValues: [x-internal: true]`` semantics
    (warp-server's ``public_api/public-openapi-filter.yaml``): the entire
    marked node is deleted, not just the marker key. This catches internal
    schema properties (e.g. ``factory_uid``, ``agent_type``) and internal
    parameters (e.g. the ``automation_id`` query parameter) wherever they
    appear in the tree — not only the top-level path operations that
    ``strip_internal_operations`` inspects. Stripping only the marker key
    (see ``_strip_flags``) would otherwise leave the internal object itself,
    just unmarked, in the published spec.
    """
    if isinstance(node, dict):
        return {
            key: _prune_internal(value)
            for key, value in node.items()
            if not _is_internal_operation(value)
        }
    if isinstance(node, list):
        return [
            _prune_internal(item)
            for item in node
            if not _is_internal_operation(item)
        ]
    return node


def strip_internal_operations(path_item: dict[str, Any]) -> dict[str, Any]:
    """Return ``path_item`` without any operation marked ``x-internal: true``.

    Non-operation keys (``parameters``, ``summary``, ``servers``, ...) are
    preserved so a partially-internal path keeps its shared metadata.
    """
    return {
        key: value
        for key, value in path_item.items()
        if not (key.lower() in HTTP_METHODS and _is_internal_operation(value))
    }


def _has_public_operation(path_item: dict[str, Any]) -> bool:
    """Whether a path item still declares at least one non-internal operation."""
    return any(
        key.lower() in HTTP_METHODS and not _is_internal_operation(value)
        for key, value in path_item.items()
    )


def _should_keep_path(path: str, path_item: dict[str, Any]) -> bool:
    if path in EXCLUDED_PATHS:
        return False
    if path.startswith(EXCLUDED_PATH_PREFIXES):
        return False
    tags = _path_tags(path_item)
    if tags and tags.issubset(EXCLUDED_TAGS):
        return False
    # A path whose every operation is marked internal has no public surface.
    if not _has_public_operation(path_item):
        return False
    return True


def _strip_flags(node: Any) -> Any:
    """Recursively remove every key in ``STRIP_FLAGS`` from ``node``.

    These extensions can appear anywhere in the spec (operations, schemas,
    individual properties, parameters), not only on the operation objects
    that ``strip_internal_operations`` already inspects, so this walks the
    entire tree rather than a fixed set of levels.
    """
    if isinstance(node, dict):
        return {
            key: _strip_flags(value)
            for key, value in node.items()
            if key not in STRIP_FLAGS
        }
    if isinstance(node, list):
        return [_strip_flags(item) for item in node]
    return node


def _collect_refs(node: Any, refs: set[tuple[str, str]]) -> None:
    """Recursively collect every ``(section, name)`` component ref in ``node``.

    Walks dicts and lists, picking up any string under a ``$ref`` key that
    points into ``#/components/<section>/<name>``. Captures refs nested
    anywhere (allOf/oneOf/anyOf, items, additionalProperties, a shared
    response under an operation's ``responses``, etc.).
    """
    if isinstance(node, dict):
        for k, v in node.items():
            if k == "$ref" and isinstance(v, str) and v.startswith("#/components/"):
                section, _, name = v[len("#/components/") :].partition("/")
                if section and name:
                    refs.add((section, name))
            else:
                _collect_refs(v, refs)
    elif isinstance(node, list):
        for item in node:
            _collect_refs(item, refs)


def _reachable_components(
    seed_refs: set[tuple[str, str]], components: dict[str, Any]
) -> set[tuple[str, str]]:
    """Closure of ``seed_refs`` under transitive $ref edges in ``components``.

    Component entries reference each other across sections — a shared
    response $refs a schema, a schema $refs another schema — so the walk
    has to follow every section, not just ``schemas``.
    """
    reachable: set[tuple[str, str]] = set()
    pending = list(seed_refs)
    while pending:
        ref = pending.pop()
        if ref in reachable:
            continue
        reachable.add(ref)
        section, name = ref
        entry = (components.get(section) or {}).get(name)
        if entry is None:
            # Dangling ref — skip silently. _validate_output surfaces it
            # before apply mode writes anything.
            continue
        new_refs: set[tuple[str, str]] = set()
        _collect_refs(entry, new_refs)
        pending.extend(r for r in new_refs if r not in reachable)
    return reachable


def _validate_output(out: dict[str, Any]) -> list[str]:
    """Return human-readable errors for any unresolved refs in ``out``.

    Walks the entire output tree and verifies that every ``$ref`` string
    points at something that actually exists in the output's components
    section. This catches cases where pruning or filtering leaves a
    dangling reference behind — a class of bug that would otherwise slip
    past `npm run build` (Astro just YAML-parses the file) and only
    surface as an empty schema box at runtime in Scalar.
    """
    components = out.get("components") or {}
    available: dict[str, set[str]] = {}
    for ck, cv in components.items():
        if isinstance(cv, dict):
            available[ck] = set(cv.keys())

    errors: list[str] = []

    def visit(node: Any, path: str) -> None:
        if isinstance(node, dict):
            for k, v in node.items():
                if k == "$ref" and isinstance(v, str):
                    if v.startswith("#/components/"):
                        parts = v[len("#/components/") :].split("/", 1)
                        if len(parts) != 2:
                            errors.append(f"{path}: malformed $ref `{v}`")
                            continue
                        section, name = parts
                        if name not in available.get(section, set()):
                            errors.append(
                                f"{path}: $ref `{v}` is not defined in components.{section}"
                            )
                else:
                    visit(v, f"{path}.{k}")
        elif isinstance(node, list):
            for i, item in enumerate(node):
                visit(item, f"{path}[{i}]")

    visit(out, "")
    return errors


def transform(source: dict[str, Any]) -> dict[str, Any]:
    """Produce the docs subset of the given source spec."""
    # Drop every x-internal-marked object (schema properties, parameters,
    # operations, tags, ...) before anything else, so a downstream pass never
    # sees an internal node it would otherwise have to know how to filter.
    source = _prune_internal(source)

    out: dict[str, Any] = {}

    for top_key in ("openapi", "info", "servers"):
        if top_key in source:
            out[top_key] = source[top_key]

    src_tags = source.get("tags") or []
    out_tags = [
        t
        for t in src_tags
        if isinstance(t, dict) and t.get("name") not in EXCLUDED_TAGS
    ]
    if out_tags:
        out["tags"] = out_tags

    src_paths = source.get("paths") or {}
    kept_paths = {
        path: strip_internal_operations(item)
        for path, item in src_paths.items()
        if isinstance(item, dict) and _should_keep_path(path, item)
    }
    out["paths"] = kept_paths

    seed_refs: set[tuple[str, str]] = set()
    _collect_refs(kept_paths, seed_refs)

    src_components = source.get("components") or {}
    reachable = _reachable_components(seed_refs, src_components)

    out_components: dict[str, Any] = {}
    for ck, cv in src_components.items():
        if ck in PRUNABLE_COMPONENT_SECTIONS and isinstance(cv, dict):
            kept = {
                name: entry for name, entry in cv.items() if (ck, name) in reachable
            }
            if kept:
                out_components[ck] = kept
        else:
            out_components[ck] = cv
    if out_components:
        out["components"] = out_components

    return _strip_flags(out)


# ---------------------------------------------------------------------------
# Diff reporting
# ---------------------------------------------------------------------------


def _summarize_drift(
    expected: dict[str, Any], actual: dict[str, Any]
) -> list[str]:
    """Return human-readable lines describing how ``actual`` drifts from ``expected``.

    ``expected`` is what the target *should* look like (i.e., the result of
    transforming the source). ``actual`` is the file currently on disk.
    """
    notes: list[str] = []

    exp_paths = set((expected.get("paths") or {}).keys())
    act_paths = set((actual.get("paths") or {}).keys())

    missing_paths = sorted(exp_paths - act_paths)
    extra_paths = sorted(act_paths - exp_paths)

    if missing_paths:
        notes.append("Paths present in source but missing from target:")
        notes.extend(f"  + {p}" for p in missing_paths)
    if extra_paths:
        notes.append("Paths present in target but absent from source subset:")
        notes.extend(f"  - {p}" for p in extra_paths)

    common_paths = exp_paths & act_paths
    changed_paths = sorted(p for p in common_paths if expected["paths"][p] != actual["paths"][p])
    if changed_paths:
        notes.append("Paths whose operations differ between source and target:")
        notes.extend(f"  ~ {p}" for p in changed_paths)

    # Every pruned section is compared, not just `schemas`: a stale entry in
    # `components.responses` (or any other shared section) is drift too, and
    # reporting only schemas let one sit in the target unnoticed.
    exp_components = expected.get("components") or {}
    act_components = actual.get("components") or {}
    for section in sorted(PRUNABLE_COMPONENT_SECTIONS):
        exp_entries = (exp_components.get(section) or {})
        act_entries = (act_components.get(section) or {})
        exp_names = set(exp_entries.keys())
        act_names = set(act_entries.keys())
        label = "Schemas" if section == "schemas" else f"Component {section}"

        missing = sorted(exp_names - act_names)
        extra = sorted(act_names - exp_names)
        if missing:
            notes.append(f"{label} present in source subset but missing from target:")
            notes.extend(f"  + {name}" for name in missing)
        if extra:
            notes.append(f"{label} present in target but absent from source subset:")
            notes.extend(f"  - {name}" for name in extra)

        changed = sorted(
            name
            for name in exp_names & act_names
            if exp_entries[name] != act_entries[name]
        )
        if changed:
            notes.append(
                f"{label} whose definitions differ between source subset and target:"
            )
            notes.extend(f"  ~ {name}" for name in changed)

    for top_key in ("openapi", "info", "servers"):
        if expected.get(top_key) != actual.get(top_key):
            notes.append(f"Top-level `{top_key}` differs between source and target.")

    return notes


def _unknown_classifications(source: dict[str, Any]) -> list[str]:
    """Flag tags or paths the policy doesn't already cover.

    The skill's policy currently knows about the `agent` and `schedules`
    tags (kept) and `memory_stores`/`harness-support` (dropped). Anything
    else needs human triage.
    """
    KNOWN_TAGS = {"agent", "schedules"} | set(EXCLUDED_TAGS)

    notes: list[str] = []
    for tag in source.get("tags") or []:
        name = tag.get("name") if isinstance(tag, dict) else None
        if name and name not in KNOWN_TAGS:
            notes.append(
                f"Unknown tag `{name}` — extend EXCLUDED_TAGS or document it as public."
            )

    for path, item in (source.get("paths") or {}).items():
        if not isinstance(item, dict):
            continue
        tags = _path_tags(item)
        unknown = tags - KNOWN_TAGS
        if unknown:
            notes.append(
                f"Path `{path}` has unknown tag(s) {sorted(unknown)} — triage before next sync."
            )
    return notes


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------


def _self_test() -> int:
    """Sanity-check the transform on a small synthetic spec."""
    sample = {
        "openapi": "3.0.0",
        "info": {"title": "t", "version": "1"},
        "tags": [
            {"name": "agent"},
            {"name": "memory_stores", "x-internal": True},
            {"name": "harness-support"},
        ],
        "paths": {
            "/agent/run": {
                "post": {
                    "tags": ["agent"],
                    "operationId": "runAgent",
                    "x-stainless-deprecation-message": "use /agent/runs instead",
                    "parameters": [
                        {
                            "name": "conversation_id",
                            "in": "query",
                            "schema": {"type": "string"},
                        },
                        {
                            "name": "factory_uid",
                            "in": "query",
                            "x-internal": True,
                            "schema": {"type": "string"},
                        },
                    ],
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/RunReq"}
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "ok",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/RunResp"}
                                }
                            },
                        },
                        "401": {"$ref": "#/components/responses/Unauthorized"},
                    },
                }
            },
            "/memory_stores": {
                "post": {
                    "tags": ["memory_stores"],
                    "operationId": "createMS",
                    "x-internal": True,
                    "responses": {"201": {"description": "ok"}},
                }
            },
            "/harness-support/transcript": {
                "get": {
                    "tags": ["harness-support"],
                    "operationId": "transcript",
                    "responses": {"200": {"description": "ok"}},
                }
            },
            "/agent/runs/{runId}/followups": {
                "post": {
                    "tags": ["agent"],
                    "operationId": "followups",
                    "responses": {"200": {"description": "ok"}},
                }
            },
        },
        "components": {
            "securitySchemes": {"bearerAuth": {"type": "http", "scheme": "bearer"}},
            "responses": {
                # Referenced by a surviving operation, and pulls a schema of
                # its own into the output.
                "Unauthorized": {
                    "description": "auth required",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/Err"}
                        }
                    },
                },
                # Referenced only by dropped Factory paths.
                "FactoryAccessDenied": {"description": "factory access denied"},
            },
            "schemas": {
                "RunReq": {
                    "type": "object",
                    "x-go-type": "models.RunReq",
                    "x-go-type-import": {"path": "warp.dev/warp-server/models"},
                    "properties": {
                        "config": {"$ref": "#/components/schemas/Config"}
                    },
                },
                "Config": {
                    "type": "object",
                    "properties": {
                        "modes": {
                            "type": "array",
                            "items": {"$ref": "#/components/schemas/Mode"},
                        },
                        "merged": {
                            "allOf": [
                                {"$ref": "#/components/schemas/Mode"},
                                {"type": "object"},
                            ]
                        },
                        "legacy_mode": {
                            "type": "string",
                            "x-go-type-skip-optional-pointer": True,
                            "x-oapi-codegen-extra-tags": {"json": "legacy_mode,omitempty"},
                        },
                        "factory_agent_type": {
                            "allOf": [{"$ref": "#/components/schemas/Mode"}],
                            "x-internal": True,
                        },
                    },
                },
                "Mode": {
                    "type": "string",
                    "x-enum-varnames": ["ModeFast", "ModeSlow"],
                    "x-stainless-naming": {"typescript": {"type": "Mode"}},
                },
                "RunResp": {"type": "object"},
                "Err": {"type": "object"},  # only reachable via a shared response
                "MSItem": {"type": "object"},  # only referenced by dropped path
                "Followup": {"type": "object"},
            },
        },
    }

    out = transform(sample)
    paths = set(out["paths"].keys())
    assert paths == {
        "/agent/run",
        "/agent/runs/{runId}/followups",
    }, f"unexpected paths: {paths}"

    schemas = set(out["components"]["schemas"].keys())
    # Config and Mode are reachable transitively (allOf, items); Err only
    # through the shared Unauthorized response.
    assert schemas == {
        "RunReq",
        "Config",
        "Mode",
        "RunResp",
        "Err",
    }, f"unexpected schemas: {schemas}"

    # Shared components outside `schemas` are pruned the same way, so a
    # response only referenced by a dropped path cannot linger in the
    # published spec.
    responses = set(out["components"]["responses"].keys())
    assert responses == {"Unauthorized"}, f"unexpected responses: {responses}"

    tag_names = [t["name"] for t in out.get("tags") or []]
    assert tag_names == ["agent"], f"unexpected tags: {tag_names}"

    assert out["components"].get("securitySchemes"), "securitySchemes should be preserved"

    ref_errors = _validate_output(out)
    assert not ref_errors, f"unexpected unresolved refs: {ref_errors}"

    # Implementation-only extensions must never survive into the output,
    # regardless of whether they sit on an operation, a schema, or a nested
    # property — mirrors warp-server's `stripFlags` filter.
    dumped = yaml.safe_dump(out)
    for flag in STRIP_FLAGS:
        assert flag not in dumped, f"{flag} leaked into the regenerated spec"
    # The objects that carried those flags must otherwise survive intact.
    assert out["paths"]["/agent/run"]["post"]["operationId"] == "runAgent"
    assert out["components"]["schemas"]["RunReq"]["type"] == "object"
    assert out["components"]["schemas"]["Config"]["properties"]["legacy_mode"][
        "type"
    ] == "string"

    # An x-internal-marked object must be dropped entirely, not just have its
    # marker key stripped — covers an internal query parameter and an
    # internal schema property, alongside the surviving public sibling in
    # each case.
    run_params = {
        p["name"] for p in out["paths"]["/agent/run"]["post"]["parameters"]
    }
    assert run_params == {"conversation_id"}, f"unexpected parameters: {run_params}"
    config_props = set(out["components"]["schemas"]["Config"]["properties"].keys())
    assert "factory_agent_type" not in config_props, (
        f"internal property survived: {config_props}"
    )
    assert "legacy_mode" in config_props, f"public property dropped: {config_props}"

    print("self-test: OK")
    return 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else (Path.cwd() / path).resolve()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument(
        "--mode",
        choices=("diff", "apply", "self-test"),
        required=True,
        help="diff: print drift; apply: write target; self-test: in-memory test.",
    )
    parser.add_argument(
        "--source",
        type=Path,
        default=DEFAULT_SOURCE,
        help="Path to warp-server's public_api/openapi.yaml.",
    )
    parser.add_argument(
        "--target",
        type=Path,
        default=DEFAULT_TARGET,
        help="Path to docs' developers/agent-api-openapi.yaml.",
    )
    args = parser.parse_args(argv)

    if args.mode == "self-test":
        return _self_test()

    source_path = _resolve(args.source)
    target_path = _resolve(args.target)

    if not source_path.exists():
        print(f"error: source spec not found at {source_path}", file=sys.stderr)
        return 2

    source = _load_yaml(source_path)
    expected = transform(source)

    unknown = _unknown_classifications(source)

    if args.mode == "diff":
        if not target_path.exists():
            print(f"error: target spec not found at {target_path}", file=sys.stderr)
            return 2
        actual = _load_yaml(target_path)
        notes = _summarize_drift(expected, actual)
        if unknown:
            notes.append("")
            notes.append("Unclassified tags/paths (require human triage):")
            notes.extend(f"  ! {n}" for n in unknown)
        if not notes:
            print("In sync. No changes needed.")
            return 0
        print(f"Drift detected between\n  source: {source_path}\n  target: {target_path}\n")
        print("\n".join(notes))
        return 1

    # apply
    ref_errors = _validate_output(expected)
    if ref_errors:
        print(
            "error: regenerated spec has unresolved $refs. Refusing to write target.",
            file=sys.stderr,
        )
        for err in ref_errors:
            print(f"  {err}", file=sys.stderr)
        return 3

    target_path.parent.mkdir(parents=True, exist_ok=True)
    _dump_yaml(expected, target_path)
    print(f"Wrote {target_path}")
    print("All $refs resolve in the regenerated spec.")
    if unknown:
        print("\nWarning: unclassified items the script auto-included or auto-dropped:")
        for n in unknown:
            print(f"  ! {n}")
        print("Triage these before merging the PR.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
