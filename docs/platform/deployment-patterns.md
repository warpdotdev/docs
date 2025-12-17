# Deployment Patterns

Teams adopt Ambient Agents in a few repeatable ways. This page outlines the most common architectures, what they’re good for, and how they fit together.

#### Quick mental model

Ambient Agent systems usually have four moving parts:

1. **Trigger**: something happens (CI step, webhook, cron, Slack mention).
2. **Orchestration**: something decides what to run and tracks it (Warp Orchestrator, GitHub Actions, your internal system).
3. **Execution**: where the agent actually runs (your runner, Warp-hosted environment, eventually self-hosted workers).
4. **Visibility**: how the team monitors and intervenes (management UI, session sharing, APIs).

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
* The Warp CLI installed on the runner / box
* Any needed credentials (often via secrets + environment variables)

***

### Pattern 2: Warp-hosted agents + Warp orchestration (managed cloud execution)

Use this when you want Warp to run agent workloads on Warp-managed infrastructure, typically inside reproducible Docker environments, with built-in lifecycle management.

#### What it looks like

* **Trigger**: first-party integrations, cron schedules, API/SDK calls, or on-demand commands
* **Orchestration**: Warp Orchestrator
* **Execution**: Warp-hosted environments (Docker-based)
* **Visibility**: management UI + session sharing + APIs/SDKs

#### Why teams choose it

* You want the simplest path to reproducible, scalable cloud execution.
* You want to run many tasks in parallel without building your own sandboxing and scaling layer.
* You want a consistent “production” setup with standardized environments and centralized configuration.

#### Common ways to trigger

* **First-party integrations (Slack, Linear, etc.)** that create tasks automatically from external events.
* **Scheduled agents** for recurring work (cron-like automation).
* **Custom triggers** from your own systems using Warp’s API/SDK.
* **On-demand cloud jobs** using CLI commands like warp agent run-ambient.

#### Example recipe: Daily dead-code cleanup

1. Define a Warp Environment with the repo + toolchain.
2. Create a schedule with a fixed prompt for cleanup.
3. Warp runs the agent on the cadence.
4. Your team monitors runs in the management UI, reviews artifacts (PRs, plans), and intervenes when needed.
5. Define a Warp Environment with the target repo.
6. Register a Sentry webhook to your handler (server, cloud function, Zapier/n8n).
7. Handler extracts crash details, constructs a prompt, and calls Warp’s Orchestrator API/SDK to start a task.
8. Warp spins up the run in the environment and you monitor progress via UI/API.

#### Example recipe: Fan-out parallel work (sharding)

If a task is naturally divisible:

* Launch multiple cloud agents via warp agent run-ambient, each with:
  * A shard of the repo (directory/module ownership)
  * A shard of the prompt (one responsibility)
* Aggregate results (PRs, notes, plans) in whatever system you prefer.

#### Example recipe: Same task across multiple models

* Launch N runs with the same prompt, but different profiles that map to different models.
* Compare results and choose the best output (or merge).

***

### Pattern 3: Self-hosted execution (coming soon)

Use this when you need execution and code to remain inside your network boundary, but still want Warp’s orchestration and visibility model.

#### Intended model

* Warp Orchestrator still manages lifecycle and observability.
* Execution happens on customer-managed infrastructure.
