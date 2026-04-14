---
description: >-
  Run background agents in the cloud from events, schedules, or integrations
  with team-wide observability.
---

# Cloud Agents Overview

Oz Cloud Agents are **cloud-connected**, **background agents** that run on the [Oz Platform](platform.md).

**New to cloud agents?** Start with the [Cloud Agents Quick Start](quickstart.md) to run your first cloud agent in ~10 minutes.

{% embed url="https://youtu.be/poLkJhO7fdo" %}

### What cloud agents are designed for

Cloud agents are designed for situations where:

* **You need agents to react to system events.**
  * Examples include crashes, bug reports, Slack interactions, cron timers, or CI steps.
* **You want observability into agent activity across a team or system.**
  * This includes being able to see what ran, when it ran, and what it did.
* **You need more parallelism than local execution typically allows.**
  * For example, running many agent tasks concurrently in the cloud, sharding a repo-wide task into multiple runs, or fanning out the same task across multiple targets.
* **You want agents to operate continuously as part of engineering infrastructure.**
  * This includes scheduled maintenance tasks and integration-driven automation.

<figure><img src="../.gitbook/assets/oz-use-cases.png" alt="Oz use cases across the development lifecycle: Plan, Prototype, Build, Validate, Review + Merge, Deploy + Monitor"><figcaption></figcaption></figure>

***

### What is a cloud agent run?

A cloud agent run is represented as an agent task. A task is created when a trigger fires (for example a webhook event or schedule) or when a user starts a run explicitly.

Each task includes:

* **Inputs**: a prompt, and often additional context from the triggering system (for example a Slack message, PR metadata, or CI logs).
* **Execution context (optional)**: an [Environment](environments.md) that defines the repo, image, and startup commands the agent should run with.
* **Lifecycle state**: created → running → completed / failed.
* **Persistent record**: status, metadata, and a session transcript that can be reviewed after the task completes.

{% hint style="info" %}
If you are evaluating whether something should be a cloud agent, a good test is whether you can define:\
(1) what triggers it, (2) what context it needs, and (3) how the team will inspect or validate the output.
{% endhint %}

### How cloud agents work

Cloud agents run on the [Oz Platform](platform.md), which provides the primitives for triggering work, orchestrating tasks, executing agents (optionally in environments), injecting secrets, and inspecting results.

* Something **triggers** an agent task.
* The **orchestrator creates** and tracks the task.
* The agent **executes** on a host, optionally inside an [environment](environments.md), with whatever [secrets](secrets.md) and credentials it needs.

The exact way tasks are triggered and executed depends on your deployment model (for example CLI-only, Warp-hosted orchestration, or self-hosted execution). Those options are covered in the [Deployment Patterns](deployment-patterns.md) pages.

For teams that need execution to stay within their network boundary, self-hosting supports two architectures: a **managed** worker daemon that lets Oz orchestrate agents in Docker containers on your machines, and an **unmanaged** mode where you run `oz agent run` directly in your CI, Kubernetes, or dev environment. See [Self-Hosting](self-hosting.md) for details.

### What you get by default

Because cloud agents run on the [Oz Platform](platform.md), each run is tracked and produces a persistent record that can be observed, shared, and audited (even if execution happens outside the Warp app).

#### Codebase Context

Cloud agent runs automatically benefit from [Codebase Context](../warp-agents/codebase-context.md) for semantic code understanding and search, as long as Codebase Context is enabled for your account. See [Codebase Context in cloud agent runs](../warp-agents/codebase-context.md#codebase-context-in-cloud-agent-runs) for details.

#### Observability and steerability

Cloud agent tasks are designed to be inspectable by the team:

* [Agent Session Sharing](../warp-agents/session-sharing.md) lets authorized teammates attach to a running task to monitor progress and, where supported, steer the agent while it runs.
* Each run produces a session transcript and task metadata, which provides a record of what the agent did.
* A [management experience](managing-cloud-agents.md) surfaces task status and history.

#### Centralized configuration

Cloud agent workflows often rely on shared configuration such as [MCP servers](mcp.md), rules, saved prompts, environment variables, and [secrets](secrets.md).

Warp supports centralized configuration so the same workflow behaves consistently across triggers (for example Slack + CI + schedules), without duplicating setup in every system.

For details on configuring MCP servers for cloud agents, see [MCP Servers](mcp.md).

#### API access to tasks

The Oz Platform exposes task visibility via the [**Oz API and SDKs**](https://docs.warp.dev/reference/api-and-sdk), so teams can:

* Query which tasks are running or have run.
* Fetch task metadata and outcomes.
* Build internal dashboards or monitoring (for example success rates, runtime, failure reasons).

### Using cloud agents with or without the Warp app

Cloud agents do not require the Warp desktop app. Teams can deploy and operate them through the [Oz Platform](platform.md) using:

* [Oz CLI](https://docs.warp.dev/reference/cli) — run agents from scripts, CI, or the terminal
* [Oz web app](oz-web-app.md) — visual interface for managing runs, schedules, environments, and integrations (works on mobile)
* [Agent Session Sharing](../warp-agents/session-sharing.md) — attach to running tasks to monitor or steer
* [Agent Management UX](managing-cloud-agents.md) — view agent activity and run history
* [APIs and SDKs](https://docs.warp.dev/reference/api-and-sdk) — programmatic access for custom integrations

If your team also uses Warp's terminal, you get an additional workflow: tasks launched via the CLI can be handed off into an interactive session for review, edits, or continuation.

***

### Billing and plan requirements

Cloud agents and [integrations](integrations/README.md) run on the [Oz Platform](platform.md) control plane, and usage is billed using credits.

{% hint style="info" %}
[Bring Your Own Key (BYOK)](https://docs.warp.dev/support-and-community/plans-and-billing/bring-your-own-api-key) is not supported for cloud agent runs. BYOK keys are stored locally on your device and are not accessible to cloud-hosted agents. All cloud agent runs consume Warp credits.
{% endhint %}

#### For Cloud Agents via CLI/API

Individual users can run cloud agents without being on a team. Requirements:

* You need at least 20 credits (any type: normal Warp credits, [Cloud Agent Credits](https://docs.warp.dev/support-and-community/plans-and-billing/credits#cloud-agent-credits), or Build plan credits)
* Cloud agents run on Warp-hosted infrastructure
* Self-hosted agents require a team subscription

#### For Integrations (Slack/Linear)

Integrations require you to be part of a [Warp team](https://docs.warp.dev/knowledge-and-collaboration/teams) and additional requirements:

* **Plan requirements**
  * **Supported plans**: Build, Max, Business
  * Not supported: Pro, Turbo, Lightspeed, legacy Business
  * Your plan must support add-on credits.
* **Credit requirements**
  * Your team must have at least 20 credits available (any type of Warp credits work) to run cloud agents and integrations.
  * Usage is billed based on credit type and team configuration.
  * Normal credits, [Cloud Agent Credits](https://docs.warp.dev/support-and-community/plans-and-billing/credits#cloud-agent-credits), and [add-on credits](https://docs.warp.dev/support-and-community/plans-and-billing/add-on-credits) all work.

For more details, please refer to: [Access, Billing, and Identity Permissions](team-access-billing-and-identity.md)

{% hint style="warning" %}
If your credit balance reaches zero, cloud agent runs will not be able to execute until credits are replenished.
{% endhint %}

***

### Learn more

* [Cloud Agents Quick Start](quickstart.md) — run your first cloud agent with an environment in ~10 minutes.
* [Oz Platform](platform.md) — CLI, Oz API/SDK, orchestration, tasks, environments, hosts, integrations, and more.
* [Skills as Agents](skills-as-agents.md) — run agents based on reusable skill definitions from the CLI, web app, API, or on a schedule.
* [Oz CLI](https://docs.warp.dev/reference/cli) — shows how to run Oz agents in non-interactive mode from CI, scripts, or remote machines, including auth and common commands.
* [Environments](environments.md) — explains how environments provide the runtime context (repo, image, startup commands) for agent tasks.
* [Oz API and SDK](https://docs.warp.dev/reference/api-and-sdk) — documents the REST API for creating, querying, and monitoring agent tasks programmatically.
* [Agent Secrets](secrets.md) — covers how to store, scope, and inject credentials into agent runs safely.
* [MCP Servers](mcp.md) — how to configure MCP servers for agent tool access and how MCP configuration is applied across runs.
* [Deployment Patterns](deployment-patterns.md) (beta) — compares common ways to deploy cloud agents and when to use each.
* [Access, Billing, and Identity Permissions](team-access-billing-and-identity.md) — explains individual and team-level requirements, credit billing behavior, and the permission model for who can run, view, and steer cloud agent tasks.
