---
name: draft_docs
description: Draft new Warp documentation pages or update existing ones using established style conventions, with optional source code context from warp-internal and warp-server.
---

# Draft Docs

This skill helps you draft new documentation pages or update existing ones for Warp's GitBook documentation. It follows Warp's voice, tone, formatting conventions, and can optionally pull context from Warp's source repositories.

## How to use

Invoke this skill with any context that describes what you want to document:
- PRDs or feature specs
- Slack threads or meeting notes
- Existing documentation that needs updating
- A description of a feature or concept

Example: "Use the draft_docs skill to write docs for [feature name] based on this PRD: [context]"

## Workflow

When this skill is invoked, follow these steps:

### 1. Gather context
Review all provided context (PRD, spec, existing doc, etc.). Identify:
- What feature or topic is being documented
- Key user benefits and capabilities
- Technical details that need explaining

### 2. Clarify placement
Ask the user where the doc should live. The docs are organized into sections, each with its own `SUMMARY.md`:
- `docs/warp/` - Warp Terminal and IDE (Getting started, Terminal, Code, Knowledge and collaboration)
- `docs/agent-platform/` - Agent Platform (Agent, Ambient Agents, Integrations, Platform)
- `docs/reference/` - Technical reference (CLI, API & SDK)
- `docs/support-and-community/` - Support (Troubleshooting, Plans and billing, Privacy and security, Community)
- `docs/enterprise/` - Enterprise documentation
- `docs/changelog/` - Changelog

Also clarify: Is this a new page or an update to an existing page?

### 3. Research existing patterns
Before drafting, read:
1. `WARP.md` in the gitbook repo root for the complete style guide
2. 1-2 similar pages in the target section to match existing patterns

### 4. Research source code (if needed)
For technical accuracy, optionally look in Warp's source repositories:
- **warp-internal** - Client-side code (Rust, Swift, etc.)
- **warp-server** - Server-side code (Go)

To find these repos:
1. Search for directories named `warp-internal` and `warp-server` on the user's machine
2. If not found, ask the user where the repos are located

Use source code to:
- Verify technical behavior and edge cases
- Understand feature implementation details
- Find accurate terminology and configuration options

### 5. Draft the doc
Create the documentation following Warp conventions (see Style Reference below).

### 6. Review checklist
Before presenting the draft, verify:
- [ ] Frontmatter includes clear description
- [ ] Content follows established structure
- [ ] Terminology matches style guide (Agent, Agent Mode, Warp Drive, etc.)
- [ ] Headers use sentence case
- [ ] Lists use bold term + dash + explanation format
- [ ] Cross-references to related features are included
- [ ] Instructions include expected outcomes

### 7. Update navigation
If this is a new page, remind the user to add it to the relevant section's `SUMMARY.md`.

## Style reference

### Voice & tone
- **Professional yet approachable** - Write with authority but remain accessible
- **Direct and action-oriented** - Lead with what users can accomplish
- **User-focused** - Use second person ("you can", "allows you to")
- **Confident** - Avoid hedging language ("might", "could", "perhaps")

### Page structure
Every page should follow this hierarchy:
1. YAML frontmatter with description
2. H1 title (sentence case)
3. Opening paragraph with primary benefit
4. Key features section (if applicable)
5. How it works section
6. Detailed sections
7. Cross-references to related features

### Frontmatter format
```yaml
---
description: >-
  A concise 1-2 sentence summary that explains what the page covers and 
  what value it provides to the reader.
---
```

### List formatting
Use bulleted lists with bold key terms:
```markdown
* **Feature name** - Description of what it does and its benefit
* **Another feature** - Another description with user value
```

### Callouts
Use GitBook hint syntax:
```markdown
{% hint style="info" %}
For informational context, tips, or additional details
{% endhint %}

{% hint style="warning" %}
For important caveats, limitations, or things to watch out for
{% endhint %}
```

### Terminology
Always use these exact terms:
- **Warp** (not "Warp Terminal" unless distinguishing)
- **Agent** or **Agents** (capitalized for Warp's AI agents)
- **Agent Mode** (not "agent mode")
- **Warp Drive** (always capitalized)
- **Codebase Context** (capitalized as feature name)
- **macOS** (not "Mac OS" or "Mac")
- **Git repository** or **repo** (not "git repository")

## Output

Present the drafted documentation as a complete markdown file that can be saved directly to the appropriate location in `docs/`.
