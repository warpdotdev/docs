---
description: >-
  Warp's agents are capable collaborators that help you write code, debug
  issues, and complete terminal workflows -- all from natural language prompts.
---

# Agents in Warp

Describe what you want to do (_you can even use your voice_), and Warp’s agents will intelligently take action using your environment, codebase, and saved context to tailor their responses.

**Agents can:**

1. Write and edit code across single or multiple files.
2. Fix errors based on output or stack traces.
3. Execute shell commands and use the output to guide next steps
4. Automatically recover from common errors and retry with adjustments.
5. Learn and integrate with any tool that offers public docs or `--help`.
6. Leverage your saved [Warp Drive](https://docs.warp.dev/knowledge-and-collaboration/warp-drive) contents, [MCP servers](https://docs.warp.dev/knowledge-and-collaboration/mcp), and [Rules](https://docs.warp.dev/knowledge-and-collaboration/rules) to provide tailored responses.

**Give this prompt a try —** [_open the below Prompt in Warp_](https://app.warp.dev/drive/prompt/Clone-and-install-Warps-themes-repository-PkK9Zw16SCD3JKzOUoGuj4)

{% code overflow="wrap" %}
```markup
Detect my current operating system. Based on that, navigate to the appropriate Warp themes directory (e.g. ~/.warp/ on macOS). 

Then, clone the official Warp themes repository using SSH (git@github.com:warpdotdev/themes.git) into that directory, following the structure and instructions provided in the repo’s README. If SSH does not work, try HTTPS (https://github.com/warpdotdev/themes.git) or via the GitHub CLI (gh repo clone warpdotdev/themes).
```
{% endcode %}

### Agent Autonomy

Under `Settings > AI > Agents > Permissions`, you can control how much autonomy the agent has when performing different types of actions, such as:

* Reading files
* Creating plans
* Executing commands
* Calling MCP servers, and more

For each action, you can set the autonomy level to one of the following:

* Let the agent decide
* Always prompt for confirmation
* Always allow
* Never

You can also configure an **allowlist** and **denylist** for specific commands you always want to run—either with or without confirmation.

### Agent Profiles

Define profiles in `Settings > AI` with unique permissions and model choices. You can switch profiles at any time by clicking the "profile" icon in Warp's input area. In addition to your default permissions, you may create:

* YOLO mode: Loose permissions for using in personal projects
* Prod mode: Limit AI permissions to "Always Ask" when in high-risk environments like your production server

### Managing multiple agents

You can run multiple agents in Warp simultaneously, monitor their status, and step in when needed—without losing track of what’s happening across your sessions. Each tab includes a [status icon](https://docs.warp.dev/agents/using-agents/managing-agents#agent-status-indicators) that shows the agent’s current state. All of your active agents are tracked in the [Agent Management Panel](https://docs.warp.dev/agents/using-agents/managing-agents#agent-management-panel), located in the top-right corner next to your avatar.

Agents will also [notify](https://docs.warp.dev/agents/using-agents/managing-agents#agent-status-indicators) you when they need input, such as permission to run a command or approval to apply a code diff. This lets you focus on other work, knowing you’ll be alerted when your attention is required.
