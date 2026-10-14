#!/usr/bin/env python3
"""Sync the public OpenAPI spec using warp-server's release exporter.

Requires a warp-server checkout with its pinned openapi-format dependency
installed. Public/private decisions and metadata belong in the canonical spec
and public-openapi-filter.yaml, not in a second docs-only transform.

Modes:
  diff       Print structural drift; exit 1 when drift is found.
  apply      Write the canonical export; exit 3 on unresolved local references.
  self-test  Exercise the exporter integration and invalid-reference handling.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any

import yaml


DEFAULT_SERVER_ROOT = Path("../warp-server")
DEFAULT_TARGET = Path("developers/agent-api-openapi.yaml")


def _load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected a YAML mapping at the document root")
    return data


def _validate_output(out: dict[str, Any]) -> list[str]:
    """Return errors for unresolved local JSON references."""
    errors: list[str] = []

    def visit(node: Any, path: str) -> None:
        if isinstance(node, dict):
            for key, value in node.items():
                if key == "$ref" and isinstance(value, str) and value.startswith("#/"):
                    resolved: Any = out
                    try:
                        for part in value[2:].split("/"):
                            part = part.replace("~1", "/").replace("~0", "~")
                            resolved = (
                                resolved[int(part)] if isinstance(resolved, list)
                                else resolved[part]
                            )
                    except (KeyError, IndexError, ValueError, TypeError):
                        errors.append(f"{path}: unresolved $ref `{value}`")
                else:
                    visit(value, f"{path}.{key}")
        elif isinstance(node, list):
            for index, item in enumerate(node):
                visit(item, f"{path}[{index}]")

    visit(out, "")
    return errors


def _summarize_drift(
    expected: dict[str, Any], actual: dict[str, Any]
) -> list[str]:
    """Describe path, reusable-component, and top-level structural drift."""
    notes: list[str] = []

    def compare_entries(label: str, wanted: dict, found: dict) -> None:
        missing = sorted(wanted.keys() - found.keys())
        extra = sorted(found.keys() - wanted.keys())
        changed = sorted(
            key for key in wanted.keys() & found.keys()
            if wanted[key] != found[key]
        )
        if missing:
            notes.append(f"{label} present in source but missing from target:")
            notes.extend(f"  + {key}" for key in missing)
        if extra:
            notes.append(f"{label} present in target but absent from public source:")
            notes.extend(f"  - {key}" for key in extra)
        if changed:
            notes.append(f"{label} whose definitions differ:")
            notes.extend(f"  ~ {key}" for key in changed)

    compare_entries("Paths", expected.get("paths") or {}, actual.get("paths") or {})
    expected_components = expected.get("components") or {}
    actual_components = actual.get("components") or {}
    for section in sorted(expected_components.keys() | actual_components.keys()):
        compare_entries(
            f"Components.{section}",
            expected_components.get(section) or {},
            actual_components.get(section) or {},
        )
    for key in sorted(expected.keys() | actual.keys()):
        if key not in {"paths", "components"} and expected.get(key) != actual.get(key):
            notes.append(f"Top-level `{key}` differs between source and target.")
    return notes


def _self_test(server_root: Path) -> int:
    import test_sync_openapi

    test_sync_openapi.SERVER_ROOT = server_root
    suite = unittest.defaultTestLoader.loadTestsFromModule(test_sync_openapi)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if result.wasSuccessful():
        print("self-test: OK")
        return 0
    return 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument(
        "--mode", choices=("diff", "apply", "self-test"), required=True,
    )
    parser.add_argument(
        "--server-root", type=Path, default=DEFAULT_SERVER_ROOT,
        help="warp-server checkout containing script/generate-public-openapi.",
    )
    parser.add_argument(
        "--source", type=Path,
        help="Source spec; defaults to <server-root>/public_api/openapi.yaml.",
    )
    parser.add_argument("--target", type=Path, default=DEFAULT_TARGET)
    args = parser.parse_args(argv)
    server_root = args.server_root.resolve()
    if args.mode == "self-test":
        return _self_test(server_root)

    source_path = (
        args.source or server_root / "public_api/openapi.yaml"
    ).resolve()
    target_path = args.target.resolve()
    generator = server_root / "script/generate-public-openapi"
    if not source_path.is_file():
        print(f"error: source spec not found at {source_path}", file=sys.stderr)
        return 2
    if not generator.is_file():
        print(f"error: server exporter not found at {generator}", file=sys.stderr)
        return 2

    with tempfile.TemporaryDirectory() as temp_dir:
        generated_path = Path(temp_dir) / "public.yaml"
        try:
            subprocess.run(
                [str(generator), str(generated_path), str(source_path)],
                capture_output=True, text=True, check=True,
            )
            expected = _load_yaml(generated_path)
        except (OSError, ValueError, yaml.YAMLError, subprocess.CalledProcessError) as exc:
            print(f"error: public export failed: {exc}", file=sys.stderr)
            if isinstance(exc, subprocess.CalledProcessError):
                print(exc.stdout, file=sys.stderr)
                print(exc.stderr, file=sys.stderr)
            return 2

        ref_errors = _validate_output(expected)
        if ref_errors:
            print(
                "error: regenerated spec has unresolved $refs. Refusing to write target.",
                file=sys.stderr,
            )
            for error in ref_errors:
                print(f"  {error}", file=sys.stderr)
            return 3

        if args.mode == "diff":
            if not target_path.is_file():
                print(f"error: target spec not found at {target_path}", file=sys.stderr)
                return 2
            actual = _load_yaml(target_path)
            notes = _summarize_drift(expected, actual)
            if not notes:
                print("In sync. No changes needed.")
                return 0
            print(
                f"Drift detected between\n  source: {source_path}\n"
                f"  target: {target_path}\n"
            )
            print("\n".join(notes))
            return 1

        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(generated_path, target_path)
        print(f"Wrote {target_path}")
        print("All $refs resolve in the regenerated spec.")
        return 0


if __name__ == "__main__":
    sys.exit(main())
