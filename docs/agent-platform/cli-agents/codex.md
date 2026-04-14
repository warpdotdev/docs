---
description: >-
  Set up Codex in Warp with notification support, rich input, code review,
  and more.
---

# Codex

Codex is OpenAI's open-source coding agent that runs in your terminal. It can write and edit code, execute commands, and navigate your codebase through natural language. For full documentation, see the [Codex GitHub repository](https://github.com/openai/codex).

Warp auto-detects Codex when you run it, giving you access to rich input controls, code review, and other integrated features.

## Getting started

1. Install Codex globally via npm:

   ```bash
   npm install -g @openai/codex
   ```

2. Launch Codex inside Warp:

   ```bash
   codex
   ```

   Warp detects the agent session and surfaces integrated controls automatically.

## Setting up notifications

Codex supports native notifications that Warp surfaces as in-app and desktop alerts — such as when Codex completes a task, encounters an error, or needs your input.

First, update Codex to the latest version — support for this setting was recently added. See the [Codex upgrade instructions](https://developers.openai.com/codex/cli#upgrade).

Then add the following to `~/.codex/config.toml`:

```toml
[tui]
notification_condition = "always"
```

Then restart Codex. If this config isn't set, Warp displays a setup chip in the terminal with instructions you can follow directly.

## Supported Warp features

Codex supports the full set of Warp's agent integration features:

* **Agent notifications** - Receive in-app and desktop alerts when Codex needs your attention. Requires a one-time config change (see [Setting up notifications](#setting-up-notifications)).
* **Rich input editor** - Press `Ctrl-G` to open an expanded input editor for composing longer prompts.
* **Code review** - Send inline review comments directly to the agent from Warp's code review panel.
* **Attach code as context** - Select code and send it to the agent as context.
* **Vertical tabs with agent metadata** - Monitor Codex sessions with status indicators in Warp's tab bar.
* **Tab Configs** - Save and restore Codex session configurations.
* **Remote Control** - Share your Codex session with teammates via session sharing.

## Related pages

* [Third-Party CLI Agents Overview](overview.md)
* [Claude Code](claude-code.md)
* [OpenCode](opencode.md)
