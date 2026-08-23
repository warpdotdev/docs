---
description: >-
  [One sentence, 50-160 characters: what the reader can look up here.
  Name the artifacts (flags, endpoints, shortcuts), not the genre.
  Example: "Look up {{WARP_AGENT_CLI}} flags, environment variables, slash commands, and keyboard shortcuts."
  See AGENTS.md > Frontmatter > Descriptions by content type for the full rules.
  Use {{TOKEN}} syntax for any product names in src/data/vars.ts.]
---
[VARS: Add this line immediately after the closing --- above if this page references any product names from src/data/vars.ts. Then use {VARS.KEY} for those names in the prose below.
`import { VARS } from '@data/vars';`
See AGENTS.md → Content variables for the full variable list and usage rules.]

# [Title — sentence case. Title convention: noun describing contents, e.g., "CLI commands", "Keyboard shortcuts". Not a bare "Overview" or "Reference".]

[Brief intro: what this reference covers and how to use it.
1-2 sentences. This is for lookup, not learning.]

[BREVITY: Delete any section below you don't need — a short page is a finished page. See AGENTS.md → Voice & tone → Cut again.]

## [Section name — sentence case and specific. e.g., "Installing the CLI", "Authentication". Not "More details".]

[Introductory sentence or conceptual context for this section.]

## [Command/endpoint/option group — sentence case. e.g., "Running agents"]

[Use a strict repeating pattern for each entry. Every entry must
follow the same structure. Consistency is more important than style.

For commands/endpoints: name → syntax → description → flags/params → example
For settings/options: name → type → default → description

Use H2 for major sections, H3 for individual entries.
Use tables for multiple parameters, lists for single elements.]

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
