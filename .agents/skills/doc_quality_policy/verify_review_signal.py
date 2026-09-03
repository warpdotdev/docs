#!/usr/bin/env python3
"""Verify a real, current GitHub review exists for the PR's head SHA.

A successful cloud-agent process is not proof that `review-docs-pr` actually
published a review: the agent could error after its shell exits 0, publish to
the wrong PR, or the push that triggered this run could already be stale by
the time the review posts. This script closes that gap by checking the
authoritative GitHub review list directly, so `.github/workflows/
agent-docs-review.yml` fails when no review exists for the current head, or
when the latest review at that head requests changes.

Usage:
    python3 verify_review_signal.py --repo owner/repo --pr 123 --head-sha $SHA

Exit codes:
    0  a review exists for this exact head SHA and does not request changes
    1  no review exists for this head, or the latest one requests changes
    2  usage / lookup error
"""
from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path
from typing import List, Optional

_HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("check_pr_contract", _HERE / "check_pr_contract.py")
cpc = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = cpc
_spec.loader.exec_module(cpc)


def check_review_signal(repo: str, pr_number: str, head_sha: str) -> List[str]:
    """Return a list of problems; empty means a current, non-blocking review exists."""
    try:
        reviews = cpc._fetch_reviews(repo, pr_number)
    except RuntimeError as exc:
        return [f"could not fetch reviews: {exc}"]

    signals = cpc._compute_review_signals(reviews, requested_reviewers=[], head_sha=head_sha, checks_passed=True)
    head_reviews = [
        r for r in reviews
        if r.get("commit_id") == head_sha and r.get("state") in ("APPROVED", "CHANGES_REQUESTED")
    ]
    if not head_reviews:
        return [
            f"no review found for head {head_sha} -- the agent process succeeded but "
            "posted no verifiable review at the current head"
        ]
    if signals.has_unresolved_critical_or_important_finding:
        return [f"the latest review for head {head_sha} requests changes"]
    return []


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--repo", required=True, help="owner/repo")
    parser.add_argument("--pr", required=True, help="PR number")
    parser.add_argument("--head-sha", required=True, help="PR head SHA to verify a review against")
    args = parser.parse_args(argv)

    problems = check_review_signal(args.repo, args.pr, args.head_sha)
    if problems:
        print("Agent docs review verification FAILED:", file=sys.stderr)
        for problem in problems:
            print(f"  - {problem}", file=sys.stderr)
        return 1

    print(f"Confirmed a current, non-blocking review exists for head {args.head_sha}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
