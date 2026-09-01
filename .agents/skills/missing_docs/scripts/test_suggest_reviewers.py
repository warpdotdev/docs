#!/usr/bin/env python3
"""Unit tests for suggest_reviewers.py.

Run with: python3 .agents/skills/missing_docs/scripts/test_suggest_reviewers.py
(stdlib unittest only; no third-party deps).
"""

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_MODULE_PATH = _HERE / "suggest_reviewers.py"

_spec = importlib.util.spec_from_file_location("suggest_reviewers", _MODULE_PATH)
sr = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(sr)


class TestPatternMatches(unittest.TestCase):
    def test_anchored_dir_prefix(self):
        self.assertTrue(sr.pattern_matches("/app/src/settings/", "app/src/settings/ssh.rs"))
        # The directory path itself (no trailing slash on the candidate) matches.
        self.assertTrue(sr.pattern_matches("/app/src/settings/", "app/src/settings"))

    def test_dir_prefix_does_not_match_sibling_prefix(self):
        # "settingsX" must NOT match the "settings/" directory rule.
        self.assertFalse(sr.pattern_matches("/app/src/settings/", "app/src/settingsX/y.rs"))

    def test_exact_file(self):
        self.assertTrue(sr.pattern_matches("/app/src/tab.rs", "app/src/tab.rs"))
        self.assertFalse(sr.pattern_matches("/app/src/tab.rs", "app/src/tab.rs.bak"))
        self.assertFalse(sr.pattern_matches("/app/src/tab.rs", "app/src/other.rs"))

    def test_dir_without_trailing_slash(self):
        # A bare path can match a file under it (treated as a directory).
        self.assertTrue(sr.pattern_matches("/app/src/code", "app/src/code/file_tree.rs"))
        self.assertTrue(sr.pattern_matches("/app/src/code", "app/src/code"))
        self.assertFalse(sr.pattern_matches("/app/src/code", "app/src/codex/y.rs"))

    def test_glob(self):
        self.assertTrue(sr.pattern_matches("*.md", "README.md"))
        self.assertFalse(sr.pattern_matches("*.md", "main.rs"))

    def test_default_root_rule(self):
        # `/ @team` is the catch-all fallback and matches anything.
        self.assertTrue(sr.pattern_matches("/", "literally/anything/here"))


class TestOwnersFor(unittest.TestCase):
    def setUp(self):
        self.rules = [
            ("/", ["@warpdotdev/oss-maintainers"]),
            ("/app/src/settings/", ["@lucie"]),
            ("/app/src/search/slash_command_menu/", ["@moira"]),
            ("/app/src/search/slash_command_menu/static_commands/commands.rs", ["@lucie2"]),
        ]

    def test_last_match_wins_specific_over_broad(self):
        owners, pat = sr.owners_for(
            "app/src/search/slash_command_menu/static_commands/commands.rs", self.rules
        )
        self.assertEqual(owners, ["@lucie2"])
        self.assertEqual(pat, "/app/src/search/slash_command_menu/static_commands/commands.rs")

    def test_dir_match(self):
        owners, _ = sr.owners_for("app/src/search/slash_command_menu/menu.rs", self.rules)
        self.assertEqual(owners, ["@moira"])

    def test_settings_dir_match(self):
        owners, _ = sr.owners_for("app/src/settings/ssh.rs", self.rules)
        self.assertEqual(owners, ["@lucie"])

    def test_fallback_to_default(self):
        owners, pat = sr.owners_for("crates/warp_features/src/lib.rs", self.rules)
        self.assertEqual(owners, ["@warpdotdev/oss-maintainers"])
        self.assertEqual(pat, "/")

    def test_no_rules_returns_none(self):
        self.assertEqual(sr.owners_for("anything", []), (None, None))


class TestParseOwnership(unittest.TestCase):
    def test_parses_and_skips_comments_blanks(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "STAKEHOLDERS"
            f.write_text(
                "# a comment\n"
                "\n"
                "/app/ @alice @bob\n"
                "/lib/ @warpdotdev/team\n"
                "/no-owner-here/\n",  # line without owners is ignored
                encoding="utf-8",
            )
            rules = sr.parse_ownership(f)
        self.assertEqual(rules, [("/app/", ["@alice", "@bob"]), ("/lib/", ["@warpdotdev/team"])])

    def test_missing_file_returns_empty(self):
        self.assertEqual(sr.parse_ownership(Path("/nope/does/not/exist")), [])


class TestMainCLI(unittest.TestCase):
    """End-to-end test of the script: ownership files -> deduped reviewers + teams."""

    def _make_repo(self, root, stakeholders):
        gh = Path(root) / ".github"
        gh.mkdir(parents=True, exist_ok=True)
        (gh / "STAKEHOLDERS").write_text(stakeholders, encoding="utf-8")

    def test_resolution_dedup_and_team_split(self):
        with tempfile.TemporaryDirectory() as d:
            warp = Path(d) / "warp"
            server = Path(d) / "warp-server"
            self._make_repo(
                warp,
                "/ @warpdotdev/oss-maintainers\n"
                "/app/src/settings/ @lucie\n"
                "/app/src/ai/agent/ @zach\n",
            )
            self._make_repo(server, "/router/ @ian\n")
            result = subprocess.run(
                [
                    sys.executable,
                    str(_MODULE_PATH),
                    "--warp",
                    str(warp),
                    "--warp-server",
                    str(server),
                    "warp:app/src/settings/ssh.rs",
                    "warp:app/src/settings/code.rs",  # same owner -> dedup
                    "warp:app/src/ai/agent/api.rs",
                    "warp:crates/warp_features/src/lib.rs",  # default team fallback
                    "warp-server:router/handlers/x.go",
                    "warp-server:nope/unmatched.go",  # no match -> unresolved
                ],
                capture_output=True,
                text=True,
                stdin=subprocess.DEVNULL,
            )
        out = result.stdout
        self.assertEqual(result.returncode, 0, result.stderr)
        # Users deduped (lucie once) and ordered; teams separated.
        self.assertIn("Reviewers (users): lucie, zach, ian", out)
        self.assertIn("Reviewers (teams): warpdotdev/oss-maintainers", out)
        # gh snippet present.
        self.assertIn("--add-reviewer lucie,zach,ian,warpdotdev/oss-maintainers", out)
        # The unmatched server path is reported, not fatal.
        self.assertIn("no owner match", out)

    def test_reviewers_only_prints_bare_add_reviewer_argument(self):
        """--reviewers-only must be directly consumable by `gh pr edit --add-reviewer`."""
        with tempfile.TemporaryDirectory() as d:
            warp = Path(d) / "warp"
            self._make_repo(
                warp,
                "/ @warpdotdev/oss-maintainers\n/app/src/settings/ @lucie\n",
            )
            result = subprocess.run(
                [
                    sys.executable,
                    str(_MODULE_PATH),
                    "--reviewers-only",
                    "--warp",
                    str(warp),
                    "warp:app/src/settings/ssh.rs",
                    "warp:crates/warp_features/src/lib.rs",  # default team fallback
                ],
                capture_output=True,
                text=True,
                stdin=subprocess.DEVNULL,
            )
        self.assertEqual(result.returncode, 0, result.stderr)
        # Exactly one line, no resolution table, no "Suggested command" prose.
        self.assertEqual(result.stdout, "lucie,warpdotdev/oss-maintainers\n")

    def test_reviewers_only_is_empty_when_nothing_resolves(self):
        """An empty result is the caller's cue to use the fallback reviewer."""
        with tempfile.TemporaryDirectory() as d:
            warp = Path(d) / "warp"
            self._make_repo(warp, "/app/src/settings/ @lucie\n")
            result = subprocess.run(
                [
                    sys.executable,
                    str(_MODULE_PATH),
                    "--reviewers-only",
                    "--warp",
                    str(warp),
                    "warp:crates/nothing/owns/this.rs",
                ],
                capture_output=True,
                text=True,
                stdin=subprocess.DEVNULL,
            )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "")
        # A silent fallback is indistinguishable from a correct resolution when you
        # read the log afterwards, so the reason must still surface on stderr.
        self.assertIn("no owner match", result.stderr)
        self.assertIn("no owners resolved", result.stderr)

    def test_reviewers_only_keeps_stdout_clean_when_diagnosing(self):
        """Diagnostics must not leak into the captured reviewer list."""
        with tempfile.TemporaryDirectory() as d:
            warp = Path(d) / "warp"
            self._make_repo(warp, "/app/src/settings/ @lucie\n")
            result = subprocess.run(
                [
                    sys.executable,
                    str(_MODULE_PATH),
                    "--reviewers-only",
                    "--warp",
                    str(warp),
                    "warp:app/src/settings/ssh.rs",  # resolves
                    "warp:crates/nothing/owns/this.rs",  # does not
                ],
                capture_output=True,
                text=True,
                stdin=subprocess.DEVNULL,
            )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "lucie\n")
        self.assertIn("no owner match", result.stderr)

    def test_warp_internal_alias(self):
        with tempfile.TemporaryDirectory() as d:
            warp = Path(d) / "warp"
            self._make_repo(warp, "/app/ @alice\n")
            result = subprocess.run(
                [
                    sys.executable,
                    str(_MODULE_PATH),
                    "--warp",
                    str(warp),
                    "warp-internal:app/x.rs",  # alias should resolve against --warp
                ],
                capture_output=True,
                text=True,
                stdin=subprocess.DEVNULL,
            )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Reviewers (users): alice", result.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
