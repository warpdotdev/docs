#!/usr/bin/env python3
"""Regression tests for request-engineering-review.yml reviewer routing.

The tests execute the workflow's exact run block with a stubbed `gh` command.
They cover the add-once policy: exactly one distinct human owner, no existing
request or submitted review, and no reviewer-removal event.

Run with: python3 .github/workflows/test_request_engineering_review.py
"""

import json
import os
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


WORKFLOW = Path(__file__).with_name("request-engineering-review.yml")
REPO_ROOT = WORKFLOW.parents[2]

GH_STUB = """#!/usr/bin/env python3
import json
import os
import sys
from pathlib import Path

args = sys.argv[1:]
calls_file = Path(os.environ["GH_STUB_CALLS"])
with calls_file.open("a", encoding="utf-8") as stream:
    stream.write(json.dumps(args) + "\\n")

if args[:2] == ["pr", "view"]:
    print(os.environ.get("GH_STUB_REQUESTED", ""))
    sys.exit(0)
if args[:1] == ["api"]:
    endpoint = args[1]
    if endpoint.endswith("/reviews"):
        print(os.environ.get("GH_STUB_REVIEWED", ""))
    elif endpoint.endswith("/timeline"):
        print(os.environ.get("GH_STUB_REMOVED", ""))
    else:
        sys.exit(1)
    sys.exit(0)
if args[:2] == ["pr", "edit"]:
    sys.exit(0)
sys.exit(1)
"""


def reviewer_request_script():
    """Extract and dedent the workflow's reviewer-request run block."""
    text = WORKFLOW.read_text(encoding="utf-8")
    start = text.index("          printf '%s' \"$PR_BODY\" > /tmp/pr-body.md")
    return textwrap.dedent(text[start:])


def risk_body(reviewers):
    return (
        "## Documentation risk\n"
        "Risk: engineering-review-required\n"
        "Rationale: Changes a technical claim.\n"
        f"Requested engineering reviewers: {reviewers}\n"
        "Engineering review status: pending\n"
        "Docs override: none\n"
    )


class EngineeringReviewRequestTest(unittest.TestCase):
    def run_request(
        self, reviewers, *, requested="", reviewed="", removed=""
    ):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bin_dir = root / "bin"
            bin_dir.mkdir()
            gh = bin_dir / "gh"
            gh.write_text(GH_STUB, encoding="utf-8")
            gh.chmod(0o755)

            calls_file = root / "calls.jsonl"
            calls_file.write_text("", encoding="utf-8")
            env = os.environ.copy()
            env.update(
                {
                    "PATH": f"{bin_dir}{os.pathsep}{env['PATH']}",
                    "GH_STUB_CALLS": str(calls_file),
                    "GH_STUB_REQUESTED": requested,
                    "GH_STUB_REVIEWED": reviewed,
                    "GH_STUB_REMOVED": removed,
                    "PR_BODY": risk_body(reviewers),
                    "PR_NUMBER": "123",
                    "REPOSITORY": "warpdotdev/docs",
                }
            )
            result = subprocess.run(
                ["bash", "-c", reviewer_request_script()],
                cwd=REPO_ROOT,
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

    def test_single_human_owner_is_requested(self):
        result, calls = self.run_request("alice")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.requested_reviewers(calls), ["alice"])

    def test_team_and_single_human_requests_only_the_human(self):
        result, calls = self.run_request("warpdotdev/docs, alice")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.requested_reviewers(calls), ["alice"])

    def test_multiple_human_owners_request_nobody(self):
        result, calls = self.run_request("alice, bob")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.requested_reviewers(calls), [])
        self.assertIn("multiple human owners", result.stdout)

    def test_duplicate_human_owner_is_requested_once(self):
        result, calls = self.run_request("alice, Alice")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.requested_reviewers(calls), ["alice"])

    def test_existing_requested_reviewer_stops_request(self):
        result, calls = self.run_request("alice", requested="carol")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.requested_reviewers(calls), [])

    def test_any_submitted_review_stops_request(self):
        result, calls = self.run_request("alice", reviewed="carol")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.requested_reviewers(calls), [])
        self.assertIn("already has submitted review(s)", result.stdout)

    def test_any_reviewer_removal_stops_request(self):
        result, calls = self.run_request("alice", removed="carol")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.requested_reviewers(calls), [])
        self.assertIn("reviewer-removal event(s)", result.stdout)


if __name__ == "__main__":
    if sys.platform.startswith("win"):
        print("skipping: reviewer workflow requires bash")
        sys.exit(0)
    unittest.main()
