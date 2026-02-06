# Agent Modality (Beta)

### Agent Conversations: the new modality

{% hint style="info" %}
Agent modality is currently in beta and only available in [**Warp Preview**](https://warp.dev/download-preview)**. If you notice something that is missing, broken, or unclear, please share your feedback in the** [Warp Community Slack](https://join.slack.com/t/warpcommunity/shared_invite/zt-3n000083p-sshYx6qVdDvFq~Ht3QoJXQ). If you can, please include screenshots or a short screen recording with your feedback.
{% endhint %}

Agent modality, an **experimental** UI under development for [agent conversations](./), gives you two distinct ways to work in Warp: a clean terminal for commands, and a dedicated conversation view for multi-turn agent workflows.&#x20;

{% embed url="https://www.loom.com/share/b5b58c5cd3af42748c890680f3f7692d" %}

***

### Why we built this

The default Warp input combines terminal commands and agent interactions in one place. As usage evolved, this made the input feel busier than necessary and sometimes unclear about which mode you were in. Auto-detection between shell commands and natural language helps, but it has limits. This modality is our way of addressing that.

Agent modality separates your terminal and agent workflows into distinct modes:

* **Clean terminal by default**: Minimal input when you're running commands. Agent controls appear only when you need them.
* **Dedicated conversation view**: Multi-turn agent workflow spaces have full controls like model select, voice input, image attachments, and conversation history.
* **Smarter mode switching**: Warp detects whether you're typing a command or a prompt. Use `⌘+I` to override the auto-detection.

### What's changing

Experience Warp in **two distinct modes**:

#### Terminal mode (default)

* Looks and behaves like a traditional terminal input.
* Agent controls are not always visible, but clear to send something to an agent.

<figure><img src="../../.gitbook/assets/terminal-modality.png" alt=""><figcaption></figcaption></figure>

If auto-detection is enabled, Warp may label your input as "agent" or "shell" before you submit. You can always use `⌘I` to override the detected mode.

#### Agent mode (expanded UI)

* A dedicated conversation view with richer agent controls including model select, voice input, image attachments, and conversation management.
* Familiar "charms" (current directory, git branch, diff view entry point, etc.) are still available.
* Designed for multi-turn workflows and managing multiple conversations.

<figure><img src="../../.gitbook/assets/agent-modality-convo.png" alt=""><figcaption></figcaption></figure>

**Key difference**

Agent controls appear only when you're in a conversation, keeping your terminal clean otherwise.&#x20;

In the old UI, agent controls were always present—with the new minimal modality, these controls are not displayed by default but appear **once you enter an agent conversation in the agent mode.**

{% hint style="info" %}
Distinct agent conversation views are identified with an alternative background and the new input tool belt.
{% endhint %}

**Auto-detection in a conversation**

Auto-detection still applies in agent conversations:

* If you type something like `ls`, Warp auto-detects the shell command.
* Warp will show that it’s auto-detected a shell command. Use `⌘I` to toggle back to an agent prompt.

***

### Availability + defaults

* Preview-only right now.
* Auto-detection will be disabled by default for new users (both now and at launch).
* For existing users, it may respect your existing settings (depending on how you’re already configured).

***

### Core concept: auto-detection + override

Warp interprets each input as either a shell command or an agent request. When auto-detection is enabled, Warp shows an **inline indicator** in the prompt (for example, “auto-detected”).

<figure><img src="../../.gitbook/assets/send-to-agent.png" alt=""><figcaption></figcaption></figure>

#### Override auto-detection (important)

Press `⌘I` to switch between command and agent mode.

Common examples:

* You typed something that looks like a command, but you intended an agent request.
* You typed a sentence, but you intended it to run as a command (rare, but it happens).

{% hint style="info" %}
**Note:** After you override, the selection is “sticky” for that entry, so you can submit confidently.
{% endhint %}

### How to enter an agent conversation

There are two main methods for entering an agent conversation:

#### A) Type naturally (auto-detection will route you)

1. Type a request. For example, “Summarize the dependencies in this project”.
2. If Warp detects an agent request, submit it.
3. You’ll enter an agent conversation automatically.

Use this method for quick, text-only requests.

#### B) Enter explicitly (recommended if you need rich controls first)

Press `⌘↩` (Command+Enter) to enter the conversation view immediately.

**Use this when you want to:**

* attach an image
* use voice input
* access other conversation-only controls before sending your first message

### Starting a new conversation + navigating

This modality changes how conversations are organized.

<figure><img src="../../.gitbook/assets/agent-conversations-new-modality.png" alt=""><figcaption></figcaption></figure>

The **Conversation Panel** on the left is the new home for browsing and switching between agent conversations.&#x20;

It’s designed to make multi-threaded work obvious: you can see what’s active, what you ran recently, and jump back into any thread without guessing where your context went.

### Panel layout

The conversation panel is split into two dropdowns (collapsible sections) that help you navigate between conversations:

#### Active

The **Active** dropdown lists the conversations that are currently open in this window/workspace.

* Select a conversation to switch to it immediately.
* The conversation you’re currently viewing is highlighted.

#### Past

The Past dropdown lists your recent conversation history.

Each row typically shows:

* Conversation title
* When it happened (for example, “8 min ago”, “3 days ago”)
* Working directory (when relevant)

Use **Past** to jump back into something you were working on earlier, without needing a separate “conversation switcher” in the main view.

#### Search

Use the search field at the top of the conversation panel to quickly find your conversation.

* Type to filter conversations by title (and, in some builds, by directory/context).
* Useful when you have many threads and want to jump directly to one.

#### New conversation

Click the `+` button near the top-right of the panel to start a new conversation.

Starting a new conversation creates a fresh thread in the **Active** dropdown, without deleting or overwriting your previous ones.

#### No classic conversation switcher

In the minimal modality, you’re “in” a conversation and navigation is designed to be more direct. Instead of a traditional conversation switcher, conversations are represented explicitly in the UI (as separate conversation blocks/threads).

#### Ways to move around

* `esc`: exit the current conversation back to your previous terminal session (“escape hatch”)
* `⌘K`: start a new agent conversation (clears the current conversation view and begins a fresh thread)

Practical mental model:

* You can go “one level deep” into a conversation.
* You can pop back out to your terminal context with `esc` at any time.
* Starting a new conversation creates a new thread rather than mixing unrelated topics.

### Using slash commands

**In an agent conversation**

<figure><img src="../../.gitbook/assets/slash-commands-agent-modality.png" alt=""><figcaption></figcaption></figure>

While you're in an agent conversation, you can access Warp's [slash commands](../../capabilities/slash-commands.md) any time by typing `/` in the input.

* Type `/` to open the command menu
* Keep typing to filter commands (for example: `/conversations`, `/compact`)
* Use `↑` / `↓` to navigate and Enter to run
* Press `esc` to dismiss the menu

Slash commands are a quick way to take common actions without leaving the keyboard, like opening conversation history, compacting context, or kicking off guided flows.

**In terminal mode**

<figure><img src="../../.gitbook/assets/slash-commands-terminal-modality.png" alt=""><figcaption></figcaption></figure>

Slash commands aren’t just for agent conversations. You can also type `/` in the normal terminal mode to open a limited set of commands.

**In general**

* Agent conversations expose the full set of slash commands (more agent-specific actions).
* Terminal mode exposes a reduced set focused on quick, lightweight actions.

***

### Keyboard shortcuts (quick reference)

In conversation view (agent mode), press `?` to show/hide shortcuts. Common ones include:

* `!` → shell mode
  * prepend this to your input to force shell mode.
* `/` → agent commands
* `@` → file paths / attach context
* `esc` → exit conversation
* `⌘⇧I` → toggle auto-accept
* `^C` → stop
* `⌘⇧+` → open code review
* `⌘⇧H` → toggle conversation list
* `?` → show/hide shortcuts

{% hint style="info" %}
Availability of keyboard shortcuts may vary while this feature is in Preview.
{% endhint %}

### Known gaps / rough edges (Preview)

Agent modality is in active development. You might notice:

* Not every control from the old UI is present everywhere yet (e.g., some switchers or entry points).
* Visual treatments, like conversation background shading, may change before stable release.
* Some shortcut hints or in-product help text may be incomplete.

**Share feedback**

The most helpful details to include are:

* what you expected
* what happened instead
* whether auto-detection got it wrong
* your OS + Warp version
* screenshots or a short recording
