#!/usr/bin/env python3
"""Unit tests for check_new_release.py.

Stdlib only, no network. The fetch is stubbed so the gate logic can be tested
deterministically -- the point of these tests is the decision the gate makes, not
whether app.warp.dev is reachable.

Run:
    python3 .agents/skills/missing_docs/scripts/test_check_new_release.py
"""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))

import check_new_release as gate  # noqa: E402


SAMPLE_CHANGELOG = {
    "date": "2026-08-18T14:15:48Z",
    "markdown_sections": [
        {"title": "Improvements", "markdown": "* First thing. ([#1](url))\n* Second thing. ([#2](url))"},
        {"title": "Bug fixes", "markdown": "* A fix. ([#3](url))"},
    ],
    "oz_updates": ["An Automation Platform update. ([#4](url))"],
}


def make_payload(version: str = "v0.2026.08.18.02.52.stable_00") -> dict:
    return {
        "stable": {"version": version},
        "changelogs": {"stable": {version: SAMPLE_CHANGELOG}},
    }


class FetchTests(unittest.TestCase):
    def test_parses_version_date_and_changelog(self):
        with mock.patch.object(gate, "urllib") as urllib_mock:
            urllib_mock.request.urlopen.return_value.__enter__.return_value = (
                _JsonResponse(make_payload())
            )
            version, date, changelog = gate.fetch_current_stable()
        self.assertEqual(version, "v0.2026.08.18.02.52.stable_00")
        self.assertEqual(date, "2026-08-18T14:15:48Z")
        self.assertEqual(len(changelog["oz_updates"]), 1)

    def test_missing_stable_version_raises(self):
        with mock.patch.object(gate, "urllib") as urllib_mock:
            urllib_mock.request.urlopen.return_value.__enter__.return_value = (
                _JsonResponse({"beta": {"version": "x"}})
            )
            with self.assertRaises(RuntimeError) as ctx:
                gate.fetch_current_stable()
        self.assertIn("stable.version", str(ctx.exception))

    def test_empty_version_raises(self):
        with mock.patch.object(gate, "urllib") as urllib_mock:
            urllib_mock.request.urlopen.return_value.__enter__.return_value = (
                _JsonResponse({"stable": {"version": ""}})
            )
            with self.assertRaises(RuntimeError):
                gate.fetch_current_stable()

    def test_absent_changelog_is_tolerated(self):
        """A release with no changelog entry should still gate correctly."""
        with mock.patch.object(gate, "urllib") as urllib_mock:
            urllib_mock.request.urlopen.return_value.__enter__.return_value = (
                _JsonResponse({"stable": {"version": "v1"}, "changelogs": {"stable": {}}})
            )
            version, date, changelog = gate.fetch_current_stable()
        self.assertEqual(version, "v1")
        self.assertIsNone(date)
        self.assertEqual(changelog, {})


class StateTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.state_path = Path(self._tmp.name) / "last_release_processed.json"

    def tearDown(self):
        self._tmp.cleanup()

    def test_missing_state_reads_as_empty(self):
        self.assertEqual(gate.read_state(self.state_path), {})

    def test_corrupt_state_reads_as_empty_not_crash(self):
        """A corrupt state file must not wedge the pipeline -- it re-processes instead."""
        self.state_path.write_text("{not json", encoding="utf-8")
        self.assertEqual(gate.read_state(self.state_path), {})

    def test_non_dict_state_reads_as_empty(self):
        self.state_path.write_text('["unexpected"]', encoding="utf-8")
        self.assertEqual(gate.read_state(self.state_path), {})

    def test_write_then_read_round_trip(self):
        gate.write_state(self.state_path, "v1", "2026-08-18T14:15:48Z", SAMPLE_CHANGELOG)
        state = gate.read_state(self.state_path)
        self.assertEqual(state["last_processed_version"], "v1")
        self.assertEqual(state["release_date"], "2026-08-18T14:15:48Z")

    def test_write_counts_changelog_entries_across_sections(self):
        gate.write_state(self.state_path, "v1", None, SAMPLE_CHANGELOG)
        state = json.loads(self.state_path.read_text(encoding="utf-8"))
        self.assertEqual(state["changelog_entry_count"], 3)
        self.assertEqual(state["oz_updates_count"], 1)

    def test_write_creates_parent_directory(self):
        nested = Path(self._tmp.name) / "deep" / "nested" / "state.json"
        gate.write_state(nested, "v1", None, {})
        self.assertTrue(nested.exists())


class ExitCodeTests(unittest.TestCase):
    """The exit codes are the skill's contract -- assert them explicitly."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.state_path = Path(self._tmp.name) / "state.json"

    def tearDown(self):
        self._tmp.cleanup()

    def _run(self, argv, fetch_result=None, fetch_error=None):
        args = ["check_new_release.py", "--state", str(self.state_path)] + argv
        patcher = (
            mock.patch.object(gate, "fetch_current_stable", side_effect=fetch_error)
            if fetch_error
            else mock.patch.object(gate, "fetch_current_stable", return_value=fetch_result)
        )
        with mock.patch.object(sys, "argv", args), patcher:
            return gate.main()

    def test_new_release_exits_zero(self):
        code = self._run([], fetch_result=("v2", "2026-08-18T00:00:00Z", SAMPLE_CHANGELOG))
        self.assertEqual(code, gate.EXIT_NEW_RELEASE)

    def test_same_release_exits_ten(self):
        gate.write_state(self.state_path, "v2", None, {})
        code = self._run([], fetch_result=("v2", None, SAMPLE_CHANGELOG))
        self.assertEqual(code, gate.EXIT_NO_NEW_RELEASE)

    def test_fetch_failure_exits_one_not_ten(self):
        """A fetch failure must never be mistaken for 'nothing shipped'."""
        code = self._run([], fetch_error=RuntimeError("network down"))
        self.assertEqual(code, gate.EXIT_FETCH_FAILED)
        self.assertNotEqual(code, gate.EXIT_NO_NEW_RELEASE)

    def test_check_does_not_write_state(self):
        """The check is read-only; only --commit writes. This is what makes a
        crashed run retry the same release instead of skipping it."""
        self._run([], fetch_result=("v2", None, SAMPLE_CHANGELOG))
        self.assertFalse(self.state_path.exists())

    def test_commit_writes_state_and_exits_zero(self):
        code = self._run(["--commit"], fetch_result=("v2", None, SAMPLE_CHANGELOG))
        self.assertEqual(code, gate.EXIT_NEW_RELEASE)
        self.assertEqual(gate.read_state(self.state_path)["last_processed_version"], "v2")

    def test_full_cycle_new_then_commit_then_noop(self):
        result = ("v3", "2026-08-25T00:00:00Z", SAMPLE_CHANGELOG)
        self.assertEqual(self._run([], fetch_result=result), gate.EXIT_NEW_RELEASE)
        self.assertEqual(self._run(["--commit"], fetch_result=result), gate.EXIT_NEW_RELEASE)
        self.assertEqual(self._run([], fetch_result=result), gate.EXIT_NO_NEW_RELEASE)

    def test_next_release_reopens_the_gate(self):
        gate.write_state(self.state_path, "v3", None, {})
        code = self._run([], fetch_result=("v4", None, SAMPLE_CHANGELOG))
        self.assertEqual(code, gate.EXIT_NEW_RELEASE)


class _JsonResponse:
    """Minimal stand-in for the urlopen context-manager result.

    `json.load(fp)` just calls `fp.read()` and hands the result to `json.loads`, which
    accepts bytes as well as str. Returning encoded bytes here matches what a real
    HTTP response yields, so no patching of `json.load` is needed -- and patching it
    globally would break `read_state`, which reads a text file through the same call.
    """

    def __init__(self, payload):
        self._payload = payload

    def read(self):
        return json.dumps(self._payload).encode("utf-8")


if __name__ == "__main__":
    unittest.main(verbosity=2)
