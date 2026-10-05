#!/usr/bin/env python3
"""Regression tests for audit_consistency.py."""

from __future__ import annotations

import copy
import datetime as dt
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("audit_consistency.py")
SPEC = importlib.util.spec_from_file_location("audit_consistency", SCRIPT)
assert SPEC and SPEC.loader
audit = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(audit)


RULES = {
    "version": 1,
    "inventory": {
        "excluded_globs": ["changelog/**"],
        "excluded_paths": ["404.mdx"],
    },
    "default_precedence": ["authority", "docs-prose", "faq"],
    "categories": {
        "api": {"precedence": ["released-openapi", "docs-prose"]},
        "plan-gating": {"precedence": ["effective-billing-policy", "docs-prose"]},
    },
}


def claim(
    *,
    path: str = "page.mdx",
    heading: str = "Limits",
    topic: str = "plan-gating",
    entity: str = "codebase-context",
    predicate: str = "files-per-repo",
    value=5000,
    value_type: str = "integer",
    qualifiers=None,
    quote: str = "All plans support 5,000 files.",
    source_class: str = "docs-prose",
    line_start: int = 1,
    line_end: int = 1,
    polarity: str = "affirmative",
):
    return {
        "source": {
            "repository": "warpdotdev/docs",
            "path": path,
            "route": "/" + path,
            "heading": heading,
            "heading_anchor": audit.stable_heading_anchor(heading),
            "line_start": line_start,
            "line_end": line_end,
        },
        "category": topic,
        "topic": topic,
        "entity": entity,
        "predicate": predicate,
        "value": {"type": value_type, "normalized": value},
        "qualifiers": qualifiers or {},
        "polarity": polarity,
        "quote": quote,
        "source_class": source_class,
    }


def finding(*claims, severity="medium", confidence="high", rationale_class="typed"):
    return audit.normalize_finding({
        "title": "Conflicting limit",
        "category": "plan-gating",
        "severity": severity,
        "confidence": confidence,
        "topic": "plan-gating",
        "entity": "codebase-context",
        "predicate": "files-per-repo",
        "claims": list(claims),
        "verdict": "contradiction",
        "rationale_class": rationale_class,
        "canonical_source": "effective-billing-policy",
        "suggested_resolution_class": "align-prose",
    })


class InventoryTests(unittest.TestCase):
    def test_inventory_excludes_history_and_redirect_paths(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "changelog").mkdir()
            (root / "changelog/2026.mdx").write_text("# 2026\nA plan supports 10 files.\n")
            (root / "404.mdx").write_text("# Missing\n")
            (root / "guide.mdx").write_text(
                "---\ntitle: Guide\n---\n# Guide\n## Limits\nBuild supports 10 files.\n"
            )
            inventory = audit.inventory_pages(root, RULES)
            self.assertEqual(set(inventory["pages"]), {"guide.mdx"})
            self.assertEqual(inventory["pages"]["guide.mdx"]["route"], "/guide/")
            self.assertEqual(inventory["counts"]["candidate_sections"], 1)

    def test_inventory_reuses_unchanged_page_and_full_invalidates_it(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "guide.mdx").write_text("# Guide\nBuild supports 10 files.\n")
            first = audit.inventory_pages(root, RULES)
            previous = {
                "extractor_version": audit.EXTRACTOR_VERSION,
                "model_contract_version": audit.MODEL_CONTRACT_VERSION,
                "pages": first["pages"],
            }
            second = audit.inventory_pages(root, RULES, previous)
            full = audit.inventory_pages(root, RULES, previous, full=True)
            self.assertEqual(second["changed_pages"], [])
            self.assertEqual(second["pages"]["guide.mdx"]["extraction_status"], "unchanged")
            self.assertEqual(full["pages"]["guide.mdx"]["extraction_status"], "invalidated")

    def test_inventory_includes_factual_page_introduction_before_first_heading(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "guide.mdx").write_text(
                "---\ntitle: Guide\n---\n"
                "Build supports 10 files.\n\n"
                "## Details\nNo limits are listed here.\n"
            )
            inventory = audit.inventory_pages(root, RULES)
            sections = inventory["pages"]["guide.mdx"]["candidate_sections"]
            self.assertEqual(sections[0]["heading"], "")
            self.assertEqual(sections[0]["line_start"], 4)


class EvidenceAndNormalizationTests(unittest.TestCase):
    def test_exact_quote_validation_accepts_exact_substring(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "page.mdx").write_text("First line\nExact quote here.\n")
            value = claim(
                quote="Exact quote",
                line_start=2,
                line_end=2,
            )
            audit.validate_claim_quote(value, {"warpdotdev/docs": root})

    def test_exact_quote_validation_rejects_unsupported_quote(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "page.mdx").write_text("First line\nExact quote here.\n")
            value = claim(
                quote="Paraphrased quote",
                line_start=2,
                line_end=2,
            )
            with self.assertRaises(audit.AuditError):
                audit.validate_claim_quote(value, {"warpdotdev/docs": root})

    def test_typed_normalization_converts_units_paths_and_plans(self):
        self.assertEqual(
            audit.normalize_typed_value({"type": "bytes", "normalized": "2 GB"})["normalized"],
            2_000_000_000,
        )
        self.assertEqual(
            audit.normalize_typed_value({"type": "duration", "normalized": "2 hours"})["normalized"],
            7200,
        )
        self.assertEqual(
            audit.normalize_typed_value({"type": "path", "normalized": "/runs/:run_id"})["normalized"],
            "/runs/{}",
        )
        self.assertEqual(
            audit.normalize_typed_value({"type": "plan", "normalized": "build max"})["normalized"],
            "MAX",
        )


class QualifierAndBlockingTests(unittest.TestCase):
    def test_disjoint_specific_qualifiers_are_not_compatible(self):
        compatible, conflicts, _ = audit.qualifier_compatibility(
            {"plans": ["free"]},
            {"plans": ["build"]},
        )
        self.assertFalse(compatible)
        self.assertEqual(conflicts, ["plans"])

    def test_universal_claim_is_compatible_with_specific_counterexample(self):
        compatible, conflicts, universal_specific = audit.qualifier_compatibility(
            {"plans": ["all"]},
            {"plans": ["free"]},
        )
        self.assertTrue(compatible)
        self.assertEqual(conflicts, [])
        self.assertTrue(universal_specific)

    def test_explicit_universal_exception_excludes_matching_specific_scope(self):
        compatible, conflicts, universal_specific = audit.qualifier_compatibility(
            {"actors": ["all"], "exceptions": ["api-key-runs"]},
            {"actors": ["api-key"]},
        )
        self.assertFalse(compatible)
        self.assertEqual(conflicts, ["explicit-exception"])
        self.assertTrue(universal_specific)

    def test_operating_system_install_method_and_version_controls(self):
        for key, left, right in (
            ("operating_systems", "macos", "windows"),
            ("install_methods", "direct", "homebrew"),
            ("versions", "<1.2", ">=1.2"),
        ):
            compatible, conflicts, _ = audit.qualifier_compatibility(
                {key: [left]},
                {key: [right]},
            )
            self.assertFalse(compatible)
            self.assertEqual(conflicts, [key])

    def test_candidate_blocking_never_compares_unrelated_predicates(self):
        left = claim(value=5000)
        right = claim(path="other.mdx", predicate="indices", value=3)
        self.assertEqual(audit.generate_candidates([left, right], RULES), [])

    def test_authority_centered_star_avoids_peer_quadratic_pairs(self):
        authority = claim(
            path="policy.yaml",
            value=3000,
            source_class="effective-billing-policy",
        )
        peers = [
            claim(path=f"page-{index}.mdx", value=5000 + index)
            for index in range(5)
        ]
        candidates = audit.generate_candidates([authority, *peers], RULES)
        self.assertEqual(len(candidates), 5)
        self.assertTrue(all(item["left"]["source_class"] == "effective-billing-policy" for item in candidates))

    def test_authority_selection_uses_category_registry(self):
        prose = claim(
            topic="api",
            entity="create-run",
            predicate="path",
            value="/agent/runs",
            value_type="path",
        )
        authority = claim(
            path="openapi.yaml",
            topic="api",
            entity="create-run",
            predicate="path",
            value="/agent/run",
            value_type="path",
            source_class="released-openapi",
        )
        candidate = audit.generate_candidates([prose, authority], RULES)[0]
        self.assertEqual(candidate["left"]["source_class"], "released-openapi")

    def test_free_text_differences_require_semantic_review(self):
        left = claim(value="available to teams", value_type="free-text")
        right = claim(
            path="other.mdx",
            value="available to individual users",
            value_type="free-text",
        )
        candidate = audit.generate_candidates([left, right], RULES)[0]
        self.assertFalse(candidate["exact_typed_mismatch"])


class FingerprintAndLifecycleTests(unittest.TestCase):
    def setUp(self):
        self.left = claim()
        self.right = claim(path="policy.yaml", value=3000, source_class="effective-billing-policy")
        self.finding = finding(self.left, self.right)

    def test_claim_identity_ignores_line_and_quote_changes(self):
        changed = copy.deepcopy(self.left)
        changed["source"]["line_start"] = 40
        changed["source"]["line_end"] = 42
        changed["quote"] = "Every plan supports at least 5,000 files."
        before = audit.normalize_claim(self.left)
        after = audit.normalize_claim(changed)
        self.assertEqual(before["claim_id"], after["claim_id"])
        self.assertNotEqual(
            before["claim_content_fingerprint"],
            after["claim_content_fingerprint"],
        )

    def test_finding_identity_is_stable_across_content_change(self):
        changed_left = copy.deepcopy(self.left)
        changed_left["quote"] = "Every plan supports at least 5,000 files."
        changed = finding(changed_left, self.right)
        self.assertEqual(self.finding["finding_id"], changed["finding_id"])
        self.assertNotEqual(
            self.finding["finding_content_fingerprint"],
            changed["finding_content_fingerprint"],
        )

    def test_all_lifecycle_transitions(self):
        new = audit.calculate_lifecycle([self.finding], {"findings": {}}, "run-1", True)
        current = next(iter(new["findings"].values()))
        self.assertEqual(current["lifecycle"], "new")

        existing = audit.calculate_lifecycle(
            [self.finding],
            {"findings": new["findings"]},
            "run-2",
            True,
        )
        self.assertEqual(next(iter(existing["findings"].values()))["lifecycle"], "existing")

        changed_finding = copy.deepcopy(self.finding)
        changed_finding["severity"] = "high"
        changed_finding = audit.normalize_finding(changed_finding)
        changed = audit.calculate_lifecycle(
            [changed_finding],
            {"findings": new["findings"]},
            "run-3",
            True,
        )
        self.assertEqual(next(iter(changed["findings"].values()))["lifecycle"], "changed")

        resolved = audit.calculate_lifecycle(
            [],
            {"findings": new["findings"]},
            "run-4",
            True,
        )
        tombstone = next(iter(resolved["findings"].values()))
        self.assertEqual(tombstone["lifecycle"], "resolved")
        self.assertEqual(tombstone["status"], "resolved")

        reopened = audit.calculate_lifecycle(
            [self.finding],
            {"findings": resolved["findings"]},
            "run-5",
            True,
        )
        reopened_finding = next(iter(reopened["findings"].values()))
        self.assertEqual(reopened_finding["lifecycle"], "changed")
        self.assertTrue(reopened_finding["reopened"])

    def test_incomplete_run_never_resolves_prior_finding(self):
        prior = audit.calculate_lifecycle([self.finding], {"findings": {}}, "run-1", True)
        partial = audit.calculate_lifecycle(
            [],
            {"findings": prior["findings"]},
            "run-2",
            False,
        )
        carried = next(iter(partial["findings"].values()))
        self.assertEqual(carried["status"], "active")
        self.assertEqual(carried["lifecycle"], "existing")
        self.assertTrue(carried["carried_forward_due_to_incomplete_run"])


class PipelinePrepassTests(unittest.TestCase):
    def test_prepass_writes_semantic_candidates_without_state(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "page.mdx").write_text(
                "Available to teams.\nAvailable to individual users.\n"
            )
            claims_path = root / "claims.json"
            claims_path.write_text(json.dumps({
                "claims": [
                    claim(
                        quote="Available to teams.",
                        value="available to teams",
                        value_type="free-text",
                    ),
                    claim(
                        quote="Available to individual users.",
                        value="available to individual users",
                        value_type="free-text",
                        line_start=2,
                        line_end=2,
                    ),
                ]
            }))
            args = type("Args", (), {
                "run_id": "prepass",
                "claims": str(claims_path),
                "repository_root": [f"warpdotdev/docs={root}"],
                "state_dir": str(root / "state"),
                "inventory": None,
                "authority_rules": str(audit.DEFAULT_AUTHORITY_RULES),
                "suppressions": str(audit.DEFAULT_SUPPRESSIONS),
                "candidate_output": str(root / "candidates.json"),
                "source_commit": "abc123",
                "coverage": "complete",
                "source_availability": None,
                "model_calls": 0,
                "pages": 1,
                "characters": 52,
                "artifact_json": str(root / "artifact.json"),
                "artifact_markdown": str(root / "artifact.md"),
                "no_state_write": True,
                "model_identifier": "test-model",
            })
            audit.run_pipeline(args)
            candidates = json.loads((root / "candidates.json").read_text())
            artifact = json.loads((root / "artifact.json").read_text())
            self.assertEqual(candidates["summary"]["semantic_review_required"], 1)
            self.assertEqual(candidates["summary"]["exact_typed_mismatches"], 0)
            self.assertEqual(artifact["summary"]["active"], 0)
            self.assertFalse((root / "state").exists())


class SuppressionTests(unittest.TestCase):
    def setUp(self):
        self.finding = finding(
            claim(),
            claim(path="policy.yaml", value=3000, source_class="effective-billing-policy"),
        )

    def test_unexpired_suppression_removes_candidate(self):
        suppressions = {
            "suppressions": [{
                "id": "known",
                "finding_id": self.finding["finding_id"],
                "owner": "docs",
                "reason": "Intentional exception",
                "created": "2026-01-01",
                "expires": "2027-01-01",
            }]
        }
        active, suppressed, expired = audit.apply_suppressions(
            [self.finding], suppressions, dt.date(2026, 10, 5)
        )
        self.assertEqual(active, [])
        self.assertEqual(len(suppressed), 1)
        self.assertEqual(expired, [])

    def test_expired_suppression_returns_candidate_for_review(self):
        suppressions = {
            "suppressions": [{
                "id": "expired",
                "finding_id": self.finding["finding_id"],
                "owner": "docs",
                "reason": "Migration window",
                "created": "2025-01-01",
                "expires": "2026-01-01",
            }]
        }
        active, suppressed, expired = audit.apply_suppressions(
            [self.finding], suppressions, dt.date(2026, 10, 5)
        )
        self.assertEqual(len(active), 1)
        self.assertEqual(suppressed, [])
        self.assertEqual(len(expired), 1)


class AuthorityAdapterTests(unittest.TestCase):
    def test_tier_inheritance_merges_feature_policies(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "free.yaml").write_text(
                "id: FREE\npolicies:\n"
                "  - feature_type: CODEBASE_CONTEXT\n"
                "    feature_policy:\n"
                "      max_indices: \"3\"\n"
                "      max_files_per_repo: \"5000\"\n"
            )
            (root / "build.yaml").write_text(
                "id: BUILD\nextends: free.yaml\npolicies:\n"
                "  - feature_type: CODEBASE_CONTEXT\n"
                "    feature_policy:\n"
                "      max_files_per_repo: \"100000\"\n"
            )
            effective = audit.effective_tier(root / "build.yaml", {})
            policy = effective["policies"]["CODEBASE_CONTEXT"]
            self.assertEqual(policy["max_indices"], 3)
            self.assertEqual(policy["max_files_per_repo"], 100000)


class GuardTests(unittest.TestCase):
    def test_schedule_guard_accepts_daylight_and_standard_windows(self):
        daylight = type("Args", (), {"at": "2026-07-06T17:00:00Z"})
        standard = type("Args", (), {"at": "2026-12-07T18:00:00Z"})
        self.assertEqual(audit.schedule_guard_command(daylight), 0)
        self.assertEqual(audit.schedule_guard_command(standard), 0)

    def test_schedule_guard_rejects_inactive_paired_schedule(self):
        inactive = type("Args", (), {"at": "2026-07-06T18:00:00Z"})
        self.assertEqual(audit.schedule_guard_command(inactive), 10)


class NotificationTests(unittest.TestCase):
    def render(self, artifact):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            artifact_path = root / "artifact.json"
            output_path = root / "notification.json"
            artifact_path.write_text(json.dumps(artifact))
            args = type("Args", (), {
                "artifact": str(artifact_path),
                "output": str(output_path),
                "run_url": "https://example.test/run",
                "state_pr_url": "https://example.test/pr",
            })
            audit.notification_command(args)
            return json.loads(output_path.read_text())

    def test_high_confidence_change_produces_one_payload(self):
        result = self.render({
            "run_id": "run-1",
            "coverage": "complete",
            "summary": {"new": 1, "changed": 0, "resolved": 0, "active": 1},
            "lifecycle_changes": [{
                "finding_id": "sha256:" + "a" * 64,
                "title": "Conflicting limit",
                "severity": "high",
                "confidence": "high",
            }],
        })
        self.assertTrue(result["should_post"])
        self.assertEqual(len(result["actionable_finding_ids"]), 1)
        self.assertEqual(result["message"].count("Docs consistency audit"), 1)

    def test_unchanged_run_has_no_payload(self):
        result = self.render({
            "run_id": "run-2",
            "coverage": "complete",
            "summary": {"new": 0, "changed": 0, "resolved": 0, "active": 1},
            "lifecycle_changes": [],
        })
        self.assertFalse(result["should_post"])
        self.assertIsNone(result["message"])

    def test_blocked_run_produces_payload_without_findings(self):
        result = self.render({
            "run_id": "run-3",
            "coverage": "blocked",
            "summary": {},
            "lifecycle_changes": [],
        })
        self.assertTrue(result["should_post"])
        self.assertEqual(result["reason"], "blocked")


if __name__ == "__main__":
    unittest.main(verbosity=2)
