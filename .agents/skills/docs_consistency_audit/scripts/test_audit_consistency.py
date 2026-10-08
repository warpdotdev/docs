#!/usr/bin/env python3
"""Regression tests for audit_consistency.py."""

from __future__ import annotations

import copy
import concurrent.futures
import datetime as dt
import importlib.util
import json
import shutil
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


def write_claim_page(
    root: Path,
    path: str,
    quote: str,
    *,
    route: str | None = None,
    line: int = 1,
    **kwargs,
):
    target = root / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("\n" * (line - 1) + quote + "\n")
    value = claim(
        path=path,
        quote=quote,
        line_start=line,
        line_end=line,
        **kwargs,
    )
    value["source"]["route"] = route or "/" + path.removesuffix(".mdx")
    value["source"]["content_sha256"] = audit.sha256_text(target.read_text())
    return value


def run_args(
    root: Path,
    claims_path: Path,
    *,
    state_dir: Path | None = None,
    inventory: Path | None = None,
    authorities: Path | None = None,
    no_state_write: bool = False,
    output_root: Path | None = None,
):
    output_root = output_root or root
    return type("Args", (), {
        "run_id": "test-run",
        "claims": str(claims_path),
        "repository_root": [f"warpdotdev/docs={root}"],
        "state_dir": str(state_dir or root / "state"),
        "inventory": str(inventory) if inventory else None,
        "authority_rules": str(audit.DEFAULT_AUTHORITY_RULES),
        "authorities": str(authorities) if authorities else None,
        "redirects": None,
        "suppressions": str(audit.DEFAULT_SUPPRESSIONS),
        "candidate_output": str(output_root / "candidates.json"),
        "source_commit": "abc123",
        "coverage": "complete",
        "source_availability": None,
        "model_calls": 0,
        "pages": 1,
        "characters": 100,
        "artifact_json": str(output_root / "artifact.json"),
        "artifact_markdown": str(output_root / "artifact.md"),
        "no_state_write": no_state_write,
        "model_identifier": "test-model",
    })


def verification_for(
    candidate,
    claims,
    *,
    verdict="contradiction",
    confidence="high",
    qualifier_status="complete",
    context_complete=True,
    extra_scope_quotes=None,
):
    return {
        "candidate_id": candidate["candidate_id"],
        "title": "Conflicting limit",
        "severity": "high",
        "confidence": confidence,
        "verdict": verdict,
        "rationale": "The verified public claims disagree.",
        "rationale_class": "verified-context",
        "canonical_source": "canonical-doc",
        "authority_reason": "Public canonical documentation owns this claim.",
        "suggested_resolution": "Align the non-canonical public explanation.",
        "suggested_resolution_class": "align-prose",
        "claim_ids": sorted(item["claim_id"] for item in claims),
        "scope_quotes": [
            {"source": item["source"], "quote": item["quote"]}
            for item in claims
        ] + list(extra_scope_quotes or []),
        "qualifier_status": qualifier_status,
        "context_complete": context_complete,
    }


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


class ContextVerificationTests(unittest.TestCase):
    def test_missing_qualifier_evidence_downgrades_exact_mismatch(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            left = write_claim_page(root, "left.mdx", "Limit is 5,000.", value=5000)
            right = write_claim_page(root, "right.mdx", "Limit is 3,000.", value=3000)
            normalized = [audit.normalize_claim(item) for item in (left, right)]
            candidate = audit.generate_candidates(normalized, RULES)[0]
            result = audit.verified_finding_from_candidate(
                candidate,
                verification_for(
                    candidate,
                    normalized,
                    qualifier_status="unknown",
                ),
                {"warpdotdev/docs": root},
                "run-1",
                "abc123",
            )
            self.assertIsNotNone(result)
            self.assertEqual(result["confidence"], "medium")

    def test_adjacent_exception_context_suppresses_exact_mismatch(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            left = write_claim_page(
                root,
                "left.mdx",
                "All runs accept five images.",
                value=5,
            )
            right_path = root / "right.mdx"
            right_path.write_text(
                "API-key runs are the exception.\n"
                "API-key runs accept one image.\n"
            )
            right = claim(
                path="right.mdx",
                quote="API-key runs accept one image.",
                value=1,
                line_start=2,
                line_end=2,
            )
            right["source"]["content_sha256"] = audit.sha256_text(
                right_path.read_text()
            )
            normalized = [audit.normalize_claim(item) for item in (left, right)]
            candidate = audit.generate_candidates(normalized, RULES)[0]
            adjacent = {
                "source": {
                    **right["source"],
                    "line_start": 1,
                    "line_end": 1,
                },
                "quote": "API-key runs are the exception.",
            }
            result = audit.verified_finding_from_candidate(
                candidate,
                verification_for(
                    candidate,
                    normalized,
                    verdict="intentional-exception",
                    extra_scope_quotes=[adjacent],
                ),
                {"warpdotdev/docs": root},
                "run-1",
                "abc123",
            )
            self.assertIsNone(result)

    def test_incomplete_context_suppresses_exact_mismatch(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            left = write_claim_page(root, "left.mdx", "Limit is 5,000.", value=5000)
            right = write_claim_page(root, "right.mdx", "Limit is 3,000.", value=3000)
            normalized = [audit.normalize_claim(item) for item in (left, right)]
            candidate = audit.generate_candidates(normalized, RULES)[0]
            result = audit.verified_finding_from_candidate(
                candidate,
                verification_for(
                    candidate,
                    normalized,
                    context_complete=False,
                ),
                {"warpdotdev/docs": root},
                "run-1",
                "abc123",
            )
            self.assertIsNone(result)


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

    def test_verified_redirect_preserves_claim_identity_and_provenance(self):
        old = claim(path="old.mdx")
        old["source"]["route"] = "/old"
        new = claim(path="new.mdx")
        new["source"]["route"] = "/new"
        redirects = {"/old": "/new"}
        old_normalized = audit.normalize_claim(
            audit.apply_redirect_identity(old, redirects)
        )
        new_normalized = audit.normalize_claim(
            audit.apply_redirect_identity(new, redirects)
        )
        self.assertEqual(old_normalized["claim_id"], new_normalized["claim_id"])
        self.assertEqual(old_normalized["source"]["path"], "old.mdx")
        self.assertEqual(new_normalized["source"]["path"], "new.mdx")

    def test_move_without_verified_redirect_changes_claim_identity(self):
        old = audit.normalize_claim(
            audit.apply_redirect_identity(claim(path="old.mdx"), {})
        )
        new = audit.normalize_claim(
            audit.apply_redirect_identity(claim(path="new.mdx"), {})
        )
        self.assertNotEqual(old["claim_id"], new["claim_id"])

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
                "authorities": None,
                "redirects": None,
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
            self.assertEqual(artifact["coverage"], "partial")
            self.assertEqual(len(artifact["unverified_candidate_ids"]), 1)
            self.assertFalse((root / "state").exists())


class StateDurabilityTests(unittest.TestCase):
    def inventory_document(self, root, previous=None, max_pages=0):
        inventory = audit.inventory_pages(root, RULES, previous)
        changed = inventory["changed_pages"]
        selected = changed[:max_pages] if max_pages else changed
        backlog = changed[len(selected):]
        inventory["extraction_plan"] = {
            "selected_pages": selected,
            "backlog_pages": backlog,
            "selected_characters": sum(
                inventory["pages"][page]["character_count"]
                for page in selected
            ),
            "coverage": "partial" if backlog else "complete",
            "max_pages": max_pages,
            "max_characters": 0,
        }
        return inventory

    def run_inventory(self, docs_root, work_root, state, inventory, claims):
        inventory_path = work_root / "inventory.json"
        inventory_path.write_text(json.dumps(inventory))
        claims_path = work_root / "claims.json"
        claims_path.write_text(json.dumps({
            "claims": claims,
            "processed_pages": inventory["extraction_plan"]["selected_pages"],
        }))
        args = run_args(
            docs_root,
            claims_path,
            state_dir=state,
            inventory=inventory_path,
            output_root=work_root,
        )
        audit.run_pipeline(args)

    def test_deferred_shard_and_hash_survive_then_resume(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            docs_root = root / "docs"
            state = root / "state"
            original = [
                write_claim_page(
                    docs_root,
                    "a.mdx",
                    "A supports 10 files.",
                    entity="a",
                    value=10,
                ),
                write_claim_page(
                    docs_root,
                    "b.mdx",
                    "B supports 20 files.",
                    entity="b",
                    value=20,
                ),
            ]
            initial = self.inventory_document(docs_root)
            self.run_inventory(docs_root, root, state, initial, original)
            first_manifest = json.loads((state / "manifest.json").read_text())
            old_b_hash = first_manifest["pages"]["b.mdx"]["source_sha256"]
            old_b_shard = first_manifest["page_shards"]["b.mdx"]
            claim_args = type("Args", (), {
                "state_dir": str(state),
                "event_id": "scheduled-run",
                "at": "2026-07-06T17:00:00Z",
            })
            self.assertEqual(audit.schedule_claim_command(claim_args), 0)
            receipt_path = state / "schedule_claims/2026-07-06.json"
            receipt = receipt_path.read_text()

            changed_a = write_claim_page(
                docs_root,
                "a.mdx",
                "A supports 11 files.",
                entity="a",
                value=11,
            )
            write_claim_page(
                docs_root,
                "b.mdx",
                "B supports 21 files.",
                entity="b",
                value=21,
            )
            deferred = self.inventory_document(
                docs_root,
                first_manifest,
                max_pages=1,
            )
            self.run_inventory(
                docs_root,
                root,
                state,
                deferred,
                [changed_a],
            )
            deferred_manifest = json.loads((state / "manifest.json").read_text())
            self.assertEqual(
                deferred_manifest["pages"]["b.mdx"]["source_sha256"],
                old_b_hash,
            )
            self.assertEqual(
                deferred_manifest["page_shards"]["b.mdx"],
                old_b_shard,
            )
            self.assertEqual(deferred_manifest["backlog_pages"], ["b.mdx"])
            self.assertIn(
                "B supports 20 files.",
                (state / old_b_shard).read_text(),
            )
            self.assertEqual(receipt_path.read_text(), receipt)

            changed_b = write_claim_page(
                docs_root,
                "b.mdx",
                "B supports 21 files.",
                entity="b",
                value=21,
            )
            resumed = self.inventory_document(docs_root, deferred_manifest)
            self.assertEqual(
                resumed["extraction_plan"]["selected_pages"],
                ["b.mdx"],
            )
            self.run_inventory(
                docs_root,
                root,
                state,
                resumed,
                [changed_b],
            )
            final_manifest = json.loads((state / "manifest.json").read_text())
            self.assertEqual(final_manifest["backlog_pages"], [])
            self.assertEqual(
                final_manifest["pages"]["b.mdx"]["source_sha256"],
                audit.sha256_text((docs_root / "b.mdx").read_text()),
            )
            self.assertIn(
                "B supports 21 files.",
                (state / final_manifest["page_shards"]["b.mdx"]).read_text(),
            )
            self.assertEqual(receipt_path.read_text(), receipt)

    def test_state_replacement_failure_restores_prior_tree(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            state = root / "state"
            replacement = root / "replacement"
            state.mkdir()
            replacement.mkdir()
            (state / "marker").write_text("old")
            (replacement / "marker").write_text("new")
            calls = 0

            def fail_install(source, destination):
                nonlocal calls
                calls += 1
                if calls == 2:
                    raise OSError("injected replacement failure")
                source = Path(source)
                source.rename(destination)

            with self.assertRaises(OSError):
                audit.replace_state_tree(
                    state,
                    replacement,
                    replace_operation=fail_install,
                )
            self.assertEqual((state / "marker").read_text(), "old")
            self.assertFalse(state.with_name("state.previous").exists())


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

    def test_private_authority_contract_is_consumed_without_public_leak(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            left = write_claim_page(
                root,
                "left.mdx",
                "All plans support 5,000 files.",
                value=5000,
            )
            right = write_claim_page(
                root,
                "right.mdx",
                "Free supports 3,000 files.",
                value=3000,
            )
            normalized = [audit.normalize_claim(item) for item in (left, right)]
            candidate = audit.generate_candidates(normalized, RULES)[0]
            authority = audit.authority_record(
                topic="plan-gating",
                entity="codebase-context",
                predicate="files-per-repo",
                value={"type": "integer", "normalized": 3000},
                qualifiers={"plans": ["free"]},
                source_class="effective-billing-policy",
                visibility="private",
                release_scope="effective-self-serve",
                repository="warpdotdev/warp-server",
                path="billing/config/tiers/free.yaml",
                source_commit="private-sha",
                evidence_hash="private-hash",
            )
            authorities_path = root / "authorities.json"
            authorities_path.write_text(json.dumps({
                "authority_records": [authority]
            }))
            claims_path = root / "claims.json"
            claims_path.write_text(json.dumps({
                "claims": [left, right],
                "adjudicated_findings": [
                    verification_for(candidate, normalized)
                ],
            }))
            args = run_args(
                root,
                claims_path,
                authorities=authorities_path,
            )
            audit.run_pipeline(args)
            artifact_text = (root / "artifact.json").read_text()
            candidate_text = (root / "candidates.json").read_text()
            state_text = "\n".join(
                path.read_text()
                for path in (root / "state").rglob("*.json")
            )
            for text in (artifact_text, candidate_text, state_text):
                self.assertNotIn("warp-server", text)
                self.assertNotIn("billing/config", text)
                self.assertNotIn("private-hash", text)
                self.assertNotIn("private-sha", text)
                self.assertNotIn(authority["authority_id"], text)
            artifact = json.loads(artifact_text)
            self.assertEqual(artifact["summary"]["active"], 1)
            self.assertEqual(
                artifact["authority_summary"]["private_transient"],
                1,
            )

    def test_private_claim_cannot_enter_generated_state(self):
        private = claim()
        private["source"]["repository"] = "warpdotdev/warp-server"
        private["source"]["visibility"] = "public"
        with self.assertRaises(audit.AuditError):
            audit.validate_public_claim(private)


class BenchmarkProductionPathTests(unittest.TestCase):
    def run_mutated_benchmark(self, mutate, *, update_fixture_pin=True):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            benchmark = json.loads(audit.DEFAULT_BENCHMARK.read_text())
            shutil.copytree(
                audit.REFERENCES_DIR / "benchmark_fixtures",
                root / "benchmark_fixtures",
            )
            case = benchmark["cases"][0]
            fixture_path = root / case["fixture"]
            extraction = json.loads(fixture_path.read_text())
            mutate(case, extraction, fixture_path)
            fixture_path.write_text(
                json.dumps(extraction, indent=2, sort_keys=True) + "\n"
            )
            if update_fixture_pin:
                case["fixture_sha256"] = audit.sha256_text(
                    fixture_path.read_text()
                )
            cases = root / "cases.json"
            output = root / "scorecard.json"
            cases.write_text(json.dumps(benchmark))
            args = type("Args", (), {
                "cases": str(cases),
                "authority_rules": str(audit.DEFAULT_AUTHORITY_RULES),
                "fixture_root": str(root),
                "output": str(output),
            })
            status = audit.benchmark_command(args)
            return status, json.loads(output.read_text())

    def test_path_quote_and_hash_mutations_fail_provenance(self):
        mutations = {
            "path": (
                lambda extraction: extraction["claims"][0]["source"].update({
                    "path": "missing.mdx",
                }),
                "Claim source does not exist",
            ),
            "quote": (
                lambda extraction: extraction["claims"][0].update({
                    "quote": "Unsupported paraphrase",
                }),
                "Claim quote is not an exact source substring",
            ),
            "hash": (
                lambda extraction: extraction["claims"][0]["source"].update({
                    "content_sha256": "0" * 64,
                }),
                "Claim source hash is stale",
            ),
        }
        for name, (mutate_extraction, expected_error) in mutations.items():
            with self.subTest(name=name):
                status, scorecard = self.run_mutated_benchmark(
                    lambda _case, extraction, _path: mutate_extraction(
                        extraction
                    )
                )
                first = scorecard["cases"][0]
                self.assertEqual(status, 1)
                self.assertEqual(first["predicted"], "invalid-production-path")
                self.assertIn(
                    expected_error,
                    first["production_path_error"],
                )
                self.assertFalse(
                    scorecard["thresholds"]["production_path_has_no_errors"]
                )

    def test_unpinned_extraction_mutation_fails_fixture_fingerprint(self):
        status, scorecard = self.run_mutated_benchmark(
            lambda _case, extraction, _path: extraction.update({
                "model_identifier": "mutated",
            }),
            update_fixture_pin=False,
        )
        first = scorecard["cases"][0]
        self.assertEqual(status, 1)
        self.assertEqual(first["predicted"], "invalid-production-path")
        self.assertIn(
            "extraction fixture fingerprint mismatch",
            first["production_path_error"],
        )

    def test_extraction_failure_fails_production_path_gate(self):
        status, scorecard = self.run_mutated_benchmark(
            lambda _case, extraction, _path: extraction.update({
                "extraction_failures": ["injected extraction failure"],
            })
        )
        first = scorecard["cases"][0]
        self.assertEqual(status, 1)
        self.assertEqual(first["predicted"], "invalid-production-path")
        self.assertIn("unresolved failures", first["production_path_error"])
        self.assertFalse(scorecard["thresholds"]["production_path_has_no_errors"])

    def test_incorrect_adjudication_fails_falconer_gate(self):
        status, scorecard = self.run_mutated_benchmark(
            lambda _case, extraction, _path: (
                extraction["adjudicated_findings"][0].update({
                    "verdict": "insufficient-evidence",
                })
            )
        )
        first = scorecard["cases"][0]
        self.assertEqual(status, 1)
        self.assertEqual(first["expected"], "contradiction")
        self.assertEqual(first["predicted"], "insufficient-evidence")
        self.assertFalse(first["passed"])
        self.assertFalse(scorecard["thresholds"]["all_24_accounted_for"])


class GuardTests(unittest.TestCase):
    def test_schedule_guard_accepts_daylight_and_standard_windows(self):
        daylight = type("Args", (), {"at": "2026-07-06T17:00:00Z"})
        standard = type("Args", (), {"at": "2026-12-07T18:00:00Z"})
        self.assertEqual(audit.schedule_guard_command(daylight), 0)
        self.assertEqual(audit.schedule_guard_command(standard), 0)

    def test_schedule_guard_rejects_inactive_paired_schedule(self):
        inactive = type("Args", (), {"at": "2026-07-06T18:00:00Z"})
        self.assertEqual(audit.schedule_guard_command(inactive), 10)

    def test_concurrent_active_invocations_mutate_and_notify_once(self):
        with tempfile.TemporaryDirectory() as directory:
            state = Path(directory) / "state"
            mutations = []
            notifications = []

            def invoke(index):
                args = type("Args", (), {
                    "state_dir": str(state),
                    "event_id": f"run-{index}",
                    "at": "2026-07-06T17:00:00Z",
                })
                status = audit.schedule_claim_command(args)
                if status == 0:
                    mutations.append(args.event_id)
                    notifications.append(args.event_id)
                return status

            with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
                statuses = list(executor.map(invoke, range(8)))

            self.assertEqual(statuses.count(0), 1)
            self.assertEqual(statuses.count(11), 7)
            self.assertEqual(len(mutations), 1)
            self.assertEqual(len(notifications), 1)
            receipts = list((state / "schedule_claims").glob("*.json"))
            self.assertEqual([path.name for path in receipts], ["2026-07-06.json"])
            receipt = json.loads(receipts[0].read_text())
            self.assertEqual(receipt["business_date"], "2026-07-06")
            self.assertEqual(receipt["event_id"], mutations[0])


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
