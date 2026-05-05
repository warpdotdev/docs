---
name: missing_docs
description: >-
  Find and fill documentation gaps in Warp's Astro Starlight docs by auditing coverage
  against code surfaces in warp-internal and warp-server, then drafting missing
  pages. Use when asked to find missing docs, audit documentation coverage,
  identify undocumented features, draft docs for new features, or do a docs
  coverage check. Runs a Python audit script to identify gaps, then researches
  source code and writes first-pass doc pages. Can run audit-only, draft-only,
  or end-to-end.
---

# Missing Docs

Find documentation gaps and draft missing pages in one workflow.

## Two-phase workflow

### Phase 1: Audit

Run the audit script to identify gaps:

```bash
python3 .warp/skills/missing_docs/scripts/audit_docs.py
```

Options:
- `--category features|cli|api|staleness` — run a single audit category
- `--severity high|medium|low` — filter by minimum severity
- `--output report.json` — save JSON report to file
- `--warp-internal PATH` — explicit path to warp-internal (auto-detected from sibling dirs)
- `--warp-server PATH` — explicit path to warp-server (auto-detected from sibling dirs)

The script performs 4 audits:
1. **Feature flag coverage** — compares GA flags in `warp_core/src/features.rs` + `app/Cargo.toml` against doc mentions
2. **CLI command coverage** — compares `warp_cli/src/lib.rs` subcommands against `src/content/docs/reference/cli/`
3. **API endpoint coverage** — compares `router/router.go` routes against `src/content/docs/reference/api-and-sdk/` and the OpenAPI spec
4. **Docs staleness** — checks for outdated terminology in existing docs

Present the report to the user, grouped by category and sorted by severity.

### Phase 2: Draft

For each gap the user wants to address (prioritize high → medium → low):

1. Read `references/feature_surface_map.md` to determine the target doc section
2. Read `AGENTS.md` in the docs repo root for the complete style guide
3. Read 2-3 strong examples in the target section to match formatting patterns
4. Research the relevant source code:
   - **Feature gaps** → read the implementation in warp-internal `app/src/`, check UI code, settings, user-facing strings
   - **CLI gaps** → read command definition in `warp_cli/src/`, extract flags, arguments, help text
   - **API gaps** → read handler in warp-server `router/handlers/`, route definition, request/response types
5. Draft the doc following style guide conventions:
   - YAML frontmatter with description
   - **All headings (H1–H4) must use sentence case** — capitalize only the first word and proper feature names (e.g., "Agent Mode", "Warp Drive"). ✅ `## How it works` ❌ `## How It Works`
   - Opening paragraph with user benefit
   - Key features, how it works, detailed sections, cross-references
   - Correct terminology (Agent, Agent Mode, Warp Drive, Oz, etc.)
   - Bold + dash format for list items: `* **Term** - Description`
6. Create the markdown file at the suggested path
7. Remind user to add new pages to the relevant `astro.config.mjs (sidebar config)`

To find warp-internal and warp-server, search for sibling directories of the docs repo. If not found, ask the user.

### Invocation modes

The user can trigger either phase or both:
- **"Run a docs audit"** or **"Check docs coverage"** → Phase 1 only
- **"Draft docs for [specific gap]"** → Phase 2 only (skip audit)
- **"Find and fix missing docs"** → Both phases end-to-end

### Drafting standards

- Produce complete, ready-to-commit markdown — not outlines or stubs
- For CLI docs: include command syntax, all flags with descriptions, practical examples
- For feature docs: lead with user benefit, include how-to, cross-reference related features
- For API docs: include request/response schemas, auth requirements, curl examples
- Use `codebase_semantic_search` and `grep` on source repos for technical accuracy

## References

- `references/feature_surface_map.md` — curated mapping of flags/commands to doc pages, also lists internal-only flags to ignore
- `references/stale_terms.md` — deprecated/outdated terms to flag during staleness audits, sourced from AGENTS.md terminology standards
- `AGENTS.md` (docs repo root) — full documentation style guide
