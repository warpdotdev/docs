#!/usr/bin/env python3
"""Regression cases for the RENAME_EXEMPT_SUFFIXES_BY_LITERAL guard in check_hardcoded_vars.

Run from the repo root:
    python3 .agents/skills/style_lint/test_hardcoded_var_exemptions.py

"Oz Cloud API Keys" is a literal Settings label the Warp client still renders
(see terminology.md's "What still says Oz"), so a bare "Oz" immediately
followed by " Cloud API Keys" must not be flagged as a hardcoded var that
should use {VARS.WARP_AUTOMATION_PLATFORM}. A previous migration got this
wrong exactly once (QUALITY-1768); this guard is what would have caught it.

The exemption is scoped to the "Oz" literal only, and within that literal it
is still just a suffix match, so it must stay narrow on two axes: a bare "Oz"
on its own, or "Oz" followed by unrelated text, must still be flagged; and a
*different* rename-sensitive literal that happens to end in the same suffix
(e.g. a hardcoded "Automation Platform Cloud API Keys") must still be flagged
too -- an earlier draft of this guard used one suffix list shared by every
literal, which silently suppressed that exact case.
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
    ("Click **Oz Cloud API Keys**.", False, "exempt literal Settings label"),
    (
        "**Settings** > **Cloud platform** > **Oz Cloud API Keys**.",
        False,
        "exempt literal Settings label inside a full path",
    ),
    ("Oz is deprecated in favor of the platform.", True, "bare Oz still flagged"),
    ("Ask Oz to do this.", True, "bare Oz followed by unrelated text"),
    ("Install the Oz CLI globally.", True, "distinct rename-sensitive entry still flagged"),
    (
        "Click **Automation Platform Cloud API Keys**.",
        True,
        "different literal sharing the exempt suffix still flagged",
    ),
]


def main() -> int:
    failures = 0
    for text, should_flag, description in CASES:
        issues = style_lint.check_hardcoded_vars(text.split("\n"), "test.mdx")
        flagged = bool(issues)
        ok = flagged == should_flag
        if not ok:
            failures += 1
        print(f"  [{'PASS' if ok else 'FAIL'}] {description:<52} flagged={flagged}")

    print()
    if failures:
        print(f"{failures} of {len(CASES)} cases regressed.")
        return 1
    print(f"All {len(CASES)} cases behave correctly.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
