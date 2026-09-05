---
name: sync-error-docs
description: >-
  Detect new platform error codes in warp-server that are missing documentation
  pages in the docs repo. Creates doc pages, sidebar entries, and redirects for
  any gaps. Use on a weekly schedule or when error codes change.
---

# Sync Error Docs

Ensure every `ErrorCode` in `platformerrors.go` has a corresponding documentation page, sidebar entry, and redirect.

## Agent-doc quality contract

The PR this skill opens or updates follows the shared v1 agent-doc quality
contract in `.agents/references/doc-quality-policy.md`: apply the
`warpy-factory` label and add the `## Documentation risk` block
(`.agents/skills/doc_quality_policy/finalize_pr_contract.py build`). New error
pages are `engineering-review-required` (new page, technical claims) unless
generated verbatim from `platformerrors.go` with no invented prose.

## Repos

This skill requires two repos in the agent's environment:

- `warpdotdev/warp-server` — source of truth for error codes
- `warpdotdev/docs` — documentation pages

All paths below are relative to the **docs repo root**, with `warp-server` checked out as a sibling directory (`../warp-server`), matching the convention used by `sync-openapi-spec`.

## Workflow

### Step 1: Extract error codes from warp-server

Grep the `ErrorCode` constants from `platformerrors.go`:

```bash
grep 'ErrorCode = "' ../warp-server/logic/ai/ambient_agents/platformerrors/platformerrors.go
```

Each match yields a line like `InsufficientCredits ErrorCode = "insufficient_credits"`. Extract the quoted string — that is the canonical error code (underscore format).

### Step 2: List existing doc pages

List the markdown files in the errors directory:

```bash
ls src/content/docs/reference/api-and-sdk/troubleshooting/errors/*.mdx
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
src/content/docs/reference/api-and-sdk/troubleshooting/errors/{hyphen-code}.mdx
```

### Step 5: Add to the sidebar

The sidebar lives in `src/sidebar.ts`. (`astro.config.mjs` only imports it via `starlightSidebarTopics(sidebarTopics)` — do not edit the sidebar there.)

Find the `Errors` group inside the `API Troubleshooting` group, under the `Reference` topic. Its `items` array begins with the index entry:

```ts
{ slug: 'reference/api-and-sdk/troubleshooting/errors', label: 'Errors' },
'reference/api-and-sdk/troubleshooting/errors/insufficient-credits',
'reference/api-and-sdk/troubleshooting/errors/feature-not-available',
```

Add the new page as a bare slug string using the **hyphenated** code:

```ts
'reference/api-and-sdk/troubleshooting/errors/{hyphen-code}',
```

Rules:
- Use a plain slug string. Do not use Markdown link syntax — `* [name](path.md)` is GitBook-era format and will not build.
- No `.md`/`.mdx` extension and no leading slash.
- Only add an explicit `{ slug, label }` object if the auto-derived title is wrong; the existing error entries all rely on the derived title.
- Append after the last existing error entry unless a grouping order is obvious from the surrounding entries. The list is not alphabetized and has no section labels.

### Step 6: Add the underscore-to-hyphen redirects (only when the forms differ)

Error codes are underscored (`insufficient_credits`) but page slugs are hyphenated (`insufficient-credits`). Add redirects to `vercel.json` (at the repo root) so the underscore form resolves.

**Skip this step entirely for a code that contains no underscore.** Its hyphenated slug is the same string as the code, so there is nothing to redirect: the no-slash entry would be a redundant trailing-slash normalization, and the trailing-slash entry would have `source` equal to `destination` — a self-redirect, which is an infinite loop. `conflict` is the current example. It has no redirect entries in `vercel.json`, and that is correct, not a gap. Only add redirects when `{underscore_code}` and `{hyphen-code}` actually differ.

**Otherwise add two entries, not one.** Every multi-word error code currently in `vercel.json` has both a no-trailing-slash and a trailing-slash source (34 entries covering 17 codes, with no code having only one form). Adding a single variant leaves the new code with half the coverage of every existing one, and the `/errors/:code/` catch-all forwards a trailing slash through, so the slashed underscore path would not resolve.

Check for existing entries first, to stay idempotent across re-runs:

```bash
grep -F '"/reference/api-and-sdk/troubleshooting/errors/{underscore_code}"' vercel.json
grep -F '"/reference/api-and-sdk/troubleshooting/errors/{underscore_code}/"' vercel.json
```

Add whichever variant is missing to the `redirects` array, alongside the other error-code redirects:

```json
{
  "source": "/reference/api-and-sdk/troubleshooting/errors/{underscore_code}",
  "destination": "/reference/api-and-sdk/troubleshooting/errors/{hyphen-code}/",
  "statusCode": 308
},
{
  "source": "/reference/api-and-sdk/troubleshooting/errors/{underscore_code}/",
  "destination": "/reference/api-and-sdk/troubleshooting/errors/{hyphen-code}/",
  "statusCode": 308
}
```

Both `destination` values carry a trailing slash — every existing error redirect does, regardless of its source form.

### Step 7: Confirm the site-level `/errors/` route (usually no action)

The API's `type` URI uses `https://docs.warp.dev/errors/{underscore_code}`. **Catch-all redirects already cover every code**, in both slash forms, so no per-code work is normally needed:

```json
{
  "source": "/errors/:code",
  "destination": "/reference/api-and-sdk/troubleshooting/errors/:code/",
  "statusCode": 308
},
{
  "source": "/errors/:code/",
  "destination": "/reference/api-and-sdk/troubleshooting/errors/:code/",
  "statusCode": 308
}
```

These forward `:code` unchanged, so `/errors/insufficient_credits` lands on the underscored path and is then picked up by the step 6 redirects. Completing step 6 is therefore sufficient — which is why step 6 must add both slash variants.

Verify both catch-alls are still present:

```bash
grep -F '"/errors/:code"' vercel.json
grep -F '"/errors/:code/"' vercel.json
```

If either is missing, restore it rather than adding per-code entries. Read `references/redirect-patterns.md` for background.

This step no longer uses the GitBook API. The former `docs_redirects.py` / `GITBOOK_TOKEN` flow was left over from the GitBook era and does not apply to the Astro Starlight site.

### Step 8: Commit and open PR

If any pages were created, follow the "One standing PR per automation" contract in `.agents/references/skill-authoring-guidelines.md` — new error codes trickle in over time and each dated PR would edit the same `src/sidebar.ts` and `vercel.json`, so they would conflict.

1. Look for an existing open PR, then check out the stable branch:
   ```bash
   gh pr list --repo warpdotdev/docs --state open \
     --search 'add error code pages for new platform errors in:title' \
     --json number,headRefName

   git fetch origin
   git checkout sync-error-docs 2>/dev/null || git checkout -b sync-error-docs origin/main
   git rebase origin/main
   ```
2. Commit all changes with a descriptive message.
3. Push. If a PR already exists the push updates it — append the new codes under the existing `## New error code pages` heading rather than adding a duplicate heading, which `check_pr_body.py` rejects. If none exists, open one. Write the body to a file:
   ```bash
   cat > /tmp/sync-error-docs-pr-body.md << 'EOF'
   ## New error code pages
   [list each new error code and the doc page created]

   Co-Authored-By: Oz <oz-agent@warp.dev>
   EOF

   python3 .agents/skills/create_pr/check_pr_body.py /tmp/sync-error-docs-pr-body.md
   gh pr create \
     --title "docs: add error code pages for new platform errors" \
     --body-file /tmp/sync-error-docs-pr-body.md
   ```
4. Use `report_pr` to surface the PR link

### Step 9: Report

Summarize what was found:
- Total error codes in `platformerrors.go`
- Number of existing doc pages
- New codes that were missing pages (list them)
- Pages created, `src/sidebar.ts` entries added, redirects configured
- Any codes skipped for redirects because they contain no underscore
- Or confirm everything is already in sync

Follow the actionable-only Slack rule in `.agents/references/skill-authoring-guidelines.md`: a run that finds everything already in sync writes this report to the run output and posts nothing.

## References

- `references/error-page-template.md` — template for new error doc pages
- `references/redirect-patterns.md` — detailed redirect setup instructions
