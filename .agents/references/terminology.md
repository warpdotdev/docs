# Warp terminology

Use this glossary everywhere you write about Warp. Keep definitions short, concrete, and consistent. If a term is likely unfamiliar outside developer audiences, include a short plain-language explanation you can reuse on first mention.

For the summary of the most critical terms (core features, Oz terms, terms to avoid), see the [Terminology standards](../../AGENTS.md#terminology-standards) section of AGENTS.md. This file is the full canonical reference.

> **Product name variables**: Product names are defined in `src/data/vars.ts`. When writing new content, use `{VARS.WARP_AGENT_CLI}` (body prose) or `{{WARP_AGENT_CLI}}` (frontmatter) rather than hardcoding product names. See the ["Content variables" section of AGENTS.md](../../AGENTS.md#content-variables) for full usage instructions.

## Core product terms

- **Agent** / **Agents** — Warp's AI feature for turning natural language into actions (answers, commands, code changes, and workflows).
  *Usage note:* Capitalize when referring to the feature: "Agent," "Agents."

- **Agent Mode** — The mode where Warp interprets your input as a request to an Agent (not a shell command).
  *Usage note:* Not "agent mode" or "Agent-mode."

- **Auto-detection Mode** — The mode where Warp automatically detects whether input is a command or a prompt.
  *Usage note:* Useful in onboarding and "how it works" content.

- **Block** / **Blocks** — Warp's structured unit of terminal output and history.
  *Usage note:* Use for navigation, sharing, and "how Warp organizes your terminal."

- **Command** — A shell command you run in the terminal.
  *Usage note:* Keep distinct from "prompt."

- **Prompt** — A natural-language request you give to an Agent.
  *Usage note:* Keep distinct from "command."

- **Terminal Mode** — The mode where Warp interprets your input as shell commands.
  *Usage note:* Use when contrasting with Agent Mode.

- **Universal Input** — Warp's main input surface that supports both commands and Agent prompts.
  *Usage note:* Use as the name of the feature, not "input box."

- **Warp** — The agentic development environment for professional developers, built around a modern terminal and AI agents.
  *Usage note:* Use "Warp" as the product name. Add "AI terminal" only when you need the positioning shorthand. Do not use "Warp Terminal" unless specifically distinguishing from Oz.

## Navigation and UI terms

- **Admin Panel** — The team administration interface.
  *Usage note:* Capitalize as a UI name.

- **Agent Management Panel** — The interface for managing Agent configurations, permissions, and activity.
  *Usage note:* Capitalize as a UI surface name. Avoid "agent dashboard," "dashboard of agents," or "agent manager."

- **Command Palette** — The searchable menu for actions and navigation in Warp.
  *Usage note:* Capitalize as a UI name.

- **Session** — A terminal session context (often tied to a tab/pane).
  *Usage note:* Don't use "session" to mean "conversation."

- **Settings** — Warp's configuration interface.
  *Usage note:* Capitalize as a UI name. The Settings sidebar has three **umbrellas** (**Agents**, **Code**, and **Cloud platform**) that expand into subpages — always reference the specific subpage in paths, not the umbrella alone.
  - **Agents** umbrella subpages: **Oz**, **Profiles**, **MCP servers**, **Knowledge**, **Third party CLI agents**.
  - **Code** umbrella subpages: **Indexing and projects**, **Editor and Code Review**.
  - **Cloud platform** umbrella subpages: **Environments**, **Oz Cloud API Keys**.
  - Deprecated labels to avoid:
    - **Settings** > **AI** — now under the **Agents** umbrella; pick the relevant subpage (**Oz** for the global toggle + Active AI/Input/Voice/Other/Experimental; **Profiles** for permissions and allow/denylists; **Knowledge**; **Third party CLI agents**).
    - **Settings** > **Platform** — now **Settings** > **Cloud platform** > **Oz Cloud API Keys** for `oz agent` API keys.
    - **Settings** > **MCP Servers** (top-level) — now **Settings** > **Agents** > **MCP servers**.
    - **Settings** > **Environments** (top-level) — now **Settings** > **Cloud platform** > **Environments**.

- **Tab** / **Pane** / **Window** — Warp's layout primitives: tabs within windows; panes are splits inside a tab/window.
  *Usage note:* Use precisely to avoid confusing layouts.

- **Tab Configs** — Reusable TOML-based tab layout definitions that launch preconfigured terminal sessions.
  *Usage note:* Capitalize as a feature name.

- **Vertical Tabs** — The sidebar-based tab management panel that replaces the horizontal tab bar.
  *Usage note:* Capitalize as a feature name.

## Agent concepts

- **Cloud Agents** — Agents that run in the cloud on a schedule, trigger, or integration, without interactive input. Managed by the Oz Platform.
  *Usage note:* Use lowercase "cloud agents" in most contexts. Capitalize as "Cloud Agents" only when referring to the product section or feature name.

- **Agent Profiles** — Saved configurations that define how an Agent runs (for example, permissions and model selection).
  *Usage note:* Use when describing "choose how your Agent behaves."

- **Context** — Inputs attached to a prompt to improve accuracy (files, Blocks, images, URLs, selections).
  *Usage note:* Prefer "attach context" / "add context."

- **Conversation** — A threaded interaction with an Agent, including history and attached context.
  *Usage note:* Use "conversation" consistently in product and support content.

- **Global Rules** — Rules that apply across all projects.

- **Permissions** — Controls for what an Agent is allowed to do (run commands, edit files, access tools).
  *Usage note:* Use for safety, review, and trust messaging.

- **Project Rules** — Rules that apply within a specific repo, stored in `WARP.md`.

- **Rules** — Saved guidelines that steer how Agents respond and behave.
  *Usage note:* Treat as a feature name.

- **Slash Commands** — Built-in commands you run by typing `/` to trigger actions (or run saved prompts).

- **Agent Memory** — Oz's persistent, cross-harness memory layer that lets agents read and write durable knowledge across conversations, harnesses, and devices. Currently in research preview.
  *Usage note:* Capitalize as a feature name. Lowercase "memory" only when describing the generic concept (e.g., "the memory layer").

- **memory store** — A named collection of memories owned by a user (personal) or team. Multiple agents can share a store, and per-agent attachments control read/write access.
  *Usage note:* Lowercase common noun. Capitalize the first letter only at the start of a sentence or bullet.

- **Handoff** — The feature for moving an agent's work between a local Warp session and the cloud, or continuing a finished cloud run. Supports local-to-cloud, cloud-to-cloud, and cloud-to-local directions.
  *Usage note:* Capitalize as a feature name. Use lowercase "hand off" / "handed off" only as a verb.

- **Active AI** — The feature that proactively surfaces fixes and next actions based on terminal errors, inputs, and outputs. Covers Prompt Suggestions, Next Command predictions, and Suggested Code Diffs.
  *Usage note:* Always capitalize "Active AI" — it is a proper feature name and the label of the Settings toggle. Write the full capability as **Active AI Recommendations**, matching the page title. Lowercase the following word only when it is a plain common noun rather than part of the name, as in "Active AI features" or "the Active AI toggle".

## Coding terms (Warp features)

- **Code** — Warp's coding experience for agent-assisted changes (editing, diffs, code review).
  *Usage note:* Use when describing "prompt-to-change" workflows.

- **Codebase Context** — Warp's ability to index a Git-tracked repo so Agents can understand the full codebase.
  *Usage note:* Good first-mention explanation: "Codebase Context helps Agents find the right files and make accurate repo-wide changes."

- **Code Review** — Warp's diff review experience for inspecting, refining, and applying code changes.
  *Usage note:* Treat as the feature name.

## Warp Drive terms

- **Environment Variable** / **Environment Variables** — Saved environment variables in Warp Drive, shared across sessions and teams.
  *Usage note:* Capitalize when referring to the Warp Drive feature; lowercase when referring to generic shell environment variables.

- **Notebook** / **Notebooks** — Rich documents in Warp Drive for sharing instructions, runbooks, and runnable content.

- **Prompt** / **Prompts** — Saved natural-language prompts in Warp Drive, reusable across conversations.
  *Usage note:* Capitalize when referring to the Warp Drive object type. Use lowercase "prompt" when referring generically to any natural-language request given to an Agent.

- **Warp Drive** — Warp's place to save and reuse developer artifacts (Workflows, Notebooks, Prompts, Rules, Environment Variables).
  *Usage note:* Good first-mention explanation: "Warp Drive is where Warp stores reusable pieces of your workflow."

- **Workflow** / **Workflows** — Saved, runnable workflows in Warp Drive (often multi-step command sequences).

## Oz terminology

### Warp Agent vs Oz

- **Warp Agent** — Warp's built-in agent harness. Capitalized, singular, treated as a proper noun. Use "Warp Agent" when specifically referring to the built-in harness, especially when contrasting with third-party agents (Claude Code, Codex, etc.), or when referencing the Settings label (**Settings** > **Agents** > **Warp Agent**). Use lowercase "agent" / "agents" everywhere else.
  *Usage note:* Avoid "Warp's agent" and "Warp's agents" — the ambiguous middle ground, and the main source of capitalization drift in the docs. Rewrite as "the Warp Agent" (the built-in harness), "agents" or "agents in Warp" (generic), or "the Warp Agent harness" (the server-side runtime).
  *Usage note:* In prose the term takes the definite article — "the Warp Agent". Reserve the bare form for headings, sidebar labels, page titles, and the Settings path. "Runs the Warp Agent" reads correctly; "runs Warp Agent" reads as a different product.
- **Oz is the platform, not the agent.** Never introduce Oz as "Warp's agent" or equate the two. Oz runs and coordinates agents; the Warp Agent is the agent.
- **Warp Agent CLI** — The standalone terminal program (the `warp` binary) that runs the Warp Agent in any terminal, including over SSH and on machines without the Warp app. Documented at `/agents/cli/`.
  *Usage note:* Distinct from the Oz CLI (the `oz` binary), which runs and manages cloud agents. At the next launch (approximately August 18, 2026) the Oz CLI is retired and wrapped into the Warp Agent CLI, leaving a single CLI under this name. Until that ships, keep the two clearly separate in prose; afterwards, "Warp Agent CLI" covers both.
- **Oz** — Warp's programmable platform for running and coordinating agents at scale
- There is typically one Warp environment per user session. Oz can run many agents concurrently, across machines, repos, and teams.

### Core terms

- **agent** — A combination of agent instructions (skill or prompt), trigger (cron, webhook, manual), environment (local, cloud), profile, and host. Agents can be local or cloud. Use lowercase "agent" in most contexts; use "Warp Agent" only when referring specifically to the built-in Warp harness.
  *Example:* Launch an agent from the CLI, the web app, an API or SDK, or directly inside Warp.

- **cloud agent** — An agent running in the cloud, from a trigger, schedule, or started from someone's local machine.

- **conversation** — An interactive execution lifecycle within the Warp Terminal, regardless of whether it's local or in the cloud.

- **Environment** — The execution context for an agent, including repo access, dependencies, secrets, compute, and runtime configuration.

- **Oz** — Warp's programmable platform for running and coordinating agents at scale.
  *Example:* With Oz, you can orchestrate multiple agents to automate and parallelize complex workflows.

- **Oz dashboard** — The app surface to manage all Oz runs, unified across the Warp app and web.

- **Oz run** — A single execution lifecycle of an agent, including actions, outputs, and logs. An Oz run is always cloud-based.

- **Oz web app** — The web app for configuring agents and managing runs.

- **subagent** — A child agent created by a parent agent to parallelize or delegate work.

### Oz CLI commands

- `oz agent run` — Run a local agent
- `oz agent run-cloud` — Run an adhoc cloud agent
- `oz environment create/list/get/update/delete` — CRUD on environments
- `oz integration create` — Install integrations (Slack, Linear)
- `oz run list/get` — Get info on cloud agent runs
- `oz schedule create/list/get/update/delete` — CRUD on scheduled cloud agents
- `oz secret create/list/update/delete` — CRUD on Warp-managed secrets

### Preferred phrases

- ✅ "Ask Oz to..."
- ✅ "Oz can help you..."
- ✅ "What would you like Oz to do?"

### Terms to avoid

- ❌ "Oz agent" / "Oz agents" → Use "agent" / "agents" (or "Warp Agent" / "Warp Agents" when referring to the built-in harness)
- ❌ "Oz cloud agent" → Use "cloud agent"
- ❌ "Oz subagent" → Use "subagent"
- ❌ "Oz conversation" → Use "conversation"
- ❌ "Ozzies" → Use "agents", "instances", or "subagents"
- ❌ "Deploying an Oz" → Use "Deploying an agent"
- ❌ "The Oz Agent" → Use "the agent" or "the Warp Agent"
- ❌ "Oz is running" → Use "An agent is running" or "A run is in progress"
- ❌ "AI agents" → Use "agents" (the "AI" prefix is redundant)
- ❌ "Ambient Agents" / "ambient agents" → Use "Cloud Agents" / "cloud agents" ("ambient" is no longer a product term; acceptable only in code identifiers like `AmbientAgentConfig`)
- ❌ "agent identity" / "agent identities" → Use "agent," "agents," or "cloud agent(s)" in user-facing copy. Use legacy API names such as `agent_identity_uid` or `/agent/identities` only when documenting the exact field, path, or compatibility behavior.

## Platform terms

- **Agent API** — The HTTP API for triggering and inspecting Platform runs programmatically.

- **Host** — Where a task executes (Warp-hosted or customer-hosted).

- **Integration** / **Integrations** — Configured connections between Warp and external tools (Slack, Linear, GitHub Actions) that trigger runs and post results back.
  *Usage note:* Use for the configured connection, not "plugin."

- **Outputs** — What a run produces (PRs, messages, reports, transcripts).

- **Run** — The tracked unit of work for a run, including status and outputs.
  *Usage note:* Use when describing observability, history, and auditability.

- **SDK** — Official client libraries for the Agent API (for example, TypeScript SDK, Python SDK).
  *Usage note:* Spell out the language on first mention.

- **Trigger** — The event that starts a run (Slack mention, schedule, CI event, API call).

- **Warp CLI** — Ambiguous since the Warp Agent CLI launched; avoid the bare term. Use "Oz CLI" for the `oz` binary that runs and manages cloud agents (formerly called `warp-cli`), or "Warp Agent CLI" for the `warp` binary that runs the Warp Agent in any terminal.

## Technical terms

- **AI** — not "A.I." Normalize all instances to "AI."
- **allowlist** / **denylist** — use instead of "whitelist" / "blocklist"
- **codebase** — one word, lowercase (unless part of a feature name like "Codebase Context")
- **command-line** — hyphenated when used as an adjective
- **Git repository** or **repo** — not "git repository" (capitalize "Git")
- **macOS** — not "Mac OS" or "Mac"

## Branded and informal terms

- **Warpify** / **Warpification** — Productized terms for enabling Warp features in SSH and subshell sessions.
  *Usage note:* Acceptable in docs. Used across Warpify documentation and changelogs.

- ❌ **Warping** — Avoid ad-hoc verbing ("Warping into a session"). Use "using Warp" or the specific action ("open in Warp," "enable Warpify").

- ❌ **YOLO mode** — Avoid in formal docs and UI copy. Prefer "Run until completion" or "Full autonomy." Acceptable only as a colloquial parenthetical if absolutely necessary.

## Open source

- **`warpdotdev/warp`** — The public, open source repository for Warp's client at [github.com/warpdotdev/warp](https://github.com/warpdotdev/warp). Use this as the canonical link when pointing readers at the source code.
  *Usage note:* Lowercase `warp` in the repo path. The display org/name appears in code-formatting; do not write "`Warpdotdev/Warp`" or "`warpdotdev/Warp`."

- **AGPL v3** — The license under which Warp's client is published.
  *Usage note:* Write as "AGPL v3," not "AGPLv3," "AGPL-3.0," or "GNU AGPLv3." Link the first mention to the `LICENSE` file in the repo.

- **open source** — Preferred phrasing when describing Warp.
  *Usage note:* Lowercase "open source" (no hyphen) in prose, except in quoted feature names. Both "Warp is an open source Agentic Development Environment" and "Warp's client is open source under AGPL v3" are acceptable. Use the shorter framing for landing pages and marketing-adjacent copy; use the longer framing when the client/server distinction matters (security pages, contributor docs).

- **`warp-oss`** / **WarpOss** — The OSS build identity. Lowercase `warp-oss` for the binary, CLI references, and per-channel data dirs (`~/.warp-oss` on macOS, `~/.local/share/warp-oss` on Linux, `AppData\warp\WarpOss` on Windows). CamelCase `WarpOss` for the macOS app bundle name.
  *Usage note:* Use only when documenting self-built binaries or the OSS channel. Do not use for the official Warp app.

- ❌ **OpenWarp** — Pre-launch internal codename for the OSS build. Replaced by `warp-oss` / `WarpOss` in 2026-04. Do not use anywhere in docs.

## Billing and credits

- **Add-on Credits** — capitalized as a product feature name
- **Auto-reload** — the setting that automatically purchases another add-on credit pack when a user's balance drops below 100 credits. Hyphenated; capitalize the first letter only at the start of a sentence, bullet, or bolded list term.
- **team-wide spend cap** — the admin-configured monthly ceiling on add-on credit spending across a whole team. Use instead of "budget" or "credit limit" when describing the cap. The per-account wording "monthly spend limit" refers to the same setting in single-user contexts.
- **compute credits** — lowercase common noun; capitalize the first letter only at the start of a sentence or bullet. The compute bucket, consumed when an agent run uses Warp-hosted compute. Use alongside AI credits and platform credits when describing credit types.
- **cloud agent credits** — lowercase common noun; capitalize the first letter only at the start of a sentence or bullet. Credits consumed by cloud agents, in contrast with local agent credits. Refers to the same compute bucket as compute credits; choose the term that fits the framing.
- **platform credits** — lowercase common noun; capitalize the first letter only at the start of a sentence or bullet. The platform-infrastructure bucket, consumed for every cloud agent run plus local runs with customer-supplied inference.
- **credits** — the unit of usage for AI features in Warp (lowercase, not "AI credits")
- **Warp credits** — credits included with a subscription plan. Use in user-facing copy rather than "plan credits."

## External product names

- **GitHub Actions** — capitalize "GitHub"
- **GitHub App** — GitHub's installation/auth mechanism used for repo access in integrations
- **Linear** — capitalize
- **Slack** — capitalize
