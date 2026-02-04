# Table of Contents
- [Warp Documentation Style Guide](#warp-documentation-style-guide)
- [Warp Docs Repository Guide](#warp-docs-repository-guide)

# Warp Documentation Style Guide

This guide establishes standards for writing documentation that matches Warp's voice, tone, and formatting conventions. Use this as a reference when creating or updating any documentation in the GitBook repository.

## Writing Style

### Voice & Tone
- **Professional yet approachable**: Write with authority but remain accessible to developers of all skill levels
- **Direct and action-oriented**: Lead with what users can accomplish, not just what features exist
- **User-focused**: Use second person ("you can", "allows you to") rather than passive voice
- **Confident without jargon**: Explain technical concepts clearly without oversimplifying

### Language Guidelines
- Use active voice: "Warp detects opportunities" not "opportunities are detected by Warp"
- Start sentences with strong verbs when giving instructions
- Avoid hedging language ("might", "could", "perhaps") when describing established features
- Use consistent terminology throughout (see Terminology section below)

## Content Structure

### Frontmatter
Every page must include YAML frontmatter with a description:

```yaml
---
description: >-
  A concise 1-2 sentence summary that explains what the page covers and 
  what value it provides to the reader.
---
```

### Page Structure
Follow this hierarchy for all documentation pages:

1. **H1 Title**: Clear, descriptive page title
2. **Opening paragraph**: Brief overview of the feature/topic and its primary benefit
3. **Key features section** (if applicable): Bulleted list of main capabilities
4. **How it works section**: Explain the user flow or core concepts
5. **Detailed sections**: Break down specific features, use cases, or instructions
6. **Cross-references**: Link to related features and next steps

### Headers
- Use sentence case for all headers (not title case)
- H1 for page titles only
- H2 for major sections
- H3 for subsections
- Avoid going deeper than H4

## Formatting Standards

### Lists
- Use bulleted lists for features, benefits, or non-sequential items
- Use numbered lists only for step-by-step processes
- Bold the key term or feature name at the start of each list item
- Follow the bold term with a dash and explanation

Example:
```markdown
* **Codebase Context** - Warp indexes your Git-tracked codebase to help Agents understand your code
* **Code Review** - Review, edit, and manage Git diffs in real time
```

### Code Examples
- Use proper syntax highlighting for all code blocks
- Include context about what the code does
- Provide both simple examples and real-world scenarios
- Format terminal commands consistently

### Links and Cross-References
- Use descriptive link text that explains what users will find
- Cross-reference related features prominently
- Link to external resources when they add value
- Use relative paths for internal documentation links

### Callouts and Hints
Use GitBook's hint syntax consistently:

```markdown
{% hint style="info" %}
For informational context, tips, or additional details
{% endhint %}

{% hint style="warning" %}
For important caveats, limitations, or things to watch out for
{% endhint %}
```

## Content Guidelines

### Feature Descriptions
- Lead with the user benefit, not the technical implementation
- Provide concrete examples of when and why to use the feature
- Include both overview and detailed usage sections
- Show real-world scenarios, not just toy examples

### Instructions
- Write clear, actionable steps
- Test all instructions for accuracy
- Include expected outcomes or confirmations
- Provide troubleshooting for common issues

### Examples and Use Cases
Always include practical examples:

```markdown
### Examples of Coding Capabilities
* **Code creation**
  * "Write a function in JavaScript to debounce an input"
  * "Generate a Python class for managing user sessions with Redis."
```

## Terminology Standards

Use these terms consistently throughout all documentation:

### Core Features
- **Warp** (not "Warp Terminal" unless specifically distinguishing)
- **Agent** or **Agents** (capitalized when referring to Warp's AI agents)
- **Agent Mode** (not "agent mode" or "Agent-mode")
- **Warp Drive** (always capitalized)
- **Codebase Context** (capitalized as a proper feature name)

### Oz terminology

#### Oz vs Warp
- **Warp** is the terminal and coding surface
- **Oz** is the programmable agent and orchestration-scaffolding that makes running cloud agents and automations easy
- There is typically one Warp environment per user session. Oz can run many agents concurrently, across machines, repos, and teams.

#### Core Oz terms
- **Oz** - Warp's programmable agent for running and coordinating agents at scale
- **Oz agent** - A combination of agent instructions (skill or prompt), trigger (cron, webhook, manual), environment (local, cloud), profile, and host. Agents can be local or cloud, and interactive or ambient.
- **Oz cloud agent** - An Oz agent running in the cloud, from a trigger, schedule, or started from someone's local machine
- **Oz subagent** - A child Oz agent created by a parent Oz agent to parallelize or delegate work
- **Oz run** - A single execution lifecycle of an Oz agent, including actions, outputs, and logs. Always ambient and cloud-based.
- **Oz conversation** - An interactive execution lifecycle within the Warp Terminal, regardless of whether it's local or in the cloud
- **Environment** - The execution context for an Oz agent, including repo access, dependencies, secrets, compute, and runtime configuration
- **Oz dashboard** - The app surface to manage all Oz runs, unified across the Warp app and web
- **Oz web app** - The web app for configuring Oz agents and managing runs

#### Oz CLI commands
- `oz agent run` - Run a local agent
- `oz agent run-cloud` - Run an adhoc cloud agent
- `oz integration create` - Install integrations (Slack, Linear)
- `oz environment create/list/get/update/delete` - CRUD on environments
- `oz schedule create/list/get/update/delete` - CRUD on scheduled ambient agents
- `oz secret create/list/update/delete` - CRUD on Warp-managed secrets
- `oz run list/get` - Get info on ambient agent runs

#### Preferred phrases
- ✅ "Ask Oz to..."
- ✅ "Oz can help you..."
- ✅ "What would you like Oz to do?"

#### Terms to avoid
- ❌ "Ozzies" → Use "Oz agents", "instances", or "Oz subagents"
- ❌ "Deploying an Oz" → Use "Deploying an Oz agent"
- ❌ "The Oz Agent" → Use "An Oz agent" or "A parent Oz agent"
- ❌ "Oz is running" → Use "An Oz agent is running" or "A run is in progress"

### Technical Terms
- **codebase** (one word, lowercase unless part of feature name)
- **command-line** (hyphenated when used as adjective)
- **Git repository** or **repo** (not "git repository")
- **macOS** (not "Mac OS" or "Mac")

### UI Elements
- **Settings** (capitalized when referring to the Settings panel)
- **Command Palette** (capitalized)
- Use backticks for menu paths: `Settings > AI > Knowledge`

## Common Patterns

### Feature Introduction Template
```markdown
# Feature Name

Brief description of what the feature does and its primary benefit.

## Key Features:
* **Sub-feature 1** - Description and benefit
* **Sub-feature 2** - Description and benefit

## How It Works
Explanation of user workflow and core concepts.
```

### Getting Started Section
Always include practical next steps:
```markdown
## Getting Started
1. [Action user should take first]
2. [Second step with expected outcome]
3. [Link to related features or advanced usage]
```

### FAQ Structure
For FAQ sections, structure as:
```markdown
### Question in user's voice?
Direct answer with actionable information. Include links to relevant documentation.
```

## Quality Checklist

Before publishing any documentation:

- [ ] Frontmatter includes clear description
- [ ] Content follows established structure
- [ ] All links work and point to correct destinations
- [ ] Code examples are tested and accurate
- [ ] Terminology matches this style guide
- [ ] Cross-references to related features are included
- [ ] Instructions include expected outcomes
- [ ] Content is scannable with clear headers and lists

## Content Review Process

1. **Accuracy**: Verify all technical details and instructions
2. **Consistency**: Check terminology and formatting against this guide
3. **User focus**: Ensure content answers "what can I accomplish?" before "how does it work?"
4. **Completeness**: Include necessary context, examples, and next steps
5. **Accessibility**: Test with users unfamiliar with the feature

---

*This style guide should evolve with Warp's documentation needs. Update it when establishing new patterns or conventions.*

# Warp Docs Repository Guide

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## What this repo is
This repo contains the source content for Warp’s GitBook documentation.

## Common commands

### Install dependencies
This repo uses `honkit` (a GitBook-compatible local renderer) as a dev dependency.

```bash
npm ci
```

### Preview docs locally
Serve the GitBook site from the `docs/` directory.

```bash
npx honkit serve docs
```

### Build the static site locally
Build the GitBook site from the `docs/` directory.

```bash
npx honkit build docs
```

### Lint / format
This repo is configured for the Trunk CLI via `.trunk/trunk.yaml`.

```bash
trunk check
trunk fmt
```

Notes:
- Enabled linters include `markdownlint`, `yamllint`, `gitleaks`, and `oxipng`.
- Trunk is not vendored in this repo; install it separately if you want to run these locally.

### Tests
There is no test suite configured in `package.json` (the `test` script intentionally exits with an error).

## Codebase structure and “big picture”

### GitBook root, navigation, and redirects
- **GitBook root** - `.gitbook.yaml` sets `root: ./docs/`, so GitBook (and `honkit`) treat `docs/` as the site root.
- **Sidebar / IA** - Each section directory (e.g., `docs/warp/`, `docs/agent-platform/`) contains its own `SUMMARY.md` that defines the table of contents for that section. If you add/move pages, update the relevant section's SUMMARY.md.
- **Landing pages** - `README.md` files serve as landing pages for folders and subfolders throughout the documentation hierarchy.
- **Redirects** - `.gitbook.yaml` contains a large `redirects:` map used to preserve old URLs after content moves. When you rename/move a page that's already published, add a redirect entry.

### Content organization
Documentation is organized into separate top-level section directories under `docs/`, each with its own `SUMMARY.md`:
- **warp/** - Warp Terminal and IDE documentation (Getting started, Terminal, Code, Knowledge and collaboration)
- **agent-platform/** - Agent Platform documentation (Agent, Ambient Agents, Integrations, Platform)
- **reference/** - Technical reference (CLI, API & SDK)
- **support-and-community/** - Support and community resources (Troubleshooting, Plans and billing, Privacy and security, Community)
- **enterprise/** - Enterprise documentation
- **changelog/** - Changelog
- **developers/** - Developer resources (API specs)

### Content model
The docs site has multiple levels of hierarchy:
- **Top-level category** (e.g., `docs/warp/`)
  - **Subcategories** (e.g., `docs/warp/terminal/`)
    - **Articles** (e.g., `docs/warp/code/code-overview.md`)

We organize content in logical groupings that help people find what they are searching for. We aim to limit the layers of hierarchy, with few nested subcategories, which can make it difficult to find help.

**Content order**: Organize content predictably in categories and subcategories, from broadest applicability to most specific. General order is: conceptual content, reference content, procedures, troubleshooting information.

### Assets
GitBook-managed images and GIFs live in `.gitbook/assets/` folder for each sub-folder in `docs/`.

### Redirects
Each sub-folder in `docs/` with it's own `.gitbook.yaml` file is it's own Space in GitBook. Redirects within the same sub-directory are added to the sub-folders `.gitbook.yaml` file. Redirects that cross different sub-directories are adding using the `gitbook_redirects.py` tool in the `scripts/` folder. Read the tool's readme to learn about how to use the tool. Always read the current list of redirects before adding another redirect to make sure it's not already there. Also look at the current structure of the sub-folders in `docs/` to make sure the redirects are going to the current and correct location.

### OpenAPI spec and CI workflow
`docs/developers/agent-api-openapi.yaml` is a first-class artifact: `.github/workflows/stainless.yml` watches that file on pull requests and uploads it to Stainless for preview/merge.
