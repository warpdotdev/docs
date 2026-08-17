#!/usr/bin/env python3
"""Regression cases for check_platform_determiner.

Run from the repo root:
    python3 .agents/skills/style_lint/test_platform_determiner.py

The check has to separate three referential positions (possessive,
prepositional, subject) from several attributive ones that are correctly bare.
The ordering between those tests is load-bearing and easy to get wrong: an
earlier draft applied the attributive exemption before classifying position,
which silently stopped flagging "{...} provides ..." because "provides" is
just a lowercase word to a regex. A later draft flagged "automated {...} runs"
because "runs" is in the subject-verb list even though it is a noun there.

Both bugs are covered below. If you touch the check, run this first.
"""
import importlib.util
import pathlib
import sys

HERE = pathlib.Path(__file__).parent
spec = importlib.util.spec_from_file_location("style_lint", HERE / "style_lint.py")
style_lint = importlib.util.module_from_spec(spec)
spec.loader.exec_module(style_lint)

T = "{VARS.WARP_AUTOMATION_PLATFORM}"

CASES = [
    # (text, should_flag, description)
    (f"Run agents with {T}.", True, "prepositional - needs the article"),
    (f"{T} provides the CLI and API.", True, "clause subject - needs the article"),
    (f"Connects to {T}'s backend.", True, "possessive - needs the article"),
    (f"Handled by {T}, then reported.", True, "prepositional before a comma"),
    (f"Run agents with the {T}.", False, "determiner already present"),
    (f"Use {T} orchestration for this.", False, "attributive - modifies a noun"),
    (f"An environment for automated {T} runs.", False, "attributive - 'runs' is a noun here"),
    (f"Available in {T} cloud environments.", False, "attributive - modifies a noun"),
    (f"Deploy on {T}-hosted infrastructure.", False, "hyphenated compound"),
    (f"* **{T}** - the platform.", False, "bold term lead in a definition list"),
    (f"available with the\n{T} for teams.", False, "determiner on the previous line"),
]


def main() -> int:
    failures = 0
    for text, should_flag, description in CASES:
        flagged = bool(style_lint.check_platform_determiner(text.split("\n"), "test.mdx"))
        ok = flagged == should_flag
        if not ok:
            failures += 1
        print(f"  [{'PASS' if ok else 'FAIL'}] {description:<48} flagged={flagged}")

    print()
    if failures:
        print(f"{failures} of {len(CASES)} cases regressed.")
        return 1
    print(f"All {len(CASES)} cases behave correctly.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
