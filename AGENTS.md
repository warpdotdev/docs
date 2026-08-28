# Table of Contents
- [Warp Documentation Style Guide](#warp-documentation-style-guide)
- [Warp Docs Repository Guide](#warp-docs-repository-guide)

# Warp Documentation Style Guide

This guide establishes standards for writing Warp documentation. It covers voice, formatting, content types, and terminology. Use it as the authoritative reference when creating or updating any page in the Astro Starlight repository.

## Writing style

### Voice & tone
- **Professional yet approachable**: Write with authority but remain accessible to developers of all skill levels
- **Direct and action-oriented**: Lead with what users can accomplish, not just what features exist
- **User-focused**: Use second person ("you") and active voice
- **Confident without jargon**: Explain technical concepts clearly without oversimplifying
- **Plain over polished**: Prefer the short word and the declarative sentence. A page should read like a capable colleague explaining something, not like a spec or a launch post.

Our reference points are the GitHub and Vercel docs: short declarative sentences, concrete examples, restrained formatting, and no selling.

#### Define, show, link
Introduce a concept in one to three plain sentences, give a concrete example, then link out for depth. Repeat that pattern instead of front-loading the page with context.
- ✅ "A workflow is an automated process that runs one or more jobs. For example, a workflow can label new issues automatically. For more information, see [Writing workflows](...)."
- ❌ "Before diving into the components, it helps to align on a few terms:" followed by a glossary of everything the page explains later anyway.

#### Document the user-visible model, not our architecture
Describe what the reader sees and does. Internal components get at most one sentence, and only when the reader can act on them. GitHub Actions runs on an orchestrator and a control plane; its docs never mention either. They describe workflows, events, jobs, and runners, because those are what users touch.
- ✅ "Warp tracks every run. Check its status from the CLI, the API, or the dashboard."
- ❌ "The orchestration layer runs on Warp's servers (cloud control plane), creates tasks when triggers fire, and tracks lifecycle state (created → running → completed/failed)."

This is the voice-level version of "Don't over-specify counts or internals that will drift" (see General guidance): internals aren't just a staleness risk, they're noise between the reader and the task.

When a page carries real information in the wrong register (provenance, pinned versions, maintainer process), relocate it to the surface whose audience needs it: a reference page, a script docstring, a code comment. Leave a pointer if the reader might follow the thread. Cutting for tone must not lose facts; it changes where they live.

#### Every sentence earns its place
Cut sentences that narrate the page, restate what the reader just read, or explain the obvious consequence of the previous sentence.
- **No meta-openers** - Never open with "This page covers/explains/walks through...". The title and description already frame the page; state the thing itself.
  - ✅ "Run agents directly in your GitHub Actions workflows using `oz-agent-action`."
  - ❌ "This page covers how the integration works, how to set it up, and common automation patterns for development teams."
- **No restated cause-and-effect** - Don't follow a fact with a sentence explaining why that fact is good.
  - ✅ "The container is destroyed after each run, so every run starts clean."
  - ❌ "The container is destroyed after each run. This process ensures every run starts from the same baseline, making results reproducible and debugging straightforward."
- **No recap lines** - Don't end a section by summarizing it ("In practice: triggers create tasks; tasks produce outputs.").
- **Say it once** - Don't repeat a caveat or definition across multiple sections of the same page. Put it where it matters most. The same goes for sibling pages: boilerplate like validation steps or shared prerequisites lives once on the parent or reference page, linked from the rest.
  - ✅ State a plan-tier requirement once in a `:::note` near the top of the section, then let a later procedure that depends on it link back rather than restating it.
  - ❌ Repeating the same "requires a Build plan or higher" caveat both in a section-level note and again inside a numbered step further down the page.

#### Words to avoid
These words are the strongest tell of an AI-generated draft and rarely add meaning. Replace them with the specific fact they're hiding, or delete them.
- **Marketing adjectives** - seamless(ly), powerful, robust, comprehensive, effortless, cutting-edge, game-changing, supercharged
- **Inflated verbs** - leverage (→ use), streamline (→ remove steps), empower (→ let), unlock (→ name the capability, or delete), delve into (→ cover), elevate, harness
- **Filler frames** - "designed to", "ensures that", "allows you to", "it's important to note", "it's worth noting", "in order to" (→ to)
- **Abstract dramatics** - landscape, realm, journey, tapestry, testament to

**Examples:**
- ✅ "The agent runs in your CI pipeline. It can review code, triage issues, and fix failing checks."
- ❌ "The agent integrates seamlessly into your CI pipeline, automating tasks like code review, issue triage, bug fixing, and maintenance."

If the claim is true, the reader notices without the adjective. If it isn't, the adjective won't save it.

#### Structural patterns to avoid
AI-drafted pages share a rhythm. Break it.
- **Rule-of-three padding** - Triplets of adjectives or clauses used for cadence rather than information ("scalable, autonomous, and auditable"). Keep the items that carry weight and cut the rest.
- **Rhetorical question openers** - Don't open a section with a question you immediately answer. Use a descriptive header and a declarative first sentence.
- **Hedging stacks** - Chains of "typically", "often", "generally", "where supported", and "as applicable" read as evasive. State what happens, then note the exception if there is one.
- **Bold-everything** - Bolding several phrases per paragraph kills emphasis. Reserve bold for UI elements and lead terms of list items (see Emphasis).
- **Bullets as a substitute for prose** - Bullets are for short, parallel, scannable items. If every bullet is a full paragraph, or the bullets tell a story in order, write prose.
- **Slashed shorthand** - Write "mentions and assignments", not "mention/assignment", and "4 vCPU / 8 GB", not "4/8". Slashed pairs and bare number pairs read as notes, not prose.
- **Callout spam** - Callouts follow the same restraint: never consecutive, at most one per section (see Callouts and hints).

#### Keep the author out of it
The reader came for the product, not the writer's presence in the page.
- **No self-commentary** - Don't narrate authorial intent: "deliberately unremarkable", "each prompt is worth reading", "that is the point of this example". State the fact and let it stand.
- **State rules calmly, once** - Defensive phrasing ("Do not describe or imply otherwise", "CI green is not the bar") argues with an imagined reader. Write the rule once, plainly, and give a reason only when the reason changes what the reader does.
- **Describe the present** - Write how the product works now. Renames and history belong in time-boxed transition notes or the changelog, not woven through pages ("the built-in harness is the Warp Agent harness", not "Oz is retired product language").

#### The read-aloud test
Read the paragraph aloud. If it doesn't sound like something you'd say to a colleague, rewrite it plainly. This catches over-explained cause-and-effect, hedging, and repeated rhetorical patterns faster than any checklist.

#### Cut again
A plain-language rewrite still under-cuts on the first pass. Follow it with a deletion-only pass that removes:
- Framing lines that describe the docs instead of the product ("Each example demonstrates one concept").
- Explanations of command output that the command already prints, or that a linked page already owns.
- Recaps and comparison sections that restate what the reader just read.
- Justifications for rules and defaults that don't change what the reader does.

Expect the second pass to find real deletions even after a careful first one; review feedback on past copy passes has consistently asked for more cutting, not less.

### Language guidelines
- Use consistent terminology throughout (see [Terminology standards](#terminology-standards) and the full glossary in `.agents/references/terminology.md`)
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
- **Person**: Use second person ("you") for instructions. Avoid first person plural ("we") in procedural content. First person is acceptable in conceptual or narrative text when referring to Warp as a company ("We designed the Automation Platform to...").

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
- **Machine-parseable patterns**: Consistent list formats, code block labeling, and parameter tables help agents extract structured information. The templates in `.agents/templates/` enforce this.

## Content structure

These structural rules apply to all pages regardless of content type. For type-specific page structures, see the templates in `.agents/templates/`.

### Frontmatter
Every page must include YAML frontmatter with a `description` field.

```yaml
---
description: >-
  One sentence, 50-160 characters, stating what the reader gets from this page.
---
```

The `description` field is the meta description in search results and the snippet AI engines read before deciding whether to cite the page. Write it as a standalone summary for someone who has never seen the page.
- ✅ `description: Environments give cloud agents the same toolchain and setup on every run, no matter what triggers them.`
- ❌ `description: This page describes environments.`

#### Description rules
These apply to every page, regardless of content type.
- **One sentence, 50-160 characters.** Search engines truncate past roughly 160. Two sentences almost always overshoot the budget, so prefer one that earns its length.
- **Cut filler openers.** "Learn about," "This page covers," "A guide to," and "Documentation for" spend characters without adding meaning. Start with the verb or the subject instead.
- **Describe what the reader gets, not what the page is.** "This page explains X" is always weaker than explaining X.
- **Lead with the primary keyword** when it reads naturally, ideally within the first few words.
- **Match the page's actual scope.** A description that promises more than the page delivers reads as a bait-and-switch in search results.

#### Descriptions by content type
Every description answers "what will I get from this page?" The shape of that answer depends on the type.
- **Conceptual** - Say what the thing is and why it matters. Start with the subject.
  - ✅ `Environments give cloud agents the same toolchain and setup on every run, no matter what triggers them.`
  - ❌ `Learn about environments and why they are useful.`
- **Procedural** - Say what task the reader will complete. Start with an imperative verb.
  - ✅ `Connect Slack to the Automation Platform so mentions and channel messages can trigger cloud agent runs.`
  - ❌ `This page explains the Slack integration setup process.`
- **Quickstart** - Say what the reader ends up with, plus the time budget. Start with an imperative verb.
  - ✅ `Install the Warp Agent CLI, log in, and run your first agent conversation in about five minutes.`
  - ❌ `Get started with the Warp Agent CLI.`
- **Reference** - Say what the reader can look up. Name the artifacts rather than the genre.
  - ✅ `Look up Warp Agent CLI flags, environment variables, slash commands, and keyboard shortcuts.`
  - ❌ `Reference documentation for the Warp Agent CLI.`
- **Troubleshooting** - Name the symptoms covered, not the act of troubleshooting.
  - ✅ `Fix sign-in failures, failed conversation resumes, and update problems in the Warp Agent CLI.`
  - ❌ `Troubleshooting information for common problems.`
- **FAQ** - Name the topic area the questions cover.
  - ✅ `Answers to common questions about cloud agent billing, credits, and plan limits.`
  - ❌ `Frequently asked questions.`
- **Feature documentation** - Say what the feature does and its primary benefit.
  - ✅ `Control what the agent can do with permission cards, auto-approve, and execution profiles.`
  - ❌ `Documentation for permissions and profiles.`
- **Guide** - Say what the reader will build or accomplish, using the non-branded phrasing they would search for.
  - ✅ `Set up Claude Code and run your first agentic coding session from the terminal.`
  - ❌ `A guide to using Claude Code with Warp.`

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
- **Cut first, split only if it's still long.** A page over ~1500 words is usually carrying framing, restated cause-and-effect, or boilerplate a parent page already owns — run the deletion-only "Cut again" pass (see Voice & tone → Cut again) before reaching for sub-pages or anchor links. Splitting a bloated page produces two bloated pages; only split once the content itself, not the padding, still doesn't fit on one page.
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

#### Screenshot placement guidelines
Use screenshots to clarify product surfaces, configuration points, or visual states that are hard to understand from prose alone. Don't add screenshots for every step in a straightforward procedure.

**Good screenshot placements:**
- **After the concept or behavior is introduced** — Place the screenshot immediately after the paragraph that explains the UI or state it shows.
- **Near configuration instructions** — Show settings panels, side panes, or menus where users make choices.
- **Near status or result explanations** — Show outputs, references, badges, progress indicators, or completion states that help users recognize success.
- **At the start of visual feature pages** — Use a broad orientation screenshot early when the page explains a new surface or layout.

**Avoid:**
- Repeating the same surface in multiple screenshots unless each image shows a meaningfully different state.
- Screenshots that duplicate obvious text instructions without adding visual context.
- Screenshots that include sensitive workspace data, private repo names, tokens, customer data, or personal information.
- Images with stale UI labels, hidden feature flags, or unfinished internal-only surfaces.

#### Screenshot sizing standards
Use consistent screenshot widths so docs pages feel visually balanced. Crop unnecessary empty space before resizing, then choose the closest standard size.

**Standard widths:**
- **Full content width: 736px** — Use for wide screenshots whose content cannot be cropped narrower without clipping, such as full-width terminal strips, wide status bars, and wide tables. `736px` equals the content column (`46rem`, set on `.main-pane .sl-container` in `src/styles/custom.css`), so it renders the same as omitting `maxWidth`. Set it explicitly anyway: it records that the width is deliberate rather than forgotten, and the style lint treats a missing width as an error. Reach for this tier only when a narrower size would make text illegible.
- **Large screenshots: 563px** — The default for full-window, full-pane, or broad product-surface screenshots where the surrounding layout matters. This was the usual width in legacy GitBook screenshots. Prefer this over `736px` unless the content genuinely needs the extra room.
- **Medium screenshots: ~375px** — Use for narrow UI surfaces such as popovers, command menus, side panes, dropdowns, and focused interaction flows. This is the preferred constrained size for most small Warp UI screenshots.
- **Small screenshots: ~300-350px** — Use for tightly cropped controls, chips, buttons, tooltips, and small menus. Use a smaller width only when the UI remains legible and the crop is intentionally compact.

**Rules:**
- **Avoid arbitrary widths** — Choose the nearest standard size instead of one-off values. If a screenshot needs a different size, the reason should be clear from the UI being shown.
- **Keep sequences consistent** — Screenshots in the same section or step sequence should use the same width unless they show meaningfully different UI surfaces.
- **Preserve legibility** — Text in the screenshot must remain readable at the chosen size on the docs page. This rule outranks the preference for a smaller tier: if text is unreadable at `563px`, move up to `736px` rather than shipping an illegible image.
- **Crop before widening** — Widening is the last resort. First crop out empty space and anything that is not the subject, and re-capture at a narrower terminal or window size if you can. Only step up a tier when the content itself sets the floor, as with a status bar that clips instead of reflowing.
- **Prefer the default figure size for large screenshots** — Only constrain width below `563px` when the screenshot is a narrow UI element that looks oversized at full content width.

#### Image caption guidelines
Captions orient the reader — they identify what the image shows so the reader knows where to look. They are not a place for instructions, marketing language, or exhaustive descriptions.

**Rules:**
- **Orient, don't instruct** — describe what is shown, not what to do. Procedural steps belong in the body text.
- **Write complete sentences** — every caption should read as a standalone sentence, not a fragment or label. A reader should understand what the image shows without looking at it.
- **Keep it short** — aim for 10 words or fewer. Never exceed ~20 words.
- **No marketing language** — avoid "easily," "quickly," "powerful," "at a glance," or similar.
- **Don't repeat the prose** — if the paragraph above already describes the image, the caption should add context, not echo it.
- **Don't list everything visible** — name the subject, not every detail in the screenshot.
- **Sentence case, end with a period** — consistent with all other text in the docs.

**Examples:**
- ✅ `<figcaption>The Environments page in the Oz web app.</figcaption>`
- ✅ `<figcaption>Agent Profile settings.</figcaption>`
- ✅ `<figcaption>Codebase indexing settings.</figcaption>`
- ❌ `<figcaption>Codebase indexing settings in Warp. Easily track sync status and manage which folders are indexed for AI-powered context and suggestions.</figcaption>` (marketing language, too long)
- ❌ `<figcaption>Click the toast to jump to the agent's session.</figcaption>` (procedural — belongs in body text)
- ❌ `<figcaption>Universal Input's contextual input chips, from left to right: conversation management, node version, active directory, Git and code diffs, and 2 attached images.</figcaption>` (exhaustive list)

### Links, embeds, and cross-references
- Use descriptive link text that explains what users will find. The anchor text should describe the destination or task, not the action of clicking.
  - ✅ "Learn more about [Codebase Context](...)" / "See [configuring environments](...)"
  - ❌ "Click [here](...)" / "See [this page](...)" / "Read [more](...)"
- Don't use raw URLs as link text. Name the destination so readers, search engines, and agents understand what the link points to.
  - ✅ "See the [Warp pricing page](https://www.warp.dev/pricing)"
  - ❌ "See [https://www.warp.dev/pricing](https://www.warp.dev/pricing)"
- Add context before a link when the anchor text alone doesn't explain why the reader should open it. The sentence should make the relationship between the current page and destination clear.
  - ✅ "To inspect completed runs, go to the [Runs page in the Oz web app](https://oz.warp.dev/runs)."
  - ❌ "Go to [Runs page](https://oz.warp.dev/runs)."
- Avoid redundant bold prefixes when the link text already contains the same context. Start with the link when the link is the complete item.
  - ✅ "* [Claude web search tool documentation](...)"
  - ❌ "* **Claude Web Search**: [Claude web search tool documentation](...)"
- Use articles before named destination pages when the sentence requires one.
  - ✅ "Go to the [Runs page in the Oz web app](...)."
  - ❌ "Go to [Runs page in the Oz web app](...)."
- Cross-reference related features prominently. Add internal links where they help the reader continue a workflow or understand a related concept, not as generic link lists added only for SEO.
- Link to external resources when they add value.
- Within an Astro Starlight space, use relative paths. For cross-space links, use absolute URLs (`https://docs.warp.dev/...`).
- Descriptive anchor text helps search engines understand page relationships. "Click here" provides no signal; "configuring environments" tells search engines what the linked page is about.
- Every `VideoEmbed` must include a specific `title` prop that describes the integration, workflow, feature, or task shown.
  - ✅ `<VideoEmbed url="..." title="Warp x GitHub Actions integration video" />`
  - ✅ `<VideoEmbed url="..." title="Codebase Context indexing settings demo" />`
  - ❌ `<VideoEmbed url="..." />`
  - ❌ `<VideoEmbed url="..." title="GitHub Actions video" />`
  - ❌ `<VideoEmbed url="..." title="Codebase Context video 1" />`

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

Use callouts sparingly:
- Never place two callouts back to back, and keep to at most one per section.
- Keep callouts to a sentence or two. Information that needs a list or several sentences belongs in the body under a header.
- A caveat that applies to one step belongs in that step's prose, not in a callout.

Callouts interrupt the reader. Each one spends attention the page can't get back.

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
- Use bold for interactive UI elements (e.g., buttons, toggles, dropdowns, and the option you select from one)
- Describe UI elements by name, not just appearance or location. Prefer "In the sidebar, click **Platform**" over "Click the button on the left."
- Format checkbox names in bold. Omit the word "checkbox." Use "select" or "deselect," not "check" or "uncheck."
- Use quotation marks, not bold, for a field or label name that is not itself clickable. The interactive control next to it (the dropdown, the input, the option you choose from it) still gets bold.

**Use:**
- ✅ Click your profile photo in the top-right corner, then click **Settings**.
- ✅ In the sidebar, click **Platform**.
- ✅ In the "Harness" dropdown, select **Claude Code** or **Codex**. ("Harness" labels the field but isn't itself clickable; the dropdown and its options are)

**Don't use:**
- ❌ In the API Keys section, click `+ Create API Key`.
- ❌ In the API Keys section, click `+ Create API Key`. (use bold, not backticks)
- ❌ Click `Create key`. (use bold, not backticks)
- ❌ Choose **Claude Code** or **Codex** in the **Harness** field. (the field label isn't interactive, so it shouldn't be bold)

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

The type is not a formatting choice — it follows from what the reader is trying to do. Decide that first in the content design plan (`.agents/references/content-design-plan.md`), then pick the type that serves it. Picking a template first produces pages shaped by the template.

### Titles by content type

Each type has its own title convention. Sentence case applies to all of them; this is the additional per-type rule.

- **Conceptual** — "About [subject]", or a plain noun phrase naming the subject. ✅ `About environments` ✅ `Deployment patterns` ❌ `Understanding how environments work`
- **Procedural** — begin with a gerund, naming the task. ✅ `Configuring a self-hosted GitLab integration` ❌ `Self-hosted GitLab integration setup`
- **Reference** — a noun phrase naming what can be looked up. Avoid stacked nouns; use prepositions to break them up. ✅ `Keyboard shortcuts for the code editor` ❌ `Code editor keyboard shortcut reference`
- **Troubleshooting** — the symptom or the exact error message, so search matches what the reader typed.
- **Quickstart** — name the feature. ✅ `Quickstart for cloud agents` ❌ a bare `Quickstart`
- **Tutorial** — follow the procedural convention. Do not put "tutorial" or "guide" in the title.
- **Feature documentation (combined)** — if the page contains a procedure, use a task-based gerund title. Keep it general enough to cover the range of tasks on the page, and agnostic about which option the reader picks. ✅ `Setting repository visibility` ❌ `Making a private repository public`

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
- **Include practical examples**: Show real-world scenarios, not just toy examples. Concrete examples help the reader understand when and why to use a feature. For enterprise or infrastructure-heavy features, prefer a complete example (a full config file, a linked sample repository) over a fragment — abstract features are hardest to trust without something concrete to point at.
- **Cross-reference related pages**: Link to related features, next steps, and deeper references so the reader can continue learning.
- **Sequence basics before jargon**: Explain what something is in plain language before introducing internal-sounding framing, deep lifecycle terminology, or advanced configuration. A reader who doesn't know the concept yet should never hit unexplained jargon in the first few paragraphs. Save advanced or self-referential concepts (e.g., a system that improves itself) for after the reader understands the basic flow.
- **Avoid appendix-style content**: Don't add a bullet list or table whose only job is to restate content already covered elsewhere on the page, such as an exhaustive index of tabs or settings that duplicates the dedicated sections below it. Weave supplementary details into the section they relate to instead of bolting them onto the end under a generic heading like "Good to know."
- **Don't over-specify counts or internals that will drift**: Describe a capability rather than naming an exact count of tools, steps, or subcomponents behind it (e.g., "a small set of tools" instead of "ten tools"). Precise counts go stale the moment the implementation changes, and a stale number is worse than no number.
- **Feature real differentiators structurally**: If a capability is a genuine advantage over the default path (an agent- or API-driven alternative to a UI flow, for example), give it real visual weight — a clear callout near the top of the relevant section, not a footnote after the primary steps are already done. Where something sits on the page communicates how important it is.
- **Verify claims against the live product, not just prior drafts**: Terminology, UI labels, and calculated values drift between rounds of review. Confirm names, labels, and metric definitions against the actual app, API, or codebase before publishing — especially for pages describing metrics or anything computed.

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

**Existing examples**: `platform/deployment-patterns.mdx`, `platform/index.mdx`

**Template**: `.agents/templates/conceptual.md`

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
  - **Move reference detail out of the step into a `:::note`.** When a step's supporting detail is a list of facts a reader might check rather than an instruction (accepted credential types, valid formats), keep the step to its one action and put the list in a `:::note` immediately after it.
    - ✅ A step reading "In the **Auth** field, choose a compatible, team-owned secret from the list or click **New auth secret** to create one," followed by a `:::note` listing which credential type each option accepts.
    - ❌ Folding the full list of accepted credential types into the same sentence as the instruction, so the action is buried in reference detail.
- **Motivate steps before giving instructions.** Briefly explain WHY before HOW, especially for setup steps. A single sentence of motivation prevents the reader from wondering "why am I doing this?"
  - ✅ "Export your API key so the CLI can authenticate your requests automatically."
  - ❌ "Export your API key as an environment variable." (why?)
- **Orient within the step, not just on first mention.** The page-level rule above ("Orient the reader before UI, CLI, or URL instructions") also applies inside a single step: name the field, dropdown, or location the action happens in before naming the action itself. Don't rely on referring the reader back to an earlier section instead — a step should stand on its own for a reader who lands on it directly.
  - ✅ "In the 'Harness' dropdown, select **Claude Code** or **Codex**."
  - ❌ "Choose **Claude Code** or **Codex** in the **Harness** field." (names the action before the location)
- Include expected outcomes after key steps so the reader can confirm they're on track.
- Test all instructions for accuracy.
- Provide troubleshooting for common failure points.
- **Explain the default before the override.** When documenting configurable infrastructure or advanced settings, state the default behavior and the common case first, then cover manual overrides. Don't lead with the full matrix of options before establishing what "just works" out of the box.

**Existing examples**: `reference/cli/api-keys.mdx`, `platform/integrations/slack.mdx`

**Template**: `.agents/templates/procedural.md`

### Quickstart

**What it is**: A specialized procedural doc that gets the reader to a working result fast, with only the essential steps. Style "quickstart" as one word, lowercase (unless starting a sentence or in a title).

**When to use**: When the reader already understands the feature or product and is ready to try it. A quickstart deliberately omits explanation of how something works or why they would want it — if the reader needs that, they need conceptual content, and if the task is complex enough to need context along the way, they need a tutorial.

**Scope**: About five minutes and roughly 600 words. That budget is the defining constraint, not a suggestion. A quickstart that no longer fits it has become a tutorial and should be reworked as one.

**Structure**:
1. Opening paragraph: who it is for, the prerequisites and prior knowledge assumed, what the reader will end up with, and the time budget ("in about five minutes")
2. Prerequisites (minimal — link to full setup docs rather than inlining lengthy setup)
3. Numbered steps (as few as possible to reach a working result)
4. Troubleshooting (optional — link to existing troubleshooting content rather than writing new)
5. Next steps: a one-line recap, then 2-3 actionable next steps, always including a link to the conceptual page for the feature

**Rules**:
- **Give every quickstart a descriptive H1 title.** Don't use a bare "Quickstart" — include the feature or topic name.
  - ✅ `# Quickstart for cloud agents`
  - ❌ `# Quickstart` (quickstart for what?)
- Minimize prerequisites — the reader should be able to start quickly.
- Keep steps focused on the critical path — defer edge cases and advanced options to other pages.
- Link out rather than replicating content, so the flow is not interrupted.
- Use code blocks and screenshots generously; visual confirmation reassures the reader they are on track.
- Steps can be less explicit than in full procedural content, because the audience already knows the product.
- All procedural rules apply (focused steps, motivate steps, expected outcomes).

**Existing examples**: `platform/quickstart.mdx`, `getting-started/quickstart/installation-and-setup.mdx`

**Template**: `.agents/templates/quickstart.md`

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

**Template**: `.agents/templates/reference.md`

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

**Template**: `.agents/templates/troubleshooting.md`

### FAQ

**What it is**: Question-and-answer format for common questions.

**When to use**: Rarely. **Default to "not an FAQ."**

An FAQ page pulls answers away from the page that owns the topic. The reader who lands on the owning page does not find the answer, the reader who lands on the FAQ gets an answer without its context, and the two drift apart as the product changes. Most content that arrives as "we should FAQ this" belongs on an existing conceptual, reference, or troubleshooting page.

**Admission rules — all three must hold before creating or extending an FAQ page:**

1. **The questions are genuinely cross-cutting.** They span several features or pages, so no single page owns them. Questions about one feature belong on that feature's page.
2. **There is no canonical home.** If any existing page could answer the question in context, answer it there instead. "It would be buried on that page" is a signal the page needs restructuring, not that the answer needs a second home.
3. **The question is one a reader actually asks**, in their own words, sourced from support tickets, Slack, or community threads — not one invented to organize existing content.

Before adding a question to an existing FAQ page, apply the same test. FAQ pages grow by accretion; each addition should have to justify itself.

**Where it goes instead:**

- "What is X / how does X work?" → conceptual page for X
- "What are the limits / which plans include X?" → reference section on the owning page
- "Why did I get error Y?" → troubleshooting section, keyed on the error
- "How do I do Z?" → procedural section on the owning page

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
- Never let an FAQ answer become the only place a fact lives. It should summarize and link, not own.

**Template**: `.agents/templates/faq.md`

**Existing examples**: `agent-platform/getting-started/faqs.mdx`, `support-and-community/plans-and-billing/pricing-faqs.mdx`

### Tutorial (Guides section)

**What it is**: A practical, task-oriented walkthrough of an entire workflow, start to finish. Tutorials live in the `src/content/docs/guides/` directory (the "Guides" Astro Starlight space) and can include video, written steps, or both.

"Guides" is the name of the section, not a content type. It holds both **tutorials** and **quickstarts**; pick between them by scope before drafting:

- **Quickstart** — about five minutes, ~600 words, essential steps only, for someone who already understands the product.
- **Tutorial** — a full workflow with context at the decision points, for someone extending a basic understanding to solve a real problem.

**A tutorial requires that a quickstart already exists** for the product area. If there is no quickstart, write that first — otherwise the tutorial absorbs setup content that belongs in a shorter page, and readers who only wanted to get started have to wade through the whole workflow.

**When to use**: For educational content that teaches a workflow or use case — not feature documentation (which belongs in the main docs). Tutorials focus on the "how" with real prompts and reproducible results, and are more conversational than other content: a developer-to-developer conversation that stays accessible to varied technical backgrounds.

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
- Titles should be task-oriented and scannable. Use shortened titles in the Astro Starlight nav and full descriptive titles in the article H1. Do not put "tutorial" or "guide" in the title.
- For SEO: capture the non-branded query when possible. Write the title a developer would actually search for ("How to Set Up Claude Code" not "How to Set Up Claude Code in Warp").
- All procedural rules apply (focused steps, motivate steps, expected outcomes).
- **Give real examples, not placeholders.** Do not write "enter a commit message" — supply an appropriate one that matches the preceding steps.
- **Include troubleshooting.** Acknowledge what commonly goes wrong in this workflow and how to recover. This is what most distinguishes a tutorial from a quickstart, which only links to existing troubleshooting.
- **End with a conclusion, then next steps.** Review what the reader built, referring back to the example from the introduction, then give 2-3 actionable next steps.
- Do not state an expected completion time — it varies too much by experience level. (Quickstarts do state one.)
- Link to relevant feature documentation in the main docs where concepts need deeper explanation.
- When a tutorial has a companion video, the written content should stand alone — a reader should be able to follow it without watching the video.

**Template**: A copyable starting template is available at `.agents/templates/guide-page.md`. The filename is a holdover from when this type was called "guide"; the `draft_guide` skill uses it too.

**Existing examples**: `guides/external-tools/sentry-mcp-fix-sentry-error-in-empower-website.mdx`, `guides/build-an-app-in-warp/building-a-real-time-chat-app-github-mcp-railway.mdx`


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
- **Never fold quickstart or tutorial content into a combined page.** Conceptual, procedural, reference, and troubleshooting sections can coexist here; quickstarts and tutorials cannot. Both are defined by a scope budget and a single continuous path, and both lose their purpose once embedded in a longer page. Link to them instead.
- **Order sections from broad to specific**: conceptual, then reference, then procedures in lifecycle order (enable, use, manage, disable, destructive actions), then troubleshooting.
- Use a task-based gerund title that stays agnostic about which option the reader chooses — `Setting repository visibility`, not `Making a private repository public`.

This is the type most prone to sprawl, precisely because it accepts the most kinds of content. If the page is growing past roughly 1500 words, split the procedures onto their own pages rather than adding another section.

**Existing examples**: `agent-platform/capabilities/skills.mdx`, `platform/environments.mdx`

**Template**: `.agents/templates/feature-doc.md`

## Page templates

Concrete page scaffolds for each content type are in `.agents/templates/`. Use these as starting points when creating new pages — but pick the type from the content design plan first, not by browsing this list:

- **Conceptual** — `.agents/templates/conceptual.md`
- **Procedural** — `.agents/templates/procedural.md`
- **Quickstart** — `.agents/templates/quickstart.md`
- **Reference** — `.agents/templates/reference.md`
- **Troubleshooting** — `.agents/templates/troubleshooting.md`
- **FAQ** — `.agents/templates/faq.md` (read the FAQ admission rules before using this one)
- **Tutorial** — `.agents/templates/guide-page.md` (filename is a holdover from when the type was called "guide")
- **Feature documentation (combined)** — `.agents/templates/feature-doc.md`

One template is not a page scaffold: `.agents/templates/content-design-plan.md` is the fill-in artifact completed *before* drafting, presented to the requester in an interactive session and included in the PR body in every case. See `.agents/references/content-design-plan.md`.

Every template carries its guidance as **bracketed instructions** in the body, not HTML comments — agents deprioritize comments, so the guidance would be skipped. Each one opens with a removal note; delete every bracketed instruction, including that one, before shipping.

Each **page** template also sets `title` in frontmatter and adds no H1 to the body. Starlight renders the frontmatter title as the page H1, so a body H1 produces a duplicate. This does not apply to the content design plan template, which is a PR body section rather than a page.

### Closing section

Every page ends with one of two sections, chosen by content type:

- **`## Next steps`** — quickstarts and tutorials. The reader just finished something and needs forward momentum: a one-line recap, then 2-3 actionable next steps, always including the conceptual page for the feature.
- **`## Related pages`** — every other type. The reader wants lateral material, not a sequel.

Do not use "Further reading" or "See also"; neither appears anywhere in the corpus. Whichever section applies, it goes last and contains at least one internal link whose anchor text names the destination.

## Terminology standards

Use these terms consistently throughout all documentation. For the full canonical glossary with usage notes, see `.agents/references/terminology.md`.

### Core features

Product feature names retain their standard capitalization. Match the exact casing shown in the UI.

- **Warp** (not "Warp Terminal" unless specifically distinguishing)
- **agent** / **agents** (lowercase) - the generic concept, covering any agent on any surface. See [Capitalizing "agent"](#capitalizing-agent) for the full rule.
- **Agent Mode** (not "agent mode" or "Agent-mode")
- **Terminal and Agent modes** - The two distinct modes in Warp: terminal mode (for shell commands) and Agent Mode (for multi-turn agent conversations). Use "Terminal and Agent modes" on first reference; use "terminal mode" or "Agent Mode" individually in subsequent references. Do not use "agent modality" or "Agent Modality" — this was an internal name that is not user-facing.
- **Cloud Agents** (capitalized as a product section/feature name; lowercase "cloud agents" in most contexts)
- **Warp Drive** - Shared workspace for saving and organizing commands, workflows, and environment variables across your team.
- **Codebase Context** - Warp indexes your Git-tracked codebase to help Agents understand your code.
- **Admin Panel** - Team management surface for controlling members, roles, and billing.
- **Agent Management Panel** - Interface for viewing and managing running agents (not "agent dashboard" or "agent manager").
- **Agent Memory** - Persistent, cross-harness memory layer for cloud agents that captures durable facts, decisions, and outcomes across conversations (currently in research preview). Capitalize as a feature name; use lowercase "memory store" for individual stores.
- **Handoff** - Feature for moving agent work between a local Warp session and the cloud, or continuing a finished cloud run; supports local-to-cloud, cloud-to-cloud, and cloud-to-local. Capitalize as a feature name; lowercase "hand off" only as a verb.

### Capitalizing "agent"

This is the single most drifted term in the docs, so the rule is narrow on purpose.

- **Warp Agent** - Capitalized, singular, treated as a proper noun. Use it for Warp's built-in agent harness, especially when contrasting with third-party agents (Claude Code, Codex, and so on) or when referencing the Settings label (**Settings** > **Agents** > **Warp Agent**).
- **In prose, it takes the definite article: "the Warp Agent".** The bare form is for headings, sidebar labels, page titles, and the Settings path. "Runs the Warp Agent" reads correctly; "runs Warp Agent" reads as a different product.
- **agent** / **agents** - Lowercase everywhere else. This is the generic concept and covers any agent on any surface, including cloud agents and third-party CLI agents.
- **Proper nouns keep their capital A.** `Agent Mode`, `Agent Profiles`, `Agent Memory`, `Agent Management Panel`, `Agent API`, and `Warp Agent CLI` are feature names, not instances of the generic term.

❌ **Avoid "Warp's agent" and "Warp's agents".** This is the ambiguous middle ground and the main source of drift. It reads as neither the proper noun nor the generic term, so it blurs exactly the distinction that matters. Rewrite instead:

- Referring to the built-in harness → "the Warp Agent"
- Referring to agents generally → "agents" or "agents in Warp"
- Referring to the server-side runtime → "the Warp Agent harness"

✅ "The Warp Agent can run commands and edit files." (the built-in harness)
✅ "Profiles control how agents behave." (generic)
❌ "Profiles control how Warp's agents behave." (ambiguous)
❌ "Warp's agent can run commands." (ambiguous)

### Automation Platform terminology

Renamed from "Oz" on 2026-08-18. The `oz` CLI binary and the Oz v1 web app at `oz.warp.dev` keep the Oz name until 2026-09-15 and are not stale in the meantime. See `.agents/references/terminology.md` → "What still says Oz" for the full holdout list.

#### The article rule
"Oz" was a proper noun and read correctly bare. "Automation Platform" is a common-noun phrase, so it needs a definite article in referential positions. This is the most common mistake when writing about the platform.

- **Referential** (subject, object, possessor) takes "the": "with the Automation Platform", "The Automation Platform provides", "the Automation Platform's backend".
- **Attributive** (modifying a following noun) stays bare: "Automation Platform settings", "Automation Platform-hosted", "Automation Platform overview".

Write the name as `{VARS.WARP_AUTOMATION_PLATFORM}` in body prose or `{{WARP_AUTOMATION_PLATFORM}}` in frontmatter, never as a literal string, and keep the article outside the token. `style_lint` enforces both halves: `hardcoded-var` catches the literal, `platform-determiner` catches the missing article.

#### Warp Agent vs the Automation Platform
- **Warp Agent** — Warp's built-in agent harness. Use "Warp Agent" when specifically referring to the built-in harness, especially when contrasting with third-party agents (Claude Code, Codex, etc.), or when referencing the Settings label (**Settings** > **Agents** > **Warp Agent**).
- **The Automation Platform is the platform, not the agent.** Never introduce it as "Warp's agent" or equate the two. The Automation Platform runs and coordinates agents; the Warp Agent is the agent.
- **Automation Platform** — Warp's programmable platform for running and coordinating agents at scale
- There is typically one Warp environment per user session. The Automation Platform can run many agents concurrently, across machines, repos, and teams.

#### Core terms
- **agent** - A combination of agent instructions (skill or prompt), trigger (cron, webhook, manual), environment (local, cloud), profile, and host. Agents can be local or cloud. Use lowercase "agent" in most contexts; use "Warp Agent" only when referring specifically to the built-in Warp harness.
- **cloud agent** - An agent running in the cloud, from a trigger, schedule, or started from someone's local machine
- **subagent** - A child agent created by a parent agent to parallelize or delegate work
- **conversation** - An interactive execution lifecycle within the Warp Terminal, regardless of whether it's local or in the cloud
- **Automation Platform** - Warp's programmable platform for running and coordinating agents at scale
- **cloud agent run** - A single execution lifecycle of an agent, including actions, outputs, and logs. Always cloud-based. Use `{VARS.PLATFORM_RUN}`. On factory-specific pages, write "factory run" directly.
- **Environment** - The execution context for an agent, including repo access, dependencies, secrets, compute, and runtime configuration
- **cloud agent dashboard** - The app surface to manage all runs, unified across the Warp app and web. Use `{VARS.DASHBOARD}`. On factory-specific pages, write "factory dashboard" directly.
- **Oz web app** - The web app for configuring agents and managing runs. Holds the Oz name until 2026-09-15; use `{VARS.WEB_APP}`.

#### Oz CLI commands
- `oz agent run` - Run a local agent
- `oz agent run-cloud` - Run an adhoc cloud agent
- `oz integration create` - Install integrations (Slack, Linear)
- `oz environment create/list/get/update/delete` - CRUD on environments
- `oz schedule create/list/get/update/delete` - CRUD on scheduled cloud agents
- `oz secret create/list/update/delete` - CRUD on Warp-managed secrets
- `oz run list/get` - Get info on cloud agent runs

#### Preferred phrases
The platform is not something you address — it runs and coordinates agents, and the agent is what you ask. The older "Ask Oz to..." phrasings worked only because "Oz" was doing double duty as both platform and assistant, which the rename ended.

- ✅ "Ask the agent to..."
- ✅ "Run an agent on the Automation Platform"
- ✅ "The Automation Platform can run this on a schedule"
- ❌ "Ask the Automation Platform to..." — you ask an agent, not a platform

#### Terms to avoid
- ❌ "Oz agent" / "Oz agents" → Use "agent" / "agents" (or "Warp Agent" / "Warp Agents" when referring to the built-in harness)
- ❌ "Oz cloud agent" → Use "cloud agent"
- ❌ "Oz subagent" → Use "subagent"
- ❌ "Oz conversation" → Use "conversation"
- ❌ "Ozzies" → Use "agents", "instances", or "subagents"
- ❌ "Deploying an Oz" → Use "Deploying an agent"
- ❌ "The Oz Agent" → Use "the agent" or "the Warp Agent"
- ❌ "Oz is running" → Use "An agent is running" or "A run is in progress"
- ❌ "AI agents" → Use "agents" (the "AI" prefix is redundant)
- ❌ "Ambient Agents" / "ambient agents" → Use "Cloud Agents" / "cloud agents" ("ambient" is no longer a product term)
- ❌ "Agent Modality" or "agent modality" → Use "Terminal and Agent modes" (this was an internal name, not user-facing)
- ❌ "agent identity" / "agent identities" → Use "agent," "agents," or "cloud agent(s)" in user-facing copy. Use legacy API names such as `agent_identity_uid` or `/agent/identities` only when documenting the exact field, path, or compatibility behavior.
- ❌ A bare "Automation Platform" in a referential position → Add "the". See [The article rule](#the-article-rule).
- ❌ The literal string "Automation Platform" in prose → Use `{VARS.WARP_AUTOMATION_PLATFORM}` / `{{WARP_AUTOMATION_PLATFORM}}`.

### Warp Factories terminology

This works like GitHub Actions. **Warp Factories** is the product and is always written in full. An individual **factory** is a common noun and is always lowercase. A bare capitalized **Factory** is never a proper noun.

- ✅ "Warp Factories is in Early Access" (the product)
- ✅ "your factory", "each factory's agents", "factory dashboard", "factory run", "factory agents"
- ❌ "the Factory", "your Factory", "Factory runs", "Factory metrics"
- ❌ "Factories" on its own to mean the product → write "Warp Factories"

Sentence-initial capitals are positional, not proper nouns — a heading or sidebar label may begin "Factory agents" for the same reason it would begin "Cloud agents." The rule governs mid-sentence prose. `style_lint` enforces it with the `factory-proper-noun` check.

**Exceptions, quoted as they ship:** **Factory MCP** is the feature's own name (the server registers as `warp-factory`). Verbatim UI strings — **Factory name**, **Foreman name**, **Factory integrations**, **Add your Factory to your team**, "Factory running!", and the **Factory definition** sidebar label — are quoted as the app renders them.

See `.agents/references/terminology.md` → "Warp Factories terminology" for the full glossary.

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
- **compute credits** (lowercase common noun; capitalize the first letter only at the start of a sentence or bullet) - the compute bucket; consumed when an agent run uses Warp-hosted compute. Used alongside AI credits and platform credits when describing credit types.
- **cloud agent credits** (lowercase common noun; capitalize the first letter only at the start of a sentence or bullet) - credits consumed by cloud agents (in contrast with local agent credits). Refers to the same compute bucket as compute credits; pick the term that fits the framing.
- **platform credits** (lowercase common noun; capitalize the first letter only at the start of a sentence or bullet) - the platform-infrastructure bucket
- **Warp credits** - credits included with a subscription plan. Use in user-facing copy rather than "plan credits."
- Use "credit" or "credits" without the "AI" prefix throughout documentation

### UI elements
- **Settings** (capitalized when referring to the Settings panel)
- **Command Palette** (capitalized)

## Content variables
Product names and key strings are defined in `src/data/vars.ts` as the `VARS` object. Updating a value there propagates it to every page that uses the variable — both frontmatter and body prose — on the next build. This makes future renames a one-line change.
### Option A — body prose (MDX imports)
After the closing `---` of the frontmatter block (not inside it), add the import as the first line of the file body. Then use `{VARS.KEY}` inline in prose. TypeScript catches typos at compile time.
```mdx
---
title: "{{WARP_AGENT_CLI}} reference"
description: "Use the {{WARP_AGENT_CLI}} to run and manage agents."
---
import { VARS } from '@data/vars';

Use the {VARS.WARP_AGENT_CLI} to run agents from the command line.
```
Note: this example also shows Option B in the frontmatter (`{{WARP_AGENT_CLI}}`). Both can appear in the same file — Option B covers the frontmatter YAML, Option A covers the body prose.
### Option B — frontmatter (Vite transform)
Use `{{TOKEN}}` placeholders directly in frontmatter YAML values (`title`, `description`, `sidebar.label`, etc.). The `warp-vars-transform` Vite plugin substitutes them before any parser runs.
```yaml
---
title: Getting started with {{WARP_AGENT_CLI}}
description: Learn how to use the {{WARP_AGENT_CLI}} to run and manage agents.
---
```
The build fails with a clear error if a token is unrecognized — for example, `{{WARP_AGNT_CLI}}` in frontmatter would surface as an unresolved token error. Validation applies to frontmatter only; body prose may legitimately contain `{{...}}` patterns as code examples.
### When to use vars
Use a variable for:
- Product and platform names that have changed before or are likely to change (e.g., `WARP_AGENT_CLI`, `WEB_APP`, `DASHBOARD`)
- Feature names used in many pages (e.g., `AGENT_MODE`, `WARP_DRIVE`)
- URLs that may change with a rebrand (e.g., `WEB_APP_URL`, `CONTACT_SALES_URL`)
Do **not** create variables for generic stable terms like "terminal," "command," or "repository."
### Adding a new variable
Add the key-value pair to `src/data/vars.ts` only. Both Option A (TypeScript import) and Option B (Vite transform) pick it up automatically.
### Important constraints
- **Do NOT** use `{{TOKEN}}` syntax in MDX body prose — it's only for frontmatter YAML. The Vite plugin runs before MDX parsing; curly-brace expressions in body prose are MDX syntax, not plugin tokens.
- **Do NOT** use `{VARS.x}` expressions in frontmatter — MDX expressions don't evaluate in YAML frontmatter.
- **Key naming rule**: Keys are stable identifiers. Use the future or conceptual name as the key (e.g., `WARP_AGENT_CLI`), not the current brand name that may be retired. The value holds the current string.
## SEO and AEO (AI Engine Optimization)

All documentation should be written with search discoverability in mind — both for traditional search engines (Google) and AI engines (ChatGPT, Gemini, Perplexity, Copilot).

### Frontmatter descriptions
- Every page must have a `description` in frontmatter. Write it as a standalone summary (one sentence, 50-160 characters) that includes the primary keyword naturally.
- Descriptions appear in search results and AI citations. Write for humans, but include the key terms a developer would search for.
- For the full rules and per-content-type patterns with examples, see [Frontmatter](#frontmatter) under Content structure. That section is the source of truth.

### Title framing
- For guides and educational content: capture the **non-branded query** when possible. Write the title a developer would actually search for.
  - ✅ "How to Set Up Claude Code"
  - ❌ "How to Set Up Claude Code in Warp"
- For feature documentation: use the feature name as the developer knows it.

### SEO data
When creating or updating content, use SEO and AEO data to inform titles, descriptions, and content coverage. The `docs-seo-audit` skill (`.agents/skills/docs-seo-audit/`) can identify technical SEO issues.

## Quality checklist

Before publishing any documentation, verify:

- [ ] The change passed `.agents/references/docs-worthiness-criteria.md` — the full gate with recorded evidence for automated runs, Gate 0 (shipped and public) for human-requested pages
- [ ] A content design plan exists per `.agents/references/content-design-plan.md` and appears in the PR body
- [ ] An existing page was updated rather than a new page created, unless a new page is genuinely justified
- [ ] Frontmatter includes a one-sentence description (50-160 chars) written as a standalone summary, with no filler opener
- [ ] Content type is identified and the page follows the structure for that type (see `.agents/templates/`)
- [ ] The title follows the convention for its content type (see "Titles by content type")
- [ ] No quickstart or tutorial content is folded into a combined feature page
- [ ] Headers use sentence case (with proper feature name capitalization)
- [ ] Lists use bold term + dash + explanation format
- [ ] All links work and point to correct destinations
- [ ] Link text is descriptive, not generic text like "here," "this page," or "learn more"
- [ ] Link sentences provide enough context for readers, search engines, and agents to understand the destination
- [ ] `VideoEmbed` components include specific `title` props that describe the video content
- [ ] Code examples are tested and accurate
- [ ] Terminology and product names match the glossary (`.agents/references/terminology.md`)
- [ ] Cross-references to related features are included
- [ ] Instructions include expected outcomes after key steps
- [ ] First references to prerequisites, tools, or surfaces include inline context
- [ ] Content is scannable with clear headers and lists
- [ ] Prose passes the tone rules: no marketing buzzwords, no meta-openers ("This page covers..."), no restated cause-and-effect or recap lines, and it reads naturally aloud (see Voice & tone)
- [ ] Callouts are sparse (usually 0-2 per page), never consecutive, and not a substitute for body prose
- [ ] A deletion-only "Cut again" pass removed framing lines, self-commentary, and boilerplate a parent page already covers (see Voice & tone → Cut again) before splitting a long page into sub-pages
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
- **guides/** — Quickstarts and tutorials (the "Guides" space)

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
