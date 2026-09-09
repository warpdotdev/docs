#!/usr/bin/env python3
"""Unit tests for check_compression_contract.py.

Run:
    python3 .agents/skills/doc_quality_policy/test_check_compression_contract.py
"""
from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("check_compression_contract", _HERE / "check_compression_contract.py")
ccc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ccc)


def _page(word_count: int, callouts: int = 0) -> str:
    words = " ".join(f"word{i}" for i in range(word_count))
    callout_blocks = "\n".join(
        f":::note\nnote {i}\n:::\n" for i in range(callouts)
    )
    return f"---\ndescription: test\n---\n{callout_blocks}\n{words}\n"


class TestCountWords(unittest.TestCase):
    def test_counts_body_words_excluding_frontmatter(self):
        text = "---\ntitle: x\ndescription: y\n---\none two three\n"
        self.assertEqual(ccc.count_words(text), 3)

    def test_excludes_code_fences(self):
        text = "---\ndescription: y\n---\none two\n```\ncode code code\n```\nthree\n"
        self.assertEqual(ccc.count_words(text), 3)

    def test_link_text_counts_but_url_does_not(self):
        text = "---\ndescription: y\n---\nSee [the docs](https://example.com/a/b/c) here.\n"
        # "See", "the", "docs", "here." = 4 words; URL is dropped.
        self.assertEqual(ccc.count_words(text), 4)


class TestCountCallouts(unittest.TestCase):
    def test_counts_callout_blocks(self):
        text = "---\ndescription: y\n---\n:::note\nhi\n:::\n:::tip\nyo\n:::\n"
        self.assertEqual(ccc.count_callouts(text), 2)

    def test_ignores_callout_examples_inside_code_fences(self):
        text = ":::note\nreal\n:::\n```md\n:::tip\nexample\n:::\n```\n"
        self.assertEqual(ccc.count_callouts(text), 1)


class TestCheckCompressionContract(unittest.TestCase):
    def test_quickstart_within_budget_passes(self):
        text = _page(500)
        self.assertEqual(ccc.check_compression_contract(text, "quickstart"), [])

    def test_quickstart_over_budget_fails(self):
        text = _page(700)
        findings = ccc.check_compression_contract(text, "quickstart")
        self.assertTrue(any("exceeds the quickstart budget" in f for f in findings))

    def test_feature_doc_over_budget_fails(self):
        text = _page(1600)
        findings = ccc.check_compression_contract(text, "feature-doc")
        self.assertTrue(any("exceeds the feature-doc budget" in f for f in findings))

    def test_generated_changelog_is_exempt_from_word_budget(self):
        text = _page(5000)
        self.assertEqual(ccc.check_compression_contract(text, "changelog"), [])

    def test_generated_changelog_still_enforces_callout_budget(self):
        text = _page(5000, callouts=3)
        findings = ccc.check_compression_contract(text, "changelog")
        self.assertTrue(any("callouts exceed" in f for f in findings))

    def test_too_many_callouts_fails(self):
        text = _page(100, callouts=3)
        findings = ccc.check_compression_contract(text, "quickstart")
        self.assertTrue(any("callouts exceed" in f for f in findings))

    def test_two_callouts_is_within_budget(self):
        text = _page(100, callouts=2)
        self.assertEqual(ccc.check_compression_contract(text, "quickstart"), [])


if __name__ == "__main__":
    unittest.main()
