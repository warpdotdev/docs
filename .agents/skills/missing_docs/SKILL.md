---
name: missing_docs
description: >-
  Find and fill documentation gaps in Warp's Astro Starlight docs by auditing coverage
  against code surfaces in warp-internal and warp-server, then drafting missing
  pages. Use when asked to find missing docs, audit documentation coverage,
  identify undocumented features, draft docs for new features, detect doc-impacting
  code changes since the last audit, or do a docs coverage check. Runs a Python
  audit script (coverage + snapshot-based change detection), then researches
  source code and writes first-pass doc pages. Can run audit-only, draft-only,
  drift-watch (recurring agent), or end-to-end.
---

# Missing Docs

Find documentation gaps, detect doc-impacting code changes, and draft missing pages.

## Requirements

The audit compares docs against code, so both source repos must be available:
- `warp-internal` and `warp-server`, auto-detected as siblings of the docs repo
  root (e.g. `/workspace/docs` next to `/workspace/warp-internal` and
  `/workspace/warp-server`), or passed explicitly via `--warp-internal PATH` /
  `--warp-server PATH`.

The script FAILS LOUD when a repo is missing OR when an extraction sanity guard
trips (a parser returning implausibly few surfaces means the source layout
changed and the parser needs fixing): it exits with code 2 and lists the skipped
audits in the report's `audits_skipped` field (`extraction:*` entries identify
broken parsers). Never treat an exit-2 run as a clean audit — fix the problem
and re-run. Exit 0 means all requested audits ran (findings may still exist).

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
- `--warp-internal PATH` / `--warp-server PATH` — explicit repo paths
- `--diff` — change detection against the committed snapshot (see Phase 2)
- `--update-snapshot` — regenerate `references/surface_snapshot.json` (full runs only)

The script resolves doc paths from the docs repo root and accepts `.md` and `.mdx`
interchangeably (and `README.md` ↔ `index.mdx`), so surface-map entries can use the
canonical filename even when the on-disk extension differs.

The script performs these coverage audits:
1. **Feature flag coverage** — classifies every `FeatureFlag` by rollout status using
   the cargo-feature→flag bridge in warp-internal `app/src/features.rs` plus
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
   hand-editing the YAML.
4. **Slash command coverage** — parses the static registry in warp-internal
   `app/src/search/slash_command_menu/static_commands/` and checks each `/command`
   is mentioned in docs.
5. **Settings coverage** — parses every `toml_path: "section.key"` setting
   registration in warp-internal (the same registry the JSON-schema generator uses)
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
   on the keyboard-shortcuts page that no longer exist anywhere in warp-internal.
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
- **CLI commands**: `mapped`, `doc_covered`, `finding`, `parent_flagged`
  (suppressed because the parent command is already flagged), or `hidden`.
- **API routes**: `mapped`, `spec_covered`, `docs_covered`, or `finding`.
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
possible: a feature flag that is deleted after stabilizing (per warp-internal's
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

After triaging and addressing diff findings, refresh the snapshot and commit it with
your PR so the next run diffs against the new baseline:

```bash
python3 .agents/skills/missing_docs/scripts/audit_docs.py --update-snapshot
```

### Phase 3: Draft

For each gap to address (prioritize high → medium → low):

1. Read `references/feature_surface_map.md` to determine the target doc section
2. Read `AGENTS.md` in the docs repo root for the complete style guide
3. Read 2-3 strong examples in the target section to match formatting patterns
4. Research the relevant source code:
   - **Feature gaps** → read the implementation in warp-internal `app/src/`, check UI code, settings, user-facing strings
   - **CLI gaps** → read command definition in `crates/warp_cli/src/`, extract flags, arguments, help text
   - **API gaps** → read handler in warp-server `router/handlers/public_api/`, route definition, request/response types; prefer fixing the OpenAPI spec via the `sync-openapi-spec` skill
   - **Slash command gaps** → read the registry entry and gating flags in `app/src/search/slash_command_menu/`
5. Draft the doc following style guide conventions:
   - YAML frontmatter with description
   - **All headings (H1–H4) must use sentence case** — capitalize only the first word and proper feature names (e.g., "Agent Mode", "Warp Drive"). ✅ `## How it works` ❌ `## How It Works`
   - Opening paragraph with user benefit
   - Key features, how it works, detailed sections, cross-references
   - Correct terminology (Agent, Agent Mode, Warp Drive, Oz, etc.)
   - Bold + dash format for list items: `* **Term** - Description`
6. Create the markdown file at the suggested path
7. Add new pages to the sidebar config in `astro.config.mjs`
8. **Update `references/feature_surface_map.md` in the same PR**: add a
   `Flag -> src/content/docs/...` mapping for every feature you documented (or add the
   flag to the ignore list with a comment if you confirmed it is internal-only). This
   step is NOT optional — unmapped features become repeat findings, and an unmaintained
   map is how gaps get lost.
9. Run `--update-snapshot` and commit the refreshed snapshot with the same PR.

### Drift-watch mode (recurring scheduled agent)

This is the end-to-end workflow for the scheduled cloud agent that keeps docs in sync
with the product. Each run:

1. **Audit**: run both modes and save reports. Pass explicit repo paths; verify
   exit code 0 — if the script exits 2, STOP and report the environment problem
   instead of concluding "no gaps":
   ```bash
   python3 .agents/skills/missing_docs/scripts/audit_docs.py \
     --warp-internal ../warp-internal --warp-server ../warp-server \
     --diff --output /tmp/docs_audit.json
   ```
2. **Triage**: work through `surface_changes` and `changelog_review` first (what
   changed since last run), then standing coverage findings (high → medium → low)
   across all categories: features, CLI, API, slash commands, settings, stale doc
   references, unlisted pages, map hygiene, staleness. For each item decide:
   draft/update a doc page, update the OpenAPI spec via `sync-openapi-spec`, add a
   surface-map entry (documented elsewhere), or add an ignore/`internal`/allowlist
   entry with a comment (internal-only or intentionally unlisted).
3. **Draft**: follow Phase 3 for every item that needs docs.
4. **Update references**: apply surface-map edits, then regenerate the snapshot:
   ```bash
   python3 .agents/skills/missing_docs/scripts/audit_docs.py --update-snapshot
   ```
5. **Validate**: `npm run build` if doc pages changed; re-run the audit and confirm
   the addressed findings are gone.
6. **Open a PR** with the doc pages + map + snapshot changes together, using the
   `create_pr` skill. Summarize remaining (deferred) findings in the PR body so
   nothing is silently dropped.

Recommended scheduled-agent prompt (copy when setting up the agent):

> Run the missing_docs skill in drift-watch mode. Use the audit script with explicit
> --warp-internal and --warp-server paths and --diff. If the script exits non-zero with
> skipped audits, report the environment problem and stop. Otherwise triage all
> surface_changes and changelog_review findings plus high/medium coverage findings:
> draft or update doc pages, update the surface map (mapping or ignore entry with a
> comment) for every triaged flag, and use the sync-openapi-spec skill for API spec
> gaps. Regenerate the surface snapshot with --update-snapshot. Open a single PR with
> the doc pages, feature_surface_map.md, and surface_snapshot.json changes, and list
> any findings you deferred in the PR body.

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

## References

- `references/feature_surface_map.md` — curated mapping of flags/commands/routes/slash
  commands/settings to doc pages, ignore list for internal flags, allowlist for
  intentionally unlisted pages, and the `internal` sentinel for surfaces that
  intentionally have no public docs. Update it with every docs PR that ships a
  feature.
- `references/surface_snapshot.json` — generated snapshot of all code surfaces used by
  `--diff`. Regenerate with `--update-snapshot`; never hand-edit.
- `references/stale_terms.md` — renamed/removed-feature terms to flag during staleness
  audits. Pure terminology/style policing belongs to the `style_lint` skill.
- `AGENTS.md` (docs repo root) — full documentation style guide
