#!/usr/bin/env python3
"""Unit tests for policy.py.

Stdlib unittest only, no third-party deps and no network.

Run:
    python3 .agents/skills/doc_quality_policy/test_policy.py
"""
from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_MODULE_PATH = _HERE / "policy.py"

_spec = importlib.util.spec_from_file_location("doc_quality_policy", _MODULE_PATH)
policy = importlib.util.module_from_spec(_spec)
# Registering in sys.modules before exec_module lets dataclasses (used with
# `from __future__ import annotations`) resolve field type annotations via
# `sys.modules[cls.__module__]`, which fails on an unregistered dynamic module.
sys.modules[_spec.name] = policy
_spec.loader.exec_module(policy)


class TestVerifyMarkers(unittest.TestCase):
    def test_finds_single_marker(self):
        text = "Run `warp --auto-approve` {/* VERIFY: flag name, unconfirmed against warp-internal */} to continue."
        self.assertEqual(
            policy.find_verify_markers(text),
            ["flag name, unconfirmed against warp-internal"],
        )

    def test_finds_multiple_markers_in_order(self):
        text = "{/* VERIFY: claim one */} text {/* VERIFY: claim two */}"
        self.assertEqual(policy.find_verify_markers(text), ["claim one", "claim two"])

    def test_no_markers_returns_empty(self):
        self.assertEqual(policy.find_verify_markers("Nothing to see here."), [])


class TestSectionExtraction(unittest.TestCase):
    def test_extracts_section_up_to_next_heading(self):
        body = "## Documentation risk\nRisk: low\nRationale: typo fix\n\n## Unverified claims\nNone\n"
        section = policy.extract_section(body, "## Documentation risk")
        self.assertEqual(section, "Risk: low\nRationale: typo fix")

    def test_missing_section_returns_none(self):
        self.assertIsNone(policy.extract_section("## Summary\nhello", "## Documentation risk"))

    def test_section_runs_to_end_of_body(self):
        body = "## Unverified claims\n- one\n- two"
        self.assertEqual(policy.extract_section(body, "## Unverified claims"), "- one\n- two")


class TestParseDocumentationRisk(unittest.TestCase):
    def test_parses_low_risk_block(self):
        body = (
            "## Documentation risk\n"
            "Risk: low\n"
            "Rationale: Spelling fixes only.\n"
            "Docs override: none\n"
        )
        parsed = policy.parse_documentation_risk_section(body)
        self.assertEqual(parsed.risk, policy.RISK_LOW)
        self.assertEqual(parsed.rationale, "Spelling fixes only.")
        self.assertEqual(parsed.docs_override, policy.OVERRIDE_MODE_NONE)

    def test_parses_list_fields(self):
        body = (
            "## Documentation risk\n"
            "Risk: engineering-review-required\n"
            "Rationale: New CLI flag.\n"
            "Source files consulted: app/src/cli/args.rs@abc, warp-server/pkg/foo.go@def\n"
            "Requested engineering reviewers: alice, bob\n"
        )
        parsed = policy.parse_documentation_risk_section(body)
        self.assertEqual(parsed.source_files_consulted, ["app/src/cli/args.rs@abc", "warp-server/pkg/foo.go@def"])
        self.assertEqual(parsed.requested_engineering_reviewers, ["alice", "bob"])

    def test_missing_section_returns_none(self):
        self.assertIsNone(policy.parse_documentation_risk_section("## Summary\nhello"))

    def test_parses_override_fields(self):
        body = (
            "## Documentation risk\n"
            "Risk: engineering-review-required\n"
            "Rationale: New CLI flag.\n"
            "Docs override: docs-verified\n"
            "Override reviewer: hongyi-chen\n"
            "Override reason: Confirmed against source.\n"
            "Override evidence: app/src/cli/args.rs@abc\n"
            "Override head SHA: deadbeef\n"
        )
        parsed = policy.parse_documentation_risk_section(body)
        self.assertEqual(parsed.docs_override, "docs-verified")
        self.assertEqual(parsed.override_reviewer, "hongyi-chen")
        self.assertEqual(parsed.override_head_sha, "deadbeef")


class TestParseUnverifiedClaims(unittest.TestCase):
    def test_none_sentinel_returns_empty_list(self):
        body = "## Unverified claims\nNone — all claims verified against source.\n"
        self.assertEqual(policy.parse_unverified_claims_section(body), [])

    def test_bullets_are_collected(self):
        body = "## Unverified claims\n- claim one\n- claim two\n"
        self.assertEqual(policy.parse_unverified_claims_section(body), ["claim one", "claim two"])

    def test_missing_section_returns_none(self):
        self.assertIsNone(policy.parse_unverified_claims_section("## Summary\nhello"))


# ---------------------------------------------------------------------------
# Risk allowlist — table-driven
# ---------------------------------------------------------------------------

class TestClassifyRisk(unittest.TestCase):
    def test_all_clear_is_low_risk(self):
        signals = policy.RiskSignals.all_clear()
        self.assertEqual(policy.classify_risk(signals), policy.RISK_LOW)

    def test_every_allowlist_trigger_forces_engineering_review(self):
        trigger_fields = [
            "adds_new_or_changed_feature_page",
            "changes_commands_or_code_examples",
            "changes_api_behavior",
            "changes_ui_labels_or_paths",
            "changes_defaults",
            "changes_permissions",
            "changes_availability_or_platform_support",
            "changes_plan_eligibility",
            "changes_billing_behavior",
            "changes_security_or_privacy_claims",
            "changes_data_handling",
            "changes_self_hosting_behavior",
            "changes_integration_setup",
        ]
        for field_name in trigger_fields:
            with self.subTest(trigger=field_name):
                signals = policy.RiskSignals.all_clear(**{field_name: True})
                self.assertEqual(
                    policy.classify_risk(signals),
                    policy.RISK_ENGINEERING_REVIEW_REQUIRED,
                    f"trigger {field_name} should force engineering-review-required",
                )

    def test_unresolved_verify_marker_forces_engineering_review(self):
        signals = policy.RiskSignals.all_clear(has_unresolved_verify_marker=True)
        self.assertEqual(policy.classify_risk(signals), policy.RISK_ENGINEERING_REVIEW_REQUIRED)

    def test_critical_or_important_finding_forces_engineering_review(self):
        signals = policy.RiskSignals.all_clear(has_critical_or_important_review_finding=True)
        self.assertEqual(policy.classify_risk(signals), policy.RISK_ENGINEERING_REVIEW_REQUIRED)

    def test_ambiguous_default_is_engineering_review_required(self):
        # An unconfigured RiskSignals() defaults every trigger to True, encoding
        # "ambiguous risk classification defaults to engineering-review-required".
        self.assertEqual(policy.classify_risk(policy.RiskSignals()), policy.RISK_ENGINEERING_REVIEW_REQUIRED)


# ---------------------------------------------------------------------------
# VERIFY accounting
# ---------------------------------------------------------------------------

class TestVerifyAccounting(unittest.TestCase):
    LOW_RISK_BODY = (
        "## Documentation risk\nRisk: low\nRationale: typo fix.\nDocs override: none\n\n"
        "## Unverified claims\nNone — all claims verified against source.\n"
    )
    ENG_REVIEW_BODY_TEMPLATE = (
        "## Documentation risk\nRisk: engineering-review-required\nRationale: new flag.\n"
        "Requested engineering reviewers: alice\nEngineering review status: pending\n"
        "Docs override: none\n\n## Unverified claims\n{claims}\n"
    )

    def test_unlisted_verify_marker_fails(self):
        problems = policy.validate_pr_contract(self.LOW_RISK_BODY, ["flag name unconfirmed"])
        self.assertTrue(any("not listed" in p for p in problems))

    def test_listed_marker_with_low_risk_fails(self):
        body = self.ENG_REVIEW_BODY_TEMPLATE.format(claims="- flag name unconfirmed")
        body = body.replace("Risk: engineering-review-required", "Risk: low")
        problems = policy.validate_pr_contract(body, ["flag name unconfirmed"])
        self.assertTrue(any("must be" in p for p in problems))

    def test_listed_marker_with_engineering_review_and_approval_passes(self):
        body = self.ENG_REVIEW_BODY_TEMPLATE.format(claims="- flag name unconfirmed")
        problems = policy.validate_pr_contract(
            body, ["flag name unconfirmed"], source_owner_approved_current_head=True,
        )
        self.assertEqual(problems, [])


# ---------------------------------------------------------------------------
# Override boundaries
# ---------------------------------------------------------------------------

class TestEngineeringGate(unittest.TestCase):
    def _risk(self, **kwargs):
        base = dict(risk=policy.RISK_ENGINEERING_REVIEW_REQUIRED, docs_override=policy.OVERRIDE_MODE_NONE)
        base.update(kwargs)
        return policy.DocumentationRisk(**base)

    def test_source_owner_approval_satisfies_gate(self):
        problems = policy.validate_engineering_gate(
            self._risk(),
            current_head_sha="sha1",
            authorized_docs_reviewers=(),
            deterministic_checks_passed=True,
            has_unresolved_critical_or_important_finding=False,
            source_owner_approved_current_head=True,
        )
        self.assertEqual(problems, [])

    def test_no_approval_and_no_override_fails(self):
        problems = policy.validate_engineering_gate(
            self._risk(),
            current_head_sha="sha1",
            authorized_docs_reviewers=(),
            deterministic_checks_passed=True,
            has_unresolved_critical_or_important_finding=False,
            source_owner_approved_current_head=False,
        )
        self.assertTrue(problems)

    def test_docs_verified_override_with_all_fields_passes(self):
        risk = self._risk(
            docs_override="docs-verified",
            override_reviewer="hongyi-chen",
            override_reason="Confirmed against source.",
            override_evidence="app/src/cli/args.rs@abc",
            override_head_sha="sha1",
        )
        problems = policy.validate_engineering_gate(
            risk,
            current_head_sha="sha1",
            authorized_docs_reviewers=["hongyi-chen"],
            deterministic_checks_passed=True,
            has_unresolved_critical_or_important_finding=False,
            source_owner_approved_current_head=False,
        )
        self.assertEqual(problems, [])

    def test_docs_waiver_override_with_all_fields_passes(self):
        risk = self._risk(
            docs_override="docs-waiver",
            override_reviewer="rachaelrenk",
            override_reason="No owner responded; risk is limited to wording.",
            override_evidence="n/a",
            override_head_sha="sha1",
        )
        problems = policy.validate_engineering_gate(
            risk,
            current_head_sha="sha1",
            authorized_docs_reviewers=["rachaelrenk"],
            deterministic_checks_passed=True,
            has_unresolved_critical_or_important_finding=False,
            source_owner_approved_current_head=False,
        )
        self.assertEqual(problems, [])

    def test_override_missing_field_fails(self):
        risk = self._risk(
            docs_override="docs-verified",
            override_reviewer="hongyi-chen",
            override_reason="Confirmed.",
            # override_evidence and override_head_sha missing
        )
        problems = policy.validate_engineering_gate(
            risk,
            current_head_sha="sha1",
            authorized_docs_reviewers=["hongyi-chen"],
            deterministic_checks_passed=True,
            has_unresolved_critical_or_important_finding=False,
            source_owner_approved_current_head=False,
        )
        self.assertTrue(any("missing required field" in p for p in problems))

    def test_override_by_unauthorized_reviewer_fails(self):
        risk = self._risk(
            docs_override="docs-verified",
            override_reviewer="random-person",
            override_reason="Confirmed.",
            override_evidence="app/src/cli/args.rs@abc",
            override_head_sha="sha1",
        )
        problems = policy.validate_engineering_gate(
            risk,
            current_head_sha="sha1",
            authorized_docs_reviewers=["hongyi-chen"],
            deterministic_checks_passed=True,
            has_unresolved_critical_or_important_finding=False,
            source_owner_approved_current_head=False,
        )
        self.assertTrue(any("not an authorized" in p for p in problems))

    def test_stale_override_head_sha_fails(self):
        risk = self._risk(
            docs_override="docs-verified",
            override_reviewer="hongyi-chen",
            override_reason="Confirmed.",
            override_evidence="app/src/cli/args.rs@abc",
            override_head_sha="old-sha",
        )
        problems = policy.validate_engineering_gate(
            risk,
            current_head_sha="new-sha",
            authorized_docs_reviewers=["hongyi-chen"],
            deterministic_checks_passed=True,
            has_unresolved_critical_or_important_finding=False,
            source_owner_approved_current_head=False,
        )
        self.assertTrue(any("does not match" in p for p in problems))

    def test_override_cannot_bypass_failing_deterministic_check(self):
        risk = self._risk(
            docs_override="docs-verified",
            override_reviewer="hongyi-chen",
            override_reason="Confirmed.",
            override_evidence="app/src/cli/args.rs@abc",
            override_head_sha="sha1",
        )
        problems = policy.validate_engineering_gate(
            risk,
            current_head_sha="sha1",
            authorized_docs_reviewers=["hongyi-chen"],
            deterministic_checks_passed=False,
            has_unresolved_critical_or_important_finding=False,
            source_owner_approved_current_head=False,
        )
        self.assertTrue(any("deterministic check" in p or "no override can bypass" in p for p in problems))

    def test_override_cannot_bypass_unresolved_finding(self):
        risk = self._risk(
            docs_override="docs-waiver",
            override_reviewer="hongyi-chen",
            override_reason="Confirmed.",
            override_evidence="n/a",
            override_head_sha="sha1",
        )
        problems = policy.validate_engineering_gate(
            risk,
            current_head_sha="sha1",
            authorized_docs_reviewers=["hongyi-chen"],
            deterministic_checks_passed=True,
            has_unresolved_critical_or_important_finding=True,
            source_owner_approved_current_head=False,
        )
        self.assertTrue(any("critical/important" in p for p in problems))

    def test_source_owner_approval_does_not_bypass_failing_check(self):
        problems = policy.validate_engineering_gate(
            self._risk(),
            current_head_sha="sha1",
            authorized_docs_reviewers=(),
            deterministic_checks_passed=False,
            has_unresolved_critical_or_important_finding=False,
            source_owner_approved_current_head=True,
        )
        self.assertTrue(problems)

    def test_new_head_invalidates_engineer_approval_semantics(self):
        # source_owner_approved_current_head is caller-supplied and must be
        # keyed to the *current* head; simulate a stale approval by passing
        # False (the caller's job is to only pass True for the current head).
        problems = policy.validate_engineering_gate(
            self._risk(),
            current_head_sha="new-sha",
            authorized_docs_reviewers=(),
            deterministic_checks_passed=True,
            has_unresolved_critical_or_important_finding=False,
            source_owner_approved_current_head=False,
        )
        self.assertTrue(problems)

    def test_empty_authorized_list_fails_closed_instead_of_skipping_the_check(self):
        # A PR-controlled or unavailable allowlist lookup must never be read
        # as "anyone may author an override" -- regression for a bypass where
        # an empty list silently skipped the authorization check.
        risk = self._risk(
            docs_override="docs-verified",
            override_reviewer="random-person",
            override_reason="Confirmed.",
            override_evidence="app/src/cli/args.rs@abc",
            override_head_sha="sha1",
        )
        problems = policy.validate_engineering_gate(
            risk,
            current_head_sha="sha1",
            authorized_docs_reviewers=(),
            deterministic_checks_passed=True,
            has_unresolved_critical_or_important_finding=False,
            source_owner_approved_current_head=False,
        )
        self.assertTrue(any("not an authorized" in p for p in problems))

    def test_override_with_no_current_head_sha_fails_closed(self):
        # Regression for a bypass where omitting current_head_sha entirely
        # skipped the staleness check rather than failing it.
        risk = self._risk(
            docs_override="docs-verified",
            override_reviewer="hongyi-chen",
            override_reason="Confirmed.",
            override_evidence="app/src/cli/args.rs@abc",
            override_head_sha="sha1",
        )
        problems = policy.validate_engineering_gate(
            risk,
            current_head_sha=None,
            authorized_docs_reviewers=["hongyi-chen"],
            deterministic_checks_passed=True,
            has_unresolved_critical_or_important_finding=False,
            source_owner_approved_current_head=False,
        )
        self.assertTrue(any("no current head SHA" in p for p in problems))


class TestFullContractValidation(unittest.TestCase):
    def test_missing_documentation_risk_section(self):
        problems = policy.validate_pr_contract("## Summary\nhello", [])
        self.assertEqual(len(problems), 1)
        self.assertIn("Documentation risk", problems[0])

    def test_low_risk_clean_pr_passes(self):
        body = (
            "## Documentation risk\nRisk: low\nRationale: typo fix.\nDocs override: none\n\n"
            "## Unverified claims\nNone — all claims verified against source.\n"
        )
        self.assertEqual(policy.validate_pr_contract(body, []), [])

    def test_invalid_risk_level_reported(self):
        body = (
            "## Documentation risk\nRisk: medium\nRationale: x.\nDocs override: none\n\n"
            "## Unverified claims\nNone\n"
        )
        problems = policy.validate_pr_contract(body, [])
        self.assertTrue(any("invalid risk level" in p for p in problems))


if __name__ == "__main__":
    unittest.main()
