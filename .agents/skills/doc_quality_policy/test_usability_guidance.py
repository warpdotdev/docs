"""Objective integration tests, not a report checker or semantic usability grader.

Run manually: python3 .agents/skills/doc_quality_policy/test_usability_guidance.py
"""
import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
METHOD = ".agents/references/docs-usability-validation.md"
SKILL = ".agents/skills/validate_docs_usability/SKILL.md"
TEMPLATE = ".agents/templates/usability-validation.md"
EVALS = ".agents/skills/validate_docs_usability/evals/evals.json"


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
        for relative in (METHOD, SKILL):
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
        self.assertEqual({case["name"] for case in cases}, {
            "clear-answer", "buried-answer", "missing-non-admin-prerequisite",
            "browser-only-dead-end", "broken-handoff",
            "conflicting-sibling-answer", "unavailable-preview",
        })
        for case in cases:
            with self.subTest(case=case["name"]):
                self.assertTrue(case["prompt"])
                self.assertTrue(case["expected_output"])
                self.assertIn(case["expected_result"], {
                    "Clear", "Found with friction", "Partial",
                    "Missing", "Conflicting", "Not tested",
                })
                fixture = case["fixture"]
                self.assertTrue(fixture["version"])
                if case["name"] != "unavailable-preview":
                    self.assertIn(fixture["entry"], fixture["pages"])
                else:
                    self.assertEqual(fixture["pages"], {})
                    self.assertTrue(fixture["availability"])


if __name__ == "__main__":
    unittest.main()
