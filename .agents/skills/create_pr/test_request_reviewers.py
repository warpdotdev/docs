#!/usr/bin/env python3
"""Regression tests for the reviewer-request snippet in create_pr/SKILL.md.

The tests extract the documented bash snippet and run it against a stubbed
`gh` and `suggest_reviewers.py`, so they exercise the exact text agents copy
rather than a paraphrased implementation.

The policy under test: at most ONE human reviewer, requested only when
ownership resolution names exactly one owning engineer; no fallback reviewer
of any kind; teams are never requested; a PR that already has a reviewer gets
no additions; and a reviewer a human removed (a `review_request_removed`
timeline event) is never re-added.

Run with: python3 .agents/skills/create_pr/test_request_reviewers.py
"""

import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
SKILL = HERE / "SKILL.md"

GH_STUB = """#!/usr/bin/env python3
import json
import os
import sys
from pathlib import Path

state_file = Path(os.environ["GH_STUB_STATE"])
calls_file = Path(os.environ["GH_STUB_CALLS"])
reject = set(filter(None, os.environ.get("GH_STUB_REJECT", "").split(",")))
args = sys.argv[1:]

with calls_file.open("a", encoding="utf-8") as stream:
    stream.write(json.dumps(args) + "\\n")

if args[:1] == ["api"]:
    # The snippet's only `gh api` call is the timeline query for
    # review_request_removed events; answer with the pre-joined list.
    print(os.environ.get("GH_STUB_REMOVED", ""))
    sys.exit(0)

state = json.loads(state_file.read_text(encoding="utf-8"))
if args[:2] == ["pr", "edit"]:
    reviewer = args[args.index("--add-reviewer") + 1]
    if reviewer in reject:
        sys.exit(1)
    if reviewer not in state:
        state.append(reviewer)
    state_file.write_text(json.dumps(state), encoding="utf-8")
    sys.exit(0)
if args[:2] == ["pr", "view"]:
    print(",".join(state))
    sys.exit(0)
sys.exit(1)
"""

RESOLVER_STUB = """#!/usr/bin/env python3
import os
import sys
sys.stdout.write(os.environ.get("STUB_REVIEWERS", ""))
"""


def extract_reviewer_snippet():
    """Extract the bash fence whose first line identifies the snippet."""
    text = SKILL.read_text(encoding="utf-8")
    match = re.search(r"```bash\n(PR=123\n.*?)(?=\n```)", text, re.DOTALL)
    if not match:
        raise AssertionError("reviewer-request snippet not found in SKILL.md")
    return match.group(1)


class ReviewerSnippetTest(unittest.TestCase):
    def run_snippet(self, *, initial=(), resolved="", reject="", removed=""):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bin_dir = root / "bin"
            bin_dir.mkdir()
            gh = bin_dir / "gh"
            gh.write_text(GH_STUB, encoding="utf-8")
            gh.chmod(0o755)

            resolver = (
                root / ".agents/skills/missing_docs/scripts/suggest_reviewers.py"
            )
            resolver.parent.mkdir(parents=True)
            resolver.write_text(RESOLVER_STUB, encoding="utf-8")
            resolver.chmod(0o755)

            state_file = root / "state.json"
            state_file.write_text(json.dumps(list(initial)), encoding="utf-8")
            calls_file = root / "calls.jsonl"
            calls_file.write_text("", encoding="utf-8")

            env = os.environ.copy()
            env.update(
                {
                    "PATH": f"{bin_dir}{os.pathsep}{env['PATH']}",
                    "GH_STUB_STATE": str(state_file),
                    "GH_STUB_CALLS": str(calls_file),
                    "GH_STUB_REJECT": reject,
                    "GH_STUB_REMOVED": removed,
                    "STUB_REVIEWERS": resolved,
                }
            )
            result = subprocess.run(
                ["bash", "-c", extract_reviewer_snippet()],
                cwd=root,
                env=env,
                capture_output=True,
                text=True,
            )
            state = json.loads(state_file.read_text(encoding="utf-8"))
            calls = [
                json.loads(line)
                for line in calls_file.read_text(encoding="utf-8").splitlines()
            ]
        return result, state, calls

    @staticmethod
    def requested_reviewers(calls):
        return [
            call[call.index("--add-reviewer") + 1]
            for call in calls
            if call[:2] == ["pr", "edit"]
        ]

    def test_single_owner_is_requested(self):
        result, state, calls = self.run_snippet(resolved="alice")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(state, ["alice"])
        self.assertEqual(self.requested_reviewers(calls), ["alice"])
        self.assertIn("Requested reviewer: alice", result.stdout)

    def test_team_entries_are_never_requested(self):
        """A user+team resolution requests only the single human."""
        result, state, calls = self.run_snippet(
            resolved="alice,warpdotdev/oss-maintainers"
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(state, ["alice"])
        self.assertEqual(self.requested_reviewers(calls), ["alice"])

    def test_team_only_resolution_requests_nobody(self):
        result, state, calls = self.run_snippet(resolved="warpdotdev/oss-maintainers")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(state, [])
        self.assertEqual(self.requested_reviewers(calls), [])
        self.assertIn("no owner resolved", result.stdout)

    def test_empty_resolution_requests_nobody(self):
        """No owner means no request - there is no fallback reviewer."""
        result, state, calls = self.run_snippet()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(state, [])
        self.assertEqual(self.requested_reviewers(calls), [])
        self.assertIn("no requested reviewer", result.stdout)

    def test_multiple_owners_is_not_conviction(self):
        """Two distinct resolved users is ambiguity - request nobody."""
        result, state, calls = self.run_snippet(resolved="alice,bob")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(state, [])
        self.assertEqual(self.requested_reviewers(calls), [])
        self.assertIn("no single clear owner", result.stdout)

    def test_duplicate_entries_are_still_one_owner(self):
        result, state, calls = self.run_snippet(resolved="alice,alice")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(state, ["alice"])
        self.assertEqual(self.requested_reviewers(calls), ["alice"])

    def test_existing_reviewer_means_no_new_request(self):
        """A PR that already has any reviewer gets no additions."""
        result, state, calls = self.run_snippet(initial=["carol"], resolved="alice")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(state, ["carol"])
        self.assertEqual(self.requested_reviewers(calls), [])
        self.assertIn("already has reviewer(s)", result.stdout)

    def test_removed_reviewer_is_never_readded(self):
        """A human removed the resolved owner from this PR - stay removed."""
        result, state, calls = self.run_snippet(resolved="alice", removed="alice")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(state, [])
        self.assertEqual(self.requested_reviewers(calls), [])
        self.assertIn("not re-adding", result.stdout)

    def test_removed_check_is_case_insensitive(self):
        result, state, calls = self.run_snippet(resolved="alice", removed="Alice")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(state, [])
        self.assertEqual(self.requested_reviewers(calls), [])

    def test_unrelated_removed_reviewer_does_not_block(self):
        result, state, calls = self.run_snippet(resolved="alice", removed="bob")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(state, ["alice"])
        self.assertEqual(self.requested_reviewers(calls), ["alice"])

    def test_failed_request_does_not_fall_back(self):
        """A rejected request is reported; nobody else is substituted."""
        result, state, calls = self.run_snippet(resolved="alice", reject="alice")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(state, [])
        self.assertEqual(self.requested_reviewers(calls), ["alice"])
        self.assertIn("could not request alice", result.stdout)


if __name__ == "__main__":
    if sys.platform.startswith("win"):
        print("skipping: reviewer snippet requires bash")
        sys.exit(0)
    unittest.main()
