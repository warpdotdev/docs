---
description: >-
  Get up and running with Warp in about 10 minutes. Install, run your first
  commands, talk to an agent, and discover what makes Warp different.
---

# Warp quickstart

This guide walks you through installing Warp, trying the terminal features you'll use every day, and firing off your first agent prompt. After completing the steps in this guide, you'll have a working Warp setup and a clear picture of how terminal commands and agents work together.

***

## Prerequisites

* **macOS, Windows, or Linux** - See [Installation and setup](installation-and-setup.md) for minimum requirements per platform.

***

## 1. Install Warp

Download Warp from [warp.dev](https://www.warp.dev/download) and follow the installer for your platform.

{% tabs %}
{% tab title="macOS" %}
Download and drag Warp into your Applications folder, or install with Homebrew:

```bash
brew install --cask warp
```
{% endtab %}

{% tab title="Windows" %}
Download and run the installer, or install with WinGet:

```powershell
winget install Warp.Warp
```
{% endtab %}

{% tab title="Linux" %}
Download the package for your distribution from [warp.dev/download](https://www.warp.dev/download). For Debian/Ubuntu:

```bash
sudo apt install ./warp-terminal.deb
```

See [Installation and setup](installation-and-setup.md) for all Linux options.
{% endtab %}
{% endtabs %}

When you launch Warp, you'll see a terminal session ready for input. You can optionally sign up for an account (top right), or skip and start using Warp immediately.

## 2. Run a command and see Blocks

Run any command you'd normally use, for example:

```bash
ls -la
```

You'll notice the output looks different from a traditional terminal. Every command and its output is grouped into a **Block** — a contained unit you can copy, search, filter, and navigate independently. Blocks are the foundation of how Warp organizes your terminal.

**What you can do with Blocks:**

* Click a Block to select it, then press `⌘C` (macOS) or `Ctrl+Shift+C` (Windows/Linux) to copy the output
* Use `⌘↑`/`⌘↓` (macOS) or `Ctrl+↑`/`Ctrl+↓` (Windows/Linux) to navigate between Blocks
* Click the filter icon on a Block to search within its output

Learn more about navigating, selecting, and acting on output in [Block basics](../terminal/blocks/block-basics.md).

## 3. Try the input editor

Warp's input isn't a standard terminal prompt, it's a real text editor. Try the following functionality:

* **Multi-line editing** - Press `Shift+Enter` to add a new line. Try typing three separate `echo` lines, pressing `Shift+Enter` between each, then `Enter` to run them all at once.
* **Click to place your cursor** - Click anywhere in your input to move the cursor, just like a text editor.
* **Select and edit** - Click and drag to select text, then type to replace it.

All three commands run in sequence, and each produces its own Block. No need to run commands one at a time.

Learn more about cursor movement, selections, and multi-line input in [Modern text editing](../terminal/editor/README.md).

## 4. See autosuggestions and completions

Start typing a command you've run before. You'll see a faded suggestion appear inline based on your shell history. Press `→` to accept it instantly.

Press `Tab` while typing to see completions for commands, flags, and file paths. Warp provides enhanced completions beyond what your shell offers natively.

If you mistype a command, Warp detects the error and suggests a correction. Accept the fix or dismiss it and continue.

Learn more about [Autosuggestions](../terminal/command-completions/autosuggestions.md) and [Tab completions](../terminal/command-completions/completions.md).

## 5. Ask your first agent question

Everything you've done so far has been in **terminal mode**, running shell commands the way you normally would. Warp also has **Agent Mode**, a dedicated conversation view where you interact with Oz, Warp's built-in agent, using natural language.

Start an agent conversation by pressing `⌘↩` (macOS) or `Ctrl+Shift+Enter` (Windows/Linux). Then type a prompt:

```
Explain the architecture of this project
```

Oz reads your codebase, understands its structure, and responds with a context-aware explanation. From here you can ask follow-up questions, have Oz write or refactor code, debug errors, or run commands on your behalf — all within the same conversation.

{% hint style="info" %}
You don't always need to switch modes manually. If you type a natural-language prompt in terminal mode, Warp auto-detects it and offers to send it to an agent.
{% endhint %}

Warp also works with third-party CLI agents like Claude Code and Codex. Learn more about [third-party CLI agents](https://docs.warp.dev/agent-platform/third-party-agents).

To learn more about switching between modes, see [Terminal and Agent modes](https://docs.warp.dev/agent-platform/local-agents/interacting-with-agents/terminal-and-agent-modes).

***

## What to explore next

Now that you have the basics, check out the features that make Warp a full development environment:

* **[Customizing Warp](customizing-warp.md)** — Pick a theme, configure your prompt, choose your AI model, and import keybindings from another terminal.
* **[Codebase Context](https://docs.warp.dev/agent-platform/capabilities/codebase-context)** — Index your Git repositories so agents understand your code and give context-aware answers across large, multi-repo systems.
* **[Oz cloud agents](https://docs.warp.dev/agent-platform/cloud-agents/overview)** — Run agents in the background for PR review, issue triage, dependency updates, and other tasks that don't need your immediate attention.
* **[Keyboard shortcuts](keyboard-shortcuts.md)** — The full shortcut reference for power users.
