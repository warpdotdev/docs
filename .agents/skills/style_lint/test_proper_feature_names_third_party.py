#!/usr/bin/env python3
"""Regression cases for PROPER_FEATURE_NAMES entries added on PR #583 (REV-38).

`check_header_case` mistakenly flagged and lowercased several correctly
capitalized proper nouns in headings, because they weren't in
PROPER_FEATURE_NAMES: Warp's own "Bring Your Own LLM (BYOLLM)" feature name,
and third-party/technical proper nouns ("Bitbucket Data Center", GCP's
"Workload Identity Pool and Provider" / "Workload Identity Federation", and
Warp's own "Direct backend" self-hosting term). style_lint's proper-noun
protection is scoped to Warp's own product names by design and does not
generalize to third-party proper nouns -- these are narrow, named exceptions,
not a broadening of that scope. Run this after touching PROPER_FEATURE_NAMES
or check_header_case.
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
    ("Bring Your Own LLM (BYOLLM)", False, "Warp's own BYOLLM feature name"),
    ('Does Warp support other model routers or "Bring Your Own LLM"?', False,
     "BYOLLM phrase mid-sentence inside quotes"),
    ("Bitbucket Data Center / Server", False, "Atlassian's official edition name"),
    ("Step 1: Create a Workload Identity Pool and Provider", False,
     "GCP's official IAM resource name"),
    ("Step 3: Enable Workload Identity Federation in your cloud agent environment", False,
     "GCP's official federation mechanism name"),
    ("2. Start the worker with the Direct backend", False,
     "Warp's own self-hosting backend name"),
    # A generic Title Case header unrelated to any of these terms must still flag.
    ("This Is A Generic Title Case Heading", True,
     "unrelated Title Case header is still caught"),
]


def main() -> int:
    failures = 0
    for text, should_flag, description in CASES:
        line = f"### {text}"
        issues = style_lint.check_header_case([line], "test.mdx")
        flagged = bool(issues)
        ok = flagged == should_flag
        if not ok:
            failures += 1
        print(f"  [{'PASS' if ok else 'FAIL'}] {description:<60} flagged={flagged}")

    print()
    if failures:
        print(f"{failures} of {len(CASES)} cases regressed.")
        return 1
    print(f"All {len(CASES)} cases behave correctly.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
