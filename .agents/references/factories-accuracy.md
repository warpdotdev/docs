# Factories accuracy checklist

Use this when drafting, reviewing, or answering questions about Warp Factories.
Sales engineering and support need answers that match shipped product behavior,
not marketing summaries or outdated Automation Platform pages.

## Source of truth order

1. **Shipped public docs under `src/content/docs/factories/`** for user-facing
   workflows, integrations, and operations.
2. **Released OpenAPI** at `developers/agent-api-openapi.yaml` for factory REST
   endpoints and schemas already published there (including `/factory`,
   `/factory-inbox`, nested `/factory/{uid}/...` routes, and
   `/factory-files/schemas`).
3. **Public client (`warp`)** and **server (`warp-server`)** for flags,
   defaults, runtime behavior, and unreleased-vs-GA checks.
4. **`warp-factory-examples`** for definition file examples that match the
   published schema.
5. **Warp Learn** (`https://www.warp.dev/learn`) for course-style onboarding
   only. It is not a substitute for docs or API truth.

Do not treat staging behavior, private specs, or schema fields whose server
flags are off in production as customer-ready truth. Run
`python3 .agents/skills/doc_quality_policy/server_rollout.py check <names>`
before documenting a server-backed field or endpoint.

A published docs page is not by itself proof that every related REST route is
released. For API surfaces, the released OpenAPI file is the Gate 0 test.
Conversely, do not claim factory REST is unpublished when `/factory` paths are
already in that file.

## Canonical page map

- What Factories is and how pieces fit → `/factories/`
- First successful factory → `/factories/quickstart/`
- Work-item lifecycle and stages → `/factories/how-factories-work/`
- Workers, foreman, harnesses → `/factories/factory-agents/`,
  `/factories/harnesses/`
- Blueprint stages and gates → `/factories/blueprints/`
- Definition files as code → `/factories/factory-as-code/`
- Skills for factory workers → `/factories/factory-skills/`
- Integrations and intake → `/factories/connect-your-factory/`,
  `/factories/integrations/`, `/factories/automations/`
- REST dispatch and discovery → `/factories/factory-api/`,
  `/factories/api-and-sdk/`, plus OpenAPI
- Local coding-agent handoff → `/factories/factory-mcp/`, `/factories/mcp/`
- Dashboard, runs, inbox → `/factories/factory-dashboard/`,
  `/factories/factory-home/` when relevant
- Billing and plans for factories → `/factories/managing-plans-and-billing/`
- Security, self-hosting, ZDR → `/factories/infrastructure-and-security/`,
  `/factories/self-hosting/`, `/factories/zero-data-retention/`
- Measure and improve → `/factories/measure-and-improve/`,
  `/factories/benchmarks/`
- Failures and recovery → `/factories/troubleshooting/`

Prefer these over older standalone cloud-agent pages under
`src/content/docs/platform/` when the question is about a standing factory,
foreman, blueprint, or factory definition.

## Claims that require extra verification

Before stating any of the following, confirm the current docs page and, when
technical, source or OpenAPI:

- Merge behavior, branch protection, and whether a factory can merge PRs
- Which integrations are GA vs limited, and who must install or authorize them
- Credential strategy (`EXECUTOR` vs alternatives), secret storage, and which
  identity runs Git operations
- Plan names and billing for Warp Factories vs Warp Terminal / local agent
  plans
- Whether ChatGPT/Claude/Codex *subscriptions* work inside factory workers vs
  API keys / Warp-hosted models
- Factory endpoint paths, request bodies, and which key type can call them
- Managed self-hosting eligibility and runner requirements
- Computer use, third-party harnesses, and model availability inside factory
  workers
- Whether a field exists only in a schema file or is live in production
- Factory alias rename / immutability after creation
- Label-only GitHub triggers vs mention/assignment automations
- PR author identity (human vs app vs agent) on factory-opened PRs
- Env vars in runner images for MCP auth vs Warp-managed secrets
- Bidirectional Factory MCP / coding-agent listen behavior vs polling
- Managed scorer model overrides on file-managed factories
- GHES / non-GitHub forge feature degradation

## Kapa and support themes (Docs + Front)

Use these as coverage and answer priorities. Clusters and uncertain threads
(roughly 2026-09 through 2026-11) concentrate on:

### Conceptual

- What a factory is; blueprint vs running factory; how Warp uses factories
  internally
- Foreman scoping: how large/ambiguous a task can be; what parallelizes vs
  blocks
- Whether factories have a "projects" feature; dashboard "Activity" visibility
- Isolation during implementation; context the factory keeps while working

### Configuration and code

- `factory.yaml` local use; factory-wide prompts/skills vs per-agent
- Reusing monorepo skills; coding-agent harness skills vs factory skills
- Attaching MCP servers to factory agents; env vars vs secrets for MCP
- Factory MCP from Claude Code / OpenCode; docs MCP wiring
- Alias rename after creation (often uncertain in support drafts)

### Runtime and integrations

- What starts work (labels, mentions, assignments, Linear)
- GitHub auth, resume, setup failures, runs that finish without doing work
- Gemini / context-window failures on foreman and subagent runs
- PR opener identity; GHES and generic git forge tradeoffs
- Implementer access to npm/packages in the environment
- OpenTelemetry / observability expectations

### Billing and access

- Factories Early Access credits
- BYOK and vendor subscriptions for factory inference
- Unexpected usage on first factory setup; refunds
- Scale plan factory features vs terminal plans

### Highest-uncertainty factory source pages

Docs source usage in the factories section ranked these pages with elevated
uncertain answers: `factory-as-code`, `self-hosting`, `integrations`,
`factory-mcp`, `how-factories-work`, `factory-agents`, and
`infrastructure-and-security`.

### Themes documented in the accuracy PR

These high-traffic gaps now have verified public prose:

- Alias immutability after creation → `/factories/factory-as-code/#alias`
- Subscription vs API/team-managed factory inference →
  `/factories/managing-plans-and-billing/#inference-for-factory-workers`
- Empty/failed runs, GitHub setup/resume, continue after finish →
  `/factories/troubleshooting/`

## Answering customer and SE questions

- Lead with the shipped behavior and the canonical docs link.
- Separate **infrastructure** (Warp Factories) from **a customer's factory**
  (their configured workflows and workers).
- If docs and source disagree, say so, prefer verified source for technical
  detail, and flag the docs gap.
- If evidence is missing, say what is unknown instead of filling gaps with
  likely behavior.
- Do not invent factory UIDs, plan prices, unreleased endpoints, or "always"
  rules about autonomy or merge.
- For Front/support draft prompts, answer the customer question only; do not
  narrate Kapa or internal tooling.

## Related agent skills

- `answer_question` — customer-facing synthesis with docs links
- `draft_docs` / `review-docs-pr` — writing and reviewing factories pages
- `missing_docs` — coverage gaps against code and OpenAPI
- `docs_consistency_audit` — conflicting claims across pages
