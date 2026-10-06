#!/usr/bin/env python3
"""Integration tests for audit_docs.py.

These run the audit as a subprocess against the sibling code repos (warp client +
warp-server) and assert behavioral invariants: clean exit, completeness
accounting totality, category/severity scoping, fail-loud on a missing repo, and
that --update-snapshot rejects any delta without an explicit disposition.

Tests are skipped (not failed) when the sibling code repos aren't checked out, so
the suite is safe to run anywhere.

Run with: python3 .agents/skills/missing_docs/scripts/test_audit_docs.py
(stdlib unittest only; no third-party deps).
"""

import hashlib
import importlib.util
import io
import json
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock

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


def _sha(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def _write_snapshot_with_removed_flag(path: Path) -> str:
    snapshot = json.loads(_DEFAULT_SNAPSHOT.read_text(encoding="utf-8"))
    removed_flag = next(iter(snapshot["flags"]))
    del snapshot["flags"][removed_flag]
    path.write_text(json.dumps(snapshot), encoding="utf-8")
    return removed_flag


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

    def test_diff_reports_synthetic_snapshot_delta(self):
        with tempfile.TemporaryDirectory() as d:
            tmp_snap = Path(d) / "snap.json"
            removed_flag = _write_snapshot_with_removed_flag(tmp_snap)
            rc, report, stderr = _run_audit(
                ["--diff", "--snapshot", str(tmp_snap)]
            )
        self.assertEqual(rc, 0, stderr)
        self.assertIn(
            ("flag_added", removed_flag),
            {
                (item["change"], item["surface"])
                for item in report["surface_changes"]
            },
        )

    def test_update_snapshot_rejects_unresolved_baseline_without_writing(self):
        before = _sha(_DEFAULT_SNAPSHOT)
        with tempfile.TemporaryDirectory() as d:
            tmp_snap = Path(d) / "snap.json"
            _write_snapshot_with_removed_flag(tmp_snap)
            tmp_before = _sha(tmp_snap)
            rc, report, stderr = _run_audit(
                ["--update-snapshot", "--snapshot", str(tmp_snap)]
            )
            self.assertEqual(rc, 2, stderr)
            self.assertEqual(_sha(tmp_snap), tmp_before, "a rejected update must not write")
            self.assertEqual(
                _sha(_DEFAULT_SNAPSHOT), before, "--update-snapshot must not mutate the committed snapshot"
            )
            skipped = {
                item["audit"]: item["reason"]
                for item in report["summary"]["audits_skipped"]
            }
            self.assertIn("integrity:snapshot_dispositions", skipped)
            self.assertIn(
                "missing disposition ledger",
                skipped["integrity:snapshot_dispositions"],
            )

    def test_update_snapshot_accepts_fully_dispositioned_deltas(self):
        with tempfile.TemporaryDirectory() as d:
            tmp_snap = Path(d) / "snap.json"
            _write_snapshot_with_removed_flag(tmp_snap)
            rc, report, stderr = _run_audit(["--diff", "--snapshot", str(tmp_snap)])
            self.assertEqual(rc, 0, stderr)
            changes = report["surface_changes"]
            self.assertTrue(changes, "the fixture needs pending surface changes")
            disposition_path = (
                tmp_snap.parent / audit_docs.SNAPSHOT_DISPOSITIONS_FILENAME
            )
            disposition_path.write_text(json.dumps({
                "schema_version": audit_docs.SNAPSHOT_DISPOSITION_SCHEMA_VERSION,
                "snapshot_fingerprint": audit_docs.snapshot_fingerprint(
                    json.loads(tmp_snap.read_text(encoding="utf-8"))
                ),
                "dispositions": [
                    {
                        "change": item["change"],
                        "surface": item["surface"],
                        "disposition": "no_docs_needed",
                        "evidence": "Test fixture records a terminal triage decision.",
                    }
                    for item in changes
                ],
            }), encoding="utf-8")

            rc2, _, stderr2 = _run_audit(
                ["--update-snapshot", "--snapshot", str(tmp_snap)],
                capture_report=False,
            )
            self.assertEqual(rc2, 0, stderr2)
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


class TestSnapshotDispositions(unittest.TestCase):
    def _write_ledger(self, path, fingerprint, dispositions):
        path.write_text(json.dumps({
            "schema_version": audit_docs.SNAPSHOT_DISPOSITION_SCHEMA_VERSION,
            "snapshot_fingerprint": fingerprint,
            "dispositions": dispositions,
        }), encoding="utf-8")

    def test_zero_current_delta_rejects_stale_ledger_entries(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / audit_docs.SNAPSHOT_DISPOSITIONS_FILENAME
            fingerprint = audit_docs.snapshot_fingerprint({"schema_version": 2})
            self._write_ledger(path, fingerprint, [{
                "change": "cli_command_added",
                "surface": "warp example",
                "disposition": "documented",
                "evidence": "The reference documents this command.",
            }])

            errors = audit_docs.snapshot_disposition_errors(
                [], path, fingerprint
            )

        self.assertTrue(any(
            "stale dispositions without matching snapshot changes" in error
            for error in errors
        ), errors)

    def test_rejects_ledger_for_different_input_snapshot(self):
        change = {"change": "cli_command_added", "surface": "warp example"}
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / audit_docs.SNAPSHOT_DISPOSITIONS_FILENAME
            self._write_ledger(path, "not-the-input-fingerprint", [{
                **change,
                "disposition": "documented",
                "evidence": "The reference documents this command.",
            }])

            errors = audit_docs.snapshot_disposition_errors(
                [change],
                path,
                audit_docs.snapshot_fingerprint({"schema_version": 2}),
            )

        self.assertIn(
            "disposition ledger snapshot_fingerprint does not match the input snapshot",
            errors,
        )

    def test_accepts_matching_fully_dispositioned_and_no_delta_ledgers(self):
        fingerprint = audit_docs.snapshot_fingerprint({"schema_version": 2})
        change = {"change": "cli_command_added", "surface": "warp example"}
        cases = (
            ([change], [{
                **change,
                "disposition": "documented",
                "evidence": "The reference documents this command.",
            }]),
            ([], []),
        )
        for changes, dispositions in cases:
            with self.subTest(changes=changes), tempfile.TemporaryDirectory() as d:
                path = Path(d) / audit_docs.SNAPSHOT_DISPOSITIONS_FILENAME
                self._write_ledger(path, fingerprint, dispositions)
                self.assertEqual(
                    audit_docs.snapshot_disposition_errors(
                        changes, path, fingerprint
                    ),
                    [],
                )


class TestConsistencyAudit(unittest.TestCase):
    def test_approved_seed_store_partitions_all_24_findings(self):
        result = audit_docs.audit_consistency(_DOCS_ROOT)
        self.assertEqual(result["total_seeds"], 24)
        self.assertEqual(sum(result["by_status"].values()), 24)
        self.assertEqual(
            set(result["by_status"]),
            set(audit_docs.CONSISTENCY_STATUSES),
        )
        self.assertEqual(result["accounting"]["unaccounted"], [])

    def test_removed_placeholder_passes_its_deterministic_rule(self):
        result = audit_docs.audit_consistency(_DOCS_ROOT)
        findings = [
            item
            for item in result["findings"]
            if item["seed_id"] == "cloud-concurrency-placeholder"
        ]
        self.assertEqual(findings, [])
        passed = {item["rule_id"] for item in result["rules"]["passed"]}
        self.assertIn("no-finalizing-concurrency-placeholder", passed)

    def test_resolved_statements_pass_their_rules(self):
        result = audit_docs.audit_consistency(_DOCS_ROOT)
        passed = {item["rule_id"] for item in result["rules"]["passed"]}
        self.assertIn("no-singular-create-run-example", passed)
        self.assertIn("no-five-file-cli-limit", passed)
        self.assertIn("no-old-session-sharing-links", passed)
        self.assertIn("no-finalizing-concurrency-placeholder", passed)

    def test_policy_blockers_remain_visible_with_owner_metadata(self):
        result = audit_docs.audit_consistency(_DOCS_ROOT)
        blockers = {
            item["seed_id"]: item
            for item in result["blockers"]
            if item["status"] == "policy_blocker"
        }
        self.assertEqual(
            set(blockers),
            {
                "customer-data-training-policy",
                "free-telemetry-optout-ai-policy",
                "fireworks-zdr-provider-list",
            },
        )
        for blocker in blockers.values():
            self.assertTrue(blocker["owner"])
            self.assertTrue(blocker["unresolved_question"])
            self.assertTrue(blocker["inconsistent_surfaces"])
            self.assertTrue(blocker["recheck_condition"])

    def test_exact_rule_reports_every_occurrence_and_then_passes(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            doc = root / "doc.mdx"
            doc.write_text("stale statement\nok\nSTALE STATEMENT\n", encoding="utf-8")
            store = (
                root
                / ".agents"
                / "skills"
                / "missing_docs"
                / "references"
                / "consistency_seeds.json"
            )
            store.parent.mkdir(parents=True)
            store.write_text(json.dumps({
                "schema_version": 1,
                "seeds": [{
                    "id": "multiple-occurrences",
                    "claim": "The stale statement is absent.",
                    "status": "fix",
                    "occurrence_queries": ["stale statement"],
                    "authoritative_sources": ["source.rs"],
                    "affected_surfaces": ["doc.mdx"],
                    "surface_dispositions": {"doc.mdx": "fixed"},
                    "recheck_condition": "The source statement changes.",
                    "deterministic_rules": [{
                        "id": "no-stale-statement",
                        "type": "forbidden_text",
                        "patterns": ["stale statement"],
                        "paths": ["doc.mdx"],
                    }],
                }],
            }), encoding="utf-8")

            result = audit_docs.audit_consistency(root)
            self.assertEqual(len(result["findings"]), 2)
            self.assertEqual(
                [item["line"] for item in result["findings"]],
                [1, 3],
            )
            self.assertEqual(result["rules"]["failed"][0]["match_count"], 2)

            doc.write_text("current statement\n", encoding="utf-8")
            resolved = audit_docs.audit_consistency(root)
            self.assertEqual(resolved["findings"], [])
            self.assertEqual(
                resolved["rules"]["passed"][0]["rule_id"],
                "no-stale-statement",
            )

    def test_malformed_seed_data_exits_two(self):
        with tempfile.TemporaryDirectory() as d:
            store = Path(d) / "seeds.json"
            store.write_text(
                '{"schema_version": 1, "seeds": [{"id": "unaccounted"}]}',
                encoding="utf-8",
            )
            output = Path(d) / "report.json"
            argv = [
                str(_AUDIT),
                "--category",
                "consistency",
                "--output",
                str(output),
            ]
            with (
                mock.patch.object(audit_docs, "_consistency_seed_path", return_value=store),
                mock.patch.object(sys, "argv", argv),
                redirect_stdout(io.StringIO()),
                redirect_stderr(io.StringIO()),
                self.assertRaises(SystemExit) as exited,
            ):
                audit_docs.main()
            self.assertEqual(exited.exception.code, 2)
            report = json.loads(output.read_text(encoding="utf-8"))
            skipped = {
                item["audit"]
                for item in report["summary"]["audits_skipped"]
            }
            self.assertIn("integrity:consistency_accounting", skipped)
            self.assertTrue(report["consistency"]["accounting"]["unaccounted"])

    def test_category_and_severity_scope_remain_compatible(self):
        with tempfile.TemporaryDirectory() as d:
            output = Path(d) / "report.json"
            proc = subprocess.run(
                [
                    sys.executable,
                    str(_AUDIT),
                    "--category",
                    "consistency",
                    "--severity",
                    "high",
                    "--output",
                    str(output),
                ],
                capture_output=True,
                text=True,
                stdin=subprocess.DEVNULL,
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            report = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(report["summary"]["audits_run"], ["consistency"])
            self.assertEqual(
                report["summary"]["by_category"]["undocumented_cli_commands"],
                0,
            )
            self.assertTrue(
                all(
                    item["severity"] == "high"
                    for item in report["consistency_findings"]
                )
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

    def test_marker_reader_survives_every_bad_shape(self):
        """A malformed marker must degrade to "never triaged", never raise.

        Raising here aborts diff-mode triage entirely, which is a worse failure
        than the desync this reader exists to fix. Valid JSON of the wrong
        top-level type is the case that bites: `[]` reaches `.get` and throws.
        """
        cases = {
            "list": "[]",
            "bare string": '"v0.2026.08.18.02.52.stable_00"',
            "number": "42",
            "null": "null",
            "truncated json": '{"last_processed_version":',
            "empty file": "",
            "object, wrong key": '{"version": "v0.2026.08.18.02.52.stable_00"}',
        }
        for label, payload in cases.items():
            with self.subTest(shape=label), tempfile.TemporaryDirectory() as d:
                refs = Path(d)
                (refs / "last_release_processed.json").write_text(
                    payload, encoding="utf-8")
                self.assertIsNone(
                    audit_docs.read_last_processed_release(
                        refs / "surface_snapshot.json"),
                    f"{label} marker should fall back to None")

        # A missing marker is the ordinary first-run case, not an error.
        with tempfile.TemporaryDirectory() as d:
            self.assertIsNone(audit_docs.read_last_processed_release(
                Path(d) / "surface_snapshot.json"))

        # The well-formed case still reads through.
        with tempfile.TemporaryDirectory() as d:
            refs = Path(d)
            (refs / "last_release_processed.json").write_text(
                '{"last_processed_version": "v0.2026.08.18.02.52.stable_00"}',
                encoding="utf-8")
            self.assertEqual(
                audit_docs.read_last_processed_release(
                    refs / "surface_snapshot.json"),
                "2026.08.18")


if __name__ == "__main__":
    unittest.main(verbosity=2)
