#!/usr/bin/env python3
"""Regression cases for the docs-seo-audit Slack same-day dedupe guard.

`find_existing_post()` is what stops the skill from posting a second SEO
Audit summary for a run that already succeeded (JAS-3: two chat.postMessage
calls ~11s apart for the same audit run, one with rough wording and one
cleaned up). These cases pin that a same-day top-level post is detected
regardless of exact text after the date prefix, that a different day or a
thread reply is not mistaken for one, and that an empty history never
blocks the first post.

`fetch_messages_for_date()` and `main()` are also covered here: a same-day
post that only shows up on a later history page must still be found (a
fixed single-page window can miss it in a busy channel), and a failed
history check must fail closed — skipping the post — rather than treating
an unverified history as empty and posting anyway.

Run from the repo root:
    python3 .agents/skills/docs-seo-audit/test_notify_seo_slack.py
"""
import importlib.util
import json
import pathlib
import sys
import tempfile
import urllib.error
from unittest import mock

HERE = pathlib.Path(__file__).parent
spec = importlib.util.spec_from_file_location("notify_seo_slack", HERE / "scripts" / "notify_seo_slack.py")
notify_seo_slack = importlib.util.module_from_spec(spec)
spec.loader.exec_module(notify_seo_slack)

DATE = "2026-08-28"


class _FakeResponse:
    """Minimal context-manager stand-in for the object urlopen() returns."""

    def __init__(self, payload: dict):
        self._body = json.dumps(payload).encode()

    def __enter__(self):
        return self

    def __exit__(self, *exc_info):
        return False

    def read(self):
        return self._body

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


def _paged_urlopen(pages: list, request_urls=None):
    """Return a urlopen() stand-in that serves ``pages`` in order, one per
    call, recording each request URL when ``request_urls`` is supplied."""
    call_count = {"n": 0}

    def _urlopen(req, *args, **kwargs):
        if request_urls is not None:
            request_urls.append(req.full_url)
        index = min(call_count["n"], len(pages) - 1)
        call_count["n"] += 1
        return _FakeResponse(pages[index])

    return _urlopen


def check_pagination_finds_later_page_match() -> bool:
    """A same-day post that only appears on the second history page must
    still be found — the fixed 50-message single page this regresses could
    miss it in a busy channel."""
    page_1 = {
        "ok": True,
        "messages": [{"ts": "3.0", "text": "unrelated chatter"}],
        "response_metadata": {"next_cursor": "cursor+abc&next=value"},
    }
    page_2 = {
        "ok": True,
        "messages": [{"ts": "1.0", "text": f"*SEO Audit — {DATE}*\nfound on a later page"}],
        "response_metadata": {},
    }
    request_urls = []
    with mock.patch.object(
        notify_seo_slack.urllib.request,
        "urlopen",
        _paged_urlopen([page_1, page_2], request_urls),
    ):
        messages = notify_seo_slack.fetch_messages_for_date("tok", "C123", DATE, page_size=1)
    expected_follow_up_url = (
        f"{notify_seo_slack.SLACK_API}/conversations.history?"
        "channel=C123&limit=1&oldest=1787875200.0&cursor=cursor%2Babc%26next%3Dvalue"
    )
    return (
        notify_seo_slack.find_existing_post(messages, DATE) is True
        and request_urls[1] == expected_follow_up_url
    )


def check_fetch_stops_pagination_when_no_next_cursor() -> bool:
    """A response with no ``next_cursor`` ends pagination after a single
    page instead of looping forever."""
    page_1 = {"ok": True, "messages": [{"ts": "1.0", "text": "only page"}], "response_metadata": {}}
    with mock.patch.object(notify_seo_slack.urllib.request, "urlopen", _paged_urlopen([page_1])):
        messages = notify_seo_slack.fetch_messages_for_date("tok", "C123", DATE)
    return messages == [{"ts": "1.0", "text": "only page"}]


def check_main_fails_closed_on_history_error() -> bool:
    """When the history check itself fails, main() must skip the post
    (non-zero exit, no chat.postMessage call) rather than treat the
    unverified history as empty and post anyway."""
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as f:
        f.write("*SEO Audit — 2026-08-28*\nsummary body")
        message_file = f.name

    argv = [
        "notify_seo_slack.py",
        "--channel", "C123",
        "--date", DATE,
        "--message-file", message_file,
        "--token-env", "TEST_SLACK_TOKEN",
    ]
    with mock.patch.object(sys, "argv", argv), \
         mock.patch.dict(notify_seo_slack.os.environ, {"TEST_SLACK_TOKEN": "xoxb-test"}), \
         mock.patch.object(
             notify_seo_slack, "fetch_messages_for_date",
             side_effect=RuntimeError("conversations.history failed: ratelimited"),
         ), \
         mock.patch.object(notify_seo_slack, "post_message") as post_mock:
        exit_code = notify_seo_slack.main()

    return exit_code != 0 and not post_mock.called


def check_main_fails_closed_on_url_error() -> bool:
    """A network-level failure (URLError) during the history check must
    also fail closed, not just the RuntimeError (Slack ``ok: false``) case."""
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as f:
        f.write("*SEO Audit — 2026-08-28*\nsummary body")
        message_file = f.name

    argv = [
        "notify_seo_slack.py",
        "--channel", "C123",
        "--date", DATE,
        "--message-file", message_file,
        "--token-env", "TEST_SLACK_TOKEN",
    ]
    with mock.patch.object(sys, "argv", argv), \
         mock.patch.dict(notify_seo_slack.os.environ, {"TEST_SLACK_TOKEN": "xoxb-test"}), \
         mock.patch.object(
             notify_seo_slack, "fetch_messages_for_date",
             side_effect=urllib.error.URLError("connection refused"),
         ), \
         mock.patch.object(notify_seo_slack, "post_message") as post_mock:
        exit_code = notify_seo_slack.main()

    return exit_code != 0 and not post_mock.called


BEHAVIOR_CHECKS = [
    ("same-day post found on a later pagination page", check_pagination_finds_later_page_match),
    ("pagination stops when a page has no next_cursor", check_fetch_stops_pagination_when_no_next_cursor),
    ("main() fails closed (skips posting) on a Slack API history error", check_main_fails_closed_on_history_error),
    ("main() fails closed (skips posting) on a network history error", check_main_fails_closed_on_url_error),
]


def main() -> int:
    failures = 0

    for description, messages, expected in CASES:
        result = notify_seo_slack.find_existing_post(messages, DATE)
        ok = result == expected
        failures += 0 if ok else 1
        print(f"  [{'PASS' if ok else 'FAIL'}] {description:<70} got={result}")

    for description, check in BEHAVIOR_CHECKS:
        ok = check()
        failures += 0 if ok else 1
        print(f"  [{'PASS' if ok else 'FAIL'}] {description:<70}")

    total = len(CASES) + len(BEHAVIOR_CHECKS)
    print()
    if failures:
        print(f"{failures} of {total} cases regressed.")
        return 1
    print(f"All {total} cases behave correctly.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
