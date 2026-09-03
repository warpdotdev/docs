#!/usr/bin/env python3
"""Regression tests for release-docs-update.yml reviewer assignment.

The tests execute the workflow's exact final run block with stubbed `oz` and
`gh` commands. This specifically guards against GitHub silently dropping both
the selected reviewer and the final dannyneira fallback.

Run with: python3 .github/workflows/test_release_docs_reviewer.py
"""

import json
import os
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path


WORKFLOW = Path(__file__).with_name("release-docs-update.yml")

OZ_STUB = """#!/usr/bin/env python3
print("PR: docs #123")
"""
GREP_STUB = """#!/bin/sh
cat >/dev/null
printf '123\\n'
"""

GH_STUB = """#!/usr/bin/env python3
import json
import os
import sys
from pathlib import Path

state_file = Path(os.environ["GH_STUB_STATE"])
calls_file = Path(os.environ["GH_STUB_CALLS"])
silent_drops = set(filter(None, os.environ.get("GH_STUB_SILENT_DROPS", "").split(",")))
args = sys.argv[1:]

with calls_file.open("a", encoding="utf-8") as stream:
    stream.write(json.dumps(args) + "\\n")

if args[:1] == ["api"]:
    print("[]")
    sys.exit(0)

state = json.loads(state_file.read_text(encoding="utf-8"))
if args[:2] == ["pr", "edit"]:
    reviewer = args[args.index("--add-reviewer") + 1]
    if reviewer not in silent_drops and reviewer not in state:
        state.append(reviewer)
        state_file.write_text(json.dumps(state), encoding="utf-8")
    sys.exit(0)
if args[:2] == ["pr", "view"]:
    print(",".join(state))
    sys.exit(0)
sys.exit(1)
"""


def reviewer_assignment_script():
    """Extract and dedent the workflow's exact final reviewer-assignment run."""
    text = WORKFLOW.read_text(encoding="utf-8")
    start = text.index("          # Get the PR number from the oz run")
    return textwrap.dedent(text[start:]).replace(
        "${{ steps.oz-dispatch.outputs.run_id }}", "test-run-id"
    )


class ReleaseDocsReviewerTest(unittest.TestCase):
    def run_assignment(self, *, silent_drops=()):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bin_dir = root / "bin"
            bin_dir.mkdir()
            for name, source in (
                ("oz", OZ_STUB),
                ("grep", GREP_STUB),
                ("gh", GH_STUB),
            ):
                command = bin_dir / name
                command.write_text(source, encoding="utf-8")
                command.chmod(0o755)

            state_file = root / "state.json"
            calls_file = root / "calls.jsonl"
            state_file.write_text("[]", encoding="utf-8")
            calls_file.write_text("", encoding="utf-8")
            env = os.environ.copy()
            env.update(
                {
                    "PATH": f"{bin_dir}{os.pathsep}{env['PATH']}",
                    "GH_STUB_STATE": str(state_file),
                    "GH_STUB_CALLS": str(calls_file),
                    "GH_STUB_SILENT_DROPS": ",".join(silent_drops),
                }
            )
            result = subprocess.run(
                ["bash", "-c", reviewer_assignment_script()],
                cwd=root,
                env=env,
                capture_output=True,
                text=True,
            )
            calls = [
                json.loads(line)
                for line in calls_file.read_text(encoding="utf-8").splitlines()
            ]
        return result, calls

    @staticmethod
    def requested_reviewers(calls):
        return [
            call[call.index("--add-reviewer") + 1]
            for call in calls
            if call[:2] == ["pr", "edit"]
        ]

    def test_fails_when_final_fallback_is_silently_dropped(self):
        result, calls = self.run_assignment(
            silent_drops=("hongyi-chen", "dannyneira")
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(
            self.requested_reviewers(calls), ["hongyi-chen", "dannyneira"]
        )
        self.assertIn(
            "::error::dannyneira is not on the reviewRequests read-back either",
            result.stdout,
        )

    def test_succeeds_when_final_fallback_is_confirmed(self):
        result, calls = self.run_assignment(silent_drops=("hongyi-chen",))
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertEqual(
            self.requested_reviewers(calls), ["hongyi-chen", "dannyneira"]
        )


if __name__ == "__main__":
    unittest.main()
