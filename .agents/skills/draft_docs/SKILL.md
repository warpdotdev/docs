---
name: draft_docs
description: Draft new Warp documentation pages or update existing ones using established style conventions, with optional source code context from warp-internal and warp-server.
---

# Draft Docs

This skill guides the process of drafting new documentation pages or updating existing ones for Warp's documentation (referred to as "docs"), which lives at https://docs.warp.dev. All style rules, content type structures, formatting standards, and terminology live in `AGENTS.md` at the docs repo root. That file is the single source of truth and must be read before drafting new docs.

## How to use

Invoke this skill with any context that describes what you want to document:
- PRDs or feature specs
- Slack threads or meeting notes
- Existing documentation that needs updating
- A description of a feature or concept
- AEO, SEO, Peec, or answer-engine source data that should inform a draft

Example: "Use the draft_docs skill to write docs for [feature name] based on this PRD: [context]"

## Workflow

When this skill is invoked, follow these steps in order:

### 1. Gather context
Review all provided context (PRD, spec, existing doc, etc.). Identify:
- What feature or topic is being documented
- Key user benefits and capabilities
- Technical details that need explaining

**If no spec was provided, go looking for one.** "Provided" assumes a requester, and a
scheduled run has none — which is how automated drafts end up with an audience invented from a
one-line changelog bullet. Check warp-server for a `specs/<id>/PRODUCT.md` matching the
feature. Only some specs have one, and `TECH.md` is the implementation plan, not the product
reasoning.

Use it for framing only: audience, problem, goals, and explicit non-goals. Per step 6 it is
never verification for labels, flags, or defaults, and it is never evidence that a feature
shipped. Never quote it into a page — warp-server is private and specs describe unshipped
plans. If none exists, proceed without one and note the absence in the content design plan
rather than inventing an audience.

### 1.5. Create an AEO brief when source data drives the request
If the request mentions AEO, SEO, Peec, answer-engine visibility, search-query vocabulary, content gaps, or whether to create a new page versus update an existing page, read `.agents/skills/aeo_brief/SKILL.md` and create the brief before drafting. Use the brief to decide:
- Which page or section should change
- Which user/search vocabulary belongs in the draft
- Which product terms or UI surfaces need precise naming
- Which topics to avoid because they duplicate existing docs or create a junk-drawer page
- Which questions require human review before publishing

### 2. Clarify placement
Ask the user where the doc should live. The docs are organized into sections, with navigation configured in `src/sidebar.ts`:
- `src/content/docs/` - Warp Terminal and IDE → `docs.warp.dev/`
- `src/content/docs/agent-platform/` - Agent Platform → `docs.warp.dev/agent-platform/`
- `src/content/docs/reference/` - Technical reference (CLI, API & SDK) → `docs.warp.dev/reference/`
- `src/content/docs/support-and-community/` - Support → `docs.warp.dev/support-and-community/`
- `src/content/docs/enterprise/` - Enterprise → `docs.warp.dev/enterprise/`
- `src/content/docs/changelog/` - Changelog → `docs.warp.dev/changelog/`

Also clarify: Is this a new page or an update to an existing page?

### 3. Read the style guide
Read `AGENTS.md` in the docs repo root. This is required — it contains all voice/tone rules, formatting standards, content type structures, terminology, and the quality checklist. Do not draft without reading it first.

### 3.5. Confirm the doc should exist, then design it

Two gates, in order. Both come before you open a template.

**First, should this doc exist at all?** Apply `.agents/references/docs-worthiness-criteria.md`.

How much of the gate applies depends on who is asking:

- **Automated runs** (`missing_docs` drift-watch, or any scheduled agent) apply the **full gate**. The default is no docs and the burden is on the change to earn a page. Record the verdict with the gate it passed and the concrete evidence — a setting key, CLI flag, quoted error string, changed default, API field, or (for Gate 4) the newly possible job plus the in-product surfaces you checked and found silent. If nothing passes, say so and stop; "this is new and users should know about it" is not a reason to write a page.
- **A person asking directly** is subject to **Gate 0 only**. Gate 0 is a factual check — has this shipped, is the surface public — and a requester can simply be wrong about it, so verify it and stop if it fails. Drafting for an unshipped feature is the most common failure regardless of who asked.

  Gates 1 through 4 are judgment, and a person requesting the page usually has context you do not: the roadmap, the support queue, a conversation you were not in. **Do not decline their request on Gates 1-4.** If something looks off — an existing page already covers the surface, or the change looks like a pure UI affordance — say so once, then defer to their answer and proceed.

When the change passes, choose the outcome explicitly: **update an existing page** (preferred), **new page**, or **no docs**. Prefer updating whenever a page already covers the surface. When Gate 4 is the only gate it passed, the outcome is capped at an update.

**Second, what should the doc be?** Pick the form with the routing rule in `.agents/references/content-design-plan.md`: a new page gets the full form in `.agents/templates/content-design-plan.md`, an update that adds a concept gets the three-line short form, and a correction gets no plan. Use the reference for what each field is asking.

The plan decides the content type — step 4 records that decision rather than making it. Starting at the template produces pages shaped by the template instead of by the reader's need.

**When a person invoked this skill, present the plan and wait before drafting.** This is the checkpoint: redirecting the audience or content type now costs a conversation, and after the prose exists it costs a rewrite. Do not skip it just because the requester seems confident about what they want.

Carry the completed plan into the PR body as a `## Content design plan` section either way. In an unattended run there is no one to present it to, so the PR body is the only place a human will see the reasoning.

Small corrections listed under "When a plan can be skipped" in that reference are exempt from both gates.

### 4. Identify the content type and template
Record the content type chosen in the design plan, and pick its template and type-specific skill from this table. If drafting has diverged from the plan's chosen type, revisit the plan rather than silently switching templates.

| Content type | Use when | Template | Skill |
|---|---|---|---|
| **Conceptual** | Explains what/why, no procedures | `.agents/templates/conceptual.md` | `draft_conceptual` |
| **Procedural** | Step-by-step task instructions | `.agents/templates/procedural.md` | `draft_procedural` |
| **Quickstart** | Fast path to a working result | `.agents/templates/quickstart.md` | `draft_quickstart` |
| **Reference** | Structured information for lookup | `.agents/templates/reference.md` | `draft_reference` |
| **Troubleshooting** | Problem → cause → solution | `.agents/templates/troubleshooting.md` | `draft_troubleshooting` |
| **FAQ** | Rarely — cross-cutting questions with no canonical home | `.agents/templates/faq.md` | `draft_faq` |
| **Tutorial** | Full workflow walkthrough (Guides section) | `.agents/templates/guide-page.md` | `draft_guide` |
| **Feature documentation** | Combined conceptual + procedural (most common) | `.agents/templates/feature-doc.md` | `draft_feature_doc` |

Two of these carry admission rules rather than just structure, and both are checked in review:

- **FAQ** defaults to "not an FAQ." All three admission rules in `AGENTS.md` must hold before you create or extend one. Most FAQ-shaped content belongs on the page that owns the topic.
- **Quickstart vs. tutorial** is a scope decision, not a location one. A quickstart is ~5 minutes and ~600 words for someone who already knows the product; a tutorial walks a full workflow and requires that a quickstart already exists. "Guides" is the section name and holds both.

Once the content type is identified:
- Use the corresponding **template** as the starting scaffold for the page.
- If a **type-specific skill** exists (listed above), read it for additional rules and examples specific to that content type.
- Follow the structure and rules for the identified type in `AGENTS.md`.

### 5. Research existing patterns
Read 2-3 strong examples in the target section to match existing patterns and conventions.

### 6. Research source code (if needed)
For technical accuracy, optionally look in Warp's source repositories:
- **warp-internal** - Client-side code (Rust, Swift, etc.)
- **warp-server** - Server-side code (Go)

To find these repos, search for directories named `warp-internal` and `warp-server` on the user's machine. If not found, ask the user where the repos are located.

Use source code to verify technical behavior, understand feature implementation, and find accurate terminology.

When the draft names UI labels, Settings paths, CLI flags, default permissions, plan eligibility, or platform support, treat source (or a live build) as required verification, not optional color. A PRD or spec is not verification: labels and flag names routinely change between spec and ship.

If you cannot verify a claim (for example, the source repos are not available in this environment), do not guess and do not silently drop it. Choose one of these, and record the claim either way:

1. **Omit the claim** - Write around it when the page still works without it. Describe the action without naming the exact flag, or link to the reference page that will carry the detail.
2. **Include it with an inline marker** - Keep the spec's wording and flag it in an MDX comment next to the claim: `{/* VERIFY: flag name from PRD, unconfirmed against warp-internal */}`.

Keep a running list of every unverified claim as you draft. Reporting that list is required — see step 9.5.

### 6.5. Critical formatting rules

These rules are frequently violated by agents. Apply them carefully during drafting:

- **Product name variables** — For any product name in `src/data/vars.ts`, use the variable instead of the hardcoded string. Add `import { VARS } from '@data/vars';` immediately after the frontmatter closing `---`. Use `{VARS.KEY}` in MDX prose (e.g. `{VARS.WARP_AGENT_CLI}` not "Oz CLI"). Use `{{TOKEN}}` directly in frontmatter YAML values (e.g. `title: "{{WARP_AGENT_CLI}} reference"`). Key vars: `WARP_AGENT_CLI`, `WARP_AUTOMATION_PLATFORM`, `WEB_APP`, `WEB_APP_URL`, `DASHBOARD`, `AGENT_MODE`, `WARP_DRIVE`. See `src/data/vars.ts` for the full list.

- **Sentence case for all headings (H1–H4)** — Capitalize only the first word and proper feature names. ✅ `## How it works` ❌ `## How It Works`
- **Descriptive, specific headings** — Beyond correct case, a heading should name the specific topic so readers and agents can scan the page and extract a self-contained answer. Prefer the concrete object or outcome over a vague section label. ✅ `## How key type affects billing and GitHub access` / `## Configuring Workload Identity Federation` ❌ `## More details` / `## Overview` / `## Additional information` / `## Other`
- **Frontmatter `description` is a standalone search summary** — One to two sentences, roughly 50–160 characters, stating the user benefit and primary keywords. It must make sense out of context, in a search result or an AI citation. ✅ `description: Environments keep cloud agents on a consistent toolchain across every trigger.` ❌ `description: This page describes environments.` ❌ a description that only restates the title
- **Bold + dash format for list items** — `* **Term** - Description`, not `* Term: Description` and not `* **Term** — Description`. Use a hyphen with spaces around it as the separator after the bold term.
- **Unordered list marker is `*`** — Match the templates and existing docs. Reserve `-` for nested lists whose parent already uses `*`; use `1.` for numbered procedures. ✅ `* **Codebase Context** - Warp indexes your Git-tracked codebase` ❌ `- **Codebase Context** - ...` as the top-level marker on a new page
- **Tables or parallel bullets for comparison and reference data** — When you present two or more parallel items (key types, plan tiers, environments) or structured reference data (API endpoints, parameters), use a Markdown table or tightly parallel bullets instead of one dense paragraph. ✅ a table with one row per API endpoint, or parallel `**Personal API keys**` / `**Agent API keys**` bullet groups ❌ a single paragraph mixing both key types and their billing rules
- **Bold for UI elements** — Use `**Save**` not `` `Save` `` after action verbs like "click"
- **Quotes for non-clickable field labels** — If a name labels a field but is not itself clickable, put it in quotation marks, not bold. Bold only interactive controls with their own visible labels and the option the reader selects. ✅ `In the "Harness" dropdown, select **Claude Code** or **Codex**.` ❌ `In the **Harness** dropdown, select **Claude Code**.` ❌ `Choose **Claude Code** in the **Harness** field.`
- **Bold per-segment for Settings paths** — Use `**Settings** > **AI** > **Knowledge**` not `` `Settings > AI > Knowledge` ``
- **Orient the reader before every Settings path, CLI command, or URL** — On first reference in the page, name the app or tool. ✅ `In the Warp app, go to **Settings** > **AI** > **Knowledge**.` ❌ `Go to **Settings** > **AI** > **Knowledge**.`
- **Verify labels, flags, and defaults against source** — Before documenting a button name, Settings path, CLI flag, permission default, or eligibility rule, confirm it in `warp-internal` / `warp-server` or the live UI. ✅ `warp --auto-approve` after checking `TuiArgs` ❌ inventing `--fast-forward` from memory or an old PR description
- **Document durable behavior, not ephemeral chrome** — Prefer workflows, shortcuts, and outcomes that stay true when styling shifts. Drop glyph colors, pixel-level layout narration, and other pure presentation detail unless the reader must recognize them to succeed. ✅ "Press `Ctrl+C` once to stop the in-progress response." ❌ a full inventory of pending/running/failed glyph colors
- **State availability honestly** — If a capability is preview-only, platform-limited, interactive-only, or not yet in cloud agents, say so next to the claim. Never describe limited-preview behavior as generally available. ✅ "Linux post-processing adds smart cut; macOS applies a uniform speedup." ❌ listing smart cut as a property of every recording
- **Cover team-wide and admin effects** — For integrations and team features, state who can install, whether every teammate gets access immediately, and any per-user auth or admin steps on the external system. ✅ "A Jira admin must install the app; each teammate links their own account for run attribution." ❌ setup steps that only describe the installer's happy path
- **Section order follows reader chronology** — Prerequisites and requirements before setup, setup before usage, usage before advanced options. ✅ `## Prerequisites` → `## Set up the integration` → `## Start a run` ❌ setup steps before the reader knows what they need
- **Keep error messages out of the main flow** — Do not weave full error strings through conceptual or procedural sections. Put them in a dedicated `## Troubleshooting` section near the end, formatted symptom → cause → fix. ✅ one Troubleshooting section with the exact error as a bold lead-in ❌ repeating the same error callout after every step
- **Use callouts sparingly** — Prefer body prose. At most one or two callouts per page unless the content type template requires more, never two callouts back to back, and at most one per section. ✅ a single `:::note` for a non-obvious prerequisite ❌ a `:::note` / `:::tip` after every subsection
- **No AI-ism buzzwords or meta-openers** — Never open with "This page covers/explains/walks through..."; state the thing itself. Avoid marketing adjectives (seamless, powerful, robust, comprehensive), inflated verbs (leverage, streamline, empower, unlock), restated cause-and-effect ("This process ensures..."), and recap lines. See AGENTS.md → Voice & tone for the full lists. ✅ "Run agents directly in your GitHub Actions workflows using `oz-agent-action`." ❌ "This page covers how the integration works, how to set it up, and common automation patterns."
- **Cut length before shipping** — Brevity is a drafting rule, not only a review checklist item. After the first complete draft, run a deletion-only "Cut again" pass (AGENTS.md → Voice & tone → Cut again): remove framing lines, restated cause-and-effect, internal implementation detail the reader cannot act on, and boilerplate a parent page already owns. Prefer one concrete sentence over a paragraph that re-explains the same step. A page past ~1500 words usually still has padding — cut first; split only if the remaining content still does not fit. ✅ a setup section that states only the required clicks and links out for credential types ❌ a multi-paragraph walkthrough of harness internals on a how-to page
- **Document the user-visible model, not internal architecture** — Internal components (orchestrators, control planes, lifecycle state machines) get at most one sentence, and only when the reader can act on them. ✅ "Warp tracks every run. Check its status from the CLI, the API, or the dashboard." ❌ "The orchestration layer runs on Warp's servers (cloud control plane) and tracks lifecycle state (created → running → completed/failed)."
- **Descriptive link text, and no dead-end pages** — Never use "here", "this page", or a bare URL as link text. End every new page with `## Next steps` (quickstarts and tutorials) or `## Related pages` (every other type), containing at least one internal link whose anchor names the destination topic. Do not use "Further reading" or "See also". ✅ `Learn more about [Codebase Context](/code/codebase-context/)` ❌ `Click [here](/code/codebase-context/)` ❌ ending a new feature page with no cross-links
- **Disambiguate conditional and multi-clause wording** — If a sentence has two plausible readings (especially with "when", "if", "can", or stacked clauses), rewrite it so only one meaning remains. Prefer one idea per sentence. ✅ `Cloud handoff keeps your conversation's model only when that model is available in the cloud.` ❌ `Cloud handoff keeps your conversation's model when it can run in the cloud.` (keeps the model when it can? or only when cloud supports the model?)
- **Lead instructional sentences with the action or goal** — In steps, keyboard shortcuts, and "how to" sentences, put the action or goal first, then the control or condition. Readers should not need prior context to know what values or targets you mean. ✅ `To open the searchable environment and model selectors, press Ctrl+E.` ❌ `To change either value, press Ctrl+E.` (which values?)
- **Screenshots for hard-to-describe UI** — When a page documents a visual surface (statusline chips, tab bars, settings panes, multi-control layouts), include a screenshot after the prose that introduces that surface. Prefer prose for straightforward clicks, and prefer one well-placed figure over repeating the same surface. Always use descriptive alt text, never "screenshot". Do not invent or request screenshots of internal-only, flagged, or unfinished UI. ✅ a statusline screenshot after the paragraph that names the chips ❌ describing chip layout in a long paragraph with no image when humans keep asking "should we include a screenshot?"
- **`VideoEmbed` requires a specific `title`** — Every `<VideoEmbed>` must include a `title` prop that names the integration, workflow, feature, or task shown. ✅ `<VideoEmbed url="..." title="Warp Agent CLI conversation transcript walkthrough" />` ❌ `<VideoEmbed url="..." />` or a generic title like `"video"` / `"demo"`

### 7. Draft the doc
Create the documentation using the appropriate template from `.agents/templates/`. Follow the structure for the identified content type and all rules in `AGENTS.md`. Each template includes visible bracketed instructions explaining what to put in each section.

### 8. Run style lint
Run `python3 .agents/skills/style_lint/style_lint.py --changed` on the drafted file to catch formatting and terminology issues before presenting to the user.

If this skill is running as a cloud agent producing an agent-authored PR, capture a violation summary for the self-improvement loop **after the PR is created**:

1. Re-run with `--output /tmp/style_lint_out.json` to get machine-readable output.
2. Aggregate the `issues` array by `check` field to get violation counts per check name.
3. Include the following structured marker in your **text response** (write it as part of your agent message, not via a shell `echo` command). This ensures it appears as a `TextContentBlock` in the conversation, where `oz run get --conversation` can reliably retrieve it:
   ```
   [SIGNAL:style-lint] {"date":"YYYY-MM-DD","pr":"NNN","branch":"BRANCH_NAME","authored_by":"agent","skill_used":"SKILL_NAME","files_scanned":N,"violations":{"check_name":count}}
   ```

The `improve-drafting-skills` outer loop reads this signal from the conversation via `oz run get --conversation`, scanning assistant `TextContentBlock` messages for the marker. No git operations are required.

Skip steps 1–3 in local/interactive sessions.

### 9. Review against checklist
Before presenting the draft, verify against the quality checklist in `AGENTS.md`:
- [ ] The change passed `.agents/references/docs-worthiness-criteria.md`, and the verdict names a gate plus concrete evidence
- [ ] A content design plan exists with every field filled in, and the draft matches the content type it chose
- [ ] The outcome is the lightest correct one — an existing page was updated unless a new page is genuinely justified
- [ ] Frontmatter description is a standalone search summary (benefit + keywords; not "This page describes..." and not a restatement of the title)
- [ ] Content follows the structure for its content type
- [ ] Section order follows reader chronology (requirements → setup → usage → advanced → troubleshooting)
- [ ] Error messages and failure modes live in Troubleshooting, not woven through the main flow
- [ ] Callouts are sparse (usually 0–2 per page), never consecutive, and not used as a substitute for body prose
- [ ] Prose passes the tone rules: no marketing buzzwords, no meta-openers ("This page covers..."), no restated cause-and-effect or recap lines, and it reads naturally aloud (AGENTS.md → Voice & tone)
- [ ] Internal architecture (orchestrators, control planes, lifecycle states) appears only where the reader can act on it, and relocated detail landed on a maintainer-facing surface instead of being deleted
- [ ] A deletion-only second pass removed framing lines, self-commentary, rule justifications, and boilerplate a parent page already covers (AGENTS.md → Voice & tone → Cut again)
- [ ] Terminology matches the glossary (`.agents/references/terminology.md`)
- [ ] Headers use sentence case (with proper feature name capitalization)
- [ ] Headers name a specific topic (not bare Overview / More details / Other)
- [ ] Lists use `*` markers with bold term + hyphen + explanation format
- [ ] Cross-references are included, and the page ends with `## Next steps` (quickstart or tutorial) or `## Related pages` (every other type)
- [ ] Every bracketed template instruction has been deleted, including the `[BEFORE PUBLISHING: ...]` note
- [ ] The title is in frontmatter and there is no H1 in the body
- [ ] Link text names the destination topic (not "here" / "this page" / raw URLs)
- [ ] The first Settings path, CLI command, or URL on the page names the app or tool
- [ ] Non-clickable field labels use quotation marks; only interactive controls and chosen options are bold
- [ ] Instructions include expected outcomes
- [ ] Instructional sentences lead with the action or goal before the control, shortcut, or condition
- [ ] Conditional or multi-clause sentences have only one clear reading (no ambiguous "when/if/can" stacking)
- [ ] Procedures are scannable: dense sections are split into numbered steps, short bullets, or concise subsections
- [ ] UI surfaces and product terms use canonical names from `.agents/references/terminology.md`
- [ ] UI labels, CLI flags, permission defaults, and eligibility claims were verified against source or the live product — anything unverified is marked inline and reported per step 9.5
- [ ] The draft emphasizes durable behavior over ephemeral UI chrome (glyphs, pure styling, layout minutiae)
- [ ] Preview-only, platform-limited, or interactive-only capabilities are labeled as such
- [ ] Integrations and team features state admin requirements and who gets access after install
- [ ] Product names with a corresponding entry in `src/data/vars.ts` use the variable syntax (`{VARS.KEY}` in prose, `{{TOKEN}}` in frontmatter) — not hardcoded strings
- [ ] If AEO-driven, the draft follows the AEO brief, uses source vocabulary naturally, and avoids duplicative or junk-drawer coverage
- [ ] Images have descriptive alt text and are used only where the UI is hard to describe in prose
- [ ] Visual UI surfaces that are hard to reconstruct from prose include a screenshot (or an explicit note that no screenshot is available yet)
- [ ] Every `VideoEmbed` includes a specific `title` prop describing the workflow or feature shown

### 9.5. Report unverified claims

Inline `{/* VERIFY: ... */}` markers alone are skippable: a reviewer who skims the rendered page or the diff will miss them. Surface the full list where the human cannot miss it.

- **Agent-authored PRs** - Add an `## Unverified claims` section to the PR description. Include one bullet per claim with the claim itself, the file and section where it appears, and what would confirm it (for example, "check `TuiArgs` in `warp-internal`"). Include the section even when the list is empty, with the single line `None — all UI labels, flags, defaults, and eligibility claims were verified against source.` Never drop the section.
- **Local or interactive sessions** - List the same claims in your response to the user, before they review the draft.

A reviewer must be able to see every unconfirmed claim without opening the diff.

### 10. Update navigation and redirects
If this is a new page, remind the user to:
- Add it to the relevant section in `src/sidebar.ts`.

If this page replaces, renames, or moves an existing page, remind the user to add a redirect to the `redirects` array in `vercel.json` at the repo root:

```json
{
  "source": "/old/path",
  "destination": "/new/path/",
  "statusCode": 308
}
```

All redirects live in that one file, including redirects between top-level sections — there is no separate per-section redirect file and no UI for managing them. Include the trailing slash on `destination` to match the existing entries.

Always check the current list of redirects before adding a new one to avoid duplicates.

## Output

Present the drafted documentation as a complete markdown file that can be saved directly to the appropriate location in `docs/`.
