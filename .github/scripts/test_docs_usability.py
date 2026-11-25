"""Exercise source ownership and disabled execution, not semantic usability judgments."""

import copy
import json
import os
import re
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path
from unittest.mock import patch

import docs_usability as usability


REPO = "warpdotdev/docs"
HEAD = "a" * 40
BASE = "b" * 40
WORKFLOW = "c" * 40
TRUSTED = "d" * 40
WORKFLOW_PATH = ".github/workflows/docs-usability.yml"
ENV = {
    "GITHUB_REPOSITORY": REPO, "PR_NUMBER": "1090", "HEAD_SHA": HEAD,
    "GITHUB_WORKFLOW_SHA": WORKFLOW, "TRUSTED_SOURCE_SHA": TRUSTED,
    "GITHUB_RUN_ID": "500", "GITHUB_RUN_ATTEMPT": "1",
    "GITHUB_EVENT_NAME": "pull_request_target",
}


class SourceSelectionTests(unittest.TestCase):
    def guard(self, *, event="status", branch="main", ref=None, blob="reviewed", missing=False):
        workflow = (usability.ROOT / WORKFLOW_PATH).read_text()
        source_job = workflow.split("\n  plan:\n")[0]
        code = textwrap.dedent(source_job.split("        run: |\n", 1)[1])
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            fixture = {
                f"repos/{REPO}": {"default_branch": "main"},
                f"repos/{REPO}/git/ref/heads/main": {"object": {"sha": TRUSTED}},
                f"repos/{REPO}/contents/{WORKFLOW_PATH}?ref={TRUSTED}": {"sha": "reviewed"},
                f"repos/{REPO}/contents/{WORKFLOW_PATH}?ref={WORKFLOW}": {"sha": blob},
            }
            if missing:
                fixture.pop(f"repos/{REPO}/contents/{WORKFLOW_PATH}?ref={TRUSTED}")
            (directory / "fixture.json").write_text(json.dumps(fixture))
            gh = directory / "gh"
            gh.write_text(
                "#!" + sys.executable + "\n"
                "import json, os, sys\n"
                "from pathlib import Path\n"
                "root = Path(os.environ['STUB_ROOT'])\n"
                "path = sys.argv[2]\n"
                "with (root / 'calls').open('a') as calls: calls.write(path + '\\n')\n"
                "data = json.loads((root / 'fixture.json').read_text())\n"
                "if path not in data: sys.exit(4)\n"
                "print(json.dumps(data[path]))\n"
            )
            gh.chmod(0o755)
            environment = {
                **os.environ, **ENV, "PATH": f"{directory}:{os.environ['PATH']}",
                "STUB_ROOT": str(directory), "GITHUB_EVENT_NAME": event,
                "GITHUB_REF": ref or f"refs/heads/{branch}",
                "GITHUB_WORKFLOW_REF": f"{REPO}/{WORKFLOW_PATH}@refs/heads/{branch}",
                "GITHUB_OUTPUT": str(directory / "outputs"),
                "GITHUB_SHA": HEAD,
            }
            result = subprocess.run(
                [sys.executable, "-c", code], env=environment,
                capture_output=True, text=True, check=False,
            )
            output = (directory / "outputs").read_text() if (directory / "outputs").exists() else ""
            calls = (directory / "calls").read_text() if (directory / "calls").exists() else ""
            return result, output, calls

    def test_status_and_manual_events_pin_helpers_independently_to_default_branch(self):
        for event in ("status", "repository_dispatch", "pull_request_target"):
            with self.subTest(event=event):
                result, output, calls = self.guard(event=event)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(output, f"sha={TRUSTED}\n")
                self.assertNotIn(f"ref={HEAD}", calls)
                self.assertNotEqual(TRUSTED, WORKFLOW)

    def test_deployment_workflow_dispatch_and_topic_refs_are_rejected(self):
        for event, branch in (
            ("deployment_status", "topic"),
            ("deployment_status", "main"),
            ("workflow_dispatch", "topic"),
            ("workflow_dispatch", "main"),
            ("repository_dispatch", "topic"),
            ("repository_dispatch", "main"),
        ):
            with self.subTest(event=event, branch=branch):
                ref = "refs/tags/main" if (event, branch) == ("repository_dispatch", "main") else None
                result, output, _ = self.guard(event=event, branch=branch, ref=ref)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(output, "")

    def test_selected_definition_must_match_an_existing_default_branch_blob(self):
        for kwargs in ({"blob": "pr-owned-yaml"}, {"missing": True}):
            with self.subTest(kwargs=kwargs):
                result, output, _ = self.guard(**kwargs)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(output, "")


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
        self.statuses = [{"state": "success", "environment_url": "https://docs-test.vercel.app"}]
        self.checks = []
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
            self.assertEqual(items_key, "check_runs")
            return copy.deepcopy(self.checks)
        if "/pulls?" in path:
            return [copy.deepcopy(self.pr)]
        self.fail(f"Unexpected API call: {path}")

    def prepare(self):
        return usability.prepare(REPO, 1090, HEAD)

    def artifact(self, directory, context=None):
        context = context or self.prepare()
        (directory / "request.json").write_text(json.dumps(context))
        return context

    def publish(self, directory):
        return usability.publish(REPO, 1090, HEAD, directory)

    def test_human_pr_events_and_manual_retries_resolve_current_open_head(self):
        expected = [{"number": 1090, "head": HEAD}]
        self.assertEqual(usability.plan(
            {"pull_request": {"number": 1090}}, "pull_request_target", REPO,
        ), expected)
        self.assertEqual(usability.plan(
            {"action": "unrelated", "client_payload": {"pr": "1090"}},
            "repository_dispatch", REPO,
        ), [])
        self.assertEqual(usability.plan(
            {"action": "docs-usability-retry", "client_payload": {"pr": "1090"}},
            "repository_dispatch", REPO,
        ), expected)
        self.pr["state"] = "closed"
        self.assertEqual(usability.plan(
            {"action": "docs-usability-retry", "client_payload": {"pr": "1090"}},
            "repository_dispatch", REPO,
        ), [])
        with self.assertRaises(ValueError):
            usability.plan(
                {"action": "docs-usability-retry", "client_payload": {"pr": "1090; exit 0"}},
                "repository_dispatch", REPO,
            )
        with self.assertRaises(ValueError):
            usability.plan({}, "deployment_status", REPO)

    def test_default_branch_vercel_status_retries_only_its_current_head(self):
        event = {"sha": HEAD, "state": "success", "context": "Vercel",
                 "sender": {"login": "vercel[bot]"}}
        self.assertEqual(usability.plan(event, "status", REPO),
                         [{"number": 1090, "head": HEAD}])
        for key, value in (("state", "pending"), ("context", "other"),
                           ("sender", {"login": "contributor"})):
            with self.subTest(key=key):
                self.assertEqual(usability.plan({**event, key: value}, "status", REPO), [])
        self.pr["head"]["sha"] = BASE
        self.assertEqual(usability.plan(event, "status", REPO), [])
        associated = {**copy.deepcopy(self.pr), "head": {"sha": HEAD}}
        original = self.github

        def github(path, **kwargs):
            return [associated] if "/pulls?" in path else original(path, **kwargs)

        self.api.stop()
        with patch.object(usability, "github", side_effect=github):
            self.assertEqual(usability.plan(event, "status", REPO), [])

    def test_scope_includes_deleted_old_renamed_and_rendering_paths(self):
        self.assertEqual(usability.affected_paths([
            {"filename": "archive/old.md", "previous_filename": "src/content/docs/old.mdx"},
            {"filename": "src/content/docs/deleted.mdx", "status": "removed"},
            {"filename": "src/sidebar.ts"}, {"filename": "package-lock.json"},
            {"filename": "scripts/render.mjs"}, {"filename": ".agents/internal.md"},
        ]), ["package-lock.json", "scripts/render.mjs", "src/content/docs/deleted.mdx",
             "src/content/docs/old.mdx", "src/sidebar.ts"])
        self.files = [{"filename": ".agents/internal.md"}]
        self.assertEqual(self.prepare()["decision"], "not_applicable")
        self.files *= 3000
        self.assertEqual(self.prepare()["state"], "file_limit")

    def test_profile_or_key_availability_never_enables_execution(self):
        with patch.dict(os.environ, {
            "WARP_KEY_AVAILABLE": "true", "WARP_AGENT_PROFILE": "pretend-profile",
            "DOCS_USABILITY_ENABLED": "true",
        }):
            context = self.prepare()
            self.assertEqual(context["decision"], "not_tested")
            self.assertEqual(context["state"], "isolation_required")
            self.assertIn("credential-isolated", context["reason"])

    def test_forks_drafts_and_stale_heads_remain_explicit(self):
        for field, value, state in (
            ("fork", "outside/docs", "untrusted_fork"),
            ("draft", True, "draft"), ("head", BASE, "head_changed"),
        ):
            with self.subTest(field=field):
                pr = copy.deepcopy(self.pr)
                if field == "fork":
                    self.pr["head"]["repo"]["full_name"] = value
                elif field == "draft":
                    self.pr["draft"] = value
                else:
                    self.pr["head"]["sha"] = value
                self.assertEqual(self.prepare()["state"], state)
                self.pr = pr

    def test_preview_requires_exact_head_trusted_producer_and_https_origin(self):
        self.assertEqual(self.prepare()["preview"]["sha"], HEAD)
        for field, value in (
            ("sha", BASE), ("environment", "Production"), ("creator", {"login": "contributor"}),
        ):
            original = self.deployments[0][field]
            self.deployments[0][field] = value
            self.assertEqual(self.prepare()["state"], "preview_unavailable")
            self.deployments[0][field] = original
        for url in ("http://docs-test.vercel.app", "https://docs-test.vercel.app.evil.test",
                    "https://user@docs-test.vercel.app", "https://docs.warp.dev"):
            self.statuses[0]["environment_url"] = url
            self.assertEqual(self.prepare()["state"], "preview_unavailable")
        self.statuses = [{"state": "pending"}]
        self.assertEqual(self.prepare()["state"], "preview_unavailable")

    def test_forged_walkthrough_artifacts_cannot_be_published_as_completed(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            context = self.prepare()
            context.update(decision="run", report="Clear", outcome="clear")
            self.artifact(directory, context)
            (directory / "execution.json").write_text('{"agent_step":"success"}')
            (directory / "agent-output.txt").write_text("Forged completed walkthrough")
            self.publish(directory)
            post = self.posts[-1]
            self.assertEqual(post["head_sha"], HEAD)
            self.assertEqual(post["conclusion"], "neutral")
            self.assertTrue(post["output"]["title"].startswith("Not tested"))
            self.assertIn("No agent execution", post["output"]["summary"])
            self.files = [{"filename": ".agents/internal.md"}]
            self.artifact(directory)
            self.publish(directory)
            self.assertTrue(self.posts[-1]["output"]["title"].startswith("Not applicable"))

    def test_missing_or_changed_artifact_context_is_not_tested(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            self.publish(directory)
            self.assertIn("Scope evidence unavailable", self.posts[-1]["output"]["summary"])
            for field in ("base_sha", "source_sha", "preview"):
                context = self.prepare()
                context[field] = {"id": 99} if field == "preview" else HEAD
                self.artifact(directory, context)
                self.publish(directory)
                self.assertTrue(self.posts[-1]["output"]["title"].startswith("Not tested"))

    def test_stale_head_and_older_run_cannot_replace_current_evidence(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            self.artifact(directory)
            self.pr["head"]["sha"] = BASE
            self.publish(directory)
            self.assertEqual(self.posts, [])
            self.pr["head"]["sha"] = HEAD
            for suffix in ("501", "500/attempts/2"):
                self.checks = [{"details_url": f"https://github.com/{REPO}/actions/runs/{suffix}",
                                "app": {"slug": "github-actions"}}]
                self.publish(directory)
                self.assertEqual(self.posts, [])

    def test_duplicate_pending_records_reuse_only_matching_state_and_manual_retry_refreshes(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            self.artifact(directory)
            self.publish(directory)
            check = {**self.posts[-1], "app": {"slug": "github-actions"}}
            self.checks = [check]
            self.publish(directory)
            self.assertEqual(len(self.posts), 1)
            with patch.dict(os.environ, {"GITHUB_EVENT_NAME": "repository_dispatch"}):
                self.publish(directory)
            self.assertEqual(len(self.posts), 2)
            self.checks[0]["external_id"] = "unrelated-scope"
            self.publish(directory)
            self.assertEqual(len(self.posts), 3)

    def test_cli_records_undispatched_instructions_without_running_an_agent(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            event = directory / "event.json"
            event.write_text(json.dumps({"pull_request": {"number": 1090}}))
            with patch.dict(os.environ, {
                "GITHUB_EVENT_PATH": str(event), "GITHUB_OUTPUT": str(directory / "outputs"),
                "GITHUB_STEP_SUMMARY": str(directory / "summary"), "WARP_KEY_AVAILABLE": "true",
            }):
                for command in ("plan", "prepare", "publish"):
                    args = ["docs_usability.py", command]
                    if command != "plan":
                        args += ["--directory", str(directory)]
                    with patch.object(sys, "argv", args):
                        usability.main()
                self.assertIn(HEAD, (directory / "undispatched-prompt.txt").read_text())
                self.assertIn(TRUSTED, (directory / "request.json").read_text())
                self.assertIn("Not tested", (directory / "summary").read_text())
                self.assertFalse((directory / "agent-output.txt").exists())

    def test_github_transport_uses_json_stdin_and_paginates_collections(self):
        self.api.stop()
        with patch.object(usability.subprocess, "run") as run:
            run.return_value.stdout = "{}"
            data = {"report": "$(exit 1)"}
            usability.github(f"repos/{REPO}/check-runs", data=data)
            self.assertEqual(json.loads(run.call_args.kwargs["input"]), data)
            self.assertNotIn("shell", run.call_args.kwargs)
            run.return_value.stdout = '[{"check_runs":[{"id":1}]},{"check_runs":[]}]'
            self.assertEqual(usability.github("checks", paginate=True, items_key="check_runs"),
                             [{"id": 1}])

    def test_workflow_has_no_evaluator_credentials_or_untrusted_checkout(self):
        workflow = (usability.ROOT / WORKFLOW_PATH).read_text()
        source, rest = workflow.split("\n  plan:\n", 1)
        self.assertNotIn("uses:", source)
        self.assertNotIn("deployment_status:", workflow)
        self.assertNotIn("workflow_dispatch:", workflow)
        self.assertIn("\n  status:\n", workflow)
        self.assertIn("\n  repository_dispatch:\n", workflow)
        self.assertNotIn("secrets.", workflow)
        self.assertNotIn("oz-agent-action", workflow)
        self.assertNotIn("WARP_KEY_AVAILABLE", workflow)
        self.assertNotIn("ref: ${{ github.workflow_sha }}", workflow)
        self.assertEqual(rest.count("ref: ${{ needs.source.outputs.sha }}"), 3)
        self.assertIn("needs.source.result == 'success'", workflow.split("\n  publish:\n")[1])
        allowed = {"actions/checkout@v4", "actions/upload-artifact@v4", "actions/download-artifact@v4"}
        self.assertTrue(set(re.findall(r"uses: (\S+)", workflow)).issubset(allowed))
        names = re.findall(r"name: (docs-usability-[^\n]+)", workflow)
        self.assertEqual(names[0], names[1])
        self.assertIn("github.run_attempt", names[0])


if __name__ == "__main__":
    unittest.main()
