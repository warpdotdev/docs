#!/usr/bin/env python3
"""Print stale GitHub Actions change-request review IDs, one per line."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Iterable, Mapping, Optional


def stale_review_ids(
    reviews: Iterable[Mapping[str, object]],
    head_sha: str,
    reviewer_login: str = "github-actions[bot]",
) -> list[int]:
    """Select only prior blocking reviews published by the automation account."""
    stale_ids: list[int] = []
    for review in reviews:
        author = review.get("user")
        login = author.get("login") if isinstance(author, Mapping) else None
        if (
            login == reviewer_login
            and review.get("state") == "CHANGES_REQUESTED"
            and review.get("commit_id") != head_sha
            and isinstance(review.get("id"), int)
        ):
            stale_ids.append(review["id"])
    return stale_ids


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reviews", required=True, type=Path)
    parser.add_argument("--head-sha", required=True)
    parser.add_argument("--reviewer-login", default="github-actions[bot]")
    args = parser.parse_args(argv)
    try:
        reviews = json.loads(args.reviews.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    if not isinstance(reviews, list):
        print("error: reviews JSON must be an array", file=sys.stderr)
        return 1
    for review_id in stale_review_ids(
        reviews, args.head_sha, args.reviewer_login
    ):
        print(review_id)
    return 0


if __name__ == "__main__":
    sys.exit(main())
