#!/usr/bin/env python3
"""Unit tests for verify_review_signal.py.

Stubs `cpc._fetch_reviews` so these run without a live `gh` call.
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

GOOD_OUTPUT = (
    '[SIGNAL:pr-review] {"pr":"1","head_sha":"sha1",'
    '"verdict":"Approve","critical":0,"important":0}'
)


class TestCheckReviewSignal(unittest.TestCase):
    def test_no_review_at_all_fails(self):
        with mock.patch.object(vrs.cpc, "_fetch_reviews", return_value=[]):
            problems = vrs.check_review_signal("o/r", "1", "sha1", GOOD_OUTPUT)
        self.assertTrue(any("no review found" in p for p in problems))

    def test_missing_signal_fails(self):
        reviews = [{"user": {"login": "bot"}, "state": "APPROVED", "commit_id": "sha1"}]
        with mock.patch.object(vrs.cpc, "_fetch_reviews", return_value=reviews):
            problems = vrs.check_review_signal("o/r", "1", "sha1", "review complete")
        self.assertTrue(any("expected exactly one" in p for p in problems))

    def test_stale_signal_fails(self):
        reviews = [{"user": {"login": "bot"}, "state": "APPROVED", "commit_id": "sha1"}]
        stale_output = GOOD_OUTPUT.replace('"sha1"', '"old-sha"')
        with mock.patch.object(vrs.cpc, "_fetch_reviews", return_value=reviews):
            problems = vrs.check_review_signal("o/r", "1", "sha1", stale_output)
        self.assertTrue(any("does not match current head" in p for p in problems))

    def test_blocking_signal_fails(self):
        reviews = [{"user": {"login": "bot"}, "state": "APPROVED", "commit_id": "sha1"}]
        blocking_output = GOOD_OUTPUT.replace('"Approve"', '"Request changes"').replace('"critical":0', '"critical":1')
        with mock.patch.object(vrs.cpc, "_fetch_reviews", return_value=reviews):
            problems = vrs.check_review_signal("o/r", "1", "sha1", blocking_output)
        self.assertTrue(any("blocking verdict" in p for p in problems))
        self.assertTrue(any("critical finding" in p for p in problems))

    def test_changes_requested_on_current_head_fails(self):
        reviews = [{"user": {"login": "bot"}, "state": "CHANGES_REQUESTED", "commit_id": "sha1"}]
        with mock.patch.object(vrs.cpc, "_fetch_reviews", return_value=reviews):
            problems = vrs.check_review_signal("o/r", "1", "sha1", GOOD_OUTPUT)
        self.assertTrue(any("requests changes" in p for p in problems))

    def test_approved_review_and_passing_signal_on_current_head_passes(self):
        reviews = [{"user": {"login": "bot"}, "state": "APPROVED", "commit_id": "sha1"}]
        with mock.patch.object(vrs.cpc, "_fetch_reviews", return_value=reviews):
            problems = vrs.check_review_signal("o/r", "1", "sha1", GOOD_OUTPUT)
        self.assertEqual(problems, [])

    def test_fetch_failure_fails_closed(self):
        with mock.patch.object(vrs.cpc, "_fetch_reviews", side_effect=RuntimeError("boom")):
            problems = vrs.check_review_signal("o/r", "1", "sha1", GOOD_OUTPUT)
        self.assertTrue(any("could not fetch reviews" in p for p in problems))


if __name__ == "__main__":
    unittest.main()
