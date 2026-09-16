#!/usr/bin/env python3
"""Unit tests for normalize_review_signal.py."""
from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_SPEC = importlib.util.spec_from_file_location(
    "normalize_review_signal", _HERE / "normalize_review_signal.py"
)
nrs = importlib.util.module_from_spec(_SPEC)
sys.modules[_SPEC.name] = nrs
_SPEC.loader.exec_module(nrs)


class TestNormalizeReviewSignal(unittest.TestCase):
    def test_replaces_workflow_owned_identifiers(self):
        output = (
            '[SIGNAL:pr-review] {"pr":"old","head_sha":"old","verdict":"Approve",'
            '"critical":0,"important":0,"reviewer_login":"agent"}'
        )

        normalized = nrs.normalize_review_signal(
            output, "748", "current-sha", "github-actions[bot]"
        )
        signal = json.loads(normalized.removeprefix("[SIGNAL:pr-review] "))

        self.assertEqual(signal["pr"], "748")
        self.assertEqual(signal["head_sha"], "current-sha")
        self.assertEqual(signal["reviewer_login"], "github-actions[bot]")


if __name__ == "__main__":
    unittest.main()
