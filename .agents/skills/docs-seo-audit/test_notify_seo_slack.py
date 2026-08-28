#!/usr/bin/env python3
"""Regression cases for the docs-seo-audit Slack same-day dedupe guard.

`find_existing_post()` is what stops the skill from posting a second SEO
Audit summary for a run that already succeeded (JAS-3: two chat.postMessage
calls ~11s apart for the same audit run, one with rough wording and one
cleaned up). These cases pin that a same-day top-level post is detected
regardless of exact text after the date prefix, that a different day or a
thread reply is not mistaken for one, and that an empty history never
blocks the first post.

Run from the repo root:
    python3 .agents/skills/docs-seo-audit/test_notify_seo_slack.py
"""
import importlib.util
import pathlib
import sys

HERE = pathlib.Path(__file__).parent
spec = importlib.util.spec_from_file_location("notify_seo_slack", HERE / "scripts" / "notify_seo_slack.py")
notify_seo_slack = importlib.util.module_from_spec(spec)
spec.loader.exec_module(notify_seo_slack)

DATE = "2026-08-28"

# (description, messages, expected find_existing_post result)
CASES = [
    (
        "no messages at all",
        [],
        False,
    ),
    (
        "top-level message already posted for today, exact wording",
        [{"ts": "1.0", "text": "*SEO Audit — 2026-08-28*\n276 pages scanned | ✅ No issues found"}],
        True,
    ),
    (
        "top-level message already posted for today, different wording after the prefix",
        [{"ts": "1.0", "text": "*SEO Audit — 2026-08-28*\nSome other draft of the same summary"}],
        True,
    ),
    (
        "message is for a different date",
        [{"ts": "1.0", "text": "*SEO Audit — 2026-08-21*\n183 issues found"}],
        False,
    ),
    (
        "matching text but it's a thread reply, not a top-level post",
        [{"ts": "2.0", "thread_ts": "1.0", "text": "*SEO Audit — 2026-08-28*\nfollow-up in thread"}],
        False,
    ),
    (
        "thread parent (thread_ts == ts) still counts as top-level",
        [{"ts": "1.0", "thread_ts": "1.0", "text": "*SEO Audit — 2026-08-28*\nhas replies now"}],
        True,
    ),
    (
        "unrelated top-level message present, no SEO Audit post yet",
        [{"ts": "1.0", "text": "good morning docs team"}],
        False,
    ),
]


def main() -> int:
    failures = 0

    for description, messages, expected in CASES:
        result = notify_seo_slack.find_existing_post(messages, DATE)
        ok = result == expected
        failures += 0 if ok else 1
        print(f"  [{'PASS' if ok else 'FAIL'}] {description:<70} got={result}")

    total = len(CASES)
    print()
    if failures:
        print(f"{failures} of {total} cases regressed.")
        return 1
    print(f"All {total} cases behave correctly.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
