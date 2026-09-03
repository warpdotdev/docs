#!/usr/bin/env python3
"""Regression cases for check_header_case's sentence-boundary handling.

A header is normally sentence case: only the very first word is capitalized.
But a header can legitimately contain more than one rendered sentence (a
two-question FAQ title, for example), and each sentence gets its own
capitalized first word. Before this test existed, `check_header_case` and
`_to_sentence_case` only ever protected word index 0, so a rework on PR #583
found this had silently lowercased the second sentence's leading word in a
two-question FAQ heading ("...yet. How does billing work?" -> "...yet. how
does billing work?"). Run this after touching `_to_sentence_case`,
`check_header_case`, or `_sentence_start_indices`.
"""
import importlib.util
import pathlib
import sys

HERE = pathlib.Path(__file__).parent
spec = importlib.util.spec_from_file_location("style_lint", HERE / "style_lint.py")
style_lint = importlib.util.module_from_spec(spec)
spec.loader.exec_module(style_lint)

# (header text without the leading '#'s, should_flag, description)
CASES = [
    ("Enabling Computer Use", False,
     "single sentence, fully protected proper feature name"),
    ("My co-workers are using Lovelace but were not on a Team Together yet. How does billing work?", True,
     "two-sentence FAQ title; genuine Title Case words (Team, Together) in the first sentence trigger the fix"),
    ("Is Warp Fully Free? No it Requires a plan", True,
     "second sentence starts right after a question mark, with a genuine mid-sentence Title Case word (Requires) later in that sentence"),
]

# (header text, expected fixed text) -- the fix must lowercase genuine
# mid-sentence Title Case words while preserving the capital that starts the
# second sentence.
FIX_CASES = [
    (
        "My co-workers are using Lovelace but were not on a Team Together yet. How does billing work?",
        "My co-workers are using lovelace but were not on a team together yet. How does billing work?",
    ),
    (
        "Is Warp Fully Free? No it Requires a plan",
        "Is warp fully free? No it requires a plan",
    ),
]


def main() -> int:
    failures = 0
    for text, should_flag, description in CASES:
        line = f"## {text}"
        issues = style_lint.check_header_case([line], "test.mdx")
        flagged = bool(issues)
        ok = flagged == should_flag
        if not ok:
            failures += 1
        print(f"  [{'PASS' if ok else 'FAIL'}] {description:<90} flagged={flagged}")

    for text, expected_fixed in FIX_CASES:
        fixed = style_lint._to_sentence_case(text)
        ok = fixed == expected_fixed
        if not ok:
            failures += 1
        print(f"  [{'PASS' if ok else 'FAIL'}] fix preserves the second sentence's capital: {fixed!r}")

    total = len(CASES) + len(FIX_CASES)
    print()
    if failures:
        print(f"{failures} of {total} cases regressed.")
        return 1
    print(f"All {total} cases behave correctly.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
