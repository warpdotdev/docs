---
description: >-
  Common architectures for deploying cloud agents, including CLI-only,
  Oz-hosted, and self-hosted execution patterns.
---

# Deployment Patterns

Teams adopt cloud agents in a few repeatable ways. This page outlines the most common architectures, what they're good for, and how they fit together.

#### Quick mental model

Oz cloud agent setups usually have four moving parts:

1. **Trigger**: something happens (CI step, webhook, cron, Slack mention).
2. **Orchestration**: something decides what to run and tracks it (Oz orchestrator, GitHub Actions, your internal system).
3. **Execution**: where the agent actually runs (your runner, Oz-hosted environment, or self-hosted workers).
4. **Visibility**: how the team monitors and intervenes (Oz dashboard, session sharing, APIs).

***

### Pattern 1: CLI-only agents (bring your own orchestrator)

Use this when you already have a system that schedules work (CI, dev boxes, internal orchestrators), and you just need a reliable, cloud-connected agent runner.

#### What it looks like

* **Trigger**: GitHub Actions / CI, a script, a dev box action, or an internal orchestrator
* **Orchestration**: your existing system
* **Execution**: wherever that system runs
* **Warp adds**: cloud connectivity, shared context, visibility, session sharing, and tracking

#### Why teams choose it

* You want a **drop-in replacement** for other CLI/SDK-based agents (Claude Code, Codex CLI, Gemini CLI/SDK-style flows).
* You want to run agents anywhere without requiring Warp desktop.
* You still want **team-level observability** even when execution is “outside Warp.”

#### Common examples

* **CI PR helper**: run formatting checks, generate review comments, suggest fixes, open PRs.
* **Remote dev box agent**: run refactors or debugging tasks inside a pre-provisioned box.
* **Internal orchestrator integration**: treat Warp as one agent option alongside other model providers.

#### What you still get even without Warp orchestration

* Access to your shared Warp context (for example MCP config, Warp Drive context, rules/prompts).
* Agent Session Sharing to monitor/steer runs.
* Read-only APIs for tracking and reporting.
* A path to “handoff” workflows (where a run can be continued or inspected in richer surfaces).

#### Minimal setup checklist

* A Warp team
* A service account (recommended for automation)
* The Oz CLI installed on the runner / box
* Any needed credentials (often via secrets + environment variables)

***

### Pattern 2: Oz-hosted agents + Oz orchestration (managed cloud execution)

Use this when you want Oz to run agent workloads on Warp-managed infrastructure, typically inside reproducible Docker environments, with built-in lifecycle management.

<figure><img src="../.gitbook/assets/cloud-agents-infra.png" alt="Warp enterprise SaaS architecture showing customer infrastructure, isolated tenant sandboxes, Warp backend, and LLM providers"><figcaption></figcaption></figure>

#### What it looks like

* **Trigger**: first-party integrations, cron schedules, API/SDK calls, or on-demand commands
* **Orchestration**: Oz orchestrator
* **Execution**: Oz-hosted environments (Docker-based)
* **Visibility**: Oz dashboard + session sharing + APIs/SDKs

#### Why teams choose it

* You want the simplest path to reproducible, scalable cloud execution.
* You want to run many tasks in parallel without building your own sandboxing and scaling layer.
* You want a consistent “production” setup with standardized environments and centralized configuration.

#### Common ways to trigger

* **First-party integrations (Slack, Linear, etc.)** that create tasks automatically from external events.
* **Scheduled agents** for recurring work (cron-like automation).
* **Custom triggers** from your own systems using Warp’s API/SDK.
* **On-demand cloud jobs** using CLI commands like oz agent run-cloud.

#### Example recipe: daily dead-code cleanup

1. Define an Oz Environment with the repo + toolchain.
2. Create a schedule with a fixed prompt for cleanup.
3. Oz runs the agent on the cadence.
4. Your team monitors runs in the Oz dashboard, reviews artifacts (PRs, plans), and intervenes when needed.

#### Example recipe: crash triage via Sentry webhook

1. Define an Oz Environment with the target repo.
2. Register a Sentry webhook to your handler (server, cloud function, Zapier/n8n).
3. Handler extracts crash details, constructs a prompt, and calls the Oz orchestrator API/SDK to start a task.
4. Warp spins up the run in the environment and you monitor progress via UI/API.

#### Example recipe: fan-out parallel work (sharding)

If a task is naturally divisible:

* Launch multiple cloud agents via oz agent run-cloud, each with:
  * A shard of the repo (directory/module ownership)
  * A shard of the prompt (one responsibility)
* Aggregate results (PRs, notes, plans) in whatever system you prefer.

#### Example recipe: same task across multiple models

* Launch N runs with the same prompt, but different profiles that map to different models.
* Compare results and choose the best output (or merge).

***

### Pattern 3: Self-hosted execution

Use this when you need to control where agent execution happens while still using Oz orchestration and visibility. Repositories are cloned and stored only on your infrastructure. Orchestration metadata, session transcripts, and LLM inference route through Warp's backend under [ZDR](https://docs.warp.dev/enterprise/security-and-compliance/security-overview#zero-data-retention-zdr).

{% hint style="info" %}
**Enterprise feature**: Self-hosted execution is available exclusively to teams on an Enterprise plan.
{% endhint %}

Self-hosting supports two deployment modes:

* **Managed** — Run the `oz-agent-worker` daemon. Oz orchestrates agents remotely, starting them in isolated Docker containers, Kubernetes Jobs, or directly on the host. Works like a [GitHub self-hosted runner](https://docs.github.com/en/actions/hosting-your-own-runners).
* **Unmanaged** — Use `oz agent run` in your existing CI, Kubernetes, or dev environment. You control orchestration; Warp provides tracking.

#### Managed architecture

* **Trigger**: integrations (Slack, Linear), schedules, CLI (`oz agent run-cloud`), API/SDK
* **Orchestration**: Oz orchestrator
* **Execution**: your infrastructure, running the `oz-agent-worker` daemon with Docker, Kubernetes, or the Direct backend
* **Visibility**: same Oz dashboard, session sharing, and APIs as Oz-hosted

#### Unmanaged architecture

* **Trigger**: your existing system (CI, Kubernetes, scripts, internal orchestrators)
* **Orchestration**: your system
* **Execution**: anywhere `oz agent run` can execute (Linux, macOS, Windows)
* **Visibility**: tracked sessions, session sharing, and APIs

#### Why teams choose it

* You need code and execution to stay within your network boundary.
* You have compliance or security requirements that prevent using Warp-hosted compute.
* You need agents to access services behind a VPN or self-hosted SCMs like GitLab or Bitbucket. Warp-hosted agents can also access GitLab and Bitbucket repositories over the public internet — see the [GitLab](integrations/gitlab.md) and [Bitbucket](integrations/bitbucket.md) setup guides.
* You have complex environments (multi-service stacks, heavy resource requirements) that don't fit in a single Docker container.
* You want to use your own infrastructure while still benefiting from Oz orchestration and observability.

#### How it works

**Managed:** You run a worker daemon on your infrastructure that connects to Oz. When you create a task with `--host "your-worker-id"`, Oz routes it to your worker, which runs it in an isolated Docker container, Kubernetes Job, or directly on the host depending on the configured backend.

**Unmanaged:** You run `oz agent run` in your CI pipeline, Kubernetes pod, VM, or dev box. The agent runs directly on the host and reports its session back to Warp for tracking and observability.

In both modes, your team gets the same observability (Oz dashboard, session sharing, APIs) as Oz-hosted runs.

For setup instructions and a decision guide, see [Self-Hosting](self-hosting.md).
