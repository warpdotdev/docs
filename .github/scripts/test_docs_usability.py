"""Exercise orchestration boundaries, not the semantic quality of walkthroughs."""

import copy
import json
import os
import re
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import docs_usability as usability


REPO = "warpdotdev/docs"
HEAD = "a" * 40
BASE = "b" * 40
WORKFLOW = "c" * 40
ENV = {
    "GITHUB_REPOSITORY": REPO, "PR_NUMBER": "1090", "HEAD_SHA": HEAD,
    "GITHUB_WORKFLOW_SHA": WORKFLOW, "GITHUB_RUN_ID": "500",
    "GITHUB_RUN_ATTEMPT": "1", "GITHUB_EVENT_NAME": "pull_request_target",
}


class UsabilityTests(unittest.TestCase):
    def setUp(self):
        self.env = patch.dict(os.environ, ENV)
        self.env.start()
        self.addCleanup(self.env.stop)
        self.pr = {
            "number": 1090, "state": "open", "draft": False,
            "head": {"sha": HEAD, "repo": {"full_name": REPO}},
            "base": {"sha": BASE},
        }
        self.files = [{"filename": "src/content/docs/platform/index.mdx", "status": "modified"}]
        self.deployments = [{
            "id": 42, "sha": HEAD, "environment": "Preview",
            "creator": {"login": "vercel[bot]"},
        }]
        self.statuses = [{
            "state": "success", "environment_url": "https://docs-test.vercel.app",
        }]
        self.checks = []
        self.jobs = [{
            "name": "Evaluate PR 1090", "conclusion": "success",
            "steps": [{
                "name": "Run the reader journey, not fixture calibration",
                "conclusion": "success",
            }],
        }]
        self.posts = []
        self.api = patch.object(usability, "github", side_effect=self.github)
        self.api.start()
        self.addCleanup(self.api.stop)

    def github(self, path, *, data=None, paginate=False, items_key=None):
        if data is not None:
            self.assertEqual(path, f"repos/{REPO}/check-runs")
            self.posts.append(data)
            return {}
        if path == f"repos/{REPO}/pulls/1090":
            return copy.deepcopy(self.pr)
        if "/files?" in path:
            self.assertTrue(paginate)
            return copy.deepcopy(self.files)
        if "/deployments?" in path:
            self.assertIn(f"sha={HEAD}", path)
            return copy.deepcopy(self.deployments)
        if "/statuses?" in path:
            return copy.deepcopy(self.statuses)
        if "/check-runs?" in path:
            return {"check_runs": copy.deepcopy(self.checks)}
        if "/attempts/1/jobs?" in path:
            self.assertEqual(items_key, "jobs")
            return copy.deepcopy(self.jobs)
        if "/pulls?" in path:
            self.assertTrue(paginate)
            return [copy.deepcopy(self.pr)]
        self.fail(f"Unexpected API call: {path}")

    def prepare(self, has_key=True):
        return usability.prepare(REPO, 1090, HEAD, has_key)

    def artifact(self, directory, context=None, outcome="clear", agent_step="success"):
        context = context or self.prepare()
        (directory / "request.json").write_text(json.dumps(context))
        (directory / "execution.json").write_text(json.dumps({"agent_step": agent_step}))
        signal = {
            "head_sha": HEAD, "outcome": outcome,
            "report": "Synthetic transport input, not a real usability walkthrough.",
        }
        (directory / "agent-output.txt").write_text(
            "[USABILITY_RESULT]" + json.dumps(signal) + "[/USABILITY_RESULT]",
        )
        return context

    def publish(self, directory):
        return usability.publish(REPO, 1090, HEAD, directory)

    def test_human_pr_events_and_manual_retries_resolve_current_open_head(self):
        expected = [{"number": 1090, "head": HEAD}]
        self.assertEqual(usability.plan(
            {"pull_request": {"number": 1090}}, "pull_request_target", REPO,
        ), expected)
        self.assertEqual(usability.plan(
            {"inputs": {"pr": "1090"}}, "workflow_dispatch", REPO,
        ), expected)
        self.pr["state"] = "closed"
        self.assertEqual(usability.plan(
            {"inputs": {"pr": "1090"}}, "workflow_dispatch", REPO,
        ), [])
        with self.assertRaises(ValueError):
            usability.plan({"inputs": {"pr": "1090; exit 0"}}, "workflow_dispatch", REPO)

    def test_only_successful_preview_events_retry_associated_current_heads(self):
        event = {
            "deployment": self.deployments[0], "deployment_status": {"state": "success"},
        }
        self.assertEqual(usability.plan(event, "deployment_status", REPO),
                         [{"number": 1090, "head": HEAD}])
        self.pr["head"]["sha"] = "d" * 40
        self.assertEqual(usability.plan(event, "deployment_status", REPO), [])
        event["deployment_status"]["state"] = "failure"
        self.assertEqual(usability.plan(event, "deployment_status", REPO), [])

    def test_scope_includes_deleted_and_old_renamed_paths_and_rendering(self):
        self.assertEqual(usability.affected_paths([
            {"filename": "archive/old.md", "previous_filename": "src/content/docs/old.mdx"},
            {"filename": "src/content/docs/deleted.mdx", "status": "removed"},
            {"filename": "src/sidebar.ts"}, {"filename": "package-lock.json"},
            {"filename": "scripts/render.mjs"}, {"filename": ".agents/internal.md"},
        ]), [
            "package-lock.json", "scripts/render.mjs", "src/content/docs/deleted.mdx",
            "src/content/docs/old.mdx", "src/sidebar.ts",
        ])
        self.files = [{"filename": ".agents/internal.md"}]
        self.assertEqual(self.prepare()["decision"], "not_applicable")
        self.files *= 3000
        self.assertEqual(self.prepare()["decision"], "not_tested")

    def test_forks_drafts_stale_heads_and_missing_credentials_never_dispatch(self):
        for field, value, decision in (
            ("fork", "outside/docs", "not_tested"),
            ("draft", True, "not_tested"),
            ("head", "d" * 40, "superseded"),
            ("key", False, "not_tested"),
        ):
            with self.subTest(field=field):
                pr = copy.deepcopy(self.pr)
                if field == "fork":
                    self.pr["head"]["repo"]["full_name"] = value
                elif field == "draft":
                    self.pr["draft"] = value
                elif field == "head":
                    self.pr["head"]["sha"] = value
                self.assertEqual(self.prepare(field != "key")["decision"], decision)
                self.pr = pr

    def test_preview_requires_exact_head_vercel_producer_success_and_https_origin(self):
        self.assertEqual(self.prepare()["decision"], "run")
        for field, value in (
            ("sha", "d" * 40), ("environment", "Production"),
            ("creator", {"login": "contributor"}),
        ):
            with self.subTest(field=field):
                original = self.deployments[0][field]
                self.deployments[0][field] = value
                self.assertEqual(self.prepare()["decision"], "not_tested")
                self.deployments[0][field] = original
        for url in (
            "http://docs-test.vercel.app", "https://docs-test.vercel.app.evil.test",
            "https://user@docs-test.vercel.app", "https://docs.warp.dev",
        ):
            with self.subTest(url=url):
                self.statuses[0]["environment_url"] = url
                self.assertEqual(self.prepare()["decision"], "not_tested")
        self.statuses = [{"state": "pending"}]
        self.assertEqual(self.prepare()["decision"], "not_tested")

    def test_duplicate_reports_are_reused_but_manual_dispatch_retries(self):
        context = self.prepare()
        self.checks = [{
            "external_id": context["evaluation_key"],
            "output": {"title": "Walkthrough reported: clear"},
            "app": {"slug": "github-actions"}, "html_url": "https://github.com/check/1",
        }]
        self.assertEqual(self.prepare()["decision"], "duplicate")
        with patch.dict(os.environ, {"GITHUB_EVENT_NAME": "workflow_dispatch"}):
            self.assertEqual(self.prepare()["decision"], "run")
        self.checks[0]["output"]["title"] = "Not tested: evidence unavailable"
        self.assertEqual(self.prepare()["decision"], "run")

    def test_failed_malformed_or_wrong_head_output_is_not_tested(self):
        context = self.prepare()
        signal = {"head_sha": HEAD, "outcome": "clear", "report": "Synthetic record"}

        def wrapped(value):
            return "[USABILITY_RESULT]" + json.dumps(value) + "[/USABILITY_RESULT]"

        for output, execution in (
            (wrapped(signal), {"agent_step": "failure"}),
            (wrapped(signal), {"agent_step": "cancelled"}),
            (wrapped(signal), []),
            ("", {"agent_step": "success"}),
            (wrapped(signal) * 2, {"agent_step": "success"}),
            (wrapped({**signal, "head_sha": BASE}), {"agent_step": "success"}),
            (wrapped({**signal, "outcome": "pass"}), {"agent_step": "success"}),
            (wrapped({**signal, "report": ""}), {"agent_step": "success"}),
            (wrapped([]), {"agent_step": "success"}),
        ):
            with self.subTest(output=output, execution=execution):
                self.assertEqual(usability.reported_result(context, output, execution)[0],
                                 "not_tested")

    def test_reported_outcomes_remain_distinct_neutral_and_head_pinned(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            for outcome, title in (
                ("clear", "Walkthrough reported: clear"),
                ("findings", "Walkthrough reported: findings"),
                ("reduced_scope", "Reduced-scope checks reported"),
                ("not_tested", "Not tested: evidence or trusted execution unavailable"),
            ):
                with self.subTest(outcome=outcome):
                    self.artifact(directory, outcome=outcome)
                    self.publish(directory)
                    post = self.posts[-1]
                    self.assertEqual(post["head_sha"], HEAD)
                    self.assertEqual(post["conclusion"], "neutral")
                    self.assertEqual(post["output"]["title"], title)

    def test_missing_artifacts_and_changed_base_preview_or_trust_fail_closed(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            self.publish(directory)
            self.assertTrue(self.posts[-1]["output"]["title"].startswith("Not tested"))
            for field in ("base", "preview", "draft", "fork"):
                with self.subTest(field=field):
                    context = self.artifact(directory)
                    pr = copy.deepcopy(self.pr)
                    if field == "base":
                        self.pr["base"]["sha"] = "d" * 40
                    elif field == "preview":
                        context["preview"]["id"] = 99
                        (directory / "request.json").write_text(json.dumps(context))
                    elif field == "draft":
                        self.pr["draft"] = True
                    else:
                        self.pr["head"]["repo"]["full_name"] = "outside/docs"
                    self.publish(directory)
                    self.assertTrue(self.posts[-1]["output"]["title"].startswith("Not tested"))
                    self.pr = pr

    def test_stale_head_and_older_run_cannot_replace_current_evidence(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            self.artifact(directory)
            self.pr["head"]["sha"] = "d" * 40
            self.publish(directory)
            self.assertEqual(self.posts, [])
            self.pr["head"]["sha"] = HEAD
            self.checks = [{
                "details_url": f"https://github.com/{REPO}/actions/runs/501",
                "app": {"slug": "github-actions"},
            }]
            self.publish(directory)
            self.assertEqual(self.posts, [])

    def test_dispatch_failure_cannot_be_forged_by_artifact_execution_status(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            self.artifact(directory)
            self.jobs[0]["conclusion"] = "failure"
            self.publish(directory)
            self.assertTrue(self.posts[-1]["output"]["title"].startswith("Not tested"))
            self.jobs[0]["conclusion"] = "success"
            self.jobs[0]["steps"][0]["conclusion"] = "skipped"
            self.publish(directory)
            self.assertTrue(self.posts[-1]["output"]["title"].startswith("Not tested"))

    def test_publisher_recomputes_applicability_instead_of_trusting_artifact(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            context = self.prepare()
            context.update(decision="not_applicable", reason="Forged scope")
            self.artifact(directory, context)
            self.publish(directory)
            self.assertTrue(self.posts[-1]["output"]["title"].startswith("Not tested"))
            self.files = [{"filename": ".agents/internal.md"}]
            self.publish(directory)
            self.assertTrue(self.posts[-1]["output"]["title"].startswith("Not applicable"))

    def test_github_transport_passes_untrusted_data_as_json_stdin(self):
        data = {"report": "$(exit 1) `rm bogus`"}
        self.api.stop()
        with patch.object(usability.subprocess, "run") as run:
            run.return_value.stdout = "{}"
            usability.github(f"repos/{REPO}/check-runs", data=data)
            args, kwargs = run.call_args
            self.assertEqual(args[0][-4:], ["--method", "POST", "--input", "-"])
            self.assertEqual(json.loads(kwargs["input"]), data)
            self.assertNotIn("shell", kwargs)
            run.return_value.stdout = json.dumps([{"jobs": [self.jobs[0]]}, {"jobs": []}])
            self.assertEqual(usability.github("jobs", paginate=True, items_key="jobs"), self.jobs)
            self.assertIn("--slurp", run.call_args.args[0])

    def test_cli_preserves_the_actual_prompt_request_and_execution_artifacts(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            event = directory / "event.json"
            event.write_text(json.dumps({"pull_request": {"number": 1090}}))
            with patch.dict(os.environ, {
                "GITHUB_EVENT_PATH": str(event), "GITHUB_OUTPUT": str(directory / "outputs"),
                "GITHUB_STEP_SUMMARY": str(directory / "summary"),
                "WARP_KEY_AVAILABLE": "true",
            }):
                with patch.object(sys, "argv", ["docs_usability.py", "plan"]):
                    usability.main()
                with patch.object(sys, "argv", [
                    "docs_usability.py", "prepare", "--directory", str(directory),
                ]):
                    usability.main()
                evidence = directory / "evidence"
                context = json.loads((evidence / "request.json").read_text())
                self.assertEqual(context["decision"], "run")
                self.assertIn(HEAD, (evidence / "prompt.txt").read_text())
                self.assertIn("run<<", (directory / "outputs").read_text())
                self.artifact(evidence, context)
                with patch.dict(os.environ, {
                    "AGENT_OUTPUT": (evidence / "agent-output.txt").read_text(),
                    "AGENT_OUTCOME": "success",
                }), patch.object(sys, "argv", [
                    "docs_usability.py", "collect", "--directory", str(directory),
                ]):
                    usability.main()
                with patch.object(sys, "argv", [
                    "docs_usability.py", "publish", "--directory", str(evidence),
                ]):
                    usability.main()
                self.assertEqual(self.posts[-1]["head_sha"], HEAD)
                self.assertIn("Walkthrough reported: clear", (directory / "summary").read_text())

    def test_workflow_uses_trusted_code_and_separate_write_only_publisher(self):
        workflow = (usability.ROOT / ".github/workflows/docs-usability.yml").read_text()
        evaluator, publisher = workflow.split("\n  publish:\n")
        self.assertNotIn("checks: write", evaluator)
        self.assertNotIn("WARP_API_KEY", publisher)
        self.assertEqual(workflow.count("ref: ${{ github.workflow_sha }}"), 3)
        self.assertNotIn("head.ref", workflow)
        self.assertNotIn("warpy-factory", workflow)
        self.assertIn("b0c640eb560d1f2fc283244c582830aa16cefd8c", workflow)
        names = re.findall(r"name: (docs-usability-[^\n]+)", workflow)
        self.assertEqual(len(names), 2)
        self.assertEqual(names[0], names[1])
        self.assertIn("github.run_attempt", names[0])


if __name__ == "__main__":
    unittest.main()
