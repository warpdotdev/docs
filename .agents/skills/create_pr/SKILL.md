---
name: create_pr
description: Create a pull request in the docs repository for the current branch. Use when the user mentions opening a PR, creating a pull request, submitting changes for review, or preparing documentation for merge.
---

# create_pr

## Overview

This guide covers best practices for creating pull requests in the docs documentation repository, including syncing with main, running linting checks, validating links, and structuring your PR for effective review.

## Related Skills

- `draft_docs` - Draft new documentation pages or update existing ones using established style conventions
- `check_for_broken_links` - Check documentation for broken internal and external links before opening PR
- `doc_quality_policy` - Shared v1 agent-doc quality contract (marker, risk classification, overrides) this skill's PRs must satisfy

## Pre-PR Checklist

### 1. Sync with main

**Always merge main into your feature branch before opening a PR.**

```bash
git fetch origin
git merge origin/main
```

Resolve any merge conflicts locally before opening the PR.

### 2. Run linting checks

This repo uses Trunk CLI for linting. Run these checks before opening or updating a PR:

```bash
# Check for linting issues
trunk check

# Auto-format files
trunk fmt
```

Enabled linters include:
- `markdownlint` - Markdown formatting and style
- `yamllint` - YAML file validation
- `gitleaks` - Secret detection
- `oxipng` - PNG optimization

:::note
Trunk CLI is not vendored in this repo. Install it separately: https://docs.trunk.io/check/usage
:::

### 3. Check for broken links

Run the link checker to validate all internal and external links:

```bash
# Quick internal-only check (fast, no HTTP requests)
python3 .agents/skills/check_for_broken_links/check_links.py --internal-only

# Full check including external links
python3 .agents/skills/check_for_broken_links/check_links.py
```

Fix any broken links before opening the PR. See the `check_for_broken_links` skill for detailed guidance on fixing different link types.

### 4. Review your changes

Before creating a PR, review what you're about to submit:

```bash
# View commits in your branch
git --no-pager log origin/main..HEAD --oneline

# View file statistics
git --no-pager diff origin/main...HEAD --stat

# View full diff
git --no-pager diff origin/main...HEAD
```

This helps you:
- Verify all intended changes are included
- Catch unintended changes before review
- Write an accurate PR description

### 5. Verify sidebar updates

If you added, moved, or renamed any documentation pages:

- Update the sidebar in `src/sidebar.ts`. That file is the source of truth; `astro.config.mjs` only imports it via `starlightSidebarTopics(sidebarTopics)`.
- Ensure the label matches the H1 title in the document, or omit the label and let Starlight derive it.
- Check that the slug is correct: no leading slash and no `.md`/`.mdx` extension.

### 6. Add redirects for moved/renamed pages

If you renamed or moved a page that's already published, add a redirect to the `redirects` array in `vercel.json` at the repo root. Every redirect lives in that one file, including redirects between top-level sections — there is no per-section redirect file and no external redirect tool.

Check existing redirects first to avoid duplicates.

```json
{
  "source": "/old/path",
  "destination": "/new/path/",
  "statusCode": 308
}
```

Include the trailing slash on `destination` and the `statusCode`, matching the existing entries.

## PR Description Guidelines

Structure your PR description with these sections, in this order. The feature summary comes first; everything else follows it.

### What this feature does (required on drafting PRs)

Open the body with a plain-language summary of what the feature does **for the user**. This is the first thing a reviewing engineer reads, so it must not be pipeline bookkeeping — which spec produced the draft, which workflow generated it, and which run it came from all belong further down. A reviewer who only reads this section should be able to tell whether the docs describe the right thing.

End the summary with the shipped-in fact, not a forecast. Read the version and date from the release accessor the drift-watch gate already uses, rather than adding a second way to look up a release:

```bash
# Exits 10 when the current stable release was already processed, which is not an
# error for this purpose — we only want the version and date it reports.
python3 .agents/skills/missing_docs/scripts/check_new_release.py --json > /tmp/release.json || true
python3 -c "import json; d=json.load(open('/tmp/release.json')); print(d['current_version'], d['release_date'])"
```

Write "shipped in `<version>` (`<date>`)". Do not write a target or predicted ship date: there is no trustworthy source for one, and a forecast in a merged PR body ages into a false claim.

**Length budget: 75 words maximum**, ideally two to four sentences. Drafts are already too wordy; a summary that runs longer than a short paragraph has stopped being a summary. `check_pr_body.py` enforces the budget, the heading text, and the position.

```markdown
## What this feature does

Workspace admin roles let a workspace owner delegate whole-workspace management — membership, billing, and cloud agent run visibility — to an admin without handing over ownership. Shipped in `v0.2026.08.18.02.52.stable_00` (`2026-08-18`).
```

Verify it before submitting, along with the other body checks:

```bash
python3 .agents/skills/create_pr/check_pr_body.py /tmp/pr-body.md \
  --require-lead-section "## What this feature does"
```

The check fails if the section is missing, is not the first content in the body, is empty, or exceeds the word budget. Position is checked against content rather than headings, so a body cannot open with a few unheaded lines of spec/workflow/run-ID preamble and still pass. Omit the section — and the flag — only for the small corrections listed under "When a plan can be skipped": typos, link fixes, terminology sweeps, generated updates, and screenshot swaps have no feature to summarize.

### Summary
Brief explanation of what the PR accomplishes and why. This is where the pipeline detail goes: the source spec, the generating workflow, the new page path, and the sidebar entry.

### Changes
Bulleted list of specific changes, organized by file or area:

```markdown
## Summary
This PR updates the Terminal and Agent modes documentation for the Oz launch.

## Changes

### src/content/docs/agent-platform/local-agents/interacting-with-agents/terminal-and-agent-modes.md
- Added Getting Started section with first-time and existing user experiences
- Updated keyboard shortcuts with comprehensive tables
- Added fork functionality documentation

### src/sidebar.ts
- Updated navigation entry title
```

### Content design plan (required on drafting PRs)

Any PR that adds a page or makes a substantive update to one must carry the content design plan that preceded the draft. Keeping it next to the diff is the point: a reviewer can then disagree with who the page is for and what job it serves, which is far cheaper to resolve before the prose is written. See `.agents/references/content-design-plan.md` for the field definitions and `.agents/references/docs-worthiness-criteria.md` for the gate that runs before it.

```markdown
## Content design plan

**Audience and JTBD:** A backend engineer connecting their first factory to a self-hosted GitLab instance, who needs runs to authenticate without a personal token.

**Problem:** The GitLab integration page covers GitLab.com only, so self-hosted users follow steps that silently fail at the auth step.

**Goals:**
- The reader can tell whether their GitLab instance needs the self-hosted path.
- The reader can complete the self-hosted connection and confirm it worked.

**Purpose and value:** Without it, self-hosted users file support tickets after the happy path fails. No existing page covers the self-hosted variant.

**Content type:** Procedural — the reader is performing a setup task, not learning a concept.

**Skill and template:** `draft_procedural` / `.agents/templates/procedural.md`

**High-impact scenarios:**
- Covers: self-hosted GitLab with a project access token; verifying the connection.
- Excludes: GitLab behind a corporate proxy — rare, and the proxy config is the user's own infrastructure concern.
```

For the small corrections listed under "When a plan can be skipped" — typos, link fixes, terminology sweeps, generated updates, screenshot swaps — omit the section rather than filling it with placeholders.

### Unverified claims (required on drafting PRs)

Any PR that adds or updates page content must state which UI labels, Settings paths, CLI flags, permission defaults, plan eligibility, and platform-support claims could not be verified against `warp-internal`, `warp-server`, or a live build. See step 9.5 of the `draft_docs` skill.

Include the section even when nothing is outstanding:

```markdown
## Unverified claims
None — all UI labels, flags, defaults, and eligibility claims were verified against source.
```

When claims are outstanding, give the reviewer one bullet per claim with what would confirm it:

```markdown
## Unverified claims
- `--auto-approve` flag name — `cloud-agents.mdx`, "Run an agent" — taken from the PRD; confirm against `TuiArgs` in `warp-internal`.
- **Settings** > **Agents** > **Permissions** path — `permissions.mdx`, "Defaults" — source repos were not available in this environment.
```

### Documentation risk (required on all content PRs)

Every content PR carries a `## Documentation risk` section and the
`warpy-factory` label, per the shared v1 agent-doc quality contract in
`.agents/references/doc-quality-policy.md`. Classify risk against the
low-risk allowlist there, then build the section:

```bash
python3 .agents/skills/doc_quality_policy/finalize_pr_contract.py build \
  --risk low --rationale "One-line reason the change is low risk."
```

Insert the printed block into the body (after "Unverified claims" is a good
place) and apply the label once the PR exists:

```bash
gh pr edit <pr> --repo warpdotdev/docs --add-label warpy-factory
```

Before marking the PR ready, verify the contract:

```bash
python3 .agents/skills/doc_quality_policy/check_pr_contract.py --body /tmp/pr-body.md
```

### Additional context (optional)
- Link to related issues or discussions
- Screenshots for visual changes
- Notes for reviewers

## CLI Workflow

### Check if PR exists for current branch

```bash
gh pr view --json number,url
```

Exit code 0 if PR exists, 1 if not.

### Create a new PR

:::caution
**Always use `--body-file` instead of `--body` for PR descriptions.** Documentation PRs frequently contain backticks, quotes, and other special characters that get corrupted by shell escaping when passed inline. Write the description to a file first, then reference it.

`--body-file` avoids shell-escaping corruption, but it does **not** catch repetition-loop degeneration — a failure mode where the model repeats a phrase or bullet several times and cuts off mid-token (e.g. a sentence ending in an unclosed inline-code span like `` because `m ``). That corrupted text is already in the generated body and survives `--body-file` unchanged. Always run the body integrity checker (`check_pr_body.py`) before creating or editing a PR.
:::

```bash
# 1. Write the description to a temp file using the create_file tool or a heredoc.
#    The `## What this feature does` block is DRAFTING-PR ONLY - drop it (and the
#    --require-lead-section flag in step 2) for typos, link fixes, terminology
#    sweeps, generated updates, and screenshot swaps.
cat > /tmp/pr-body.md << 'EOF'
## What this feature does
One short paragraph: what the feature does for the user, ending with
shipped in `<version>` (`<date>`).

## Summary
Description of changes

## Changes
- Change 1
- Change 2

Co-Authored-By: Oz <oz-agent@warp.dev>
EOF

# 2. Verify the body for corruption before submitting (exits non-zero on failure).
python3 .agents/skills/create_pr/check_pr_body.py /tmp/pr-body.md \
  --require-lead-section "## What this feature does"   # drafting PRs only

# For a non-drafting correction, run the check without the flag:
# python3 .agents/skills/create_pr/check_pr_body.py /tmp/pr-body.md

# 3. Create the PR using the file (only if the check passed)
gh pr create --title "docs: Add feature documentation" --body-file /tmp/pr-body.md

# 4. Optionally request ONE reviewer - only when ownership resolution names
#    exactly one owning engineer (see "Request a reviewer" below).
#    No clear owner means no request.

# Open in browser to fill details
gh pr create --web
```

### Request a reviewer (at most one, only with conviction)

Reviewer requests are rare and small by design. Docs PRs used to over-tag: multi-owner requests, a mandatory fallback chain, and re-requests on every update paged people who had no reason to look. Three rules replace all of that, and each one is load-bearing:

1. **At most one reviewer, always a human.** Never request more than one person on a PR, and never request a team — a team handle (e.g. `warpdotdev/oss-maintainers`) pages several people for a change one engineer can review, and most teams resolved from ownership files have no access to `warpdotdev/docs` anyway. If ownership genuinely spans several engineers, request nobody and name the candidates in the PR body instead.
2. **Request only with 100% conviction.** Make a request only when ownership resolution (`suggest_reviewers.py` against the source files behind the change) identifies exactly one owning engineer. An empty resolution or a multi-owner resolution is not conviction: open the PR with no requested reviewer and record why in the run output. **There is no fallback reviewer.** Never substitute the run's requester, a teammate, or a default human when nothing resolves — a PR honestly waiting for triage beats a review request aimed at the wrong person.
3. **Never fight a human over the reviewer list.** If someone removed a reviewer from the PR (a `review_request_removed` event in its timeline), do not add that person back — and treat the removal as a signal to stop adding reviewers to that PR at all. If the PR already has a requested reviewer or a submitted review, add nobody. A reviewer request happens at most once, immediately after PR creation; later pushes or body edits never top the list back up.

When you do request the one resolved owner, make it a real request. A `/cc @engineer` mention in the body notifies nobody through GitHub's review queue — PRs #414–#417 named reviewers in prose and got zero reviews — so mention and request the same single engineer together, via `gh pr edit --add-reviewer`. When there is no conviction, do neither.

```bash
PR=123

# 1. Resolve the owning engineer(s) for the source files behind the change.
#    For missing_docs drift-watch runs, see that skill's "Reviewer routing"
#    section for how to pick the source files. Diagnostics go to stderr, so
#    this captures only the reviewer list.
REVIEWERS=$(python3 .agents/skills/missing_docs/scripts/suggest_reviewers.py \
  --reviewers-only --warp ../warp --warp-server ../warp-server \
  warp:app/src/settings/ssh.rs < /dev/null)

# 2. Distill the resolution to at most ONE human. Team entries (org/slug)
#    are never requested. Two or more distinct users is ambiguity, not
#    conviction: request nobody and name the candidates in the PR body.
CANDIDATE=""
CANDIDATE_KEY=""
AMBIGUOUS=0
IFS=',' read -ra RESOLVED <<< "$REVIEWERS"
for R in "${RESOLVED[@]}"; do
  [[ -z "$R" || "$R" == */* ]] && continue
  R_KEY="${R,,}"
  if [[ -z "$CANDIDATE" ]]; then
    CANDIDATE="$R"
    CANDIDATE_KEY="$R_KEY"
  elif [[ "$R_KEY" != "$CANDIDATE_KEY" ]]; then
    AMBIGUOUS=1
  fi
done
if [[ -z "$CANDIDATE" ]]; then
  echo "note: no owner resolved for PR $PR - opening it with no requested reviewer"
elif (( AMBIGUOUS )); then
  echo "note: multiple owners resolved for PR $PR ($REVIEWERS) - no single clear owner, requesting nobody"
  CANDIDATE=""
fi

# 3. Requests are add-once. Skip when the PR already has a requested reviewer
#    or a submitted review, and stop adding reviewers after any human removal.
if [[ -n "$CANDIDATE" ]]; then
  if ! REQUESTED=$(gh pr view "$PR" --repo warpdotdev/docs \
    --json reviewRequests --jq '[.reviewRequests[] | .login // .slug // .name] | join(",")'); then
    echo "warning: could not read requested reviewers for PR $PR - requesting nobody"
    CANDIDATE=""
  elif [[ -n "$REQUESTED" ]]; then
    echo "note: PR $PR already has reviewer(s) ($REQUESTED) - not adding more"
    CANDIDATE=""
  fi
fi
if [[ -n "$CANDIDATE" ]]; then
  if ! REVIEWED=$(gh api "repos/warpdotdev/docs/pulls/$PR/reviews" --paginate \
    --jq '[.[].user.login] | unique | join(",")'); then
    echo "warning: could not read submitted reviews for PR $PR - requesting nobody"
    CANDIDATE=""
  elif [[ -n "$REVIEWED" ]]; then
    echo "note: PR $PR already has submitted review(s) ($REVIEWED) - not adding a reviewer"
    CANDIDATE=""
  fi
fi
if [[ -n "$CANDIDATE" ]]; then
  if ! REMOVED=$(gh api "repos/warpdotdev/docs/issues/$PR/timeline" --paginate \
    --jq '[.[] | select(.event == "review_request_removed")
           | (.requested_reviewer.login // .requested_team.slug // empty)] | unique | join(",")'); then
    echo "warning: could not read reviewer-removal history for PR $PR - requesting nobody"
    CANDIDATE=""
  elif [[ -n "$REMOVED" ]]; then
    echo "note: PR $PR has a reviewer-removal event ($REMOVED) - not adding reviewers"
    CANDIDATE=""
  fi
fi

# 4. Request the single owner. A failed request is a reportable outcome,
#    never a reason to substitute someone else.
if [[ -n "$CANDIDATE" ]]; then
  if gh pr edit "$PR" --repo warpdotdev/docs --add-reviewer "$CANDIDATE"; then
    echo "Requested reviewer: $CANDIDATE"
  else
    echo "warning: could not request $CANDIDATE on PR $PR - leaving it with no requested reviewer"
  fi
fi
```

A PR with an empty requested-reviewers list is a valid, reportable outcome — say why in the run output (no owner resolved, several owners resolved, a human removed the reviewer, or the request failed). What is never acceptable is inventing a reviewer just to make the list non-empty.

:::note
A requested review does not block merge. The Docs team owns the merge decision after its normal review, whether the engineer replies in GitHub, replies elsewhere, or does not reply.
:::

### Update an existing PR

When updating the body of an existing PR, make the **smallest** change rather than regenerating the whole description from memory — re-emitting a long body is what invites repetition-loop degeneration. Fetch the current body, apply a minimal or additive edit, verify it, then submit.

```bash
# 1. Fetch the current body to a file
gh pr view 123 --json body --jq .body > /tmp/pr-body.md

# 2. Make a minimal/additive edit to /tmp/pr-body.md (e.g. append a new section)
#    with the edit_files or create_file tools — do not rewrite untouched sections.

# 3. Verify the body for corruption before submitting (exits non-zero on failure)
python3 .agents/skills/create_pr/check_pr_body.py /tmp/pr-body.md

# 4. Edit the body using the file (only if the check passed)
gh pr edit 123 --body-file /tmp/pr-body.md

# Edit title only
gh pr edit 123 --title "New title"

# Add labels
gh pr edit 123 --add-label documentation

# Do NOT add reviewers while updating an existing PR. A reviewer request
# happens at most once, at creation ("Request a reviewer" above) - and anyone
# a human removed stays removed.
```

### View PR status

```bash
gh pr status
gh pr checks
```

## Co-Author Attribution

When creating commits or PRs with AI assistance, include attribution at the end of every commit message or PR description:

```
Co-Authored-By: Oz <oz-agent@warp.dev>
```

## After Opening the PR

1. **Leave the reviewer list to humans** - If you requested an owner, confirm once that it landed. An empty `reviewRequests` list is a valid outcome when no single owner resolved, and if anyone removes a reviewer later, do not re-add them. See "Request a reviewer (at most one, only with conviction)".
2. **Monitor for merge conflicts** - If main is updated, merge it into your branch
3. **Respond to review comments** - Address feedback promptly
4. **Re-run checks after changes** - Run `trunk check` and link checker after making updates
5. **Verify Astro Starlight preview** - Astro Starlight automatically generates a preview for PRs; check that rendering looks correct

## Best Practices

- **Keep PRs focused** - One logical documentation change per PR when possible
- **Use descriptive titles** - Start with `docs:` prefix for documentation changes
- **Follow the style guide** - Refer to `AGENTS.md` for voice, tone, and formatting conventions
- **Test locally** - Use `npm run dev` to preview changes before opening PR
- **Include context** - Help reviewers understand why changes were made, not just what changed
