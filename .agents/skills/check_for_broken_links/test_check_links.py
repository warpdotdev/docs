#!/usr/bin/env python3
"""Regression cases for same-page (`#fragment`) link validation.

`should_skip()` used to filter out every bare `#fragment` link before
`check_fragment()` ever ran, so a same-page link to a renamed or deleted
heading passed silently instead of being reported broken. These cases pin
the fix: a valid same-page fragment stays valid, and an invalid one is
flagged.

Run from the repo root:
    python3 .agents/skills/check_for_broken_links/test_check_links.py
"""
import importlib.util
import pathlib
import sys
import tempfile

HERE = pathlib.Path(__file__).parent
spec = importlib.util.spec_from_file_location("check_links", HERE / "check_links.py")
check_links = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check_links)

# (description, filename, page content, expected broken urls)
CASES = [
    (
        "valid bare #fragment matches a heading on the same page",
        "valid.md",
        "## Getting Started\n\nSee [the setup steps](#getting-started) for details.\n",
        [],
    ),
    (
        "invalid bare #fragment has no matching heading on the same page",
        "invalid.md",
        "## Getting Started\n\nSee [a missing section](#does-not-exist) for details.\n",
        ["#does-not-exist"],
    ),
]


def main() -> int:
    failures = 0

    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)
        checker = check_links.LinkChecker(root)

        skip = checker.should_skip("#getting-started")
        ok = skip is False
        failures += 0 if ok else 1
        print(f"  [{'PASS' if ok else 'FAIL'}] should_skip() no longer drops bare #fragment links")

        for description, filename, content, expected_broken in CASES:
            page = root / filename
            page.write_text(content, encoding="utf-8")

            broken, _ = checker.check_file(page, check_internal=True, check_external=False)
            broken_urls = [link["url"] for link in broken]
            ok = broken_urls == expected_broken
            failures += 0 if ok else 1
            print(f"  [{'PASS' if ok else 'FAIL'}] {description:<58} broken={broken_urls}")

    total = len(CASES) + 1
    print()
    if failures:
        print(f"{failures} of {total} cases regressed.")
        return 1
    print(f"All {total} cases behave correctly.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
