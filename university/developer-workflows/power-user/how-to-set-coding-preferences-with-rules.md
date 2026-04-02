---
description: >-
  Set persistent environment and tool preferences with Rules so Warp's agents
  always use your preferred setup.
metaLinks:
  alternates:
    - >-
      https://app.gitbook.com/s/c5dAwvMCRiTxUOdDicqy/developer-workflows/power-user/how-to-set-coding-preferences-with-rules
---

# How To: Set Coding Preferences with Rules

Learn how to use Warp’s Rules feature to define your personal environment and tool preferences for every coding session.

{% embed url="https://youtu.be/zWvRB2zWr-4?si=tv-TIhsqEtLG9iDs" %}

This tutorial teaches you how to customize your development setup using **Warp’s Rules** — ensuring the AI agent always works in your preferred environment. Instead of constantly reminding it which package manager or environment to use, you can **store those preferences as persistent Rules** that apply automatically across projects.

{% stepper %}
{% step %}
#### The Problem

When using AI tools to write or modify code, they often default to outdated or undesired tools.\
For example, many agents still use **npm** instead of **pnpm** — or **pip** instead of **miniconda**.

Warp fixes this by letting you define your preferences once, and then applying them automatically whenever your agent runs commands.
{% endstep %}

{% step %}
#### The Rule Setup

You can set Rules for how you want the AI to handle environments, dependencies, and commands.

**Example Rule**

{% code title="Example Rule" %}
```
Rule: Environment Preferences
- Always use pnpm for Node.js projects unless the project already uses npm.
- Default to miniconda for Python environments.
- Use the Tauri CLI when building desktop apps.
```
{% endcode %}

This ensures the agent automatically chooses the right package manager or environment — no extra prompts required.
{% endstep %}

{% step %}
#### Supported Use Cases

You can apply Rules to:

* Package managers (e.g., npm → pnpm)
* Environment tools (e.g., virtualenv → miniconda)
* Framework defaults (e.g., Next.js over React)
* CLI utilities or custom build tools
{% endstep %}
{% endstepper %}
