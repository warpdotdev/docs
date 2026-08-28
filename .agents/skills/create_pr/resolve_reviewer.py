#!/usr/bin/env python3
"""Resolve a task requester's Slack user id to a GitHub handle, for this repo.

This is the docs-repo-local counterpart to `factory-agents`' broader
`scripts/factory-resolve-reviewer`. That script lives in the separate
`factory-agents` repo and is not checked out alongside a normal
`warpdotdev/docs` clone, so a call to it from this repo's `create_pr/SKILL.md`
reviewer-request chain fails in a real docs run and silently falls through to
the next tier. This script covers exactly the requester tier: a manual,
checked-in override map (`reviewer_overrides.json`, sibling to this script)
keyed by Slack user id.

It intentionally does the bare minimum and nothing more — no public-email
search, no cross-repo assumptions, no guessing. An unresolved Slack id prints
nothing (exit 0) and the caller's chain moves to the next tier, matching the
"never guesses" contract of `factory-resolve-reviewer`.

Usage:
    python3 resolve_reviewer.py --user <slack_id>

Prints the resolved GitHub handle to stdout, or nothing when unresolved.
"""
import argparse
import json
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OVERRIDES_PATH = os.path.join(SCRIPT_DIR, "reviewer_overrides.json")


def load_overrides(path=OVERRIDES_PATH):
    """Return a {slack_id: github_handle} map from reviewer_overrides.json.

    Returns an empty map when the file is absent, malformed, or has no usable
    entries — a missing override is not an error, it just fails to resolve.
    """
    try:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
    except (FileNotFoundError, OSError, json.JSONDecodeError):
        return {}
    users = data.get("users") if isinstance(data, dict) else None
    if not isinstance(users, list):
        return {}
    indexed = {}
    for user in users:
        if not isinstance(user, dict):
            continue
        slack_id = str(user.get("slack_id", "")).strip()
        github = str(user.get("github", "")).strip()
        if slack_id and github:
            indexed[slack_id] = github
    return indexed


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="resolve_reviewer.py",
        description="Resolve a Slack user id to a GitHub handle via this repo's checked-in override map.",
    )
    parser.add_argument("--user", dest="user", help="Slack user id to resolve.")
    args = parser.parse_args(argv)

    if not args.user:
        return 0

    handle = load_overrides().get(args.user)
    if handle:
        print(handle)
    return 0


if __name__ == "__main__":
    sys.exit(main())
