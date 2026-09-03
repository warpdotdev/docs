#!/usr/bin/env python3
"""Unit tests for build_baseline_records.py.

Run:
    python3 .agents/skills/improve-drafting-skills/scripts/test_build_baseline_records.py
"""
from __future__ import annotations

import importlib.util
import unittest
from datetime import date
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("build_baseline_records", _HERE / "build_baseline_records.py")
bbr = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(bbr)


def _fake_fetch(totals):
    def fetch(repo, pr):
        return totals.get(pr)
    return fetch


class TestHumanEditLines(unittest.TestCase):
    def test_parses_plus_minus_lines(self):
        self.assertEqual(bbr._human_edit_lines("Human edit after agent commit: +40 -12 lines"), 52)

    def test_no_match_returns_zero(self):
        self.assertEqual(bbr._human_edit_lines("no match here"), 0)


class TestBuildBaselineRecords(unittest.TestCase):
    def test_aggregates_comments_and_human_lines_per_pr(self):
        comments = [
            {"date": "2026-08-05", "pr": "100", "feedback_type": "review_verdict", "comment": "x", "pattern_category": "general"},
            {"date": "2026-08-05", "pr": "100", "feedback_type": "human_edit", "comment": "Human edit after agent commit: +10 -5 lines", "pattern_category": "callout"},
            {"date": "2026-08-06", "pr": "100", "feedback_type": "review_comment", "comment": "nit", "pattern_category": "general"},
        ]
        records = bbr.build_baseline_records(
            comments, date(2026, 8, 1), date(2026, 8, 31), "o/r",
            fetch_total_lines=_fake_fetch({"100": 40}),
        )
        self.assertEqual(len(records), 1)
        record = records[0]
        self.assertEqual(record["pr"], "100")
        self.assertEqual(record["human_review_comments"], 2)
        self.assertEqual(record["human_lines_changed_after_last_agent_commit"], 15)
        self.assertEqual(record["agent_lines_changed"], 25)  # 40 - 15
        self.assertEqual(record["risk"], "unknown")
        self.assertFalse(record["engineering_required"])
        self.assertTrue(record["has_agent_commit"])

    def test_excludes_records_outside_window(self):
        comments = [
            {"date": "2026-07-01", "pr": "1", "feedback_type": "review_verdict", "comment": "x"},
        ]
        records = bbr.build_baseline_records(
            comments, date(2026, 8, 1), date(2026, 8, 31), "o/r",
            fetch_total_lines=_fake_fetch({}),
        )
        self.assertEqual(records, [])

    def test_failed_line_lookup_marks_no_agent_commit(self):
        comments = [
            {"date": "2026-08-05", "pr": "200", "feedback_type": "review_verdict", "comment": "x"},
        ]
        records = bbr.build_baseline_records(
            comments, date(2026, 8, 1), date(2026, 8, 31), "o/r",
            fetch_total_lines=_fake_fetch({}),  # PR "200" not found
        )
        self.assertEqual(len(records), 1)
        self.assertFalse(records[0]["has_agent_commit"])
        self.assertEqual(records[0]["agent_lines_changed"], 0)

    def test_negative_derived_agent_lines_floors_at_zero(self):
        # If logged human-edit lines somehow exceed the PR's total (e.g. a
        # human reverted content the agent never counted), never go negative.
        comments = [
            {"date": "2026-08-05", "pr": "300", "feedback_type": "human_edit", "comment": "Human edit after agent commit: +50 -50 lines"},
        ]
        records = bbr.build_baseline_records(
            comments, date(2026, 8, 1), date(2026, 8, 31), "o/r",
            fetch_total_lines=_fake_fetch({"300": 10}),
        )
        self.assertEqual(records[0]["agent_lines_changed"], 0)


if __name__ == "__main__":
    unittest.main()
