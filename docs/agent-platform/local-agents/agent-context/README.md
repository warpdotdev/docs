---
description: >-
  How to attach various forms of multi-modal context directly to Warp's Agent
  within a prompt.
---

# Agent Context

In Warp, you can pass different types of input directly to the Agent to guide its behavior and improve response quality. These inputs are known as **Agent Context**: ad-hoc pieces of information you manually supply during a session.

**You can attach context in several ways:**

* [Blocks as Context](blocks-as-context.md) - share output from your terminal to help the Agent understand errors, logs, or previous commands.
* [Images as Context](images-as-context.md) - include screenshots, diagrams, or other visuals to provide additional clarity.
* [URLs as Context](urls-as-context.md) - attach public webpages so the Agent can extract and reference their content.
* [Selection as Context](selection-as-context.md) - attach code snippets from the editor or review panel to enrich your prompts with precise context.
* [Using @ to Add Context](using-to-add-context.md) - reference files, folders, code symbols, or Warp Drive objects directly in your prompts.

***

This is distinct from other persistent or automatic sources of context, such as [Rules](https://docs.warp.dev/knowledge-and-collaboration/rules), [Warp Drive as Agent Mode Context](https://docs.warp.dev/knowledge-and-collaboration/warp-drive/warp-drive-as-agent-mode-context), and [Model Context Protocol (MCP)](https://docs.warp.dev/knowledge-and-collaboration/mcp), which the Agent also uses when available.
