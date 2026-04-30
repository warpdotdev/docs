---
description: >-
  [1-2 sentences: what is documented and how to use this reference.
  Example: "Use the Oz CLI to run, configure, and manage agents from the terminal."]
---

# [Title — sentence case. Title convention: noun describing contents, e.g., "CLI commands", "Keyboard shortcuts"]

[Brief intro: what this reference covers and how to use it.
1-2 sentences. This is for lookup, not learning.]

## [Section name — sentence case. e.g., "Installing the CLI", "Authentication"]

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
