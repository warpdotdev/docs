---
description: Use natural language to accomplish any task in the terminal
---

# Untitled

## What is Agent Mode?

Agent Mode is a mode in Warp that lets you perform any terminal task with natural language. Type the task into your terminal input, press `ENTER`, and Warp AI runs highly accurate commands tailored to your environment.\
\
Agent Mode can:

1. Understand plain English (not just commands)
2. Execute commands and use that output to guide you
3. Correct itself when it encounters mistakes
4. Learn and integrate with any service that has public docs or --help
5. Utilize your saved workflows to answer queries

[Visit the example gallery to watch videos of Agent Mode in action](https://www.warp.dev/ai).

### How to enter Agent Mode

You may enter Agent Mode in a few ways:

{% tabs %}
{% tab title="macOS" %}
* Type any natural language, like a task or a question, in the terminal input. Warp will recognize natural language with a local auto-detection feature and prepare to send your query to Warp AI.
* Use keyboard shortcuts to toggle into Agent Mode `CMD-I` or type `ASTERISK-SPACE`.
* Click the “AI” sparkles icon in the menu bar, and this will open a new terminal pane that starts in Agent Mode.
* From a block, you want to ask Warp AI about. You can click the sparkles icon in the toolbelt, or click on its block context menu item “Attach block(s) to AI query”.
{% endtab %}

{% tab title="Windows" %}
* Type any natural language, like a task or a question, in the terminal input. Warp will recognize natural language with a local auto-detection feature and prepare to send your query to Warp AI.
* Use keyboard shortcuts to toggle into Agent Mode `CTRL-I` or type `ASTERISK-SPACE`.
* Click the “AI” sparkles icon in the menu bar, and this will open a new terminal pane that starts in Agent Mode.
* From a block, you want to ask Warp AI about. You can click the sparkles icon in the toolbelt, or click on its block context menu item “Attach block(s) to AI query”.
{% endtab %}

{% tab title="Linux" %}
* Type any natural language, like a task or a question, in the terminal input. Warp will recognize natural language with a local auto-detection feature and prepare to send your query to Warp AI.
* Use keyboard shortcuts to toggle into Agent Mode `CTRL-I` or type `ASTERISK-SPACE`.
* Click the “AI” sparkles icon in the menu bar, and this will open a new terminal pane that starts in Agent Mode.
* From a block, you want to ask Warp AI about. You can click the sparkles icon in the toolbelt, or click on its block context menu item “Attach block(s) to AI query”.
{% endtab %}
{% endtabs %}

This will put you in _Pair_ mode by default. While pairing with Warp, you can write out questions and tasks in an ongoing conversation.

When you are in Agent Mode, a ✨ sparkles icon will display in line with your terminal input.

<figure><img src="../../.gitbook/assets/undo_my_git_commit.png" alt="The sparkles on the command line indicate Agent Mode is active."><figcaption><p>The sparkles on the command line indicate Agent Mode is active.</p></figcaption></figure>

### Auto-detection for natural language and configurable settings

The feature Warp uses to detect natural language automatically is completely local. None of your input is sent to AI unless you press `ENTER` in Agent Mode.

If you find that certain shell commands are falsely detected as natural language, you can fix the model by adding those commands to a denylist in `Settings > AI > Auto-detection denylist`.

You may also turn autodetection off from `Settings > AI > Input Auto-detection`.

The first time you enter Agent Mode, you will be served a banner with the option to disable auto-detection for natural language on your command line:

<figure><img src="../../.gitbook/assets/banner_for_auto-detection_first_experience.png" alt="Warp displays an option to toggle natural language detection on / off"><figcaption><p>Warp displays an option to toggle natural language detection on / off</p></figcaption></figure>

### Input Hints

Warp input occasionally shows hints within the input editor in a light grey text that helps users learn about features. It's enabled by default.

* Toggle this feature `Settings > AI > Show input hint text` or search for "Input hint text" in the [Command Palette](../../terminal/command-palette.md) or Right-click on the input editor.

### How to exit Agent Mode

{% tabs %}
{% tab title="macOS" %}
You can quit Agent Mode at any point with `ESC` or `CTRL-C`, or toggle out of Agent Mode with `CMD-I`.
{% endtab %}

{% tab title="Windows" %}
You can quit Agent Mode at any point with `ESC` or `CTRL-C`, or toggle out of Agent Mode with `CTRL-I`.
{% endtab %}

{% tab title="Linux" %}
You can quit Agent Mode at any point with `ESC` or `CTRL-C`, or toggle out of Agent Mode with `CTRL-I`.
{% endtab %}
{% endtabs %}

### How to run commands in Agent Mode

Once you have typed your question or task in the input, press `ENTER` to execute your AI query. Agent Mode will send your request to Warp AI and begin streaming output in the form of an AI block.

Unlike a chat panel, Agent Mode can complete tasks for you by running commands directly in your session.

#### Agent Mode Command Suggestions

If Agent Mode finds a suitable command that will accomplish your task, it will describe the command in the AI block. It will also fill your terminal input with the suggested command so you can press `ENTER` to run the command.

When you run a command suggested by Agent Mode, that command will work like a standard command you've written in the terminal. No data will be sent back to the AI.

If the suggested command fails and you want to resolve the error, you may start a new AI query to address the problem.

<figure><img src="../../.gitbook/assets/agent-mode-suggestion (3) (1).png" alt="Agent Mode makes a suggestion to run a command."><figcaption><p>Agent Mode makes a suggestion to run a command.</p></figcaption></figure>

#### Agent Mode Requested Commands

If Agent Mode doesn't have enough context to assist with a task, it will ask permission to run a command and read the output of that command.

You must explicitly agree and press `ENTER` to run the requested command. When you hit enter, both the command input and the output will be sent to Warp AI.

If you do not wish to send the command or its output to AI, you can click Cancel or press `CTRL-C` to exit Agent Mode and return to the traditional command line.

<figure><img src="../../.gitbook/assets/warp-ai-permissions.png" alt="Warp AI asks permission to run a command and read the output."><figcaption><p>Warp AI asks permission to run a command and read the output.</p></figcaption></figure>

Once a requested command is executed, you may click to expand the output and view command details.

<figure><img src="../../.gitbook/assets/warp-ai-viewing-commands.png" alt=""><figcaption><p>Viewing command details</p></figcaption></figure>

In the case that a requested command fails, Warp AI will detect that. Agent Mode is self-correcting. It will request another command until it completes the task for you.

Warp lets you choose from a curated list of LLMs for use in Agent Mode. By default, Warp uses **Claude 4 Sonnet** for auto, but you can switch to other supported models, including:

* **OpenAI (General Purpose)**: `GPT-4o`, `GPT-4.1`
* **OpenAI (Reasoning Models)**: `o3-mini`, `o3`, `o4-mini`
* **Anthropic**: `Claude 4 Sonnet`, `Claude 3.7 Sonnet`, `Claude 3.5 Sonnet`, `Claude 3.5 Haiku`
* **Google**: `Gemini 2.0 Flash`, `Gemini 2.5 Pro`
* **DeepSeek**: `R1`, `V3` (hosted by [Fireworks AI](https://fireworks.ai/) in the US)

#### Codebase context database

Warp saves the data from codebase context to local json files on your computer. You can open the files directly and inspect the full contents in the following location:

{% tabs %}
{% tab title="macOS" %}
```bash
cd "$HOME/Library/Application Support/dev.warp.Warp-Stable/codebase_index_snapshots"
```
{% endtab %}

{% tab title="Windows" %}
```powershell
Set-Location $env:LOCALAPPDATA\warp\Warp\data\codebase_index_snapshots
```
{% endtab %}

{% tab title="Linux" %}
```bash
cd "${XDG_STATE_HOME:-$HOME/.local/state}/warp-terminal/codebase_index_snapshots"
```
{% endtab %}
{% endtabs %}

## Dispatch

If you have questions or need extended access, feel free to reach out to us at [feedback@warp.dev](mailto:feedback@warp.dev).\
\
&#xNAN;**"Request failed with error: QuotaLimit" error**

Once you exceed your AI token limits, all models will be disabled. Note that requests and tokens are calculated separately, and even though the plans may have a set number of requests, they also have a limited number of tokens.
