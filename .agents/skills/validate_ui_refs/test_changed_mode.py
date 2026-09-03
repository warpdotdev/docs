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
import subprocess
import tempfile
import unittest
from pathlib import Path

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

    def test_resolve_source_repository_parses_https_remote(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "warp"
            repo.mkdir()
            _run(["git", "init", "-q"], repo)
            _run(["git", "remote", "add", "origin", "https://github.com/warpdotdev/warp.git"], repo)
            self.assertEqual(vur._resolve_source_repository(repo), "warpdotdev/warp")


if __name__ == "__main__":
    unittest.main()
