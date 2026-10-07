#!/usr/bin/env python3
"""Build compute_metrics.py-compatible per-PR records from the existing
per-comment `human_review_feedback.jsonl` signal log, for a pre-rollout
baseline window that predates the v1 contract (so risk/check_outcome/
review_outcome/engineering_required are genuinely unknown -- the v1 checks
did not exist yet).

`human_review_feedback.jsonl` already has real per-comment data (date, pr,
feedback_type, comment) going back to the "Improve AI-generated docs" outer
loop, but it is a comment-level log, not a per-PR record. This script:

1. Groups comment-level rows by `pr` within the requested date window.
2. Counts `human_review_comments` per PR from `review_comment` /
   `review_verdict` rows.
3. Sums the logged `Human edit after agent commit: +X -Y lines` deltas per PR
   for `human_lines_changed_after_last_agent_commit`.
4. Resolves each PR's total changed lines live via `gh pr view --json
   additions,deletions` and derives `agent_lines_changed` as
   `total - human_lines_changed_after_last_agent_commit` (floored at 0), since
   the total is real, already-merged line-change data and the human-edit
   portion is already logged separately.
5. Emits one JSONL record per PR with the v1 fields the pre-rollout window
   cannot know (`risk`, `check_outcome`, `review_outcome`,
   `engineering_required`) explicitly set to their documented "unknown"/
   not-applicable values, per compute_metrics.py's degrade-to-missing rule.

Usage:
    python3 build_baseline_records.py --repo warpdotdev/docs \
        --input .agents/logs/human_review_feedback.jsonl \
        --start 2026-08-01 --end 2026-08-30 \
        --output /tmp/baseline-records.jsonl
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import date
from pathlib import Path
from typing import Any, Dict, List, Optional


def load_comment_records(path: Path) -> List[Dict[str, Any]]:
    records = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            records.append(json.loads(line))
    return records


def _in_window(record: Dict[str, Any], start: date, end: date) -> bool:
    raw = record.get("date")
    if not raw:
        return False
    try:
        d = date.fromisoformat(raw)
    except ValueError:
        return False
    return start <= d <= end


def _human_edit_lines(comment: str) -> int:
    # "Human edit after agent commit: +40 -0 lines"
    import re

    m = re.search(r"\+(\d+)\s+-(\d+)\s+lines", comment or "")
    if not m:
        return 0
    return int(m.group(1)) + int(m.group(2))


def fetch_pr_total_changed_lines(repo: str, pr_number: str) -> Optional[int]:
    """Live `additions + deletions` for a merged/open PR, or None if unavailable."""
    result = subprocess.run(
        ["gh", "pr", "view", pr_number, "--repo", repo, "--json", "additions,deletions"],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        return None
    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        return None
    additions = data.get("additions")
    deletions = data.get("deletions")
    if additions is None or deletions is None:
        return None
    return int(additions) + int(deletions)


def build_baseline_records(
    comment_records: List[Dict[str, Any]],
    start: date,
    end: date,
    repo: str,
    *,
    fetch_total_lines=fetch_pr_total_changed_lines,
) -> List[Dict[str, Any]]:
    """Aggregate comment-level rows into one v1-shaped record per PR."""
    by_pr: Dict[str, List[Dict[str, Any]]] = {}
    for record in comment_records:
        if not _in_window(record, start, end):
            continue
        pr = record.get("pr")
        if not pr:
            continue
        by_pr.setdefault(pr, []).append(record)

    output: List[Dict[str, Any]] = []
    for pr, rows in sorted(by_pr.items(), key=lambda kv: int(kv[0]) if kv[0].isdigit() else kv[0]):
        earliest_date = min(r["date"] for r in rows if r.get("date"))
        human_review_comments = sum(
            1 for r in rows if r.get("feedback_type") in ("review_comment", "review_verdict")
        )
        human_lines = sum(
            _human_edit_lines(r.get("comment", ""))
            for r in rows if r.get("feedback_type") == "human_edit"
        )
        comment_categories: Dict[str, int] = {}
        for r in rows:
            if r.get("feedback_type") not in ("review_comment", "review_verdict"):
                continue
            category = r.get("pattern_category") or "general"
            comment_categories[category] = comment_categories.get(category, 0) + 1

        total_lines = fetch_total_lines(repo, pr)
        has_agent_commit = True
        if total_lines is None:
            # Live lookup failed (PR deleted/inaccessible) -- record the PR
            # without a churn ratio rather than fabricating a line count.
            agent_lines = 0
            has_agent_commit = False
        else:
            agent_lines = max(total_lines - human_lines, 0)

        skill_used = next((r.get("skill_used") for r in rows if r.get("skill_used") not in (None, "unknown")), "unknown")

        output.append({
            "date": earliest_date,
            "pr": pr,
            "skill_used": skill_used,
            "risk": "unknown",  # pre-rollout: the v1 contract did not exist yet
            "head_sha": "unknown",
            "check_outcome": "unknown",
            "review_outcome": "unknown",
            "review_critical": 0,
            "review_important": 0,
            "review_categories": {},
            "human_review_comments": human_review_comments,
            "human_review_comment_categories": comment_categories,
            "agent_lines_changed": agent_lines,
            "human_lines_changed_after_last_agent_commit": human_lines,
            "has_agent_commit": has_agent_commit,
            "engineering_required": False,  # pre-rollout: risk classification did not exist yet
            "completion_method": "n/a",
        })
    return output


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--input", required=True, help="path to human_review_feedback.jsonl")
    parser.add_argument("--repo", required=True, help="owner/repo to resolve PR line counts from")
    parser.add_argument("--start", required=True, help="window start date, YYYY-MM-DD (inclusive)")
    parser.add_argument("--end", required=True, help="window end date, YYYY-MM-DD (inclusive)")
    parser.add_argument("--output", required=True, help="write the resulting JSONL records here")
    args = parser.parse_args(argv)

    comment_records = load_comment_records(Path(args.input))
    start = date.fromisoformat(args.start)
    end = date.fromisoformat(args.end)
    records = build_baseline_records(comment_records, start, end, args.repo)

    with open(args.output, "w", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(record) + "\n")

    print(f"Wrote {len(records)} per-PR baseline record(s) to {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
