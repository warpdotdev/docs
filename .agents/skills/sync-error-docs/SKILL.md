---
name: sync-error-docs
description: >-
  Detect new platform error codes in warp-server that are missing documentation
  pages in the docs repo. Creates doc pages, astro.config.mjs (sidebar config) entries, and
  redirects for any gaps. Use on a weekly schedule or when error codes change.
---

# Sync Error Docs

Ensure every `ErrorCode` in `platformerrors.go` has a corresponding documentation page, astro.config.mjs (sidebar config) entry, and redirects.

## Repos

This skill requires two repos in the agent's environment:

- `warpdotdev/warp-server` — source of truth for error codes
- `warpdotdev/docs` — documentation pages

## Workflow

### Step 1: Extract error codes from warp-server

Grep the `ErrorCode` constants from `platformerrors.go`:

```bash
grep 'ErrorCode = "' warp-server/logic/ai/ambient_agents/platformerrors/platformerrors.go
```

Each match yields a line like `InsufficientCredits ErrorCode = "insufficient_credits"`. Extract the quoted string — that is the canonical error code (underscore format).

### Step 2: List existing doc pages

List the markdown files in the errors directory:

```bash
ls docs/src/content/docs/reference/api-and-sdk/troubleshooting/errors/*.mdx
```

Each file is named `{hyphen-code}.mdx` (e.g., `insufficient-credits.mdx`). Ignore `index.mdx`.

### Step 3: Compare and find missing pages

For each error code from Step 1, convert underscores to hyphens (e.g., `insufficient_credits` → `insufficient-credits`) and check whether a corresponding `.mdx` file exists.

### Step 4: Create missing doc pages

For each missing code, read `references/error-page-template.md` in this skill directory for the template.

**Heading case:** All headings (H1–H4) must use sentence case — capitalize only the first word and proper feature names. ✅ `## When does this occur?` ❌ `## When Does This Occur?`

To fill in the template accurately:
1. Read the error code's doc comment and `FromError()` case in `platformerrors.go` to determine:
   - HTTP status code
   - Whether it's retryable
   - Whether it's a user error (FAILED) or platform error (ERROR)
   - The user-facing message
2. If the code has a dedicated constructor (e.g., `NewExternalAuthRequired`), read it for additional context

Place the new file at:
```
docs/src/content/docs/reference/api-and-sdk/troubleshooting/errors/{hyphen-code}.mdx
```

### Step 5: Add to astro.config.mjs (sidebar config)

Add the new page to `docs/src/content/docs/reference/astro.config.mjs (sidebar config)` under the Errors section.

- User errors: insert before `authentication_required` (which begins the platform errors group)
- Platform errors: append after `internal_error` (currently the last entry in the list)
- Note: the list has no explicit section labels. The platform errors group starts at `authentication_required` and currently contains `authentication_required`, `resource_unavailable`, and `internal_error`.
- Use the format: `    * [{underscore\_code}](api-and-sdk/troubleshooting/errors/{hyphen-code}.md)`
- Note: underscores in the display name must be escaped as `\_` for Astro Starlight

### Step 6: Add vercel.json (redirects) redirect

Add a redirect entry in `docs/src/content/docs/reference/vercel.json (redirects)` that maps the underscore path to the hyphen path. This handles visitors who type the underscore form directly:

```yaml
api-and-sdk/troubleshooting/errors/{underscore_code}: api-and-sdk/troubleshooting/errors/{hyphen-code}.md
```

Before adding, check if the entry already exists to avoid duplicates on re-runs:

```bash
grep 'api-and-sdk/troubleshooting/errors/{underscore_code}:' docs/src/content/docs/reference/vercel.json (redirects)
```

If it returns a match, skip this step. Otherwise, add the entry under the existing `redirects:` block.

### Step 7: Create site-level redirect

The API's `type` URI uses the format `https://docs.warp.dev/errors/{underscore_code}`. This needs a site-level redirect to reach the actual doc page.

<!-- TODO: Post-migration, update this step to use vercel.json redirects instead of the GitBook API. -->
Use the existing `docs_redirects.py` script (requires `GITBOOK_TOKEN` env var and `requests` Python package).

First, check if the redirect already exists to avoid duplicates on re-runs:

```bash
python3 docs/scripts/docs_redirects.py get-by-source \
  --source "/errors/{underscore_code}"
```

If a redirect is returned, skip the `create` step. Otherwise, create it:

```bash
python3 docs/scripts/docs_redirects.py create \
  --source "/errors/{underscore_code}" \
  --destination-json '{"kind": "url", "url": "https://docs.warp.dev/reference/api-and-sdk/troubleshooting/errors/{hyphen-code}"}'
```

Read `references/redirect-patterns.md` in this skill directory for more details on the redirect setup.

If `GITBOOK_TOKEN` is not set, skip this step and note it in the report.

### Step 8: Commit and open PR

If any pages were created:

1. Create a branch in the docs repo (e.g., `sync-error-docs/{date}`)
2. Commit all changes with a descriptive message
3. Push and open a PR targeting `main`
4. Use `report_pr` to surface the PR link

### Step 9: Report

Summarize what was found:
- Total error codes in `platformerrors.go`
- Number of existing doc pages
- New codes that were missing pages (list them)
- Pages created, astro.config.mjs (sidebar config) entries added, redirects configured
- Or confirm everything is already in sync

## References

- `references/error-page-template.md` — template for new error doc pages
- `references/redirect-patterns.md` — detailed redirect setup instructions
