# Table of Contents
- [Warp Documentation Style Guide](#warp-documentation-style-guide)
- [Warp Docs Repository Guide](#warp-docs-repository-guide)

# Warp Documentation Style Guide

This guide establishes standards for writing Warp documentation. It covers voice, formatting, content types, and terminology. Use it as the authoritative reference when creating or updating any page in the Astro Starlight repository.

## Writing style

### Voice & tone
- **Professional yet approachable**: Write with authority but remain accessible to developers of all skill levels
- **Direct and action-oriented**: Lead with what users can accomplish, not just what features exist
- **User-focused**: Use second person ("you can", "allows you to") rather than passive voice
- **Confident without jargon**: Explain technical concepts clearly without oversimplifying

### Language guidelines
- Use consistent terminology throughout (see [Terminology standards](#terminology-standards) and the full glossary in `.warp/references/terminology.md`)
- Em dashes are acceptable for occasional variation in narrative/conceptual text, but use sparingly
- Never use em dashes in procedural or instructional text

#### Active vs. passive voice
Use active voice whenever possible. Active voice is clearer and more direct.
- ✅ "Warp indexes your codebase to help Agents understand your code."
- ❌ "Your codebase is indexed by Warp to help Agents understand your code."

Passive voice is acceptable when the action's recipient is more important than the agent, or when the agent is unknown or irrelevant:
- ✅ "A critical security vulnerability was discovered in the authentication module." (emphasis on the vulnerability, not who found it)
- ✅ "The environment is destroyed after the run completes." (the system does this automatically; no human agent)

#### Ambiguous verbs
When a task is required, use clear, direct verbs. Avoid ambiguous modal verbs like "may," "might," "should," "could," "would," and "can" — these can be interpreted as either a command or a suggestion.
- ✅ "Use `oz agent run` to start a local agent." (required action)
- ✅ "You can optionally specify an Agent Profile." (clearly marked as optional)
- ❌ "You can use `oz agent run` to start a local agent." (is this required or optional?)
- ❌ "You should configure an environment before running cloud agents." (must I, or is it just a suggestion?)

#### Vague nouns and pronouns
If a pronoun could refer to more than one thing, replace it with the specific noun.
- ✅ "After you merge your pull request, you can delete the branch."
- ❌ "After you merge your pull request, you can delete it." (delete the PR or the branch?)

#### Stacked modifiers
Avoid strings of nouns that create ambiguity. Use prepositions to clarify relationships.
- ✅ "Default permissions for cloud agents"
- ❌ "Cloud agent default permission settings"

#### Nominalizations
Avoid turning verbs into nouns. Use the verb form for clearer, shorter sentences.
- ✅ "After the run completes, the container is destroyed."
- ❌ "After the completion of the run, the container undergoes destruction."

#### Invisible plurals
Avoid words that are ambiguous between singular and plural.
- ✅ "After the file is retrieved, select where to save it."
- ❌ "After file retrieval, select where to save it." (one file or many?)

### Punctuation and mechanics
- **Serial comma**: Always use it. "Environments, integrations, and schedules" — not "Environments, integrations and schedules."
- **Contractions**: Allowed and encouraged to match our approachable tone. Use "you're," "don't," "it's," "can't." Exception: avoid contractions in error messages or formal warnings.
- **Tense**: Use present tense to describe how things work ("Warp indexes your codebase"). Use imperative for instructions ("Configure your environment").
- **Person**: Use second person ("you") for instructions. Avoid first person plural ("we") in procedural content. First person is acceptable in conceptual or narrative text when referring to Warp as a company ("We designed Oz to...").

### Inclusive language
- Use gender-neutral pronouns ("they/them") for unknown users
- Avoid ableist language ("simple," "easy," "just" — these dismiss the reader's experience)
- Avoid culturally specific idioms or slang that may not translate across regions
- Describe UI elements by name and function, not by appearance alone (supports screen readers and non-visual contexts)

### Writing for accessibility and agents

These practices serve both human accessibility needs and AI agent consumption (AEO — Answer Engine Optimization).

**Accessibility:**
- Include captions or a brief text summary for video embeds so content is accessible without playing the video
- Don't rely on color alone to convey meaning (e.g., "the green status badge"). Always pair color with a text label (e.g., "the **Active** status badge")
- Use header rows in tables. Keep tables simple — avoid deeply nested structures
- Many rules in this guide (active voice, short sentences, plain language, descriptive links, alt text) also serve non-native English speakers and screen reader users

**Writing for agents (AEO):**
- **Descriptive headers**: Use specific, parseable headers ("Configuring environments") not vague ones ("Getting set up"). Agents use headers as semantic signals to extract answers.
- **Explicit context**: Don't assume the reader arrived from a parent page. State what a thing is before explaining how to use it. This helps agents extract self-contained answers.
- **Frontmatter descriptions**: Agents and search engines use the `description` field to determine relevance before reading the full page. Write descriptions as standalone summaries.
- **Consistent terminology**: Agents struggle when the same concept has multiple names. Use the glossary terms consistently.
- **Machine-parseable patterns**: Consistent list formats, code block labeling, and parameter tables help agents extract structured information. The templates in `.warp/templates/` enforce this.

## Content structure

These structural rules apply to all pages regardless of content type. For type-specific page structures, see the templates in `.warp/templates/`.

### Frontmatter
Every page must include YAML frontmatter with a `description` field.

```yaml
---
description: >-
  A concise 1-2 sentence summary that explains what the page covers and
  what value it provides to the reader.
---
```

Write descriptions as standalone summaries that would make sense in a search result. Lead with the user benefit, include key terms for the topic.
- ✅ `description: Environments ensure your cloud agents run with consistent toolchains across all triggers. Learn when to use environments and how to configure them.`
- ❌ `description: This page describes environments.`

The `description` field is used as the meta description in search results — write it as a summary that would make someone click.

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

### File and URL naming
File names become URL slugs in Astro Starlight. Use lowercase, hyphens, and descriptive names that include key terms.
- ✅ `environments.md` → `/environments`
- ✅ `agent-profiles-permissions.md` → `/agent-profiles-permissions`
- ❌ `setup-guide-v2.md`, `new-page.md`, `doc1.md`

Clean, descriptive URLs rank better in search and are more shareable.

### Page length and scannability
- Aim for scannable pages. Use clear section headers, short paragraphs (2-4 sentences), and bulleted lists.
- If a page exceeds ~1500 words, consider breaking it into sub-pages or using clear anchor links.
- Avoid thin pages with only a sentence or two — consolidate with related content instead. When two pages cover nearly the same topic, merge them.

### Opening paragraphs
The first paragraph sets expectations for the entire page. Lead with what the feature does and its primary benefit.
- ✅ "Environments ensure your cloud agents run with the same toolchain and setup every time, regardless of where they're triggered from."
- ❌ "This page explains environments."

Search engines and AI agents give extra weight to the first paragraph. Lead with the key terms and the user benefit.

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

### Emphasis
Use formatting consistently to distinguish different types of content:
- **Bold** — UI elements, key terms on first use in a list, feature names in context
- *Italic* — introducing a new term inline (not a feature name), titles of external works
- `Backticks` — code, commands, file paths, keyboard keys, config values, CLI flags
- Underline — avoid (poor web accessibility, looks like a link)

### Code examples
- Always specify the language identifier for syntax highlighting (`bash`, `yaml`, `json`, etc.)
- For terminal commands: use `bash` language. Include `$` prompt only if showing output alongside the command.
- For file contents: use the appropriate language and add a title on the fence, e.g., ` ```yaml title="config.yaml" `
- For placeholder values in commands, use ALL_CAPS: `export WARP_API_KEY=YOUR_API_KEY`
- Use angle brackets in syntax descriptions: `oz agent run <agent-name>`
- Always explain what a placeholder represents
- Include context about what the code does
- Provide both simple examples and real-world scenarios

### Images and media
- Always include descriptive alt text (describe what the image shows, not just "screenshot")
  - ✅ `alt="Creating a new environment in the Oz Web App"`
  - ❌ `alt="screenshot"` or `alt=""`
- Use `<figure>` with `<figcaption>` for images that need captions
- Prefer GIFs for short interactions (under ~15 seconds). Use video embeds for longer demos.
- File naming: lowercase, hyphens, descriptive (`agent-mode-code-diff.png`, not `Screenshot 2026-03-15.png`)
- Store PNGs in `src/assets/<section>/` (Astro optimizes them) and GIFs in `public/assets/<section>/` (to bypass optimization). See the "Assets" section below for the full convention.

### Links and cross-references
- Use descriptive link text that explains what users will find
  - ✅ "Learn more about [Codebase Context](...)" / "See [configuring environments](...)"
  - ❌ "Click [here](...)" / "See [this page](...)"
- Cross-reference related features prominently
- Link to external resources when they add value
- Within an Astro Starlight space, use relative paths. For cross-space links, use absolute URLs (`https://docs.warp.dev/...`)
- Descriptive anchor text helps search engines understand page relationships. "Click here" provides no signal; "configuring environments" tells search engines what the linked page is about.

### Callouts and hints
Use Astro Starlight's hint syntax. Choose the style based on the type of information:

- `:::note` — supplemental context, tips, "good to know" information
- `:::caution` — caveats, limitations, things that could cause confusion or errors
- `:::danger` — destructive actions, irreversible operations, security implications
- `:::tip` — confirmation of expected outcomes, "you're on the right track"

```markdown
:::note
For informational context, tips, or additional details
:::

:::caution
For important caveats, limitations, or things to watch out for
:::
```

Use callouts sparingly. A page with 5+ callouts loses its visual impact.

### Placeholders and dynamic text
- Use ALL_CAPS for placeholder values in commands: `git clone REPO_URL`
- Use angle brackets in syntax descriptions: `oz agent run <agent-name>`
- Use ALL_CAPS for text that changes in the UI: Click **Add** USERNAME **to** REPONAME.
- Always explain what the placeholder represents near where it appears

### Keys and shortcuts
Keyboard keys and shortcuts use backticks. Use `+` as the separator between keys in a combo. Capitalize only the first letter of each key name (matching keyboard labels). Prefer macOS symbols (`⌘`, `⌥`, `⇧`, `⌃`) when targeting macOS users.
- Single keys: `Enter`, `Esc`, `Tab`, `Space`, `Backspace`, `Delete`
- Arrow keys: `↑`, `↓`, `←`, `→`
- Letter/number keys used as shortcuts: `R`, `E`
- Modifier combos (macOS symbols): `⌘+I`, `⌘+Shift++`
- Modifier combos (spelled out): `Ctrl+G`, `Ctrl+Shift+Enter`
- Cross-platform: `⌘+Shift++` (macOS) or `Ctrl+Shift++` (Windows/Linux)
- Function keys: `F1`, `F12`

**Rules:**
- Always use backticks, never bold
- Use `+` as separator (not `-`), to avoid ambiguity with the minus/hyphen key
- Capitalize only the first letter: `Ctrl`, `Shift`, `Enter` (not `CTRL`, `SHIFT`, `ENTER`)
- When a `+` key is part of the shortcut, context makes it clear: `⌘+Shift++` means Cmd, Shift, and the plus key

**Examples:**
- ✅ Press `⌘+I` to switch between command and Agent Mode
- ✅ Open the Code Review panel with `⌘+Shift++` (macOS) or `Ctrl+Shift++` (Windows/Linux)
- ✅ Press `Ctrl+G` to open the rich input editor
- ❌ Press **Enter** (should be `Enter`)
- ❌ `CMD-ENTER` (should be `⌘+Enter` or `Cmd+Enter`)
- ❌ `CTRL+G` (should be `Ctrl+G`)

### Menu paths
- Bold each UI element in a menu path; leave the > separator plain: **Settings** > **AI** > **Knowledge**
- For macOS menu paths, begin the path with the Apple icon (, Unicode `U+F8FF`).
  - **IMPORTANT — preserving the Apple icon**: The `U+F8FF` character is in Unicode's Private Use Area. It renders as the Apple logo only on Apple devices and is **invisible in most editors, terminals, and AI contexts**. It is frequently stripped during edits. When editing any line with a macOS menu path, always verify this character (UTF-8 bytes `EF A3 BF`) is present before the first `>`. If it has been stripped, re-insert it with: `printf '\xEF\xA3\xBF'`
- When referencing a menu path, CLI command, or URL for the first time on a page, orient the reader by identifying the application, website, or tool. Don't assume the reader knows which surface you mean.
- For URLs, name the surface even though the link provides the destination — not all readers will recognize what the URL points to.

**Use:**
- ✅ **Settings** > **AI** > **Knowledge**
- ✅   > **System Settings** > **Privacy & Security** > **Local Network**
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
- ❌ **System Settings** > **Privacy & Security** > **Local Network** (macOS path missing the Apple icon — `U+F8FF` must appear before the first `>`)

### UI elements
- Use bold for interactive UI elements (e.g., buttons, toggles, dropdowns)
- Describe UI elements by name, not just appearance or location. Prefer "In the sidebar, click **Platform**" over "Click the button on the left."
- Format checkbox names in bold. Omit the word "checkbox." Use "select" or "deselect," not "check" or "uncheck."

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
  - ✅ "**A Warp API key** - Authenticate API requests with a key from **Settings** > **Platform** in the Warp app. See the API Keys reference for details."
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

**Existing examples**: `agent-platform/cloud-agents/deployment-patterns.mdx`, `agent-platform/cloud-agents/overview.mdx`

**Template**: `.warp/templates/conceptual.md`

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

**Existing examples**: `reference/cli/api-keys.mdx`, `agent-platform/cloud-agents/integrations/slack.mdx`

**Template**: `.warp/templates/procedural.md`

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

**Existing examples**: `agent-platform/cloud-agents/quickstart.mdx`, `getting-started/quickstart/installation-and-setup.mdx`

**Template**: `.warp/templates/quickstart.md`

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

**Existing examples**: `reference/cli/index.mdx`, `reference/api-and-sdk/index.mdx`

**Template**: `.warp/templates/reference.md`

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

**Existing examples**: `support-and-community/troubleshooting-and-support/known-issues.mdx`, `reference/cli/troubleshooting.mdx`

**Template**: `.warp/templates/troubleshooting.md`

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

**Template**: `.warp/templates/faq.md`

**Existing examples**: `agent-platform/getting-started/faqs.mdx`, `support-and-community/plans-and-billing/pricing-faqs.mdx`

### Guide (Guides section)

**What it is**: A practical, task-oriented walkthrough that helps a developer accomplish a specific goal using Warp. Guides live in the `src/content/docs/university/` directory (the "Guides" Astro Starlight space) and can include video, written steps, or both.

**When to use**: For educational content that teaches a workflow or use case — not feature documentation (which belongs in the main docs). Guides focus on the "how" with real prompts and reproducible results.

**Structure**:
1. Frontmatter with `description` (for SEO and search)
2. H1 title — task-oriented, reads like a search query (e.g., "How to Set Up Claude Code" not "Claude Code Setup Tutorial")
3. One-sentence goal — what the reader will accomplish
4. Video embed (if applicable) — kept but not the primary content
5. Prerequisites (if any)
6. Numbered steps with exact prompts/commands
7. Inline explanation of why at decision points. Link to open-source repos when available.
8. Productivity tips (optional) — showcase relevant features as natural workflow extensions
9. "What you achieved" summary at the end with links to related docs

**Rules**:
- Titles should be task-oriented and scannable. Use shortened titles in the Astro Starlight nav and full descriptive titles in the article H1.
- For SEO: capture the non-branded query when possible. Write the title a developer would actually search for ("How to Set Up Claude Code" not "How to Set Up Claude Code in Warp").
- All procedural rules apply (focused steps, motivate steps, expected outcomes).
- Link to relevant feature documentation in the main docs where concepts need deeper explanation.
- When a guide has a companion video, the written content should stand alone — a reader should be able to follow the guide without watching the video.

**Template**: A copyable starting template is available at `.warp/templates/guide-page.md`. Use this when creating new guide pages.

**Existing examples**: `university/mcp-servers/sentry-mcp-fix-sentry-error-in-empower-website.mdx`, `university/end-to-end-builds/building-a-real-time-chat-app-github-mcp-+-railway.mdx`


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

**Existing examples**: `agent-platform/capabilities/skills.mdx`, `agent-platform/cloud-agents/environments.mdx`

**Template**: `.warp/templates/feature-doc.md`

## Page templates

Concrete page scaffolds for each content type are in `.warp/templates/`. Use these as starting points when creating new pages:

- `.warp/templates/conceptual.md`
- `.warp/templates/procedural.md`
- `.warp/templates/quickstart.md`
- `.warp/templates/reference.md`
- `.warp/templates/troubleshooting.md`
- `.warp/templates/faq.md`
- `.warp/templates/guide-page.md`
- `.warp/templates/feature-doc.md`

Each template includes inline HTML comments explaining what to put in each section and why.

## Terminology standards

Use these terms consistently throughout all documentation. For the full canonical glossary with usage notes, see `.warp/references/terminology.md`.

### Core features

Product feature names retain their standard capitalization. Match the exact casing shown in the UI.

- **Warp** (not "Warp Terminal" unless specifically distinguishing)
- **Agent** or **Agents** (capitalized when referring to Warp's AI agents)
- **Agent Mode** (not "agent mode" or "Agent-mode")
- **Terminal and Agent modes** - The two distinct modes in Warp: terminal mode (for shell commands) and Agent Mode (for multi-turn agent conversations). Use "Terminal and Agent modes" on first reference; use "terminal mode" or "Agent Mode" individually in subsequent references. Do not use "agent modality" or "Agent Modality" — this was an internal name that is not user-facing.
- **Ambient Agents** (capitalized as a feature/section name; lowercase "ambient agents" only when describing the generic concept)
- **Warp Drive** - Shared workspace for saving and organizing commands, workflows, and environment variables across your team.
- **Codebase Context** - Warp indexes your Git-tracked codebase to help Agents understand your code.
- **Admin Panel** - Team management surface for controlling members, roles, and billing.
- **Agent Management Panel** - Interface for viewing and managing running agents (not "agent dashboard" or "agent manager").

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
- ❌ "Agent Modality" or "agent modality" → Use "Terminal and Agent modes" (this was an internal name, not user-facing)

### Technical terms
- **AI** (not "A.I.")
- **allowlist** / **denylist** (not "whitelist" / "blocklist")
- **codebase** (one word, lowercase unless part of feature name)
- **command-line** (hyphenated when used as adjective)
- **Git repository** or **repo** (not "git repository")
- **macOS** (not "Mac OS" or "Mac")

### Billing and credits
- **credits** (lowercase, not "AI credits") - the unit of usage for AI features in Warp
- **Add-on Credits** (capitalized as a product feature name)
- **Cloud Agent Credits** (capitalized as a billing feature name)
- **plan credits** - credits included with a subscription plan
- Use "credit" or "credits" without the "AI" prefix throughout documentation

### UI elements
- **Settings** (capitalized when referring to the Settings panel)
- **Command Palette** (capitalized)

## SEO and AEO (AI Engine Optimization)

All documentation should be written with search discoverability in mind — both for traditional search engines (Google) and AI engines (ChatGPT, Gemini, Perplexity, Copilot).

### Frontmatter descriptions
- Every page must have a `description` in frontmatter. Write it as a standalone summary (50-160 characters) that includes the primary keyword naturally.
- Descriptions appear in search results and AI citations. Write for humans, but include the key terms a developer would search for.

### Title framing
- For guides and educational content: capture the **non-branded query** when possible. Write the title a developer would actually search for.
  - ✅ "How to Set Up Claude Code"
  - ❌ "How to Set Up Claude Code in Warp"
- For feature documentation: use the feature name as the developer knows it.

### SEO data
When creating or updating content, use SEO and AEO data to inform titles, descriptions, and content coverage. The `docs-seo-audit` skill (`.warp/skills/docs-seo-audit/`) can identify technical SEO issues.

## Quality checklist

Before publishing any documentation, verify:

- [ ] Frontmatter includes a clear, 1-2 sentence description written as a standalone summary
- [ ] Content type is identified and the page follows the structure for that type (see `.warp/templates/`)
- [ ] Headers use sentence case (with proper feature name capitalization)
- [ ] Lists use bold term + dash + explanation format
- [ ] All links work and point to correct destinations
- [ ] Code examples are tested and accurate
- [ ] Terminology and product names match the glossary (`.warp/references/terminology.md`)
- [ ] Cross-references to related features are included
- [ ] Instructions include expected outcomes after key steps
- [ ] First references to prerequisites, tools, or surfaces include inline context
- [ ] Content is scannable with clear headers and lists
- [ ] Images have descriptive alt text (not "screenshot" or empty)
- [ ] File name is lowercase, hyphenated, and descriptive (it becomes the URL slug)
- [ ] Frontmatter description includes the primary keyword naturally (50-160 chars)

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
This repo contains the source content for Warp’s Astro Starlight documentation.

## Common commands

### Install dependencies

```bash
npm install
```

### Preview docs locally

```bash
npm run dev
```

Open [http://localhost:4321](http://localhost:4321) to preview locally.

### Build the static site locally

```bash
npm run build
```

Build output goes to `./dist/`. Deployed via Vercel.

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
No test suite. Run `npm run build` to validate all content compiles correctly.

## Codebase structure and “big picture”

### Site framework
This site is built with [Astro](https://astro.build) + [Starlight](https://starlight.astro.build). Content is written in MDX (Markdown with JSX components).

### Navigation and redirects
- **Sidebar** — Defined in `astro.config.mjs` via the `starlight-sidebar-topics` plugin. Each top-level directory becomes a tab. If you add/move pages, update the sidebar config in `astro.config.mjs`.
- **Landing pages** — `index.mdx` files serve as landing pages for directories.
- **Redirects** — `vercel.json` contains all redirects. When you rename/move a published page, add a redirect entry.

### Content organization
Content lives in `src/content/docs/`, organized by topic:
- **terminal/** — Warp Terminal features (blocks, editor, sessions, appearance, etc.)
- **code/** — Code editor, code review, git worktrees
- **getting-started/** — Installation, quickstart, migration
- **knowledge-and-collaboration/** — Warp Drive, teams, admin panel
- **agent-platform/** — Agent Platform (capabilities, local agents, cli agents, cloud agents)
- **reference/** — CLI and API/SDK reference
- **support-and-community/** — Troubleshooting, billing, privacy
- **enterprise/** — Enterprise features, SSO, team management
- **changelog/** — Release changelog
- **university/** — Guides and tutorials

### Content model
The docs site has multiple levels of hierarchy:
- **Top-level section** (e.g., `src/content/docs/agent-platform/`)
  - **Subsections** (e.g., `src/content/docs/agent-platform/capabilities/`)
    - **Articles** (e.g., `src/content/docs/agent-platform/capabilities/skills.mdx`)

We organize content in logical groupings that help people find what they are searching for. We aim to limit the layers of hierarchy, with few nested subcategories, which can make it difficult to find help.

**Content order**: Organize content predictably in categories and subcategories, from broadest applicability to most specific. General order is: conceptual content, reference content, procedures, troubleshooting information.

### Assets
- **Static images (PNG)** live in `src/assets/` organized by section (e.g., `src/assets/terminal/`, `src/assets/agent-platform/`). Astro optimizes these at build time.
- **GIFs** live in `public/assets/` (same section structure) to bypass image optimization.
- Reference images using relative paths from content files: `![alt](../../../assets/terminal/image.png)` for PNGs, `![alt](/assets/terminal/animation.gif)` for GIFs.

### Redirects
All redirects are in `vercel.json` at the repo root. When renaming or moving a page, add a redirect entry. Check the current list before adding to avoid duplicates.

### Content format
Pages use MDX with Starlight components:
- **Callouts**: `:::note`, `:::tip`, `:::caution`, `:::danger`
- **Tabs**: `<Tabs>` / `<TabItem>` (import from `@astrojs/starlight/components`)
- **Video embeds**: `<VideoEmbed url="..." />` (import from `@components/VideoEmbed.astro`)
- **Steps**: `<Steps>` (import from `@astrojs/starlight/components`)
- **Code blocks**: Standard fenced code blocks with Expressive Code features (titles, line highlighting)

### Adding pages
1. Create an `.mdx` file in the appropriate directory under `src/content/docs/`
2. Use `index.mdx` for directory landing pages
3. Add the page to the sidebar config in `astro.config.mjs`
4. Add images to `src/assets/` (PNGs) or `public/assets/` (GIFs)

### Sample doc URLs
Documentation pages are published at `docs.warp.dev/`. For example:
- `docs.warp.dev/terminal/blocks/block-basics`
- `docs.warp.dev/agent-platform/capabilities/skills`
- `docs.warp.dev/reference/cli`

### OpenAPI spec
`developers/agent-api-openapi.yaml` is the OpenAPI spec for the Warp Agent API.
