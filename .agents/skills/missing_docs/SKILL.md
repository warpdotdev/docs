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

The script FAILS LOUD when a repo is missing: it exits with code 2 and lists the
skipped audits in the report's `audits_skipped` field. Never treat an exit-2 run
as a clean audit — fix the repo paths and re-run. Exit 0 means all requested
audits ran (findings may still exist).

## Workflows

### Phase 1: Audit (coverage)

Run the audit script to identify gaps:

```bash
python3 .agents/skills/missing_docs/scripts/audit_docs.py
```

Options:
- `--category features|cli|api|slash|staleness|map` — run a single audit category
- `--severity high|medium|low` — filter by minimum severity
- `--weak-coverage` — also flag GA features whose mapped doc exists but doesn't mention feature keywords (low-severity, noisy)
- `--output report.json` — save JSON report to file
- `--warp-internal PATH` / `--warp-server PATH` — explicit repo paths
- `--diff` — change detection against the committed snapshot (see Phase 2)
- `--update-snapshot` — regenerate `references/surface_snapshot.json` (full runs only)

The script resolves doc paths from the docs repo root and accepts `.md` and `.mdx`
interchangeably (and `README.md` ↔ `index.mdx`), so surface-map entries can use the
canonical filename even when the on-disk extension differs.

The script performs 6 coverage audits:
1. **Feature flag coverage** — classifies every `FeatureFlag` by rollout status using
   the cargo-feature→flag bridge in warp-internal `app/src/features.rs` plus
   `RELEASE_FLAGS`/`PREVIEW_FLAGS`/`DOGFOOD_FLAGS` in `crates/warp_features/src/lib.rs`.
   GA flags must be mapped in the surface map or covered in docs; Preview flags produce
   low-severity "docs needed soon" findings; dogfood/other flags are tracked by the
   snapshot only.
2. **CLI command coverage** — parses the full `oz` command tree (top-level commands and
   subcommands, skipping `hide = true`) from `crates/warp_cli/src/` and checks the CLI
   reference docs.
3. **API endpoint coverage** — extracts public routes from warp-server
   `router/handlers/public_api/*.go` (nested gin groups resolved) and checks them
   against `developers/agent-api-openapi.yaml` and the API reference docs. For spec
   drift, run the docs `sync-openapi-spec` skill (or warp-server's
   `update-open-api-spec`) instead of hand-editing the YAML.
4. **Slash command coverage** — parses the static registry in warp-internal
   `app/src/search/slash_command_menu/static_commands/` and checks each `/command`
   is mentioned in docs.
5. **Docs staleness** — flags renamed/removed-feature terminology in prose (code
   spans stripped; historical changelog pages excluded). Broader terminology and
   style enforcement is owned by the `style_lint` skill — delegate pure wording
   issues there.
6. **Surface map hygiene** — flags map entries whose flag/command no longer exists in
   code, and mapped doc targets that no longer exist. Verify the doc page is still
   accurate, then prune or update the entry.

Present the report to the user, grouped by category and sorted by severity.

### Phase 2: Change detection (diff mode)

The snapshot at `references/surface_snapshot.json` records all extracted surfaces
(flags + rollout status, CLI commands, API routes, slash commands) plus the last-seen
docs-changelog version. It makes change detection possible: a feature flag that is
deleted after stabilizing (per warp-internal's remove-feature-flag policy) would
otherwise vanish from the audit's universe silently.

```bash
python3 .agents/skills/missing_docs/scripts/audit_docs.py --diff
```

Diff mode reports, since the snapshot was last updated:
- **Added / removed / promoted surfaces** — e.g. a new GA flag (high), a flag promoted
  dogfood→ga (high), a removed flag ("feature stabilized or killed — verify docs and
  map entry"), new CLI/API/slash surfaces.
- **Changelog items to verify** — "New features" and "Improvements" bullets from
  `src/content/docs/changelog/<year>.mdx` entries newer than the snapshot's last-seen
  version. This is the best signal for launches no static code parse can see
  (server-side features, Oz web app, experiment rollouts). A changelog mention is NOT
  documentation — verify each item has real doc coverage.

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
   changed since last run), then standing coverage findings (high → medium → low).
   For each item decide: draft/update a doc page, update the OpenAPI spec via
   `sync-openapi-spec`, add a surface-map entry (documented elsewhere), or add an
   ignore/`internal` entry with a comment (internal-only).
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
  commands to doc pages, ignore list for internal flags, and the `internal` sentinel
  for surfaces that intentionally have no public docs. Update it with every docs PR
  that ships a feature.
- `references/surface_snapshot.json` — generated snapshot of all code surfaces used by
  `--diff`. Regenerate with `--update-snapshot`; never hand-edit.
- `references/stale_terms.md` — renamed/removed-feature terms to flag during staleness
  audits. Pure terminology/style policing belongs to the `style_lint` skill.
- `AGENTS.md` (docs repo root) — full documentation style guide
