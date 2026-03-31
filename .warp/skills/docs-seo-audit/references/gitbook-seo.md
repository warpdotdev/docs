# How GitBook generates SEO title tags

GitBook constructs the HTML `<title>` tag as: `{Page Title} | {Space Title} | {Site Title}`

**The page title comes from the SUMMARY.md link text, not the H1 heading.** For example, `[Skills](capabilities/skills.md)` in SUMMARY.md produces `<title>Skills | Agents | Warp</title>`, regardless of what the H1 says in the markdown file.

This is not documented by GitBook. Their SEO docs only say "the HTML title is based on the page and space title" without specifying that "page title" means the SUMMARY.md link text.

Changing the SUMMARY.md link text also changes the sidebar label, breadcrumbs, and prev/next pagination. It does NOT change the URL (URLs are based on the file path).

Meta descriptions come from the `description` field in YAML frontmatter — this part is straightforward.
