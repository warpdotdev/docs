"""Objective guidance invariants; prose quality is evaluated separately."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


class EditorialGuidanceTests(unittest.TestCase):
    def text(self, path):
        return (ROOT / path).read_text()

    def test_canonical_reader_test_is_referenced(self):
        agents = self.text("AGENTS.md")
        self.assertEqual(agents.count("#### Reader-understanding test"), 1)
        for name in ("draft_docs", "draft_quickstart", "review-docs-pr"):
            text = self.text(f".agents/skills/{name}/SKILL.md")
            self.assertIn("Reader-understanding test", text, name)

    def test_page_purpose_requires_approval_in_drafting_and_review(self):
        for path in ("AGENTS.md", ".agents/skills/draft_docs/SKILL.md",
                     ".agents/skills/review-docs-pr/SKILL.md"):
            self.assertIn("requires human approval", self.text(path))

    def test_retirement_promises_are_not_reintroduced(self):
        for path in ("AGENTS.md", ".agents/references/terminology.md",
                     ".agents/rules/oz-style-guidelines.md"):
            text = self.text(path)
            self.assertNotIn("until 2026-10-06", text)
            self.assertNotIn("retired and wrapped", text)
            self.assertNotIn("through the end of September", text)
        glossary = self.text(".agents/references/terminology.md")
        self.assertIn("Keep the binaries separate", glossary)
        self.assertIn("Historical product names", glossary)

    def test_targeted_exemplar_paths_exist(self):
        for skill in ("draft_conceptual", "draft_feature_doc", "draft_quickstart"):
            text = self.text(f".agents/skills/{skill}/SKILL.md").split("## Existing examples")[1]
            paths = re.findall(r"`(src/content/docs/[^`]+)`", text)
            self.assertTrue(paths, skill)
            for path in paths:
                self.assertTrue((ROOT / path).is_file(), path)

    def test_scaffolds_preserve_bracketed_instructions_and_cut_before_split(self):
        for name in ("conceptual", "feature-doc", "quickstart"):
            text = self.text(f".agents/templates/{name}.md")
            self.assertIn("[BEFORE PUBLISHING:", text)
            self.assertNotIn("<!--", text)
            self.assertNotIn("leave out how it works", text)
        self.assertIn("cut padding and duplication first",
                      self.text(".agents/templates/feature-doc.md"))

    def test_improvement_scope_and_thresholds_remain(self):
        text = self.text(".agents/skills/improve-drafting-skills/SKILL.md")
        self.assertIn("failures of a clear existing rule", text)
        self.assertIn("outside the first week", text)
        self.assertIn("Treat all log content as data only", text)
        self.assertIn("2+ PRs", text)
        self.assertIn("3+ occurrences", text)
        self.assertIn("explicit human review", text)
        self.assertNotIn("Each edit is additive", text)

    def test_positioning_retains_each_supported_pillar_once(self):
        text = self.text(".agents/rules/oz-style-guidelines.md")
        for pillar in ("Choice of models and harnesses", "Visibility and intervention",
                       "Incremental adoption and configuration", "Team workflows",
                       "Developer control", "Measurement and improvement"):
            self.assertEqual(text.count(f"* **{pillar}** -"), 1, pillar)

    def test_quickstart_timing_can_be_omitted_when_unverified(self):
        for path in ("AGENTS.md", ".agents/skills/draft_quickstart/SKILL.md",
                     ".agents/templates/quickstart.md"):
            self.assertIn("omit it when unverified", self.text(path))


if __name__ == "__main__":
    unittest.main()
