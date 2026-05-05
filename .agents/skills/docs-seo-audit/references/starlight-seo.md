# How Astro Starlight generates SEO title tags

Astro Starlight constructs the HTML `<title>` tag as: `{Page Title} | {Site Title}` (e.g., `Skills | Warp`).

**The page title is resolved in this order of precedence:**
1. The `title` field in the page's YAML frontmatter (if present)
2. The `label` property in the sidebar config (`src/sidebar.ts`)
3. The slug-derived title (auto-generated from the file name)

The H1 heading does **not** affect the `<title>` tag.

For example, if `src/sidebar.ts` has `{ slug: 'agent-platform/capabilities', label: 'Overview' }` and the page has no frontmatter `title`, the rendered title is `<title>Overview | Warp</title>`. But if the page has `title: Capabilities overview` in frontmatter, that takes precedence and produces `<title>Capabilities overview | Warp</title>`.

## Decoupling sidebar label from page title

To give a page a unique SEO title while keeping a short sidebar label, use both `title` and `sidebar.label` in frontmatter:

```yaml
---
title: Capabilities overview
sidebar:
  label: "Overview"
---
```

This produces `<title>Capabilities overview | Warp</title>` while displaying "Overview" in the sidebar.

## Side effects of changing sidebar config labels

Changing the `label` in `src/sidebar.ts` also changes the sidebar label, breadcrumbs, and prev/next pagination. It does NOT change the URL (URLs are based on the file path/slug).

## Meta descriptions

Meta descriptions come from the `description` field in YAML frontmatter — this part is straightforward.
