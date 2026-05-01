---
name: answer_question
description: Answer questions about Warp, Oz, agents, terminal features, billing, pricing, troubleshooting, privacy, skills, MCP, integrations, or any other Warp-related topic. Use when a user, support person, or engineer asks a question that can be answered from Warp's documentation. Searches the docs, synthesizes a comprehensive answer, and provides links to relevant doc pages.
---

# Answer Question

Answer any question about Warp or Oz by searching the documentation in this repository and synthesizing a comprehensive, matter-of-fact response with links to source pages. For deep technical questions, also search Warp's source repositories for implementation details.

## Workflow

### 1. Search for relevant docs

The documentation lives in `docs/` with these sections:
- `src/content/docs/` — Warp Terminal and IDE (getting started, terminal, code editor, knowledge & collaboration)
- `src/content/docs/agent-platform/` — Agent Platform (local agents, cloud agents, capabilities, integrations)
- `src/content/docs/reference/` — Technical reference (Oz CLI, API & SDK)
- `src/content/docs/support-and-community/` — Support (troubleshooting, billing, privacy)
- `src/content/docs/enterprise/` — Enterprise
- `src/content/docs/changelog/` — Changelog

Search strategy:
- Use `codebase_semantic_search` on the docs repo to find relevant doc pages for the user's question.
- Use `grep` when searching for exact feature names, settings, CLI commands, or specific terms.
- Read matched files to gather authoritative content. Skim broadly first, then read key sections in detail.
- If the question spans multiple topics (e.g. "How do skills work with cloud agents?"), search each topic independently and cross-reference.
- Check `astro.config.mjs (sidebar config)` files in the relevant section if you need to locate a page by name.

### 2. Search source code (if needed)

For technical questions where the docs are insufficient, incomplete, or you want to validate your answer, search Warp's source repositories:

- **warp-internal** — Client-side code (Rust, Swift). Contains terminal features, editor, UI, Agent Mode client logic, Warp Drive, etc.
- **warp-server** — Server-side code (Go). Contains API endpoints, cloud agent orchestration, billing, auth, etc.

To find these repos, search for directories named `warp-internal` and `warp-server` on the user's machine. If not found, ask the user where they are.

Use source code to:
- Verify technical behavior, edge cases, or implementation details that docs don't fully cover
- Find exact CLI flag names, config options, or API parameters
- Understand how features interact under the hood
- Answer "how does X actually work?" questions that go beyond the docs

Both repos are indexed for `codebase_semantic_search`. Use `grep` for exact symbol/function names.

**Important:** Docs are the primary source of truth for user-facing answers. Use source code as supplementary context, not as a replacement. Always prefer doc-based explanations when available.

### 3. Compose the answer

- Be direct and matter-of-fact. Answer the question, don't summarize the docs.
- Be comprehensive — cover what the user needs to fully understand the answer — but don't pad with tangential information.
- Use Warp's standard terminology from `AGENTS.md` and the full glossary in `.warp/references/terminology.md`. Key rules: capitalize feature names (Agent, Agent Mode, Warp Drive, Codebase Context), use "Oz agent" not "Ozzie" or "the Oz Agent", use "credits" not "AI credits."
- If the docs do not cover the topic, say so honestly. Do not guess or fabricate information.

### 4. Generate doc links

Every answer must end with a **Relevant docs** section listing links to the source pages used.

URL mapping rules (file path → published URL):

| File path | URL |
|---|---|
| `src/content/docs/{path}.mdx` | `https://docs.warp.dev/{path}` |
| `src/content/docs/agent-platform/{path}.mdx` | `https://docs.warp.dev/agent-platform/{path}` |
| `src/content/docs/reference/{path}.mdx` | `https://docs.warp.dev/reference/{path}` |
| `src/content/docs/support-and-community/{path}.mdx` | `https://docs.warp.dev/support-and-community/{path}` |
| `src/content/docs/enterprise/{path}.mdx` | `https://docs.warp.dev/enterprise/{path}` |
| `src/content/docs/changelog/{path}.mdx` | `https://docs.warp.dev/changelog/{path}` |

Key rules:
- **`src/content/docs/` is the homepage space** — the `warp/` prefix is NOT included in URLs. Example: `src/content/docs/terminal/blocks/block-basics.mdx` → `https://docs.warp.dev/terminal/blocks/block-basics`
- All other spaces include the space name in the URL. Example: `src/content/docs/agent-platform/capabilities/skills.mdx` → `https://docs.warp.dev/agent-platform/capabilities/skills`
- Strip the `.mdx` extension.
- `index.mdx` resolves to the parent directory path. Example: `src/content/docs/agent-platform/cloud-agents/integrations/index.mdx` → `https://docs.warp.dev/agent-platform/cloud-agents/integrations`

### 5. Output format

```
[Direct, comprehensive answer to the question]

**Relevant docs:**
- [Page title](https://docs.warp.dev/...)
- [Page title](https://docs.warp.dev/...)
```
