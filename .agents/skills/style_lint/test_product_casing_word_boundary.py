#!/usr/bin/env python3
"""Regression cases for check_product_casing's word-boundary matching.

`check_product_casing` used to find wrong-casing terms with a plain
`str.find`, which matches a term as a substring of a longer word. Since
"agent mode" is literally a substring of "agent model", this corrupted
"Switch the base agent model" into "Switch the base Agent Model" on
`--fix` (found during the PR #583 rework, REV-38). A plain `\\b...\\b`
regex does not fully fix this either: `\\b` requires a transition to/from a
word character, which fails for terms ending in punctuation (e.g. "A.I."
followed by a space or end of line has no such transition). The fix uses
lookarounds that only check the adjacent character is not a word character,
which handles both cases. Run this after touching `check_product_casing`,
`_word_bounded_pattern`, `PRODUCT_CASING`, or `EXTERNAL_CASING`.
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
    ("Switch the base agent model", False,
     "'agent mode' must not match inside 'agent model'"),
    ("Switch the base agent mode", True,
     "genuine 'agent mode' still flagged"),
    ("Toggle agent modes for different tasks", False,
     "'agent mode' must not match inside plural 'agent modes'"),
    ("This uses A.I. today", True,
     "'A.I.' followed by a space still flagged despite ending in punctuation"),
    ("This uses A.I.s today", False,
     "'A.I.' must not match inside 'A.I.s'"),
    ("I use Warp Terminal daily", True, "genuine 'Warp Terminal' still flagged"),
    ("Uses MacOSX for testing", False, "'MacOS' must not match inside 'MacOSX'"),
    ("Uses MacOS for testing", True, "genuine 'MacOS' still flagged"),
]


def main() -> int:
    failures = 0
    for text, should_flag, description in CASES:
        issues = style_lint.check_product_casing([text], "test.mdx")
        flagged = bool(issues)
        ok = flagged == should_flag
        if not ok:
            failures += 1
        print(f"  [{'PASS' if ok else 'FAIL'}] {description:<70} flagged={flagged}")

    print()
    if failures:
        print(f"{failures} of {len(CASES)} cases regressed.")
        return 1
    print(f"All {len(CASES)} cases behave correctly.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
