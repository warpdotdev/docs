#!/usr/bin/env python3
"""Regression tests for moved-settings-control detection in validate_ui_path.

Covers QUALITY-2052: neither `validate_ui_refs` nor `missing_docs` caught the
2026.04.22 settings reorg that moved four controls from
`Settings > Features > General` to `Settings > Code > Editor and Code Review`
(fixed in docs PR #708, originally reported in docs#587). The root cause is
that `sub_sections` in `valid_paths.json` only tracks section-header-level
names ("General" is still a real sub-section of "Features"), so a path that
names an individual control past that level was never inspected at all —
`validate_ui_path` returned `valid: True` purely because "Features" and
"General" both still exist, regardless of what control name followed.

These tests exercise the `moved_settings_controls` mechanism added to close
that gap: a hand-curated list (mirroring `deprecated_sections`) of specific
controls known to have relocated, checked via `_check_moved_control`.

Run:
    python3 .agents/skills/validate_ui_refs/test_moved_controls.py
"""
from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("validate_ui_refs", _HERE / "validate_ui_refs.py")
vur = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(vur)


_MOVED_CONTROLS = [
    {
        "label": "Group files into single editor pane",
        "aliases": ["Group files into a single editor pane"],
        "old_path": "Settings > Features > General",
        "new_path": "Settings > Code > Editor and Code Review",
        "moved_in": "test fixture",
    },
]

_BASE_VALID_PATHS = {
    "umbrellas": {
        "Code": {
            "subpages": ["Indexing and projects", "Editor and Code Review"],
        },
    },
    "deprecated_sections": {},
    "settings_sections": {
        "Features": {
            "sub_sections": ["General", "Session"],
        },
        "Editor and Code Review": {
            "sub_sections": [],
            "umbrella": "Code",
        },
        "Indexing and projects": {
            "sub_sections": [],
            "umbrella": "Code",
        },
    },
    "macos_menu_bar": {},
    "warp_drive": {},
}


def _valid_paths(moved_controls):
    data = dict(_BASE_VALID_PATHS)
    data["moved_settings_controls"] = moved_controls
    return data


class TestMovedControlDetection(unittest.TestCase):
    """Regression for QUALITY-2052."""

    def test_stale_path_to_moved_control_is_flagged(self):
        """The exact stale pattern from docs PR #708 must now be caught.

        Before the fix, this returned valid=True because "Features" and
        "General" are both still real names in valid_paths.json — nothing
        ever looked at the fourth segment.
        """
        result = vur.validate_ui_path(
            "Settings > Features > General > Group files into single editor pane",
            _valid_paths(_MOVED_CONTROLS),
        )
        self.assertFalse(result["valid"])
        self.assertEqual(result["fix_type"], "moved_control")
        self.assertIn(
            "Settings > Code > Editor and Code Review > Group files into single editor pane",
            result["suggestion"],
        )

    def test_alias_wording_is_also_flagged(self):
        """The original (pre-PR-708) docs wording used a slightly different
        label ("a single editor pane" vs "single editor pane"); the alias
        list must catch that phrasing too, not just the canonical label.
        """
        result = vur.validate_ui_path(
            "Settings > Features > General > Group files into a single editor pane",
            _valid_paths(_MOVED_CONTROLS),
        )
        self.assertFalse(result["valid"])
        self.assertEqual(result["fix_type"], "moved_control")

    def test_corrected_path_validates_cleanly(self):
        """The path docs PR #708 actually landed must not be flagged."""
        result = vur.validate_ui_path(
            "Settings > Code > Editor and Code Review > Group files into single editor pane",
            _valid_paths(_MOVED_CONTROLS),
        )
        self.assertTrue(result["valid"])

    def test_unrelated_control_under_same_still_valid_subsection_is_unaffected(self):
        """Other, unrelated controls under Settings > Features > General must
        still validate normally (the fix must not over-flag)."""
        result = vur.validate_ui_path(
            "Settings > Features > General > Some unrelated toggle",
            _valid_paths(_MOVED_CONTROLS),
        )
        self.assertTrue(result["valid"])

    def test_no_moved_controls_configured_is_a_no_op(self):
        """An empty/missing moved_settings_controls list must not change
        behavior — this keeps the mechanism strictly additive."""
        result = vur.validate_ui_path(
            "Settings > Features > General > Group files into single editor pane",
            _valid_paths([]),
        )
        self.assertTrue(result["valid"])


class TestCheckMovedControlHelper(unittest.TestCase):
    def test_returns_none_when_trailing_segments_empty(self):
        self.assertIsNone(
            vur._check_moved_control(["Features", "General"], [], _MOVED_CONTROLS)
        )

    def test_returns_none_when_already_at_new_location(self):
        self.assertIsNone(
            vur._check_moved_control(
                ["Code", "Editor and Code Review"],
                ["Group files into single editor pane"],
                _MOVED_CONTROLS,
            )
        )

    def test_case_insensitive_match(self):
        result = vur._check_moved_control(
            ["Features", "General"],
            ["group files into single editor pane"],
            _MOVED_CONTROLS,
        )
        self.assertIsNotNone(result)
        self.assertEqual(result["fix_type"], "moved_control")


if __name__ == "__main__":
    unittest.main()
