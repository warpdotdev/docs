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

# 4. REQUIRED: request the reviewer for real (see "Request reviewers" below).
#    The PR is not complete until this has succeeded.

# Open in browser to fill details
gh pr create --web
```

### Request reviewers (required)

**Naming a reviewer in the body is not a review request.** A `/cc @engineer` mention notifies nobody through GitHub's review queue: the PR shows no requested reviewer, never appears in that engineer's "Review requested" filter, and quietly goes unreviewed. Every one of the four ambient-drafted docs PRs — #414, #415, #416, #417 — named reviewers in prose and received zero reviews; three had an empty requested-reviewers list and the fourth had a single reviewer added by hand.

So the mention stays, and a real request is added alongside it. **A PR is not complete until `gh pr edit --add-reviewer` has succeeded and been verified.**

A resolution failure must fall back, never no-op. When no owner resolves — the common case for a small, ambient/agent-generated docs PR — prefer the run's requester next, then a secondary human fallback, and only then `dannyneira` as the final safety net (the release docs workflow keeps its own last-resort `dannyneira` fallback too — `.github/workflows/release-docs-update.yml`, "Assign last docs PR reviewer"). An unassignable reviewer is a problem to surface, not a reason to ship an unreviewed PR.

The full priority chain, in order: (1) the CODEOWNERS/git-blame owner from `suggest_reviewers.py`; (2) the run's requester, resolved via this repo's own `.agents/skills/create_pr/resolve_reviewer.py --user <requester_slack_id>` and a runtime-supplied private override map; (3) a secondary human fallback, currently `hongyi-chen` ("HYC"); (4) `dannyneira`.

Step 2's resolver is a docs-repo-local script, not `factory-agents`' `scripts/factory-resolve-reviewer`: that script lives in the separate `factory-agents` repo and is not checked out alongside a normal `warpdotdev/docs` clone, so calling it by that relative path fails in a real docs run and silently falls through to the next tier. The invoking factory must mount its private Slack-to-GitHub override map and set `REVIEWER_OVERRIDES_PATH` before calling `resolve_reviewer.py`; never commit Slack user IDs or mappings to this repository. The helper does nothing else — no public-email search, no cross-repo assumptions — so the requester tier resolves from a plain docs checkout when that private runtime context is available. Like `factory-resolve-reviewer`, it never guesses: an unavailable map or unresolved Slack id prints nothing and the chain moves to the next tier.

The factory-level private override map owns requester identity mappings. This repository stores no real Slack IDs: keep `REQUESTER_SLACK_ID` as a runtime value and use a placeholder in examples and tests.

Two details below are load-bearing, and getting either wrong reintroduces the silent drop this section exists to prevent:

- **Request one reviewer per call.** `gh pr edit --add-reviewer a,b,c` sends a single atomic mutation, so one unassignable entry rejects the whole list. Since a resolution routinely mixes users with a team, and a team with no access to this repo cannot be requested here, a comma-joined call can fail wholesale and take every valid owner down with it.
- **Verify against the resolved set, not against emptiness.** "Is the list non-empty?" passes when the real owner was dropped and only the fallback landed, which looks identical to success.

```bash
PR=123
REQUESTER_SLACK_ID=""        # this run's requester Slack user id, when known
SECONDARY_FALLBACK_REVIEWER=hongyi-chen   # HYC - confirmed second-tier fallback
FALLBACK_REVIEWER=dannyneira               # final safety net; never remove

# 1. Resolve the owning engineer(s). For missing_docs drift-watch runs, use the
#    ownership resolver with the source files behind the change; see the
#    missing_docs skill's "Reviewer routing" section for how to pick those files.
#    Diagnostics go to stderr, so this captures only the reviewer list.
REVIEWERS=$(python3 .agents/skills/missing_docs/scripts/suggest_reviewers.py \
  --reviewers-only --warp ../warp --warp-server ../warp-server \
  warp:app/src/settings/ssh.rs < /dev/null)

# 2. No code-owner resolved. For a small, ambient/agent-generated PR with no
#    clear owner - the common case here - prefer the run's requester over
#    paging dannyneira: resolve their GitHub handle with this docs-local helper
#    and the invoking factory's private REVIEWER_OVERRIDES_PATH map. The helper
#    is callable from a plain docs checkout, unlike factory-agents'
#    scripts/factory-resolve-reviewer, which lives in a separate repo that
#    isn't checked out alongside this one.
#    Fall to the secondary human fallback next, and only then to the final
#    dannyneira safety net. Never let an empty resolution drop the request.
#    Track that this was a fallback so step 6 does not report it as an owner
#    who was requested.
RESOLUTION_WAS_EMPTY=0
if [[ -z "$REVIEWERS" ]]; then
  RESOLUTION_WAS_EMPTY=1
  if [[ -n "$REQUESTER_SLACK_ID" ]]; then
    REVIEWERS=$(python3 .agents/skills/create_pr/resolve_reviewer.py --user "$REQUESTER_SLACK_ID")
  fi
  [[ -z "$REVIEWERS" ]] && REVIEWERS="$SECONDARY_FALLBACK_REVIEWER"
  [[ -z "$REVIEWERS" ]] && REVIEWERS="$FALLBACK_REVIEWER"
  echo "warning: no owner resolved - falling back to $REVIEWERS"
fi

# 3. Request each reviewer separately so one bad entry cannot drop the rest.
IFS=',' read -ra WANT <<< "$REVIEWERS"
GOT=()
for R in "${WANT[@]}"; do
  if gh pr edit "$PR" --repo warpdotdev/docs --add-reviewer "$R"; then
    GOT+=("$R")
  else
    echo "warning: could not request $R on PR $PR"
  fi
done

# 4. Read back from the PR. This is the only trustworthy signal: `gh pr edit`
#    can exit 0 while quietly skipping a reviewer, so GOT records what gh
#    *claimed* and the read-back is what actually landed. Every decision below
#    keys off the read-back. Note the jq: teams have no .login, and
#    `[.reviewRequests[].login // .reviewRequests[].name]` silently drops them
#    from a mixed list.
read_requested() {
  gh pr view "$PR" --repo warpdotdev/docs \
    --json reviewRequests --jq '[.reviewRequests[] | .login // .slug // .name] | join(",")'
}
REQUESTED=$(read_requested)

# 5. A helper to check whether a specific reviewer is present in the
#    read-back, not just whether the read-back is non-empty. Match on the
#    last path segment, lowercased: a team resolves as `org/team` but reads
#    back as its bare slug, and GitHub logins are case-insensitive.
_norm() { printf '%s' "${1##*/}" | tr 'A-Z' 'a-z'; }
has_reviewer() {
  local want target
  want=$(_norm "$1")
  IFS=',' read -ra _have <<< "$REQUESTED"
  for target in "${_have[@]}"; do
    [[ "$(_norm "$target")" == "$want" ]] && return 0
  done
  return 1
}

# 6. Verify the fallback actually landed whenever resolution came back empty,
#    and otherwise fall back when nothing at all landed. An emptiness check on
#    $REQUESTED alone is wrong for the empty-resolution case: a PR that
#    already carries an unrelated reviewer (requested before this script ran,
#    e.g. by a human) makes $REQUESTED non-empty even though the fallback was
#    never assigned, which would skip re-requesting it here and then have the
#    next step falsely report it as requested when it never landed.
request_fallback() {
  local candidate="$1"
  if ! has_reviewer "$candidate"; then
    gh pr edit "$PR" --repo warpdotdev/docs --add-reviewer "$candidate" ||
      echo "warning: fallback $candidate could not be requested"
    REQUESTED=$(read_requested)
  fi
}

if (( RESOLUTION_WAS_EMPTY )); then
  request_fallback "$REVIEWERS"
  if [[ "$REVIEWERS" != "$FALLBACK_REVIEWER" ]] && ! has_reviewer "$REVIEWERS"; then
    # The settled-on fallback (requester tier or HYC) was rejected - a
    # rejection at this tier must still reach the final dannyneira safety net
    # rather than stopping here.
    echo "warning: $REVIEWERS rejected - advancing to final fallback $FALLBACK_REVIEWER"
    REVIEWERS="$FALLBACK_REVIEWER"
    request_fallback "$REVIEWERS"
  fi
elif [[ -z "$REQUESTED" ]]; then
  request_fallback "$FALLBACK_REVIEWER"
fi

if [[ -z "$REQUESTED" ]]; then
  echo "ERROR: no reviewer is on PR $PR - not even the fallback landed"
  exit 1
fi
if (( RESOLUTION_WAS_EMPTY )) && ! has_reviewer "$REVIEWERS"; then
  echo "ERROR: fallback $REVIEWERS could not be requested on PR $PR" \
       "(existing reviewers: $REQUESTED); report this run as failed."
  exit 1
fi

# 7. Compare the read-back against what was resolved.
IFS=',' read -ra HAVE <<< "$REQUESTED"
MISSING=()
for R in "${WANT[@]}"; do
  found=0
  for H in "${HAVE[@]}"; do
    [[ "$(_norm "$R")" == "$(_norm "$H")" ]] && { found=1; break; }
  done
  (( found )) || MISSING+=("$R")
done

if (( RESOLUTION_WAS_EMPTY )); then
  # Step 6 already guaranteed the settled-on fallback landed (or exited
  # above), so this always reports a true outcome, not just "nothing
  # resolved."
  echo "note: no owner resolved for PR $PR; fallback $REVIEWERS requested"
elif (( ${#MISSING[@]} == ${#WANT[@]} )); then
  # Owners resolved and none of them are on the PR. It has a reviewer, but not
  # the right one, and that must not read as success.
  echo "ERROR: none of the ${#WANT[@]} resolved owners are on PR $PR" \
       "(wanted: ${WANT[*]}); only the fallback is assigned. Report this run as failed."
  exit 1
elif (( ${#MISSING[@]} > 0 )); then
  echo "warning: ${#MISSING[@]}/${#WANT[@]} resolved owners missing from PR $PR" \
       "(missing: ${MISSING[*]}); name them and why in the run output"
fi

echo "Requested reviewers: $REQUESTED"
```

A partial result is a reportable outcome, not a pass: if some owners could not be requested, say which ones and why in the run output, so the gap is visible rather than buried. If even the fallback cannot be assigned, report the run as failed. Do not close out a PR whose requested-reviewers list is empty.

:::caution
A team handle resolved from `STAKEHOLDERS` or `CODEOWNERS` can only be requested on a repo that team has access to. `warpdotdev/oss-maintainers` is the root-rule owner in the warp client repo and therefore appears in most resolutions, but it has no access to `warpdotdev/docs`, so requesting it here fails. That is why step 3 requests one at a time.
:::

:::note
Auto-requesting the review does not make it *block* merge. Whether an ambient docs PR should require that approval through branch protection is an open question for the docs owner, not something this skill decides.
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

# Add reviewers - see "Request reviewers (required)" above; this is mandatory on a
# new PR, not an optional extra.
gh pr edit 123 --add-reviewer username
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

1. **Confirm the review request landed** - Re-read `reviewRequests` on the PR. An empty list means the PR is not finished, whatever the body says. See "Request reviewers (required)".
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
