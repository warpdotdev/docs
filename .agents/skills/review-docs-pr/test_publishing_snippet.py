#!/usr/bin/env python3
"""Regression test for the manual review-publishing snippet in SKILL.md.

`review-docs-pr/SKILL.md` documents two ways a `[SIGNAL:pr-review]` record
reaches GitHub: the automated `agent-docs-review.yml` workflow, which calls
`doc_quality_policy/publish_review_signal.py`, and the manual/interactive
path documented under "Publishing a GitHub review" here, whose python
snippet independently builds the same review body. The two must stay in
sync: PR #686 hid the signal behind an HTML comment in
`publish_review_signal.py` but initially left this documented snippet
rendering it under a visible "## Review signal" heading, so a manually
published review kept leaking the machine-readable record into GitHub's
rendered PR body.

This extracts the documented bash+python snippet and runs it against a
stubbed `review.json` and signal file, exercising the exact text agents
copy rather than a paraphrase of it.

Run with: python3 .agents/skills/review-docs-pr/test_publishing_snippet.py
"""
from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL = HERE / "SKILL.md"

_spec = importlib.util.spec_from_file_location(
    "verify_review_signal",
    HERE.parent / "doc_quality_policy" / "verify_review_signal.py",
)
vrs = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = vrs
_spec.loader.exec_module(vrs)


def extract_publishing_snippet(signal_path: Path, request_path: Path) -> str:
    """Extract the documented python heredoc that builds the pinned review payload.

    Retargets the hardcoded `/tmp/review-signal.json` and
    `/tmp/review-request.json` paths to test-local paths so the test does
    not read or write real `/tmp` state.
    """
    text = SKILL.read_text(encoding="utf-8")
    anchor = text.index("2. Write the signal JSON object")
    match = re.search(r"```bash\n((?: {3}[^\n]*\n|\n)+?) {3}```", text[anchor:])
    if not match:
        raise AssertionError("publishing snippet not found in review-docs-pr/SKILL.md")
    lines = match.group(1).splitlines()
    dedented = "\n".join(line[3:] if line.startswith("   ") else line for line in lines)
    dedented = dedented.replace("/tmp/review-signal.json", str(signal_path))
    dedented = dedented.replace("/tmp/review-request.json", str(request_path))
    return dedented


class PublishingSnippetTest(unittest.TestCase):
    def _run(self, *, comments=None, summary="Looks good.", verdict="Approve"):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            signal_path = root / "review-signal.json"
            request_path = root / "review-request.json"
            (root / "review.json").write_text(
                json.dumps({"summary": summary, "comments": comments or []}),
                encoding="utf-8",
            )
            signal = {
                "pr": "1",
                "head_sha": "sha1",
                "verdict": verdict,
                "critical": 0,
                "important": 0,
                "reviewer_login": "some-reviewer",
            }
            signal_path.write_text(json.dumps(signal), encoding="utf-8")

            snippet = extract_publishing_snippet(signal_path, request_path)
            snippet = snippet.replace(
                'HEAD_SHA="<evaluated PR head SHA>"', 'HEAD_SHA="sha1"'
            )
            snippet = snippet.replace(
                'VERDICT="<Approve|Approve with nits|Request changes>"',
                f'VERDICT="{verdict}"',
            )

            result = subprocess.run(
                ["bash", "-c", snippet],
                cwd=root,
                capture_output=True,
                text=True,
                stdin=subprocess.DEVNULL,
                timeout=10,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(request_path.read_text(encoding="utf-8"))
        return payload, signal

    def test_signal_is_hidden_in_html_comment(self):
        payload, _ = self._run()
        self.assertNotIn("## Review signal", payload["body"])
        self.assertIn("<!-- [SIGNAL:pr-review]", payload["body"])

    def test_hidden_signal_remains_parseable(self):
        payload, signal = self._run()
        parsed, problems = vrs._parse_signal(
            payload["body"], signal["pr"], signal["head_sha"]
        )
        self.assertEqual(problems, [])
        self.assertEqual(parsed["verdict"], signal["verdict"])

    def test_findings_and_verdict_are_still_rendered(self):
        payload, _ = self._run(
            comments=[{"path": "a.md", "line": 3, "body": "Fix this typo."}],
            verdict="Request changes",
        )
        self.assertIn("## Findings", payload["body"])
        self.assertIn("`a.md:3` — Fix this typo.", payload["body"])
        self.assertIn("## Verdict\nRequest changes", payload["body"])
        self.assertEqual(payload["event"], "REQUEST_CHANGES")


if __name__ == "__main__":
    if sys.platform.startswith("win"):
        print("skipping: publishing snippet requires bash")
        sys.exit(0)
    unittest.main()
