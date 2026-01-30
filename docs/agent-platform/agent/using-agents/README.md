---
description: >-
  Agents in Warp let you collaborate with AI in natural language to run terminal
  and coding workflows, manage context, and break complex tasks into clear,
  actionable steps.
---

# Using Agents

## Agents in Warp

Agents in Warp let you go beyond manual commands by collaborating with AI directly inside the [Agentic Development Environment](https://www.warp.dev/blog/reimagining-coding-agentic-development-environment). You can describe a task in natural language, and the Agent will translate it into runnable commands, manage context, and break complex requests into clear steps.

Agents are designed to work alongside you. They never act without visibility, and you remain in control of their autonomy and permissions.

**Key concepts related to Agents include:**

* Agent Mode — run terminal or coding workflows with natural language.
* [Conversations](agent-conversations/) — group queries and blocks for a specific task.
* [Context](agent-context/) — attach and manage information to improve responses.
* [Task Lists](agent-tasklists.md) — break complex requests into clear, trackable steps.
* [Agent Management](managing-agents.md) — monitor, configure, and control active agents.
* [Profiles and Permissions](agent-profiles-permissions.md) — customize autonomy, tools, and behavior.

{% hint style="info" %}
To make sure you can fully use Agents, confirm that the global AI toggle is enabled under `Settings > AI`.
{% endhint %}

## What is Agent Mode?

Agent Mode is the primary way to interact with Warp's Agent. It lets you run terminal or coding workflows by typing plain English instead of shell commands or IDE operations. When you enter a request, Warp uses leading LLMs to interpret it, suggest or run the right commands, surface code diffs when applicable, and stream results directly into your session, all tailored to your environment and setup.\
\
**Agent Mode can:**

1. Understand natural language input, not just command syntax.
2. Execute commands and use their output to guide the next step.
3. Correct itself when it encounters mistakes or errors occur.
4. Learn and integrate with any service that has public docs or `--help`.
5. Leverage saved workflows, project context, and other guidelines to improve accuracy.

### Entering Agent Mode

Agent Mode is how you interact directly with Warp’s AI to ask questions, run tasks, and collaborate in natural language. There are multiple ways to enter Agent Mode depending on where you are in your workflow:

{% tabs %}
{% tab title="macOS" %}
* Type natural language directly: If auto-detection is enabled, you can type a task or question into the input, and Warp will recognize it as natural language using its local auto-detection feature.
* Use keyboard shortcuts: Quickly toggle into Agent Mode with `CMD + I`.
* Attach blocks to a prompt: From any block you want to use as context, click the ✨ icon in the toolbelt or select Attach block(s) to AI query from the block’s context menu.
{% endtab %}

{% tab title="Windows" %}
* Type natural language directly: If auto-detection is enabled, you can type a task or question into the input, and Warp will recognize it as natural language using its local auto-detection feature.
* Use keyboard shortcuts: Quickly toggle into Agent Mode with `CTRL + I`.
* Attach blocks to a prompt: From any block you want to use as context, click the ✨ icon in the toolbelt or select Attach block(s) to AI query from the block’s context menu.
{% endtab %}

{% tab title="Linux" %}
* Type natural language directly: If auto-detection is enabled, you can type a task or question into the input, and Warp will recognize it as natural language using its local auto-detection feature.
* Use keyboard shortcuts: Quickly toggle into Agent Mode with `CTRL + I`.
* Attach blocks to a prompt: From any block you want to use as context, click the ✨ icon in the toolbelt or select Attach block(s) to AI query from the block’s context menu.
{% endtab %}
{% endtabs %}

When you're in Agent Mode, the **Agent icon** will be highlighted in the [Universal Input](https://docs.warp.dev/terminal/universal-input/).

<figure><img src="../../.gitbook/assets/using-agents-universal-input.png" alt=""><figcaption><p>The Agent icon in the Universal input indicates that Agent Mode is active.</p></figcaption></figure>

In Classic Input, you’ll also see a ✨ sparkles indicator inline.&#x20;

<figure><img src="../../.gitbook/assets/undo_my_git_commit.png" alt="The sparkles on the command line indicate Agent Mode is active."><figcaption><p>The sparkles in the Classic input indicates that Agent Mode is active.</p></figcaption></figure>

By default, entering Agent Mode starts you in _Pair Mode_, where you can continue an ongoing conversation by asking follow-up questions or assigning tasks. From here, you can ask the agent to build, debug, fix, or even deploy code as needed.

### Models Powering Agent Mode

Agent Mode is backed by a curated selection of leading large language models (LLMs). By default, Warp uses **Claude 4 Sonnet** for "auto", balancing speed and quality.&#x20;

However, you can switch to other supported models at any time based on your needs—for example, choosing a faster model for quick iterations or a more advanced model for complex reasoning.

For the full list of available models and guidance on when to use each, see [Model Choice](model-choice.md).

### Demo: Starting a Coding Task with Warp

Here's an example from [Warp University](https://www.warp.dev/university), where Zach demonstrates a quick fix using Warp’s Agents to code:

{% embed url="https://www.youtube.com/watch?v=IuFSuOYstfg" %}
