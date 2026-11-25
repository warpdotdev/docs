"""Objective integration tests, not a report checker or semantic usability grader.

Run manually: python3 .agents/skills/doc_quality_policy/test_usability_guidance.py
"""
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
METHOD = ".agents/references/docs-usability-validation.md"
SKILL = ".agents/skills/validate_docs_usability/SKILL.md"
TEMPLATE = ".agents/templates/usability-validation.md"
EVALS = ".agents/skills/validate_docs_usability/evals/evals.json"
RUBRIC = ".agents/skills/validate_docs_usability/evals/rubric.json"
RUNNER = ".agents/skills/validate_docs_usability/evals/calibrate.py"


class UsabilityGuidanceTests(unittest.TestCase):
    def text(self, path):
        return (ROOT / path).read_text()

    def test_shared_workflows_invoke_the_skill_and_reference_the_method(self):
        for path in (
            "AGENTS.md",
            ".agents/references/doc-quality-policy.md",
            ".agents/skills/doc_quality_policy/SKILL.md",
            ".agents/skills/draft_docs/SKILL.md",
            ".agents/skills/review-docs-pr/SKILL.md",
            ".agents/skills/create_pr/SKILL.md",
        ):
            with self.subTest(path=path):
                text = self.text(path)
                self.assertIn(SKILL, text)
                self.assertIn("docs-usability-validation.md", text)

    def test_type_specific_skills_inherit_shared_drafting(self):
        for name in (
            "draft_conceptual", "draft_procedural", "draft_quickstart",
            "draft_reference", "draft_troubleshooting", "draft_faq",
            "draft_guide", "draft_feature_doc",
        ):
            with self.subTest(name=name):
                self.assertIn(
                    ".agents/skills/draft_docs/SKILL.md",
                    self.text(f".agents/skills/{name}/SKILL.md"),
                )

    def test_direct_content_callers_reference_scoped_validation(self):
        for name in (
            "missing_docs", "sync-error-docs", "docs-seo-audit",
            "afdocs-fix", "aeo_crosslink_audit",
        ):
            with self.subTest(name=name):
                self.assertIn(METHOD, self.text(f".agents/skills/{name}/SKILL.md"))

    def test_new_markdown_links_resolve_on_disk(self):
        for relative in (
            METHOD, SKILL, ".agents/references/docs-usability-worked-record.md",
            ".agents/references/docs-usability-automation.md",
            ".agents/skills/validate_docs_usability/evals/README.md",
        ):
            path = ROOT / relative
            for target in re.findall(r"\]\(([^)]+)\)", path.read_text()):
                with self.subTest(path=relative, target=target):
                    self.assertTrue((path.parent / target).is_file())

    def test_template_instructions_are_visible_and_cover_evidence(self):
        text = self.text(TEMPLATE)
        self.assertIn("[BEFORE HANDOFF:", text)
        self.assertNotIn("<!--", text)
        self.assertEqual(text.count("## Usability validation\n"), 1)
        for label in (
            "Scope", "Scenarios", "Tested version", "Method and limitations",
            "Question results", "Persona and priority", "Sufficient answer",
            "Entry and path", "Answer evidence", "Result",
            "Findability and completeness", "Finding and next action", "Retest",
        ):
            self.assertIn(f"* {label}: [", text)
        self.assertIn("### Readiness", text)

    def test_skill_frontmatter_and_name(self):
        text = self.text(SKILL)
        self.assertTrue(text.startswith("---\n"))
        frontmatter = text.split("---", 2)[1]
        self.assertIn("name: validate_docs_usability\n", frontmatter)
        self.assertRegex(frontmatter, r"\ndescription: .+")

    def test_fixtures_are_complete_calibration_inputs(self):
        data = json.loads(self.text(EVALS))
        self.assertEqual(data["skill_name"], "validate_docs_usability")
        self.assertIn("Synthetic", data["fixture_notice"])
        cases = data["evals"]
        self.assertEqual(len({case["id"] for case in cases}), len(cases))
        rubric = json.loads(self.text(RUBRIC))["evals"]
        self.assertEqual({case["id"] for case in cases}, {
            case["id"] for case in rubric
        })
        self.assertEqual({case["name"] for case in rubric}, {
            "clear-answer", "buried-answer", "missing-non-admin-prerequisite",
            "browser-only-dead-end", "broken-handoff",
            "conflicting-sibling-answer", "unavailable-preview",
            "stale-published-escape", "correct-page-broken-anchor",
            "secondary-incomplete-answer", "primary-incomplete-answer",
        })
        for case in cases:
            with self.subTest(case=case["id"]):
                self.assertEqual(set(case), {"id", "prompt", "fixture", "files"})
                self.assertTrue(case["prompt"])
                fixture = case["fixture"]
                self.assertTrue(fixture["version"])
                if fixture["pages"]:
                    self.assertIn(fixture["entry"], fixture["pages"])
                else:
                    self.assertTrue(fixture["availability"])

    def run_calibration(self, *args):
        return subprocess.run(
            [sys.executable, str(ROOT / RUNNER), *args],
            capture_output=True, text=True, cwd=tempfile.gettempdir(),
        )

    def compare(self, report):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "report.json"
            path.write_text(json.dumps(report))
            result = self.run_calibration("compare", "--report", str(path))
        return result, json.loads(result.stdout)

    def test_exported_payloads_contain_no_grader_fields_or_case_names(self):
        rubric = json.loads(self.text(RUBRIC))["evals"]
        for case in rubric:
            with self.subTest(case=case["id"]):
                result = self.run_calibration("export", "--case", str(case["id"]))
                self.assertEqual(result.returncode, 0, result.stderr)
                payload = json.loads(result.stdout)
                self.assertEqual(set(payload), {
                    "instructions", "fixture_notice", "method", "template", "case",
                })
                self.assertEqual(set(payload["case"]), {"id", "prompt", "fixture"})
                self.assertEqual(payload["case"]["id"], case["id"])
                self.assertEqual(payload["method"], self.text(METHOD))
                self.assertEqual(payload["template"], self.text(TEMPLATE))
                for graded_case in rubric:
                    self.assertNotIn(graded_case["name"], result.stdout)
                    self.assertNotIn(graded_case["criteria"], result.stdout)

    def test_deterministic_reports_round_trip_through_cli(self):
        for case in json.loads(self.text(RUBRIC))["evals"]:
            with self.subTest(case=case["id"]):
                exported = self.run_calibration("export", "--case", str(case["id"]))
                payload = json.loads(exported.stdout)
                report = {
                    "id": payload["case"]["id"],
                    "results": case["expected_results"],
                    "readiness": case["readiness"],
                    "report": "Deterministic plumbing test, not evaluator evidence.",
                }
                if "expected_retest_results" in case:
                    report["retest"] = {
                        "results": case["expected_retest_results"],
                        "readiness": case["retest_readiness"],
                        "report": "Deterministic retest, not evaluator evidence.",
                    }
                result, comparison = self.compare(report)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(comparison["mismatches"], [])
                self.assertTrue(comparison["manual_review_required"])
                self.assertEqual(comparison["criteria"], case["criteria"])

    def test_false_clear_on_primary_blocker_fails_comparison(self):
        result, comparison = self.compare({
            "id": 3, "results": ["Clear"], "readiness": "ready",
        })
        self.assertEqual(result.returncode, 1)
        self.assertTrue(comparison["false_clear_primary"])
        self.assertEqual(
            {item["field"] for item in comparison["mismatches"]},
            {"results", "readiness"},
        )

    def test_secondary_gap_is_not_reported_as_primary_false_clear(self):
        result, comparison = self.compare({
            "id": 10, "results": ["Clear", "Clear"], "readiness": "ready",
        })
        self.assertEqual(result.returncode, 1)
        self.assertFalse(comparison["false_clear_primary"])
        self.assertEqual(
            [item["field"] for item in comparison["mismatches"]], ["results"],
        )

    def test_primary_priority_changes_readiness_without_changing_pages(self):
        cases = {
            case["id"]: case
            for case in json.loads(self.text(EVALS))["evals"]
        }
        self.assertEqual(cases[10]["fixture"], cases[11]["fixture"])
        result, comparison = self.compare({
            "id": 11, "results": ["Partial", "Clear"], "readiness": "ready",
        })
        self.assertEqual(result.returncode, 1)
        self.assertEqual(comparison["mismatches"], [{
            "field": "readiness", "expected": "blocked", "actual": "ready",
        }])

    def test_retest_does_not_replace_initial_outcome(self):
        result, comparison = self.compare({
            "id": 4, "results": ["Clear"], "readiness": "ready",
            "retest": {"results": ["Clear"], "readiness": "ready"},
        })
        self.assertEqual(result.returncode, 1)
        self.assertTrue(comparison["false_clear_primary"])
        result, comparison = self.compare({
            "id": 4, "results": ["Partial"], "readiness": "blocked",
        })
        self.assertEqual(result.returncode, 1)
        self.assertEqual(
            {item["field"] for item in comparison["mismatches"]},
            {"retest.results", "retest.readiness"},
        )

    def test_unknown_case_fails_without_emitting_a_payload(self):
        result = self.run_calibration("export", "--case", "999")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertIn("Invalid case", result.stderr)


if __name__ == "__main__":
    unittest.main()
