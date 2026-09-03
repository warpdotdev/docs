#!/usr/bin/env python3
"""Unit tests for verify_review_signal.py.

Stubs `cpc._fetch_reviews` so these run without a live `gh` call.

Run:
    python3 .agents/skills/doc_quality_policy/test_verify_review_signal.py
"""
from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path
from unittest import mock

_HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("verify_review_signal", _HERE / "verify_review_signal.py")
vrs = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = vrs
_spec.loader.exec_module(vrs)


class TestCheckReviewSignal(unittest.TestCase):
    def test_no_review_at_all_fails(self):
        with mock.patch.object(vrs.cpc, "_fetch_reviews", return_value=[]):
            problems = vrs.check_review_signal("o/r", "1", "sha1")
        self.assertTrue(any("no review found" in p for p in problems))

    def test_stale_review_on_old_head_fails(self):
        reviews = [{"user": {"login": "bot"}, "state": "APPROVED", "commit_id": "old-sha"}]
        with mock.patch.object(vrs.cpc, "_fetch_reviews", return_value=reviews):
            problems = vrs.check_review_signal("o/r", "1", "sha1")
        self.assertTrue(any("no review found" in p for p in problems))

    def test_changes_requested_on_current_head_fails(self):
        reviews = [{"user": {"login": "bot"}, "state": "CHANGES_REQUESTED", "commit_id": "sha1"}]
        with mock.patch.object(vrs.cpc, "_fetch_reviews", return_value=reviews):
            problems = vrs.check_review_signal("o/r", "1", "sha1")
        self.assertTrue(any("requests changes" in p for p in problems))

    def test_approved_review_on_current_head_passes(self):
        reviews = [{"user": {"login": "bot"}, "state": "APPROVED", "commit_id": "sha1"}]
        with mock.patch.object(vrs.cpc, "_fetch_reviews", return_value=reviews):
            problems = vrs.check_review_signal("o/r", "1", "sha1")
        self.assertEqual(problems, [])

    def test_fetch_failure_fails_closed(self):
        with mock.patch.object(vrs.cpc, "_fetch_reviews", side_effect=RuntimeError("boom")):
            problems = vrs.check_review_signal("o/r", "1", "sha1")
        self.assertTrue(any("could not fetch reviews" in p for p in problems))

    def test_main_exit_codes(self):
        with mock.patch.object(vrs.cpc, "_fetch_reviews", return_value=[
            {"user": {"login": "bot"}, "state": "APPROVED", "commit_id": "sha1"},
        ]):
            self.assertEqual(vrs.main(["--repo", "o/r", "--pr", "1", "--head-sha", "sha1"]), 0)
        with mock.patch.object(vrs.cpc, "_fetch_reviews", return_value=[]):
            self.assertEqual(vrs.main(["--repo", "o/r", "--pr", "1", "--head-sha", "sha1"]), 1)


if __name__ == "__main__":
    unittest.main()
