---
name: review-docs-pr
description: Reviews documentation pull requests for the Warp docs repository. Checks for broken links, style guide compliance, content quality, and Astro Starlight structure. Use when reviewing documentation PRs or when you need to provide feedback on markdown documentation changes.
---

# Review Documentation PR

This skill reviews documentation pull requests for the Warp docs repository.

## Usage

Use this skill when reviewing documentation changes in PRs. The skill will:
- Check for potential broken links
- Verify style guide compliance
- Review content quality
- Check Astro Starlight structure integrity

## Review Instructions

Review this documentation PR for the docs repository.

Focus on:
1. **Broken links**: Check for potential broken internal links (relative paths, cross-space links). You can run the broken link checker at `python3 .warp/skills/check_for_broken_links/check_links.py --internal-only` if helpful.
2. **Style guide compliance**: Reference `AGENTS.md` for documentation standards (voice, formatting, terminology).
3. **Content quality**: Check for clarity, accuracy, proper frontmatter, and appropriate use of headers/lists.
4. **Code snippets**: Verify that any code examples, commands, or configuration snippets are correct and will work as documented. If you're unsure about technical details, use the `answer_question` skill to verify against the docs or search the source code.
5. **Astro Starlight structure**: Verify astro.config.mjs (sidebar config) updates if files were moved/renamed, and that redirects are added to vercel.json (redirects) when needed.

Provide actionable, constructive feedback. Focus on documentation quality issues, not code bugs.

### Severity Labels (Required)

Every comment body MUST begin with one of:
- `🚨 [CRITICAL]` — Broken links, incorrect commands/code, factually wrong information that could confuse users
- `⚠️ [IMPORTANT]` — Style guide violations, missing redirects, structural issues
- `💡 [SUGGESTION]` — Improvements to clarity, wording, or structure
- `🧹 [NIT]` — Typos, minor formatting (ONLY if providing a suggestion block)

### Using answer_question for verification

If you encounter:
- Unclear or potentially incorrect technical information
- Commands or code examples you want to verify
- Feature descriptions that seem outdated or inaccurate
- Questions about how something actually works

Use the `answer_question` skill to search the documentation and source code for authoritative information before making your review comment.

## Output Format

Create a `review.json` file with the following structure:

```json
{
  "summary": "High-level overview of the changes and verdict",
  "comments": [
    {
      "path": "path/to/file.md",
      "line": 42,
      "side": "RIGHT",
      "body": "Your feedback here"
    }
  ]
}
```

### Summary Requirements

The summary should:
- Start with a brief (2-3 sentence) overview of what the PR changes and your assessment
- Include issue counts: "Found: X critical, Y important, Z suggestions, N nits"
- End with final recommendation: "Approve", "Approve with nits", or "Request changes"

Keep the tone helpful and constructive. The summary can mention positive aspects (e.g., "good improvements to clarity") alongside concerns.

### Comment Format

Each comment should:
- Reference a specific line in a changed file
- Be actionable and constructive
- Use `side: "RIGHT"` for new/added lines (the new content after changes) - use this in most cases
- Use `side: "LEFT"` only when commenting on deleted/old lines (the content before changes)
- Focus on the diff, not unchanged code
- Keep comment spans ≤10 lines (i.e., `line - start_line <= 10`) for easier review
- Use single-line comments for specific issues (typos, broken links); use multi-line spans when the issue or suggestion requires multiple lines of context

#### Using GitHub Suggestion Syntax

When you have a specific fix or improvement, use GitHub's suggestion syntax in your comment body. This allows the author to apply your suggestion with one click.

Use suggestions for:
- Fixing typos or grammar
- Correcting commands or code snippets
- Improving wording or phrasing
- Fixing broken links
- Correcting terminology to match the style guide

If the changes look good with no major issues, indicate approval in the summary. For minor issues, suggest improvements but still recommend approval. Only request changes if there are significant problems that need to be fixed before merge.

## Validation

After creating `review.json`:
- Validate JSON with `jq . review.json` - if this fails, fix the JSON syntax and try again
- Verify all paths exist in the PR diff and match the changed files
- Check that line numbers are within the changed files and reference lines that were actually modified
- Ensure comment spans don't exceed 10 lines
