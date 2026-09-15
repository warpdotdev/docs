#!/usr/bin/env python3
"""Unit tests for validate_ui_refs.py's --changed mode and snapshot provenance.

Uses a throwaway git repo fixture (no dependency on the real docs repo's
history) so these tests are hermetic and match `style_lint.py`'s own
`--changed` test approach of exercising real git behavior rather than mocking
subprocess.

Run:
    python3 .agents/skills/validate_ui_refs/test_changed_mode.py
"""
from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

_HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("validate_ui_refs", _HERE / "validate_ui_refs.py")
vur = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(vur)


def _run(cmd, cwd):
    subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, check=True)


def _init_repo_with_main_and_changes(tmp: Path) -> Path:
    """Create a git repo with an `origin/main` ref and unstaged HEAD changes."""
    repo = tmp / "repo"
    repo.mkdir()
    _run(["git", "init", "-q"], repo)
    _run(["git", "config", "user.email", "test@example.com"], repo)
    _run(["git", "config", "user.name", "Test"], repo)

    docs_dir = repo / "src" / "content" / "docs"
    docs_dir.mkdir(parents=True)
    (docs_dir / "existing.mdx").write_text("existing content\n", encoding="utf-8")
    (docs_dir / "changelog").mkdir()
    (docs_dir / "changelog" / "2026.mdx").write_text("changelog\n", encoding="utf-8")
    _run(["git", "add", "."], repo)
    _run(["git", "commit", "-q", "-m", "initial"], repo)
    # Fake an origin/main remote-tracking ref pointing at the initial commit.
    # `git branch -f refs/remotes/origin/main` would create refs/heads/refs/...
    # (branch names live under refs/heads/), so use update-ref directly.
    _run(["git", "update-ref", "refs/remotes/origin/main", "HEAD"], repo)

    # Now make changes on top: a new page, an edit to an existing page, and a
    # non-markdown file (should never be picked up).
    (docs_dir / "new-page.mdx").write_text("new page\n", encoding="utf-8")
    (docs_dir / "existing.mdx").write_text("existing content, edited\n", encoding="utf-8")
    (repo / "README.md").write_text("not in docs dir\n", encoding="utf-8")
    _run(["git", "add", "."], repo)
    _run(["git", "commit", "-q", "-m", "changes"], repo)
    return repo


class TestFindChangedMdFiles(unittest.TestCase):
    def test_finds_new_and_edited_files_under_docs_dir(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = _init_repo_with_main_and_changes(Path(tmp))
            docs_dir = repo / "src" / "content" / "docs"
            import os
            old_cwd = os.getcwd()
            os.chdir(repo)
            try:
                files = vur.find_changed_md_files(docs_dir)
            finally:
                os.chdir(old_cwd)
            names = sorted(f.name for f in files)
            self.assertEqual(names, ["existing.mdx", "new-page.mdx"])

    def test_excludes_changelog_by_default(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = _init_repo_with_main_and_changes(Path(tmp))
            docs_dir = repo / "src" / "content" / "docs"
            (docs_dir / "changelog" / "2026.mdx").write_text("changelog, edited\n", encoding="utf-8")
            _run(["git", "add", "."], repo)
            _run(["git", "commit", "-q", "-m", "changelog edit"], repo)

            import os
            old_cwd = os.getcwd()
            os.chdir(repo)
            try:
                files = vur.find_changed_md_files(docs_dir)
                files_with_changelog = vur.find_changed_md_files(docs_dir, include_changelog=True)
            finally:
                os.chdir(old_cwd)

            self.assertNotIn("2026.mdx", [f.name for f in files])
            self.assertIn("2026.mdx", [f.name for f in files_with_changelog])

    def test_deleted_file_is_excluded(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = _init_repo_with_main_and_changes(Path(tmp))
            docs_dir = repo / "src" / "content" / "docs"
            (docs_dir / "existing.mdx").unlink()
            _run(["git", "add", "."], repo)
            _run(["git", "commit", "-q", "-m", "delete existing"], repo)

            import os
            old_cwd = os.getcwd()
            os.chdir(repo)
            try:
                files = vur.find_changed_md_files(docs_dir)
            finally:
                os.chdir(old_cwd)
            self.assertNotIn("existing.mdx", [f.name for f in files])

    def test_unresolvable_diff_raises_instead_of_falling_back(self):
        with tempfile.TemporaryDirectory() as tmp:
            # A repo with no origin/main ref at all: the diff can't resolve.
            repo = Path(tmp) / "no_main"
            repo.mkdir()
            _run(["git", "init", "-q"], repo)
            docs_dir = repo / "src" / "content" / "docs"
            docs_dir.mkdir(parents=True)

            import os
            old_cwd = os.getcwd()
            os.chdir(repo)
            try:
                with self.assertRaises(vur.ChangedFilesUnresolvedError):
                    vur.find_changed_md_files(docs_dir)
            finally:
                os.chdir(old_cwd)


class TestRequireProvenanceFlag(unittest.TestCase):
    """Regression for the required-CI-gate fail-closed rule: an incomplete
    snapshot (missing source_repository/source_sha) must not be silently
    trusted just because scanning found no other issues.
    """

    def _run_with_snapshot(self, valid_paths: dict) -> int:
        with tempfile.TemporaryDirectory() as tmp:
            repo = _init_repo_with_main_and_changes(Path(tmp))
            valid_paths_file = repo / "valid_paths.json"
            valid_paths_file.write_text(json.dumps(valid_paths), encoding="utf-8")
            docs_dir = repo / "src" / "content" / "docs"
            old_argv = sys.argv
            sys.argv = [
                "validate_ui_refs.py", "--changed", "--require-provenance",
                "--docs-dir", str(docs_dir), "--valid-paths", str(valid_paths_file),
            ]
            old_cwd = os.getcwd()
            os.chdir(repo)
            try:
                return vur.main()
            finally:
                sys.argv = old_argv
                os.chdir(old_cwd)

    def test_missing_provenance_fails_closed(self):
        exit_code = self._run_with_snapshot({"settings_sections": {}, "generated_at": "2026-01-01T00:00:00Z"})
        self.assertEqual(exit_code, 1)

    def test_null_source_sha_fails_closed(self):
        exit_code = self._run_with_snapshot({
            "settings_sections": {}, "source_repository": "warpdotdev/warp",
            "source_sha": None, "generated_at": "2026-01-01T00:00:00Z",
        })
        self.assertEqual(exit_code, 1)

    def test_complete_provenance_passes(self):
        exit_code = self._run_with_snapshot({
            "settings_sections": {}, "source_repository": "warpdotdev/warp",
            "source_sha": "abc123", "generated_at": "2026-01-01T00:00:00Z",
        })
        self.assertEqual(exit_code, 0)


class TestSnapshotProvenance(unittest.TestCase):
    def test_resolve_source_sha_reads_head(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "warp"
            repo.mkdir()
            _run(["git", "init", "-q"], repo)
            _run(["git", "config", "user.email", "test@example.com"], repo)
            _run(["git", "config", "user.name", "Test"], repo)
            (repo / "f.txt").write_text("x", encoding="utf-8")
            _run(["git", "add", "."], repo)
            _run(["git", "commit", "-q", "-m", "c"], repo)
            expected = subprocess.run(
                ["git", "-C", str(repo), "rev-parse", "HEAD"],
                capture_output=True, text=True, check=True,
            ).stdout.strip()
            self.assertEqual(vur._resolve_source_sha(repo), expected)

    def test_resolve_source_sha_missing_repo_returns_none(self):
        self.assertIsNone(vur._resolve_source_sha(Path("/nonexistent/path/xyz")))

    def test_refresh_preserves_existing_source_sha_when_git_resolution_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "valid_paths.json"
            output.write_text(
                json.dumps({"source_repository": "warpdotdev/warp", "source_sha": "trusted-sha"}),
                encoding="utf-8",
            )
            with mock.patch.object(vur, "_extract_settings_sections", return_value={}), \
                 mock.patch.object(vur, "_extract_command_palette_commands", return_value={}), \
                 mock.patch.object(vur, "_extract_umbrellas", return_value={}), \
                 mock.patch.object(vur, "_resolve_source_repository", return_value=None), \
                 mock.patch.object(vur, "_resolve_source_sha", return_value=None):
                vur.refresh_valid_paths(Path(tmp) / "missing-warp", output)
            refreshed = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(refreshed["source_sha"], "trusted-sha")
    def test_refresh_preserves_notification_dedupe_metadata(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "valid_paths.json"
            output.write_text(
                json.dumps(
                    {
                        "last_notified_signature": "report-signature",
                        "last_notified_at": "2026-09-11T16:50:14+00:00",
                    }
                ),
                encoding="utf-8",
            )
            with mock.patch.object(vur, "_extract_settings_sections", return_value={}), \
                 mock.patch.object(vur, "_extract_command_palette_commands", return_value={}), \
                 mock.patch.object(vur, "_extract_umbrellas", return_value={}):
                vur.refresh_valid_paths(Path(tmp) / "missing-warp", output)
            refreshed = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(refreshed["last_notified_signature"], "report-signature")
            self.assertEqual(
                refreshed["last_notified_at"], "2026-09-11T16:50:14+00:00"
            )

    def test_resolve_source_repository_parses_https_remote(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "warp"
            repo.mkdir()
            _run(["git", "init", "-q"], repo)
            _run(["git", "remote", "add", "origin", "https://github.com/warpdotdev/warp.git"], repo)
            self.assertEqual(vur._resolve_source_repository(repo), "warpdotdev/warp")


class TestUnresolvedIssueSignature(unittest.TestCase):
    """Regression for QUALITY-2038: the `UI Reference Validation Report` Slack
    notification reposted an identical report on consecutive scheduled runs
    because `main()` notified whenever *any* unresolved issue remained, with
    no comparison to what was already reported. These tests cover the pure
    decision logic that fixes that: `unresolved_issue_signature()` must be
    stable/order-independent so two runs finding the same issues compare
    equal, and `should_notify_slack()` must only return True when that
    signature actually changes.
    """

    def _issue(self, file: str, line: int, issue_text: str) -> dict:
        return {"file": file, "line": line, "validation": {"issue": issue_text}}

    def test_signature_is_stable_across_runs_with_identical_issues(self):
        repo_root = Path("/repo")
        issues_a = [
            self._issue("/repo/docs/a.mdx", 10, "bad path"),
            self._issue("/repo/docs/b.mdx", 20, "bad command"),
        ]
        issues_b = [
            self._issue("/repo/docs/b.mdx", 20, "bad command"),
            self._issue("/repo/docs/a.mdx", 10, "bad path"),
        ]
        sig_a = vur.unresolved_issue_signature(issues_a, [], [], repo_root)
        sig_b = vur.unresolved_issue_signature(issues_b, [], [], repo_root)
        self.assertEqual(sig_a, sig_b)

    def test_signature_changes_when_issues_change(self):
        repo_root = Path("/repo")
        before = [self._issue("/repo/docs/a.mdx", 10, "bad path")]
        after_new_issue = before + [self._issue("/repo/docs/c.mdx", 5, "new issue")]
        after_resolved = []
        sig_before = vur.unresolved_issue_signature(before, [], [], repo_root)
        sig_new = vur.unresolved_issue_signature(after_new_issue, [], [], repo_root)
        sig_resolved = vur.unresolved_issue_signature(after_resolved, [], [], repo_root)
        self.assertNotEqual(sig_before, sig_new)
        self.assertNotEqual(sig_before, sig_resolved)

    def test_signature_round_trips_through_pr_body_marker(self):
        repo_root = Path("/repo")
        issues = [self._issue("/repo/docs/a.mdx", 10, "bad path")]
        sig = vur.unresolved_issue_signature(issues, [], [], repo_root)
        body = vur._pr_body([], repo_root, unresolved_signature=sig, remaining_count=1)
        self.assertEqual(vur.extract_unresolved_signature(body), sig)

    def test_extract_unresolved_signature_handles_missing_marker(self):
        self.assertIsNone(vur.extract_unresolved_signature(None))
        self.assertIsNone(vur.extract_unresolved_signature("## Summary\nNo marker here."))


class TestShouldNotifySlack(unittest.TestCase):
    """Regression for QUALITY-2038's core Slack-spam bug (see class docstring
    above): identical unresolved issues must not trigger a second
    notification, but a clean scan or a genuinely new/resolved issue must.
    """

    def test_no_issues_never_notifies(self):
        self.assertFalse(vur.should_notify_slack(0, "anysig", None))
        self.assertFalse(vur.should_notify_slack(0, "anysig", "anysig"))

    def test_first_time_seeing_issues_notifies(self):
        self.assertTrue(vur.should_notify_slack(2, "sig-a", None))

    def test_identical_signature_does_not_renotify(self):
        # This is the exact regression: a scheduled run finds the same
        # unresolved issues as the last reported run and must not re-post.
        self.assertFalse(vur.should_notify_slack(2, "sig-a", "sig-a"))

    def test_changed_signature_notifies(self):
        self.assertTrue(vur.should_notify_slack(2, "sig-b", "sig-a"))


class TestSnapshotUncommittedChanges(unittest.TestCase):
    """Regression for QUALITY-2038 hypothesis (a): a `--refresh-valid-paths`
    run that bumps `source_sha` but finds no auto-fixable doc issues was
    silently discarded (never committed) because `create_pr()` was gated on
    `fixes` alone. `_snapshot_has_uncommitted_changes()` is the signal `main()`
    now uses to also commit a fixless snapshot refresh.
    """

    def _init_repo(self, tmp: Path) -> Path:
        repo = tmp / "repo"
        repo.mkdir()
        _run(["git", "init", "-q"], repo)
        _run(["git", "config", "user.email", "test@example.com"], repo)
        _run(["git", "config", "user.name", "Test"], repo)
        return repo

    def test_false_when_file_matches_last_commit(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = self._init_repo(Path(tmp))
            valid_paths_file = repo / "valid_paths.json"
            valid_paths_file.write_text(json.dumps({"source_sha": "abc"}), encoding="utf-8")
            _run(["git", "add", "."], repo)
            _run(["git", "commit", "-q", "-m", "initial"], repo)
            self.assertFalse(vur._snapshot_has_uncommitted_changes(valid_paths_file, repo))

    def test_true_after_a_refresh_bumps_source_sha_with_no_other_changes(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = self._init_repo(Path(tmp))
            valid_paths_file = repo / "valid_paths.json"
            valid_paths_file.write_text(json.dumps({"source_sha": "abc"}), encoding="utf-8")
            _run(["git", "add", "."], repo)
            _run(["git", "commit", "-q", "-m", "initial"], repo)

            # Simulate `--refresh-valid-paths` advancing source_sha locally,
            # uncommitted — the exact state that used to get silently dropped.
            valid_paths_file.write_text(json.dumps({"source_sha": "def"}), encoding="utf-8")
            self.assertTrue(vur._snapshot_has_uncommitted_changes(valid_paths_file, repo))


if __name__ == "__main__":
    unittest.main()
