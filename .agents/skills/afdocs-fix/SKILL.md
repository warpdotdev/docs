---
name: afdocs-fix
description: >-
  Fix agent-friendly documentation issues found by the afdocs-audit skill.
  Reads the AFDocs audit report and applies automated fixes for failing checks.
  Use after running the afdocs-audit skill, or when asked to fix AFDocs issues,
  improve the agent-ready score, or remediate llms.txt / markdown availability
  problems.
---

# AFDocs Fix

Apply automated fixes for issues found by the `afdocs-audit` skill. This skill reads an AFDocs audit report and remediates fixable issues.

## Prerequisites

1. Run the audit skill first to produce a report:
   ```bash
   node .agents/skills/afdocs-audit/scripts/afdocs_audit.mjs --output /tmp/afdocs-report.json
   ```
2. Read the report and cross-reference against `afdocs-audit/references/known-exceptions.md` to identify which issues are genuine (vs. allowlisted).

## Fix procedures by check

For each failing or warning check, follow the procedure below. Skip checks listed in `known-exceptions.md`.

### llms-txt-directive-html (Content Discoverability)

**What's wrong**: No agent-facing directive pointing to llms.txt in the HTML pages.

**Fix**: Add a visually-hidden element in `src/components/CustomHeader.astro` before the `.header` div:

```html
<div class="llms-directive sr-only" aria-hidden="true">
	For the complete documentation in markdown, see <a href="/llms.txt">llms.txt</a>.
	Markdown versions of each page are available by appending .md to any URL.
</div>
```

The `.sr-only` class is Starlight's built-in screen-reader-only utility. The `sanitizeRoot` function in `docs-markdown-integration.js` strips `.sr-only` elements during HTML → markdown conversion, so this directive will appear only in the HTML version (the markdown version gets its own directive — see below).

**Files**: `src/components/CustomHeader.astro`

### llms-txt-directive-md (Content Discoverability)

**What's wrong**: No llms.txt directive in the generated markdown pages.

**Fix**: In `src/integrations/docs-markdown-integration.js`, in the `convertHtmlToMarkdown` function, prepend a blockquote before the title:

```javascript
const llmsDirective =
    '> For the complete documentation index, see [llms.txt](/llms.txt).\n' +
    '> Markdown versions of each page are available by appending .md to any URL.';
const sections = [llmsDirective, `# ${normalizeWhitespace(title)}`];
```

**Files**: `src/integrations/docs-markdown-integration.js`

### content-negotiation (Markdown Availability)

**What's wrong**: Server ignores `Accept: text/markdown` header and returns HTML.

**Fix**: Create Astro middleware at `src/middleware.ts` that uses the existing `shouldServeMarkdown()` helper from `src/lib/docs-markdown.js`:

```typescript
import { defineMiddleware } from 'astro:middleware';
import {
    shouldServeMarkdown,
    isEligibleDocHtmlPath,
    getMarkdownPathFromHtmlPath,
} from './lib/docs-markdown.js';

export const onRequest = defineMiddleware(async (context, next) => {
    const { request, url } = context;
    if (!isEligibleDocHtmlPath(url.pathname)) return next();
    if (!shouldServeMarkdown(request)) return next();
    const mdPath = getMarkdownPathFromHtmlPath(url.pathname);
    return context.rewrite(mdPath);
});
```

The `shouldServeMarkdown` helper checks both the `Accept` header (for `text/markdown` and `text/plain`) and user-agent tokens (ChatGPT, Claude, Cursor, etc.).

**Files**: `src/middleware.ts` (new file)

### llms-txt-coverage (Observability)

**What's wrong**: llms.txt covers less than 95% of sitemap pages.

**Fix**: Update the `customSets` paths in `astro.config.mjs` under `starlightLlmsTxt()`:

1. Check that every content directory under `src/content/docs/` has a matching customSet entry.
2. Common mismatches:
   - Directory was renamed but customSet path wasn't updated (e.g., `university/**` → `guides/**`)
   - New content directories added without a corresponding customSet
   - Sub-paths excluded too aggressively (e.g., `support-and-community/community/` pages)
3. For large pages that cause `hast-util-to-text` stack overflows: the `exclude` option only applies to `llms-small.txt`, NOT `llms-full.txt`. Do not add pages to `exclude` expecting them to be skipped in `llms-full.txt`.

**Diagnostic steps**:
```bash
# List content directories
ls src/content/docs/

# Compare against customSets in astro.config.mjs
grep -A1 "label:" astro.config.mjs | grep "paths:"
```

**Files**: `astro.config.mjs`

### markdown-url-support (Markdown Availability)

**What's wrong**: Some pages don't return markdown when `.md` is appended to the URL.

**Fix**: Check that `src/integrations/docs-markdown-integration.js` and `src/pages/[...slug].md.ts` are both present and correctly configured. The integration generates static `.md` files at build time; the page route serves them in dev mode.

**Files**: `src/integrations/docs-markdown-integration.js`, `src/pages/[...slug].md.ts`

### http-status-codes (URL Stability)

**What's wrong**: The site returns 200 for non-existent pages (soft 404).

**Fix**: Ensure `public/404.html` or an Astro 404 page exists and returns a proper 404 status code. In Vercel, configure `cleanUrls` and ensure the adapter handles 404 responses correctly.

**Files**: `vercel.json`, `src/pages/404.astro` (if it exists)

### MCP Server Discoverable

**What's wrong**: No MCP server discovery endpoint found.

**Fix**: Add a static discovery file at `public/.well-known/mcp.json`:

```json
{
  "name": "Warp Documentation",
  "description": "Search and retrieve Warp documentation.",
  "url": "https://warp.mcp.kapa.ai"
}
```

This points to the existing Kapa-hosted MCP server (OAuth-protected). No custom implementation needed.

**Files**: `public/.well-known/mcp.json` (new file)

## Checks with no automated fix

These checks require infrastructure or design changes that can't be automated:

- **content-start-position** — Inherent to Starlight's layout. Mitigated by content negotiation and llms.txt directives. See `known-exceptions.md`.
- **page-size-markdown / page-size-html** — Requires editorial decision to split long pages. Flag in the report but do not auto-fix.
- **section-header-quality** — Content-level change requiring human judgment.

## Applying fixes

1. Create a branch: `git checkout -b afdocs-fixes origin/main`
2. Apply the fixes for each failing check (skip allowlisted checks).
3. Validate: `npm run build` (the build must succeed).
4. Commit with the prefix: `AFDocs fixes: <summary of what was fixed>`
5. Open a PR: `gh pr create`

## PR conventions

- Title must be prefixed with `AFDocs fixes:` (e.g., `AFDocs fixes: add llms.txt directive and content negotiation middleware`)
- Include the audit score (before/after if known) in the PR description
- Include the co-author line: `Co-Authored-By: Oz <oz-agent@warp.dev>`
