---
title: [Sentence case. A noun phrase naming what can be looked up. Break up stacked nouns with prepositions: "Keyboard shortcuts for the code editor", not "Code editor keyboard shortcut reference". Never a bare "Overview" or "Reference". This renders as the page H1 — do not add an H1 in the body.]
description: >-
  [One sentence, 50-160 characters: what the reader can look up here. Name the artifacts —
  flags, endpoints, shortcuts — not the genre. Example: "Look up {{WARP_AGENT_CLI}} flags,
  environment variables, slash commands, and keyboard shortcuts."
  Use {{TOKEN}} syntax for product names in src/data/vars.ts.]
---
[BEFORE PUBLISHING: Delete every bracketed instruction in this file, including this one. They are guidance for the author, not page content.]
[VARS: If this page names a product from src/data/vars.ts, add `import { VARS } from '@data/vars';` on the line directly below the frontmatter, then use {VARS.KEY} in prose. See AGENTS.md → Content variables.]

[Opening: what this reference covers and how to use it. 1-2 sentences. The reader already knows what they want — this is for lookup, not learning.]

[BREVITY: Delete any section below you don't need — a short page is a finished page. See AGENTS.md → Voice & tone → Cut again.]

## [Entry group — sentence case and specific, e.g. "Running agents"]

[One sentence introducing the group.]

[REPEATING PATTERN: pick one structure per page and apply it to every entry without exception. Consistency matters more here than in any other content type, because readers scan rather than read.

For commands and endpoints: name → syntax → description → flags → example.
For settings and options: name → type → default → description.

Use H2 for groups, H3 for individual entries. Tables for multiple parameters, lists for single elements. Alphabetize where order does not carry meaning.]

### `command-name`

[What this command does, in one or two sentences.]

```sh
command-name [options] <required-arg>
```

**Flags:**

* `--flag-name` (`-f`) — What it does.
* `--another-flag` — What it does.

**Example:**

```sh
command-name --flag-name value
```

### `another-command`

[Same structure, every time. Be exhaustive: document every option, flag, and value. A reference with gaps sends the reader to the source.]

## Related pages

[Cross-links. Use descriptive link text that names the destination.]

* [Conceptual page for this feature](path/to/page.md)
* [How to use it](path/to/procedural-page.md)
