---
description: >
  Warp's Oz agents are capable collaborators that help you write code, debug
  issues, and complete terminal workflows, all from natural language prompts.
---

# Agents in Warp

Warp includes Oz agents. These coding agents are designed to help you build, test, deploy, and debug while keeping you in control. Describe what you want to do in natural language (_you can even use your voice_), and Oz will take action using your environment, codebase, and saved context.

## What Oz agents can do

Oz agents understand your codebase and can execute tasks autonomously while keeping you in control:

* **Write and edit code** - Create new files, refactor existing code, or make changes across multiple files in your codebase
* **Debug and fix errors** - Analyze stack traces, interpret error output, and apply fixes
* **Run commands** - Execute shell commands and use the output to guide next steps
* **Recover from errors** - Automatically retry failed operations with adjustments
* **Learn tools** - Integrate with any CLI tool by reading its `--help` or public documentation
* **Use your context** - Leverage [Warp Drive](https://docs.warp.dev/knowledge-and-collaboration/warp-drive), [MCP servers](../capabilities/mcp.md), [Rules](../capabilities/rules.md), and [codebase indexing](../capabilities/codebase-context.md) for tailored responses

**Try this prompt** — [_open in Warp_](https://app.warp.dev/drive/prompt/Clone-and-install-Warps-themes-repository-PkK9Zw16SCD3JKzOUoGuj4)

{% code overflow="wrap" %}
```markup
Detect my current operating system. Based on that, navigate to the appropriate Warp themes directory (e.g. ~/.warp/ on macOS). 

Then, clone the official Warp themes repository using SSH (git@github.com:warpdotdev/themes.git) into that directory, following the structure and instructions provided in the repo's README. If SSH does not work, try HTTPS (https://github.com/warpdotdev/themes.git) or via the GitHub CLI (gh repo clone warpdotdev/themes).
```
{% endcode %}

***

## Agent autonomy

Under `Settings > AI > Agents > Permissions`, you can control how much autonomy the agent has when performing different types of actions:

* Reading files
* Creating plans
* Executing commands
* Calling MCP servers

For each action, set the autonomy level to:

* **Let the agent decide** - The agent chooses when to ask for confirmation
* **Always prompt for confirmation** - Require approval before each action
* **Always allow** - Execute without prompting
* **Never** - Disable this action entirely

You can also configure an **allowlist** and **denylist** for specific commands you always want to run—either with or without confirmation.

***

## Agent profiles

Profiles let you define different permission and model configurations for different contexts. Create and manage profiles in `Settings > AI`, then switch between them by clicking the profile icon in Warp's input area.

Common profile patterns:

* **Default** - Balanced permissions for everyday use
* **YOLO mode** - Loose permissions for personal projects where you want the agent to move fast
* **Prod mode** - Restrictive permissions ("Always Ask") for high-risk environments like production servers

For more details, see [Agent Profiles & Permissions](../capabilities/agent-profiles-permissions.md).

***

## Managing agents

You can run multiple Oz agents simultaneously in Warp. All active agents—both local conversations and cloud agent runs—are tracked in the [management view](../cloud-agents/managing-cloud-agents.md).

Agents notify you when they need input, such as permission to run a command or approval to apply a code diff. This lets you focus on other work, knowing you'll be alerted when your attention is required.

To access conversations across devices, share them with teammates, or restore past conversations, enable [cloud-synced conversations](../local-agents/cloud-conversations.md).

***

## Context and knowledge

Oz agents work best when they understand your codebase and workflows. Warp provides several ways to give agents the context they need:

* [**Codebase Context**](../capabilities/codebase-context.md) - Warp indexes your Git-tracked files so agents can search and understand your code
* [**Rules**](../capabilities/rules.md) - Define global and project-level guidelines that shape agent behavior
* [**Skills**](../capabilities/skills.md) - Reusable instructions that teach agents how to perform specific tasks
* [**MCP Servers**](../capabilities/mcp.md) - Connect external tools and data sources (GitHub, Linear, databases) to your agents
* [**Warp Drive**](https://docs.warp.dev/knowledge-and-collaboration/warp-drive) - Save prompts, workflows, and notebooks that agents can reference

***

## From local to cloud

The same Oz agent capabilities that power interactive conversations in Warp also run in the cloud. Cloud agents can:

* React to events from Slack, Linear, or GitHub
* Run on schedules for recurring tasks like dependency updates
* Execute in parallel across repos or tasks
* Produce tracked, auditable, shareable runs

Cloud agents are ideal for work that doesn't need your immediate attention—PR reviews, issue triage, routine maintenance, and integration-driven workflows.

→ [Learn about Cloud Agents](../cloud-agents/overview.md)

***

## Resources

* [**Oz web app**](https://oz.warp.dev) - Create runs, manage schedules, browse skills, and configure integrations
* [**Local Agents Overview**](../local-agents/overview.md) - Detailed guide to working with agents in Warp
* [**Capabilities**](../capabilities/README.md) - All agent capabilities: planning, task lists, model choice, and more
* [**Oz CLI**](https://docs.warp.dev/reference/cli) - Run agents from the command line
* [**Oz Agent API & SDK**](https://docs.warp.dev/reference/api-and-sdk/agent) - Programmatic access to agent runs
