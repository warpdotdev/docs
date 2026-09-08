#!/usr/bin/env python3
"""Unit tests for verify_review_signal.py."""
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
    '[SIGNAL:pr-review] {"pr":"1","head_sha":"sha1","reviewer_login":"github-actions[bot]",'
    '"verdict":"Approve","critical":0,"important":0}'
)
GOOD_REVIEW = {
    "user": {"login": "github-actions[bot]"},
    "state": "APPROVED",
    "commit_id": "sha1",
    "body": GOOD_OUTPUT,
}


class TestCheckReviewSignal(unittest.TestCase):
    def test_missing_published_review_fails(self):
        with mock.patch.object(vrs.cpc, "_fetch_reviews", return_value=[]):
            problems = vrs.check_review_signal("o/r", "1", "sha1", GOOD_OUTPUT)
        self.assertTrue(any("no current GitHub review" in p for p in problems))

    def test_missing_signal_fails(self):
        with mock.patch.object(vrs.cpc, "_fetch_reviews", return_value=[GOOD_REVIEW]):
            problems = vrs.check_review_signal("o/r", "1", "sha1", "review complete")
        self.assertTrue(any("expected exactly one" in p for p in problems))

    def test_repeated_identical_signal_passes(self):
        output = f"{GOOD_OUTPUT}\n\n{GOOD_OUTPUT}"
        with mock.patch.object(vrs.cpc, "_fetch_reviews", return_value=[GOOD_REVIEW]):
            problems = vrs.check_review_signal("o/r", "1", "sha1", output)
        self.assertEqual(problems, [])
    def test_ignores_malformed_marker_example_when_current_signal_is_valid(self):
        example = '[SIGNAL:pr-review] {"pr":"NNN","head_sha":"SHA","critical":N}'
        output = f"{example}\n\n{GOOD_OUTPUT}"
        with mock.patch.object(vrs.cpc, "_fetch_reviews", return_value=[GOOD_REVIEW]):
            problems = vrs.check_review_signal("o/r", "1", "sha1", output)
        self.assertEqual(problems, [])

    def test_ignores_a_valid_signal_for_an_older_head(self):
        stale_signal = GOOD_OUTPUT.replace('"sha1"', '"old-sha"')
        output = f"{stale_signal}\n\n{GOOD_OUTPUT}"
        with mock.patch.object(vrs.cpc, "_fetch_reviews", return_value=[GOOD_REVIEW]):
            problems = vrs.check_review_signal("o/r", "1", "sha1", output)
        self.assertEqual(problems, [])

    def test_escaped_action_output_signal_passes(self):
        output = GOOD_OUTPUT.replace('"', '\\"')
        with mock.patch.object(vrs.cpc, "_fetch_reviews", return_value=[GOOD_REVIEW]):
            problems = vrs.check_review_signal("o/r", "1", "sha1", output)
        self.assertEqual(problems, [])

    def test_distinct_signals_fail(self):
        different_signal = GOOD_OUTPUT.replace('"Approve"', '"Approve with nits"')
        output = f"{GOOD_OUTPUT}\n\n{different_signal}"
        with mock.patch.object(vrs.cpc, "_fetch_reviews", return_value=[GOOD_REVIEW]):
            problems = vrs.check_review_signal("o/r", "1", "sha1", output)
        self.assertTrue(any("found 2" in p for p in problems))

    def test_runner_identity_is_used_when_agent_signal_omits_it(self):
        output = GOOD_OUTPUT.replace(',"reviewer_login":"github-actions[bot]"', "")
        with mock.patch.object(vrs.cpc, "_fetch_reviews", return_value=[GOOD_REVIEW]):
            problems = vrs.check_review_signal("o/r", "1", "sha1", output)
        self.assertEqual(problems, [])

    def test_human_approval_does_not_satisfy_agent_review_requirement(self):
        human_review = {**GOOD_REVIEW, "user": {"login": "human-reviewer"}}
        with mock.patch.object(vrs.cpc, "_fetch_reviews", return_value=[human_review]):
            problems = vrs.check_review_signal("o/r", "1", "sha1", GOOD_OUTPUT)
        self.assertTrue(any("no current GitHub review" in p for p in problems))

    def test_review_without_matching_published_signal_fails(self):
        review = {**GOOD_REVIEW, "body": "Approve"}
        with mock.patch.object(vrs.cpc, "_fetch_reviews", return_value=[review]):
            problems = vrs.check_review_signal("o/r", "1", "sha1", GOOD_OUTPUT)
        self.assertTrue(any("no current GitHub review" in p for p in problems))

    def test_stale_signal_fails(self):
        stale_output = GOOD_OUTPUT.replace('"sha1"', '"old-sha"')
        with mock.patch.object(vrs.cpc, "_fetch_reviews", return_value=[GOOD_REVIEW]):
            problems = vrs.check_review_signal("o/r", "1", "sha1", stale_output, "agent-bot")
        self.assertTrue(any("found 0" in p for p in problems))

    def test_blocking_signal_fails(self):
        blocking_output = GOOD_OUTPUT.replace('"Approve"', '"Request changes"').replace('"critical":0', '"critical":1')
        with mock.patch.object(vrs.cpc, "_fetch_reviews", return_value=[GOOD_REVIEW]):
            problems = vrs.check_review_signal("o/r", "1", "sha1", blocking_output, "agent-bot")
        self.assertTrue(any("blocking verdict" in p for p in problems))
        self.assertTrue(any("critical finding" in p for p in problems))

    def test_matching_published_review_and_passing_signal_pass(self):
        with mock.patch.object(vrs.cpc, "_fetch_reviews", return_value=[GOOD_REVIEW]):
            problems = vrs.check_review_signal("o/r", "1", "sha1", GOOD_OUTPUT)
        self.assertEqual(problems, [])

    def test_fetch_failure_fails_closed(self):
        with mock.patch.object(vrs.cpc, "_fetch_reviews", side_effect=RuntimeError("boom")):
            problems = vrs.check_review_signal("o/r", "1", "sha1", GOOD_OUTPUT)
        self.assertTrue(any("could not fetch reviews" in p for p in problems))


if __name__ == "__main__":
    unittest.main()
