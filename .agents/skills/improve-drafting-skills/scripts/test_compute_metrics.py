#!/usr/bin/env python3
"""Unit tests for compute_metrics.py.

Run:
    python3 .agents/skills/improve-drafting-skills/scripts/test_compute_metrics.py
"""
from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from datetime import date
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("compute_metrics", _HERE / "compute_metrics.py")
cm = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cm)


def _record(**overrides):
    base = {
        "date": "2026-01-10",
        "pr": "1",
        "skill_used": "draft_feature_doc",
        "risk": "low",
        "head_sha": "sha1",
        "check_outcome": "pass",
        "review_outcome": "approve",
        "review_critical": 0,
        "review_important": 0,
        "review_categories": {},
        "human_review_comments": 2,
        "human_review_comment_categories": {"header_case": 1},
        "agent_lines_changed": 100,
        "human_lines_changed_after_last_agent_commit": 10,
        "has_agent_commit": True,
        "engineering_required": False,
        "completion_method": "n/a",
    }
    base.update(overrides)
    return base


class TestWindowFiltering(unittest.TestCase):
    def test_excludes_records_outside_window(self):
        records = [_record(date="2025-12-31", pr="0"), _record(date="2026-01-15", pr="1")]
        report = cm.compute_metrics(records, date(2026, 1, 1), date(2026, 1, 31))
        self.assertEqual(report["in_scope_prs"], 1)

    def test_missing_date_is_excluded(self):
        records = [{"pr": "no-date"}]
        report = cm.compute_metrics(records, date(2026, 1, 1), date(2026, 1, 31))
        self.assertEqual(report["in_scope_prs"], 0)


class TestChurnAndComments(unittest.TestCase):
    def test_churn_ratio_computed_correctly(self):
        records = [_record(agent_lines_changed=100, human_lines_changed_after_last_agent_commit=25)]
        report = cm.compute_metrics(records, date(2026, 1, 1), date(2026, 1, 31))
        self.assertEqual(report["human_edit_churn_ratio"]["mean"], 0.25)

    def test_zero_denominator_reported_separately(self):
        records = [_record(agent_lines_changed=0, human_lines_changed_after_last_agent_commit=5)]
        report = cm.compute_metrics(records, date(2026, 1, 1), date(2026, 1, 31))
        self.assertEqual(report["human_edit_churn_ratio"]["zero_denominator_count"], 1)
        self.assertIsNone(report["human_edit_churn_ratio"]["mean"])

    def test_no_agent_commit_reported_separately(self):
        records = [_record(has_agent_commit=False)]
        report = cm.compute_metrics(records, date(2026, 1, 1), date(2026, 1, 31))
        self.assertEqual(report["human_edit_churn_ratio"]["no_agent_commit_count"], 1)

    def test_human_comment_categories_aggregate_across_records(self):
        records = [
            _record(pr="1", human_review_comment_categories={"header_case": 2}),
            _record(pr="2", human_review_comment_categories={"header_case": 1, "link_quality": 3}),
        ]
        report = cm.compute_metrics(records, date(2026, 1, 1), date(2026, 1, 31))
        self.assertEqual(
            report["human_review_comments"]["targeted_categories"],
            {"header_case": 3, "link_quality": 3},
        )


class TestEngineeringReviewCompletion(unittest.TestCase):
    def test_completion_rates_computed_per_method(self):
        records = [
            _record(pr="1", engineering_required=True, completion_method="source_owner_approval"),
            _record(pr="2", engineering_required=True, completion_method="docs_verified"),
            _record(pr="3", engineering_required=True, completion_method="unresolved_owner"),
            _record(pr="4", engineering_required=False),
        ]
        report = cm.compute_metrics(records, date(2026, 1, 1), date(2026, 1, 31))
        eng = report["engineering_review_required"]
        self.assertEqual(eng["total"], 3)
        self.assertEqual(eng["completed_by"]["source_owner_approval"], 1)
        self.assertEqual(eng["completed_by"]["docs_verified"], 1)
        self.assertEqual(eng["completed_by"]["unresolved_owner"], 1)
        self.assertAlmostEqual(eng["completion_rates"]["source_owner_approval"], 1 / 3, places=4)


class TestGatePassRate(unittest.TestCase):
    def test_all_passed_required_checks_true_when_every_pr_passes(self):
        records = [_record(pr="1"), _record(pr="2")]  # check_outcome=pass, review_outcome=approve by default
        report = cm.compute_metrics(records, date(2026, 1, 1), date(2026, 1, 31))
        self.assertEqual(report["prs_with_passing_checks"], 2)
        self.assertTrue(report["all_passed_required_checks"])

    def test_all_passed_required_checks_false_when_one_pr_failed_checks(self):
        records = [_record(pr="1"), _record(pr="2", check_outcome="fail")]
        report = cm.compute_metrics(records, date(2026, 1, 1), date(2026, 1, 31))
        self.assertEqual(report["prs_with_passing_checks"], 1)
        self.assertFalse(report["all_passed_required_checks"])

    def test_failed_check_still_counts_as_complete_gate_coverage(self):
        # A failed check is data, not missing data -- coverage tracks
        # whether the gate reported an outcome, separately from whether it passed.
        records = [_record(pr="1", check_outcome="fail")]
        report = cm.compute_metrics(records, date(2026, 1, 1), date(2026, 1, 31))
        self.assertEqual(report["prs_with_complete_gate_coverage"], 1)
        self.assertEqual(report["gate_coverage_missing_data_count"], 0)
        self.assertFalse(report["all_passed_required_checks"])

    def test_missing_review_outcome_is_incomplete_gate_coverage(self):
        record = _record(pr="1")
        del record["review_outcome"]
        report = cm.compute_metrics([record], date(2026, 1, 1), date(2026, 1, 31))
        self.assertEqual(report["prs_with_complete_gate_coverage"], 0)
        self.assertEqual(report["gate_coverage_missing_data_count"], 1)

    def test_request_changes_review_outcome_is_not_passing(self):
        records = [_record(pr="1", review_outcome="request_changes")]
        report = cm.compute_metrics(records, date(2026, 1, 1), date(2026, 1, 31))
        self.assertEqual(report["prs_with_passing_checks"], 0)
        self.assertFalse(report["all_passed_required_checks"])

    def test_no_in_scope_prs_is_not_trivially_all_passed(self):
        report = cm.compute_metrics([], date(2026, 1, 1), date(2026, 1, 31))
        self.assertFalse(report["all_passed_required_checks"])


class TestReproducibility(unittest.TestCase):
    def test_running_twice_over_frozen_dates_is_byte_equivalent(self):
        records = [
            _record(pr=str(i), date=f"2026-01-{10 + (i % 15):02d}")
            for i in range(15)
        ]
        with tempfile.TemporaryDirectory() as tmp:
            input_path = Path(tmp) / "records.jsonl"
            with open(input_path, "w", encoding="utf-8") as f:
                for r in records:
                    f.write(json.dumps(r) + "\n")

            out1 = Path(tmp) / "out1.json"
            out2 = Path(tmp) / "out2.json"
            cm.main(["--input", str(input_path), "--start", "2026-01-01", "--end", "2026-01-31", "--output", str(out1)])
            cm.main(["--input", str(input_path), "--start", "2026-01-01", "--end", "2026-01-31", "--output", str(out2)])
            self.assertEqual(out1.read_text(encoding="utf-8"), out2.read_text(encoding="utf-8"))


class TestOutcomeEvaluation(unittest.TestCase):
    def _report(self, in_scope, comments_mean, churn_mean, all_passed_required_checks=True):
        return {
            "in_scope_prs": in_scope,
            "human_review_comments": {"per_pr": {"mean": comments_mean}},
            "human_edit_churn_ratio": {"mean": churn_mean},
            "all_passed_required_checks": all_passed_required_checks,
            "prs_with_passing_checks": in_scope if all_passed_required_checks else in_scope - 1,
            "prs_with_complete_gate_coverage": in_scope,
            "gate_coverage_missing_data_count": 0,
        }

    def test_small_sample_is_inconclusive(self):
        baseline = self._report(5, 3.0, 0.2)
        current = self._report(12, 2.0, 0.1)
        outcome = cm.evaluate_outcome(baseline, current)
        self.assertEqual(outcome["result"], "inconclusive-small-sample")

    def test_pass_when_both_improve_or_hold(self):
        baseline = self._report(12, 3.0, 0.3)
        current = self._report(12, 2.0, 0.3)
        outcome = cm.evaluate_outcome(baseline, current)
        self.assertEqual(outcome["result"], "pass")

    def test_fail_when_either_regresses(self):
        baseline = self._report(12, 3.0, 0.2)
        current = self._report(12, 3.5, 0.1)
        outcome = cm.evaluate_outcome(baseline, current)
        self.assertEqual(outcome["result"], "fail")

    def test_fail_when_neither_improves(self):
        baseline = self._report(12, 3.0, 0.2)
        current = self._report(12, 3.0, 0.2)
        outcome = cm.evaluate_outcome(baseline, current)
        self.assertEqual(outcome["result"], "fail")

    def test_fail_when_not_every_current_pr_passed_required_checks(self):
        # Regression: comments/churn improving must not paper over a PR that
        # didn't actually pass the required editorial/technical/review gates.
        baseline = self._report(12, 3.0, 0.3)
        current = self._report(12, 1.0, 0.1, all_passed_required_checks=False)
        outcome = cm.evaluate_outcome(baseline, current)
        self.assertEqual(outcome["result"], "fail")
        self.assertIn("passed the required", outcome["reason"])

    def test_fail_when_current_gate_coverage_is_incomplete(self):
        baseline = self._report(12, 3.0, 0.3)
        current = self._report(12, 1.0, 0.1)
        current["prs_with_complete_gate_coverage"] = 11
        current["gate_coverage_missing_data_count"] = 1
        outcome = cm.evaluate_outcome(baseline, current)
        self.assertEqual(outcome["result"], "fail")
        self.assertIn("complete", outcome["reason"])


class TestSummary(unittest.TestCase):
    def test_summary_is_human_readable(self):
        report = cm.compute_metrics([_record()], date(2026, 1, 1), date(2026, 1, 31))
        summary = cm.format_summary(report)
        self.assertIn("Window: 2026-01-01 to 2026-01-31", summary)
        self.assertIn("Gate coverage:", summary)


if __name__ == "__main__":
    unittest.main()
