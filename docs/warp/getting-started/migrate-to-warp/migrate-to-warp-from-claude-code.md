---
description: >-
  Keep using Claude Code in Warp — with rich input, code review, and
  notifications — or switch from Claude Code to Warp's Agent Mode as your
  primary coding agent.
---

# Migrate to Warp from Claude Code

Claude Code is different from the other sources in this section: it's not a terminal emulator, it's a CLI agent that runs inside any terminal. Warp is an agentic development environment with a built-in [code editor](../../code/code-editor/README.md), [Code Review](../../code/code-review.md), [team collaboration](../../knowledge-and-collaboration/warp-drive/README.md), and [MCP](https://docs.warp.dev/agent-platform/warp-agents/mcp) support — so you have two paths to choose from:

* **[Using Claude Code inside Warp](#using-claude-code-inside-warp)** - you want to keep using Claude Code as your coding agent and run it in Warp's terminal.
* **[Switching to Agent Mode from Claude Code](#switching-to-agent-mode-from-claude-code)** - you want to replace Claude Code with Warp's built-in [Agent Mode](https://docs.warp.dev/agent-platform/warp-agents).

## Using Claude Code inside Warp

Warp provides first-class support for Claude Code through its [third-party CLI agents](https://docs.warp.dev/agent-platform/cli-agents) integration. Open a new tab and run:

```bash
claude
```

Warp auto-detects Claude Code and unlocks IDE-level features on top of the TUI:

* **[Rich input editor](https://docs.warp.dev/agent-platform/cli-agents/rich-input)** (`Ctrl+G`) - compose multi-line prompts with `@` mentions, voice input, and slash commands.
* **[Agent notifications](https://docs.warp.dev/agent-platform/warp-agents/agent-notifications)** - in-app and desktop alerts when Claude Code needs your input. Requires a one-time plugin install (Warp prompts you).
* **Inline code review** - send review comments directly to the agent from Warp's [Code Review](../../code/code-review.md) panel.
* **[Vertical tabs with agent metadata](../../terminal/windows/vertical-tabs.md)** - track multiple Claude Code sessions across tabs with status indicators.
* **[Remote control](https://docs.warp.dev/agent-platform/cli-agents/remote-control)** - share or steer a Claude Code session from another device.
* **[Tab Configs](../../terminal/windows/tab-configs.md)** - save and reopen Claude Code session layouts.

For full setup steps (notification plugin, productivity tips, troubleshooting), see [Claude Code in Warp](https://docs.warp.dev/agent-platform/cli-agents/claude-code) and the [How to set up Claude Code](https://docs.warp.dev/guides/integrations/how-to-set-up-claude-code) guide.

### Tips

* **Run Claude Code in [terminal mode](https://docs.warp.dev/agent-platform/warp-agents/interacting-with-agents/terminal-and-agent-modes)**, not Agent Mode. Press `⌘+I` (macOS) or `Ctrl+I` (Linux/Windows) to toggle modes if you're in Agent Mode by accident.
* **`Shift+Enter` for newlines.** Use `Shift+Enter` to insert a newline in Claude Code's prompt. If it submits the message instead, check that you're in terminal mode (not Agent Mode) and that you're on a recent Warp version.
* **Copy/paste handling.** Warp enables bracketed paste by default, so multi-line pastes into Claude Code work without extra configuration.
* **Resuming after a Warp restart.** Warp's [session restoration](../../terminal/sessions/session-restoration.md) preserves tabs and panes, but not running CLI processes — closing Warp ends Claude Code's session. Use Claude Code's built-in resume options (e.g., `claude --resume`) to continue a conversation after reopening Warp.

### API keys and authentication

Claude Code's authentication (API key or Anthropic account) is handled by Claude Code itself, not Warp. Warp does not proxy or modify Claude Code's network calls. Configure your `ANTHROPIC_API_KEY` environment variable via [Warp Drive environment variables](../../knowledge-and-collaboration/warp-drive/environment-variables.md) to share it across sessions without committing it to shell config files.

## Switching to Agent Mode from Claude Code

If you're ready to replace Claude Code with Warp's built-in agent, the core workflow is:

1. Open a new tab in Warp.
2. To switch to switch to [Agent Mode](https://docs.warp.dev/agent-platform/warp-agents) from terminal mode, press `⌘+Enter` (or `Ctrl+Shift+Enter`)
3. Describe what you want in natural language.

Warp's agent reads your codebase, runs commands, and edits files the same way Claude Code does.

### What transfers: context and rules

A recurring question from Claude Code users: **what files and context does Warp's agent read automatically?** Warp picks up project rules from an `AGENTS.md` (or `WARP.md`) at your repo root — the direct equivalent of Claude Code's `CLAUDE.md`. Run `/init` in Agent Mode to generate one, or rename your existing rules file and you're done — no rewriting needed.

Warp's agent also pulls context from several other explicit sources:

* **[Codebase Context](https://docs.warp.dev/agent-platform/warp-agents/codebase-context)** - when you open a directory, Warp indexes your Git-tracked files so the agent can search and reference your code without you pasting snippets.
* **[Rules](https://docs.warp.dev/agent-platform/warp-agents/rules)** - global and project-scoped rules. `AGENTS.md` and `WARP.md` are automatically picked up at the project root; additional rules live in Warp Drive.
* **[Warp Drive](../../knowledge-and-collaboration/warp-drive/README.md)** - notebooks, workflows, and environment variables you've saved are available to the agent as context.
* **[Agent Mode context](../../knowledge-and-collaboration/warp-drive/agent-mode-context.md)** - pin specific files or notebooks to a conversation so the agent always has them in scope.
* **[MCP](https://docs.warp.dev/agent-platform/warp-agents/mcp)** - any MCP servers you've configured give the agent access to external tools and data.

### What to reconfigure

* **Bring over your `CLAUDE.md`.** Rename it to `AGENTS.md` (or copy it into a Warp [Rule](https://docs.warp.dev/agent-platform/warp-agents/rules) if you want it scoped beyond the repo). Warp applies it automatically to new conversations.
* **Set up [MCP servers](https://docs.warp.dev/agent-platform/warp-agents/mcp)** you relied on in Claude Code.
* **Pick a model** per conversation using the model selector. See [model choice](https://docs.warp.dev/agent-platform/warp-agents/model-choice). Warp supports Claude, GPT, Gemini, and Auto.
* **Configure [agent profiles and permissions](https://docs.warp.dev/agent-platform/warp-agents/agent-profiles-permissions)** for what the agent can auto-execute.

### Key differences from Claude Code

* **Tight terminal integration.** Agent Mode runs inside Warp and sees the full state of your terminal session — open files, command history, environment variables — without needing you to paste context.
* **Parallel agents.** Warp runs multiple agent conversations across tabs simultaneously, each with its own state, which you can track in the Agent Management Panel.
* **Code Review built in.** Agent-generated diffs open in Warp's [Code Review](../../code/code-review.md) panel, not the terminal.
* **Cloud orchestration.** Long-running or scheduled agent work can be offloaded to [Oz](https://docs.warp.dev/agent-platform/cloud-agents/overview).

## Warp-native equivalents

Claude Code concepts and their closest Warp analog:

| From Claude Code | In Warp |
| --- | --- |
| `CLAUDE.md` | `AGENTS.md` (or `WARP.md`) at the project root, picked up as a [Rule](https://docs.warp.dev/agent-platform/warp-agents/rules) |
| Claude Code slash commands | Warp's own [slash commands](https://docs.warp.dev/agent-platform/warp-agents/slash-commands) (`/init`, `/plan`, `/model`, etc.); save your own as [Warp Drive prompts](../../knowledge-and-collaboration/warp-drive/prompts.md) |
| Tool definitions | [MCP](https://docs.warp.dev/agent-platform/warp-agents/mcp) |
| Resume conversation | Warp persists agent conversations per tab; pair with [tab configs](../../terminal/windows/tab-configs.md) to reopen the same project layout |

For a deeper tour of Agent Mode, see [Coding in Warp](../coding-in-warp.md) and the [Warp Agents docs](https://docs.warp.dev/agent-platform/warp-agents).
