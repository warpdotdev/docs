#!/usr/bin/env python3
"""Resolve a task requester's Slack user id to a GitHub handle, for this repo.

This docs-repo-local helper covers only the requester tier. Its private
Slack-to-GitHub mapping is supplied at runtime through
`REVIEWER_OVERRIDES_PATH`; it is intentionally not committed to this
repository. This keeps requester identity data in the factory-level private
override map while allowing a normal docs checkout to resolve a requester when
that map is mounted by the invoking environment.

It intentionally does the bare minimum and nothing more — no public-email
search, no cross-repo assumptions, no guessing. A missing map or unresolved
Slack id prints nothing (exit 0) and the caller's chain moves to the next tier.

Usage:
    REVIEWER_OVERRIDES_PATH=/private/path/reviewer_overrides.json \
      python3 resolve_reviewer.py --user <slack_id>

Prints the resolved GitHub handle to stdout, or nothing when unresolved.
"""
import argparse
import json
import os
import sys


def load_overrides(path):
    """Return a {slack_id: github_handle} map from a private override map.

    Returns an empty map when its runtime path is absent, missing, malformed,
    or has no usable entries — a missing override is not an error, it just
    fails to resolve.
    """
    if not path:
        return {}
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
        description="Resolve a Slack user id to a GitHub handle via a private override map.",
    )
    parser.add_argument("--user", dest="user", help="Slack user id to resolve.")
    parser.add_argument(
        "--overrides",
        help="Private override-map path; defaults to REVIEWER_OVERRIDES_PATH.",
    )
    args = parser.parse_args(argv)

    if not args.user:
        return 0
    handle = load_overrides(
        args.overrides or os.environ.get("REVIEWER_OVERRIDES_PATH")
    ).get(args.user)
    if handle:
        print(handle)
    return 0


if __name__ == "__main__":
    sys.exit(main())
