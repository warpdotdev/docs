---
description: >-
  How to attach various forms of multi-modal context directly to Warp's Agent
  within a prompt.
---

# Agent Context

In Warp, you can pass different types of input directly to the Agent to guide its behavior and improve response quality. These inputs are known as **Agent Context**: ad-hoc pieces of information you manually supply during a session.

**You can attach context in several ways:**

* [blocks-as-context.md](blocks-as-context.md "mention") - share output from your terminal to help the Agent understand errors, logs, or previous commands.
* [images-as-context.md](images-as-context.md "mention") - include screenshots, diagrams, or other visuals to provide additional clarity.
* [urls-as-context.md](urls-as-context.md "mention") - attach public webpages so the Agent can extract and reference their content.
* [selection-as-context.md](selection-as-context.md "mention") - attach code snippets from the editor or review panel to enrich your prompts with precise context.
* [using-to-add-context.md](using-to-add-context.md "mention") - reference files, folders, code symbols, or Warp Drive objects directly in your prompts.

***

This is distinct from other persistent or automatic sources of context, such as [rules.md](../../../knowledge-and-collaboration/rules.md "mention"), [warp-drive-as-agent-mode-context.md](../../../knowledge-and-collaboration/warp-drive/warp-drive-as-agent-mode-context.md "mention"), and [mcp.md](../../../knowledge-and-collaboration/mcp.md "mention"), which the Agent also uses when available.
