#!/usr/bin/env python3
"""One-shot Slack poster for the SEO audit summary, with same-day dedupe.

Ensures a single audit run never posts its Slack summary more than once,
even across a "let me clean up the wording" retry: it checks the channel
for an existing top-level SEO Audit message dated today before posting,
and skips when one is already there. There is no separate post-then-check
step to race against, so an agent that runs this twice in one turn cannot
produce two messages.

Usage:
    python3 notify_seo_slack.py --channel CHANNEL_ID --date YYYY-MM-DD \
        --message-file /path/to/summary.txt

Exits 0 when the notification was posted, skipped due to dedupe, or
skipped because the token env var is unset. Exits non-zero when the
Slack API fails to post, or when the same-day history check itself
could not be verified — an unverified history check is treated as a
failure rather than an empty history, so a duplicate is never posted
on the ambiguous retry path. A non-zero exit is the only case that
warrants a retry.
"""
import argparse
import datetime
import json
import os
import sys
import urllib.error
import urllib.request

SLACK_API = "https://slack.com/api"


def is_top_level(message: dict) -> bool:
    """A message is top-level (not a reply within a thread) when it has no
    ``thread_ts``, or ``thread_ts`` equals its own ``ts`` (the parent of a
    thread is still that thread's original top-level post)."""
    thread_ts = message.get("thread_ts")
    return thread_ts is None or thread_ts == message.get("ts")


def find_existing_post(messages: list, date_str: str) -> bool:
    """Return True if ``messages`` already contains a top-level SEO Audit
    summary for ``date_str`` (e.g. ``2026-08-28``)."""
    prefix = f"*SEO Audit — {date_str}*"
    for message in messages:
        if not is_top_level(message):
            continue
        if message.get("text", "").startswith(prefix):
            return True
    return False


def day_start_ts(date_str: str) -> float:
    """Return the Unix timestamp for the start (UTC midnight) of ``date_str``,
    used as the ``oldest`` bound so pagination can stop once history is older
    than the target date."""
    day = datetime.datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=datetime.timezone.utc)
    return day.timestamp()


def fetch_messages_for_date(token: str, channel: str, date_str: str, page_size: int = 200) -> list:
    """Fetch every message posted on or after the start of ``date_str`` by
    paginating ``conversations.history`` with ``oldest`` set to that day's
    start. A fixed-size single page can push an earlier same-day summary out
    of a busy channel's dedupe window, so this keeps requesting the next
    cursor until Slack reports no more pages."""
    oldest = day_start_ts(date_str)
    messages = []
    cursor = None
    while True:
        url = (
            f"{SLACK_API}/conversations.history?channel={channel}"
            f"&limit={page_size}&oldest={oldest}"
        )
        if cursor:
            url += f"&cursor={cursor}"
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
        with urllib.request.urlopen(req) as resp:
            result = json.load(resp)
        if not result.get("ok"):
            raise RuntimeError(f"conversations.history failed: {result.get('error')}")
        messages.extend(result.get("messages", []))
        cursor = result.get("response_metadata", {}).get("next_cursor")
        if not cursor:
            break
    return messages


def post_message(token: str, channel: str, text: str) -> dict:
    payload = json.dumps(
        {
            "channel": channel,
            "text": text,
            "unfurl_links": False,
            "unfurl_media": False,
        }
    ).encode()
    req = urllib.request.Request(
        f"{SLACK_API}/chat.postMessage",
        data=payload,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req) as resp:
        return json.load(resp)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--channel", required=True, help="Slack channel ID to post to")
    parser.add_argument("--date", required=True, help="Today's date, e.g. 2026-08-28")
    parser.add_argument("--message-file", required=True, help="Path to the message text to post")
    parser.add_argument("--token-env", default="BUZZ_SLACK_TOKEN", help="Env var holding the Slack bot token")
    args = parser.parse_args()

    token = os.environ.get(args.token_env, "")
    if not token:
        print(f"{args.token_env} not set — skipping Slack notification", file=sys.stderr)
        return 0

    with open(args.message_file, "r", encoding="utf-8") as f:
        message = f.read()

    try:
        recent = fetch_messages_for_date(token, args.channel, args.date)
    except (urllib.error.URLError, RuntimeError) as exc:
        # An unverified history check can't rule out an earlier same-day post,
        # so fail closed rather than risk sending a duplicate: report the
        # failure and skip the post instead of posting on an empty history.
        print(f"error: could not check channel history ({exc}); skipping post to avoid a possible duplicate", file=sys.stderr)
        return 1

    if find_existing_post(recent, args.date):
        print(f"Skipping post: a SEO Audit summary for {args.date} already exists in {args.channel}.")
        return 0

    try:
        result = post_message(token, args.channel, message)
    except urllib.error.URLError as exc:
        print(f"Slack post failed: {exc}", file=sys.stderr)
        return 1

    if not result.get("ok"):
        print(f"Slack error: {result.get('error')}", file=sys.stderr)
        return 1

    print("Posted SEO Audit summary to Slack.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
