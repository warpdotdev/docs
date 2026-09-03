#!/usr/bin/env python3
"""CI-callable checker for the agent-doc quality PR contract.

Wraps `policy.py` with the I/O CI needs: reading a PR body file, discovering
`{/* VERIFY: ... */}` markers in the changed docs files, and optionally taking
live signals (head SHA, review outcome, deterministic-check result) as flags
so this stays callable from a GitHub Actions step without a live `gh` call
baked into the checker itself.

Usage:
    python3 check_pr_contract.py --body /tmp/pr-body.md [changed_file ...]
    python3 check_pr_contract.py --body /tmp/pr-body.md \\
        --head-sha "$HEAD_SHA" --source-owner-approved

When no changed-file paths are given, changed `.md`/`.mdx` files under
`src/content/docs` are discovered via `git diff --diff-filter=d
origin/main...HEAD`, matching `style_lint.py --changed` and
`validate_ui_refs.py --changed`'s scope. Unlike `style_lint`'s `--changed`,
this never falls back to a full-tree scan: a diff that can't be resolved is a
hard failure, so required CI never silently widens scope.

Exit codes:
    0  the PR contract is satisfied
    1  one or more contract violations (see stderr)
    2  usage / file error
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
import sys
from pathlib import Path
from typing import List, Optional

_HERE = Path(__file__).resolve().parent
_DOCS_ROOT = "src/content/docs"
_DEFAULT_AUTHORIZED_REVIEWERS_FILE = _HERE / "authorized_docs_reviewers.json"

_spec = importlib.util.spec_from_file_location("doc_quality_policy", _HERE / "policy.py")
policy = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = policy  # required for dataclass field resolution
_spec.loader.exec_module(policy)


def _autodiscover_changed_files() -> List[Path]:
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", "--diff-filter=d", "origin/main...HEAD", "--", _DOCS_ROOT],
            capture_output=True, text=True, check=True,
        )
    except (subprocess.CalledProcessError, OSError) as exc:
        raise RuntimeError(f"could not determine changed files vs origin/main...HEAD: {exc}") from exc
    files = []
    for line in result.stdout.strip().splitlines():
        line = line.strip()
        if not line or not (line.endswith(".md") or line.endswith(".mdx")):
            continue
        p = Path(line)
        if p.exists():
            files.append(p)
    return files


def _load_authorized_reviewers(path: Path) -> List[str]:
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    return list(data.get("authorized_docs_reviewers", []))


def _collect_verify_markers(files: List[Path]) -> List[str]:
    markers: List[str] = []
    seen = set()
    for f in files:
        try:
            text = f.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        for marker in policy.find_verify_markers(text):
            if marker not in seen:
                seen.add(marker)
                markers.append(marker)
    return markers


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--body", required=True, help="path to the PR body file")
    parser.add_argument("changed_files", nargs="*", help="changed content files (auto-discovered if omitted)")
    parser.add_argument("--head-sha", help="current PR head SHA")
    parser.add_argument(
        "--authorized-reviewers-file",
        default=str(_DEFAULT_AUTHORIZED_REVIEWERS_FILE),
        help="JSON file with an 'authorized_docs_reviewers' array",
    )
    parser.add_argument(
        "--deterministic-checks-failed", action="store_true",
        help="pass when style_lint/validate_ui_refs did not pass on this head",
    )
    parser.add_argument(
        "--unresolved-important-finding", action="store_true",
        help="pass when review-docs-pr reported an unresolved critical/important finding",
    )
    parser.add_argument(
        "--source-owner-approved", action="store_true",
        help="pass when a requested source-owning engineer approved the current head",
    )
    args = parser.parse_args(argv)

    body_path = Path(args.body)
    try:
        body = body_path.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"error: could not read {args.body}: {exc}", file=sys.stderr)
        return 2

    if args.changed_files:
        changed_files = [Path(p) for p in args.changed_files]
    else:
        try:
            changed_files = _autodiscover_changed_files()
        except RuntimeError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 2

    verify_markers = _collect_verify_markers(changed_files)
    authorized_reviewers = _load_authorized_reviewers(Path(args.authorized_reviewers_file))

    problems = policy.validate_pr_contract(
        body,
        verify_markers,
        current_head_sha=args.head_sha,
        authorized_docs_reviewers=authorized_reviewers,
        deterministic_checks_passed=not args.deterministic_checks_failed,
        has_unresolved_critical_or_important_finding=args.unresolved_important_finding,
        source_owner_approved_current_head=args.source_owner_approved,
    )

    if problems:
        print("Documentation risk contract check FAILED:\n", file=sys.stderr)
        for problem in problems:
            print(f"  - {problem}", file=sys.stderr)
        return 1

    print(
        f"Documentation risk contract check passed "
        f"({len(verify_markers)} VERIFY marker(s), {len(changed_files)} changed file(s))."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
