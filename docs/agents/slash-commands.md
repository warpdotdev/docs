---
description: >-
  Use Slash Commands (/) in Agent Mode or Auto-Detection Mode to quickly run
  built-in actions or saved prompts without leaving the input field.
---

# Slash Commands

When using Agent Mode or Auto-Detection Mode, typing `/` in the input field opens the Slash Commands menu.

As you type, the menu filters results in real time, making it easy to find and run the command or prompt you need.

## Static Slash Commands

Warp currently supports the following built-in Slash Commands:

<table><thead><tr><th width="211.64453125">Slash Command</th><th>Description</th></tr></thead><tbody><tr><td><code>/add-mcp</code></td><td>Add a new <a href="../knowledge-and-collaboration/mcp.md">MCP server</a>.</td></tr><tr><td><code>/add-prompt</code></td><td>Add a new <a href="../knowledge-and-collaboration/warp-drive/prompts.md">Agent Prompt</a> in Warp Drive.</td></tr><tr><td><code>/add-rule</code></td><td>Add a new <a href="../knowledge-and-collaboration/rules.md">Global Rule</a> for the Agent.</td></tr><tr><td><code>/diff-review</code></td><td>Open the <a href="../code/reviewing-code.md">diff review pane</a>.</td></tr><tr><td><code>/index</code></td><td>Index the current codebase using <a href="../code/codebase-context.md">Codebase Context</a>.</td></tr><tr><td><code>/init</code></td><td>Index the current codebase and generate a <a href="../knowledge-and-collaboration/rules.md">WARP.md file</a>.</td></tr><tr><td><code>/open-project-rules</code></td><td>Open the Project-specific Rules file (<code>WARP.md</code>).</td></tr><tr><td><code>/view-mcp</code></td><td>View the status of your <a href="../knowledge-and-collaboration/mcp.md">MCP servers</a>.</td></tr></tbody></table>

#### Using Prompts via Slash Commands

In addition to static commands, the menu also shows [Agent Prompts](../knowledge-and-collaboration/warp-drive/prompts.md) saved in your [Warp Drive](../knowledge-and-collaboration/warp-drive/).

* These prompts can be custom ones you’ve created or ones shared with you.
* As you type after `/`, prompts are filtered dynamically, so you can quickly run them without leaving the input field.

### Tips

* **Context-aware:** Many Slash Commands use your current working directory or file selection as context.
* **Quick access:** Use `/` from anywhere in Agent Mode or Auto-Detection Mode to avoid navigating through menus.
