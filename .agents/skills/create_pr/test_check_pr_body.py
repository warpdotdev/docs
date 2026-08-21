#!/usr/bin/env python3
"""Unit tests for check_pr_body.py.

Stdlib unittest only, no third-party deps and no network.

Run:
    python3 .agents/skills/create_pr/test_check_pr_body.py
"""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_MODULE_PATH = _HERE / "check_pr_body.py"

_spec = importlib.util.spec_from_file_location("check_pr_body", _MODULE_PATH)
cpb = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cpb)

LEAD = "## What this feature does"

GOOD_BODY = """## What this feature does

Workspace admin roles let an owner delegate whole-workspace management -- membership,
billing, and run visibility -- without handing over ownership. Shipped in
`v0.2026.08.18.02.52.stable_00` (2026-08-18).

## Summary

Auto-drafted documentation for workspace admin roles.

## Content design plan

**Audience and JTBD:** A workspace owner onboarding a second admin.
"""


def lines(text: str):
    return text.splitlines()


class TestCheckLeadSection(unittest.TestCase):
    def test_accepts_a_well_formed_lead_section(self):
        self.assertEqual(cpb.check_lead_section(lines(GOOD_BODY), LEAD), [])

    def test_heading_is_matched_after_whitespace_normalization(self):
        self.assertEqual(cpb.check_lead_section(lines(GOOD_BODY), f"  {LEAD}  "), [])

    def test_missing_lead_section(self):
        body = "## Summary\n\nAuto-drafted documentation.\n"
        problems = cpb.check_lead_section(lines(body), LEAD)
        self.assertEqual(len(problems), 1)
        self.assertIn("missing required lead section", problems[0])

    def test_lead_section_not_first(self):
        body = (
            "## Summary\n\nAuto-drafted documentation for workspace admin roles.\n\n"
            f"{LEAD}\n\nIt lets an owner delegate workspace management. "
            "Shipped in `v1` (2026-08-18).\n"
        )
        problems = cpb.check_lead_section(lines(body), LEAD)
        self.assertEqual(len(problems), 1)
        self.assertIn("lead section is not first", problems[0])
        self.assertIn("## Summary", problems[0])

    def test_lead_section_with_no_content(self):
        body = f"{LEAD}\n\n## Summary\n\nAuto-drafted documentation.\n"
        problems = cpb.check_lead_section(lines(body), LEAD)
        self.assertEqual(len(problems), 1)
        self.assertIn("has no content under it", problems[0])

    def test_lead_section_over_word_budget(self):
        filler = " ".join(["word"] * (cpb.LEAD_SECTION_MAX_WORDS + 1))
        body = f"{LEAD}\n\n{filler}\n\n## Summary\n\nAuto-drafted documentation.\n"
        problems = cpb.check_lead_section(lines(body), LEAD)
        self.assertEqual(len(problems), 1)
        self.assertIn(f"budget: {cpb.LEAD_SECTION_MAX_WORDS}", problems[0])

    def test_lead_section_exactly_at_word_budget_is_allowed(self):
        filler = " ".join(["word"] * cpb.LEAD_SECTION_MAX_WORDS)
        body = f"{LEAD}\n\n{filler}\n\n## Summary\n\nAuto-drafted documentation.\n"
        self.assertEqual(cpb.check_lead_section(lines(body), LEAD), [])

    def test_duplicate_lead_section(self):
        body = (
            f"{LEAD}\n\nIt delegates workspace management. Shipped in `v1` (2026-08-18).\n\n"
            f"{LEAD}\n\nAgain.\n"
        )
        problems = cpb.check_lead_section(lines(body), LEAD)
        self.assertTrue(any("appears 2x" in p for p in problems), problems)

    def test_heading_inside_a_code_fence_does_not_count_as_first(self):
        """A fenced example of the template must not satisfy or displace the check."""
        body = (
            "```markdown\n## Summary\nan example\n```\n\n"
            f"{LEAD}\n\nIt delegates workspace management. Shipped in `v1` (2026-08-18).\n"
        )
        self.assertEqual(cpb.check_lead_section(lines(body), LEAD), [])


class TestMainExitCodes(unittest.TestCase):
    def _write(self, tmpdir: Path, text: str) -> str:
        path = tmpdir / "body.md"
        path.write_text(text, encoding="utf-8")
        return str(path)

    def test_exit_zero_on_good_body(self):
        import tempfile

        with tempfile.TemporaryDirectory() as d:
            path = self._write(Path(d), GOOD_BODY)
            self.assertEqual(cpb.main([path, "--require-lead-section", LEAD]), 0)

    def test_exit_one_when_lead_section_missing(self):
        import tempfile

        with tempfile.TemporaryDirectory() as d:
            path = self._write(Path(d), "## Summary\n\nAuto-drafted documentation.\n")
            self.assertEqual(cpb.main([path, "--require-lead-section", LEAD]), 1)

    def test_lead_section_check_is_opt_in(self):
        """Without the flag, a body with no lead section still passes."""
        import tempfile

        with tempfile.TemporaryDirectory() as d:
            path = self._write(Path(d), "## Summary\n\nAuto-drafted documentation.\n")
            self.assertEqual(cpb.main([path]), 0)


class TestExistingChecksStillWork(unittest.TestCase):
    def test_unbalanced_backtick_detected(self):
        issues = cpb.find_unbalanced_backticks(lines("A sentence that stops because `m\n"))
        self.assertEqual(len(issues), 1)

    def test_duplicate_heading_detected(self):
        self.assertEqual(
            cpb.find_duplicate_headings(lines("## Summary\na\n## Summary\nb\n")),
            ["## Summary"],
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
