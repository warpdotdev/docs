---
description: >-
  Frequently asked questions about cloud agents, including where agents run, how runs work, supported models, security, and common workflows.
---

# Cloud agents FAQs

This page answers common questions about cloud agents, including where they run, how they're configured, and how teams use cloud agents for day-to-day engineering work.

## Architecture and execution

### Where do cloud agents run? What's the architecture?

Agents run either **locally** (inside your Warp session) or **in the cloud** as a **cloud agent run**, inside an **environment** (see [Environments](../platform/environments.md)).

The cloud agents platform is built around modular, observable execution:

- A **trigger** starts work (manual, schedule/cron, webhook, or an integration like Slack/GitHub).
- The **agent** executes inside an **environment** (either a Warp-hosted cloud sandbox, or a **self-hosted sandbox** on your infrastructure, depending on plan/support).
- Every step is recorded: **transcripts, tool calls, logs, and outputs**, so work is auditable and debuggable instead of a black box.

The same agent can be invoked consistently across entry points (Warp Terminal conversation, cloud agent web app, the CLI, API/SDK, Slack/GitHub triggers) without rewriting the underlying instructions.

### What exactly are cloud agents in Warp?

A **cloud agent** is a packaged automation unit made up of:

- **Instructions** — A reusable skill/prompt (what it should do).
- **Profile** — Model selection + tools + permissions (how it operates).
- **Trigger** — Manual, cron/schedule, webhook, or integration event (when it starts).
- **Environment** — Repo access, dependencies (Docker image), secrets, setup commands, and runtime config (where it runs).
- **Host** — Local (interactive) or cloud (run), and optionally self-hosted execution (where supported).

Because the agent definition is modular, the same cloud agent can be started from different surfaces (terminal, web app, CLI, integrations) with a consistent interface.

### Can we intervene mid-run?

Yes. For **cloud agent runs**, you can:

- Inspect **run state**, tool calls, and logs.
- **Steer** the agent while it's running.
- Unblock it with additional instructions or context.

If you're not happy with where it landed, you can take over to finish the task. That human handoff is a core part of making agents reliable beyond demos.

### Can I access a shell inside a cloud agent environment? Are there limitations (Docker, Playwright, etc.)?

Yes. Cloud agent runs execute in a full Linux environment and behave like a local development session. You can install dependencies, run Docker, and use headless tools like Playwright, subject to standard sandbox resource limits.

### Do cloud agents support a fully self-hosted, on-prem, or offline mode?

The cloud agents platform supports self-hosting the **agent sandbox** (the execution environment). The **control plane**—which handles orchestration, tracking, and auditability—is not self-hosted.

You can bring your own model API keys through the Build plan and control where execution happens, but full offline control-plane operation is not currently supported.

## Models

### Which models are supported?

Cloud agents are **multi-model by design**. You can choose models based on cost, latency, and capability, and teams commonly mix models by workflow:

- Faster/cheaper models for triage and routine tasks.
- Stronger models for complex changes (refactors, multi-file work, deeper reasoning).

Model choice is configurable per **agent** (and often per environment/workflow), depending on how you set up your profiles.

### Can I choose which model cloud agents use?

Yes. Cloud agents support the same set of models available in Warp. Model selection is configurable per agent or environment.

### Can I authenticate cloud agents with my own ChatGPT or Claude Pro / Max plan?

We're strong proponents of this, but it ultimately depends on model provider policies. We're actively working with providers to explore whether direct third-party authentication is possible.

### Do you support local or private LLMs for compliance or air-gapped environments?

Enterprise plans will support managed integrations like AWS Bedrock and Google Vertex.

Fully local, offline LLM execution is difficult given the current cloud agents orchestration and runtime architecture, but private-model support via enterprise cloud providers is on the roadmap.

### Will cloud agents support Agent-to-Agent Protocols (A2A)?

It’s something we’re actively exploring. Our focus is on building durable orchestration primitives—runs, environments, audit logs, steering, and coordination—that can support A2A and other emerging standards over time.

## Security and billing

### Will cloud storage for agent definitions, runs, and conversations be secure and encrypted?

Yes. All cloud agent data stored in the cloud is encrypted at rest and in transit, and protected by Warp account–level access controls.

Cloud agent environments are sandboxed by default, with scoped access to repos, secrets, and compute. Security and isolation are first-class design constraints for the cloud agent runtime.

### Are cloud agents included in the Build plan, or is it a separate add-on?

Cloud agents are included in the Build plan. Usage is metered via credits, with pricing based on agent runs and resource consumption. Concurrency limits and credit allocation details are still being finalized.

### How do cloud agents handle API keys and secrets for agents?

Secrets are managed via the cloud agents CLI. Secrets are encrypted at rest, scoped to your Warp account, and injected into the agent environment at runtime. They are never hard-coded into agent instructions or logs.

To learn more about how secrets work in practice, see [Agent secrets](agent-secrets.md).

## Workflows

### How do agents handle branching, merge conflicts, and multi-agent coordination with cloud agents?

The cloud agents platform is intentionally flexible. As the developer, you decide how agents should branch, coordinate, and resolve conflicts.

Interactive agents can plan work and spawn subagents to parallelize tasks. Cloud agents provide the building blocks for running and coordinating multiple concurrent agents, rather than enforcing a fixed workflow.

### Why focus on orchestration primitives instead of immediately adopting new agent standards?

We believe durable infrastructure matters more than transient standards. The cloud agents platform is designed to provide stable building blocks—agent runs, environments, auditability, steering, and coordination—that orchestration frameworks and emerging standards can plug into over time.

### Can cloud agents integrate with external tools, APIs, or services (like n8n connectors)?

Yes, and cloud agents do not rely on rigid, predefined workflows. Agents can install CLIs, call external APIs, use MCP servers, and access the internet directly.

The intent is to delegate flexibility to agents rather than constrain them with fixed connectors.

### Can I export agent conversations and runs from cloud agents?

Yes. Conversations can be copied directly from the UI. The cloud agent CLI and API also provide access to full conversation text, logs, and outputs programmatically.

### How do cloud agents handle environment access, files, and security compared to SSH-based setups?

Access is handled through Warp session sharing rather than SSH keys. Authentication is tied to Warp accounts and access controls, enabling secure person-to-person sharing.

Configuration files and credentials can be managed using encrypted .env workflows (for example, dotenv-style encryption), avoiding repeated manual decrypt/encrypt cycles.

### Can cloud agents review PRs like a teammate?

Yes. Common patterns for a **cloud agent** in PR review:

- Summarize changes and intent.
- Flag risky diffs and edge cases.
- Suggest tests and missing coverage.
- Propose refactors for maintainability.

A typical workflow is: the agent leaves structured review comments and optionally opens a follow-up PR for mechanical fixes (or commits to the branch, if you choose to allow that).

### Can cloud agents write unit tests?

Yes, especially when:

- The repo has a consistent test framework.
- The **environment** is reproducible (dependencies and setup are reliable).

The strongest loop is: a cloud agent generates tests, runs them in the environment, iterates until green, then opens a PR with the tests plus a short explanation of coverage and assumptions.

### Can cloud agents do big refactors?

It can help, but the best practice is to scope into smaller, reviewable chunks.

Agents are strongest when they can continuously validate progress (tests, lint, typecheck). For large refactors, a staged approach with checkpoints (and possibly multiple subagents for parallel exploration) tends to work better than one giant prompt.

### Can cloud agents triage issues / tickets automatically?

Yes. A common cloud agent workflow:

- When a ticket/issue is created (via integration trigger), a cloud agent gathers context (recent changes, logs/metrics links, ownership).
- Proposes labels/priority and likely causes.
- Drafts next steps or a response.
- Asks clarifying questions back to the reporter when needed.

### Can cloud agents do dependency upgrades?

Yes. Scheduled dependency bumps are a classic cloud agent use case:

- Open a PR.
- Run tests.
- Resolve simple conflicts.
- Attach a risk summary (optional).

This is usually implemented as a scheduled **cloud agent** producing recurring **runs**.

### Can cloud agents keep docs up to date?

Yes. With cloud agents, agents can:

- Scan for drift (commands that no longer work, onboarding steps that changed).
- Run validations in a docs/test environment.
- Propose doc updates as PRs.

This is most successful with “docs as code” workflows (GitBook/Mintlify/Docusaurus style), where updates go through normal review.

## Roadmap

### Does Warp have plans to improve workflows around Git worktrees?

This is an active area of interest, but there’s nothing to announce yet.