# Table of Contents
- [Warp Documentation Style Guide](#warp-documentation-style-guide)
- [Warp Docs Repository Guide](#warp-docs-repository-guide)

# Warp Documentation Style Guide

This guide establishes standards for writing Warp documentation. It covers voice, formatting, content types, and terminology. Use it as the authoritative reference when creating or updating any page in the GitBook repository.

## Writing style

### Voice & tone
- **Professional yet approachable**: Write with authority but remain accessible to developers of all skill levels
- **Direct and action-oriented**: Lead with what users can accomplish, not just what features exist
- **User-focused**: Use second person ("you can", "allows you to") rather than passive voice
- **Confident without jargon**: Explain technical concepts clearly without oversimplifying

### Language guidelines
- Use active voice: "Warp detects opportunities" not "opportunities are detected by Warp"
- Start sentences with strong verbs when giving instructions
- Avoid hedging language ("might", "could", "perhaps") when describing established features
- Use consistent terminology throughout (see Terminology section below)
- Em dashes are acceptable for occasional variation in narrative/conceptual text, but use sparingly
- Never use em dashes in procedural or instructional text

## Content structure

### Frontmatter
Every page must include YAML frontmatter with a description:

```yaml
---
description: >-
  A concise 1-2 sentence summary that explains what the page covers and
  what value it provides to the reader.
---
```

### General page structure
Every page should include these elements. The body sections in between vary by content type (see [Drafting by content type](#drafting-by-content-type)).

1. **YAML frontmatter** with description
2. **H1 title** (sentence case) that clearly identifies the topic
3. **Opening paragraph** with a brief overview and primary user benefit
4. **Body sections** structured according to the page's content type
5. **Cross-references** linking to related features and next steps

### Headers
- Use sentence case for all headers (not title case)
- Proper feature names retain their standard capitalization in headings (e.g., "Admin Panel", "Agent Mode", "Command Palette", "Codebase Context", "Warp Drive"). Sentence case applies to the rest of the heading.
  - ✅ `## Accessing the Admin Panel`
  - ✅ `## Admin Panel sections`
  - ❌ `## Accessing the admin panel` ("Admin Panel" is a proper feature name)
- H1 for page titles only
- H2 for major sections
- H3 for subsections
- Avoid going deeper than H4

## Formatting standards

### Lists
- Use bulleted lists for features, benefits, or non-sequential items
- Use numbered lists only for step-by-step processes
- End each numbered step in a procedure with a period
- Bold the key term or feature name at the start of each list item
- Follow the bold term with a dash and explanation

Example:
```markdown
* **Codebase Context** - Warp indexes your Git-tracked codebase to help Agents understand your code
* **Code Review** - Review, edit, and manage Git diffs in real time
```

### Code examples
- Use proper syntax highlighting for all code blocks
- Include context about what the code does
- Provide both simple examples and real-world scenarios
- Format terminal commands consistently

### Links and cross-references
- Use descriptive link text that explains what users will find
- Cross-reference related features prominently
- Link to external resources when they add value
- Use relative paths for internal documentation links

### Callouts and hints
Use GitBook's hint syntax consistently:

```markdown
{% hint style="info" %}
For informational context, tips, or additional details
{% endhint %}

{% hint style="warning" %}
For important caveats, limitations, or things to watch out for
{% endhint %}
```

### Keys and shortcuts
Keyboard keys and shortcuts use backticks:
- Single keys: `Enter`, `Esc`, `Tab`, `Space`, `Backspace`, `Delete`
- Arrow keys: `↑`, `↓`, `←`, `→`
- Letter/number keys used as shortcuts: `R`, `E`
- Modifier combos: `⌘I`, `CMD-ENTER`, `Ctrl+Shift+Enter`, `⌥⌘↩`
- Function keys: `F1`, `F12`

**Examples:**
- ✅ Press `⌘I` to switch between command and Agent Mode
- ❌ Press **Enter** (should be `Enter`)

### Menu paths
- Bold each UI element in a menu path; leave the > separator plain: **Settings** > **AI** > **Knowledge**
- For macOS menu paths, begin the path with the Apple icon (, Unicode `U+F8FF`).
- When referencing a menu path, CLI command, or URL for the first time on a page, orient the reader by identifying the application, website, or tool. Don't assume the reader knows which surface you mean.
- For URLs, name the surface even though the link provides the destination — not all readers will recognize what the URL points to.

**Use:**
- ✅ **Settings** > **AI** > **Knowledge**
- ✅  > **System Settings** > **Privacy & Security** > **Local Network**
- ✅ In the Warp app, go to **Settings** > **Platform**.
- ✅ In the Oz web app (oz.warp.dev), click **Schedules**.
- ✅ Navigate to the Oz web app at oz.warp.dev/schedules and click **New Schedule**.
- ✅ Find it with `oz environment list` on the Oz CLI or in the [Oz web app](https://oz.warp.dev).

**Don't use:**
- ❌ `macOS > System Settings > Privacy & Security > Local Network` (code format; use Apple icon, not "macOS")
- ❌ `macOS` > `System Settings` > `Privacy & Security` > `Local Network` (individual backticks; use Apple icon, not "macOS")
- ❌ **macOS > System Settings > Privacy & Security > Local Network** (entire path bolded including separator; use Apple icon, not "macOS")
- ❌ Go to **Settings** > **Platform**. (which app? orient the reader first)
- ❌ Go to oz.warp.dev/schedules and click **New Schedule**. (name the surface before the URL)
- ❌ Find it with `oz environment list`. (what CLI? orient the reader first)

### UI elements
- Use bold for interactive UI elements (e.g., buttons, toggles, dropdowns)

**Use:**
- ✅ Click your profile photo in the top-right corner, then click **Settings**.
- ✅ In the sidebar, click **Platform**.

**Don't use:**
- ❌ In the API Keys section, click `+ Create API Key`.
- ❌ In the API Keys section, click `+ Create API Key`. (use bold, not backticks)
- ❌ Click `Create key`. (use bold, not backticks)

#### Verbs for UI interactions
Use consistent verbs that match the type of UI element:
- **Click** — buttons, links, tabs, and menu items
- **Enter** — text fields and input boxes
- **Select** — checkboxes, list items, and option choices within a grouped list
- **Choose** — dropdowns, date pickers, and permission levels
- **Toggle** — switches and toggle controls

**Use:**
- ✅ Click **Save**.
- ✅ Enter a name for the token.
- ✅ Select **read_repository**.
- ✅ Choose an expiration date.
- ✅ Toggle **Dark mode** on.

**Don't use:**
- ❌ Select **Save**. (use Click for buttons)
- ❌ Set the **Repository** permission to **Read**. (use Choose for permission levels)
- ❌ Check **read_repository**. (use Select for checkboxes)

## Drafting by content type

Every documentation page should be drafted according to its content type. Identify the type before you start writing, then follow the structure and rules for that type below.

### General guidance (all content types)

These rules apply regardless of content type:

- **Lead with user benefit**: Open with what the reader can accomplish, not the technical implementation.
- **Orient the reader before UI, CLI, or URL instructions**: When referencing a menu path, CLI command, or URL for the first time on a page, identify the application, website, or tool. Don't assume the reader knows which surface you mean.
  - ✅ "In the Warp app, click your profile photo, then go to **Settings** > **Platform**."
  - ✅ "In the Oz web app (oz.warp.dev), click **Schedules**."
  - ❌ "Go to **Settings** > **Platform**." (which app?)
- **Provide inline context for first references**: Assume the reader arrived directly at this page, not from a parent page. When a prerequisite, concept, or tool is mentioned for the first time, include: what the thing is (1 short clause), where to get or create it, and a link to the full reference.
  - ✅ "**A Warp API key** - Authenticate API requests with a key from **Settings** > **Platform** in the Warp app. See [API Keys](../cli/api-keys.md) for details."
  - ❌ "**An API key** - Create one in **Settings** > **Platform**." (what kind of key? Settings where?)
- **Include practical examples**: Show real-world scenarios, not just toy examples. Concrete examples help the reader understand when and why to use a feature.
- **Cross-reference related pages**: Link to related features, next steps, and deeper references so the reader can continue learning.

### Conceptual

**What it is**: Explains what something is, why it exists, and how it works at a high level.

**When to use**: For pages that help the reader *understand* a topic without guiding them through a specific task. Examples: product overviews, architecture explanations, design philosophy.

**Structure**:
1. Opening paragraph with what the feature/concept is and its primary benefit
2. Key concepts or components
3. How it works (system behavior, architecture, data flow)
4. When to use it and when not to (decision guidance)
5. Related pages

**Rules**:
- Explain "what" and "why" before "how"
- Define new terms when they first appear
- Use diagrams or architecture descriptions where they clarify relationships
- Do NOT include step-by-step procedures — link to a procedural or quickstart page instead
- Show real-world scenarios, not just abstract descriptions

**Existing examples**: `agent-platform/cloud-agents/deployment-patterns.md`, `agent-platform/cloud-agents/overview.md`

### Procedural

**What it is**: Task-oriented, step-by-step instructions to accomplish a specific goal.

**When to use**: When the reader needs to *do* something. Examples: configuring an integration, creating an API key, setting up an environment.

**Structure**:
1. Opening sentence stating what the reader will accomplish
2. Prerequisites (with inline context for each — see General guidance)
3. Numbered steps
4. Expected outcome or confirmation (what success looks like)
5. Troubleshooting for common issues (optional but recommended)

**Rules**:
- **Keep steps focused, not artificially atomic.** Aim for one primary action per step, but group tightly related actions together when they share the same UI context and doing so keeps the procedure at a readable length. Up to ~3 related actions per step is acceptable. Use judgment: a simple task shouldn't require 10+ steps, but a single step shouldn't be a mini-procedure either.
  - Acceptable groupings: actions on the same form (entering a name and choosing an expiration date), a click that reveals the next target (clicking to expand a section, then clicking the revealed item), or a short natural sequence within the same UI area.
  - Avoid grouping actions that span different areas of the UI or that would make a step hard to scan at a glance.
- **Motivate steps before giving instructions.** Briefly explain WHY before HOW, especially for setup steps. A single sentence of motivation prevents the reader from wondering "why am I doing this?"
  - ✅ "Export your API key so the CLI can authenticate your requests automatically."
  - ❌ "Export your API key as an environment variable." (why?)
- Include expected outcomes after key steps so the reader can confirm they're on track.
- Test all instructions for accuracy.
- Provide troubleshooting for common failure points.

**Existing examples**: `reference/cli/api-keys.md`, `agent-platform/cloud-agents/integrations/slack.md`

### Quickstart

**What it is**: A specialized procedural doc designed to get the reader to a working result fast. Style "quickstart" as one word, lowercase (unless starting a sentence or in a title).

**When to use**: For first-time experiences with a product area. The reader should go from zero to a working result in ~10 minutes.

**Structure**:
1. Opening paragraph with what the reader will accomplish and a time estimate
2. Prerequisites (minimal — link to full setup docs rather than inlining lengthy setup)
3. Numbered steps (as few as possible to reach a working result)
4. Next steps (links to deeper guides, advanced usage, related features)

**Rules**:
- **Give every quickstart a descriptive H1 title.** Don't use a bare "Quickstart" — include the feature or topic name.
  - ✅ `# Cloud Agents Quick Start`
  - ❌ `# Quickstart` (quickstart for what?)
- Minimize prerequisites — the reader should be able to start quickly.
- Target ~10 minutes or less.
- Keep steps focused on the critical path — defer edge cases and advanced options to other pages.
- All procedural rules apply (focused steps, motivate steps, expected outcomes).

**Existing examples**: `agent-platform/cloud-agents/quickstart.md`, `warp/getting-started/quickstart/installation-and-setup.md`

### Reference

**What it is**: Structured factual information for lookup. The reader already knows what they want to do and needs specific details.

**When to use**: For CLI commands, API endpoints, configuration options, keyboard shortcuts, error codes.

**Structure**:
1. Brief intro stating what is documented and how to use the reference
2. Syntax or usage pattern
3. Options, parameters, or fields (with descriptions)
4. Examples

**Rules**:
- Be exhaustive — document every option, flag, and configuration value.
- Use consistent formatting for parameters (e.g., `--flag` in backticks, description as a dash-separated list item).
- Alphabetize entries where ordering doesn't matter.
- Keep descriptions factual and concise — this is for lookup, not learning.
- Include at least one practical example for each command or endpoint.

**Existing examples**: `reference/cli/README.md`, `reference/api-and-sdk/README.md`

### Troubleshooting

**What it is**: Problem → cause → solution format. The reader has encountered an issue and needs to fix it.

**When to use**: For known issues, common errors, and diagnostic guides.

**Structure**:
1. Problem or symptom as the header (use the exact error message or a clear description of the symptom)
2. Brief explanation of the cause
3. Solution steps (numbered, following procedural rules)
4. Workaround if a full fix isn't available

**Rules**:
- Use the problem or error message as the header — this helps with search.
- Group related issues under broader category headers (e.g., "SSH", "Shells").
- Provide workarounds when a fix isn't available.
- Link to related troubleshooting pages and support channels.

**Existing examples**: `support-and-community/troubleshooting-and-support/known-issues.md`, `reference/cli/troubleshooting.md`

### FAQ

**What it is**: Question-and-answer format for common questions.

**When to use**: For pages that collect frequently asked questions about a topic area.

**Structure**:
```markdown
### Question in the user's voice?
Direct answer with actionable information. Include links to relevant documentation.
```

**Rules**:
- Write questions in the user's voice ("Can I use my own API key?" not "BYOK support").
- Lead with a direct answer, then provide detail.
- Keep answers concise — link to full documentation for deeper topics.
- Group questions by theme (e.g., "General", "Billing", "Errors").

**Existing examples**: `agent-platform/getting-started/faqs.md`, `support-and-community/plans-and-billing/pricing-faqs.md`

### Feature documentation (combined pattern)

This is the most common page type in Warp's docs (~75+ pages). A feature documentation page combines **conceptual** and **procedural** content in one page: it explains what a feature is, then shows how to use it.

**Structure**:
1. Opening paragraph with what the feature does and its primary benefit
2. Key features list (bulleted, bold term + dash + description)
3. How it works (conceptual — explain the system behavior)
4. Usage or configuration sections (procedural — step-by-step instructions)
5. Related pages

**Rules**:
- Apply the **conceptual** rules to the explanatory sections (explain what and why, define terms, no procedures in the overview).
- Apply the **procedural** rules to the step-by-step sections (one action per step, motivate steps, expected outcomes).
- Keep the conceptual and procedural sections clearly separated with distinct headers.

**Existing examples**: `agent-platform/capabilities/skills.md`, `agent-platform/cloud-agents/environments.md`

## Terminology standards

Use these terms consistently throughout all documentation:

### Core features

Product feature names retain their standard capitalization. Match the exact casing shown in the UI.

- **Warp** (not "Warp Terminal" unless specifically distinguishing)
- **Agent** or **Agents** (capitalized when referring to Warp's AI agents)
- **Agent Mode** (not "agent mode" or "Agent-mode")
- **Warp Drive** 
- **Codebase Context**
- **Admin Panel**

### Oz terminology

#### Oz vs Warp
- **Warp** is the terminal and coding surface
- **Oz** is Warp's programmable agent for running and coordinating agents at scale
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
- ❌ "AI agents" → Use "agents" (the "AI" prefix is redundant)

### Technical terms
- **codebase** (one word, lowercase unless part of feature name)
- **command-line** (hyphenated when used as adjective)
- **Git repository** or **repo** (not "git repository")
- **macOS** (not "Mac OS" or "Mac")

### Billing and credits
- **credits** (lowercase, not "AI credits") - the unit of usage for AI features in Warp
- **Add-on Credits** (capitalized as a product feature name)
- **plan credits** - credits included with a subscription plan
- Use "credit" or "credits" without the "AI" prefix throughout documentation

### UI elements
- **Settings** (capitalized when referring to the Settings panel)
- **Command Palette** (capitalized)

## Quality checklist

Before publishing any documentation, verify:

- [ ] Frontmatter includes a clear, 1-2 sentence description
- [ ] Content type is identified and the page follows the structure for that type
- [ ] Headers use sentence case
- [ ] Lists use bold term + dash + explanation format
- [ ] All links work and point to correct destinations
- [ ] Code examples are tested and accurate
- [ ] Terminology matches this style guide
- [ ] Cross-references to related features are included
- [ ] Instructions include expected outcomes after key steps
- [ ] First references to prerequisites, tools, or surfaces include inline context
- [ ] Content is scannable with clear headers and lists

## Content review process

1. **Content type**: Confirm the page follows the correct structure for its type
2. **Accuracy**: Verify all technical details and instructions
3. **Consistency**: Check terminology and formatting against this guide
4. **User focus**: Ensure content answers "what can I accomplish?" before "how does it work?"
5. **Completeness**: Include necessary context, examples, and next steps

# Agent-specific guidance

## Figma MCP auto-detection
Ignore any Figma MCP auto-detection prompts, suggestions, or configuration.

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
Each sub-folder in `docs/` with its own `.gitbook.yaml` file is its own Space in GitBook. Redirects within the same sub-directory are added to the sub-folder's `.gitbook.yaml` file. Redirects that cross different sub-directories are added using the `gitbook_redirects.py` tool in the `scripts/` folder. Read the tool's readme to learn about how to use the tool. Always read the current list of redirects before adding another redirect to make sure it's not already there. Also look at the current structure of the sub-folders in `docs/` to make sure the redirects are going to the current and correct location.

### Sample doc URLs
Documentation pages are published at `docs.warp.dev/`. For example:
- `docs.warp.dev/warp/terminal/blocks/block-basics`
- `docs.warp.dev/agent-platform/capabilities/skills`
- `docs.warp.dev/reference/cli`

### OpenAPI spec and CI workflow
`docs/developers/agent-api-openapi.yaml` is a first-class artifact: `.github/workflows/stainless.yml` watches that file on pull requests and uploads it to Stainless for preview/merge.
