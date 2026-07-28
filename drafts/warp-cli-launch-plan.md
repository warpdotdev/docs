# Warp CLI launch — internal docs plan

Status: planning scaffold for the Warp CLI (TUI) launch docs.
Docs owner: Hong Yi Chen. Eng lead: Kevin Yang.
Feature source of truth: Linear project "TUI" (linear.app/warpdotdev/project/tui-47ce492eb0d5). Milestones: Dogfood (done), **Stable = launch scope**, Fast follows (post-launch unless already Done).

This file is internal planning material: do not publish it or link it from published pages. It intentionally contains Linear IDs and engineer names; **published pages must contain neither**.

## Naming

- Product name in docs: **Warp Agent CLI** (confirmed via the launch blog draft, 2026-07-28).
- Body prose uses `{VARS.WARP_CLI}` (key stays `WARP_CLI`; value is "Warp Agent CLI"). Frontmatter uses the literal string — `{{TOKEN}}` substitution does not work in content-layer frontmatter (Astro parses it outside Vite), so titles/descriptions are literals.
- UNRESOLVED: the pre-existing `WARP_AGENT_CLI` var ("Oz CLI") was reserved for renaming the Oz CLI to "Warp Agent CLI" — the TUI product now takes that name, so the Oz CLI rename plan conflicts. Needs Kevin/marketing decision before launch.
- The command is `warp` (binary renamed from `warp-tui`, CODE-1875). It runs the Warp Agent harness (`platform/harnesses/warp-agent`).

## Scope rules

- Public-facing behavior only. Never mention: feature flags, dogfood/preview gating, internal crate/module names (`warp_tui`, `blocklist`, "HoA", etc.), Linear IDs, or engineer names.
- Launch scope = Stable-milestone tickets that are Done (or verified shipped in code), plus Dogfood-milestone work. Fast-follow items are excluded unless already Done (e.g. tab completions CODE-1853 is Done — verify, then include).
- Verify every claim against the `warpdotdev/warp` repo on `master` (`crates/warp_tui/`, `app/src/search/slash_command_menu/static_commands/commands.rs`, `specs/tui-*`, `specs/code-1822-*`) — not against Linear titles alone.
- Cross-link canonical concept docs instead of duplicating them (skills, MCP, BYOK, model choice, handoff, profiles under `agent-platform/` and `platform/`). CLI pages document CLI-specific behavior and UI only.
- Open-source messaging: overview gets a short "Open source" section — "we plan to open source the Warp CLI", no dates, no license commitments. Needs marketing sign-off before launch.

## Skeleton

New sidebar topic **Warp CLI** → `src/content/docs/cli/` (URLs under docs.warp.dev/cli/):

- `cli/index.mdx` — overview + open source section
- `cli/quickstart.mdx` — install, login, first prompt
- `cli/agent-conversations.mdx` — transcript, tool calls, diffs, questions, tasks, planning
- `cli/shell-commands.mdx` — shell mode, NLD, history, long-running commands
- `cli/input-and-editing.mdx` — slash menu, completions, mouse, images, voice, vim
- `cli/permissions-and-profiles.mdx` — approvals, auto-approve, fast-forward, profiles
- `cli/conversations.mdx` — persistence, history, compact, resume
- `cli/cloud-and-orchestration.mdx` — handoff, cloud resume, multi-agent
- `cli/context.mdx` — rules/AGENTS.md, skills, MCP
- `cli/configuration.mdx` — settings file, themes, statusline, keybindings
- `cli/models-and-usage.mdx` — model picker, BYOK, routing, cost
- `cli/reference.mdx` — flags, env vars, slash commands, shortcuts
- `cli/troubleshooting.mdx` — logs, login issues, updating

## Page inventory (features → tickets → reviewer)

### cli/index.mdx + cli/quickstart.mdx — agent `cli-overview` — reviewer: Kevin
- What the Warp CLI is; relationship to the Warp app and Oz; Warp Agent harness link.
- Install + supported platforms: macOS now; Linux/Windows bundling CODE-1874 **in progress — confirm before merge**; binary bundling CODE-1803; rename CODE-1875.
- Autoupdate CODE-1812 (managed versioned layout).
- Login: device-auth flow, login screen (APP-4937, CODE-1860); `--api-key` / `WARP_API_KEY` for non-interactive auth; `/logout` + web sign-out (APP-4919, APP-4977).
- Zero state (CODE-1823, CODE-1876): directory path, hints, version line.
- Open source section (messaging only).
- Bundled migration skill for GUI users (CODE-1872) — mention in overview "coming from the Warp app".

### cli/agent-conversations.mdx — agent `cli-agent-conversations` — reviewers: harry + ian (moira for markdown)
- Streaming transcript view (CODE-1798), markdown rendering (CODE-1849, APP-4886), mermaid (CODE-1850).
- Tool-call rendering (CODE-1799, CODE-1815, CODE-1814), file-edit diffs (CODE-1810, CODE-1800), expand/collapse + `e` expand-all (APP-5011).
- Thinking blocks (CODE-1801).
- Agent questions: interactive ask-question tool (CODE-1846, CODE-1855), "(recommended)" answers (APP-5018 — in review, confirm).
- Agent task lists (CODE-1829).
- Planning with `/plan` (CODE-1817).
- Selection/copy in transcript (CODE-1806, CODE-1883, APP-4994 auto-copy opt-in).

### cli/shell-commands.mdx — agent `cli-shell-commands` — reviewer: Kevin (moira for manual attach)
- Shell mode + prompt styling (CODE-1805, CODE-1892); yellow command rows (APP-4900).
- Natural language detection: opt-in, `/natural-language-detection` toggle (CODE-1848, CODE-1893).
- Shell command history in up-arrow menu (CODE-1906).
- Long-running/interactive commands (CODE-1819, CODE-1838, CODE-1857): input passthrough, typed-char carryover (CODE-1895), ghost hints during LRC (CODE-1900).
- Alt-screen/full-screen apps (CODE-1844, CODE-1922); manual attach (CODE-1915 — in progress, confirm).
- Ctrl+C stop vs double-Ctrl+C exit (CODE-1811); exit confirmation.

### cli/input-and-editing.mdx — agent `cli-input` — reviewers: Kevin + moira (ian for hints)
- Slash command menu UI (CODE-1818); argument hints.
- Up-arrow prompt history (CODE-1871).
- Tab completions for shell commands (CODE-1853 — Done under Fast follows, verify shipped).
- Mouse: selection in input (CODE-1804), inline-menu clicks (APP-5008 — in review, confirm), selection persistence (CODE-1841).
- Attach images (CODE-1881).
- Voice input: `/voice`, Ctrl+S, configurable keybinding (CODE-1884, APP-4988).
- Vim mode (CODE-1926 — in review, confirm before merge).
- Ghost-text keybinding hints (CODE-1889 + CODE-1897/1898/1899/1901).
- Shortcuts menu (CODE-1907).
- Soft-wrapping (CODE-1843) — mention only if user-visible behavior worth documenting.

### cli/permissions-and-profiles.mdx — agent `cli-permissions` — reviewer: harry
- Permission request cards for tool calls (CODE-1809); code-diff approval card behavior (APP-5011).
- Default execution profile: "agent decides" for shell commands (CODE-1908).
- Settings-file-based execution profiles (CODE-1880, APP-5021).
- `/auto-approve` toggle.
- Fast-forward mode (CODE-1858) + `/fast-forward` toggle & dynamic hint (APP-4901).
- `--dangerously-skip-permissions` (APP-4992 — **backlog, confirm shipped or drop**).
- Cross-link: agent-platform/capabilities/agent-profiles-permissions.

### cli/conversations.mdx — agent `cli-conversations` — reviewer: harry
- Conversation persistence + restore (CODE-1820, CODE-1917 diff rehydration fixed).
- Conversation management: `/conversations` menu, left-arrow at start opens list (CODE-1821, CODE-1868).
- `/new`, `/agent`, `/clear` (APP-5023).
- `/compact` + styling (CODE-1919); context management.
- Exit summary + `--resume <token>` (session exit prints resume command).
- Multiple in-progress conversations (CODE-1845 — **backlog, confirm or drop**).

### cli/cloud-and-orchestration.mdx — agent `cli-cloud-orchestration` — reviewer: harry
- `/handoff` to cloud agents (CODE-1827); what carries over.
- Resuming/viewing cloud conversations in the CLI (CODE-1925 public angle: continue cloud runs in the CLI; keep internal compat details out).
- Multi-agent orchestration (CODE-1822 family): tab bar, child agents, cloud children.
- Kill a child agent with Ctrl+C (APP-5031 — in progress, confirm).
- Orchestration-aware hints (CODE-1901).
- Cross-link: platform/orchestration, platform/handoff.

### cli/context.mdx — agent `cli-context` — reviewers: Kevin + moira
- Project context: AGENTS.md/rules pickup (CODE-1826); working-directory context.
- Skills: `/skills` invoke, skills menu (CODE-1824); bundled skills: update-settings (CODE-1869), migrate-from-GUI (CODE-1872).
- MCP: `/mcp` manage view (CODE-1825); project-scoped servers (CODE-1863 — **confirm shipped**); import/discovery (CODE-1864 — fast follow, exclude unless Done).
- Cross-link: agent-platform/capabilities/skills, agent-platform/capabilities/mcp.

### cli/configuration.mdx — agent `cli-configuration` — reviewers: Kevin + moira
- TOML settings file (CODE-1802): location, local-only (never cloud-synced — settings mode is TUI-specific), schema pointers.
- Edit settings by asking the agent (bundled skill CODE-1869).
- Themes: `/theme` auto|light|dark (CODE-1916), terminal-background detection (CODE-1807), live refresh (CODE-1909 — in review, confirm).
- Statusline: V2 (CODE-1890) + `/statusline` customization (CODE-1891 — in review, confirm).
- Keybindings: customization support; cmd-modified keys (CODE-1920 — backlog, likely drop).

### cli/models-and-usage.mdx — agent `cli-reference` (bundle) — reviewers: harry + ian + moira
- `/model` picker; footer model click (APP-4908); per-profile default model (APP-4916 fixed behavior).
- BYOK: `/add-api-key`, `/clear-provider-api-key`, `--set-provider-api-key`, `--clear-provider-api-key` (CODE-1923); Grok (APP-5024 — in review, confirm); no-credit-charge behavior when BYOK active.
- Custom model routing (CODE-1914 — in progress, confirm or drop).
- Cost transparency (CODE-1828): footer credits + click-to-toggle (CODE-1831), `/cost` (APP-4924), last-response duration + credits (CODE-1832).
- Cross-link: agent-platform/inference/* pages.

### cli/reference.mdx — agent `cli-reference` — reviewers: harry + Kevin
- Flags (from `crates/warp_tui/src/session.rs`): `--resume`, `--api-key` (env `WARP_API_KEY`), `--set-provider-api-key`, `--clear-provider-api-key`, `--version`, `--help`.
- `--list-models`, headless run (APP-4993, CODE-1924 — **not shipped, exclude unless landed**).
- Slash command table — source: `static_commands/commands.rs`, include only `TuiOnly` + `GuiAndTui` commands actually reachable in the CLI. Currently: /agent, /new, /clear, /plan, /compact, /model, /cost, /conversations, /skills, /handoff, /export-to-clipboard, /export-to-file, /create-new-project, /theme, /statusline, /auto-approve, /natural-language-detection, /mcp, /add-api-key, /clear-provider-api-key, /voice, /view-logs, /version, /logout, /exit. Confirm at write time: /status (APP-4973), /copy-debugging-link (APP-5030), /fast-forward (APP-4901), /pr-comments display (CODE-1918).
- Keyboard shortcuts table (shortcuts menu CODE-1907 as source).

### cli/troubleshooting.mdx — agent `cli-reference` — reviewers: harry + Kevin
- `/view-logs` bundle (CODE-1882); log locations (CODE-1902).
- `/copy-debugging-link` (APP-5030 — in progress, confirm).
- Login troubleshooting (device-auth issues); `/version`; updating (autoupdate CODE-1812).
- Sending feedback; link to support pages.

## Reviewer map (summary)

- **Kevin Yang** — overview/install/login/autoupdate, shell & NLD & long-running commands, MCP & project context, settings file & themes, vim mode, images, shortcuts menu.
- **harry** — permissions/profiles/fast-forward, conversations/resume, handoff & orchestration, BYOK, transcript/tool calls/diffs, logs & troubleshooting.
- **moira** — slash command UI, skills, planning, markdown/mermaid, statusline, custom routing, tab completions, login/logout UX, /cost /logout.
- **ian** — agent questions, task lists, cost transparency, keybinding hints.

## Workflow

- Base branch: `hyc/launch-cli` (this skeleton). One agent per page bundle, branch `hyc/launch-cli-<name>`, git worktree, PR into `hyc/launch-cli`.
- Each PR body lists: pages, features covered, dropped "confirm" items with reasons, and the suggested eng reviewer (Hong Yi tags them).
- Validation per PR: `npm run build` green.
- Launch: single PR `hyc/launch-cli` → `main`, timed with the release.

## Open questions

- Final name: "Warp CLI" vs "Warp Agent CLI" (and the `WARP_AGENT_CLI` var collision with the Oz CLI rename).
- Distribution/install channels (brew? curl script? winget?) and Linux/Windows timing — need Kevin's confirmation.
- Screenshot/asciinema pass: do after content lands; assets go to `src/assets/cli/`.
