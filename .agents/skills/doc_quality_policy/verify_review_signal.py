#!/usr/bin/env python3
"""Verify a current independent-agent review and its structured signal."""
from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

_HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("check_pr_contract", _HERE / "check_pr_contract.py")
cpc = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = cpc
_spec.loader.exec_module(cpc)

_SIGNAL_RE = re.compile(r"\[SIGNAL:pr-review\]\s*(\{.*?\})", re.DOTALL)
_PASSING_VERDICTS = {"approve", "approve with nits", "approve_with_nits"}


def _parse_signal(text: str) -> Tuple[Optional[Dict[str, object]], List[str]]:
    matches = _SIGNAL_RE.findall(text)
    if not matches:
        return None, ["expected exactly one [SIGNAL:pr-review] record, found 0"]

    unique_signals = {}
    for match in matches:
        try:
            signal = json.loads(match)
        except json.JSONDecodeError as exc:
            return None, [f"review signal is not valid JSON: {exc}"]
        if not isinstance(signal, dict):
            return None, ["review signal must contain a JSON object"]
        unique_signals[json.dumps(signal, sort_keys=True, separators=(",", ":"))] = signal

    if len(unique_signals) != 1:
        return None, [
            "expected one unique [SIGNAL:pr-review] record, "
            f"found {len(unique_signals)} distinct records across {len(matches)} occurrences"
        ]
    return next(iter(unique_signals.values())), []


def _validate_signal(signal: Dict[str, object], pr_number: str, head_sha: str) -> List[str]:
    problems = []
    if str(signal.get("pr")) != str(pr_number):
        problems.append(f"review signal PR {signal.get('pr')!r} does not match {pr_number!r}")
    if signal.get("head_sha") != head_sha:
        problems.append(
            f"review signal head SHA {signal.get('head_sha')!r} does not match current head {head_sha!r}"
        )
    if str(signal.get("verdict", "")).strip().lower() not in _PASSING_VERDICTS:
        problems.append(f"review signal has blocking verdict {signal.get('verdict')!r}")
    if not signal.get("reviewer_login"):
        problems.append("review signal is missing reviewer_login")
    for field in ("critical", "important"):
        try:
            value = int(signal.get(field))
        except (TypeError, ValueError):
            problems.append(f"review signal has invalid {field} count {signal.get(field)!r}")
            continue
        if value != 0:
            problems.append(f"review signal reports {value} {field} finding(s)")
    return problems


def _published_review_matches_signal(
    reviews: List[dict],
    signal: Dict[str, object],
    head_sha: str,
) -> bool:
    reviewer_login = signal.get("reviewer_login")
    for review in reviews:
        if review.get("commit_id") != head_sha:
            continue
        if (review.get("user") or {}).get("login") != reviewer_login:
            continue
        published_signal, problems = _parse_signal(review.get("body") or "")
        if problems or published_signal is None:
            continue
        fields = ("pr", "head_sha", "verdict", "critical", "important", "reviewer_login")
        if all(published_signal.get(field) == signal.get(field) for field in fields):
            return True
    return False


def check_review_signal(repo: str, pr_number: str, head_sha: str, agent_output: str) -> List[str]:
    """Return problems; empty means the independent agent published a passing review."""
    signal, problems = _parse_signal(agent_output)
    if signal is None:
        return problems
    problems.extend(_validate_signal(signal, pr_number, head_sha))
    if problems:
        return problems
    try:
        reviews = cpc._fetch_reviews(repo, pr_number)
    except RuntimeError as exc:
        return [f"could not fetch reviews: {exc}"]
    if not _published_review_matches_signal(reviews, signal, head_sha):
        return [
            f"no current GitHub review by {signal['reviewer_login']!r} contains the matching "
            "[SIGNAL:pr-review] record"
        ]
    return []


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

    print(f"Confirmed a passing independent review for head {args.head_sha}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
