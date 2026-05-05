# Warp terminology

Use this glossary everywhere you write about Warp. Keep definitions short, concrete, and consistent. If a term is likely unfamiliar outside developer audiences, include a short plain-language explanation you can reuse on first mention.

For the summary of the most critical terms (core features, Oz terms, terms to avoid), see the [Terminology standards](../../AGENTS.md#terminology-standards) section of AGENTS.md. This file is the full canonical reference.

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

## Agent concepts

- **Ambient Agents** — Oz agents that run automatically in the background on a schedule or trigger, without interactive input.
  *Usage note:* Capitalize as a feature/section name. Use lowercase "ambient agents" only when describing the generic concept of agents running in the background.

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

### Oz vs Warp

- **Warp** is the terminal and coding surface
- **Oz** is Warp's programmable agent for running and coordinating agents at scale
- There is typically one Warp environment per user session. Oz can run many agents concurrently, across machines, repos, and teams.

### Core Oz terms

- **Environment** — The execution context for an Oz agent, including repo access, dependencies, secrets, compute, and runtime configuration.

- **Oz** — Warp's programmable agent for running and coordinating agents at scale.
  *Example:* With Oz, you can orchestrate multiple agents to automate and parallelize complex workflows.

- **Oz agent** — A combination of agent instructions (skill or prompt), trigger (cron, webhook, manual), environment (local, cloud), profile, and host. Agents can be local or cloud, and interactive or ambient.
  *Example:* Launch an Oz agent from the CLI, the web app, an API or SDK, or directly inside Warp.

- **Oz cloud agent** — An Oz agent running in the cloud, from a trigger, schedule, or started from someone's local machine. Cloud agents can be interactive or ambient.

- **Oz conversation** — An interactive execution lifecycle within the Warp Terminal. An Oz conversation is interactive, started in the terminal regardless of whether it's local or in the cloud.

- **Oz dashboard** — The app surface to manage all Oz runs, unified across the Warp app and web.

- **Oz run** — A single execution lifecycle of an Oz agent, including actions, outputs, and logs. An Oz run is always ambient and cloud-based.

- **Oz subagent** — A child Oz agent created by a parent Oz agent to parallelize or delegate work.

- **Oz web app** — The web app for configuring Oz agents and managing runs.

### Oz CLI commands

- `oz agent run` — Run a local agent
- `oz agent run-cloud` — Run an adhoc cloud agent
- `oz environment create/list/get/update/delete` — CRUD on environments
- `oz integration create` — Install integrations (Slack, Linear)
- `oz run list/get` — Get info on ambient agent runs
- `oz schedule create/list/get/update/delete` — CRUD on scheduled ambient agents
- `oz secret create/list/update/delete` — CRUD on Warp-managed secrets

### Preferred phrases

- ✅ "Ask Oz to..."
- ✅ "Oz can help you..."
- ✅ "What would you like Oz to do?"

### Terms to avoid

- ❌ "Ozzies" → Use "Oz agents", "instances", or "Oz subagents"
- ❌ "Deploying an Oz" → Use "Deploying an Oz agent"
- ❌ "The Oz Agent" → Use "An Oz agent" or "A parent Oz agent"
- ❌ "Oz is running" → Use "An Oz agent is running" or "A run is in progress"
- ❌ "AI agents" → Use "agents" (the "AI" prefix is redundant)

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

- **Warp CLI** — The command-line tool for running and managing Warp Platform workflows. Formerly called `warp-cli`, now `oz`.

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
- **Cloud Agent Credits** — capitalized as a billing feature name
- **credits** — the unit of usage for AI features in Warp (lowercase, not "AI credits")
- **plan credits** — credits included with a subscription plan

## External product names

- **GitHub Actions** — capitalize "GitHub"
- **GitHub App** — GitHub's installation/auth mechanism used for repo access in integrations
- **Linear** — capitalize
- **Slack** — capitalize
