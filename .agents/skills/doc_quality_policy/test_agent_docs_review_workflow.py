#!/usr/bin/env python3
"""Regression tests for agent-docs-review workflow eligibility and handoff."""
from __future__ import annotations

import re
import unittest
from pathlib import Path


_REPO_ROOT = Path(__file__).resolve().parents[3]
_WORKFLOW = _REPO_ROOT / ".github/workflows/agent-docs-review.yml"


class TestAgentDocsReviewWorkflow(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workflow = _WORKFLOW.read_text(encoding="utf-8")

    def test_review_waits_until_a_draft_is_ready(self):
        trigger = re.search(
            r"^on:\n  pull_request:\n    types: \[([^\]]+)\]",
            self.workflow,
            re.MULTILINE,
        )
        self.assertIsNotNone(trigger)
        trigger_types = {
            event.strip() for event in trigger.group(1).split(",")
        }
        self.assertIn("ready_for_review", trigger_types)
        self.assertIn("github.event.pull_request.draft == false", self.workflow)

    def test_all_review_findings_must_supply_actionable_details(self):
        self.assertIn("actionable_findings", self.workflow)
        self.assertIn("critical, important, suggestion, or nit", self.workflow)
        self.assertIn("file and line or quoted text", self.workflow)

    def test_review_signal_is_passed_through_a_file(self):
        self.assertIn('oz "${args[@]}" > /tmp/agent-output.txt', self.workflow)
        self.assertIn("--agent-output /tmp/agent-output.txt", self.workflow)
        self.assertNotIn(".agent-docs-review-signal.txt", self.workflow)
        self.assertNotIn(
            "AGENT_OUTPUT: ${{ steps.oz-review.outputs.agent_output }}", self.workflow
        )

    def test_review_uses_a_signed_oz_package(self):
        self.assertIn("0913165C78D5B7A41B42AC657FF7AB39D60F803F", self.workflow)
        self.assertIn("signed-by=/etc/apt/keyrings/warpdotdev.gpg", self.workflow)
        self.assertIn("sudo apt-get install -y oz-stable", self.workflow)


if __name__ == "__main__":
    unittest.main()
