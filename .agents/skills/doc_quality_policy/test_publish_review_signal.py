#!/usr/bin/env python3
"""Unit tests for publish_review_signal.py."""
from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("publish_review_signal", _HERE / "publish_review_signal.py")
prs = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = prs
_spec.loader.exec_module(prs)


def _signal(verdict: str = "Approve") -> str:
    return (
        '[SIGNAL:pr-review] {"pr":"1","head_sha":"sha1",'
        f'"verdict":"{verdict}","critical":0,"important":0,'
        '"suggestions":0,"nits":0,"top_categories":[]}'
    )


class TestBuildReviewPayload(unittest.TestCase):
    def test_approve_maps_to_github_approval(self):
        payload = prs.build_review_payload(_signal(), "1", "sha1", "github-actions[bot]")
        self.assertEqual(payload["event"], "APPROVE")
        self.assertEqual(payload["commit_id"], "sha1")
        self.assertIn("## Verdict\nApprove", payload["body"])
        self.assertIn('"reviewer_login": "github-actions[bot]"', payload["body"])

    def test_approve_with_nits_maps_to_github_approval(self):
        payload = prs.build_review_payload(
            _signal("Approve with nits"), "1", "sha1", "github-actions[bot]"
        )
        self.assertEqual(payload["event"], "APPROVE")

    def test_request_changes_maps_to_github_change_request(self):
        payload = prs.build_review_payload(
            _signal("Request changes"), "1", "sha1", "github-actions[bot]"
        )
        self.assertEqual(payload["event"], "REQUEST_CHANGES")

    def test_rejects_signal_for_another_head(self):
        with self.assertRaises(ValueError):
            prs.build_review_payload(_signal(), "1", "other-sha", "github-actions[bot]")


if __name__ == "__main__":
    unittest.main()
