---
name: review-docs-pr
description: Reviews documentation pull requests for the Warp docs repository. Checks for broken links, style guide compliance, content quality, AEO/source-data fit, and Astro Starlight structure. Use when reviewing documentation PRs or when you need to provide feedback on markdown documentation changes.
---

# Review Documentation PR

This skill reviews documentation pull requests for the Warp docs repository.

## Usage

Use this skill when reviewing documentation changes in PRs. The skill will:
- Check for potential broken links
- Verify style guide compliance
- Review content quality
- Review AEO/source-data fit for docs changes that target search or answer-engine visibility
- Check Astro Starlight structure integrity

When the PR carries the `warpy-factory` label, this is the **independent v1
agent-doc quality review pass** dispatched by
`.github/workflows/agent-docs-review.yml` for the current head SHA (see
"Agent-marked PR review (v1 contract)" below).

## Agent-marked PR review (v1 contract)

For a PR carrying the `warpy-factory` label, in addition to the standard
review focus areas, this pass is the human-review-blocking gate defined in
`.agents/references/doc-quality-policy.md`:

1. **Re-validate the declared risk.** Parse the PR's `## Documentation risk`
   section (`.agents/skills/doc_quality_policy/policy.py`'s
   `parse_documentation_risk_section`). Walk the diff against the low-risk
   allowlist yourself. A declared `low` risk that actually touches any
   engineering-review trigger (a new/changed feature page, or any of the
   technical claim categories in the allowlist) is a **risk
   misclassification** — flag it `⚠️ [IMPORTANT]` and reflect it in the
   verdict (see "Severity Labels" below); it is not a soft suggestion.
2. **Verify technical claims against source** when the PR is (or should be)
   `engineering-review-required`: confirm the cited `Source files consulted`
   actually support the claims. Use `answer_question` when source access is
   available.
3. **Check the compression contract.** Run
   `.agents/skills/doc_quality_policy/check_compression_contract.py` against
   each changed content-type page. An unjustified violation (no reasoning in
   the PR body for the overage) is `⚠️ [IMPORTANT]`; a justified one is
   `💡 [SUGGESTION]` at most.
4. **Check VERIFY accounting.** Run the structural mode of
   `.agents/skills/doc_quality_policy/check_pr_contract.py --body <file>
   <changed files>` against the current head. Do not invoke
   `--enforce-engineering-gate` during the independent review; a pending human
   approval is not itself a contract violation. Any reported contract
   violation (missing section, unlisted marker, listed marker at `low` risk)
   is `🚨 [CRITICAL]`.

## Review Instructions

Review this documentation PR for the docs repository.

Focus on:
1. **Broken links**: Check for potential broken internal links (relative paths, cross-space links). You can run the broken link checker at `python3 .agents/skills/check_for_broken_links/check_links.py --internal-only` if helpful.
2. **Style guide compliance**: Reference `AGENTS.md` for documentation standards (voice, formatting, terminology).
3. **Content quality**: Check for clarity, accuracy, proper frontmatter, and appropriate use of headers/lists.
4. **Code snippets**: Verify that any code examples, commands, or configuration snippets are correct and will work as documented. If you're unsure about technical details, use the `answer_question` skill to verify against the docs or search the source code.
5. **Astro Starlight structure**: Verify `src/sidebar.ts` updates if files were added, moved, or renamed, and that redirects are added to the `redirects` array in `vercel.json` when needed.
6. **Product name variables**: Check whether any product names with a corresponding entry in `src/data/vars.ts` are hardcoded as literal strings instead of using `{VARS.KEY}` (prose) or `{{TOKEN}}` (frontmatter). Key strings to watch for: "Oz CLI", "Oz web app", "oz.warp.dev", "Oz dashboard", "Oz run". Flag as `⚠️ [IMPORTANT]` if a new file adds these without using the variable system. For existing files, flag as `💡 [SUGGESTION]`.
7. **Tone and AI-isms**: Flag marketing buzzwords (seamless, powerful, robust, comprehensive, leverage, streamline), meta-openers ("This page covers/explains/walks through..."), restated cause-and-effect ("This process ensures..."), recap lines, consecutive callouts or more than one callout per section, and internal-architecture detail the reader can't act on (orchestrators, control planes, lifecycle states). Reference the "Voice & tone" section of `AGENTS.md`. Use `💡 [SUGGESTION]` for isolated instances; use `⚠️ [IMPORTANT]` when the pattern is pervasive in new content.
8. **Length and brevity**: Flag a page that could be materially shorter, not just wordy sentences — a 2,000-word page that should be 600 is a more expensive problem than an isolated buzzword. Check whether a deletion-only "Cut again" pass (AGENTS.md → Voice & tone → Cut again) happened before the page was split into sub-pages, since splitting a bloated page produces two bloated pages. Use `💡 [SUGGESTION]` unless the page is far outside its content type's expected length, then use `⚠️ [IMPORTANT]`.
9. **AEO/source-data fit**:

Provide actionable, constructive feedback. Focus on documentation quality issues, not code bugs.

### Severity Labels (Required)

Every comment body MUST begin with one of:
- `🚨 [CRITICAL]` — Broken links, incorrect commands/code, factually wrong information that could confuse users, or a v1 contract violation (missing/invalid `## Documentation risk`, an unlisted `VERIFY` marker)
- `⚠️ [IMPORTANT]` — Style guide violations, missing redirects, structural issues, a documentation-risk misclassification, or an unjustified compression-contract violation
- `💡 [SUGGESTION]` — Improvements to clarity, wording, or structure
- `🧹 [NIT]` — Typos, minor formatting (ONLY if providing a suggestion block)

**Blocking rule for agent-marked PRs.** Any `🚨 [CRITICAL]` or `⚠️ [IMPORTANT]`
finding — including a risk misclassification — means the verdict is
**Request changes**. Suggestions and nits never block.

### Using answer_question for verification

If you encounter:
- Unclear or potentially incorrect technical information
- Commands or code examples you want to verify
- Feature descriptions that seem outdated or inaccurate
- Questions about how something actually works

Use the `answer_question` skill to search the documentation and source code for authoritative information before making your review comment.

### AEO review guidance

For AEO-driven docs PRs, review the diff through these questions:
- **Source rationale** - Is it clear which Peec prompt, search-query cluster, recommendation, or content gap motivated the change? If not, ask for the source signal or suggest narrowing the scope.
- **Vocabulary translation** - Does the draft preserve high-intent search terms where useful while translating awkward source-data language into natural docs language?
- **Reader value** - Would the page help a developer complete or understand a real workflow, or is it collecting loosely related keywords?
- **Terminology and UI surfaces** - Are product names, settings paths, panel names, and navigation labels consistent with `AGENTS.md`, `.agents/references/terminology.md`, and the actual UI?
- **Scannability** - Are dense procedures broken into numbered steps, bullets, or concise subsections with expected outcomes?
- **Duplication risk** - Should the content update an existing page, link to an existing page, or be merged with related content instead of living as a new standalone doc?

When the issue is a judgment call, prefer a `💡 [SUGGESTION]` comment that explains the tradeoff rather than blocking the PR.

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

## Signal logging

After creating and validating `review.json` (immediately after the Validation section above), emit a summary record for the `improve-drafting-skills` outer loop. Do this before any step that submits or hands off the review — the marker must appear in the Oz run output regardless of how the review is ultimately published. Apply only when reviewing an agent-authored PR (branch created by a drafting skill, or commit author is `oz-agent@warp.dev`).

1. Count comments in `review.json` by severity label (`🚨 [CRITICAL]`, `⚠️ [IMPORTANT]`, `💡 [SUGGESTION]`, `🧹 [NIT]`).
2. Identify the top 3 issue categories by frequency (use the `check` name if available from style lint output, or infer a short category from the comment body).
3. Determine the skill used from the PR branch name or PR description if available.
4. Include the following structured marker in your **text response** (write it as part of your agent message, not via a shell `echo` command). This ensures it appears as a `TextContentBlock` in the conversation, where `oz run get --conversation` can reliably retrieve it:
   ```
   [SIGNAL:pr-review] {"date":"YYYY-MM-DD","pr":"NNN","branch":"branch-name","head_sha":"abc1234","skill_used":"draft_feature_doc","reviewer_login":"GITHUB_LOGIN","verdict":"Request changes","critical":N,"important":N,"suggestions":N,"nits":N,"top_categories":["category (N)","category (N)","category (N)"]}
   ```
   Set `head_sha` to the exact commit SHA this review evaluated (the head SHA
   `.github/workflows/agent-docs-review.yml` passed in, or `gh pr view NNN
   --json headRefOid --jq .headRefOid` when reviewing interactively). A push
   of a new commit makes any earlier signal for this PR stale; the collector
   in `improve-drafting-skills` keys its `review_outcome` lookup on this field
   matching the PR's current head.

The `improve-drafting-skills` outer loop reads this signal from the conversation via `oz run get --conversation`, scanning assistant `TextContentBlock` messages for the marker. No git operations are required.

## Publishing a GitHub review

After creating `review.json`, publishing the signal, and completing validation, create one GitHub PR review pinned to the evaluated head SHA. The review body must include the same `[SIGNAL:pr-review]` JSON record used in the text response.

1. Determine the authenticated reviewer and map the verdict:
   ```bash
   REVIEWER_LOGIN=$(gh api user --jq .login)
   ```
   Use `APPROVE` for `Approve`, `REQUEST_CHANGES` for `Request changes`, and `COMMENT` for `Approve with nits`.
2. Write the signal JSON object to `/tmp/review-signal.json`, set its
   `reviewer_login` to `$REVIEWER_LOGIN`, and render that same object as the
   `[SIGNAL:pr-review]` line in the final response. Then construct the
   pinned review request from `review.json`:
   ```bash
   HEAD_SHA="<evaluated PR head SHA>"
   VERDICT="<Approve|Approve with nits|Request changes>"
   export HEAD_SHA VERDICT
   python3 - <<'PY'
   import json
   import os
   from pathlib import Path

   review = json.loads(Path("review.json").read_text())
   signal = json.loads(Path("/tmp/review-signal.json").read_text())
   event = {
       "Approve": "APPROVE",
       "Approve with nits": "COMMENT",
       "Request changes": "REQUEST_CHANGES",
   }[os.environ["VERDICT"]]
   payload = {
       "commit_id": os.environ["HEAD_SHA"],
       "event": event,
       "body": f"{review['summary']}\n\n[SIGNAL:pr-review] {json.dumps(signal, sort_keys=True)}",
       "comments": review["comments"],
   }
   Path("/tmp/review-request.json").write_text(json.dumps(payload))
   PY
   ```
3. Submit the review:
   ```bash
   gh api --method POST "repos/OWNER/REPO/pulls/PR_NUMBER/reviews" \
     --input /tmp/review-request.json
   ```
   Replace `OWNER/REPO`, `PR_NUMBER`, and `commit_id` with the pull request being reviewed and its exact head SHA.

The workflow verifies that a current-head review from `reviewer_login` contains the exact signal fields. Do not leave the signal only in the agent response or an issue comment.
