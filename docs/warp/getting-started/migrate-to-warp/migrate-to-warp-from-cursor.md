---
description: >-
  Reconfigure your terminal and agent settings when switching to Warp from
  Cursor, or run Warp alongside Cursor as your agent terminal.
---

# Migrate to Warp from Cursor

Warp gives Cursor users two clean migration paths: keep Cursor as your editor and use Warp for terminal and agent work, or move fully to Warp's built-in code editor and Agent Mode. This page walks through both options.

## What transfers automatically

Warp doesn't ship a Cursor importer. Cursor is built on the VS Code codebase, so its terminal settings live in `settings.json` under keys like `terminal.integrated.fontFamily` and `terminal.integrated.defaultProfile.*`. Open your user settings with **Command Palette** > **Preferences: Open User Settings (JSON)** to reference them while you reconfigure Warp.

## Use Warp's agent to migrate your settings (recommended)

The fastest way to bring over your Cursor terminal setup is to ask Warp's agent to translate your `settings.json` directly. Warp ships a [`settings.toml` file](../../terminal/settings/README.md) and a bundled `modify-settings` skill that lets the agent read your existing config and write equivalent values into Warp's settings.

1. In Warp, open a new tab and switch to [Agent Mode](https://docs.warp.dev/agent-platform/warp-agents) with `⌘+I` (macOS) or `Ctrl+I` (Linux/Windows).
2. Paste a prompt like:

   > Read my Cursor `settings.json` (`~/Library/Application Support/Cursor/User/settings.json` on macOS) and port the equivalent terminal settings (font, cursor style, default profile) into my Warp `settings.toml` using the `modify-settings` skill. Show me a diff before applying.

3. Review the proposed diff and approve. Warp hot-reloads `settings.toml`, so changes take effect immediately.

If you'd rather configure each setting manually through the Settings UI, the steps below cover the most common cases.

## What to reconfigure manually

### Terminal settings

Terminal settings in Cursor follow the same schema as VS Code. The migration steps are identical to the VS Code terminal migration - see [Migrate to Warp from VS Code terminal](migrate-to-warp-from-vs-code-terminal.md) for step-by-step guidance on shell, font, theme, and keybinding setup.

### Agent and AI settings

Cursor's Composer and Agent features don't have a one-to-one migration path - they map to different Warp concepts.

* **Composer / Agent** in Cursor maps to Warp's [Agent Mode](https://docs.warp.dev/agent-platform/warp-agents). Start an agent conversation in any tab.
* **Rules files** (`.cursorrules`) - Warp uses [Rules](https://docs.warp.dev/agent-platform/warp-agents/rules) stored in Warp Drive or committed to your repo as `AGENTS.md` (or `WARP.md`). Run `/init` in Agent Mode to generate an `AGENTS.md`, or copy your `.cursorrules` content directly.
* **MCP servers** - Warp supports MCP natively. See [MCP](https://docs.warp.dev/agent-platform/warp-agents/mcp) for configuration.

### Model choice

Cursor lets you pick a model per conversation. Warp does the same - use the model selector in any agent conversation. See [model choice](https://docs.warp.dev/agent-platform/warp-agents/model-choice).

### Keybindings

Warp's [keyboard shortcuts](../keyboard-shortcuts.md) differ from Cursor's. Most notably, `⌘+I` (or `Ctrl+I` on Linux/Windows) toggles between terminal and Agent Mode. From terminal mode you can also press `⌘+Enter` (or `Ctrl+Shift+Enter`) as an alternate shortcut into Agent Mode.

## Choosing your setup

### Use Warp alongside Cursor

Keep Cursor as your editor for tight in-file AI assistance, and use Warp as the terminal you switch to for:

* Long-running commands and SSH.
* [Agent Mode](https://docs.warp.dev/agent-platform/warp-agents) conversations that execute commands, not just edit files.
* [Code Review](../../code/code-review.md) for managing diffs.
* [Warp Drive](../../knowledge-and-collaboration/warp-drive/README.md) for team knowledge.

### Replace Cursor with Warp

Warp's built-in [code editor](../../code/code-editor/README.md) supports Language Server Protocol, a [file tree](../../code/code-editor/file-tree.md), [find and replace](../../code/code-editor/find-and-replace.md), and [Vim keybindings](../../code/code-editor/code-editor-vim-keybindings.md). Combined with Agent Mode, Code Review, and Warp Drive, the full Cursor workflow is reachable in Warp without a separate editor.

## Warp-native equivalents

Cursor features and their Warp counterparts:

| From Cursor | In Warp |
| --- | --- |
| Composer / Agent panel | [Agent Mode](https://docs.warp.dev/agent-platform/warp-agents) in any tab (toggle with `⌘+I`) |
| Agent tabs | Multiple [agents in parallel](https://docs.warp.dev/agent-platform/warp-agents) across tabs |
| `.cursorrules` | `AGENTS.md` / `WARP.md` at the project root, picked up as a [Rule](https://docs.warp.dev/agent-platform/warp-agents/rules) |
| MCP servers | [MCP](https://docs.warp.dev/agent-platform/warp-agents/mcp) |
| Model choice per conversation | [Model selector](https://docs.warp.dev/agent-platform/warp-agents/model-choice) |
| Codebase indexing | [Codebase Context](https://docs.warp.dev/agent-platform/warp-agents/codebase-context) |
| Inline diff review | [Code Review](../../code/code-review.md) |

See [Coding in Warp](../coding-in-warp.md) for a tour of the development workflow.
