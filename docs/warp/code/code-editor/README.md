---
description: >-
  Warp’s built-in code editor lets you make quick, in-context edits with
  essentials like syntax highlighting, tabs, find and replace, Vim keybindings,
  and a file tree.
---

# Code Editor

## Built-in Code Editor

Warp comes with a native code editor designed for quick, in-flow edits alongside your Agent conversations. Instead of switching back and forth to an IDE, you can open and edit files directly in Warp — with essentials like syntax highlighting, a tabbed file viewer, find and replace, Vim keybindings, and a file tree for browsing and adding files as context.

The editor is built for fast changes to agent-generated code: renaming a variable, tweaking copy, or rewriting a short function. Having just enough editing power in-context makes it easier to land an agent’s changes and keep momentum.

### Opening Files in Warp

**You can open files in the editor in several ways:**

1. **Click a file path** from the terminal output or an AI conversation and select "Open in Warp."
2.  **Use the file menu in the command palette** (`CMD + O` on macOS, `CTRL + SHIFT + O` on Windows or Linux) when in a Git-tracked repo to search for and open files inside that repo.

    1. You can also access this via the magnifying glass icon in the pane coding toolbelt at the top left of any pane.

    <figure><img src="../../.gitbook/assets/search-files-icon.png" alt=""><figcaption></figcaption></figure>
3. **Browse via the** [File Tree (Project Explorer)](file-tree.md) to open or create files.
4. **Opening a generated code diff** from an Agent Conversation: [Code Diffs in Agent Conversations](https://docs.warp.dev/agent-platform/local-agents/code-diffs-in-agent-conversations).

{% embed url="https://screen.studio/share/H7hTUgf2" %}

**To save your changes to files**: use `CMD + S` on macOS or `CTRL + S` on Windows or Linux.

### Tabbed File Viewer

Warp can group multiple files into a single tabbed viewer, reducing clutter and making it easier to work across multiple files.

<figure><img src="../../.gitbook/assets/tabbed-file-viewer.png" alt=""><figcaption></figcaption></figure>

* Enabled by default for new users (can be toggled in `Settings > Features > General > Group files into a single editor pane`)
* Reorder, close, or drag file viewers between tabs.
* Merge entire panes together by dragging one into another.

**Here's a more in-depth demo:**

{% embed url="https://www.loom.com/share/a682461da66944f583e2fa3d27b71189?sid=679ce8f6-e530-4c0d-99ab-0613d1269f8b" %}

### **File Layout Options**

Choose how new files open in Warp by default in: `Settings > Features > General > Choose a layout to open files in Warp`

* **Split pane**: new files open alongside the current editor
* **New tab**: new files open in their own tabbed viewer

### Supported Languages

The editor supports syntax highlighting and editing for a wide range of languages, including:

Rust, Go, YAML, Python, JavaScript/TypeScript, JSX/TSX, Java/Groovy, C++, Shell/Bash, C#, HTML, CSS, C, JSON, HCL/Terraform, Lua, Ruby, PHP, TOML, Swift, Kotlin, Starlark, SQL, Powershell, and Elixir.

We’re continuously expanding language support.

### Other Editor Features

Warp's native code editor also supports the following features:

* [File Tree (Project Explorer)](file-tree.md) — Browse, open, and manage your project with Warp’s native file tree.
* [Find and Replace](find-and-replace.md) — Use Warp’s built-in find and replace to quickly search across a file, jump between matches, and make precise edits with options for regex, case sensitivity, and smart case preservation.
* [Code Editor Vim Keybindings](code-editor-vim-keybindings.md) - Use Vim keybindings to edit code and text in Warp's native code editor.

