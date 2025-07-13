---
description: Agents can generate and edit code directly from within Warp.
---

# Coding in Warp

When Warp detects an opportunity to apply a code diff, it activates an advanced code generation flow that supports both single-file edits and multi-file changes.

* **Code creation**: “Write a function in JavaScript to debounce an input”
* **Based on error outputs, suggest fixes**: “Fix this TypeScript error.”
* **Edit a single file**: “Update all instances of ‘var’ to ‘let’ in this file.”
* **Make batch changes**: “Add headers to all .py files in this directory”

**The best way to experience this is to try it yourself —** [_open the Prompt below in Warp_](https://app.warp.dev/drive/prompt/Generate-a-custom-Warp-theme-K8oloLrCZAHuaYKfz2cNqI)

{% code overflow="wrap" %}
```markup
Detect the correct Warp themes directory based on the current operating system:
- On macOS, use ~/.warp/themes/
- On Linux, use ${XDG_DATA_HOME:-$HOME/.local/share}/warp-terminal/themes/
- On Windows, use $env:APPDATA\warp\Warp\data\themes\

Create the directory if it doesn’t already exist. 

Then, generate a custom Warp theme named {{theme_name}} in valid YAML format, following the official structure from Warp’s documentation. Exclude the background_image field, and do not include any extra or missing fields. Save the theme as {{theme_name}}.yaml in the detected themes directory.

Once the theme is created and verified, confirm completion by telling me where the theme file was saved.
```
{% endcode %}

***

### Context

#### Codebase Context

Warp can index your Git-tracked codebases to help agents understand your code and generate accurate, context-aware responses. **No code is stored on Warp servers**.

You can view and manage your indexed codebases under `Settings > Code > Codebase Index` and you can also specify whether to automatically index new folders as you navigate them.

If your codebase is large, you can exclude specific files by adding them to a `.warpindexingignore` file.

#### Other types of context

You can provide different types of input as context directly to the agent to guide its behavior and improve response quality. This includes:

* [Blocks](https://docs.warp.dev/agents/using-agents/agent-context#attaching-blocks-as-context) from your terminal output
* [Images](https://docs.warp.dev/agents/using-agents/agent-context#attaching-images-as-context)
* [Files and code](https://docs.warp.dev/agents/using-agents/agent-context#referencing-files-and-code-using) (using the @ symbol)
* [Public websites](https://docs.warp.dev/agents/using-agents/agent-context#referencing-websites-via-urls) via URLs

#### Warp Drive as Context

Agents pull directly from your [**Warp Drive**](https://docs.warp.dev/features/warp-drive) contents to generate more accurate responses -- including your **Workflows**, **Notebooks**, **Prompts**, and **Environment Variables**.

* When used, context appears under the “References” or “Derived from” section in the conversation.
* This setting is **enabled by default** and can be managed via: `Settings > AI > Knowledge > Warp Drive as Agent Mode Context`.

#### Rules

**Rules** let you provide persistent context to Agents, enabling smarter and more personalized responses. You can create your own Rules, and Warp will also suggest new ones based on your usage patterns.

**Examples of Rules include:**

* Coding standards and best practices
* Project- or workspace-specific guidelines
* Personal preferences for tools, formatting, or behavior

How to access Rules

1. From the [Warp Drive](https://docs.warp.dev/features/warp-drive) > Personal > Rules
2. From the [Command Palette](../../features/warp-ai/command-palette.md), search for "Open AI Rules"
3. From the Settings panel, `Settings > AI > Knowledge > Manage Rules`
4. From the macOS Menu, `AI > Open Rules`
