#!/usr/bin/env python3
"""Focused regression tests for weekly 404 report normalization and filtering."""

import contextlib
import csv
import importlib.util
import io
import json
import pathlib
import tempfile
import unittest
from unittest import mock


HERE = pathlib.Path(__file__).parent
spec = importlib.util.spec_from_file_location(
    "run_404_report",
    HERE / "run_404_report.py",
)
run_404_report = importlib.util.module_from_spec(spec)
spec.loader.exec_module(run_404_report)


class RedirectSourceNormalizationTests(unittest.TestCase):
    def test_optional_trailing_slash_matches_requested_path(self):
        redirects = {
            "redirects": [
                {
                    "source": "/Features/Session_Management/Launch-Configuration(/?)",
                    "destination": "/terminal/sessions/launch-configurations/",
                    "statusCode": 308,
                }
            ]
        }

        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / "vercel.json"
            path.write_text(json.dumps(redirects), encoding="utf-8")
            with contextlib.redirect_stderr(io.StringIO()):
                sources = run_404_report.load_redirect_sources(path)

        self.assertEqual(
            sources,
            {"/features/session_management/launch-configuration"},
        )

    def test_real_query_and_fragment_are_removed(self):
        redirects = {
            "redirects": [
                {
                    "source": "/Legacy/Query?campaign=docs",
                    "destination": "/current/query/",
                    "statusCode": 308,
                },
                {
                    "source": "/Legacy/Fragment#overview",
                    "destination": "/current/fragment/",
                    "statusCode": 308,
                },
                {
                    "source": "/Legacy/Trailing/",
                    "destination": "/current/trailing/",
                    "statusCode": 308,
                }
            ]
        }

        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / "vercel.json"
            path.write_text(json.dumps(redirects), encoding="utf-8")
            with contextlib.redirect_stderr(io.StringIO()):
                sources = run_404_report.load_redirect_sources(path)

        self.assertEqual(
            sources,
            {"/legacy/query", "/legacy/fragment", "/legacy/trailing"},
        )
        self.assertEqual(
            run_404_report.normalise_url(
                "https://docs.warp.dev/Legacy/Path/?campaign=docs#overview"
            ),
            "/legacy/path",
        )


class UnroutablePathTests(unittest.TestCase):
    def test_only_colon_prefixed_segments_are_unroutable(self):
        self.assertTrue(run_404_report.is_unroutable_path("/:*logging"))
        self.assertTrue(run_404_report.is_unroutable_path("/foo/:)%3cb%3evoice"))
        self.assertFalse(run_404_report.is_unroutable_path("/foo:bar"))
        self.assertFalse(run_404_report.is_unroutable_path("/normal/path"))

    def test_unroutable_paths_stay_in_raw_and_csv_accounting(self):
        current = [
            {"broken_url": "/:*logging", "hits": 10},
            {"broken_url": "/:)%3cb%3evoice", "hits": 9},
            {"broken_url": "/real-gap", "hits": 7},
            {"broken_url": "/long-tail", "hits": 2},
        ]
        prior = [{"broken_url": "/:)%3cb%3evoice", "hits": 4}]

        with tempfile.TemporaryDirectory() as tmp:
            report_dir = pathlib.Path(tmp) / "reports"
            with mock.patch.object(
                run_404_report,
                "query_404_events",
                side_effect=[current, prior],
            ), mock.patch.object(
                run_404_report,
                "total_404_count",
                side_effect=[28, 4],
            ), mock.patch.object(
                run_404_report,
                "load_redirect_sources",
                return_value=set(),
            ), mock.patch.dict(
                run_404_report.os.environ,
                {
                    "REPORT_DIR": str(report_dir),
                    "VERCEL_JSON_PATH": str(pathlib.Path(tmp) / "vercel.json"),
                    "REPORT_MIN_HITS": "5",
                },
                clear=False,
            ), contextlib.redirect_stdout(io.StringIO()) as stdout, \
                 contextlib.redirect_stderr(io.StringIO()):
                run_404_report.main()

            summary = json.loads(stdout.getvalue())
            with open(summary["csv_path"], newline="", encoding="utf-8") as report:
                csv_rows = list(csv.DictReader(report))

        self.assertEqual(summary["uncovered_count"], 4)
        self.assertEqual(summary["new_gaps_count"], 3)
        self.assertEqual(summary["unroutable_count"], 2)
        self.assertEqual(summary["significant_uncovered_count"], 1)
        self.assertEqual(summary["significant_new_gaps_count"], 1)
        self.assertEqual(summary["long_tail_count"], 1)
        self.assertEqual(
            [row["broken_url"] for row in summary["top_significant_uncovered"]],
            ["/real-gap"],
        )
        self.assertEqual(
            {row["broken_url"] for row in csv_rows},
            {"/:*logging", "/:)%3cb%3evoice", "/real-gap", "/long-tail"},
        )


if __name__ == "__main__":
    unittest.main()
