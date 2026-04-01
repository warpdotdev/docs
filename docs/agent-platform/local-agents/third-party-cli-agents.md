---
description: >-
  Warp provides an integrated utility bar for third-party CLI coding agents
  like Claude Code, Codex, and Gemini CLI, with built-in voice, image, and
  code review support.
---

# Third-Party CLI Agents

Warp can show an agent utility bar when you’re working with third-party CLI coding agents. It provides integrated controls for images, voice, files, and diffs, giving those agents first-class support directly in Warp.

{% embed url="https://youtu.be/5InYfCq0u_k" %}
Third-Party CLI Agents in Warp
{% endembed %}

This includes:

* Built-in [Voice](interacting-with-agents/voice.md) transcription.
* An easy way to [attach images as context](agent-context/images-as-context.md) to your prompt
* Browse files in the [Code Editor](https://docs.warp.dev/code/code-editor/) and review code changes directly in the [Code Review](https://docs.warp.dev/code/code-review/) panel.

Note: when Warp detects an agent session, the utility bar appears automatically.

### Supported CLI agents

Warp currently supports:

* Claude Code
* OpenAI Codex (CLI)
* Amp
* Gemini CLI
* Droid
* OpenCode

{% hint style="info" %}
If you’re using one of these and don’t see the utility bar, make sure you’re on the latest Warp version and that the command is being run inside Warp (not an external terminal).
{% endhint %}
