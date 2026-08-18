#!/usr/bin/env python3
"""Regression cases for check_factory_proper_noun.

Run from the repo root:
    python3 .agents/skills/style_lint/test_factory_proper_noun.py

The rule is narrow: "Warp Factories" is the product, an individual "factory" is
a lowercase common noun, and a bare capitalized "Factory" is never a proper
noun. Almost all of the difficulty is in NOT firing, because a capital F is
usually positional rather than a name -- headings, sidebar labels, bullets,
table cells, quoted terms, and link text all start with one legitimately.

The first draft of this check produced 9 hits across the docs and 8 of them
were wrong: heading-initial ("## Factory-definition pull request checks"),
list-initial link text ("* [Factory dashboard](...)"), frontmatter labels, a
quoted term at the start of a sentence, a verbatim UI string ("Add your Factory
to your team"), and a reference to Factory.ai, the company behind Droid. Each
of those is a case below. If you touch the check, run this first.
"""
import importlib.util
import pathlib
import sys

HERE = pathlib.Path(__file__).parent
spec = importlib.util.spec_from_file_location("style_lint", HERE / "style_lint.py")
style_lint = importlib.util.module_from_spec(spec)
spec.loader.exec_module(style_lint)

CASES = [
    # (text, should_flag, description)
    # --- genuine proper-noun uses ---
    ("See [Factory agents](/factories/factory-agents/) for the roles.", True,
     "mid-sentence link text"),
    ("Every Factory gets its own Slack app.", True,
     "mid-sentence, standing in for the product"),
    ("Runs started by the Factory are tracked.", True,
     "definite article plus a capital"),
    ("Review the Factory metrics before deciding.", True,
     "mid-sentence attributive use of the banned form"),
    # --- the product name, written correctly ---
    ("Warp Factories is in Early Access.", False, "the product name"),
    ("Connect Warp Factories to your repository.", False, "product name mid-sentence"),
    # --- positional capitals ---
    ("## Factory-definition pull request checks", False, "heading-initial"),
    ("### Factory agents", False, "subheading-initial"),
    ("* [Factory dashboard](/factories/factory-dashboard/) - the surface.", False,
     "list-initial link text"),
    ("Factory setup doesn't choose models for you.", False, "sentence-initial"),
    ('"Factory dashboard" names the whole surface.', False, "quoted term, sentence-initial"),
    ("| **Factory definition** | The definition files |", False, "table-cell-initial"),
    ("The tab is read-only. Factory owners can still edit it.", False,
     "initial after a sentence boundary"),
    # --- sanctioned exceptions ---
    ("Send work through the Factory MCP.", False, "Factory MCP is the shipped feature name"),
    ("Enter a **Factory name**, such as `Payments`.", False, "verbatim UI field label"),
    ("The **Factory definition** tab lists the files.", False, "verbatim UI tab label"),
    ("1. In factory setup, go to **Add your Factory to your team**.", False,
     "verbatim UI string, allowlisted as a phrase"),
    ("* **Droid** — Factory's CLI coding agent", False,
     "Factory.ai, an unrelated company"),
    # --- non-prose ---
    ("Fetch `/api/v1/Factory/source` for the definition.", False, "inline code"),
    ('<img alt="Factory settings page" src="x.png" />', False, "HTML attribute"),
]

FRONTMATTER_CASE = (
    ['---', 'title: Factory dashboard', 'sidebar:', '  label: "Factory agents"', '---',
     'The factory dashboard is the web app for one factory.'],
    False,
    "frontmatter titles and labels are headline-style",
)


def main() -> int:
    failures = 0
    for text, should_flag, description in CASES:
        flagged = bool(style_lint.check_factory_proper_noun(text.split("\n"), "test.mdx"))
        ok = flagged == should_flag
        if not ok:
            failures += 1
        print(f"  [{'PASS' if ok else 'FAIL'}] {description:<48} flagged={flagged}")

    lines, should_flag, description = FRONTMATTER_CASE
    flagged = bool(style_lint.check_factory_proper_noun(lines, "test.mdx"))
    ok = flagged == should_flag
    if not ok:
        failures += 1
    print(f"  [{'PASS' if ok else 'FAIL'}] {description:<48} flagged={flagged}")

    total = len(CASES) + 1
    print()
    if failures:
        print(f"{failures} of {total} cases regressed.")
        return 1
    print(f"All {total} cases behave correctly.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
