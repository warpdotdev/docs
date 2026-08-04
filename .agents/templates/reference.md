---
description: >-
  [1-2 sentences: what is documented and how to use this reference.
  Standalone search summary: name the surface and the job-to-be-done.
  Example: "Use the {{WARP_AGENT_CLI}} to run, configure, and manage agents from the terminal."
  Do NOT write "This page describes..." or only restate the title.
  Use {{TOKEN}} syntax for any product names in src/data/vars.ts.]
---
[VARS: Add this line immediately after the closing --- above if this page references any product names from src/data/vars.ts. Then use {VARS.KEY} for those names in the prose below.
`import { VARS } from '@data/vars';`
See AGENTS.md → Content variables for the full variable list and usage rules.]

# [Title — sentence case. Title convention: noun describing contents, e.g., "CLI commands", "Keyboard shortcuts". Not bare "Overview" or "Reference".]

[Brief intro: what this reference covers and how to use it.
1-2 sentences. This is for lookup, not learning.]

## [Section name — sentence case and specific. e.g., "Installing the CLI", "Authentication". Not "More details".]

[Introductory sentence or conceptual context for this section.]

## [Command/endpoint/option group — sentence case. e.g., "Running agents"]

[Use a strict repeating pattern for each entry. Every entry must
follow the same structure. Consistency is more important than style.

For commands/endpoints: name → syntax → description → flags/params → example
For settings/options: name → type → default → description

Use H2 for major sections, H3 for individual entries.
Use tables for multiple parameters, lists for single elements.
For unordered bullets, use `*` markers (not `-`) and keep flag lists parallel.]

### `command-name`

[Brief description of what this command does.]

```sh
command-name [options] <required-arg>
```

**Key flags:**

* `--flag-name` (`-f`) — Description of what this flag does.
* `--another-flag` — Description.

**Example:**

```sh
command-name --flag-name value
```

### `another-command`

[Repeat the same structure for every entry.
Alphabetize entries where ordering doesn't matter.]

## Related pages

[Include on new reference pages when a conceptual or procedural companion exists.
Use descriptive link text that names the destination topic.]

* [Conceptual overview](path/to/conceptual.md)
* [Setup guide](path/to/procedural.md)
