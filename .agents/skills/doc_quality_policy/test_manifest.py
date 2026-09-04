#!/usr/bin/env python3
"""Enforce that every PR-producing content skill/script references the shared
v1 agent-doc quality contract.

This is a "does not bypass the shared finalization path" regression test.
Rather than checking a manually maintained list -- which a new PR-producing
skill or script can silently join without ever being added -- this test
*discovers* every file under `.agents/skills/` whose text contains a direct
PR-creation signal (a literal `gh pr create` invocation, a `subprocess`
argv building one, a `--create-pr` flag, or a `def create_pr(` definition)
and asserts each discovered file references the shared contract. A new
PR-producing entry point that skips the contract fails this test by being
discovered, not by being missing from a list someone forgot to update.

Run:
    python3 .agents/skills/doc_quality_policy/test_manifest.py
"""
from __future__ import annotations

import re
import unittest
from pathlib import Path
from typing import List

_SKILLS_ROOT = Path(__file__).resolve().parents[1]

# Any of these appearing in a file's text is a direct PR-creation code path --
# not merely a mention of, or delegation to, another skill that creates PRs.
_PR_CREATION_SIGNALS = (
    re.compile(r"gh[\"']?\s*,?\s*[\"']?pr[\"']?\s*,?\s*[\"']?create"),  # `gh pr create` or ["gh","pr","create"]
    re.compile(r"--create-pr\b"),
    re.compile(r"^def create_pr\w*\(", re.MULTILINE),
)

# Any of these appearing in the same file satisfies the shared-contract
# requirement. A file can reference the reference doc directly, the marker
# label, or the shared scripts under doc_quality_policy/.
_CONTRACT_REFERENCE_MARKERS = (
    "doc-quality-policy.md",
    "doc_quality_policy",
    "warpy-factory",
)

# Files that are part of the contract's own implementation/tests, or that are
# not documentation-content skills, so a PR-creation-shaped string in them
# (e.g. quoting `gh pr create` in a docstring example, or the manifest's own
# regex source) is not a bypass. Recorded here, one line each, so removing an
# entry is a deliberate, reviewed decision rather than a silent gap.
_EXEMPT_RELATIVE_PATHS = {
    # This file's own PR-creation regex source text matches its own pattern.
    "doc_quality_policy/test_manifest.py",
    # Documents when to run the checker ("before `gh pr create`"); the
    # checker validates PR body text and never calls `gh pr create` itself.
    "create_pr/check_pr_body.py",
    # Documents the downstream validate_ui_refs `--create-pr` step it runs
    # before; this skill only compares screenshots and never opens a PR.
    "verify-settings-subsections/SKILL.md",
}

_SCAN_SUFFIXES = (".md", ".py")


def discover_pr_producing_files(skills_root: Path) -> List[Path]:
    """Return every file under `skills_root` with a direct PR-creation signal."""
    found = []
    for path in sorted(skills_root.rglob("*")):
        if not path.is_file() or path.suffix not in _SCAN_SUFFIXES:
            continue
        rel = path.relative_to(skills_root).as_posix()
        if rel in _EXEMPT_RELATIVE_PATHS:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        if any(pattern.search(text) for pattern in _PR_CREATION_SIGNALS):
            found.append(path)
    return found


def references_shared_contract(text: str) -> bool:
    return any(marker in text for marker in _CONTRACT_REFERENCE_MARKERS)


class TestDiscoveredPrProducingFilesReferenceTheSharedContract(unittest.TestCase):
    def test_discovery_finds_the_known_pr_producing_entry_points(self):
        """Sanity check on the discovery mechanism itself: if this drops to
        zero, the regexes have drifted and the real assertion below would
        pass vacuously.
        """
        discovered = discover_pr_producing_files(_SKILLS_ROOT)
        self.assertGreater(len(discovered), 5, f"discovered only {discovered!r}")

    def test_every_discovered_pr_producing_file_references_the_shared_contract(self):
        missing = []
        for path in discover_pr_producing_files(_SKILLS_ROOT):
            text = path.read_text(encoding="utf-8")
            if not references_shared_contract(text):
                missing.append(str(path.relative_to(_SKILLS_ROOT)))
        self.assertEqual(
            missing, [],
            "these files directly create PRs but do not reference the shared "
            f"doc-quality contract ({_CONTRACT_REFERENCE_MARKERS}): {missing}",
        )


if __name__ == "__main__":
    unittest.main()
