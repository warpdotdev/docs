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
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

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

    def _write_authorized_reviewers_fixture(self) -> Path:
        return self._write(
            "authorized.json", json.dumps({"authorized_docs_reviewers": ["hongyi-chen"]}),
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
        authorized = self._write_authorized_reviewers_fixture()
        self.assertEqual(
            cpc.main([
                "--body", str(body), str(content), "--head-sha", "deadbeef",
                "--authorized-reviewers-file", str(authorized),
                "--enforce-engineering-gate", "--approved-reviewer", "hongyi-chen",
            ]), 0,
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
        authorized = self._write_authorized_reviewers_fixture()
        self.assertEqual(
            cpc.main([
                "--body", str(body), str(content), "--head-sha", "new-sha",
                "--authorized-reviewers-file", str(authorized),
                "--enforce-engineering-gate", "--approved-reviewer", "hongyi-chen",
            ]), 1,
        )

    def test_docs_verified_override_by_unauthorized_reviewer_fails_with_no_fixture(self):
        """Without an explicit --authorized-reviewers-file and outside a git
        checkout with the trusted ref, the allowlist load fails closed to
        empty -- so even a plausible-looking override author is rejected.
        """
        body_text = (
            "## Documentation risk\nRisk: engineering-review-required\nRationale: new flag.\n"
            "Docs override: docs-verified\nOverride reviewer: hongyi-chen\n"
            "Override reason: Confirmed against source.\nOverride evidence: app/foo.rs@abc\n"
            "Override head SHA: deadbeef\n\n## Unverified claims\nNone\n"
        )
        body = self._write("body.md", body_text)
        content = self._write("page.mdx", "no markers")
        self.assertEqual(
            cpc.main([
                "--body", str(body), str(content), "--head-sha", "deadbeef",
                "--authorized-reviewers-ref", "refs/does-not-exist",
                "--enforce-engineering-gate", "--approved-reviewer", "hongyi-chen",
            ]), 1,
        )

    def test_missing_body_file_is_usage_error(self):
        self.assertEqual(cpc.main(["--body", str(self.tmp_path / "nope.md")]), 2)


class TestShouldRunContractCheck(unittest.TestCase):
    def test_agent_marked_pull_request_runs(self):
        self.assertTrue(cpc.should_run_contract_check("pull_request", ["warpy-factory", "documentation"]))

    def test_non_agent_pull_request_skips(self):
        self.assertFalse(cpc.should_run_contract_check("pull_request", ["documentation"]))

    def test_pull_request_with_no_labels_skips(self):
        self.assertFalse(cpc.should_run_contract_check("pull_request", []))

    def test_push_event_skips_even_with_the_label(self):
        self.assertFalse(cpc.should_run_contract_check("push", ["warpy-factory"]))


def _git(cmd, cwd):
    subprocess.run(["git", *cmd], cwd=cwd, capture_output=True, text=True, check=True)


class TestLoadAuthorizedReviewersFromRef(unittest.TestCase):
    def test_reads_the_ref_version_not_the_working_tree(self):
        """Regression: a PR that edits its own working-tree copy of
        authorized_docs_reviewers.json to add its author must not thereby
        authorize itself -- the trusted ref's committed version always wins.
        """
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "repo"
            repo.mkdir()
            _git(["init", "-q"], repo)
            _git(["config", "user.email", "test@example.com"], repo)
            _git(["config", "user.name", "Test"], repo)
            rel_path = "authorized_docs_reviewers.json"
            (repo / rel_path).write_text(
                json.dumps({"authorized_docs_reviewers": ["hongyi-chen"]}), encoding="utf-8",
            )
            _git(["add", "."], repo)
            _git(["commit", "-q", "-m", "trusted allowlist"], repo)
            _git(["update-ref", "refs/remotes/origin/main", "HEAD"], repo)

            # Simulate a malicious PR editing its own working-tree copy to
            # add the author, without committing (or on a divergent branch).
            (repo / rel_path).write_text(
                json.dumps({"authorized_docs_reviewers": ["hongyi-chen", "attacker"]}), encoding="utf-8",
            )

            import os
            old_cwd = os.getcwd()
            os.chdir(repo)
            try:
                result = cpc._load_authorized_reviewers_from_ref("origin/main", rel_path)
            finally:
                os.chdir(old_cwd)
            self.assertEqual(result, ["hongyi-chen"])
            self.assertNotIn("attacker", result)

    def test_missing_ref_fails_closed_to_empty_list(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "repo"
            repo.mkdir()
            _git(["init", "-q"], repo)
            import os
            old_cwd = os.getcwd()
            os.chdir(repo)
            try:
                result = cpc._load_authorized_reviewers_from_ref("origin/main", "nope.json")
            finally:
                os.chdir(old_cwd)
            self.assertEqual(result, [])


class TestComputeReviewSignals(unittest.TestCase):
    def test_stale_review_on_old_head_does_not_count(self):
        reviews = [{"user": {"login": "alice"}, "state": "APPROVED", "commit_id": "old-sha"}]
        signals = cpc._compute_review_signals(reviews, ["alice"], "new-sha", checks_passed=True)
        self.assertFalse(signals.source_owner_approved_current_head)

    def test_approval_by_a_requested_reviewer_on_current_head_counts(self):
        reviews = [{"user": {"login": "alice"}, "state": "APPROVED", "commit_id": "sha1"}]
        signals = cpc._compute_review_signals(reviews, ["alice"], "sha1", checks_passed=True)
        self.assertTrue(signals.source_owner_approved_current_head)

    def test_approval_by_a_non_requested_reviewer_does_not_count_as_source_owner(self):
        reviews = [{"user": {"login": "random-person"}, "state": "APPROVED", "commit_id": "sha1"}]
        signals = cpc._compute_review_signals(reviews, ["alice"], "sha1", checks_passed=True)
        self.assertFalse(signals.source_owner_approved_current_head)

    def test_changes_requested_on_current_head_is_unresolved(self):
        reviews = [{"user": {"login": "alice"}, "state": "CHANGES_REQUESTED", "commit_id": "sha1"}]
        signals = cpc._compute_review_signals(reviews, ["alice"], "sha1", checks_passed=True)
        self.assertTrue(signals.has_unresolved_critical_or_important_finding)

    def test_later_approval_supersedes_earlier_changes_requested_by_same_reviewer(self):
        reviews = [
            {"user": {"login": "alice"}, "state": "CHANGES_REQUESTED", "commit_id": "sha1"},
            {"user": {"login": "alice"}, "state": "APPROVED", "commit_id": "sha1"},
        ]
        signals = cpc._compute_review_signals(reviews, ["alice"], "sha1", checks_passed=True)
        self.assertFalse(signals.has_unresolved_critical_or_important_finding)
        self.assertTrue(signals.source_owner_approved_current_head)

    def test_no_reviews_means_no_approval_and_no_unresolved_finding(self):
        signals = cpc._compute_review_signals([], ["alice"], "sha1", checks_passed=True)
        self.assertFalse(signals.source_owner_approved_current_head)
        self.assertFalse(signals.has_unresolved_critical_or_important_finding)

    def test_declared_source_owner_counts_after_pending_request_is_removed(self):
        reviews = [{"user": {"login": "alice"}, "state": "APPROVED", "commit_id": "sha1"}]
        with mock.patch.object(cpc, "_resolve_required_checks_passed", return_value=True), \
             mock.patch.object(cpc, "_fetch_reviews", return_value=reviews), \
             mock.patch.object(cpc, "_fetch_requested_reviewers", return_value=[]):
            signals = cpc.resolve_live_review_signals("o/r", "1", "sha1", ["alice"])
        self.assertTrue(signals.source_owner_approved_current_head)

    def test_override_requires_the_same_fields_in_an_approved_review_body(self):
        override = policy.DocumentationRisk(
            risk=policy.RISK_ENGINEERING_REVIEW_REQUIRED,
            docs_override=policy.OVERRIDE_MODE_VERIFIED,
            override_reviewer="hongyi-chen",
            override_reason="Confirmed against source.",
            override_evidence="app/foo.rs@abc",
            override_head_sha="sha1",
        )
        review = {
            "user": {"login": "hongyi-chen"},
            "state": "APPROVED",
            "commit_id": "sha1",
            "body": (
                "Docs override: docs-verified\n"
                "Override reviewer: hongyi-chen\n"
                "Override reason: Confirmed against source.\n"
                "Override evidence: app/foo.rs@abc\n"
                "Override head SHA: sha1"
            ),
        }
        signals = cpc._compute_review_signals([review], [], "sha1", True, override)
        self.assertEqual(signals.approved_reviewers_current_head, ("hongyi-chen",))

    def test_unrecorded_override_approval_does_not_count(self):
        override = policy.DocumentationRisk(
            risk=policy.RISK_ENGINEERING_REVIEW_REQUIRED,
            docs_override=policy.OVERRIDE_MODE_VERIFIED,
            override_reviewer="hongyi-chen",
            override_reason="Confirmed against source.",
            override_evidence="app/foo.rs@abc",
            override_head_sha="sha1",
        )
        review = {
            "user": {"login": "hongyi-chen"},
            "state": "APPROVED",
            "commit_id": "sha1",
            "body": "Looks good.",
        }
        signals = cpc._compute_review_signals([review], [], "sha1", True, override)
        self.assertEqual(signals.approved_reviewers_current_head, ())


if __name__ == "__main__":
    unittest.main()
