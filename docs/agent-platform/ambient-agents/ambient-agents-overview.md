---
description: >-
  Warp Ambient Agents are cloud connected background agents that run from
  events, schedules, or integrations, giving teams scalable automation with
  shared observability and centralized configs (beta)
---

# Ambient Agents Overview

{% hint style="info" %}
**Beta**: Ambient Agents are currently in beta. APIs, CLI commands, and product behavior may change. If you have feedback, reach out in the [Warp Community Slack](https://go.warp.dev/join-preview).
{% endhint %}

Warp's Ambient Agents are **cloud connected**, **background agents** built on the [Warp Platform](../platform/warp-platform.md). They run automatically in response to system events, schedules, or integrations.

{% embed url="https://www.youtube.com/watch?v=V-8_fZExlFQ" %}

### What Ambient Agents are designed for

Ambient Agents are designed for situations where:

* **You need agents to react to system events.**
  * Examples include crashes, bug reports, Slack interactions, cron timers, or CI steps.
* **You want observability into agent activity across a team or system.**
  * This includes being able to see what ran, when it ran, and what it did.
* **You need more parallelism than local execution typically allows.**
  * For example, running many agent tasks concurrently in the cloud, sharding a repo-wide task into multiple runs, or fanning out the same task across multiple targets.
* **You want agents to operate continuously as part of engineering infrastructure.**
  * This includes scheduled maintenance tasks and integration-driven automation.

***

### What is an Ambient Agent run?

An Ambient Agent run is represented as an agent task. A task is created when a trigger fires (for example a webhook event or schedule) or when a user starts a run explicitly.

Each task includes:

* **Inputs**: a prompt, and often additional context from the triggering system (for example a Slack message, PR metadata, or CI logs).
* **Execution context (optional)**: an [Environment](https://docs.warp.dev/reference/cli/integrations-and-environments#what-is-an-environment) that defines the repo, image, and startup commands the agent should run with.
* **Lifecycle state**: created → running → completed / failed.
* **Persistent record**: status, metadata, and a session transcript that can be reviewed after the task completes.

{% hint style="info" %}
If you are evaluating whether something should be an Ambient Agent, a good test is whether you can define:\
(1) what triggers it, (2) what context it needs, and (3) how the team will inspect or validate the output.
{% endhint %}

### How Ambient Agents work

Ambient Agents run on the [Warp Platform](../platform/warp-platform.md), which provides the primitives for triggering work, orchestrating tasks, executing agents (optionally in Environments), injecting secrets, and inspecting results.

* Something **triggers** an agent task.
* The **orchestrator creates** and tracks the task.
* The agent **executes** on a host, optionally inside an [environment](https://docs.warp.dev/reference/cli/integrations-and-environments#what-is-an-environment), with whatever [secrets](agent-secrets.md) and credentials it needs.
The exact way tasks are triggered and executed depends on your deployment model (for example CLI-only, Warp-hosted orchestration, or self-hosted execution). Those options are covered in the [Deployment Patterns](../platform/deployment-patterns.md) pages.

### What you get by default

Because Ambient Agents run on the [Warp Platform](../platform/warp-platform.md), each run is tracked and produces a persistent record that can be observed, shared, and audited (even if execution happens outside the Warp app).

#### Observability and steerability

Ambient Agent tasks are designed to be inspectable by the team:

* [Agent Session Sharing](https://docs.warp.dev/knowledge-and-collaboration/session-sharing/ambient-agents-session-sharing) lets authorized teammates attach to a running task to monitor progress and, where supported, steer the agent while it runs.
* Each run produces a session transcript and task metadata, which provides a record of what the agent did.
* A [management experience](managing-ambient-agents/) surfaces task status and history.

#### Centralized configuration

Ambient Agent workflows often rely on shared configuration such as [MCP servers](mcp-servers-for-agents.md), rules, saved prompts, environment variables, and [secrets](agent-secrets.md).

Warp supports centralized configuration so the same workflow behaves consistently across triggers (for example Slack + CI + schedules), without duplicating setup in every system.

#### API access to tasks

The Warp Platform exposes task visibility via the [**Agent API and SDKs**](https://docs.warp.dev/reference/api-and-sdk/README), so teams can…

* Query which tasks are running or have run.
* Fetch task metadata and outcomes.
* Build internal dashboards or monitoring (for example success rates, runtime, failure reasons).

### Using Ambient Agents with or without Warp’s app

Ambient Agents do not require the Warp desktop app. Teams can deploy and operate them through the [Warp Platform](../platform/warp-platform.md) using:

* [Warp CLI](https://docs.warp.dev/reference/cli/README)
* Web surfaces (where available)
* [Agent Session Sharing](https://docs.warp.dev/knowledge-and-collaboration/session-sharing/agent-session-sharing)
* [Agent Management UX](../agent/using-agents/managing-agents.md
* Admin settings and [APIs](https://docs.warp.dev/reference/api-and-sdk/README)
If your team also uses Warp’s terminal, you get an additional workflow: tasks launched via the CLI can be handed off into an interactive session for review, edits, or continuation.

***

### Team and billing requirements

Ambient Agents and [integrations](../integrations/integrations-overview.md) run on the [Warp Platform](../platform/warp-platform.md) control plane, and usage is billed using AI credits.

To run **integrations (and most Ambient Agent automation)**, your team must meet the following requirements:

* **Plan requirements**
  * **Supported plans**: Build, Business
  * Not supported: Pro, Turbo, Lightspeed, legacy Business
  * Your plan must support add-on credits.
* **Credit requirements**
* Your team must have at least 20 [add-on credits](https://docs.warp.dev/support-and-community/plans-and-billing/add-on-credits) available to run an integration.
  * Integration usage is billed to the team’s add-on credit balance.
  * Ambient Agents and integrations do not draw from personal monthly base credits.

For more details, please refer to: [Team Access Billing And Identity Permissions](../platform/team-access-billing-and-identity-permissions.md)

{% hint style="warning" %}
If the team’s add-on credit balance reaches zero, integrations and Ambient Agent runs that require add-on credits will not be able to execute until credits are replenished.
{% endhint %}

***

### Learn more

* [Warp Platform](../platform/warp-platform.md) — CLI, Agent API/SDK, orchestration, tasks, environments, hosts, integrations, and more.
* [Warp CLI](https://docs.warp.dev/reference/cli/README) — shows how to run Warp's agent in non-interactive mode from CI, scripts, or remote machines, including auth and common commands.
* [Integrations and Environments](https://docs.warp.dev/reference/cli/integrations-and-environments) — explains how triggers (Slack/Linear/webhooks/schedules) create agent tasks and how environments provide the runtime context (repo, image, startup commands).
* [Agent API and SDK](https://docs.warp.dev/reference/api-and-sdk/README) — documents the REST API for creating, querying, and monitoring agent tasks programmatically.
* [Agent Secrets](agent-secrets.md) — covers how to store, scope, and inject credentials into agent runs safely.
* [MCP Servers for Agents](mcp-servers-for-agents.md) — describes how to configure MCP servers for agent tool access and how MCP configuration is applied across runs.
* [Deployment Patterns](../platform/deployment-patterns.md) (beta) — compares common ways to deploy Ambient Agents and when to use each.
* [Team Access Billing And Identity Permissions](../platform/team-access-billing-and-identity-permissions.md) — explains team-level requirements, credit billing behavior, and the permission model for who can run, view, and steer Ambient Agent tasks.
