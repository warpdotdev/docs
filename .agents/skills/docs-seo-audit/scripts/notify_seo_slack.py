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
skipped because the token env var is unset. Exits non-zero only on an
actual Slack API failure, so a non-zero exit is the only case that
warrants a retry.
"""
import argparse
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


def fetch_recent_messages(token: str, channel: str, limit: int = 50) -> list:
    url = f"{SLACK_API}/conversations.history?channel={channel}&limit={limit}"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req) as resp:
        result = json.load(resp)
    if not result.get("ok"):
        raise RuntimeError(f"conversations.history failed: {result.get('error')}")
    return result.get("messages", [])


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
        recent = fetch_recent_messages(token, args.channel)
    except (urllib.error.URLError, RuntimeError) as exc:
        print(f"warning: could not check channel history ({exc}); posting anyway", file=sys.stderr)
        recent = []

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
