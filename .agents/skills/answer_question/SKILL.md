---
name: answer_question
description: >-
  Answer questions about Warp, Oz, agents, terminal features, billing, pricing,
  troubleshooting, privacy, skills, MCP, integrations, or any other Warp-related
  topic. Use when a user, support person, or engineer asks a question that can
  be answered from Warp's documentation. Searches the docs, synthesizes a
  comprehensive answer, and provides links to relevant doc pages.
---

# Answer Question

Answer questions about Warp by searching this docs repo and synthesizing a
direct response with links. For Factories, billing edge cases, CLI/API details,
or anything the docs leave ambiguous, verify against released OpenAPI and
product source before answering.

## When Factories is in scope

Treat any question about factories, factory runs, foreman, blueprints,
factory-as-code, Factory MCP, factory agents, factory billing, factory
integrations, or standing multi-agent workflows as a **Factories** question.

1. Read `.agents/references/factories-accuracy.md` first.
2. Prefer pages under `src/content/docs/factories/` over older standalone
   cloud-agent pages under `src/content/docs/platform/` when both could apply.
3. For API shape, endpoint existence, or request/response fields, check
   `developers/agent-api-openapi.yaml`. Factory paths such as `/factory`,
   `/factory-inbox`, and `/factory-files/schemas` are part of the released
   public surface when present there.
4. If docs and source disagree, say so, prefer verified source for technical
   detail, and name the docs gap.
5. If evidence is missing, say what is unknown. Do not invent UIDs, prices,
   unreleased endpoints, merge guarantees, or "always" rules about autonomy.

## Workflow

### 1. Search the docs

Content lives under `src/content/docs/`:

| Section | Path |
| --- | --- |
| Terminal and getting started | `src/content/docs/getting-started/`, `src/content/docs/terminal/`, `src/content/docs/code/` |
| Agents | `src/content/docs/agents/` |
| Standalone cloud-agent platform | `src/content/docs/platform/` |
| Warp Factories | `src/content/docs/factories/` |
| Guides | `src/content/docs/guides/` |
| Support, billing, privacy | `src/content/docs/support-and-community/` |
| Enterprise | `src/content/docs/enterprise/` |
| Changelog | `src/content/docs/changelog/` |

Search strategy:

- Use `codebase_semantic_search` on the docs repo for the user's question.
- Use `grep` for exact feature names, settings paths, CLI commands, API paths,
  or error strings.
- Read matched files. Skim broadly, then read the owning section in detail.
- If the question spans topics, search each topic and cross-reference.
- Use `src/sidebar.ts` when you need the navigation tree or to confirm a page
  is public.

Do **not** look for `src/content/docs/agent-platform/` or
`src/content/docs/reference/`. Those paths are gone. Agents content is under
`agents/`; Factories under `factories/`; CLI/API reference is split across
`agents/cli/`, `factories/api-and-sdk/`, and
`developers/agent-api-openapi.yaml`.

### 2. Verify outside the prose when needed

Use extra sources when the docs are thin, conflicting, or the question is
operational:

| Source | Use for |
| --- | --- |
| `developers/agent-api-openapi.yaml` | Released public API paths and schemas |
| Public client repo (`warp`) | UI labels, settings, client flags |
| `warp-server` | Runtime defaults, billing, factory handlers |
| `warp-factory-examples` | Example factory definition files |
| `.agents/references/terminology.md` | Product names and wording |
| `AGENTS.md` | Style and terminology rules |

Locate sibling checkouts on the machine (`warp`, `warp-server`). If they are
missing and the answer depends on them, say what you could not verify.

Before treating a server-backed field or endpoint as customer-ready, confirm
production rollout with
`python3 .agents/skills/doc_quality_policy/server_rollout.py check <names>`
when available. Schema presence alone is not release evidence.

**Priority:** shipped public docs for user-facing workflow; OpenAPI for the
released API contract; source for verification and gaps. Never replace a clear
docs answer with an undocumented implementation detail unless you are
correcting a docs error and you say so.

### 3. Compose the answer

- Lead with the direct answer, then the minimum context needed to act or
  decide.
- Use terminology from `AGENTS.md` and `.agents/references/terminology.md`.
  - **Warp Factories** for the platform; lowercase **factory** for one
    customer's system.
  - **agent** / **agents** generically; **Warp Agent** only for the built-in
    harness.
  - **the Automation Platform** when referring to that platform (article
    outside the var).
  - Do not say "Oz agent", "AI credits" as the product noun, or bare
    "Factories" for the platform.
- Separate plan families: Warp Terminal / local agent plans vs Warp Factories
  plans.
- For support-style drafts, stay technical and brief; do not promise account
  actions you cannot perform.
- If docs do not cover the topic, say so. Do not guess.

### 4. Generate doc links

End every answer with a **Relevant docs** section.

URL rules:

| File path | URL |
| --- | --- |
| `src/content/docs/{path}.mdx` | `https://docs.warp.dev/{path}` |
| `src/content/docs/factories/{path}.mdx` | `https://docs.warp.dev/factories/{path}` |
| `src/content/docs/agents/{path}.mdx` | `https://docs.warp.dev/agents/{path}` |
| `src/content/docs/platform/{path}.mdx` | `https://docs.warp.dev/platform/{path}` |
| `src/content/docs/support-and-community/{path}.mdx` | `https://docs.warp.dev/support-and-community/{path}` |
| `src/content/docs/enterprise/{path}.mdx` | `https://docs.warp.dev/enterprise/{path}` |
| `src/content/docs/guides/{path}.mdx` | `https://docs.warp.dev/guides/{path}` |
| `src/content/docs/changelog/{path}.mdx` | `https://docs.warp.dev/changelog/{path}` |

Rules:

- Strip `.mdx`. `index.mdx` resolves to the parent path.
- No `agent-platform` segment in URLs.
- Prefer the canonical Factories owner page from
  `.agents/references/factories-accuracy.md` when several pages touch the
  topic.

### 5. Output format

```
[Direct answer]

**Relevant docs:**
- [Page title](https://docs.warp.dev/...)
- [Page title](https://docs.warp.dev/...)
```

When something is unverified, add one short line naming the gap (for example,
"OpenAPI has the route; production flag state was not checked in this
environment.").

## High-traffic Factories themes

Recurring Kapa / support themes. Start on the listed owners, then verify:

- What a factory is, blueprints vs a running factory, foreman scope →
  `/factories/`, `/factories/how-factories-work/`, `/factories/blueprints/`,
  `/factories/factory-agents/`
- Factory-as-code, `factory.yaml`, skills reuse, MCP on agents →
  `/factories/factory-as-code/`, `/factories/factory-skills/`,
  `/factories/factory-mcp/`, `/factories/mcp/`
- Triggers, labels, GitHub/Linear intake →
  `/factories/connect-your-factory/`, `/factories/automations/`, integrations
  under `/factories/integrations/`
- Harnesses, BYOK / subscription inference vs Warp-hosted usage →
  `/factories/harnesses/`, `/factories/managing-plans-and-billing/`, billing
  pages under `/support-and-community/plans-and-billing/`
- Run failures, resume, GitHub auth, empty runs →
  `/factories/troubleshooting/`, `/factories/factory-dashboard/`, code-forge
  pages
- API dispatch, metrics, scorers, benchmarks → `/factories/factory-api/`,
  `/factories/api-and-sdk/`, OpenAPI
- Alias rename, self-hosting, security, ZDR → factory-as-code + self-hosting +
  infrastructure pages; do not invent mutability rules

## Related references

- `.agents/references/factories-accuracy.md` — source order, page map,
  high-risk claims
- `.agents/references/docs-page-feedback.md` — footer thumbs events and
  Kapa/feedback rollups
- `.agents/references/terminology.md` — glossary
- `.agents/references/compliance-claims-policy.md` — compliance claims
- `missing_docs` — coverage gaps against code and OpenAPI
