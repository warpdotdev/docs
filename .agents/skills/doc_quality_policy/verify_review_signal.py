#!/usr/bin/env python3
"""Verify a real, current independent-review signal and GitHub review.

A successful cloud-agent process is not proof that `review-docs-pr` actually
published a review: the agent could error after its shell exits 0, publish to
the wrong PR, or the push that triggered this run could already be stale by
the time the review posts. The workflow receives the agent's final text
output, where review-docs-pr is required to emit exactly one parseable
`[SIGNAL:pr-review]` JSON record. This script checks both sources.

Usage:
    python3 verify_review_signal.py --repo owner/repo --pr 123 --head-sha $SHA \
        --agent-output /tmp/agent-output.txt

Exit codes:
    0  a passing signal and review exist for this exact head SHA
    1  the signal/review is missing, stale, blocking, or malformed
    2  usage / lookup error
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path
from typing import List, Optional

_HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("check_pr_contract", _HERE / "check_pr_contract.py")
cpc = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = cpc
_spec.loader.exec_module(cpc)

_SIGNAL_RE = re.compile(r"\[SIGNAL:pr-review\]\s*(\{.*?\})", re.DOTALL)
_PASSING_VERDICTS = {"approve", "approve with nits", "approve_with_nits"}


def _validate_signal(agent_output: str, pr_number: str, head_sha: str) -> List[str]:
    matches = _SIGNAL_RE.findall(agent_output)
    if len(matches) != 1:
        return [f"expected exactly one [SIGNAL:pr-review] record, found {len(matches)}"]
    try:
        signal = json.loads(matches[0])
    except json.JSONDecodeError as exc:
        return [f"review signal is not valid JSON: {exc}"]

    problems = []
    if str(signal.get("pr")) != str(pr_number):
        problems.append(f"review signal PR {signal.get('pr')!r} does not match {pr_number!r}")
    if signal.get("head_sha") != head_sha:
        problems.append(
            f"review signal head SHA {signal.get('head_sha')!r} does not match current head {head_sha!r}"
        )
    if str(signal.get("verdict", "")).strip().lower() not in _PASSING_VERDICTS:
        problems.append(f"review signal has blocking verdict {signal.get('verdict')!r}")
    for field in ("critical", "important"):
        try:
            value = int(signal.get(field))
        except (TypeError, ValueError):
            problems.append(f"review signal has invalid {field} count {signal.get(field)!r}")
            continue
        if value != 0:
            problems.append(f"review signal reports {value} {field} finding(s)")
    return problems


def check_review_signal(repo: str, pr_number: str, head_sha: str, agent_output: str) -> List[str]:
    """Return problems; empty means the signal and review pass for the current head."""
    problems = _validate_signal(agent_output, pr_number, head_sha)
    try:
        reviews = cpc._fetch_reviews(repo, pr_number)
    except RuntimeError as exc:
        return [*problems, f"could not fetch reviews: {exc}"]

    signals = cpc._compute_review_signals(reviews, requested_reviewers=[], head_sha=head_sha, checks_passed=True)
    head_reviews = [
        r for r in reviews
        if r.get("commit_id") == head_sha and r.get("state") in ("APPROVED", "CHANGES_REQUESTED")
    ]
    if not head_reviews:
        problems.append(
            f"no review found for head {head_sha} -- the agent process succeeded but "
            "posted no verifiable review at the current head"
        )
    if signals.has_unresolved_critical_or_important_finding:
        problems.append(f"the latest review for head {head_sha} requests changes")
    return problems


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--repo", required=True, help="owner/repo")
    parser.add_argument("--pr", required=True, help="PR number")
    parser.add_argument("--head-sha", required=True, help="PR head SHA to verify a review against")
    parser.add_argument("--agent-output", required=True, help="file containing the agent's final text output")
    args = parser.parse_args(argv)
    try:
        agent_output = Path(args.agent_output).read_text(encoding="utf-8")
    except OSError as exc:
        print(f"error: could not read agent output: {exc}", file=sys.stderr)
        return 2

    problems = check_review_signal(args.repo, args.pr, args.head_sha, agent_output)
    if problems:
        print("Agent docs review verification FAILED:", file=sys.stderr)
        for problem in problems:
            print(f"  - {problem}", file=sys.stderr)
        return 1

    print(f"Confirmed a passing signal and current review for head {args.head_sha}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
