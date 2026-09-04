#!/usr/bin/env python3
"""Unit tests for stale_review_requests.py."""
from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


_HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location(
    "stale_review_requests", _HERE / "stale_review_requests.py"
)
srr = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = srr
_spec.loader.exec_module(srr)


class TestStaleReviewIds(unittest.TestCase):
    def test_selects_only_prior_automated_change_requests(self):
        reviews = [
            {
                "id": 1,
                "state": "CHANGES_REQUESTED",
                "commit_id": "old-sha",
                "user": {"login": "github-actions[bot]"},
            },
            {
                "id": 2,
                "state": "CHANGES_REQUESTED",
                "commit_id": "current-sha",
                "user": {"login": "github-actions[bot]"},
            },
            {
                "id": 3,
                "state": "APPROVED",
                "commit_id": "old-sha",
                "user": {"login": "github-actions[bot]"},
            },
            {
                "id": 4,
                "state": "CHANGES_REQUESTED",
                "commit_id": "old-sha",
                "user": {"login": "reviewer"},
            },
        ]

        self.assertEqual(srr.stale_review_ids(reviews, "current-sha"), [1])


if __name__ == "__main__":
    unittest.main()
