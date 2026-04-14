---
description: >-
  Agents use your Warp Drive content—Workflows, Notebooks, Rules, MCP Servers,
  and Environment Variables—for context-aware responses.
---

# Agent Mode Context

[Agent Mode](https://docs.warp.dev/agent-platform/warp-agents/interacting-with-agents) can leverage your [Warp Drive](./) contents to tailor responses to your personal and team developer workflows and environments.

## Objects used as context

Agents can automatically pull in relevant context from:

* **Workflows** - Saved commands and scripts
* **Notebooks** - Documentation and notes
* **Environment Variables** - Configuration values
* **Rules** - Guidelines that shape agent behavior (see [Rules](https://docs.warp.dev/agent-platform/warp-agents/rules))
* **MCP Servers** - External tools and data sources (see [MCP](https://docs.warp.dev/agent-platform/warp-agents/mcp))

When a Warp Drive object is pulled as context, it will be displayed in the conversation as a citation under "References" or "Derived from".

## Settings

Enabled by default, this can be toggled in **Settings** > **AI** > **Knowledge** > **Warp Drive as Agent Mode Context**.

## Related

* [AI-Integrated Objects](ai-objects.md) - Overview of all AI-related objects in Warp Drive
