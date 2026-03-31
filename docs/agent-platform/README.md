---
description: >
  Oz is the orchestration platform for cloud agents, powering both
  interactive and autonomous agents for development workflows.
---

# Agents Overview

Warp includes **Oz**, the orchestration platform for cloud agents. While Warp provides the terminal and coding surface you work in day-to-day, Oz is the underlying orchestration layer that makes running agents at scale possible.

With Oz, you can:

* Run interactive agent conversations in Warp for real-time coding assistance
* Deploy autonomous agents that run in the cloud from triggers, schedules, or integrations
* Coordinate multiple agents concurrently across machines, repos, and teams
* Track, audit, and share agent activity with full visibility into what ran and what it did

Oz is fully programmable—launch agents manually or build custom logic around them with triggers, schedules, environments, and your choice of hosting (Warp's cloud or your own).

***

## Key capabilities

* [**Local Agents**](local-agents/overview.md) - Interactive Oz agents embedded in Warp. Use natural language to write code, debug issues, run commands, and automate development tasks with full terminal access.
* [**Oz Cloud Agents**](cloud-agents/overview.md) - Autonomous Oz agents that run in the background in response to system events, schedules, or integrations.
* [**Integrations**](cloud-agents/integrations/README.md) - Connect external system events to autonomous agent execution. Use [Slack](cloud-agents/integrations/slack.md), [Linear](cloud-agents/integrations/linear.md), [GitHub Actions](cloud-agents/integrations/github-actions.md), and other integrations to trigger agents in the cloud.
* [**Oz Platform**](cloud-agents/platform.md) - The underlying infrastructure that powers Oz, including the CLI, API/SDK, orchestration layer, environments, secrets, and management/observability.

***

## Getting started

* [**Agents in Warp**](getting-started/agents-in-warp.md) - Start using Oz agents interactively in Warp
* [**Oz web app**](https://oz.warp.dev) - Create runs, manage schedules, browse skills, and configure integrations
* [**Oz CLI**](https://docs.warp.dev/reference/cli) - Run agents from the command line, in CI, or on remote machines
* [**Oz API & SDK**](https://docs.warp.dev/reference/api-and-sdk/agent) - Programmatically create and monitor agent runs

***

## Learn more

* [Local Agents Overview](local-agents/overview.md) - Interactive agents in Warp
* [Cloud Agents Overview](cloud-agents/overview.md) - Background agents for automation at scale
* [Agent Capabilities](capabilities/README.md) - Skills, planning, MCP, rules, and more
* [Oz Platform](cloud-agents/platform.md) - CLI, API/SDK, orchestration, environments, and hosts
* [Environments](cloud-agents/environments.md) - Configure execution context for cloud agents
* [Integrations](cloud-agents/integrations/README.md) - Slack, Linear, GitHub Actions, and custom integrations
* [Skills as Agents](cloud-agents/skills-as-agents.md) - Run agents from reusable skill definitions
* [Managing Cloud Agents](cloud-agents/managing-cloud-agents.md) - Monitor and manage agent activity
