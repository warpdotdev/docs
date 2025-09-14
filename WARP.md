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