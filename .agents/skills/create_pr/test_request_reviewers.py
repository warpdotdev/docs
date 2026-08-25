#!/usr/bin/env python3
"""Regression tests for the reviewer-request snippet in create_pr/SKILL.md.

The tests extract the documented bash snippet and run it against stubbed `gh`
and `suggest_reviewers.py` commands. This exercises the text users copy rather
than a paraphrased implementation.

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
    """Extract the bash fence whose first two assignments identify the snippet."""
    text = SKILL.read_text(encoding="utf-8")
    match = re.search(
        r"```bash\n(PR=123\nFALLBACK_REVIEWER=dannyneira\n.*?)(?=\n```)",
        text,
        re.DOTALL,
    )
    if not match:
        raise AssertionError("reviewer-request snippet not found in SKILL.md")
    return match.group(1)


class ReviewerSnippetTest(unittest.TestCase):
    def run_snippet(self, *, initial=(), resolved="", reject=""):
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

    def test_resolved_owner_lands(self):
        result, state, calls = self.run_snippet(resolved="alice")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(state, ["alice"])
        self.assertEqual(self.requested_reviewers(calls), ["alice"])

    def test_empty_resolution_requests_fallback(self):
        result, state, calls = self.run_snippet()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(state, ["dannyneira"])
        self.assertEqual(self.requested_reviewers(calls), ["dannyneira"])

    def test_unrelated_existing_reviewer_does_not_skip_fallback(self):
        result, state, calls = self.run_snippet(initial=["carol"])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("dannyneira", self.requested_reviewers(calls))
        self.assertEqual(set(state), {"carol", "dannyneira"})
        self.assertIn(
            "no owner resolved for PR 123; fallback dannyneira requested",
            result.stdout,
        )

    def test_unrelated_reviewer_does_not_mask_fallback_failure(self):
        result, state, calls = self.run_snippet(
            initial=["carol"], reject="dannyneira"
        )
        self.assertIn("dannyneira", self.requested_reviewers(calls))
        self.assertEqual(state, ["carol"])
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(
            "ERROR: fallback dannyneira could not be requested on PR 123",
            result.stdout,
        )
        self.assertNotIn("note: no owner resolved", result.stdout)


if __name__ == "__main__":
    if sys.platform.startswith("win"):
        print("skipping: reviewer snippet requires bash")
        sys.exit(0)
    unittest.main()
