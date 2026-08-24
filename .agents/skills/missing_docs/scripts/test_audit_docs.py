#!/usr/bin/env python3
"""Integration tests for audit_docs.py.

These run the audit as a subprocess against the sibling code repos (warp client +
warp-server) and assert behavioral invariants: clean exit, completeness
accounting totality, category/severity scoping, fail-loud on a missing repo, and
that --update-snapshot honors --snapshot without mutating the committed snapshot.

Tests are skipped (not failed) when the sibling code repos aren't checked out, so
the suite is safe to run anywhere.

Run with: python3 .agents/skills/missing_docs/scripts/test_audit_docs.py
(stdlib unittest only; no third-party deps).
"""

import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_AUDIT = _HERE / "audit_docs.py"
_DOCS_ROOT = _HERE.parents[3]  # scripts -> missing_docs -> skills -> .agents -> docs
_DEFAULT_SNAPSHOT = _HERE.parent / "references" / "surface_snapshot.json"
_SIBLINGS = _DOCS_ROOT.parent


def _find_warp():
    for name in ("warp", "warp-internal"):
        if (_SIBLINGS / name / ".github").exists() or (_SIBLINGS / name / "app").exists():
            return _SIBLINGS / name
    return None


def _find_server():
    p = _SIBLINGS / "warp-server"
    return p if p.exists() else None


WARP = _find_warp()
SERVER = _find_server()
_REPOS_AVAILABLE = WARP is not None and SERVER is not None

# Import the audit module directly for repo-free unit tests of pure logic.
_spec = importlib.util.spec_from_file_location("audit_docs", _AUDIT)
audit_docs = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(audit_docs)


def _run_audit(extra_args, capture_report=True):
    """Run audit_docs.py; return (returncode, report_dict_or_None)."""
    out_path = None
    args = [sys.executable, str(_AUDIT), "--warp", str(WARP), "--warp-server", str(SERVER)]
    if capture_report:
        out_path = Path(tempfile.mkstemp(suffix=".json")[1])
        args += ["--output", str(out_path)]
    args += extra_args
    proc = subprocess.run(args, capture_output=True, text=True, stdin=subprocess.DEVNULL)
    report = None
    if capture_report and out_path and out_path.exists() and out_path.stat().st_size > 0:
        try:
            report = json.loads(out_path.read_text())
        except json.JSONDecodeError:
            report = None
    return proc.returncode, report, proc.stderr


def _sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


@unittest.skipUnless(_REPOS_AVAILABLE, "warp/warp-server repos not checked out as siblings")
class TestAuditBehavior(unittest.TestCase):
    def test_full_run_is_clean_and_accounts_for_everything(self):
        rc, report, stderr = _run_audit([])
        self.assertEqual(rc, 0, f"audit should exit 0 on a healthy run; stderr={stderr}")
        self.assertIsNotNone(report, "audit should emit a JSON report")
        summary = report["summary"]
        self.assertEqual(summary.get("audits_skipped"), [], "no audits should be skipped")
        self.assertEqual(
            summary["accounting"].get("unaccounted"), {}, "every surface must be accounted for"
        )

    def test_category_scopes_to_one_audit(self):
        rc, report, stderr = _run_audit(["--category", "settings"])
        self.assertEqual(rc, 0, stderr)
        audits_run = report["summary"].get("audits_run", [])
        self.assertIn("settings", audits_run)
        self.assertNotIn("cli", audits_run)
        # CLI category did not run, so its findings should be absent/zero.
        self.assertEqual(report["summary"]["by_category"].get("undocumented_cli_commands", 0), 0)

    def test_severity_filter_excludes_lower_severities(self):
        rc, report, _ = _run_audit(["--severity", "high"])
        self.assertEqual(rc, 0)
        bad = []
        for key, value in report.items():
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, dict) and item.get("severity") in ("low", "medium"):
                        bad.append((key, item.get("severity")))
        self.assertEqual(bad, [], f"--severity high must drop low/medium findings, found: {bad[:5]}")

    def test_fail_loud_on_missing_repo(self):
        # Point --warp at a nonexistent path; the script must exit 2, not pretend "no gaps".
        out_path = Path(tempfile.mkstemp(suffix=".json")[1])
        proc = subprocess.run(
            [
                sys.executable,
                str(_AUDIT),
                "--warp",
                str(_SIBLINGS / "definitely-not-a-real-repo"),
                "--warp-server",
                str(SERVER),
                "--output",
                str(out_path),
            ],
            capture_output=True,
            text=True,
            stdin=subprocess.DEVNULL,
        )
        self.assertEqual(proc.returncode, 2, f"missing repo must exit 2; stderr={proc.stderr}")

    def test_diff_against_committed_snapshot_is_current(self):
        # The committed snapshot should reflect current code (no pending surface drift).
        rc, report, stderr = _run_audit(["--diff"])
        self.assertEqual(rc, 0, stderr)
        self.assertEqual(
            report["summary"]["by_category"].get("surface_changes", 0),
            0,
            "committed snapshot is stale; regenerate with --update-snapshot",
        )

    def test_update_snapshot_respects_snapshot_flag_and_roundtrips(self):
        before = _sha(_DEFAULT_SNAPSHOT)
        with tempfile.TemporaryDirectory() as d:
            tmp_snap = Path(d) / "snap.json"
            # Regenerate into the temp path (must NOT touch the committed snapshot).
            rc, _, stderr = _run_audit(
                ["--update-snapshot", "--snapshot", str(tmp_snap)], capture_report=False
            )
            self.assertEqual(rc, 0, stderr)
            self.assertTrue(tmp_snap.exists() and tmp_snap.stat().st_size > 0,
                            "--update-snapshot should write to the --snapshot path")
            self.assertEqual(
                _sha(_DEFAULT_SNAPSHOT), before, "--update-snapshot must not mutate the committed snapshot"
            )
            # Diffing current code against the just-generated snapshot shows no drift.
            rc2, report2, _ = _run_audit(["--diff", "--snapshot", str(tmp_snap)])
            self.assertEqual(rc2, 0)
            self.assertEqual(report2["summary"]["by_category"].get("surface_changes", 0), 0)

    def test_research_preview_surfaces_are_deferred(self):
        # Public vs. private boundary: Agent Memory is research preview (not public),
        # so its CLI (`oz memory*`) and REST API (`/memory_stores/*`) must never be
        # flagged for documentation. Guards the surface-map deferrals from regressing.
        rc, report, _ = _run_audit([])
        self.assertEqual(rc, 0)
        flagged = []
        for cat in ("undocumented_cli_commands", "undocumented_api_endpoints"):
            for item in report.get(cat, []):
                name = item.get("command") or item.get("endpoint") or ""
                if "memory" in name.lower():
                    flagged.append(name)
        self.assertEqual(
            flagged, [], f"research-preview Agent Memory surfaces must stay deferred, found: {flagged}"
        )


class TestGatedLogic(unittest.TestCase):
    """Repo-free unit tests for the `gated:<Flag>` rollout-aware deferral."""

    def test_gated_flag_helper(self):
        self.assertEqual(audit_docs._gated_flag("gated:AIMemories"), "AIMemories")
        self.assertEqual(audit_docs._gated_flag("gated: Spaced "), "Spaced")
        self.assertIsNone(audit_docs._gated_flag("internal"))
        self.assertIsNone(audit_docs._gated_flag("src/content/docs/x.mdx"))
        self.assertIsNone(audit_docs._gated_flag(None))

    def _run_cli(self, status_map):
        """Run audit_cli on one gated command with the given flag statuses."""
        with tempfile.TemporaryDirectory() as d:
            surface_map = {"cli_to_doc": {"oz memx": "gated:MemFlag"}}
            commands = [{"command": "oz memx", "hidden": False,
                         "subcommands": [], "source_file": None}]
            return audit_docs.audit_cli(
                None, Path(d), surface_map, {},
                cli_commands=commands, flag_statuses=status_map)

    def test_gated_non_ga_cli_is_deferred(self):
        findings = self._run_cli({"MemFlag": "other"})
        self.assertEqual(findings, [], "non-GA gated CLI command must be deferred")

    def test_gated_ga_cli_auto_surfaces(self):
        findings = self._run_cli({"MemFlag": "ga"})
        cmds = [f["command"] for f in findings]
        self.assertIn("oz memx", cmds, "a GA gated command must surface as a finding")

    def test_gated_unknown_flag_cli_surfaces(self):
        # Unknown gating flag is treated conservatively (not silently deferred).
        findings = self._run_cli({})
        self.assertIn("oz memx", [f["command"] for f in findings])

    def test_map_hygiene_flags_unknown_gated_flag(self):
        surface_map = {
            "cli_to_doc": {"oz good": "gated:KnownFlag", "oz bad": "gated:BogusFlag"},
            "feature_to_doc": {}, "api_to_doc": {}, "slash_to_doc": {},
            "settings_to_doc": {}, "ignore_flags": set(), "duplicates": [],
        }
        cli_commands = [
            {"command": "oz good", "hidden": False, "subcommands": []},
            {"command": "oz bad", "hidden": False, "subcommands": []},
        ]
        with tempfile.TemporaryDirectory() as d:
            findings = audit_docs.audit_map_hygiene(
                surface_map, {"KnownFlag": "other"}, cli_commands, [], [], {}, Path(d))
        gated_findings = [f for f in findings if "Gated target" in f["reason"]]
        self.assertEqual(len(gated_findings), 1, gated_findings)
        self.assertEqual(gated_findings[0]["entry"], "oz bad")


class TestChangelogTriage(unittest.TestCase):
    """Regression cases for the drift-watch triage baseline and section guard.

    All three failures these cover are silent: the run exits 0 and reports
    nothing, which is indistinguishable from "nothing shipped".
    """

    ENTRY = (
        "### 2099.01.02 (v0.2099.01.02.00.00)\n\n"
        "**New features**\n\n"
        "* A tracked bullet.\n\n"
        "**Automation Platform updates**\n\n"
        "* A bullet under the post-rename platform heading.\n\n"
        "**Bug fixes**\n\n"
        "* Deliberately untracked.\n\n"
        "**Sparkles**\n\n"
        "* A bullet under a heading the parser has never seen.\n"
    )

    def _entries(self, text):
        with tempfile.TemporaryDirectory() as d:
            changelog = Path(d) / "src" / "content" / "docs" / "changelog"
            changelog.mkdir(parents=True)
            (changelog / "2099.mdx").write_text(text, encoding="utf-8")
            return audit_docs.parse_changelog_entries(Path(d))

    def test_normalize_release_version(self):
        """The marker and the snapshot store versions in different shapes."""
        self.assertEqual(
            audit_docs.normalize_release_version("v0.2026.08.18.02.52.stable_00"),
            "2026.08.18")
        self.assertEqual(
            audit_docs.normalize_release_version("2026.08.19"), "2026.08.19")
        self.assertIsNone(audit_docs.normalize_release_version(None))
        self.assertIsNone(audit_docs.normalize_release_version("not-a-version"))

    def test_baseline_uses_the_earlier_marker(self):
        """A snapshot refresh must not skip a release that was never triaged.

        Bookkeeping PRs regenerate surface_snapshot.json, advancing its
        changelog pointer without triaging anything. Taking the snapshot alone
        as the baseline drops every entry in between.
        """
        self.assertEqual(
            audit_docs.changelog_review_baseline(
                "2026.08.19", "v0.2026.08.18.02.52.stable_00"),
            "2026.08.18")
        # Either side missing falls back to the other rather than to "all seen".
        self.assertEqual(
            audit_docs.changelog_review_baseline("2026.08.19", None), "2026.08.19")
        self.assertEqual(
            audit_docs.changelog_review_baseline(None, "v0.2026.08.18.02.52.stable_00"),
            "2026.08.18")
        # No markers at all means nothing has been triaged; review everything.
        self.assertIsNone(audit_docs.changelog_review_baseline(None, None))

    def test_desynced_markers_still_surface_the_release(self):
        """End to end: the snapshot ahead of the marker must not hide bullets."""
        entries = self._entries(self.ENTRY)
        ahead = audit_docs.changelog_review_findings(entries, "2099.01.02")
        self.assertEqual(ahead, [], "snapshot-only baseline hides the entry")
        recovered = audit_docs.changelog_review_findings(
            entries, "2099.01.02", "2099.01.01")
        self.assertEqual(len(recovered), 2, recovered)

    def test_tracked_untracked_and_unknown_sections(self):
        entry = self._entries(self.ENTRY)[0]
        categories = sorted(i["category"] for i in entry["items"])
        self.assertEqual(categories, ["automation platform updates", "new features"])
        # Bug fixes are skipped on purpose, so they must not read as a rename.
        self.assertEqual(entry["unknown_sections"], ["sparkles"])

    def test_unknown_section_guard_ignores_already_triaged_history(self):
        """Old launch posts use prose headings; policing them fails every run."""
        entries = self._entries(self.ENTRY)
        self.assertEqual(
            audit_docs.unreviewed_unknown_sections(entries, "2099.01.02"), [],
            "entries at or below the baseline are already triaged")
        self.assertEqual(
            audit_docs.unreviewed_unknown_sections(entries, "2099.01.01"),
            ["sparkles"],
            "an unrecognized heading in a pending entry must fail loud")


if __name__ == "__main__":
    unittest.main(verbosity=2)
