#!/usr/bin/env python3
"""Regression tests for the reviewer-request snippet in create_pr/SKILL.md.

The tests extract the documented bash snippet and run it against stubbed `gh`,
`suggest_reviewers.py`, and `factory-resolve-reviewer` commands. This exercises
the text users copy rather than a paraphrased implementation.

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

REQUESTER_RESOLVER_STUB = """#!/usr/bin/env python3
import os
import sys
sys.stdout.write(os.environ.get("STUB_REQUESTER_REVIEWER", ""))
"""


def extract_reviewer_snippet(requester_slack_id=None, secondary_fallback=None):
    """Extract the bash fence whose first assignments identify the snippet.

    ``requester_slack_id`` / ``secondary_fallback``, when given, override the
    documented placeholder values via targeted substitution so tests can
    exercise the requester and secondary-fallback tiers without hand-copying
    the script's logic.
    """
    text = SKILL.read_text(encoding="utf-8")
    match = re.search(
        r"```bash\n(PR=123\nREQUESTER_SLACK_ID=.*?)(?=\n```)",
        text,
        re.DOTALL,
    )
    if not match:
        raise AssertionError("reviewer-request snippet not found in SKILL.md")
    snippet = match.group(1)

    if requester_slack_id is not None:
        snippet, count = re.subn(
            r'REQUESTER_SLACK_ID="[^"]*"',
            'REQUESTER_SLACK_ID="%s"' % requester_slack_id,
            snippet,
            count=1,
        )
        if count != 1:
            raise AssertionError("could not override REQUESTER_SLACK_ID in snippet")

    if secondary_fallback is not None:
        snippet, count = re.subn(
            r"SECONDARY_FALLBACK_REVIEWER=\S+",
            "SECONDARY_FALLBACK_REVIEWER=%s" % secondary_fallback,
            snippet,
            count=1,
        )
        if count != 1:
            raise AssertionError(
                "could not override SECONDARY_FALLBACK_REVIEWER in snippet"
            )

    return snippet


class ReviewerSnippetTest(unittest.TestCase):
    def run_snippet(
        self,
        *,
        initial=(),
        resolved="",
        reject="",
        requester_slack_id=None,
        requester_resolved="",
        secondary_fallback=None,
    ):
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

            requester_resolver = root / "scripts/factory-resolve-reviewer"
            requester_resolver.parent.mkdir(parents=True)
            requester_resolver.write_text(REQUESTER_RESOLVER_STUB, encoding="utf-8")
            requester_resolver.chmod(0o755)

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
                    "STUB_REQUESTER_REVIEWER": requester_resolved,
                }
            )
            snippet = extract_reviewer_snippet(
                requester_slack_id=requester_slack_id,
                secondary_fallback=secondary_fallback,
            )
            result = subprocess.run(
                ["bash", "-c", snippet],
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

    def test_secondary_fallback_used_with_no_requester_context(self):
        """The documented default (no REQUESTER_SLACK_ID) skips straight to HYC."""
        result, state, calls = self.run_snippet()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(state, ["hongyi-chen"])
        self.assertEqual(self.requested_reviewers(calls), ["hongyi-chen"])

    def test_requester_resolves_before_secondary_and_final_fallback(self):
        result, state, calls = self.run_snippet(
            requester_slack_id="U_TEST", requester_resolved="the-requester"
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(state, ["the-requester"])
        self.assertEqual(self.requested_reviewers(calls), ["the-requester"])

    def test_secondary_fallback_used_when_requester_unresolved(self):
        result, state, calls = self.run_snippet(requester_slack_id="U_TEST")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(state, ["hongyi-chen"])
        self.assertEqual(self.requested_reviewers(calls), ["hongyi-chen"])

    def test_final_fallback_still_reachable_when_secondary_unset(self):
        """dannyneira remains the ultimate safety net if HYC is ever blanked."""
        result, state, calls = self.run_snippet(secondary_fallback="")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(state, ["dannyneira"])
        self.assertEqual(self.requested_reviewers(calls), ["dannyneira"])

    def test_unrelated_existing_reviewer_does_not_skip_fallback(self):
        result, state, calls = self.run_snippet(initial=["carol"])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("hongyi-chen", self.requested_reviewers(calls))
        self.assertEqual(set(state), {"carol", "hongyi-chen"})
        self.assertIn(
            "no owner resolved for PR 123; fallback hongyi-chen requested",
            result.stdout,
        )

    def test_unrelated_reviewer_does_not_mask_fallback_failure(self):
        result, state, calls = self.run_snippet(
            initial=["carol"], reject="hongyi-chen"
        )
        self.assertIn("hongyi-chen", self.requested_reviewers(calls))
        self.assertEqual(state, ["carol"])
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(
            "ERROR: fallback hongyi-chen could not be requested on PR 123",
            result.stdout,
        )
        self.assertNotIn("note: no owner resolved", result.stdout)


if __name__ == "__main__":
    if sys.platform.startswith("win"):
        print("skipping: reviewer snippet requires bash")
        sys.exit(0)
    unittest.main()
