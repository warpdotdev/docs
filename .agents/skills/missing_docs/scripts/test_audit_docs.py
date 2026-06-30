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


if __name__ == "__main__":
    unittest.main(verbosity=2)
