#!/usr/bin/env python3
"""Build the `## Documentation risk` PR-body block.

PR-producing skills call this before requesting review to render the
machine-readable risk section in the shape `policy.py` parses. It does not
call `gh` itself — the invoking skill applies the `warpy-factory` label
(`gh pr edit --add-label warpy-factory`) and inserts the printed block into
the PR body it already assembles (see `create_pr/SKILL.md`).

Usage:
    python3 finalize_pr_contract.py build --risk low \\
        --rationale "Spelling and link-text fixes only; no technical claims changed."

    python3 finalize_pr_contract.py build --risk engineering-review-required \\
        --rationale "Documents a new CLI flag." \\
        --source-files app/src/cli/args.rs@abc123 \\
        --reviewers alice \\
        --engineering-review-status pending

    python3 finalize_pr_contract.py build --risk engineering-review-required \\
        --rationale "Documents a new CLI flag; engineer did not respond in time." \\
        --override-mode docs-waiver \\
        --override-reviewer hongyi-chen \\
        --override-reason "No source-owner response after 3 days; risk is limited to wording." \\
        --override-evidence "app/src/cli/args.rs@abc123" \\
        --override-head-sha "$HEAD_SHA"
"""
from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path
from typing import List, Optional

_HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("doc_quality_policy", _HERE / "policy.py")
policy = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = policy  # required for dataclass field resolution
_spec.loader.exec_module(policy)


def build_documentation_risk_block(
    *,
    risk: str,
    rationale: str,
    source_files: Optional[List[str]] = None,
    reviewers: Optional[List[str]] = None,
    engineering_review_status: Optional[str] = None,
    override_mode: str = policy.OVERRIDE_MODE_NONE,
    override_reviewer: Optional[str] = None,
    override_reason: Optional[str] = None,
    override_evidence: Optional[str] = None,
    override_head_sha: Optional[str] = None,
) -> str:
    if risk not in policy.VALID_RISK_LEVELS:
        raise ValueError(f"risk must be one of {policy.VALID_RISK_LEVELS}, got {risk!r}")
    if override_mode not in policy.VALID_OVERRIDE_MODES:
        raise ValueError(f"override_mode must be one of {policy.VALID_OVERRIDE_MODES}, got {override_mode!r}")

    lines = [policy.DOC_RISK_HEADING, f"Risk: {risk}", f"Rationale: {rationale}"]
    if source_files:
        lines.append(f"Source files consulted: {', '.join(source_files)}")
    if reviewers:
        lines.append(f"Requested engineering reviewers: {', '.join(reviewers)}")
    if engineering_review_status:
        lines.append(f"Engineering review status: {engineering_review_status}")
    lines.append(f"Docs override: {override_mode}")
    if override_mode != policy.OVERRIDE_MODE_NONE:
        lines.append(f"Override reviewer: {override_reviewer or ''}")
        lines.append(f"Override reason: {override_reason or ''}")
        lines.append(f"Override evidence: {override_evidence or ''}")
        lines.append(f"Override head SHA: {override_head_sha or ''}")
    return "\n".join(lines)


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    build = sub.add_parser("build", help="print the ## Documentation risk block")
    build.add_argument("--risk", required=True, choices=policy.VALID_RISK_LEVELS)
    build.add_argument("--rationale", required=True)
    build.add_argument("--source-files", help="comma-separated file@sha list")
    build.add_argument("--reviewers", help="comma-separated GitHub handles")
    build.add_argument("--engineering-review-status", choices=("not-applicable", "pending", "approved"))
    build.add_argument("--override-mode", default=policy.OVERRIDE_MODE_NONE, choices=policy.VALID_OVERRIDE_MODES)
    build.add_argument("--override-reviewer")
    build.add_argument("--override-reason")
    build.add_argument("--override-evidence")
    build.add_argument("--override-head-sha")

    args = parser.parse_args(argv)

    if args.command == "build":
        block = build_documentation_risk_block(
            risk=args.risk,
            rationale=args.rationale,
            source_files=[s.strip() for s in args.source_files.split(",")] if args.source_files else None,
            reviewers=[s.strip() for s in args.reviewers.split(",")] if args.reviewers else None,
            engineering_review_status=args.engineering_review_status,
            override_mode=args.override_mode,
            override_reviewer=args.override_reviewer,
            override_reason=args.override_reason,
            override_evidence=args.override_evidence,
            override_head_sha=args.override_head_sha,
        )
        print(block)
        print(
            f"\nReminder: apply the marker label with "
            f"'gh pr edit <pr> --add-label {policy.AGENT_MARKER}'.",
            file=sys.stderr,
        )
        return 0

    return 2


if __name__ == "__main__":
    sys.exit(main())
