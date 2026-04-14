---
description: >-
  Set up Claude Code in Warp, configure it for your project, and learn
  productivity tips — from voice prompting to visual code review.
---

# How to set up Claude Code

Claude Code is Anthropic's AI coding agent. It reads your codebase, writes and edits code, runs commands, and handles complex refactors using natural language prompts. This guide takes you from zero to a working Claude Code session in Warp in about 5 minutes, then shows you how to get the most out of it.

## Prerequisites

* **A Claude account with CLI access** — Claude Code requires a paid plan or API credits. See [Claude Code requirements](https://docs.anthropic.com/en/docs/claude-code/setup) for eligible plans.
* **macOS 13+, Windows 10+, or Ubuntu 20.04+** — See [Claude Code system requirements](https://docs.anthropic.com/en/docs/claude-code/setup) for full platform details.
* **Git** — Claude Code works best inside a Git repository. On Windows, [Git for Windows](https://git-scm.com) is required.


## 1. Install Claude Code

Follow Anthropic's [official installation guide](https://docs.anthropic.com/en/docs/claude-code/quickstart) to install Claude Code. The native installer (recommended) requires no dependencies and auto-updates in the background.

When you launch Claude Code inside Warp, Warp auto-detects the agent session and surfaces integrated controls, including rich input, code review, vertical tab metadata, and more.

## 2. Authenticate

The first time you run Claude Code, it opens your browser for login.

```bash
claude
```

Sign in with your Claude account. Once authenticated, the token is stored locally and you won't need to log in again.

For headless environments or CI/CD, set an API key instead:

```bash
export ANTHROPIC_API_KEY=YOUR_API_KEY
```

## 3. Start your first session

Navigate to any project directory and launch Claude Code:

```bash
cd ~/your-project
claude
```

Try giving it a task, for example:

```
Explain the architecture of this project
```

Or something more hands-on:

```
Add input validation to the user registration endpoint
```

Claude Code will find the relevant files, show you the proposed changes, and ask for confirmation before modifying anything.

## 4. Configure for your project

Create a `CLAUDE.md` file at your project root to teach Claude Code your project's conventions. Claude Code reads this file at the start of every session.

```markdown
# My Project

## Stack
- Backend: Python 3.12, FastAPI, SQLAlchemy
- Frontend: React, TypeScript, Vite
- Database: PostgreSQL 16

## Commands
- `npm run dev` starts the dev server
- `pytest -v` runs the test suite
- `npm run lint` checks code style

## Conventions
- Use async/await for all database operations
- Type hints on all function signatures
- ESM imports only (no require())
```

This prevents Claude Code from guessing your conventions and ensures it follows your team's standards from the first prompt.

## 5. Choose a model and permissions

Claude Code uses the latest Claude model by default. To use a specific model:

```bash
claude --model MODEL_NAME
```

By default, Claude Code asks for permission before every file write and command execution. You can pre-approve safe operations in `.claude/settings.json`:

```json
{
  "permissions": {
    "allow": [
      "Read",
      "Glob",
      "Grep",
      "Bash(pytest*)",
      "Bash(npm run lint)"
    ]
  }
}
```

This lets Claude read files and run your test/lint commands without prompting, while still asking before writing files.

## 6. Set up agent notifications

Warp supports agent notifications for Claude Code through the `warpdotdev/claude-code-warp` plugin. Once installed, Warp surfaces in-app and desktop alerts when Claude Code needs your input, such as command approval, code review, or error intervention.

**Auto-install:** When you run Claude Code in Warp without the notification plugin installed, a notification chip appears offering one-click installation. Click the chip and Warp installs the plugin automatically.

**Manual install:** If the auto-install chip doesn't appear, install from inside Claude Code:

```bash
/plugin marketplace add warpdotdev/claude-code-warp
/plugin install warp@claude-code-warp
```

After installing, restart Claude Code or run `/reload-plugins` to activate the plugin.

{% hint style="info" %}
The notification plugin requires `jq`. Install it with your package manager (e.g., `brew install jq` on macOS) if it's not already available.
{% endhint %}

For plugin source and updates, see the [claude-code-warp GitHub repository](https://github.com/warpdotdev/claude-code-warp).

## Productivity tips

* **Use voice to prompt Claude Code** — Instead of typing complex instructions, dictate them. Warp supports [voice transcription](https://docs.warp.dev/agent-platform/local-agents/interacting-with-agents/voice) that works with any CLI agent, including Claude Code. Press the microphone icon or the `fn` key to start recording.
* **Attach images as context** — Paste screenshots of bug reports, design mockups, or error messages directly into your prompt. Warp's [images as context](https://docs.warp.dev/agent-platform/local-agents/agent-context/images-as-context) feature lets Claude Code see what you see.
* **Review diffs visually** — After Claude Code makes changes, open Warp's [Code Review panel](https://docs.warp.dev/warp/code/code-review) (`⌘+Shift++`) to see a visual diff of every file changed. You can leave inline comments and send them back to Claude Code for corrections.
* **Run multiple Claude Code sessions in parallel** — Use [vertical tabs](https://docs.warp.dev/warp/terminal/windows/vertical-tabs) to run different Claude Code tasks side by side, one session fixing bugs while another writes tests. Each tab shows which agent is running and its current status.
* **Compose richer prompts** — Press `Ctrl+G` to open Warp's rich input editor for Claude Code. This gives you a full text editor experience for composing prompts — click to position your cursor, select text, and edit naturally instead of navigating with arrow keys.

<!-- If a standalone summary feels valuable, add a ## Recap heading above this paragraph. -->

## Next steps

You installed Claude Code, authenticated, started your first session, configured it for your project, and learned the key productivity features that make it faster to use in Warp.


Explore related guides and features:
* [Set up Codex CLI](how-to-set-up-codex-cli.md) to run a second agent alongside Claude Code
* [How to review AI-generated code](../developer-workflows/how-to-review-ai-generated-code.md) — a structured workflow for reviewing and refining agent output
* [Run multiple agents at once](../developer-workflows/how-to-run-multiple-ai-coding-agents.md) — use Claude Code and Codex side by side
* [Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code/quickstart) — Anthropic's official reference
* [Claude Code in Warp](https://warp.dev/agents/claude-code) — overview of Claude Code support in Warp
* [Claude Code in Warp (docs)](https://docs.warp.dev/agent-platform/cli-agents/claude-code) — full reference for Claude Code's Warp integration, including notification setup
* [Third-party CLI agents](https://docs.warp.dev/agent-platform/cli-agents/overview) — all supported agents and Warp's universal agent features
