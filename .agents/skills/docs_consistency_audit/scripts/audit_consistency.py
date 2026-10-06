#!/usr/bin/env python3
"""Deterministic mechanics for the docs consistency audit.

Models extract claims and adjudicate semantic candidates. This module owns the
reproducible parts of the pipeline: page inventory, evidence validation, typed
normalization, qualifier-aware blocking, fingerprints, lifecycle state,
structured authority adapters, state validation, and benchmark scoring.
"""

from __future__ import annotations

import argparse
import copy
import datetime as dt
import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from collections import defaultdict
from decimal import Decimal
from pathlib import Path
from typing import Any, Iterable
from zoneinfo import ZoneInfo


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
REFERENCES_DIR = SKILL_DIR / "references"
DEFAULT_AUTHORITY_RULES = REFERENCES_DIR / "authority_rules.json"
DEFAULT_SUPPRESSIONS = REFERENCES_DIR / "suppressions.json"
DEFAULT_BENCHMARK = REFERENCES_DIR / "benchmark_cases.json"

SCHEMA_VERSION = 1
EXTRACTOR_VERSION = "1.0.0"
MODEL_CONTRACT_VERSION = "1.0.0"
STATE_BRANCH = "chore/docs-consistency-audit-state"
STATE_PATH = Path(".agents/state/docs_consistency_audit")

FACTUAL_PATTERN = re.compile(
    r"""
    (?:
        \b\d+(?:[.,]\d+)*(?:\s*(?:KB|MB|GB|TB|seconds?|minutes?|hours?|days?))?\b
        |\b(?:free|build|max|business|enterprise|plan|billing|pricing|credit)\b
        |\b(?:security|privacy|retention|telemetry|permission|redaction|training)\b
        |\b(?:default|require(?:s|d)?|support(?:s|ed)?|available|unavailable)\b
        |\b(?:legacy|preview|beta|deprecated|renamed|resolved|end[ -]of[ -]support)\b
        |--[a-z0-9][a-z0-9-]*
        |/(?:api/)?[a-z0-9_{}./:-]+
        |\b(?:GET|POST|PUT|PATCH|DELETE)\b
    )
    """,
    re.IGNORECASE | re.VERBOSE,
)

PLAN_ORDER = {
    "FREE": 0,
    "BUILD": 1,
    "MAX": 2,
    "BUILD_MAX": 2,
    "BUSINESS": 3,
    "SELF_SERVE_BUSINESS_PLAN": 3,
    "ENTERPRISE": 4,
}
QUALIFIER_KEYS = (
    "plans",
    "operating_systems",
    "architectures",
    "shells",
    "versions",
    "install_methods",
    "environments",
    "actors",
    "release_statuses",
)
UNIVERSAL_MARKERS = {"*", "all", "any"}
EXACT_VALUE_TYPES = {
    "boolean",
    "integer",
    "decimal",
    "duration",
    "bytes",
    "plan",
    "ordered-list",
    "enum",
    "path",
    "flag",
    "parameter",
    "version",
    "date",
    "range",
    "support-matrix",
}
PUBLIC_REPOSITORIES = {"warpdotdev/docs", "warpdotdev/warp"}
REPORTABLE_VERDICTS = {"contradiction", "stale", "duplicate-canonical", "gap"}
FINDING_STATES = {"new", "existing", "changed", "resolved"}
VERDICTS = {
    "contradiction",
    "stale",
    "duplicate-canonical",
    "gap",
    "intentional-exception",
    "insufficient-evidence",
    "not-related",
    "delegated",
}


class AuditError(RuntimeError):
    """Raised when a run cannot safely produce lifecycle changes."""


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_json(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical_json(value).encode()).hexdigest()


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()


def source_visibility(source: dict[str, Any]) -> str:
    explicit = source.get("visibility")
    if explicit in {"public", "private"}:
        return explicit
    return "public" if source.get("repository") in PUBLIC_REPOSITORIES else "private"


def normalize_route(route: str) -> str:
    route = "/" + route.strip().lstrip("/")
    if route != "/":
        route = route.rstrip("/")
    return route


def load_verified_redirects(path: Path | None) -> dict[str, str]:
    if not path or not path.exists():
        return {}
    document = load_json(path)
    redirects: dict[str, str] = {}
    for item in document.get("redirects", []):
        source = item.get("source")
        destination = item.get("destination")
        if not isinstance(source, str) or not isinstance(destination, str):
            continue
        if "://" in destination:
            continue
        if any(token in source for token in (":", "*", "(", "{")):
            continue
        redirects[normalize_route(source)] = normalize_route(destination)
    return redirects


def canonical_redirect_route(route: str, redirects: dict[str, str]) -> str | None:
    current = normalize_route(route)
    destinations = set(redirects.values())
    if current not in redirects and current not in destinations:
        return None
    seen = set()
    while current in redirects:
        if current in seen:
            raise AuditError(f"Redirect cycle detected at {current}")
        seen.add(current)
        current = redirects[current]
    return current


def apply_redirect_identity(
    claim: dict[str, Any],
    redirects: dict[str, str],
) -> dict[str, Any]:
    claim = copy.deepcopy(claim)
    source = claim["source"]
    canonical_route = canonical_redirect_route(source.get("route", ""), redirects)
    if canonical_route:
        source["canonical_route"] = canonical_route
        source["canonical_identity"] = f"route:{canonical_route}"
    else:
        source["canonical_identity"] = f"path:{source['path']}"
    return claim


def validate_public_claim(claim: dict[str, Any]) -> None:
    source = claim["source"]
    if (
        source.get("repository") not in PUBLIC_REPOSITORIES
        or source_visibility(source) != "public"
    ):
        raise AuditError("Private evidence cannot be persisted as a claim")


def load_json(path: Path, default: Any = None) -> Any:
    if not path.exists():
        if default is not None:
            return copy.deepcopy(default)
        raise AuditError(f"Required JSON file is missing: {path}")
    try:
        return json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        raise AuditError(f"Cannot parse JSON file {path}: {exc}") from exc


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def git_value(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode:
        raise AuditError(f"git {' '.join(args)} failed for {repo}: {result.stderr.strip()}")
    return result.stdout.strip()


def repo_ref(repo: Path) -> dict[str, str]:
    if not (repo / ".git").exists():
        raise AuditError(f"Required Git repository is missing: {repo}")
    return {
        "path": str(repo),
        "commit": git_value(repo, "rev-parse", "HEAD"),
        "branch": git_value(repo, "rev-parse", "--abbrev-ref", "HEAD"),
    }


def stable_heading_anchor(heading: str) -> str:
    value = heading.strip().lower()
    value = re.sub(r"[`*_~]", "", value)
    value = re.sub(r"[^\w\s-]", "", value)
    return re.sub(r"[-\s]+", "-", value).strip("-")


def parse_frontmatter_title(lines: list[str], fallback: str) -> str:
    if not lines or lines[0].strip() != "---":
        return fallback
    for line in lines[1:]:
        if line.strip() == "---":
            break
        match = re.match(r"title:\s*[\"']?(.*?)[\"']?\s*$", line)
        if match:
            return match.group(1)
    return fallback


def page_route(path: Path, docs_root: Path) -> str:
    relative = path.relative_to(docs_root).with_suffix("")
    parts = list(relative.parts)
    if parts and parts[-1] in {"index", "README"}:
        parts.pop()
    return "/" + "/".join(parts) + ("/" if parts else "")


def page_role(relative: str) -> str:
    lower = relative.lower()
    if "faq" in lower:
        return "faq"
    if "migration" in lower or "migrat" in lower:
        return "migration"
    if "/reference/" in f"/{lower}" or lower.startswith("reference/"):
        return "reference"
    if lower.endswith("index.mdx") or lower.endswith("index.md"):
        return "canonical-overview"
    return "docs-prose"


def is_excluded(relative: str, rules: dict[str, Any]) -> bool:
    normalized = relative.replace(os.sep, "/")
    for pattern in rules.get("inventory", {}).get("excluded_globs", []):
        if Path(normalized).match(pattern):
            return True
    excluded = set(rules.get("inventory", {}).get("excluded_paths", []))
    excluded.update(rules.get("inventory", {}).get("historical_migration_allowlist", []))
    return normalized in excluded


def split_sections(lines: list[str]) -> list[dict[str, Any]]:
    headings: list[tuple[int, str, str]] = []
    for index, line in enumerate(lines, 1):
        match = re.match(r"^(#{1,4})\s+(.+?)\s*$", line)
        if match:
            heading = re.sub(r"\s+\{#.*?\}\s*$", "", match.group(2))
            headings.append((index, heading, stable_heading_anchor(heading)))
    if not headings:
        return [{
            "heading": "",
            "anchor": "",
            "line_start": 1,
            "line_end": len(lines),
            "text": "\n".join(lines),
        }]
    sections: list[dict[str, Any]] = []
    body_start = 1
    if lines and lines[0].strip() == "---":
        for index, line in enumerate(lines[1:], 2):
            if line.strip() == "---":
                body_start = index + 1
                break
    first_heading_line = headings[0][0]
    if first_heading_line > body_start:
        preamble = "\n".join(lines[body_start - 1:first_heading_line - 1])
        if preamble.strip():
            sections.append({
                "heading": "",
                "anchor": "",
                "line_start": body_start,
                "line_end": first_heading_line - 1,
                "text": preamble,
            })
    for position, (start, heading, anchor) in enumerate(headings):
        end = headings[position + 1][0] - 1 if position + 1 < len(headings) else len(lines)
        sections.append({
            "heading": heading,
            "anchor": anchor,
            "line_start": start,
            "line_end": end,
            "text": "\n".join(lines[start - 1:end]),
        })
    return sections


def inventory_pages(
    docs_root: Path,
    authority_rules: dict[str, Any],
    previous_manifest: dict[str, Any] | None = None,
    full: bool = False,
    path_prefix: str = "",
) -> dict[str, Any]:
    pages: dict[str, Any] = {}
    previous_pages = (previous_manifest or {}).get("pages", {})
    for path in sorted((*docs_root.rglob("*.md"), *docs_root.rglob("*.mdx"))):
        relative = path.relative_to(docs_root).as_posix()
        if is_excluded(relative, authority_rules):
            continue
        repository_relative = "/".join(part for part in (path_prefix.strip("/"), relative) if part)
        text = path.read_text()
        lines = text.splitlines()
        source_hash = sha256_text(text)
        sections = split_sections(lines)
        pages[repository_relative] = {
            "path": repository_relative,
            "route": page_route(path, docs_root),
            "title": parse_frontmatter_title(lines, path.stem),
            "role": page_role(relative),
            "source_sha256": source_hash,
            "character_count": len(text),
            "headings": [
                {
                    "text": section["heading"],
                    "anchor": section["anchor"],
                    "line_start": section["line_start"],
                }
                for section in sections
            ],
            "candidate_sections": [
                {
                    "heading": section["heading"],
                    "anchor": section["anchor"],
                    "line_start": section["line_start"],
                    "line_end": section["line_end"],
                    "character_count": len(section["text"]),
                }
                for section in sections
                if FACTUAL_PATTERN.search(section["text"])
            ],
        }
        previous = previous_pages.get(repository_relative)
        pages[repository_relative]["extraction_status"] = (
            "invalidated"
            if full
            else "unchanged"
            if previous
            and previous.get("source_sha256") == source_hash
            and previous_manifest.get("extractor_version") == EXTRACTOR_VERSION
            and previous_manifest.get("model_contract_version") == MODEL_CONTRACT_VERSION
            else "changed"
            if previous
            else "new"
        )
    deleted = sorted(set(previous_pages) - set(pages))
    planned = sorted(
        path for path, page in pages.items()
        if page["extraction_status"] != "unchanged"
    )
    return {
        "schema_version": SCHEMA_VERSION,
        "extractor_version": EXTRACTOR_VERSION,
        "model_contract_version": MODEL_CONTRACT_VERSION,
        "pages": pages,
        "changed_pages": planned,
        "deleted_pages": deleted,
        "counts": {
            "pages": len(pages),
            "changed_pages": len(planned),
            "deleted_pages": len(deleted),
            "candidate_sections": sum(len(page["candidate_sections"]) for page in pages.values()),
        },
    }


def inventory_command(args: argparse.Namespace) -> int:
    docs_repo = Path(args.docs_repo).resolve()
    docs_root = docs_repo / args.content_root
    if not docs_root.exists():
        raise AuditError(f"Docs content root is missing: {docs_root}")
    rules = load_json(Path(args.authority_rules))
    previous = load_json(Path(args.previous_manifest), {}) if args.previous_manifest else {}
    inventory = inventory_pages(
        docs_root,
        rules,
        previous,
        args.full,
        path_prefix=args.content_root,
    )
    selected = []
    backlog = []
    selected_characters = 0
    for page in inventory["changed_pages"]:
        characters = inventory["pages"][page]["character_count"]
        page_limit_hit = args.max_pages and len(selected) >= args.max_pages
        character_limit_hit = (
            args.max_characters
            and selected
            and selected_characters + characters > args.max_characters
        )
        if page_limit_hit or character_limit_hit:
            backlog.append(page)
        else:
            selected.append(page)
            selected_characters += characters
    inventory["extraction_plan"] = {
        "selected_pages": selected,
        "backlog_pages": backlog,
        "selected_characters": selected_characters,
        "coverage": "partial" if backlog else "complete",
        "max_pages": args.max_pages,
        "max_characters": args.max_characters,
    }
    inventory["source_repositories"] = {"docs": repo_ref(docs_repo)}
    write_json(Path(args.output), inventory)
    print(canonical_json(inventory["counts"]))
    return 0


def normalize_scalar(value: Any) -> Any:
    if isinstance(value, bool) or value is None:
        return value
    if isinstance(value, (int, float)):
        return value
    text = str(value).strip()
    lower = text.lower()
    if lower in {"true", "enabled", "yes", "supported", "available"}:
        return True
    if lower in {"false", "disabled", "no", "unsupported", "unavailable"}:
        return False
    if text.upper() in PLAN_ORDER:
        aliases = {"BUILD_MAX": "MAX", "SELF_SERVE_BUSINESS_PLAN": "BUSINESS"}
        return aliases.get(text.upper(), text.upper())
    compact = lower.replace(",", "").replace("_", "")
    number_match = re.fullmatch(r"(-?\d+(?:\.\d+)?)\s*([kmgt]?b|seconds?|minutes?|hours?|days?)?", compact)
    if number_match:
        number = Decimal(number_match.group(1))
        unit = (number_match.group(2) or "").lower()
        factors = {
            "kb": Decimal(1000),
            "mb": Decimal(1000**2),
            "gb": Decimal(1000**3),
            "tb": Decimal(1000**4),
            "second": Decimal(1),
            "seconds": Decimal(1),
            "minute": Decimal(60),
            "minutes": Decimal(60),
            "hour": Decimal(3600),
            "hours": Decimal(3600),
            "day": Decimal(86400),
            "days": Decimal(86400),
        }
        number *= factors.get(unit, Decimal(1))
        return int(number) if number == number.to_integral() else str(number.normalize())
    if text.startswith("/"):
        text = re.sub(r":([A-Za-z_][A-Za-z0-9_]*)", r"{\1}", text)
        text = re.sub(r"\{[^}]+\}", "{}", text)
        text = re.sub(r"/{2,}", "/", text)
    return text


def normalize_typed_value(value: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(value, dict) or "type" not in value:
        raise AuditError("Claim value must be an object with a type")
    normalized = copy.deepcopy(value)
    raw = value.get("normalized", value.get("raw"))
    kind = value["type"]
    if kind in {"ordered-list", "enum", "support-matrix"}:
        if not isinstance(raw, list):
            raise AuditError(f"{kind} claim values must be lists")
        normalized["normalized"] = [normalize_scalar(item) for item in raw]
    elif kind == "range":
        if not isinstance(raw, dict):
            raise AuditError("range claim values must be objects")
        normalized["normalized"] = {
            key: normalize_scalar(raw.get(key)) for key in ("minimum", "maximum")
        }
    elif kind == "plan":
        plan = str(raw).upper().replace("-", "_").replace(" ", "_")
        aliases = {"PRO": "BUILD", "BUILD_MAX": "MAX", "SELF_SERVE_BUSINESS_PLAN": "BUSINESS"}
        normalized["normalized"] = aliases.get(plan, plan)
    else:
        normalized["normalized"] = normalize_scalar(raw)
    return normalized


def normalize_qualifiers(qualifiers: dict[str, Any] | None) -> dict[str, Any]:
    qualifiers = copy.deepcopy(qualifiers or {})
    result: dict[str, Any] = {}
    for key in QUALIFIER_KEYS:
        values = qualifiers.get(key, [])
        if isinstance(values, str):
            values = [values]
        result[key] = sorted({str(item).strip().lower() for item in values if str(item).strip()})
    result["legacy"] = bool(qualifiers.get("legacy", False))
    result["time_scope"] = qualifiers.get("time_scope")
    result["exceptions"] = sorted({
        str(item).strip().lower()
        for item in qualifiers.get("exceptions", [])
        if str(item).strip()
    })
    return result


def qualifier_dimension_compatible(left: list[str], right: list[str]) -> bool:
    if not left or not right:
        return True
    left_set, right_set = set(left), set(right)
    if left_set & UNIVERSAL_MARKERS or right_set & UNIVERSAL_MARKERS:
        return True
    return bool(left_set & right_set)


def exception_matches_scope(broad: dict[str, Any], narrow: dict[str, Any]) -> bool:
    exceptions = broad["exceptions"]
    if not exceptions:
        return False
    specific_values = {
        value
        for key in QUALIFIER_KEYS
        if narrow[key] and not set(narrow[key]) & UNIVERSAL_MARKERS
        for value in narrow[key]
    }
    return any(
        exception == value
        or exception.startswith(value + "-")
        or exception.endswith("-" + value)
        for exception in exceptions
        for value in specific_values
    )


def qualifier_compatibility(
    left: dict[str, Any],
    right: dict[str, Any],
) -> tuple[bool, list[str], bool]:
    left = normalize_qualifiers(left)
    right = normalize_qualifiers(right)
    conflicts = [
        key for key in QUALIFIER_KEYS
        if not qualifier_dimension_compatible(left[key], right[key])
    ]
    if left["legacy"] != right["legacy"] and not (left["legacy"] is False and right["legacy"] is False):
        conflicts.append("legacy")
    if left["time_scope"] and right["time_scope"] and left["time_scope"] != right["time_scope"]:
        conflicts.append("time_scope")
    universal_specific = any(
        (not left[key] or set(left[key]) & UNIVERSAL_MARKERS)
        != (not right[key] or set(right[key]) & UNIVERSAL_MARKERS)
        for key in QUALIFIER_KEYS
    )
    if universal_specific:
        left_is_broad = all(
            not left[key] or bool(set(left[key]) & UNIVERSAL_MARKERS)
            for key in QUALIFIER_KEYS
        )
        right_is_broad = all(
            not right[key] or bool(set(right[key]) & UNIVERSAL_MARKERS)
            for key in QUALIFIER_KEYS
        )
        if (
            left_is_broad
            and exception_matches_scope(left, right)
            or right_is_broad
            and exception_matches_scope(right, left)
        ):
            conflicts.append("explicit-exception")
    return not conflicts, conflicts, universal_specific


def claim_identity_payload(claim: dict[str, Any]) -> dict[str, Any]:
    source = claim["source"]
    return {
        "repository": source["repository"],
        "source_identity": source.get("canonical_identity", f"path:{source['path']}"),
        "heading_anchor": source.get("heading_anchor") or stable_heading_anchor(source.get("heading", "")),
        "topic": claim["topic"],
        "entity": claim["entity"],
        "predicate": claim["predicate"],
        "qualifier_key": normalize_qualifiers(claim.get("qualifiers")),
    }


def normalize_claim(claim: dict[str, Any]) -> dict[str, Any]:
    required = {
        "source", "topic", "entity", "predicate", "value", "qualifiers",
        "polarity", "quote", "source_class",
    }
    missing = required - set(claim)
    if missing:
        raise AuditError(f"Claim is missing fields: {', '.join(sorted(missing))}")
    normalized = copy.deepcopy(claim)
    normalized["source"]["visibility"] = source_visibility(normalized["source"])
    normalized["topic"] = re.sub(r"\s+", "-", str(claim["topic"]).strip().lower())
    normalized["entity"] = re.sub(r"\s+", "-", str(claim["entity"]).strip().lower())
    normalized["predicate"] = re.sub(r"\s+", "-", str(claim["predicate"]).strip().lower())
    normalized["value"] = normalize_typed_value(claim["value"])
    normalized["qualifiers"] = normalize_qualifiers(claim["qualifiers"])
    normalized["claim_id"] = sha256_json(claim_identity_payload(normalized))
    normalized["claim_content_fingerprint"] = sha256_json({
        "value": normalized["value"],
        "qualifiers": normalized["qualifiers"],
        "polarity": normalized["polarity"],
        "quote": normalized["quote"],
    })
    return normalized


def validate_claim_quote(claim: dict[str, Any], repository_roots: dict[str, Path]) -> None:
    source = claim["source"]
    repo = source["repository"]
    if repo not in repository_roots:
        raise AuditError(f"No repository root is registered for {repo}")
    path = repository_roots[repo] / source["path"]
    if not path.exists():
        raise AuditError(f"Claim source does not exist: {path}")
    lines = path.read_text().splitlines()
    start, end = int(source["line_start"]), int(source["line_end"])
    if start < 1 or end < start or end > len(lines):
        raise AuditError(f"Invalid claim line range {start}-{end} for {path}")
    excerpt = "\n".join(lines[start - 1:end])
    quote = claim["quote"]
    if quote not in excerpt:
        raise AuditError(f"Claim quote is not an exact source substring: {path}:{start}-{end}")
    expected_hash = source.get("content_sha256")
    if expected_hash and expected_hash != sha256_text(path.read_text()):
        raise AuditError(f"Claim source hash is stale: {path}")


def values_conflict(left: dict[str, Any], right: dict[str, Any]) -> bool:
    left_type = left["value"]["type"]
    right_type = right["value"]["type"]
    if left_type != right_type or left_type not in EXACT_VALUE_TYPES:
        return False
    left_value = left["value"]["normalized"]
    right_value = right["value"]["normalized"]
    if left["polarity"] != right["polarity"] and left_value == right_value:
        return True
    return left_value != right_value


def block_key(claim: dict[str, Any]) -> str:
    return "|".join((claim["topic"], claim["entity"], claim["predicate"]))


def candidate_identity(left: dict[str, Any], right: dict[str, Any]) -> str:
    return sha256_json({
        "block_key": block_key(left),
        "claim_ids": sorted((left["claim_id"], right["claim_id"])),
    })


def authority_rank(
    claim: dict[str, Any],
    authority_rules: dict[str, Any],
) -> tuple[int, str]:
    category = claim.get("category", claim["topic"])
    category_rules = authority_rules.get("categories", {}).get(category, {})
    precedence = category_rules.get(
        "precedence",
        authority_rules.get("default_precedence", []),
    )
    try:
        return precedence.index(claim["source_class"]), claim["source_class"]
    except ValueError:
        return len(precedence) + 100, claim["source_class"]


def generate_candidates(
    claims: Iterable[dict[str, Any]],
    authority_rules: dict[str, Any],
) -> list[dict[str, Any]]:
    blocks: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for claim in claims:
        normalized = normalize_claim(claim)
        blocks[block_key(normalized)].append(normalized)
    candidates: list[dict[str, Any]] = []
    for key, block in sorted(blocks.items()):
        if len(block) < 2:
            continue
        ranked = sorted(block, key=lambda claim: authority_rank(claim, authority_rules))
        best_rank = authority_rank(ranked[0], authority_rules)[0]
        authorities = [claim for claim in ranked if authority_rank(claim, authority_rules)[0] == best_rank]
        peers = [claim for claim in ranked if claim not in authorities]
        pairs: list[tuple[dict[str, Any], dict[str, Any]]] = []
        if peers:
            pairs.extend((authority, peer) for authority in authorities[:1] for peer in peers)
            if len(authorities) > 1:
                pairs.extend(
                    (authorities[index], authorities[index + 1])
                    for index in range(len(authorities) - 1)
                )
        else:
            pairs.extend(
                (ranked[index], ranked[index + 1])
                for index in range(len(ranked) - 1)
            )
        for left, right in pairs:
            compatible, conflicts, universal_specific = qualifier_compatibility(
                left["qualifiers"], right["qualifiers"]
            )
            candidate = {
                "candidate_id": candidate_identity(left, right),
                "block_key": key,
                "left": left,
                "right": right,
                "qualifiers_compatible": compatible,
                "qualifier_conflicts": conflicts,
                "universal_specific": universal_specific,
                "exact_typed_mismatch": compatible and values_conflict(left, right),
                "authority": left["source_class"],
            }
            if compatible:
                candidates.append(candidate)
    return candidates


def finding_identity_payload(finding: dict[str, Any]) -> dict[str, Any]:
    return {
        "category": finding["category"],
        "topic": finding["topic"],
        "entity": finding["entity"],
        "predicate": finding["predicate"],
        "claims": sorted(claim["claim_id"] for claim in finding["claims"]),
    }


def normalize_finding(finding: dict[str, Any]) -> dict[str, Any]:
    normalized = copy.deepcopy(finding)
    normalized["claims"] = [normalize_claim(claim) for claim in finding["claims"]]
    normalized["finding_id"] = sha256_json(finding_identity_payload(normalized))
    normalized["finding_content_fingerprint"] = sha256_json({
        "claim_content_fingerprints": sorted(
            claim["claim_content_fingerprint"] for claim in normalized["claims"]
        ),
        "canonical_source": normalized.get("canonical_source"),
        "severity": normalized["severity"],
        "confidence": normalized["confidence"],
        "rationale_class": normalized.get("rationale_class", normalized.get("verdict")),
        "suggested_resolution_class": normalized.get("suggested_resolution_class"),
    })
    return normalized


def calculate_lifecycle(
    current_findings: Iterable[dict[str, Any]],
    previous_state: dict[str, Any],
    run_id: str,
    complete: bool,
) -> dict[str, Any]:
    previous = previous_state.get("findings", {})
    current = {finding["finding_id"]: finding for finding in map(normalize_finding, current_findings)}
    result: dict[str, Any] = {}
    changes: list[dict[str, Any]] = []
    for finding_id, finding in current.items():
        old = previous.get(finding_id)
        reopened = bool(old and old.get("status") == "resolved")
        if not old:
            lifecycle = "new"
        elif reopened or old.get("finding_content_fingerprint") != finding["finding_content_fingerprint"]:
            lifecycle = "changed"
        else:
            lifecycle = "existing"
        finding.update({
            "lifecycle": lifecycle,
            "reopened": reopened,
            "status": "active",
            "first_seen_run": old.get("first_seen_run", run_id) if old else run_id,
            "last_seen_run": run_id,
        })
        result[finding_id] = finding
        if lifecycle != "existing":
            changes.append(finding)
    for finding_id, old in previous.items():
        if finding_id in current:
            continue
        carried = copy.deepcopy(old)
        if not complete:
            carried["lifecycle"] = "existing"
            carried["status"] = old.get("status", "active")
            carried["carried_forward_due_to_incomplete_run"] = True
            result[finding_id] = carried
            continue
        if old.get("status") == "active":
            carried.update({
                "lifecycle": "resolved",
                "status": "resolved",
                "resolved_run": run_id,
                "last_seen_run": run_id,
            })
            changes.append(carried)
        result[finding_id] = carried
    return {"findings": result, "changes": changes}


def suppression_matches(finding: dict[str, Any], suppression: dict[str, Any]) -> bool:
    if suppression.get("finding_id") == finding["finding_id"]:
        return True
    matcher = suppression.get("matcher", {})
    return bool(matcher) and all(finding.get(key) == value for key, value in matcher.items())


def apply_suppressions(
    findings: Iterable[dict[str, Any]],
    suppressions: dict[str, Any],
    today: dt.date,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    active, suppressed, expired = [], [], []
    for finding in findings:
        match = next(
            (
                item for item in suppressions.get("suppressions", [])
                if suppression_matches(finding, item)
            ),
            None,
        )
        if not match:
            active.append(finding)
            continue
        expiry = dt.date.fromisoformat(match["expires"])
        if expiry < today:
            finding = copy.deepcopy(finding)
            finding["expired_suppression"] = match["id"]
            expired.append(finding)
            active.append(finding)
        else:
            finding = copy.deepcopy(finding)
            finding["suppression_id"] = match["id"]
            suppressed.append(finding)
    return active, suppressed, expired


def parse_simple_tier_yaml(path: Path) -> dict[str, Any]:
    result: dict[str, Any] = {"policies": {}}
    current_feature = None
    in_policy = False
    for raw_line in path.read_text().splitlines():
        line = raw_line.split("#", 1)[0].rstrip()
        if not line:
            continue
        if match := re.match(r"^(id|name|extends):\s*[\"']?(.+?)[\"']?$", line):
            result[match.group(1)] = match.group(2)
        elif match := re.match(r"^\s*-\s+feature_type:\s*(\S+)", line):
            current_feature = match.group(1)
            result["policies"].setdefault(current_feature, {})
            in_policy = False
        elif current_feature and re.match(r"^\s+feature_policy:\s*$", line):
            in_policy = True
        elif current_feature and in_policy and (
            match := re.match(r"^\s+([a-zA-Z0-9_]+):\s*[\"']?(.+?)[\"']?$", line)
        ):
            result["policies"][current_feature][match.group(1)] = normalize_scalar(match.group(2))
    return result


def effective_tier(path: Path, cache: dict[Path, dict[str, Any]]) -> dict[str, Any]:
    if path in cache:
        return cache[path]
    parsed = parse_simple_tier_yaml(path)
    parent_name = parsed.get("extends")
    if parent_name:
        parent = effective_tier(path.parent / parent_name, cache)
        effective = copy.deepcopy(parent)
        effective.update({key: value for key, value in parsed.items() if key != "policies"})
        for feature, policy in parsed["policies"].items():
            effective["policies"].setdefault(feature, {}).update(policy)
    else:
        effective = parsed
    cache[path] = effective
    return effective


def load_missing_docs_module(docs_repo: Path):
    module_path = docs_repo / ".agents/skills/missing_docs/scripts/audit_docs.py"
    if not module_path.exists():
        raise AuditError(f"missing_docs extractor is unavailable: {module_path}")
    spec = importlib.util.spec_from_file_location("missing_docs_audit", module_path)
    if not spec or not spec.loader:
        raise AuditError(f"Cannot load missing_docs extractor: {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def authority_record(
    *,
    topic: str,
    entity: str,
    predicate: str,
    value: dict[str, Any],
    qualifiers: dict[str, Any],
    source_class: str,
    visibility: str,
    release_scope: str,
    repository: str,
    path: str,
    source_commit: str,
    evidence_hash: str,
) -> dict[str, Any]:
    record = {
        "topic": topic,
        "entity": entity,
        "predicate": predicate,
        "value": normalize_typed_value(value),
        "qualifiers": normalize_qualifiers(qualifiers),
        "source_class": source_class,
        "visibility": visibility,
        "release_scope": release_scope,
        "source_ref": {
            "repository": repository,
            "path": path,
            "commit": source_commit,
        },
        "evidence_hash": evidence_hash,
    }
    record["authority_id"] = sha256_json(record)
    return record


def validate_authority_contract(document: dict[str, Any]) -> list[dict[str, Any]]:
    records = document.get("authority_records")
    if not isinstance(records, list):
        raise AuditError("Authority contract must contain an authority_records list")
    normalized = []
    required = {
        "authority_id",
        "topic",
        "entity",
        "predicate",
        "value",
        "qualifiers",
        "source_class",
        "visibility",
        "release_scope",
        "source_ref",
        "evidence_hash",
    }
    for record in records:
        missing = required - set(record)
        if missing:
            raise AuditError(
                "Authority record is missing fields: " + ", ".join(sorted(missing))
            )
        if record["visibility"] not in {"public", "private"}:
            raise AuditError("Authority visibility must be public or private")
        if not record["release_scope"]:
            raise AuditError("Authority release_scope cannot be empty")
        source_ref = record["source_ref"]
        if (
            not isinstance(source_ref, dict)
            or not all(
                source_ref.get(field)
                for field in ("repository", "path", "commit")
            )
        ):
            raise AuditError("Authority source_ref requires repository, path, and commit")
        if (
            record["visibility"] == "public"
            and source_ref["repository"] not in PUBLIC_REPOSITORIES
        ):
            raise AuditError("Public authority records require a public repository")
        if not record["evidence_hash"]:
            raise AuditError("Authority evidence_hash cannot be empty")
        normalized_record = copy.deepcopy(record)
        normalized_record["value"] = normalize_typed_value(record["value"])
        normalized_record["qualifiers"] = normalize_qualifiers(record["qualifiers"])
        expected_id = sha256_json({
            key: normalized_record[key]
            for key in normalized_record
            if key != "authority_id"
        })
        if expected_id != record["authority_id"]:
            raise AuditError(f"Authority fingerprint mismatch: {record['authority_id']}")
        normalized.append(normalized_record)
    return normalized


def public_authority_dto(record: dict[str, Any]) -> dict[str, Any]:
    result = {
        "source_class": record["source_class"],
        "visibility": record["visibility"],
        "release_scope": record["release_scope"],
        "evidence_available": True,
    }
    if record["visibility"] == "public":
        result["authority_id"] = record["authority_id"]
        result["value"] = record["value"]
        result["source_ref"] = record["source_ref"]
    return result


def matching_authorities(
    candidate: dict[str, Any],
    records: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    left = candidate["left"]
    matches = []
    for record in records:
        if (
            record["topic"],
            record["entity"],
            record["predicate"],
        ) != (left["topic"], left["entity"], left["predicate"]):
            continue
        if any(
            qualifier_compatibility(record["qualifiers"], claim["qualifiers"])[0]
            for claim in (candidate["left"], candidate["right"])
        ):
            matches.append(record)
    return matches


def authority_adapters(
    docs_repo: Path,
    warp_repo: Path,
    warp_server: Path,
    fetch_pricing: bool = False,
) -> dict[str, Any]:
    missing_docs = load_missing_docs_module(docs_repo)
    public_spec = docs_repo / "developers/agent-api-openapi.yaml"
    server_spec = warp_server / "public_api/openapi.yaml"
    if not public_spec.exists():
        raise AuditError(f"Released public OpenAPI document is missing: {public_spec}")
    tier_dir = warp_server / "billing/config/tiers"
    tier_files = [
        tier_dir / "free.yaml",
        tier_dir / "build.yaml",
        tier_dir / "build_max.yaml",
        tier_dir / "self_serve_business_plan.yaml",
    ]
    if any(not path.exists() for path in tier_files):
        raise AuditError("Required self-serve billing tier configuration is incomplete")
    tier_cache: dict[Path, dict[str, Any]] = {}
    tiers = {
        path.stem: effective_tier(path, tier_cache)
        for path in tier_files
    }
    refs = {
        "docs": repo_ref(docs_repo),
        "warp": repo_ref(warp_repo),
        "warp_server": repo_ref(warp_server),
    }
    commands = missing_docs.parse_cli_commands(warp_repo)
    cli = {
        "commands": commands,
        "flags_by_module": missing_docs.parse_cli_flags(warp_repo, commands),
    }
    public_text = public_spec.read_text()
    api = {
        "released_paths": sorted(missing_docs.parse_openapi_paths(public_text)),
        "released_sha256": sha256_text(public_text),
        "server_sha256": sha256_text(server_spec.read_text()) if server_spec.exists() else None,
        "server_available": server_spec.exists(),
    }
    terminology = docs_repo / ".agents/references/terminology.md"
    variables = docs_repo / "src/data/vars.ts"
    pricing = {"available": False, "fetched_at": None, "sha256": None}
    if fetch_pricing:
        try:
            with urllib.request.urlopen("https://www.warp.dev/pricing", timeout=30) as response:
                pricing_text = response.read().decode()
            pricing = {
                "available": True,
                "fetched_at": dt.datetime.now(dt.timezone.utc).isoformat(),
                "sha256": sha256_text(pricing_text),
            }
        except Exception as exc:
            pricing["error"] = type(exc).__name__
    authority_records = []
    for tier_name, tier in sorted(tiers.items()):
        plan = tier.get("id", tier_name).upper()
        for feature, policy in sorted(tier["policies"].items()):
            for field, value in sorted(policy.items()):
                value_type = (
                    "boolean" if isinstance(value, bool)
                    else "integer" if isinstance(value, int)
                    else "decimal" if isinstance(value, float)
                    else "free-text"
                )
                tier_path = f"billing/config/tiers/{tier_name}.yaml"
                authority_records.append(authority_record(
                    topic="plan-gating",
                    entity=feature.lower().replace("_", "-"),
                    predicate=field.replace("_", "-"),
                    value={"type": value_type, "normalized": value},
                    qualifiers={"plans": [plan]},
                    source_class="effective-billing-policy",
                    visibility="private",
                    release_scope="effective-self-serve",
                    repository="warpdotdev/warp-server",
                    path=tier_path,
                    source_commit=refs["warp_server"]["commit"],
                    evidence_hash=sha256_text((warp_server / tier_path).read_text()),
                ))
    for path in api["released_paths"]:
        authority_records.append(authority_record(
            topic="api",
            entity=path,
            predicate="released",
            value={"type": "boolean", "normalized": True},
            qualifiers={"release_statuses": ["ga"]},
            source_class="released-openapi",
            visibility="public",
            release_scope="released-public-openapi",
            repository="warpdotdev/docs",
            path="developers/agent-api-openapi.yaml",
            source_commit=refs["docs"]["commit"],
            evidence_hash=api["released_sha256"],
        ))
    for command in commands:
        if command["hidden"]:
            continue
        for visible_command in [command["command"], *(
            item["command"] for item in command["subcommands"] if not item["hidden"]
        )]:
            source_path = command.get("source_file") or "crates/warp_cli/src/lib.rs"
            resolved_source = warp_repo / source_path
            authority_records.append(authority_record(
                topic="cli",
                entity=visible_command,
                predicate="visible",
                value={"type": "boolean", "normalized": True},
                qualifiers={"release_statuses": ["ga"]},
                source_class="public-cli-source",
                visibility="public",
                release_scope="visible-ga",
                repository="warpdotdev/warp",
                path=source_path,
                source_commit=refs["warp"]["commit"],
                evidence_hash=(
                    sha256_text(resolved_source.read_text())
                    if resolved_source.exists()
                    else refs["warp"]["commit"]
                ),
            ))
    validate_authority_contract({"authority_records": authority_records})
    return {
        "schema_version": SCHEMA_VERSION,
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "source_repositories": refs,
        "billing_tiers": tiers,
        "public_api": api,
        "cli": cli,
        "terminology": {
            "glossary_sha256": sha256_text(terminology.read_text()),
            "variables_sha256": sha256_text(variables.read_text()),
        },
        "pricing": pricing,
        "authority_records": authority_records,
    }


def adapters_command(args: argparse.Namespace) -> int:
    result = authority_adapters(
        Path(args.docs_repo).resolve(),
        Path(args.warp_repo).resolve(),
        Path(args.warp_server).resolve(),
        args.fetch_pricing,
    )
    write_json(Path(args.output), result)
    print(canonical_json({
        "tiers": len(result["billing_tiers"]),
        "cli_commands": len(result["cli"]["commands"]),
        "api_paths": len(result["public_api"]["released_paths"]),
        "pricing_available": result["pricing"]["available"],
        "authority_records": len(result["authority_records"]),
    }))
    return 0


def validate_state_tree(state_dir: Path) -> list[str]:
    errors: list[str] = []
    manifest_path = state_dir / "manifest.json"
    findings_path = state_dir / "findings.json"
    if not manifest_path.exists():
        errors.append("manifest.json is missing")
        return errors
    if not findings_path.exists():
        errors.append("findings.json is missing")
        return errors
    manifest = load_json(manifest_path)
    findings = load_json(findings_path)
    if manifest.get("schema_version") != SCHEMA_VERSION:
        errors.append("manifest schema_version is unsupported")
    if findings.get("schema_version") != SCHEMA_VERSION:
        errors.append("findings schema_version is unsupported")
    page_shards = manifest.get("page_shards", {})
    for page, shard in page_shards.items():
        shard_path = state_dir / shard
        if not shard_path.exists():
            errors.append(f"claim shard is missing for {page}: {shard}")
            continue
        shard_data = load_json(shard_path)
        for claim in shard_data.get("claims", []):
            try:
                validate_public_claim(claim)
                normalized = normalize_claim(claim)
            except AuditError as exc:
                errors.append(f"invalid claim in {shard}: {exc}")
                continue
            if claim.get("claim_id") != normalized["claim_id"]:
                errors.append(f"claim_id mismatch in {shard}")
            if claim.get("claim_content_fingerprint") != normalized["claim_content_fingerprint"]:
                errors.append(f"claim content fingerprint mismatch in {shard}")
    for finding_id, finding in findings.get("findings", {}).items():
        try:
            ensure_no_private_reference(finding)
        except AuditError as exc:
            errors.append(f"private evidence in finding {finding_id}: {exc}")
            continue
        if finding_id != finding.get("finding_id"):
            errors.append(f"finding key mismatch: {finding_id}")
            continue
        normalized = normalize_finding(finding)
        if normalized["finding_id"] != finding_id:
            errors.append(f"finding_id fingerprint mismatch: {finding_id}")
        if normalized["finding_content_fingerprint"] != finding.get("finding_content_fingerprint"):
            errors.append(f"finding content fingerprint mismatch: {finding_id}")
        if finding.get("lifecycle") not in FINDING_STATES:
            errors.append(f"invalid lifecycle for {finding_id}")
    schedule_claims = state_dir / "schedule_claims"
    claim_paths = schedule_claims.glob("*.json") if schedule_claims.exists() else []
    for claim_path in claim_paths:
        schedule_claim = load_json(claim_path)
        if schedule_claim.get("business_date") != claim_path.stem:
            errors.append(f"schedule claim date mismatch: {claim_path.name}")
        try:
            dt.date.fromisoformat(schedule_claim.get("business_date", ""))
        except (TypeError, ValueError):
            errors.append(f"invalid schedule claim date: {claim_path.name}")
        if schedule_claim.get("schema_version") != SCHEMA_VERSION:
            errors.append(f"invalid schedule claim schema: {claim_path.name}")
        if not schedule_claim.get("event_id"):
            errors.append(f"schedule claim event_id is missing: {claim_path.name}")
        try:
            dt.datetime.fromisoformat(schedule_claim.get("claimed_at", ""))
        except (TypeError, ValueError):
            errors.append(f"invalid schedule claim timestamp: {claim_path.name}")
    return errors


def validate_state_command(args: argparse.Namespace) -> int:
    errors = validate_state_tree(Path(args.state_dir))
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print("State schema and fingerprint integrity checks passed.")
    return 0


PRIVATE_MARKERS = (
    "warpdotdev/warp-server",
    "/workspace/warp-server",
    "billing/config/",
    "public_api/openapi.yaml",
)


def ensure_no_private_reference(
    value: Any,
    authority_records: list[dict[str, Any]] | None = None,
) -> None:
    serialized = canonical_json(value)
    markers = set(PRIVATE_MARKERS)
    for record in authority_records or []:
        if record.get("visibility") != "private":
            continue
        markers.update(
            str(item)
            for item in (
                record.get("authority_id"),
                record.get("evidence_hash"),
                *record.get("source_ref", {}).values(),
            )
            if item
        )
    if any(marker in serialized for marker in markers):
        raise AuditError("Public output contains a private authority reference")


def validate_scope_quote(
    evidence: dict[str, Any],
    repository_roots: dict[str, Path],
) -> None:
    source = evidence.get("source", {})
    validate_claim_quote(
        {
            "source": source,
            "quote": evidence.get("quote", ""),
        },
        repository_roots,
    )
    try:
        validate_public_claim({"source": source})
    except AuditError as exc:
        raise AuditError("Scope verification requires public evidence") from exc


def verified_finding_from_candidate(
    candidate: dict[str, Any],
    verification: dict[str, Any],
    repository_roots: dict[str, Path],
    run_id: str,
    source_commit: str,
) -> dict[str, Any] | None:
    required = {
        "candidate_id",
        "title",
        "severity",
        "confidence",
        "verdict",
        "rationale",
        "rationale_class",
        "canonical_source",
        "authority_reason",
        "suggested_resolution",
        "suggested_resolution_class",
        "claim_ids",
        "scope_quotes",
        "qualifier_status",
        "context_complete",
    }
    missing = required - set(verification)
    if missing:
        raise AuditError(
            "Context verification is missing fields: " + ", ".join(sorted(missing))
        )
    if verification["candidate_id"] != candidate["candidate_id"]:
        raise AuditError("Context verification candidate_id mismatch")
    expected_claim_ids = sorted((
        candidate["left"]["claim_id"],
        candidate["right"]["claim_id"],
    ))
    if sorted(verification["claim_ids"]) != expected_claim_ids:
        raise AuditError("Context verification claim_ids mismatch")
    if verification["verdict"] not in VERDICTS:
        raise AuditError(f"Invalid adjudication verdict: {verification['verdict']}")
    if verification["severity"] not in {"high", "medium", "low"}:
        raise AuditError("Invalid adjudication severity")
    if verification["confidence"] not in {"high", "medium", "low"}:
        raise AuditError("Invalid adjudication confidence")
    if verification["qualifier_status"] not in {"complete", "unknown"}:
        raise AuditError("qualifier_status must be complete or unknown")
    if (
        not isinstance(verification["scope_quotes"], list)
        or not verification["scope_quotes"]
    ):
        raise AuditError("scope_quotes must be a non-empty list")
    if not isinstance(verification["context_complete"], bool):
        raise AuditError("context_complete must be boolean")
    for evidence in verification["scope_quotes"]:
        validate_scope_quote(evidence, repository_roots)
    supported_paths = {
        evidence["source"]["path"] for evidence in verification["scope_quotes"]
    }
    claim_paths = {
        candidate["left"]["source"]["path"],
        candidate["right"]["source"]["path"],
    }
    full_context = (
        verification["context_complete"] is True
        and verification["qualifier_status"] == "complete"
        and claim_paths <= supported_paths
    )
    decision = copy.deepcopy(verification)
    if decision["confidence"] == "high" and not full_context:
        decision["confidence"] = "medium"
        decision["confidence_downgrade"] = "incomplete qualifier or scope evidence"
    ensure_no_private_reference(
        decision,
        candidate.get("authority_records", []),
    )
    if decision["context_complete"] is not True:
        return None
    if decision["verdict"] not in REPORTABLE_VERDICTS:
        return None
    claims = [candidate["left"], candidate["right"]]
    for claim in claims:
        validate_public_claim(claim)
    left = candidate["left"]
    finding = {
        "title": decision["title"],
        "category": left.get("category", left["topic"]),
        "severity": decision["severity"],
        "confidence": decision["confidence"],
        "topic": left["topic"],
        "entity": left["entity"],
        "predicate": left["predicate"],
        "claims": claims,
        "verdict": decision["verdict"],
        "rationale": decision["rationale"],
        "rationale_class": decision["rationale_class"],
        "canonical_source": decision["canonical_source"],
        "authority_reason": decision["authority_reason"],
        "suggested_resolution": decision["suggested_resolution"],
        "suggested_resolution_class": decision["suggested_resolution_class"],
        "scope_quotes": decision["scope_quotes"],
        "qualifier_status": decision["qualifier_status"],
        "context_complete": decision["context_complete"],
        "audit_run_id": run_id,
        "source_commit": source_commit,
    }
    ensure_no_private_reference(
        finding,
        candidate.get("authority_records", []),
    )
    return finding


def public_candidate_dto(candidate: dict[str, Any]) -> dict[str, Any]:
    result = {
        key: copy.deepcopy(value)
        for key, value in candidate.items()
        if key != "authority_records"
    }
    result["authority_records"] = [
        public_authority_dto(record)
        for record in candidate.get("authority_records", [])
    ]
    ensure_no_private_reference(
        result,
        candidate.get("authority_records", []),
    )
    return result


def artifact_markdown(artifact: dict[str, Any]) -> str:
    lines = [
        "# Docs consistency audit",
        "",
        f"- Run: `{artifact['run_id']}`",
        f"- Coverage: `{artifact['coverage']}`",
        f"- Active findings: {artifact['summary']['active']}",
        f"- New: {artifact['summary']['new']}",
        f"- Changed: {artifact['summary']['changed']}",
        f"- Resolved: {artifact['summary']['resolved']}",
        f"- Suppressed candidates: {artifact['summary']['suppressed']}",
        "",
        "## Lifecycle changes",
    ]
    changes = artifact.get("lifecycle_changes", [])
    if not changes:
        lines.append("")
        lines.append("No lifecycle changes.")
    for finding in changes:
        lines.extend([
            "",
            f"### {finding['title']}",
            "",
            f"- Lifecycle: `{finding['lifecycle']}`",
            f"- Severity: `{finding['severity']}`",
            f"- Confidence: `{finding['confidence']}`",
            f"- Finding ID: `{finding['finding_id']}`",
        ])
    return "\n".join(lines) + "\n"


def fsync_tree(root: Path) -> None:
    for path in sorted(root.rglob("*")):
        if path.is_file():
            with path.open("rb") as handle:
                os.fsync(handle.fileno())
    directories = [path for path in root.rglob("*") if path.is_dir()]
    for directory in [*sorted(directories, reverse=True), root]:
        descriptor = os.open(directory, os.O_RDONLY)
        try:
            os.fsync(descriptor)
        finally:
            os.close(descriptor)


def replace_state_tree(
    state_dir: Path,
    temp_dir: Path,
    replace_operation=os.replace,
) -> None:
    backup = state_dir.with_name(state_dir.name + ".previous")
    if backup.exists():
        if state_dir.exists():
            shutil.rmtree(backup)
        else:
            replace_operation(backup, state_dir)
    fsync_tree(temp_dir)
    had_state = state_dir.exists()
    if had_state:
        replace_operation(state_dir, backup)
    try:
        replace_operation(temp_dir, state_dir)
        parent_descriptor = os.open(state_dir.parent, os.O_RDONLY)
        try:
            os.fsync(parent_descriptor)
        finally:
            os.close(parent_descriptor)
    except Exception:
        if backup.exists():
            if state_dir.exists():
                shutil.rmtree(state_dir)
            replace_operation(backup, state_dir)
        raise
    if backup.exists():
        shutil.rmtree(backup)


def load_prior_page_claims(
    state_dir: Path,
    manifest: dict[str, Any],
    pages: set[str],
) -> list[dict[str, Any]]:
    claims = []
    for page, shard in manifest.get("page_shards", {}).items():
        if page in pages:
            claims.extend(load_json(state_dir / shard).get("claims", []))
    return claims


def effective_manifest_pages(
    inventory: dict[str, Any],
    prior_manifest: dict[str, Any],
    backlog: set[str],
) -> dict[str, Any]:
    pages = copy.deepcopy(inventory.get("pages", {}))
    for page in backlog:
        prior_page = prior_manifest.get("pages", {}).get(page)
        if prior_page:
            pages[page] = copy.deepcopy(prior_page)
        else:
            pages.pop(page, None)
    return pages


def validate_extraction_document(
    document: Any,
    repository_roots: dict[str, Path],
    redirects: dict[str, str],
) -> dict[str, Any]:
    if isinstance(document, dict):
        raw_claims = document.get("claims", [])
        verifications = document.get("adjudicated_findings", [])
        extraction_failures = document.get("extraction_failures", [])
        processed_pages = document.get("processed_pages", [])
    elif isinstance(document, list):
        raw_claims = document
        verifications = []
        extraction_failures = []
        processed_pages = []
    else:
        raise AuditError(
            "Claims input must be a list or an object with a claims list"
        )
    if not isinstance(raw_claims, list):
        raise AuditError("Extraction claims must be a list")
    if not isinstance(verifications, list) or not all(
        isinstance(verification, dict)
        for verification in verifications
    ):
        raise AuditError("Extraction adjudicated_findings must be a list of objects")
    if not isinstance(extraction_failures, list):
        raise AuditError("Extraction failures must be a list")
    if extraction_failures:
        raise AuditError("Claim extraction contains unresolved failures")
    if not isinstance(processed_pages, list) or not all(
        isinstance(page, str)
        for page in processed_pages
    ):
        raise AuditError("Extraction processed_pages must be a list of paths")
    normalized_claims = []
    for raw_claim in raw_claims:
        if not isinstance(raw_claim, dict):
            raise AuditError("Every extracted claim must be an object")
        validate_public_claim(raw_claim)
        validate_claim_quote(raw_claim, repository_roots)
        normalized_claims.append(
            normalize_claim(apply_redirect_identity(raw_claim, redirects))
        )
    return {
        "claims": normalized_claims,
        "adjudicated_findings": copy.deepcopy(verifications),
        "processed_pages": list(processed_pages),
    }


def run_pipeline(args: argparse.Namespace) -> int:
    run_id = args.run_id or dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    claims_document = load_json(Path(args.claims))
    roots: dict[str, Path] = {}
    for value in args.repository_root:
        name, separator, path = value.partition("=")
        if not separator:
            raise AuditError("--repository-root values must use NAME=PATH")
        roots[name] = Path(path).resolve()
    docs_root = roots.get("warpdotdev/docs")
    redirect_path = (
        Path(args.redirects)
        if args.redirects
        else docs_root / "vercel.json"
        if docs_root
        else None
    )
    redirects = load_verified_redirects(redirect_path)
    extraction = validate_extraction_document(
        claims_document,
        roots,
        redirects,
    )
    extracted_claims = extraction["claims"]
    verifications = extraction["adjudicated_findings"]
    state_dir = Path(args.state_dir)
    inventory = load_json(Path(args.inventory), {}) if args.inventory else {}
    plan = inventory.get("extraction_plan", {})
    selected_pages = set(plan.get("selected_pages", []))
    backlog_pages = set(plan.get("backlog_pages", []))
    processed_pages = set(extraction["processed_pages"])
    if not processed_pages:
        processed_pages = {
            claim["source"]["path"]
            for claim in extracted_claims
        }
    missing_selected = selected_pages - processed_pages
    if missing_selected:
        raise AuditError(
            "Selected pages lack validated extraction results: "
            + ", ".join(sorted(missing_selected))
        )
    previous_manifest = (
        load_json(state_dir / "manifest.json", {})
        if state_dir.exists()
        else {}
    )
    unchanged_pages = {
        path
        for path, page in inventory.get("pages", {}).items()
        if page.get("extraction_status") == "unchanged"
    }
    carried_pages = unchanged_pages | backlog_pages
    prior_claims = (
        load_prior_page_claims(state_dir, previous_manifest, carried_pages)
        if state_dir.exists()
        else []
    )
    normalized_claims = []
    for prior_claim in prior_claims:
        validate_public_claim(prior_claim)
        normalized_claims.append(
            normalize_claim(apply_redirect_identity(prior_claim, redirects))
        )
    normalized_claims.extend(extracted_claims)
    rules = load_json(Path(args.authority_rules))
    authority_records = (
        validate_authority_contract(load_json(Path(args.authorities)))
        if args.authorities
        else []
    )
    candidates = generate_candidates(normalized_claims, rules)
    for candidate in candidates:
        candidate["authority_records"] = matching_authorities(
            candidate,
            authority_records,
        )
    public_candidates = [public_candidate_dto(candidate) for candidate in candidates]
    if args.candidate_output:
        write_json(Path(args.candidate_output), {
            "schema_version": SCHEMA_VERSION,
            "candidates": public_candidates,
            "summary": {
                "candidate_pairs": len(candidates),
                "exact_typed_mismatches": sum(
                    candidate["exact_typed_mismatch"] for candidate in candidates
                ),
                "semantic_review_required": sum(
                    not candidate["exact_typed_mismatch"] for candidate in candidates
                ),
            },
        })
    verification_by_id = {}
    for verification in verifications:
        candidate_id = verification.get("candidate_id")
        if not candidate_id or candidate_id in verification_by_id:
            raise AuditError("Context verifications require unique candidate_id values")
        verification_by_id[candidate_id] = verification
    candidate_by_id = {
        candidate["candidate_id"]: candidate for candidate in candidates
    }
    unknown_verifications = set(verification_by_id) - set(candidate_by_id)
    if unknown_verifications:
        raise AuditError("Context verification references an unknown candidate")
    findings = []
    adjudication_decisions = []
    for candidate_id, verification in verification_by_id.items():
        ensure_no_private_reference(verification)
        decision = copy.deepcopy(verification)
        decision["audit_run_id"] = run_id
        adjudication_decisions.append(decision)
        finding = verified_finding_from_candidate(
            candidate_by_id[candidate_id],
            verification,
            roots,
            run_id,
            args.source_commit,
        )
        if finding:
            findings.append(finding)
    unverified_candidate_ids = sorted(
        (set(candidate_by_id) - set(verification_by_id))
        | {
            candidate_id
            for candidate_id, verification in verification_by_id.items()
            if verification.get("context_complete") is not True
        }
    )
    normalized_findings = [normalize_finding(finding) for finding in findings]
    findings_by_id = {finding["finding_id"]: finding for finding in normalized_findings}
    findings = list(findings_by_id.values())
    suppressions = load_json(Path(args.suppressions))
    active, suppressed, expired = apply_suppressions(findings, suppressions, dt.date.today())
    previous_findings = load_json(
        state_dir / "findings.json",
        {"schema_version": SCHEMA_VERSION, "findings": {}},
    )
    coverage = args.coverage
    if coverage == "complete" and (backlog_pages or unverified_candidate_ids):
        coverage = "partial"
    complete = coverage == "complete"
    lifecycle = calculate_lifecycle(active, previous_findings, run_id, complete)
    active_count = sum(
        finding.get("status") == "active"
        for finding in lifecycle["findings"].values()
    )
    summary = {
        "active": active_count,
        "new": sum(item.get("lifecycle") == "new" for item in lifecycle["changes"]),
        "changed": sum(item.get("lifecycle") == "changed" for item in lifecycle["changes"]),
        "resolved": sum(item.get("lifecycle") == "resolved" for item in lifecycle["changes"]),
        "existing": sum(
            item.get("lifecycle") == "existing"
            for item in lifecycle["findings"].values()
        ),
        "suppressed": len(suppressed),
        "expired_suppressions": len(expired),
        "claims": len(normalized_claims),
        "candidate_pairs": len(candidates),
        "model_calls": int(args.model_calls),
    }
    artifact = {
        "schema_version": SCHEMA_VERSION,
        "run_id": run_id,
        "source_commit": args.source_commit,
        "coverage": coverage,
        "source_availability": (
            load_json(Path(args.source_availability), {})
            if args.source_availability
            else {}
        ),
        "authority_summary": {
            "records": len(authority_records),
            "public": sum(
                record["visibility"] == "public"
                for record in authority_records
            ),
            "private_transient": sum(
                record["visibility"] == "private" for record in authority_records
            ),
        },
        "backlog_pages": sorted(backlog_pages),
        "unverified_candidate_ids": unverified_candidate_ids,
        "summary": summary,
        "active_findings": [
            finding for finding in lifecycle["findings"].values()
            if finding.get("status") == "active"
        ],
        "lifecycle_changes": lifecycle["changes"],
        "adjudication_decisions": adjudication_decisions,
        "suppressed_candidates": suppressed,
        "expired_suppressions": expired,
        "cost_counters": {
            "pages": int(args.pages),
            "characters": int(args.characters),
            "candidate_pairs": len(candidates),
            "model_calls": int(args.model_calls),
        },
    }
    ensure_no_private_reference(artifact, authority_records)
    write_json(Path(args.artifact_json), artifact)
    Path(args.artifact_markdown).write_text(artifact_markdown(artifact))
    if args.no_state_write:
        print(canonical_json(summary))
        return 0

    temporary_parent = state_dir.parent
    temporary_parent.mkdir(parents=True, exist_ok=True)
    temp_dir = Path(tempfile.mkdtemp(prefix=".docs-consistency-", dir=temporary_parent))
    try:
        claims_dir = temp_dir / "claims"
        claims_dir.mkdir()
        page_shards = {}
        by_page: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for claim in normalized_claims:
            by_page[claim["source"]["path"]].append(claim)
        pages_to_write = set(by_page) | processed_pages | carried_pages
        for page in sorted(pages_to_write):
            page_claims = by_page.get(page, [])
            shard_name = hashlib.sha256(page.encode()).hexdigest() + ".json"
            shard_path = claims_dir / shard_name
            page_sha = inventory.get("pages", {}).get(page, {}).get("source_sha256")
            if page_claims:
                page_sha = page_claims[0]["source"].get("content_sha256") or page_sha
            write_json(shard_path, {
                "schema_version": SCHEMA_VERSION,
                "path": page,
                "page_sha256": page_sha,
                "claims": page_claims,
            })
            page_shards[page] = f"claims/{shard_name}"
        schedule_claims = state_dir / "schedule_claims"
        if schedule_claims.exists():
            shutil.copytree(schedule_claims, temp_dir / "schedule_claims")
        manifest_pages = effective_manifest_pages(
            inventory,
            previous_manifest,
            backlog_pages,
        )
        write_json(temp_dir / "manifest.json", {
            "schema_version": SCHEMA_VERSION,
            "extractor_version": EXTRACTOR_VERSION,
            "model_contract_version": MODEL_CONTRACT_VERSION,
            "authority_rules_version": rules["version"],
            "model_identifier": args.model_identifier,
            "source_repositories": {"docs": args.source_commit},
            "last_completed_run": (
                run_id
                if complete
                else previous_manifest.get("last_completed_run")
            ),
            "coverage": coverage,
            "pages": manifest_pages,
            "page_shards": page_shards,
            "backlog_pages": sorted(backlog_pages),
            "deleted_page_shards": inventory.get("deleted_pages", []),
        })
        write_json(temp_dir / "findings.json", {
            "schema_version": SCHEMA_VERSION,
            "findings": lifecycle["findings"],
        })
        errors = validate_state_tree(temp_dir)
        if errors:
            raise AuditError("Generated state failed validation: " + "; ".join(errors))
        replace_state_tree(state_dir, temp_dir)
    except Exception:
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
        raise
    print(canonical_json(summary))
    return 0


def benchmark_fixture_path(
    case: dict[str, Any],
    fixture_root: Path,
) -> Path:
    relative = case.get("fixture")
    expected_hash = case.get("fixture_sha256")
    if not isinstance(relative, str) or not expected_hash:
        raise AuditError("Benchmark case requires a pinned fixture")
    fixture_root = fixture_root.resolve()
    fixture_path = (fixture_root / relative).resolve()
    try:
        fixture_path.relative_to(fixture_root)
    except ValueError as exc:
        raise AuditError("Benchmark fixture escapes the fixture root") from exc
    if (
        fixture_path.name != "extraction.json"
        or fixture_path.parent.name != case["id"]
    ):
        raise AuditError("Benchmark fixture path must be named by its case")
    if not fixture_path.exists():
        raise AuditError(f"Benchmark fixture is missing: {relative}")
    if sha256_text(fixture_path.read_text()) != expected_hash:
        raise AuditError("Benchmark extraction fixture fingerprint mismatch")
    return fixture_path


def validate_benchmark_fixture(
    fixture_path: Path,
    rules: dict[str, Any],
) -> dict[str, Any]:
    document = load_json(fixture_path)
    manifest = document.get("evidence_manifest")
    if (
        not isinstance(manifest, dict)
        or not manifest
        or not all(
            isinstance(path, str) and isinstance(digest, str)
            for path, digest in manifest.items()
        )
    ):
        raise AuditError("Benchmark fixture requires an evidence manifest")
    fixture_dir = fixture_path.parent
    inventory = inventory_pages(fixture_dir, rules)
    if set(inventory["pages"]) != set(manifest):
        raise AuditError("Benchmark inventory does not match its evidence manifest")
    for path, expected_hash in manifest.items():
        if inventory["pages"][path]["source_sha256"] != expected_hash:
            raise AuditError(f"Benchmark evidence fingerprint mismatch: {path}")
    extraction = validate_extraction_document(
        document,
        {"warpdotdev/docs": fixture_dir},
        {},
    )
    claim_paths = {
        claim["source"]["path"]
        for claim in extraction["claims"]
    }
    if claim_paths != set(manifest):
        raise AuditError("Benchmark claims do not cover the evidence manifest")
    if set(extraction["processed_pages"]) != set(manifest):
        raise AuditError("Benchmark processed pages do not match its evidence manifest")
    return extraction


def production_benchmark_case(
    case: dict[str, Any],
    rules: dict[str, Any],
    fixture_root: Path,
) -> str:
    if case.get("delegated_to"):
        if case["delegated_to"] not in {
            "style_lint",
            "validate_ui_refs",
            "check_for_broken_links",
            "missing_docs",
        }:
            raise AuditError("Benchmark delegates to an unknown owning skill")
        return "delegated"
    fixture_path = benchmark_fixture_path(case, fixture_root)
    extraction = validate_benchmark_fixture(fixture_path, rules)
    normalized_claims = extraction["claims"]
    verifications = extraction["adjudicated_findings"]
    if len(normalized_claims) == 1:
        if verifications:
            raise AuditError("Single-claim benchmark cannot contain adjudication")
        return "gap"
    candidates = generate_candidates(normalized_claims, rules)
    if not candidates:
        if verifications:
            raise AuditError("Non-candidate benchmark cannot contain adjudication")
        compatible, conflicts, _ = qualifier_compatibility(
            normalized_claims[0]["qualifiers"],
            normalized_claims[1]["qualifiers"],
        )
        if "explicit-exception" in conflicts:
            return "intentional-exception"
        return "insufficient-evidence" if compatible else "not-related"
    verification_by_id = {}
    for verification in verifications:
        candidate_id = verification.get("candidate_id")
        if not candidate_id or candidate_id in verification_by_id:
            raise AuditError(
                "Benchmark adjudications require unique candidate IDs"
            )
        verification_by_id[candidate_id] = verification
    candidate_by_id = {
        candidate["candidate_id"]: candidate
        for candidate in candidates
    }
    if set(verification_by_id) != set(candidate_by_id):
        raise AuditError("Benchmark adjudication does not cover every candidate")
    verdicts = []
    roots = {"warpdotdev/docs": fixture_path.parent}
    for candidate_id, candidate in candidate_by_id.items():
        verification = verification_by_id[candidate_id]
        finding = verified_finding_from_candidate(
            candidate,
            verification,
            roots,
            "benchmark",
            "benchmark",
        )
        verdicts.append(
            finding["verdict"]
            if finding
            else verification["verdict"]
        )
    if len(set(verdicts)) != 1:
        raise AuditError("Benchmark candidates produced inconsistent verdicts")
    return verdicts[0]


def benchmark_command(args: argparse.Namespace) -> int:
    benchmark = load_json(Path(args.cases))
    rules = load_json(Path(args.authority_rules))
    fixture_root = Path(getattr(args, "fixture_root", REFERENCES_DIR))
    results = []
    for case in benchmark["cases"]:
        error = None
        try:
            predicted = production_benchmark_case(
                case,
                rules,
                fixture_root,
            )
        except AuditError as exc:
            predicted = "invalid-production-path"
            error = str(exc)
        expected = case["expected"]
        results.append({
            "id": case["id"],
            "group": case["group"],
            "expected": expected,
            "predicted": predicted,
            "severity": case.get("severity", "low"),
            "confidence": case.get("confidence", "high"),
            "policy_domain": case.get("policy_domain"),
            "passed": predicted == expected,
            "production_path_error": error,
        })
    falconer = [item for item in results if item["group"] == "falconer"]
    negative = [item for item in results if item["group"] == "negative-control"]
    surfaced = [
        item for item in falconer
        if item["predicted"] not in {"not-related", "insufficient-evidence"}
    ]
    high_confidence = [item for item in surfaced if item["confidence"] == "high"]
    policy_errors = [
        item for item in high_confidence
        if item["policy_domain"] in {"security", "privacy", "billing-policy"}
        and not item["passed"]
    ]
    scorecard = {
        "schema_version": SCHEMA_VERSION,
        "cases": results,
        "summary": {
            "falconer_cases": len(falconer),
            "falconer_passed": sum(item["passed"] for item in falconer),
            "negative_controls": len(negative),
            "negative_controls_passed": sum(item["passed"] for item in negative),
            "high_confidence_precision": (
                sum(item["passed"] for item in high_confidence) / len(high_confidence)
                if high_confidence else 0
            ),
            "surfaced_precision": (
                sum(item["passed"] for item in surfaced) / len(surfaced)
                if surfaced else 0
            ),
            "incorrect_high_confidence_policy_conclusions": len(policy_errors),
            "production_path_errors": sum(
                bool(item["production_path_error"]) for item in results
            ),
        },
        "thresholds": {
            "all_24_accounted_for": (
                len(falconer) == 24
                and all(item["passed"] for item in falconer)
            ),
            "high_confidence_precision_at_least_0_90": None,
            "surfaced_precision_at_least_0_80": None,
            "zero_incorrect_high_confidence_policy_conclusions": not policy_errors,
            "all_negative_controls_pass": all(item["passed"] for item in negative),
            "production_path_has_no_errors": not any(
                item["production_path_error"] for item in results
            ),
        },
    }
    scorecard["thresholds"]["high_confidence_precision_at_least_0_90"] = (
        scorecard["summary"]["high_confidence_precision"] >= 0.90
    )
    scorecard["thresholds"]["surfaced_precision_at_least_0_80"] = (
        scorecard["summary"]["surfaced_precision"] >= 0.80
    )
    scorecard["passed"] = all(scorecard["thresholds"].values())
    write_json(Path(args.output), scorecard)
    print(canonical_json(scorecard["summary"]))
    return 0 if scorecard["passed"] else 1


def schedule_guard_command(args: argparse.Namespace) -> int:
    if args.at:
        instant = dt.datetime.fromisoformat(args.at.replace("Z", "+00:00"))
        if instant.tzinfo is None:
            instant = instant.replace(tzinfo=dt.timezone.utc)
    else:
        instant = dt.datetime.now(dt.timezone.utc)
    local = instant.astimezone(ZoneInfo("America/Los_Angeles"))
    active = local.weekday() in {0, 2, 4} and local.hour == 10
    result = {
        "active": active,
        "local_time": local.isoformat(),
        "reason": "active Pacific audit window" if active else "inactive half of paired UTC schedules",
    }
    print(canonical_json(result))
    return 0 if active else 10


def schedule_claim_command(args: argparse.Namespace) -> int:
    instant = (
        dt.datetime.fromisoformat(args.at.replace("Z", "+00:00"))
        if args.at
        else dt.datetime.now(dt.timezone.utc)
    )
    if instant.tzinfo is None:
        instant = instant.replace(tzinfo=dt.timezone.utc)
    local = instant.astimezone(ZoneInfo("America/Los_Angeles"))
    active = local.weekday() in {0, 2, 4} and local.hour == 10
    if not active:
        print(canonical_json({
            "claimed": False,
            "reason": "inactive Pacific audit window",
            "local_time": local.isoformat(),
        }))
        return 10
    business_date = local.date().isoformat()
    claims_dir = Path(args.state_dir) / "schedule_claims"
    claims_dir.mkdir(parents=True, exist_ok=True)
    claim_path = claims_dir / f"{business_date}.json"
    payload = {
        "schema_version": SCHEMA_VERSION,
        "business_date": business_date,
        "event_id": args.event_id,
        "claimed_at": instant.astimezone(dt.timezone.utc).isoformat(),
    }
    try:
        descriptor = os.open(
            claim_path,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL,
            0o644,
        )
    except FileExistsError:
        print(canonical_json({
            "claimed": False,
            "reason": "Pacific business date already claimed",
            "business_date": business_date,
        }))
        return 11
    with os.fdopen(descriptor, "w") as handle:
        handle.write(json.dumps(payload, indent=2, sort_keys=True) + "\n")
        handle.flush()
        os.fsync(handle.fileno())
    parent_descriptor = os.open(claims_dir, os.O_RDONLY)
    try:
        os.fsync(parent_descriptor)
    finally:
        os.close(parent_descriptor)
    print(canonical_json({"claimed": True, **payload}))
    return 0


def notification_command(args: argparse.Namespace) -> int:
    artifact = load_json(Path(args.artifact))
    ensure_no_private_reference(artifact)
    changes = artifact.get("lifecycle_changes", [])
    actionable = [
        finding for finding in changes
        if finding.get("confidence") == "high"
        or (
            finding.get("severity") == "high"
            and finding.get("confidence") == "medium"
        )
    ]
    blocked = artifact.get("coverage") == "blocked"
    should_post = blocked or bool(actionable)
    summary = artifact.get("summary", {})
    titles = sorted(
        actionable,
        key=lambda finding: (
            {"high": 0, "medium": 1, "low": 2}.get(finding.get("severity"), 3),
            finding.get("title", ""),
        ),
    )[:3]
    lines = [
        f"{'⚠️' if blocked else '📚'} Docs consistency audit · {artifact.get('run_id', 'unknown run')}",
        (
            "Run blocked; prior findings were preserved."
            if blocked
            else (
                f"New {summary.get('new', 0)} · changed {summary.get('changed', 0)} · "
                f"resolved {summary.get('resolved', 0)} · active {summary.get('active', 0)}"
            )
        ),
    ]
    if titles:
        lines.append("Highest-severity changes: " + "; ".join(item["title"] for item in titles))
    if args.state_pr_url:
        lines.append(f"State PR: {args.state_pr_url}")
    if args.run_url:
        lines.append(f"Run: {args.run_url}")
    result = {
        "should_post": should_post,
        "reason": (
            "blocked"
            if blocked
            else "actionable lifecycle changes"
            if actionable
            else "no actionable lifecycle changes"
        ),
        "message": "\n".join(lines) if should_post else None,
        "actionable_finding_ids": [item["finding_id"] for item in actionable],
    }
    write_json(Path(args.output), result)
    print(canonical_json(result))
    return 0


def preflight_command(args: argparse.Namespace) -> int:
    repos = {
        "docs": Path(args.docs_repo).resolve(),
        "warp": Path(args.warp_repo).resolve(),
        "warp_server": Path(args.warp_server).resolve(),
    }
    result = {"repositories": {name: repo_ref(path) for name, path in repos.items()}}
    if args.fetch_state_branch:
        remote_ref = f"refs/remotes/origin/{STATE_BRANCH}"
        check = subprocess.run(
            ["git", "-C", str(repos["docs"]), "ls-remote", "--exit-code", "--heads", "origin", STATE_BRANCH],
            check=False,
            capture_output=True,
            text=True,
        )
        if check.returncode == 0:
            fetch = subprocess.run(
                ["git", "-C", str(repos["docs"]), "fetch", "origin", f"{STATE_BRANCH}:{remote_ref}"],
                check=False,
                capture_output=True,
                text=True,
            )
            if fetch.returncode:
                raise AuditError(f"State branch exists but cannot be fetched: {fetch.stderr.strip()}")
            result["state_branch"] = {"exists": True, "commit": git_value(repos["docs"], "rev-parse", remote_ref)}
        elif check.returncode == 2:
            result["state_branch"] = {"exists": False}
        else:
            raise AuditError(f"Cannot determine state branch availability: {check.stderr.strip()}")
    write_json(Path(args.output), result)
    print(canonical_json(result))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    preflight = subparsers.add_parser("preflight", help="Verify source repositories and state branch")
    preflight.add_argument("--docs-repo", default="/workspace/docs")
    preflight.add_argument("--warp-repo", default="/workspace/warp")
    preflight.add_argument("--warp-server", default="/workspace/warp-server")
    preflight.add_argument("--fetch-state-branch", action="store_true")
    preflight.add_argument("--output", required=True)
    preflight.set_defaults(func=preflight_command)

    guard = subparsers.add_parser("schedule-guard", help="Apply the Pacific-time schedule guard")
    guard.add_argument("--at", help="ISO-8601 instant used by tests")
    guard.set_defaults(func=schedule_guard_command)
    claim_schedule = subparsers.add_parser(
        "claim-schedule",
        help="Atomically claim one Pacific business date before scheduled work",
    )
    claim_schedule.add_argument("--state-dir", default=str(STATE_PATH))
    claim_schedule.add_argument("--event-id", required=True)
    claim_schedule.add_argument("--at", help="ISO-8601 instant used by tests")
    claim_schedule.set_defaults(func=schedule_claim_command)
    notification = subparsers.add_parser(
        "notification",
        help="Render at most one actionable-only Slack payload",
    )
    notification.add_argument("--artifact", required=True)
    notification.add_argument("--run-url")
    notification.add_argument("--state-pr-url")
    notification.add_argument("--output", required=True)
    notification.set_defaults(func=notification_command)

    inventory = subparsers.add_parser("inventory", help="Inventory public docs and plan changed shards")
    inventory.add_argument("--docs-repo", default="/workspace/docs")
    inventory.add_argument("--content-root", default="src/content/docs")
    inventory.add_argument("--authority-rules", default=str(DEFAULT_AUTHORITY_RULES))
    inventory.add_argument("--previous-manifest")
    inventory.add_argument("--full", action="store_true")
    inventory.add_argument("--max-pages", type=int, default=0)
    inventory.add_argument("--max-characters", type=int, default=0)
    inventory.add_argument("--output", required=True)
    inventory.set_defaults(func=inventory_command)

    adapters = subparsers.add_parser("adapters", help="Refresh structured authority inputs")
    adapters.add_argument("--docs-repo", default="/workspace/docs")
    adapters.add_argument("--warp-repo", default="/workspace/warp")
    adapters.add_argument("--warp-server", default="/workspace/warp-server")
    adapters.add_argument("--fetch-pricing", action="store_true")
    adapters.add_argument("--output", required=True)
    adapters.set_defaults(func=adapters_command)

    run = subparsers.add_parser("run", help="Compare validated claims and update generated state")
    run.add_argument("--claims", required=True)
    run.add_argument("--inventory")
    run.add_argument("--repository-root", action="append", default=[], metavar="NAME=PATH")
    run.add_argument("--state-dir", default=str(STATE_PATH))
    run.add_argument("--authority-rules", default=str(DEFAULT_AUTHORITY_RULES))
    run.add_argument("--authorities")
    run.add_argument("--redirects")
    run.add_argument("--suppressions", default=str(DEFAULT_SUPPRESSIONS))
    run.add_argument("--artifact-json", required=True)
    run.add_argument("--artifact-markdown", required=True)
    run.add_argument("--candidate-output")
    run.add_argument("--run-id")
    run.add_argument("--source-commit", required=True)
    run.add_argument("--coverage", choices=["complete", "partial", "blocked"], default="complete")
    run.add_argument("--source-availability")
    run.add_argument("--model-identifier", default="unrecorded")
    run.add_argument("--model-calls", default=0)
    run.add_argument("--pages", default=0)
    run.add_argument("--characters", default=0)
    run.add_argument("--no-state-write", action="store_true")
    run.set_defaults(func=run_pipeline)

    validate = subparsers.add_parser("validate-state", help="Validate generated state and fingerprints")
    validate.add_argument("--state-dir", default=str(STATE_PATH))
    validate.set_defaults(func=validate_state_command)

    benchmark = subparsers.add_parser("benchmark", help="Score Falconer-derived and negative-control cases")
    benchmark.add_argument("--cases", default=str(DEFAULT_BENCHMARK))
    benchmark.add_argument("--authority-rules", default=str(DEFAULT_AUTHORITY_RULES))
    benchmark.add_argument("--fixture-root", default=str(REFERENCES_DIR))
    benchmark.add_argument("--output", required=True)
    benchmark.set_defaults(func=benchmark_command)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except AuditError as exc:
        print(f"BLOCKED: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
