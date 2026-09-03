#!/usr/bin/env python3
"""Unit tests for check_pr_contract.py.

Stdlib unittest only, no third-party deps and no network. Exercises the CLI
via `main()` directly (no subprocess) so coverage tools see it, with explicit
changed-file arguments to avoid depending on git state.

Run:
    python3 .agents/skills/doc_quality_policy/test_check_pr_contract.py
"""
from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

_HERE = Path(__file__).resolve().parent

_policy_spec = importlib.util.spec_from_file_location("doc_quality_policy", _HERE / "policy.py")
policy = importlib.util.module_from_spec(_policy_spec)
sys.modules[_policy_spec.name] = policy
_policy_spec.loader.exec_module(policy)

_spec = importlib.util.spec_from_file_location("check_pr_contract", _HERE / "check_pr_contract.py")
cpc = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = cpc
_spec.loader.exec_module(cpc)


LOW_RISK_BODY = (
    "## Documentation risk\nRisk: low\nRationale: typo fix.\nDocs override: none\n\n"
    "## Unverified claims\nNone — all claims verified against source.\n"
)


class TestCheckPrContractCli(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.tmp_path = Path(self._tmp.name)

    def _write(self, name: str, content: str) -> Path:
        p = self.tmp_path / name
        p.write_text(content, encoding="utf-8")
        return p

    def test_clean_low_risk_body_passes(self):
        body = self._write("body.md", LOW_RISK_BODY)
        content = self._write("page.mdx", "no verify markers here")
        self.assertEqual(cpc.main(["--body", str(body), str(content)]), 0)

    def test_unlisted_verify_marker_fails(self):
        body = self._write("body.md", LOW_RISK_BODY)
        content = self._write("page.mdx", "{/* VERIFY: some claim */}")
        self.assertEqual(cpc.main(["--body", str(body), str(content)]), 1)

    def test_engineering_review_with_approval_and_listed_marker_passes(self):
        body_text = (
            "## Documentation risk\nRisk: engineering-review-required\nRationale: new flag.\n"
            "Requested engineering reviewers: alice\nEngineering review status: pending\n"
            "Docs override: none\n\n## Unverified claims\n- some claim\n"
        )
        body = self._write("body.md", body_text)
        content = self._write("page.mdx", "{/* VERIFY: some claim */}")
        self.assertEqual(
            cpc.main(["--body", str(body), str(content), "--source-owner-approved"]), 0,
        )

    def test_docs_verified_override_with_current_head_sha_passes(self):
        body_text = (
            "## Documentation risk\nRisk: engineering-review-required\nRationale: new flag.\n"
            "Docs override: docs-verified\nOverride reviewer: hongyi-chen\n"
            "Override reason: Confirmed against source.\nOverride evidence: app/foo.rs@abc\n"
            "Override head SHA: deadbeef\n\n## Unverified claims\nNone\n"
        )
        body = self._write("body.md", body_text)
        content = self._write("page.mdx", "no markers")
        self.assertEqual(
            cpc.main(["--body", str(body), str(content), "--head-sha", "deadbeef"]), 0,
        )

    def test_docs_verified_override_with_stale_head_sha_fails(self):
        body_text = (
            "## Documentation risk\nRisk: engineering-review-required\nRationale: new flag.\n"
            "Docs override: docs-verified\nOverride reviewer: hongyi-chen\n"
            "Override reason: Confirmed against source.\nOverride evidence: app/foo.rs@abc\n"
            "Override head SHA: old-sha\n\n## Unverified claims\nNone\n"
        )
        body = self._write("body.md", body_text)
        content = self._write("page.mdx", "no markers")
        self.assertEqual(
            cpc.main(["--body", str(body), str(content), "--head-sha", "new-sha"]), 1,
        )

    def test_missing_body_file_is_usage_error(self):
        self.assertEqual(cpc.main(["--body", str(self.tmp_path / "nope.md")]), 2)


if __name__ == "__main__":
    unittest.main()
