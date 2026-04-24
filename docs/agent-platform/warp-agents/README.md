---
description: >-
  Powerful AI features like agents, code review, voice, and active AI
  recommendations, fully integrated into the Warp Agentic Development Environment.
---

# Warp Agents overview

## AI in Warp

Warp includes Oz agents—intelligent agents designed to help you build, test, deploy, and debug while keeping you in control. Interactive Oz agent conversations in Warp can look up commands, execute tasks, fix bugs, and adapt to your workflows. You can manage agent behavior directly, with full context from your Warp Drive and your team.

{% hint style="info" %}
Warp's AI features can be globally disabled in **Settings** > **Agents** > **Oz** with the AI toggle.\
\
These features send input data to various LLM providers through their API. Warp is **SOC 2 compliant** and has **Zero Data Retention** policies with all contracted LLM providers -- no customer AI data is retained, stored, or used for training. Read more about data privacy for Warp features [on our privacy page](https://www.warp.dev/privacy).
{% endhint %}

## What you can do with agents

This section covers how to interact with Warp's agents and the capabilities available during agent conversations:

* [Interacting with Agents](interacting-with-agents/README.md) - Manage AI conversations tied to sessions, attach context, continue previous threads, or start new ones.
* [Agent Context](agent-context/README.md) - Attach images, URLs, files, code blocks, and selections as context for your prompts.
* [Model Choice](./model-choice.md) - Pick your preferred LLM from a curated set of top models, or let Warp choose the optimal one.
* [Full Terminal Use](./full-terminal-use.md) - Let the agent drive interactive terminal apps, seeing live output and running commands.
* [Interactive Code Review](interactive-code-review.md) - Review agent-generated diffs, leave inline comments, and have the agent address your feedback.
* [Task Lists](./task-lists.md) - Track complex workflows with automatic task lists that update progress in real time.
* [Web Search](./web-search.md) - Allow agents to search the web for up-to-date information.
* [Third-Party CLI Agents](../cli-agents/overview.md) - Run third-party CLI agents like Claude Code and Codex with Warp's built-in agent toolbelt.
* [Active AI Recommendations](active-ai.md) - Get proactive fix recommendations based on errors and outputs.
* [Voice](interacting-with-agents/voice.md) - Talk to Warp's agent using voice commands.

For foundational capabilities like planning, rules, MCP servers, and agent profiles, see [Capabilities](capabilities-overview.md).
