#!/usr/bin/env python3
"""Enforce that every PR-producing content skill references the shared v1
agent-doc quality contract.

This is a "does not bypass the shared finalization path" regression test: if
a new content-generating skill is added without wiring it into the contract
(the `warpy-factory` marker + `## Documentation risk` section), this test
fails and names the skill, rather than the gap surfacing only after an
unreviewed PR ships.

Run:
    python3 .agents/skills/doc_quality_policy/test_manifest.py
"""
from __future__ import annotations

import unittest
from pathlib import Path

_SKILLS_ROOT = Path(__file__).resolve().parents[1]

# Keep in sync with the "PR-producing skill manifest" section of
# .agents/references/doc-quality-policy.md. Each entry is a SKILL.md path
# relative to .agents/skills/.
PR_PRODUCING_SKILLS = [
    "create_pr/SKILL.md",
    "draft_docs/SKILL.md",
    "release_updates/SKILL.md",
    "missing_docs/SKILL.md",
    "aeo_crosslink_audit/SKILL.md",
    "aeo_new_guide_recommendations/SKILL.md",
    "sync_terminology/SKILL.md",
    "sync-error-docs/SKILL.md",
    "sync-openapi-spec/SKILL.md",
    "docs-seo-audit/SKILL.md",
    "afdocs-fix/SKILL.md",
    "update-changelog/SKILL.md",
    "improve-drafting-skills/SKILL.md",
]

# Any of these substrings referencing the shared contract satisfies the check.
# A skill can reference the reference doc directly, the marker, or the shared
# scripts under doc_quality_policy/.
CONTRACT_REFERENCE_MARKERS = (
    "doc-quality-policy.md",
    "doc_quality_policy",
    "warpy-factory",
)


class TestManifestSkillsReferenceTheSharedContract(unittest.TestCase):
    def test_every_manifest_skill_file_exists(self):
        for rel_path in PR_PRODUCING_SKILLS:
            with self.subTest(skill=rel_path):
                self.assertTrue(
                    (_SKILLS_ROOT / rel_path).exists(),
                    f"manifest lists {rel_path!r} but the file does not exist",
                )

    def test_manifest_skills_reference_the_shared_contract(self):
        missing = []
        for rel_path in PR_PRODUCING_SKILLS:
            path = _SKILLS_ROOT / rel_path
            if not path.exists():
                continue
            text = path.read_text(encoding="utf-8")
            if not any(marker in text for marker in CONTRACT_REFERENCE_MARKERS):
                missing.append(rel_path)
        self.assertEqual(
            missing, [],
            f"these PR-producing skills do not reference the shared doc-quality "
            f"contract ({CONTRACT_REFERENCE_MARKERS}): {missing}",
        )


if __name__ == "__main__":
    unittest.main()
