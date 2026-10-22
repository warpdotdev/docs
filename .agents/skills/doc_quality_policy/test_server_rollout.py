#!/usr/bin/env python3
"""Unit tests for server_rollout.py.

Run:
    python3 .agents/skills/doc_quality_policy/test_server_rollout.py
"""
from __future__ import annotations

import contextlib
import importlib.util
import io
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


_HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("server_rollout", _HERE / "server_rollout.py")
sr = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = sr
_spec.loader.exec_module(sr)


FEATURES_GO = textwrap.dedent(
    """\
    package features

    func getFeatureEnabled(name string) bool {
    \treturn viper.GetBool("features." + name)
    }

    func ShippedEnabled() bool {
    \treturn getFeatureEnabled("shipped")
    }

    func SetShippedEnabled(t *testing.T, enabled bool) {
    \tupdateTestingFeatureFlag(t, "shipped", enabled)
    }

    // DeferredReposEnabled gates deferred repositories.
    func DeferredReposEnabled() bool {
    \treturn getFeatureEnabled("deferred_repos")
    }

    func MissingFromConfigEnabled() bool {
    \treturn getFeatureEnabled("missing_from_config")
    }

    func DogfoodOnlyEnabled() bool {
    \treturn config.IsDogfood() && getFeatureEnabled("shipped")
    }

    func StagingEnvEnabled() bool {
    \treturn config.IsStaging()
    }

    func DelegatesEnabled() bool {
    \treturn DeferredReposEnabled()
    }

    func UnknownCallEnabled() bool {
    \treturn config.IsRegularServer() && getFeatureEnabled("shipped")
    }

    func EitherEnabled() bool {
    \treturn getFeatureEnabled("deferred_repos") || getFeatureEnabled("other")
    }

    func DefaultOnEnabled() bool {
    \tconst key = "features.default_on"
    \tif viper.IsSet(key) {
    \t\treturn viper.GetBool(key)
    \t}
    \treturn true
    }

    func SelfImprovementAPIEnabled() bool {
    \treturn getSelfImprovementFlagEnabled("api")
    }
    """
)

PROD_YAML = textwrap.dedent(
    """\
    server_origins:
      - https://app.warp.dev
    features:
      shipped: true
      deferred_repos: false # off until GA
      other: false
      nested_setting:
        enabled: true
      string_value: "hello"
    self_improvement:
      api: true
    unrelated:
      deferred_repos: true
    """
)

STAGING_YAML = textwrap.dedent(
    """\
    features:
      shipped: true
      deferred_repos: true
      other: false
      staging_key_only: true
    self_improvement:
      api: true
    """
)


def write_server(root: Path) -> Path:
    server = root / "warp-server"
    (server / "config" / "features").mkdir(parents=True)
    (server / "config" / "features" / "features.go").write_text(FEATURES_GO, encoding="utf-8")
    (server / "config" / "prod.yaml").write_text(PROD_YAML, encoding="utf-8")
    (server / "config" / "staging.yaml").write_text(STAGING_YAML, encoding="utf-8")
    return server


def run_main(argv):
    stdout, stderr = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
        code = sr.main(argv)
    return code, stdout.getvalue(), stderr.getvalue()


class TestParseAccessors(unittest.TestCase):
    def setUp(self):
        self.accessors = sr.parse_accessors(FEATURES_GO)

    def test_only_exported_zero_arg_bool_funcs(self):
        self.assertIn("ShippedEnabled", self.accessors)
        self.assertNotIn("SetShippedEnabled", self.accessors)
        self.assertNotIn("getFeatureEnabled", self.accessors)

    def test_reads_keys_from_both_blocks(self):
        self.assertEqual(self.accessors["ShippedEnabled"].keys, [("features", "shipped")])
        self.assertEqual(self.accessors["SelfImprovementAPIEnabled"].keys, [("self_improvement", "api")])
        self.assertEqual(self.accessors["DefaultOnEnabled"].keys, [("features", "default_on")])
        self.assertTrue(self.accessors["DefaultOnEnabled"].default_when_unset)

    def test_records_env_conditions_delegates_and_unknown_calls(self):
        self.assertEqual(self.accessors["DogfoodOnlyEnabled"].env_conditions, ["dogfood"])
        self.assertEqual(self.accessors["StagingEnvEnabled"].env_conditions, ["staging"])
        self.assertEqual(self.accessors["DelegatesEnabled"].delegates, ["DeferredReposEnabled"])
        self.assertEqual(self.accessors["UnknownCallEnabled"].unknown_calls, ["config.IsRegularServer"])
        self.assertTrue(self.accessors["EitherEnabled"].has_or)


class TestParseFlagBlocks(unittest.TestCase):
    def test_reads_first_level_bools_in_flag_blocks_only(self):
        values = sr.parse_flag_blocks(PROD_YAML)
        self.assertIs(values[("features", "shipped")], True)
        self.assertIs(values[("features", "deferred_repos")], False)
        self.assertIs(values[("self_improvement", "api")], True)
        self.assertIsNone(values[("features", "nested_setting")])
        self.assertIsNone(values[("features", "string_value")])
        self.assertNotIn(("features", "enabled"), values)
        self.assertNotIn(("unrelated", "deferred_repos"), values)


class TestEvaluate(unittest.TestCase):
    def setUp(self):
        self.rollouts = sr.ServerRollouts(
            sr.parse_accessors(FEATURES_GO),
            {"prod": sr.parse_flag_blocks(PROD_YAML), "staging": sr.parse_flag_blocks(STAGING_YAML)},
        )

    def state(self, name):
        return self.rollouts.rollout(name).state

    def test_states(self):
        cases = {
            "ShippedEnabled": "on-in-prod",
            "DeferredReposEnabled": "staging-only",
            "MissingFromConfigEnabled": "off",
            "DogfoodOnlyEnabled": "staging-only",
            "StagingEnvEnabled": "staging-only",
            "DelegatesEnabled": "staging-only",
            "SelfImprovementAPIEnabled": "on-in-prod",
            "DefaultOnEnabled": "on-in-prod",
        }
        for name, expected in cases.items():
            with self.subTest(name=name):
                self.assertEqual(self.state(name), expected)

    def test_unresolvable_conditions_are_unknown_not_guessed(self):
        self.assertIsNone(self.rollouts.rollout("UnknownCallEnabled").prod)
        self.assertIsNone(self.rollouts.rollout("EitherEnabled").prod)

    def test_unknown_call_still_false_when_a_known_condition_is_false(self):
        accessors = sr.parse_accessors(
            "func X() bool {\n\treturn config.IsRegularServer() && getFeatureEnabled(\"off_flag\")\n}\n"
        )
        self.assertIs(sr.evaluate("X", accessors, "prod", {("features", "off_flag"): False}), False)

    def test_config_keys_without_an_accessor_are_listed(self):
        names = {rollout.name: rollout.state for rollout in self.rollouts.all_rollouts()}
        self.assertEqual(names["features.staging_key_only"], "staging-only")

    def test_find_by_accessor_key_and_qualified_key(self):
        self.assertEqual([r.name for r in self.rollouts.find("DeferredReposEnabled")], ["DeferredReposEnabled"])
        self.assertEqual([r.name for r in self.rollouts.find("deferred_repos")], ["features.deferred_repos"])
        self.assertEqual([r.name for r in self.rollouts.find("features.staging_key_only")], ["features.staging_key_only"])
        self.assertEqual([r.state for r in self.rollouts.find("missing_from_config")], ["off"])
        self.assertEqual(self.rollouts.find("nope"), [])


class TestCodeMatches(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.server = write_server(Path(self.tmp.name))
        self.rollouts = sr.load(self.server)
        filler = "\n".join("\t_ = 0" for _ in range(sr.CO_OCCURRENCE_WINDOW + 5))
        self.write(
            "logic/runs/plan.go",
            "package runs\n\n"
            "func resolvePlan() {\n"
            "\tif features.DeferredReposEnabled() {\n"
            "\t\tuseRequiredRepos()\n"
            "\t}\n"
            "}\n\n"
            "func farApart() {\n"
            "\tif features.ShippedEnabled() {\n"
            "\t}\n"
            f"{filler}\n"
            "\tuseRequiredRepos()\n"
            "}\n",
        )
        self.write("logic/runs/plan_test.go", "func t() {\n\tfeatures.DeferredReposEnabled()\n\trequired_repos := 1\n}\n")
        self.write("client/x.go", "func c() {\n\tfeatures.DeferredReposEnabled()\n\trequired_repos := 1\n}\n")

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, relative, content):
        path = self.server / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def test_matches_identifier_spellings_within_window_only(self):
        matches = sr.code_matches(self.server, self.rollouts, "required_repos")
        self.assertEqual(
            [(m.path, m.line, m.function, m.rollout.name) for m in matches],
            [("logic/runs/plan.go", 4, "resolvePlan", "DeferredReposEnabled")],
        )

    def test_name_matches(self):
        self.assertEqual([r.name for r in sr.name_matches(self.rollouts, "deferred")][:1], ["DeferredReposEnabled"])


class TestMain(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.server = write_server(Path(self.tmp.name))
        (self.server / "logic").mkdir()
        (self.server / "logic" / "a.go").write_text(
            "func a() {\n\tif features.DeferredReposEnabled() {\n\t\trequiredRepos()\n\t}\n}\n", encoding="utf-8"
        )

    def tearDown(self):
        self.tmp.cleanup()

    def args(self, *rest):
        return ["--warp-server", str(self.server), *rest]

    def test_flag_exit_codes(self):
        self.assertEqual(run_main(self.args("flag", "shipped"))[0], 0)
        self.assertEqual(run_main(self.args("flag", "deferred_repos"))[0], 1)
        self.assertEqual(run_main(self.args("flag", "UnknownCallEnabled"))[0], 1)
        self.assertEqual(run_main(self.args("flag", "nope"))[0], 2)

    def test_check_blocks_on_staging_only_flag(self):
        code, out, _ = run_main(self.args("check", "required_repos"))
        self.assertEqual(code, 1)
        self.assertIn("logic/a.go:2 a() -> DeferredReposEnabled", out)
        self.assertIn("off in production", out)

    def test_check_passes_without_prod_off_flag(self):
        code, out, _ = run_main(self.args("check", "nothing_matches_this"))
        self.assertEqual(code, 0)
        self.assertIn("does not prove the surface shipped", out)

    def test_check_rejects_short_terms(self):
        self.assertEqual(run_main(self.args("check", "ab"))[0], 2)

    def test_staging_only_listing(self):
        code, out, _ = run_main(self.args("staging-only"))
        self.assertEqual(code, 0)
        self.assertIn("DeferredReposEnabled", out)
        self.assertNotIn("ShippedEnabled [", out)

    def test_missing_checkout_is_an_environment_error(self):
        code, _, err = run_main(["--warp-server", str(Path(self.tmp.name) / "absent"), "staging-only"])
        self.assertEqual(code, 2)
        self.assertIn("not found", err)


if __name__ == "__main__":
    unittest.main()
