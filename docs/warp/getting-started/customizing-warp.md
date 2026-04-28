---
description: >-
  A complete guide to customizing Warp: themes, vertical tabs, tab configs,
  prompt chips, keybindings, AI models, and more.
---

# Customizing Warp

Warp is deeply customizable. Whether you use Warp primarily as a modern terminal or as an AI-powered development environment, you can tailor the experience to fit how you work. Configure the terminal side (themes, keybindings, vertical tabs, tab configs) and the AI side (model choice, agent autonomy, default mode) independently.

Use the quick-reference table to find what you need, or browse the sections below for more details. If you want to go further than configuration, Warp's client is open source under [AGPL v3](https://github.com/warpdotdev/warp/blob/master/LICENSE) — see [Contributing to Warp](https://docs.warp.dev/support-and-community/community/contributing) to build a custom variant or contribute changes upstream.

## Quick reference

| What to customize | Where to find it | Quick action |
| --- | --- | --- |
| Theme | **Settings** > **Appearance** | Pick a preset or [create a custom YAML theme](../terminal/appearance/custom-themes.md) |
| Prompt chips | Right-click prompt area > **Edit prompt** | Drag and drop context chips (directory, git branch, time, etc.) |
| AI model | Model selector in agent conversation | Choose Claude, GPT, Gemini, or Auto |
| Keybindings | **Settings** > **Keyboard shortcuts** | Import from another terminal or set custom shortcuts |
| Vertical tabs | **Settings** > **Appearance** > **Tabs** | Switch to a sidebar tab layout for more horizontal space |
| Tab configs | **Settings** > **Features** or `/` menu | Save and restore tab layouts with startup commands |
| Settings file | **Open settings file** button in the Settings footer | Edit [`settings.toml`](../terminal/settings/README.md) directly for version control and scripting |
| Input format | **Settings** > **Appearance** > **Input** | Choose Standard or Classic |
| App icon | **Settings** > **Appearance** > **Icon** | Pick a custom icon (macOS) |
| Font & text | **Settings** > **Appearance** > **Text** | Change font, size, and cursor style |
| Agent autonomy | **Settings** > **Agents** > **Profiles** | Set what the agent can do without asking |
| Default mode | **Settings** > **Agents** > **Warp Agent** > **Input** | Choose whether new tabs open in terminal mode or Agent Mode |

***

## Appearance

In Warp, navigate to **Settings** > **Appearance** to access these options and control how Warp looks:

* **[Themes](../terminal/appearance/themes.md)** - Choose from pre-loaded themes or create your own [custom theme](../terminal/appearance/custom-themes.md) using YAML or a background image.
* **[Prompt chips](../terminal/appearance/prompt.md)** - Customize the context chips in your Warp prompt. Right-click the prompt area and select **Edit prompt** to drag and drop chips like directory, git branch, Kubernetes context, and time.
* **[App icons](../terminal/appearance/app-icons.md)** - Choose a custom app icon to distinguish Warp in your dock (macOS).
* **[Text, fonts, and cursor](../terminal/appearance/text-fonts-cursor.md)** - Change your font type, size, and cursor style.
* **[Input position](../terminal/appearance/input-position.md)** - Move your prompt and command line to the top or bottom of the window.
* **[Size, opacity, and blurring](../terminal/appearance/size-opacity-blurring.md)** - Adjust window transparency and blur effects.
* **[Pane dimming](../terminal/appearance/pane-dimming.md)** - Dim inactive panes to focus on the active one.

## Layout

Organize your workspace with tabs, panes, and window configurations.

* **[Vertical tabs](../terminal/windows/vertical-tabs.md)** - Switch to a vertical sidebar layout for tabs, giving you more horizontal space and better visibility when you have many open sessions.
* **[Tabs](../terminal/windows/tabs.md)** - Organize sessions into tabs with custom titles and colors. Right-click a tab to pick a color.
* **[Split panes](../terminal/windows/split-panes.md)** - Divide any tab into multiple panels, side-by-side or stacked.
* **[Tab configs](../terminal/windows/tab-configs.md)** - Save and restore tab layouts with predefined pane arrangements and startup commands.
* **[Global hotkey](../terminal/windows/global-hotkey.md)** - Set up a dedicated hotkey window (Quake Mode) that appears and hides with a keyboard shortcut.

## Input and editor

Configure how you type and interact with the terminal input.

* **[Standard vs Classic input](../terminal/input/classic-input.md)** - Standard input provides easier access to AI features and is the default for new users. Classic input resembles a traditional terminal prompt. Switch between them in **Settings** > **Appearance** > **Input**.
* **[Keyboard shortcuts](keyboard-shortcuts.md)** - Warp supports common shortcuts and lets you create custom ones. Manage them from **Settings** > **Keyboard shortcuts**, or import keybindings from another terminal during [migration](migrate-to-warp.md).
* **[Vim keybindings](../terminal/editor/vim.md)** - Enable Vim keybindings for keyboard-driven text editing in the input editor.
* **Tab key behavior** - Configure what `Tab` does in **Settings** > **Features**. Options include accepting autosuggestions or triggering completions.

## AI and models

Control how Warp's agents behave and which models they use.

* **[Model choice](https://docs.warp.dev/agent-platform/warp-agents/model-choice)** - Choose your preferred AI model (Claude, GPT, Gemini, or Auto) from the model selector in any agent conversation.
* **[Agent profiles and permissions](https://docs.warp.dev/agent-platform/warp-agents/agent-profiles-permissions)** - Configure how much autonomy the agent has: what it can auto-execute, what requires approval, and command allowlists/denylists.
* **Default mode for new sessions** - Choose whether new tabs open in terminal mode or Agent Mode by default. Set this in **Settings** > **Agents** > **Warp Agent** > **Input**.

## Import and sync

Bring your existing settings into Warp or keep settings synchronized across machines.

* **[Migrate from another terminal](migrate-to-warp.md)** - Import keybindings, color themes, and other settings when switching to Warp. Currently supports iTerm2 profiles.
* **[Settings sync](../terminal/more-features/settings-sync.md)** - Sync your Warp settings across machines (Beta).

***

## Next steps

Now that Warp looks and feels like yours, the next step is to put it to work on a real project. Open a codebase to unlock context-aware agents, or start an agent conversation to see how terminal commands and AI work together.

* **[Codebase Context](https://docs.warp.dev/agent-platform/warp-agents/codebase-context)** - Open a project and index your codebase so agents give you context-aware answers about your code.
* **[Terminal and Agent modes](https://docs.warp.dev/agent-platform/warp-agents/interacting-with-agents/terminal-and-agent-modes)** - Learn how terminal mode and agent conversations work together.
