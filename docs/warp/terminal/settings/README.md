---
description: >-
  Configure Warp with a plain-text TOML settings file. Learn where it lives,
  how it works with the Settings panel, and see common configuration
  examples.
---

# Settings file [Preview-only]

{% hint style="info" %}
The settings file is currently available in [Warp Preview](https://docs.warp.dev/support-and-community/community/warp-preview-and-alpha-program). Settings and behavior described on this page may change before the stable release.
{% endhint %}

Warp stores your preferences in a plain-text file called `settings.toml`. You can edit it directly in any text editor, check it into version control, or generate it with a script. Changes take effect immediately — no restart required.

The settings file works alongside the graphical Settings panel. Changes you make in either place are reflected in the other.

**Key features:**

* **Hot-reload** — Warp watches `settings.toml` for changes and applies them instantly when you save the file.
* **Error recovery** — If the file contains invalid TOML or an unrecognized value, Warp shows a warning banner and falls back to defaults for the affected settings. Fix the file and the banner clears automatically.
* **Automatic migration** — When you upgrade to a version of Warp that includes the settings file, Warp automatically migrates your existing preferences into `settings.toml`.
* **Bidirectional sync with Settings UI** — Changes in the Warp **Settings** panel (`⌘+,` on macOS) write to `settings.toml`, and hand-edits to the file are reflected in the panel.
* **Agent-powered editing** — Ask Warp's agent to change settings for you using natural language (for example, "increase my font size to 16"). The bundled `modify-settings` skill handles the file update automatically.

## Opening your settings file

There are several ways to open `settings.toml`:

* In the Warp app, go to **Settings** and click **Open settings file** at the bottom of the panel.
* Open the file directly in any editor at the path listed below for your platform.

## File location

Depending on your platform, `settings.toml` is located at:

* **macOS** — `~/.warp-preview/settings.toml`
* **Linux** — `~/.config/warp-terminal-preview/settings.toml`
* **Windows** — `%LOCALAPPDATA%\warp\WarpPreview\config\settings.toml`

When the settings file reaches stable, the paths will be:

* **macOS** — `~/.warp/settings.toml`
* **Linux** — `~/.config/warp-terminal/settings.toml`
* **Windows** — `%LOCALAPPDATA%\warp\Warp\config\settings.toml`

## Settings file format

The file uses [TOML v1.1](https://toml.io/en/v1.1.0) syntax. Settings are organized into **sections** (TOML tables) that group related options — for example, `[appearance.text]` contains font settings and `[agents.profiles]` contains agent permission settings.

Here is a minimal example showing the structure:

```toml
# Appearance settings
[appearance.text]
font_name = "JetBrains Mono"
font_size = 14.0
line_height_ratio = 1.3

[appearance.themes]
theme = "dracula"

# Terminal behavior
[terminal.input]
syntax_highlighting = true
honor_ps1 = false

# Agent permissions
[agents.profiles]
agent_mode_execute_readonly_commands = true
```

### How sections map to TOML tables

Each section in the settings file corresponds to a TOML table header in brackets. Subsections use dot-separated paths:

* `[general]` — Top-level general settings like session restoration and tab placement
* `[appearance]` — Visual settings, with subsections like `[appearance.text]`, `[appearance.themes]`, `[appearance.cursor]`
* `[agents]` — Agent and AI settings, with subsections like `[agents.profiles]`, `[agents.oz.input]`
* `[terminal]` — Terminal behavior settings, with subsections like `[terminal.input]`

For the complete list of every available setting, see [All settings reference](all-settings.md).

## How settings are applied

### Relationship between the Settings panel and the file

The Warp Settings panel (`⌘+,` on macOS, `Ctrl+,` on Linux/Windows) and `settings.toml` represent the same underlying configuration. Changing a toggle in the Settings panel writes the new value to `settings.toml`. Editing `settings.toml` by hand updates the Settings panel the next time it reads the file.

### Error banner

When `settings.toml` has errors, Warp displays a dismissible warning banner at the top of the workspace. The banner includes an **Open settings file** button so you can jump directly to the file and fix the issue. Once you save a corrected file, the banner disappears automatically.

## Common configurations

### Change theme and font

```toml
[appearance.themes]
theme = "cyber_wave"

[appearance.text]
font_name = "Fira Code"
font_size = 15.0
ligature_rendering_enabled = true
font_weight = "normal"
```

### Configure agent permissions

```toml
[agents.profiles]
agent_mode_coding_permissions = "always_allow_reading"
agent_mode_execute_readonly_commands = true
agent_mode_command_execution_allowlist = [
  "cat(\\s.*)?",
  "echo(\\s.*)?",
  "find .*",
  "grep(\\s.*)?",
  "ls(\\s.*)?",
  "which .*",
]
```

### Enable Vim keybindings

```toml
[text_editing]
vim_mode_enabled = true
vim_status_bar = true
```

## Migrating from previous settings

When you upgrade to a version of Warp that includes the settings file, Warp automatically migrates your existing preferences into `settings.toml`. No action is required — your customizations carry over and the file becomes the source of truth for all settings going forward.

## Troubleshooting

### "Your settings file contains an error" banner

This banner appears when `settings.toml` has invalid TOML syntax or an unrecognized value. Click **Open settings file** in the banner to open the file and look for:

* **Missing quotes** — String values must be wrapped in double quotes: `font_name = "Hack"`, not `font_name = Hack`.
* **Missing brackets** — Section headers require square brackets: `[appearance.text]`.
* **Wrong value types** — Check that numbers are numbers (`font_size = 13.0`), booleans are `true`/`false`, and enum values are valid strings.

### Resetting to defaults

Delete `settings.toml` (or rename it) and restart Warp. Warp falls back to built-in defaults for all settings. The file is re-created the next time you change a setting through the Settings panel.

```bash
# macOS (Preview) — back up your current settings, then delete the file
cp ~/.warp-preview/settings.toml ~/.warp-preview/settings.toml.bak
rm ~/.warp-preview/settings.toml

# Linux (Preview)
# cp ~/.config/warp-terminal-preview/settings.toml ~/.config/warp-terminal-preview/settings.toml.bak
# rm ~/.config/warp-terminal-preview/settings.toml
```

### Settings not applying

Confirm you're editing the correct file for your platform (see [File location](#file-location) above). If you run multiple [Warp release channels](https://docs.warp.dev/support-and-community/community/warp-preview-and-alpha-program), each channel has its own settings directory.

## Related pages

* [All settings reference](all-settings.md) — Complete list of every available setting with descriptions, types, and defaults
* [Customizing Warp](../../getting-started/customizing-warp.md) — Overview of all customization options
* [Custom themes](../appearance/custom-themes.md) — Create and load custom YAML or Base16 themes
* [Keyboard shortcuts](../../getting-started/keyboard-shortcuts.md) — Customize keybindings
* [Settings Sync (Beta)](../more-features/settings-sync.md) — Sync settings across machines
