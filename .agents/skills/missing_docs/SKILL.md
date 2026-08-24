---
name: missing_docs
description: >-
  Find documentation gaps in Warp's Astro Starlight docs by auditing coverage against
  code surfaces in the public warp client repo and warp-server and against the weekly
  release changelog, decide which gaps actually warrant docs, then draft only those.
  Use when asked to find missing docs, audit documentation coverage, identify
  undocumented features, draft docs for new features, detect doc-impacting code changes
  since the last audit, or do a docs coverage check. Runs a Python audit script
  (coverage + snapshot-based change detection), gates every candidate against the
  documentation-worthiness criteria, then researches source code and writes first-pass
  doc pages for the ones that pass. Can run audit-only, draft-only, drift-watch
  (release-triggered recurring agent), or end-to-end.
---

# Missing Docs

Find documentation gaps, detect doc-impacting code changes, and draft missing pages.

## Requirements

The audit compares docs against code, so both source repos must be available:
- the public warp client repo ([warpdotdev/warp](https://github.com/warpdotdev/warp))
  and `warp-server`, auto-detected as siblings of the docs repo root (e.g.
  `/workspace/docs` next to `/workspace/warp` and `/workspace/warp-server`; a
  sibling named `warp-internal` is accepted as a fallback), or passed explicitly
  via `--warp PATH` / `--warp-server PATH` (`--warp-internal` is a deprecated alias).

The script FAILS LOUD when a repo is missing OR when an extraction sanity guard
trips (a parser returning implausibly few surfaces means the source layout
changed and the parser needs fixing): it exits with code 2 and lists the skipped
audits in the report's `audits_skipped` field (`extraction:*` entries identify
broken parsers). Never treat an exit-2 run as a clean audit — fix the problem
and re-run. Exit 0 means all requested audits ran (findings may still exist).

## Public vs. private surfaces (what you may document)

Only document surfaces that are **publicly released**. This is the most important guardrail in this skill: do not reveal private or unreleased surfaces in public docs. Two independent gates, both required:

1. **Source / exposure.** The OSS warp client repo ([warpdotdev/warp](https://github.com/warpdotdev/warp); locally `warp`, or the `warp-internal` fallback) is public — its feature flags, CLI commands, settings, and slash commands are documentable. **`warp-server` is a private repo** and is not public until released; its source and most of its surfaces must NOT be documented. The one exception is the public **Oz Agent API**, whose released surface is exactly the set of endpoints already present in the OpenAPI spec (`developers/agent-api-openapi.yaml`).
2. **Rollout status.** Even for public-repo surfaces, only document **GA** features. Never document dogfood, preview, or research-preview surfaces (for example, Agent Memory is research preview, so its `oz memory*` CLI and `/memory_stores` API must not be documented yet).

Rules of thumb:
- A `warp-server` API endpoint that is **not already in the OpenAPI spec** is treated as not-yet-public: do NOT hand-write docs for it. Either confirm it has been publicly released and let the `sync-openapi-spec` skill bring it into the spec, or map it `-> internal` / defer it. When unsure, defer — never expose an unreleased endpoint or feature in public docs.
- A CLI command or API route gated by a **non-GA feature flag** should be mapped `-> gated:<Flag>` (for example, `gated:AIMemories`) rather than `-> internal`: the audit auto-defers it while the flag is non-GA and auto-surfaces it for docs once the flag goes GA. (Feature flags and settings already auto-defer by rollout status; `gated:` extends that to CLI/API.)
- The audit still *detects* these as gaps (useful signal), but detection is not permission to document. Every resolution must respect this boundary.

This section is the source of truth for **Gate 0** in
`.agents/references/docs-worthiness-criteria.md`. Passing Gate 0 only establishes that a
surface *may* be documented — it does not establish that it *should* be. Work through the
remaining gates before treating any finding as actionable.

## Workflows

### Phase 1: Audit (coverage)

Run the audit script to identify gaps:

```bash
python3 .agents/skills/missing_docs/scripts/audit_docs.py
```

Options:
- `--category features|cli|api|slash|settings|structure|staleness|map` — run a single audit category
- `--severity high|medium|low` — filter by minimum severity
- `--weak-coverage` — also flag GA features whose mapped doc exists but doesn't mention feature keywords (low-severity, noisy)
- `--output report.json` — save JSON report to file
- `--warp PATH` / `--warp-server PATH` — explicit repo paths (`--warp-internal` is a deprecated alias)
- `--diff` — change detection against the committed snapshot (see Phase 2)
- `--update-snapshot` — regenerate `references/surface_snapshot.json` (full runs only)

The script resolves doc paths from the docs repo root and accepts `.md` and `.mdx`
interchangeably (and `README.md` ↔ `index.mdx`), so surface-map entries can use the
canonical filename even when the on-disk extension differs.

The script performs these coverage audits:
1. **Feature flag coverage** — classifies every `FeatureFlag` by rollout status using
   the cargo-feature→flag bridge in the warp client repo's `app/src/features.rs` plus
   `RELEASE_FLAGS`/`PREVIEW_FLAGS`/`DOGFOOD_FLAGS` in `crates/warp_features/src/lib.rs`.
   GA flags must be mapped in the surface map or covered in docs; Preview flags produce
   low-severity "docs needed soon" findings; dogfood/other flags are tracked by the
   snapshot only.
2. **CLI command coverage** — parses the full `oz` command tree from
   `crates/warp_cli/src/` (recursive subcommands like `oz run message send`, skipping
   `hide = true`) and checks the CLI reference docs. Per-module `--long` flags are
   additionally tracked in the snapshot for change detection.
3. **API endpoint coverage** — extracts public routes from warp-server
   `router/handlers/public_api/*.go` (nested gin groups resolved, caller-passed group
   prefixes matched positionally) and checks them against
   `developers/agent-api-openapi.yaml` (param-name-insensitive: `{runId}` matches
   `{run_id}`) and the API reference docs. For spec drift, run the docs
   `sync-openapi-spec` skill (or warp-server's `update-open-api-spec`) instead of
   hand-editing the YAML. **warp-server is private** (see Public vs. private
   surfaces): a flagged endpoint is documentable only once it is part of the
   released public Oz Agent API. Never hand-draft API docs or reveal an unreleased
   endpoint — resolve released endpoints via `sync-openapi-spec`, and `-> internal`/
   defer the rest.
4. **Slash command coverage** — parses the static registry in the warp client repo's
   `app/src/search/slash_command_menu/static_commands/` and checks each `/command`
   is mentioned in docs.
5. **Settings coverage** — parses every `toml_path: "section.key"` setting
   registration in the warp client repo (the same registry the JSON-schema generator uses)
   and checks the all-settings reference page documents it. Private and
   dogfood/other-flagged settings are exempt; object-typed settings documented as
   their own `[section]` count as covered.
6. **Docs staleness** — flags renamed/removed-feature terminology in prose (code
   spans stripped; historical changelog pages excluded). Broader terminology and
   style enforcement is owned by the `style_lint` skill — delegate pure wording
   issues there.
7. **Stale doc references** — reverse checks: settings keys documented in
   all-settings.mdx that no longer exist in code (catches renames like
   `agents.oz.*` → `agents.warp_agent.*`), and keybinding actions (`scope:action`)
   on the keyboard-shortcuts page that no longer exist anywhere in the warp client repo.
8. **Docs structure** — pages on disk that are missing from `src/sidebar.ts`
   (built but unreachable through navigation). Intentionally unlisted pages go in
   the surface map's "Unlisted docs pages" section.
9. **Surface map hygiene** — flags map entries whose flag/command/route/setting no
   longer exists in code, and mapped doc targets that no longer exist. Verify the
   doc page is still accurate, then prune or update the entry.

Snapshot-only surfaces (no standing coverage audit, but added/removed/changed items
are reported by `--diff`): Oz web app routes (`AgentsApp.tsx`), server-side agent
tools (multi_agent tool registries), bundled + channel-gated skills
(`resources/bundled/skills`, `resources/channel-gated-skills`), and per-module CLI
flags.

Present the report to the user, grouped by category and sorted by severity.

Adjacent checks owned by other skills (do not duplicate them here):
- UI menu paths and Command Palette names → `validate_ui_refs`
- Platform error-code pages → `sync-error-docs`
- Broken links and 404s/redirects → `check_for_broken_links` / `weekly-404-monitor`
- Terminology/style sweeps → `style_lint`

### Completeness accounting (the no-slip guarantee)

Every full run computes a completeness accounting and embeds it in the report
(`summary.accounting` in JSON, a `COMPLETENESS ACCOUNTING` block in the printed
output). It partitions every extracted surface item into exactly one
accountability bucket and proves totality:
- **Feature flags**: every GA/Preview flag is `mapped` (surface map verified),
  `ignored` (curated internal list), or a visible `finding`; every dogfood/other
  flag is `tracked_non_ga` (snapshot diff fires on promotion or removal).
- **CLI commands**: `mapped`, `doc_covered`, `gated_non_ga` (deferred via
  `gated:<Flag>` while its gating flag is non-GA), `finding`, `parent_flagged`
  (suppressed because the parent command is already flagged), or `hidden`.
- **API routes**: `mapped`, `spec_covered`, `docs_covered`, `gated_non_ga`
  (deferred via `gated:<Flag>` while its gating flag is non-GA), or `finding`.
- **Slash commands**: `mapped`, `doc_covered`, or `finding`.
- **Settings**: `private`, `tracked_non_ga`, `mapped`, `doc_covered`, or `finding`.

If any item escapes every bucket, the run reports `integrity:accounting` in
`audits_skipped` and exits 2 — an unaccounted item means the audit logic itself
regressed, never that the item is fine. Map hygiene additionally rejects
integrity bugs in the surface map: entries that are both mapped and ignored
(the ignore silently wins) and duplicate keys within a section.

How every change path is caught, end to end:
1. **New surface item appears** (flag, command, route, slash, setting, web
   route, tool, bundled skill) → the snapshot `--diff` reports it AND, once
   GA/user-facing, the coverage audit produces a standing finding until it is
   documented + mapped or ignored with a comment.
2. **Item is promoted** (dogfood→preview→ga, setting status change, skill
   channel change) → `--diff` status-change finding + coverage finding appears.
3. **Item is removed/renamed** → `--diff` removal finding + map hygiene flags
   the dead map entry + stale-doc-reference checks flag docs still naming it.
4. **Launch with no client-code change** (server-side experiment flips to 100%,
   Oz web app backend feature) → the changelog cross-check is the net: every
   "New features"/"Improvements"/"Oz updates" bullet newer than the snapshot
   becomes a verification finding.
5. **The audit itself rots** (source layout moves, parser breaks) → extraction
   sanity guards trip, dependent audits skip, exit 2.
6. **The map rots** (dead entries, conflicts, duplicates, missing doc targets,
   unmapped-but-mentioned features) → map hygiene + fallback-transparency
   findings keep pressure until fixed.

The mapping is updated through three enforced paths: Phase 3 step 8 makes the
map+snapshot update a mandatory part of drafting; the drift-watch triage step
requires a mapping/ignore/allowlist decision for every finding; and map hygiene
findings force pruning when code moves underneath the map.

### Phase 2: Change detection (diff mode)

The snapshot at `references/surface_snapshot.json` records all extracted surfaces
(flags + rollout status, CLI commands and per-module flags, API routes, slash
commands, settings + status, Oz web app routes, server-side agent tools, bundled
skills) plus the last-seen docs-changelog version. It makes change detection
possible: a feature flag that is deleted after stabilizing (per the warp repo's
remove-feature-flag policy) would otherwise vanish from the audit's universe
silently. When a new surface type is introduced, diffing against an older snapshot
emits a one-time "surface type newly tracked" note instead of false positives.

```bash
python3 .agents/skills/missing_docs/scripts/audit_docs.py --diff
```

Diff mode reports, since the snapshot was last updated:
- **Added / removed / promoted surfaces** — e.g. a new GA flag (high), a flag promoted
  dogfood→ga (high), a removed flag ("feature stabilized or killed — verify docs and
  map entry"), new/removed CLI commands and `--flags`, API routes, slash commands,
  settings (with status promotions), Oz web app routes, server-side agent tools, and
  bundled skills.
- **Changelog items to verify** — "New features", "Improvements", and "Oz updates"
  bullets from `src/content/docs/changelog/<year>.mdx` entries newer than the
  snapshot's last-seen version. This is the best signal for launches no static code
  parse can see (server-side features, Oz web app, experiment rollouts). A changelog
  mention is NOT documentation — verify each item has real doc coverage. ("Bug fixes"
  bullets are deliberately untracked to keep weekly triage volume manageable.)

  **A changelog item is a candidate, not a work item.** Detection is not permission to
  document. Every item must pass `.agents/references/docs-worthiness-criteria.md` before
  it becomes actionable — most will not. Read
  `references/changelog_decisions.md` first and skip any PR number already decided.

#### Sources beyond the client changelog

The client changelog only covers `warpdotdev/warp`. Server and platform features ship
continuously and never appear in it, which is how they used to reach docs through the
retired spec-scan path — and why that path produced most of the unvetted drafts. Cover
them through these three layers instead, in order of preference:

1. **`oz_updates`** — the separate array in the same `client_version` payload the release
   gate already fetches. Release-gated, low-noise, and currently the most direct signal
   for platform-side changes. Triage these bullets exactly like changelog bullets: same
   gates, same ledger, same evidence requirement.

   `check_new_release.py` prints them; the audit never sees them, because it is offline
   by design and they are not part of the markdown changelog it parses. Read them from
   the gate's output, or `--json` for the full array. `oz_updates` is the API's field
   name and stays as-is regardless of product naming.
2. **The public Agent API surface** — already covered by audit category 3 and
   `sync-openapi-spec`. No new machinery; just confirm the release run actually triages
   these findings rather than deferring them by habit. A released endpoint reaches docs
   through the spec, never through hand-drafting.
3. **`warp-server` product specs** — the last resort, and the most conservative layer.
   Apply a hard rollout check *before* the worthiness gates: only consider a spec whose
   feature is verifiably enabled for users. A merged spec is not a shipped feature. If
   you cannot confirm the rollout from code or the changelog, defer it and record the
   blocking condition — do not draft against the spec text.

Layer 3 is where the old pipeline went wrong: it treated spec merge as the trigger, so it
drafted for features that had not shipped and sometimes never would. Reach for it only
when layers 1 and 2 cannot see a user-visible change you have independent evidence has
shipped.

After triaging and addressing diff findings, refresh the snapshot and commit it with
your PR so the next run diffs against the new baseline:

```bash
python3 .agents/skills/missing_docs/scripts/audit_docs.py --update-snapshot
```

### Phase 3: Draft

**Preconditions — do not draft without both:**

1. **A recorded pass verdict.** The finding must have passed
   `.agents/references/docs-worthiness-criteria.md`, with the gate and its concrete
   evidence written down. No recorded verdict means no drafting. For changelog-derived
   findings the verdict also belongs in `references/changelog_decisions.md`.
2. **A content design plan.** Route it with the rule in
   `.agents/references/content-design-plan.md`: a new page gets the full form in
   `.agents/templates/content-design-plan.md`, an update that adds a concept gets the
   three-line short form, and a correction gets no plan. Write it before opening a page
   template — the plan decides the content type; the template does not. Carry it into the PR
   body verbatim: a scheduled run has no one to present it to, so the PR body is the only
   place a human will see the reasoning.

A finding that passes the gate with the **update an existing page** outcome is still a
drafting task — it just edits a page instead of creating one. Prefer it; new pages need
to be justified against the existing information architecture, not just against the
change.

For each gap to address (prioritize high → medium → low):

1. Read `references/feature_surface_map.md` to determine the target doc section
2. Read `AGENTS.md` in the docs repo root for the complete style guide
3. Read 2-3 strong examples in the target section to match formatting patterns
4. Research the relevant source code:
   - **Feature gaps** → read the implementation in the warp client repo's `app/src/`, check UI code, settings, user-facing strings
   - **CLI gaps** → read command definition in `crates/warp_cli/src/`, extract flags, arguments, help text
   - **API gaps** → read handler in warp-server `router/handlers/public_api/`, route definition, request/response types; prefer fixing the OpenAPI spec via the `sync-openapi-spec` skill. Only act on endpoints already publicly released (see Public vs. private surfaces); never draft docs for unreleased warp-server endpoints.
   - **Slash command gaps** → read the registry entry and gating flags in `app/src/search/slash_command_menu/`

   **Then look for a product spec.** Code tells you what a surface does; it never tells you who
   it is for or what problem it solves — and those are the content design plan's first three
   fields. Check warp-server for `specs/<id>/PRODUCT.md`. Only some specs have one, and
   `TECH.md` is the implementation plan, not a substitute. Where it exists, its `Problem`,
   `Goals`, `Non-goals`, and `User experience` sections map onto the plan's Problem, Goals,
   Excludes, and high-impact scenarios almost directly.

   Three limits, all load-bearing:
   - **Framing only, never behavior.** Labels, flags, and defaults drift between spec and ship,
     so every concrete claim is still verified against code. A spec is context, not a source of
     truth.
   - **Never evidence that something shipped.** A merged spec is not a release. Gate 0 is
     settled before this step, and a spec cannot reopen it.
   - **Never quoted into a public page.** warp-server is private and specs routinely describe
     unshipped plans. Use one to understand the reader, then write the page from scratch.

   If no spec exists, proceed without one and record that in the content design plan. An
   acknowledged gap is reviewable; an invented audience is not.
5. Draft the doc following style guide conventions:
   - YAML frontmatter with description
   - **All headings (H1–H4) must use sentence case** — capitalize only the first word and proper feature names (e.g., "Agent Mode", "Warp Drive"). ✅ `## How it works` ❌ `## How It Works`
   - Opening paragraph with user benefit
   - Key features, how it works, detailed sections, cross-references
   - Correct terminology (Agent, Agent Mode, Warp Drive, Oz, etc.)
   - Bold + dash format for list items: `* **Term** - Description`
6. Create the markdown file at the suggested path
7. Add new pages to the sidebar in `src/sidebar.ts` (only a brand-new top-level topic also needs an `astro.config.mjs` change)
8. **Update `references/feature_surface_map.md`** for every feature you document: add a
   `Flag -> src/content/docs/...` mapping (or an ignore-list entry with a comment if you
   confirmed it is internal-only). This step is NOT optional — unmapped features become
   repeat findings, and an unmaintained map is how gaps get lost. Per the PR strategy
   below, collect all map edits into the single companion audit-bookkeeping PR (only fold
   them into a feature PR when the run documents exactly one feature).
9. Run `--update-snapshot` and commit the refreshed `surface_snapshot.json` in that same
   bookkeeping PR. Never split the snapshot across multiple PRs.

### Resolution patterns

Not every finding needs a new doc page — pick the lightest correct fix and verify it against source before applying:

- **No docs needed** — the finding failed every worthiness gate, or a disqualifier applied.
  This is a first-class resolution, not a silent skip: record the verdict, the
  disqualifier or failed gates, and a one-line reason. Changelog items go in
  `references/changelog_decisions.md`; code surfaces go in the surface map as an ignore
  entry with a comment. An unrecorded rejection is re-proposed next run and has to be
  rejected again by the same reviewer.
- **Deferred (Gate 0)** — real user-facing surface, but not yet GA or not yet public.
  Record it with the blocking condition so it re-surfaces when the flag goes GA or the
  endpoint reaches the released OpenAPI spec. Never draft ahead of the release; a page
  written for an unshipped feature is stale before it merges.
- **User-facing setting** — document it in `terminal/settings/all-settings.mdx` under its TOML section (type/default/options come from the `toml_path` registration).
- **Internal or state-only setting** (one-time banners, migration flags, telemetry-modeled state) — map `section.key -> internal` in the surface map instead of documenting it.
- **Feature flag with a dedicated doc page** — map the flag to that page.
- **Feature flag whose only user-facing surface is an already-documented setting** — map the flag to that setting's doc page rather than writing a new page (for example, a tab-bar visibility flag maps to the all-settings reference).
- **Preview or pre-launch feature with no docs yet** — add it to the surface-map ignore list with a comment; the snapshot diff re-flags it when it promotes to GA.
- **Stale map entry or doc reference** (map hygiene) — confirm the surface is gone from code, then prune the dead entry.
- **warp-server API endpoint not in the released OpenAPI spec** — do not hand-document it (warp-server is private). If it is part of the released public Oz Agent API, hand it to the `sync-openapi-spec` skill; if it is unreleased or internal, map it `-> internal` with a comment. Never expose an unreleased endpoint or feature in public docs.
- **CLI command or API route gated by a non-GA feature flag** — map it `-> gated:<Flag>` so it auto-defers while the flag is non-GA and auto-surfaces for docs when it GAs (e.g. Agent Memory's `oz memory*` and `/memory_stores/*` use `gated:AIMemories`). Prefer this over `-> internal`, which never re-surfaces.

### Reviewer routing

Assign the engineer who owns the *code* behind each change, so a human with real context reviews the PR. Every finding traces to a source surface; map that surface's defining file to its owner using the ownership files that already live in the code repos (CODEOWNERS format, last-match-wins):
- warp client repo: `.github/STAKEHOLDERS`
- warp-server: `.github/STAKEHOLDERS` (advisory) + `.github/CODEOWNERS` (enforced)

These are the source of truth (warp-server keeps STAKEHOLDERS fresh via the `sync-stakeholders` skill), so never hardcode owner lists here.

For each addressed finding, note the defining source file you already consulted in Phase 3 step 4:
- **Setting** → the file holding its `toml_path` registration (usually under `app/src/settings/`).
- **Slash command** → `app/src/search/slash_command_menu/static_commands/`.
- **Feature flag** → the flag's primary usage site in `app/src/` (grep the flag name); fall back to `crates/warp_features/src/lib.rs`.
- **CLI command** → `crates/warp_cli/src/`.
- **API route** → warp-server `router/handlers/public_api/` (API gaps usually go to `sync-openapi-spec`).

Resolve owners and get a ready-to-run assignment command:

```bash
python3 .agents/skills/missing_docs/scripts/suggest_reviewers.py \
  --warp ../warp --warp-server ../warp-server \
  warp:app/src/settings/ssh.rs \
  warp:app/src/search/slash_command_menu/static_commands/commands.rs
```

Then assign the resolved reviewers on the PR with `gh pr edit <PR> --add-reviewer <logins/teams>`. Unresolved paths are non-fatal — leave them for manual assignment rather than blocking the run.

### PR strategy: one PR per feature

Ship each documented feature as its own focused PR so the owning engineer reviews only
their area. Do NOT bundle unrelated features into a single mega PR.

- **One feature → one PR.** Each documented feature (or standalone correction, e.g. a
  duplicate-heading fix) gets its own branch and PR, titled and scoped to that item, with
  the owning reviewer assigned. This is the default; the rules below are the only
  exceptions.
- **Group only when features share a doc file or owner.** Two features that edit the same
  page (e.g. tab groups and drag-a-tab-to-another-window, both in
  `terminal/windows/tabs.mdx`) go in one PR — separate PRs touching the same file would
  conflict, and they usually share an owner anyway. Prefer grouping by owning engineer
  when the same file is involved.
- **Collect all surface-map + snapshot edits into a single companion "audit bookkeeping"
  PR.** `references/feature_surface_map.md` and `references/surface_snapshot.json` are
  shared files; editing them across many feature PRs causes merge conflicts, and the
  snapshot is a wholesale regen. Put every `Flag -> page` mapping, ignore/`internal`/
  `gated:` entry, and the `--update-snapshot` regen into one bookkeeping PR. Its mappings
  may point at pages that land in the sibling feature PRs — map hygiene only requires the
  target page to exist on the base branch, so the bookkeeping PR is independently
  mergeable in any order. If a run documents exactly one feature, fold its map + snapshot
  changes into that single PR and skip the companion.
- **API spec gaps stay separate** — released endpoints go through the `sync-openapi-spec`
  skill as their own change, never bundled into a feature PR.
- **Validate once, then split.** Run `npm run build` on the combined working tree (all
  features together) to confirm everything compiles, then peel each feature onto its own
  branch off `main` (e.g. `git checkout <base> -b <branch>` then
  `git checkout <combined-ref> -- <files>`). Each feature branch is then a strict subset
  of the already-validated tree.
- List any deferred findings in the most relevant PR body (or the bookkeeping PR) so
  nothing is silently dropped.

### Drift-watch mode (recurring scheduled agent)

This is the end-to-end workflow for the scheduled cloud agent that keeps docs in sync
with the product. Each run:

1. **Release gate**: check whether a new stable release has shipped since the last
   processed run. The schedule runs daily so it can catch a release whenever it lands,
   but the work only happens once per release:
   ```bash
   python3 .agents/skills/missing_docs/scripts/check_new_release.py
   ```
   Exit `0` means a new stable release is available — continue. Exit `10` means no new
   release; record the no-op outcome in run output and **stop**. Exit `1` is a fetch or
   parse failure; report it and stop rather than proceeding as if nothing shipped.

   The gate also prints any `oz_updates` bullets for the release. Keep them — they are
   platform-side changes the audit cannot see, and this is the only place they surface.

   Do not update the state file yet. It is written in step 5, after triage, so a run that
   crashes mid-triage retries the same release instead of skipping it.
2. **Audit**: run both modes and save reports. Pass explicit repo paths; verify
   exit code 0 — if the script exits 2, STOP and report the environment problem
   instead of concluding "no gaps":
   ```bash
   python3 .agents/skills/missing_docs/scripts/audit_docs.py \
     --warp ../warp --warp-server ../warp-server \
     --diff --output /tmp/docs_audit.json
   ```
3. **Triage**: read `references/changelog_decisions.md` first and drop any changelog item
   already decided. Then work through `surface_changes` and `changelog_review` (what
   changed since last run), then standing coverage findings (high → medium → low)
   across all categories: features, CLI, API, slash commands, settings, stale doc
   references, unlisted pages, map hygiene, staleness.

   **Apply `.agents/references/docs-worthiness-criteria.md` to every remaining item
   before deciding anything else.** The default is no docs; the burden is on the change
   to earn a page. Record a verdict for each item with the gate it passed (or the
   disqualifier that stopped it) and the concrete evidence — a setting key, CLI flag,
   quoted error string, changed default, or API field. Restating the changelog entry is
   not evidence. Expect most items to resolve to "no docs needed"; a run that passes
   everything it looked at has not applied the gate.

   For each item that passes, decide: update an existing page (preferred), draft a new
   page, or update the OpenAPI spec via `sync-openapi-spec`. For each item that does not,
   decide: no docs needed, deferred with a blocking condition, a surface-map entry
   (documented elsewhere), or an ignore/`internal`/allowlist entry with a comment.
4. **Draft**: follow Phase 3 for every item that needs docs. Every drafted page or
   substantive page update needs a content design plan first, carried into its PR body.
5. **Update references**: append every verdict from step 3 to
   `references/changelog_decisions.md` (rejections included), record the processed
   release with `check_new_release.py --commit`, apply surface-map edits, then regenerate
   the snapshot:
   ```bash
   python3 .agents/skills/missing_docs/scripts/check_new_release.py --commit
   python3 .agents/skills/missing_docs/scripts/audit_docs.py --update-snapshot
   ```
6. **Validate**: `npm run build` if doc pages changed; re-run the audit and confirm
   the addressed findings are gone.
7. **Route reviewers**: run `scripts/suggest_reviewers.py` (see Reviewer routing)
   with the source files behind the addressed findings to resolve the owning
   engineers for the PR.
8. **Open one PR per feature** following the PR strategy above (not a single mega PR):
   one focused PR per documented feature (grouping only features that share a doc file or
   owner), each carrying its content design plan as a section in the PR body, plus a
   single companion audit-bookkeeping PR for all `feature_surface_map.md`,
   `changelog_decisions.md`, `last_release_processed.json`, and `surface_snapshot.json`
   changes. Use the `create_pr` skill, assign each PR's owning reviewer from step 7
   (`gh pr edit <PR> --add-reviewer ...`), and summarize remaining (deferred) findings in
   the relevant PR body so nothing is silently dropped.

A run that gates out every candidate is a successful run. It opens no feature PRs and
only the bookkeeping PR recording the verdicts. Do not manufacture work to justify the
run.

Recommended scheduled-agent prompt (copy when setting up the agent):

> Run the missing_docs skill in drift-watch mode. First run
> .agents/skills/missing_docs/scripts/check_new_release.py; if it reports no new stable
> release, record the no-op outcome and stop. Otherwise use the audit script with
> explicit --warp (public warpdotdev/warp checkout) and --warp-server paths and --diff.
> If the script exits non-zero with skipped audits, report the environment problem and
> stop. Otherwise read references/changelog_decisions.md and drop already-decided items,
> then triage the remaining surface_changes and changelog_review findings plus
> high/medium coverage findings against .agents/references/docs-worthiness-criteria.md.
> The default is no docs: record a verdict and concrete evidence for every item, and
> expect most to fail. For items that pass, write a content design plan per
> .agents/references/content-design-plan.md before drafting, prefer updating an existing
> page over creating a new one, and use the sync-openapi-spec skill for API spec gaps.
> Update the surface map for every triaged flag, append every verdict to
> changelog_decisions.md, and regenerate the surface snapshot with --update-snapshot.
> Resolve reviewers by running .agents/skills/missing_docs/scripts/suggest_reviewers.py
> against the source files behind each addressed finding. Open one focused PR per
> documented feature (grouping only features that share a doc file or owner), each with
> the content design plan as a section in its body, plus a single companion bookkeeping
> PR for the feature_surface_map.md, changelog_decisions.md, last_release_processed.json,
> and surface_snapshot.json changes; assign each PR's resolved owner as reviewer, and
> list any findings you deferred in the relevant PR body.

### Invocation modes

The user can trigger any subset:
- **"Run a docs audit"** or **"Check docs coverage"** → Phase 1 only
- **"What changed since the last audit?"** → Phase 1 + 2 (`--diff`)
- **"Draft docs for [specific gap]"** → Phase 3 only (skip audit)
- **"Find and fix missing docs"** → Phases 1–3 end-to-end
- **Scheduled/recurring run** → Drift-watch mode

### Drafting standards

- Produce complete, ready-to-commit markdown — not outlines or stubs
- For CLI docs: include command syntax, all flags with descriptions, practical examples
- For feature docs: lead with user benefit, include how-to, cross-reference related features
- For API docs: include request/response schemas, auth requirements, curl examples
- Use `codebase_semantic_search` and `grep` on source repos for technical accuracy

## Tests

The skill's scripts have a stdlib-only test suite (no third-party dependencies):

```bash
python3 .agents/skills/missing_docs/scripts/test_suggest_reviewers.py
python3 .agents/skills/missing_docs/scripts/test_audit_docs.py
python3 .agents/skills/missing_docs/scripts/test_check_new_release.py
```

- `test_check_new_release.py` unit-tests the release gate with the network stubbed: exit-code
  contract (0 new / 10 no-op / 1 fetch failure), that a fetch failure is never reported as
  "no new release", that a plain check never writes state, and the full
  check → commit → no-op → next-release cycle.
- `test_suggest_reviewers.py` unit-tests reviewer resolution (CODEOWNERS matching, last-match-wins, user/team split, dedup, unresolved paths).
- `test_audit_docs.py` runs behavioral checks against the sibling code repos — clean exit, completeness accounting (`unaccounted` empty), category/severity scoping, fail-loud (exit 2) on a missing repo, snapshot round-trip, and research-preview deferral (the public/private boundary) — and skips gracefully when those repos aren't checked out.

## References

- `references/feature_surface_map.md` — curated mapping of flags/commands/routes/slash
  commands/settings to doc pages, ignore list for internal flags, allowlist for
  intentionally unlisted pages, the `internal` sentinel for surfaces that
  intentionally have no public docs, and the `gated:<Flag>` sentinel for CLI/API
  surfaces deferred until their gating flag goes GA. Update it with every docs PR
  that ships a feature.
- `references/surface_snapshot.json` — generated snapshot of all code surfaces used by
  `--diff`. Regenerate with `--update-snapshot`; never hand-edit.
- `references/last_release_processed.json` — the release gate's state: which stable
  version was last triaged. Written by `check_new_release.py --commit`, never by hand.
  Deliberately separate from `surface_snapshot.json`, which is regenerated wholesale and
  would lose the marker. Delete it to force a re-run of the current release.
- `references/changelog_decisions.md` — append-only ledger of docs-worthiness verdicts on
  changelog items. Read before triage to skip already-decided items; append a row for
  every item evaluated, rejections included. Commit it in the companion bookkeeping PR.
- `references/stale_terms.md` — renamed/removed-feature terms to flag during staleness
  audits. Pure terminology/style policing belongs to the `style_lint` skill.
- `.agents/references/docs-worthiness-criteria.md` — the gate that decides whether a
  finding should produce docs at all. Applied during triage, before any drafting.
- `.agents/references/content-design-plan.md` — the audience, problem, goals, and content
  type decisions required before drafting a page that passed the gate.
- `scripts/check_new_release.py` — the release gate. Compares the current stable version
  from `app.warp.dev/client_version` against `last_release_processed.json` so a daily
  schedule does per-release work. Run it first in drift-watch mode; run it again with
  `--commit` only after triage succeeds.
- `scripts/suggest_reviewers.py` — resolves PR reviewers from the warp and warp-server
  `.github/STAKEHOLDERS` and `CODEOWNERS` files (CODEOWNERS-format, last-match-wins),
  given the source files behind each finding. Used by the drift-watch reviewer-routing step.
- `AGENTS.md` (docs repo root) — full documentation style guide
