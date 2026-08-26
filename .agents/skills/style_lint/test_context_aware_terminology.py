#!/usr/bin/env python3
"""Regression cases for context-aware scanning in check_product_casing and
check_deprecated_terms (REV-38 rework cycle 3, PR #583).

The formal PR #583 review rejected the PR because `style_lint.py --all`
still flagged:
1. `Blocklist` in `code/code-review.mdx:64` -- the literal image filename
   `Blocklist-with-review-changes.png` inside a Markdown image's link
   destination, not prose.
2. `MacOS` in `sending-us-feedback.mdx:75,78` -- literal executable paths
   (`/Applications/Warp.app/Contents/MacOS/stable`) inside fenced ```bash
   code blocks.

Both checks only skipped a line that itself started with a backtick/fence
marker, so a multi-line fenced code block's *interior* lines (which don't
start with a backtick) and a Markdown link/image destination on an otherwise
prose line were both scanned as prose. The fix tracks complete fenced code
block spans and strips Markdown link/image destinations before matching,
while still scanning the surrounding human-visible prose normally. Run this
after touching `check_product_casing`, `check_deprecated_terms`, or
`_strip_markdown_destinations`.
"""
import importlib.util
import pathlib
import sys

HERE = pathlib.Path(__file__).parent
spec = importlib.util.spec_from_file_location("style_lint", HERE / "style_lint.py")
style_lint = importlib.util.module_from_spec(spec)
spec.loader.exec_module(style_lint)

# (check function, lines, should_flag, description)
CASES = [
    # --- deprecated-term (blocklist -> denylist) ---
    (
        style_lint.check_deprecated_terms,
        ["```", "add the user to the blocklist config", "```"],
        False,
        "'blocklist' inside a fenced code block must not be flagged",
    ),
    (
        style_lint.check_deprecated_terms,
        ["![Review changes.](../../assets/terminal/Blocklist-with-review-changes.png)"],
        False,
        "'Blocklist' inside a Markdown image destination must not be flagged",
    ),
    (
        style_lint.check_deprecated_terms,
        ["Add the user to the blocklist before continuing."],
        True,
        "genuine 'blocklist' in prose is still flagged",
    ),
    # --- external-casing (MacOS -> macOS), via check_product_casing ---
    (
        style_lint.check_product_casing,
        ["```bash", "RUST_LOG=info /Applications/Warp.app/Contents/MacOS/stable", "```"],
        False,
        "'MacOS' inside a fenced code block must not be flagged",
    ),
    (
        style_lint.check_product_casing,
        ["[Installer](https://example.com/downloads/MacOS/installer.dmg)"],
        False,
        "'MacOS' inside a Markdown link destination must not be flagged",
    ),
    (
        style_lint.check_product_casing,
        ["This build only runs on MacOS."],
        True,
        "genuine 'MacOS' in prose is still flagged",
    ),
]


def main() -> int:
    failures = 0
    for check_fn, lines, should_flag, description in CASES:
        issues = check_fn(lines, "test.mdx")
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
