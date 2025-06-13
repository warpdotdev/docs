---
description: >-
  Agent Mode’s autonomy settings let you control when commands are auto-executed
  by configuring allowlists, denylists, and model-based safety checks.
---

# Agent Autonomy

Agent Mode supports configurable autonomous command execution under `Settings > AI > Autonomy`. You can customize this by:

1. Using a command allowlist to specify which commands can auto-execute
2. Using a command denylist to specify which commands require confirmation
3. Letting the Agent Mode model automatically determine if a command is safe to execute based on whether it's read-only

<figure><img src="../../.gitbook/assets/autonomy.gif" alt="Agent Mode connects to a docker container and checks for error logs with autonomy enabled."><figcaption><p>Agent Mode connects to a docker container and checks for error logs with autonomy enabled.</p></figcaption></figure>

### Command allowlist

Agent Mode comes with default allowlist entries for common read-only commands that can be automatically executed without user confirmation.

* `which .*` - Find executable locations
* `ls(\s.*)?` - List directory contents
* `grep(\s.*)?` - Search file contents
* `find .*` - Search for files
* `echo(\s.*)?` - Print text output

You can add your own regular expressions to this list in `Settings > AI > Autonomy > Command allowlist`. Commands in the allowlist will always auto-execute, even if they are not read-only operations.

{% hint style="info" %}
Mostly any commands are allowed to be auto-executed if they are on the allowlist, with the exception of any commands that contain redirection. e.g. `which warp 2>/dev/null`
{% endhint %}

### Command denylist

Agent Mode comes with default denylist entries for potentially risky commands that always require explicit user permission before execution. A couple of examples include:

* `wget(\s.*)?` - Network downloads
* `curl(\s.*)?` - Network requests
* `rm(\s.*)?` - File deletion
* `eval(\s.*)?` - Shell code execution

The denylist takes precedence over both the allowlist and model-based auto-execution. If a command matches the denylist, user permission will always be required, regardless of other settings. You can add your own regular expressions to this list in `Settings > AI > Autonomy > Command denylist`.

### Model based auto-execution

Agent Mode can dynamically analyze command safety for automatic execution of read-only commands. This provides intelligent command safety analysis but follows a strict precedence order.

1. Denylist (highest priority) - Commands always require confirmation
2. Allowlist - Commands always auto-execute
3. Model-based analysis (lowest priority) - Agent Mode determines if a command is read-only safe

This behavior can be toggled in `Settings > AI > Autonomy > Model-based auto-execution`.

### File read permissions for coding

When performing coding tasks, Agent Mode can automatically read files. This allows Agent Mode to analyze code without requiring explicit permission for each file access.

This behavior can be toggled in `Settings > AI > Autonomy > Coding read permissions`.

## Dispatch

_Dispatch_ is a form of Agent Mode that carries out complex tasks automatically. When you make a Dispatch query, the AI will:

1. Gather context about the task, using your [codebase](agent-autonomy.md#codebase-context), [requested commands](agent-autonomy.md#agent-mode-requested-commands), and followup questions.
2. Use a reasoning model to create a plan to carry out the task. You can refine the plan with AI, or edit it directly.
3. Automatically carry out the approved plan.

While Dispatch is executing a plan, it automatically runs commands and applies code changes. However, it will still obey your [command denylist](agent-autonomy.md#command-denylist). The border along the left of the session will change color to indicate that Dispatch is running autonomously:

<figure><img src="../../.gitbook/assets/agent-mode-dispatch-exchange.gif" alt="Scrolling through a completed Dispatch task"><figcaption><p>A completed Dispatch task</p></figcaption></figure>

{% hint style="warning" %}
Dispatch is currently in beta, with ongoing improvements that will expand its capabilities over time.
{% endhint %}

### How to enter Dispatch

You can enter Dispatch in a few ways:

{% tabs %}
{% tab title="macOS" %}
Press `CMD-SHIFT-I` to toggle between Dispatch and the terminal input, or to switch from pairing to Dispatch.
{% endtab %}

{% tab title="Windows" %}
Press `CTRL-SHIFT-I` to toggle between Dispatch and the terminal input, or to switch from pairing to Dispatch.
{% endtab %}

{% tab title="Linux" %}
Press `CTRL-SHIFT-I` to toggle between Dispatch and the terminal input, or to switch from pairing to Dispatch.
{% endtab %}
{% endtabs %}

<figure><img src="../../.gitbook/assets/interaction-type-menu.gif" alt="Prompt menu for switching between pairing and dispatch in Agent Mode"><figcaption><p>In addition, within Agent Mode, you can use the menu to switch between pairing and Dispatch</p></figcaption></figure>

If you're using the [Warp prompt](../../terminal/appearance/prompt.md), you can also click the Dispatch context chip:

<figure><img src="../../.gitbook/assets/agent-mode-dispatch-prompt.png" alt="The Dispatch and Pair prompt context chips"><figcaption><p>Context chips for entering Agent Mode</p></figcaption></figure>
