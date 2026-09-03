#!/usr/bin/env python3
"""Compute the agent-doc quality baseline / outcome metrics report over a window.

Reads one JSON record per agent-authored, in-scope PR (JSONL) and emits a
deterministic JSON report plus a human-readable summary for an explicit
start/end date window. Used for both the pre-rollout 30-day baseline and the
post-rollout 30-day comparison.

Record schema (one JSON object per line; unknown/missing fields degrade to
the documented "missing" bucket rather than raising):
    {
      "date": "YYYY-MM-DD",
      "pr": "123",
      "skill_used": "draft_feature_doc",
      "risk": "low" | "engineering-review-required" | "unknown",
      "head_sha": "abc123",
      "check_outcome": "pass" | "fail" | "unknown",
      "review_outcome": "approve" | "approve_with_nits" | "request_changes" | "unknown",
      "review_critical": 0,
      "review_important": 0,
      "review_categories": {"header_case": 2},
      "human_review_comments": 3,
      "human_review_comment_categories": {"header_case": 1},
      "agent_lines_changed": 120,
      "human_lines_changed_after_last_agent_commit": 10,
      "has_agent_commit": true,
      "engineering_required": false,
      "completion_method": "n/a" | "source_owner_approval" | "docs_verified" |
                            "docs_waiver" | "unresolved_owner" | "unanswered_request"
    }

Usage:
    python3 compute_metrics.py --input records.jsonl --start 2026-01-01 --end 2026-01-30
    python3 compute_metrics.py --input records.jsonl --start 2026-01-01 --end 2026-01-30 \
        --baseline baseline.json --output report.json
"""
from __future__ import annotations

import argparse
import json
import statistics
import sys
from datetime import date
from pathlib import Path
from typing import Any, Dict, List, Optional

MIN_SAMPLE_SIZE = 10
COMPLETION_METHODS = (
    "source_owner_approval", "docs_verified", "docs_waiver",
    "unresolved_owner", "unanswered_request",
)


def load_records(path: Path) -> List[Dict[str, Any]]:
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


def _rate(numerator: int, denominator: int) -> Optional[float]:
    if denominator == 0:
        return None
    return round(numerator / denominator, 4)


def _mean_median(values: List[float]) -> Dict[str, Optional[float]]:
    if not values:
        return {"mean": None, "median": None}
    return {"mean": round(statistics.fmean(values), 4), "median": round(statistics.median(values), 4)}


def _aggregate_categories(records: List[Dict[str, Any]], field: str) -> Dict[str, int]:
    totals: Dict[str, int] = {}
    for r in records:
        for category, count in (r.get(field) or {}).items():
            totals[category] = totals.get(category, 0) + int(count)
    return dict(sorted(totals.items()))


def compute_metrics(records: List[Dict[str, Any]], start: date, end: date) -> Dict[str, Any]:
    """Compute the deterministic v1 report for records in [start, end]."""
    window_records = sorted(
        (r for r in records if _in_window(r, start, end)),
        key=lambda r: (r.get("date", ""), r.get("pr", "")),
    )

    in_scope_count = len(window_records)
    complete_gate_coverage = sum(
        1 for r in window_records
        if r.get("check_outcome") in ("pass", "fail") and r.get("review_outcome") != "unknown"
    )

    critical_total = sum(int(r.get("review_critical", 0) or 0) for r in window_records)
    important_total = sum(int(r.get("review_important", 0) or 0) for r in window_records)
    review_categories = _aggregate_categories(window_records, "review_categories")

    human_comment_counts = [int(r.get("human_review_comments", 0) or 0) for r in window_records]
    human_comment_categories = _aggregate_categories(window_records, "human_review_comment_categories")

    churn_ratios: List[float] = []
    zero_denominator_count = 0
    no_agent_commit_count = 0
    for r in window_records:
        if not r.get("has_agent_commit", True):
            no_agent_commit_count += 1
            continue
        agent_lines = int(r.get("agent_lines_changed", 0) or 0)
        human_lines = int(r.get("human_lines_changed_after_last_agent_commit", 0) or 0)
        if agent_lines == 0:
            zero_denominator_count += 1
            continue
        churn_ratios.append(human_lines / agent_lines)

    engineering_required = [r for r in window_records if r.get("engineering_required")]
    completion_counts: Dict[str, int] = {method: 0 for method in COMPLETION_METHODS}
    for r in engineering_required:
        method = r.get("completion_method")
        if method in completion_counts:
            completion_counts[method] += 1

    eng_required_total = len(engineering_required)
    completion_rates = {
        method: _rate(count, eng_required_total) for method, count in completion_counts.items()
    }

    return {
        "window": {"start": start.isoformat(), "end": end.isoformat()},
        "in_scope_prs": in_scope_count,
        "prs_with_complete_gate_coverage": complete_gate_coverage,
        "gate_coverage_missing_data_count": in_scope_count - complete_gate_coverage,
        "review_findings": {
            "critical_total": critical_total,
            "important_total": important_total,
            "critical_important_per_pr": _rate(critical_total + important_total, in_scope_count),
            "targeted_categories": review_categories,
        },
        "human_review_comments": {
            "total": sum(human_comment_counts),
            "per_pr": {**_mean_median([float(c) for c in human_comment_counts])},
            "numerator": sum(human_comment_counts),
            "denominator": in_scope_count,
            "targeted_categories": human_comment_categories,
        },
        "human_edit_churn_ratio": {
            **_mean_median(churn_ratios),
            "numerator_pr_count": len(churn_ratios),
            "denominator_pr_count": in_scope_count,
            "zero_denominator_count": zero_denominator_count,
            "no_agent_commit_count": no_agent_commit_count,
        },
        "engineering_review_required": {
            "total": eng_required_total,
            "completed_by": completion_counts,
            "completion_rates": completion_rates,
        },
    }


def evaluate_outcome(baseline: Dict[str, Any], current: Dict[str, Any]) -> Dict[str, Any]:
    """Evaluate the day-30 outcome rule against a completed baseline report.

    Returns one of `pass`, `fail`, or `inconclusive-small-sample`.
    """
    for label, report in (("baseline", baseline), ("current", current)):
        if report["in_scope_prs"] < MIN_SAMPLE_SIZE:
            return {
                "result": "inconclusive-small-sample",
                "reason": f"{label} window has only {report['in_scope_prs']} in-scope PRs "
                          f"(minimum {MIN_SAMPLE_SIZE}); extend collection to 10 PRs or 60 days, "
                          "whichever comes first.",
            }

    baseline_comments = baseline["human_review_comments"]["per_pr"]["mean"]
    current_comments = current["human_review_comments"]["per_pr"]["mean"]
    baseline_churn = baseline["human_edit_churn_ratio"]["mean"]
    current_churn = current["human_edit_churn_ratio"]["mean"]

    if baseline_comments is None or current_comments is None or baseline_churn is None or current_churn is None:
        return {
            "result": "inconclusive-small-sample",
            "reason": "one or more comparison metrics has no data in one of the windows.",
        }

    comments_not_worse = current_comments <= baseline_comments
    churn_not_worse = current_churn <= baseline_churn
    at_least_one_lower = current_comments < baseline_comments or current_churn < baseline_churn

    passed = comments_not_worse and churn_not_worse and at_least_one_lower
    return {
        "result": "pass" if passed else "fail",
        "reason": (
            f"human review comments/PR: baseline={baseline_comments} current={current_comments}; "
            f"human edit churn ratio: baseline={baseline_churn} current={current_churn}"
        ),
    }


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--input", required=True, help="JSONL file of in-scope PR records")
    parser.add_argument("--start", required=True, help="window start date, YYYY-MM-DD (inclusive)")
    parser.add_argument("--end", required=True, help="window end date, YYYY-MM-DD (inclusive)")
    parser.add_argument("--baseline", help="baseline report JSON to compare against for the day-30 outcome")
    parser.add_argument("--output", help="write the JSON report to this file (also printed to stdout)")
    args = parser.parse_args(argv)

    records = load_records(Path(args.input))
    start = date.fromisoformat(args.start)
    end = date.fromisoformat(args.end)
    report = compute_metrics(records, start, end)

    if args.baseline:
        baseline_report = json.loads(Path(args.baseline).read_text(encoding="utf-8"))
        report["day_30_outcome"] = evaluate_outcome(baseline_report, report)

    normalized = json.dumps(report, indent=2, sort_keys=True)
    print(normalized)
    if args.output:
        Path(args.output).write_text(normalized + "\n", encoding="utf-8")

    return 0


if __name__ == "__main__":
    sys.exit(main())
