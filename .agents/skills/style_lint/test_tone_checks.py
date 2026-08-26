#!/usr/bin/env python3
"""Regression cases for the tone checks: check_tone_buzzwords,
check_meta_openers, and check_callout_density.

Run from the repo root:
    python3 .agents/skills/style_lint/test_tone_checks.py

These are regexes over prose, which is exactly where false positives creep
in. The intentional exclusions (harness, unlock, elevated, journey) must
stay silent, inline code and fenced code blocks must never trip a match, and
the callout checks must tell "back to back" apart from callouts separated by
body prose.
"""
import importlib.util
import pathlib
import sys

HERE = pathlib.Path(__file__).parent
spec = importlib.util.spec_from_file_location("style_lint", HERE / "style_lint.py")
style_lint = importlib.util.module_from_spec(spec)
spec.loader.exec_module(style_lint)

BUZZWORD_CASES = [
    # (text, should_flag, description)
    ("This feature integrates seamlessly with your workflow.", True, "marketing adjective - seamless"),
    ("Leverage the API to automate this.", True, "inflated verb - leverage"),
    ("The dashboard shows the full landscape of running agents.", True, "abstract dramatics - landscape"),
    ("Enter the realm of agentic development.", True, "abstract dramatics - realm"),
    ("This is designed to help you ship faster.", True, "filler frame - designed to"),
    ("This ensures that every run starts clean.", True, "filler frame - ensures that"),
    ("Environment variables allow you to pass secrets safely.", True, "filler frame - allows you to"),
    ("Configure the key in order to authenticate.", True, "filler frame - in order to"),
    ("It's important to note that this is a preview feature.", True, "filler frame - it's important to note"),
    ("Use the agent harness to run this command.", False, "excluded - harness has a legitimate technical use"),
    ("Enter your password to unlock the keychain.", False, "excluded - unlock has a legitimate technical use"),
    ("This requires elevated permissions.", False, "excluded - elevated has a legitimate technical use"),
    ("Follow the onboarding journey to get set up.", False, "excluded - journey stays out of the lint"),
    ("Run `leverage-config` to see current settings.", False, "inline code is stripped before matching"),
]

META_OPENER_CASES = [
    (["This page covers how the integration works."], True, "meta-opener - covers"),
    (["This guide explains the setup process."], True, "meta-opener - explains"),
    (["This section walks through the API."], True, "meta-opener - walks through"),
    (["This document walks you through configuration."], True, "meta-opener - walks you through"),
    (["Run agents directly in your CI pipeline."], False, "states the thing itself"),
    (["```", "This page covers setup in a code sample.", "```"], False, "fenced code block is skipped"),
]

CALLOUT_DENSITY_CASES = [
    # (lines, should_flag, description)
    ([":::note", "one", ":::", "", ":::caution", "two", ":::"], True, "consecutive - only a blank line between"),
    ([":::note", "one", ":::", "Some body prose separates these.", ":::caution", "two", ":::"], False, "not consecutive - body prose between"),
    ([":::note", "1", ":::", ":::note", "2", ":::", ":::note", "3", ":::", ":::note", "4", ":::", ":::note", "5", ":::", "sep", ":::note", "6", ":::"], True, "over the per-page callout budget"),
]


def main() -> int:
    failures = 0
    total = 0

    print("check_tone_buzzwords:")
    for text, should_flag, description in BUZZWORD_CASES:
        total += 1
        flagged = bool(style_lint.check_tone_buzzwords(text.split("\n"), "test.mdx"))
        ok = flagged == should_flag
        if not ok:
            failures += 1
        print(f"  [{'PASS' if ok else 'FAIL'}] {description:<55} flagged={flagged}")

    print("\ncheck_meta_openers:")
    for lines, should_flag, description in META_OPENER_CASES:
        total += 1
        flagged = bool(style_lint.check_meta_openers(lines, "test.mdx"))
        ok = flagged == should_flag
        if not ok:
            failures += 1
        print(f"  [{'PASS' if ok else 'FAIL'}] {description:<55} flagged={flagged}")

    print("\ncheck_callout_density:")
    for lines, should_flag, description in CALLOUT_DENSITY_CASES:
        total += 1
        flagged = bool(style_lint.check_callout_density(lines, "test.mdx"))
        ok = flagged == should_flag
        if not ok:
            failures += 1
        print(f"  [{'PASS' if ok else 'FAIL'}] {description:<55} flagged={flagged}")

    print()
    if failures:
        print(f"{failures} of {total} cases regressed.")
        return 1
    print(f"All {total} cases behave correctly.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
