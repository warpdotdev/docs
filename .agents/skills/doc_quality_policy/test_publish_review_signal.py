#!/usr/bin/env python3
"""Unit tests for publish_review_signal.py."""
from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("publish_review_signal", _HERE / "publish_review_signal.py")
prs = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = prs
_spec.loader.exec_module(prs)


def _signal(
    verdict: str = "Approve",
    critical: int = 0,
    important: int = 0,
    blocking_findings: list[str] | None = None,
) -> str:
    signal = {
        "pr": "1",
        "head_sha": "sha1",
        "verdict": verdict,
        "critical": critical,
        "important": important,
        "suggestions": 0,
        "nits": 0,
        "top_categories": [],
    }
    if blocking_findings is not None:
        signal["blocking_findings"] = blocking_findings
    return f"[SIGNAL:pr-review] {json.dumps(signal)}"


class TestBuildReviewPayload(unittest.TestCase):
    def test_approve_maps_to_non_blocking_github_comment(self):
        payload = prs.build_review_payload(_signal(), "1", "sha1", "github-actions[bot]")
        self.assertEqual(payload["event"], "COMMENT")
        self.assertEqual(payload["commit_id"], "sha1")
        self.assertIn("## Verdict\nApprove", payload["body"])
        self.assertNotIn("## Review signal", payload["body"])
        self.assertIn("<!-- [SIGNAL:pr-review]", payload["body"])
        self.assertIn('"reviewer_login": "github-actions[bot]"', payload["body"])
        published_signal, problems = prs.vrs._parse_signal(
            payload["body"], "1", "sha1"
        )
        self.assertEqual(problems, [])
        self.assertEqual(published_signal["reviewer_login"], "github-actions[bot]")

    def test_approve_with_nits_maps_to_non_blocking_github_comment(self):
        payload = prs.build_review_payload(
            _signal("Approve with nits"), "1", "sha1", "github-actions[bot]"
        )
        self.assertEqual(payload["event"], "COMMENT")

    def test_request_changes_maps_to_non_blocking_github_comment(self):
        payload = prs.build_review_payload(
            _signal(
                "Request changes",
                important=1,
                blocking_findings=[
                    "`src/content/docs/example.mdx:42` — Use the canonical subagent "
                    "terminology. Requested change: replace `children` with `subagents`."
                ],
            ),
            "1",
            "sha1",
            "github-actions[bot]",
        )
        self.assertEqual(payload["event"], "COMMENT")
        self.assertIn("canonical subagent terminology", payload["body"])

    def test_request_changes_underscore_spelling_maps_to_non_blocking_comment(self):
        payload = prs.build_review_payload(
            _signal(
                "request_changes",
                important=1,
                blocking_findings=[
                    "`src/content/docs/example.mdx:42` — Use the canonical subagent "
                    "terminology. Requested change: replace `children` with `subagents`."
                ],
            ),
            "1",
            "sha1",
            "github-actions[bot]",
        )
        self.assertEqual(payload["event"], "COMMENT")

    def test_rejects_blocking_verdict_without_actionable_findings(self):
        with self.assertRaisesRegex(ValueError, "blocking_findings"):
            prs.build_review_payload(
                _signal("Request changes", important=1),
                "1",
                "sha1",
                "github-actions[bot]",
            )

    def test_rejects_signal_for_another_head(self):
        with self.assertRaises(ValueError):
            prs.build_review_payload(_signal(), "1", "other-sha", "github-actions[bot]")


if __name__ == "__main__":
    unittest.main()
