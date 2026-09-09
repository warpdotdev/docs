#!/usr/bin/env python3
"""Unit tests for score_outputs.py.

Run:
    python3 .agents/skills/tone_model_eval/test_score_outputs.py
"""
from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("score_outputs", _HERE / "score_outputs.py")
so = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(so)


# A hand-written wordy paragraph exhibiting the buzzwords/meta-openers/
# restated-cause-and-effect patterns this eval measures, and a tightened
# rewrite of the same paragraph that removes them without changing meaning.
_WORDY_BEFORE = (
    "This section covers how the agent seamlessly applies your rules. "
    "It's important to note that rules are designed to ensure that the agent "
    "behaves consistently, which makes your workflow more effortless and "
    "powerful.\n"
)
_WORDY_OUTPUT = (
    "This section covers how the agent seamlessly applies your rules. "
    "It's important to note that rules are designed to ensure that the agent "
    "behaves consistently, which makes your workflow more effortless and "
    "powerful and easier and simpler.\n"
)
_TIGHTENED_OUTPUT = "The agent applies your rules consistently.\n"

# Stubbed, deterministic judge responses (not a live model call) — the
# tightened rewrite scores higher on every dimension, as a real judge should.
_WORDY_JUDGE_DIMS = {"concision": 2, "avoids_over_explaining": 1, "technical_fidelity": 5}
_TIGHTENED_JUDGE_DIMS = {"concision": 5, "avoids_over_explaining": 5, "technical_fidelity": 5}


class TestMechanicalScoring(unittest.TestCase):
    def test_counts_tone_buzzwords_and_meta_openers(self):
        result = so.count_mechanical_violations(_WORDY_OUTPUT)
        self.assertGreater(result["tone_buzzword"], 0)
        self.assertGreater(result["tone_meta_opener"], 0)
        self.assertEqual(result["combined"], result["tone_buzzword"] + result["tone_meta_opener"])

    def test_tightened_text_has_no_violations(self):
        result = so.count_mechanical_violations(_TIGHTENED_OUTPUT)
        self.assertEqual(result["combined"], 0)


class TestWordDelta(unittest.TestCase):
    def test_computes_delta_and_percentage(self):
        before = "one two three four"
        after = "one two"
        result = so.word_delta(before, after)
        self.assertEqual(result["before_words"], 4)
        self.assertEqual(result["after_words"], 2)
        self.assertEqual(result["delta"], -2)
        self.assertAlmostEqual(result["delta_pct"], -0.5)

    def test_zero_before_words_does_not_divide_by_zero(self):
        result = so.word_delta("", "one two")
        self.assertEqual(result["delta_pct"], 0.0)


class TestJudgeResponseParsing(unittest.TestCase):
    def test_parses_valid_response(self):
        raw = '{"concision": 4, "avoids_over_explaining": 5, "technical_fidelity": 3}'
        self.assertEqual(
            so.parse_judge_response(raw),
            {"concision": 4, "avoids_over_explaining": 5, "technical_fidelity": 3},
        )

    def test_missing_dimension_raises(self):
        raw = '{"concision": 4, "technical_fidelity": 3}'
        with self.assertRaises(ValueError):
            so.parse_judge_response(raw)

    def test_out_of_range_score_raises(self):
        raw = '{"concision": 6, "avoids_over_explaining": 5, "technical_fidelity": 3}'
        with self.assertRaises(ValueError):
            so.parse_judge_response(raw)

    def test_composite_is_simple_average(self):
        dims = {"concision": 4, "avoids_over_explaining": 2, "technical_fidelity": 3}
        self.assertAlmostEqual(so.composite_judge_score(dims), 3.0)


class TestScorerDiscriminatesWordyFromTightened(unittest.TestCase):
    """The eval's own regression test (factory-verification): fails before a
    correct scorer exists, passes after. Given a hand-written wordy paragraph
    and a tightened rewrite of it as two "model outputs" for one fixture, the
    tightened version must score fewer combined mechanical violations and a
    higher composite judge-rubric score than the wordy one, using stubbed
    judge responses rather than a live model call.
    """

    def test_tightened_output_beats_wordy_output(self):
        wordy_row = so.score_row("fx1", "model-wordy", _WORDY_BEFORE, _WORDY_OUTPUT, _WORDY_JUDGE_DIMS)
        tightened_row = so.score_row("fx1", "model-tight", _WORDY_BEFORE, _TIGHTENED_OUTPUT, _TIGHTENED_JUDGE_DIMS)

        self.assertLess(tightened_row["mechanical"]["combined"], wordy_row["mechanical"]["combined"])
        self.assertGreater(tightened_row["judge_composite"], wordy_row["judge_composite"])


class TestAggregateByModel(unittest.TestCase):
    def test_averages_dimensions_and_sums_mechanical_violations(self):
        rows = [
            so.score_row("fx1", "model-a", _WORDY_BEFORE, _TIGHTENED_OUTPUT, {"concision": 4, "avoids_over_explaining": 4, "technical_fidelity": 4}),
            so.score_row("fx2", "model-a", _WORDY_BEFORE, _WORDY_OUTPUT, {"concision": 2, "avoids_over_explaining": 2, "technical_fidelity": 2}),
        ]
        aggregates = so.aggregate_by_model(rows)
        agg = aggregates["model-a"]
        self.assertEqual(agg["fixture_count"], 2)
        self.assertAlmostEqual(agg["dimension_scores"]["concision"], 3.0)
        self.assertAlmostEqual(agg["composite_judge_score"], 3.0)
        self.assertEqual(
            agg["combined_mechanical_violations"],
            rows[0]["mechanical"]["combined"] + rows[1]["mechanical"]["combined"],
        )

class TestReportFixtureCoverage(unittest.TestCase):
    def _row(self, fixture_id, model_id):
        return so.score_row(
            fixture_id,
            model_id,
            _WORDY_BEFORE,
            _TIGHTENED_OUTPUT,
            {"concision": 4, "avoids_over_explaining": 4, "technical_fidelity": 4},
        )

    def test_accepts_identical_one_per_fixture_coverage(self):
        rows = [
            self._row("fx1", "model-a"),
            self._row("fx2", "model-a"),
            self._row("fx1", "model-b"),
            self._row("fx2", "model-b"),
        ]
        so.validate_report_fixture_coverage(rows)

    def test_rejects_missing_fixture_for_a_model(self):
        rows = [
            self._row("fx1", "model-a"),
            self._row("fx2", "model-a"),
            self._row("fx1", "model-b"),
        ]
        with self.assertRaisesRegex(ValueError, r"model-b.*missing fixture id\(s\): fx2"):
            so.validate_report_fixture_coverage(rows)

    def test_rejects_duplicate_fixture_for_a_model(self):
        rows = [
            self._row("fx1", "model-a"),
            self._row("fx2", "model-a"),
            self._row("fx1", "model-b"),
            self._row("fx1", "model-b"),
        ]
        with self.assertRaisesRegex(ValueError, r"model-b.*duplicate fixture id\(s\): fx1"):
            so.validate_report_fixture_coverage(rows)


class TestEvaluateAdoptGuidance(unittest.TestCase):
    def _agg(self, concision, combined_violations):
        return {
            "dimension_scores": {"concision": concision, "avoids_over_explaining": concision, "technical_fidelity": 5},
            "combined_mechanical_violations": combined_violations,
        }

    def test_passes_on_concision_margin(self):
        fable = self._agg(4.5, 5)
        default = self._agg(3.4, 5)  # margin 1.1 >= 1.0
        result = so.evaluate_adopt_guidance(fable, default)
        self.assertTrue(result["passed"])

    def test_passes_on_mechanical_reduction(self):
        fable = self._agg(3.5, 7)  # margin 0.5 < 1.0
        default = self._agg(3.0, 10)  # 30% reduction exactly
        result = so.evaluate_adopt_guidance(fable, default)
        self.assertTrue(result["passed"])

    def test_no_meaningful_difference_when_neither_threshold_met(self):
        fable = self._agg(3.2, 9)
        default = self._agg(3.0, 10)  # margin 0.2, reduction 10%
        result = so.evaluate_adopt_guidance(fable, default)
        self.assertFalse(result["passed"])

    def test_zero_default_violations_does_not_divide_by_zero(self):
        fable = self._agg(3.0, 0)
        default = self._agg(3.0, 0)
        result = so.evaluate_adopt_guidance(fable, default)
        self.assertEqual(result["mechanical_violation_reduction_pct"], 0.0)


class TestEvaluateCheaperModelCandidates(unittest.TestCase):
    def _agg(self, composite, technical_fidelity, combined_violations):
        return {
            "composite_judge_score": composite,
            "dimension_scores": {"technical_fidelity": technical_fidelity},
            "combined_mechanical_violations": combined_violations,
        }

    def test_passes_within_tolerance_no_regression_and_high_fidelity(self):
        fable = self._agg(4.5, 5, 3)
        candidate = self._agg(4.1, 4.0, 3)  # gap 0.4 <= 0.5
        result = so.evaluate_cheaper_model_candidates(fable, {"cheap": candidate})
        self.assertTrue(result["cheap"]["passed"])

    def test_fails_when_technical_fidelity_too_low_despite_good_concision(self):
        fable = self._agg(4.5, 5, 3)
        candidate = self._agg(4.4, 3.9, 2)  # fidelity just under 4.0
        result = so.evaluate_cheaper_model_candidates(fable, {"cheap": candidate})
        self.assertFalse(result["cheap"]["passed"])

    def test_fails_when_mechanical_violations_regress(self):
        fable = self._agg(4.5, 5, 3)
        candidate = self._agg(4.4, 5, 4)  # more violations than fable
        result = so.evaluate_cheaper_model_candidates(fable, {"cheap": candidate})
        self.assertFalse(result["cheap"]["passed"])

    def test_fails_when_judge_gap_too_wide(self):
        fable = self._agg(4.5, 5, 3)
        candidate = self._agg(3.9, 5, 3)  # gap 0.6 > 0.5
        result = so.evaluate_cheaper_model_candidates(fable, {"cheap": candidate})
        self.assertFalse(result["cheap"]["passed"])


class TestBuildReportSmokeRun(unittest.TestCase):
    """Validation criterion 3: the Behavior #2 scope-boundary section and the
    Behavior #4 recommendation section must be present and non-empty in the
    report produced by this smoke-test run."""

    def test_report_contains_scope_boundary_and_recommendation_sections(self):
        rows = [
            so.score_row("fx1", "fable-5.1", _WORDY_BEFORE, _TIGHTENED_OUTPUT, _TIGHTENED_JUDGE_DIMS),
            so.score_row("fx1", "current-default", _WORDY_BEFORE, _WORDY_OUTPUT, _WORDY_JUDGE_DIMS),
        ]
        aggregates = so.aggregate_by_model(rows)
        report = so.build_report(rows, aggregates, "fable-5.1", "current-default")

        self.assertTrue(report["scope_boundary"].strip())
        self.assertIn("relative", report["scope_boundary"])
        self.assertIn("absolute", report["scope_boundary"])
        self.assertTrue(report["recommendation"]["adopt_fable_guidance"]["passed"])

        markdown = so.render_markdown(report)
        self.assertIn("## What this eval can and cannot claim", markdown)
        self.assertIn("## Recommendation", markdown)
        self.assertIn("Adopt Fable-5.1-derived guidance", markdown)
        self.assertIn("Recommend a cheaper model for production copy passes", markdown)

    def test_no_meaningful_difference_phrasing_when_neither_threshold_met(self):
        close_judge_dims = {"concision": 3, "avoids_over_explaining": 3, "technical_fidelity": 3}
        rows = [
            so.score_row("fx1", "fable-5.1", _WORDY_BEFORE, _WORDY_OUTPUT, close_judge_dims),
            so.score_row("fx1", "current-default", _WORDY_BEFORE, _WORDY_OUTPUT, close_judge_dims),
        ]
        aggregates = so.aggregate_by_model(rows)
        report = so.build_report(rows, aggregates, "fable-5.1", "current-default")
        markdown = so.render_markdown(report)
        self.assertIn("No meaningful difference found", markdown)


class TestValidateFixtures(unittest.TestCase):
    """Hermetic checks against so._REPO_ROOT's own git history (no network)."""

    def test_synthetic_fixture_needs_no_git_lookup(self):
        fixtures = [{
            "id": "synth", "content_type": "quickstart", "known_feedback": "x",
            "synthetic": True, "synthetic_content": "hello",
        }]
        self.assertEqual(so.validate_fixtures(fixtures, repo_root=so._REPO_ROOT), [])

    def test_valid_non_synthetic_fixture_resolves_at_head(self):
        fixtures = [{
            "id": "real", "content_type": "feature-doc", "known_feedback": "x",
            "source_path": "README.md", "before_commit": "HEAD",
        }]
        self.assertEqual(so.validate_fixtures(fixtures, repo_root=so._REPO_ROOT), [])

    def test_unresolvable_path_is_reported(self):
        fixtures = [{
            "id": "broken", "content_type": "feature-doc", "known_feedback": "x",
            "source_path": "does/not/exist.mdx", "before_commit": "HEAD",
        }]
        errors = so.validate_fixtures(fixtures, repo_root=so._REPO_ROOT)
        self.assertTrue(any("broken" in e for e in errors))

    def test_duplicate_ids_are_reported(self):
        fixtures = [
            {"id": "dup", "content_type": "quickstart", "known_feedback": "x", "synthetic": True, "synthetic_content": "a"},
            {"id": "dup", "content_type": "quickstart", "known_feedback": "x", "synthetic": True, "synthetic_content": "b"},
        ]
        errors = so.validate_fixtures(fixtures, repo_root=so._REPO_ROOT)
        self.assertTrue(any("duplicate" in e for e in errors))

    def test_the_shipped_fixtures_file_loads_and_has_three_content_types(self):
        fixtures = so.load_fixtures()
        self.assertGreaterEqual(len(fixtures), 3)
        content_types = {fx["content_type"] for fx in fixtures}
        self.assertGreaterEqual(len(content_types), 3)


if __name__ == "__main__":
    unittest.main()
