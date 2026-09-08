#!/usr/bin/env python3
"""Regression tests for agent-docs-review workflow eligibility and handoff."""
from __future__ import annotations

import unittest
from pathlib import Path


_REPO_ROOT = Path(__file__).resolve().parents[3]
_WORKFLOW = _REPO_ROOT / ".github/workflows/agent-docs-review.yml"


class TestAgentDocsReviewWorkflow(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workflow = _WORKFLOW.read_text(encoding="utf-8")

    def test_review_waits_until_a_draft_is_ready(self):
        self.assertIn("ready_for_review", self.workflow)
        self.assertIn("github.event.pull_request.draft == false", self.workflow)

    def test_blocking_reviews_must_supply_actionable_findings(self):
        self.assertIn("blocking_findings", self.workflow)
        self.assertIn("file and line or quoted text", self.workflow)


if __name__ == "__main__":
    unittest.main()
