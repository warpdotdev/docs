---
name: sync_terminology
description: >-
  Sync the Warp terminology glossary from the Notion Dictionary to the repo.
  Fetches the Notion Dictionary page, compares with .agents/references/terminology.md,
  and opens a PR for any additions or changes. Flags repo-only terms that are
  missing from Notion. Use on a weekly schedule or manually when terminology changes.
---

# Sync Terminology from Notion

Keep `.agents/references/terminology.md` in sync with the canonical Notion Dictionary.

**Direction:** Notion → repo. Notion is the source of truth. If the repo has terms not in Notion, flag them for addition to Notion rather than removing them from the repo.

## Agent-doc quality contract

The PR this skill opens or updates follows the shared v1 agent-doc quality
contract in `.agents/references/doc-quality-policy.md`: apply the
`warpy-factory` label and add the `## Documentation risk` block
(`.agents/skills/doc_quality_policy/finalize_pr_contract.py build`). A
terminology sync is typically `low` risk — it preserves product meaning and
changes only naming/formatting guidance.

## Prerequisites

- Notion MCP server must be connected and authenticated
- `gh` CLI must be available and authenticated
- You must be in the `warpdotdev/docs` repo

## Workflow

### Step 1: Fetch the Notion Dictionary

Use the Notion MCP to fetch the Dictionary page:

```
notion-fetch with id: "NOTION_DICTIONARY_PAGE_ID"
```

The page has two sections:
- **Rules section** — Uses "Use / Avoid / Notes" format for capitalization and naming consistency
- **Terminology section** — Uses glossary format with definitions and usage notes

Parse both sections. Extract each term with its:
- **Name** (the canonical form)
- **Definition or rule** (the "Use" form, or the glossary definition)
- **Avoid forms** (if any)
- **Notes** (if any)
- **Category** (infer from the Notion page's heading structure)

### Step 2: Read the current terminology.md

Read `.agents/references/terminology.md` from the repo. Parse each entry, extracting:
- **Name** (the bolded term)
- **Definition** (the text after the em dash)
- **Usage note** (the italic `*Usage note:*` line, if present)
- **Category** (the `##` heading the term falls under)

### Step 3: Compare in both directions

#### Notion → repo (new or changed terms)
For each term in Notion, check if it exists in `terminology.md`:
- **New term:** exists in Notion but not in the repo file
- **Changed term:** exists in both, but the definition, avoid forms, or notes differ meaningfully (ignore minor formatting differences)

#### Repo → Notion (orphaned terms)
For each term in `terminology.md`, check if it exists in the Notion Dictionary:
- **Orphaned term:** exists in the repo but not in Notion

Collect both lists.

### Step 4: If no differences, exit

If both lists are empty, report "Terminology is in sync" and stop. Do not create a branch or PR.

### Step 5: Update terminology.md with Notion changes

If there are new or changed terms from Notion:

1. Check out the standing branch. This skill maintains **one** long-lived sync PR rather than one per run — see "One standing PR per automation" in `.agents/references/skill-authoring-guidelines.md`.
   ```bash
   # Is there already an open terminology sync PR?
   gh pr list --repo warpdotdev/docs --state open \
     --search 'sync terminology from Notion Dictionary in:title' \
     --json number,headRefName

   git fetch origin
   # If the PR exists, continue on its branch and rebase; otherwise create it from main.
   git checkout sync-terminology 2>/dev/null || git checkout -b sync-terminology origin/main
   git rebase origin/main
   ```
   Do not create a date-suffixed branch. Terminology drift accumulates across weeks, and a dated branch per run produces a pile of PRs that all edit the same two files and conflict with each other.

2. For each **new term**, add it to the appropriate category section in `terminology.md`:
   - Match the category from Notion to the existing `##` sections in the file
   - If no matching section exists, create a new `##` section
   - Insert alphabetically within the section
   - Use the standard format:
     ```markdown
     - **Term** — Definition.
       *Usage note:* Additional guidance.
     ```
   - For "Avoid" rules from Notion's Rules section, format as:
     ```markdown
     - ❌ **Avoided Term** — Explanation. Use "Preferred Form" instead.
     ```

3. For each **changed term**, update the existing entry to match Notion.

4. Also update the corresponding summary entries in `AGENTS.md` under `## Terminology standards` if the term appears there. The AGENTS.md section is a summary — only add terms there if they are core features, Oz terms, technical terms, billing terms, or UI elements.

### Step 6: Commit and open a PR

```bash
git add .agents/references/terminology.md AGENTS.md
git commit -m "docs: sync terminology from Notion Dictionary

Co-Authored-By: Oz <oz-agent@warp.dev>"
git push origin sync-terminology
```

If a PR already exists for this branch, the push updates it — do not open a second one. Append this run's terms to the existing body under its existing headings rather than adding a new dated section: `check_pr_body.py` rejects duplicate headings, so per-run copies of `## Terms added` would fail the check and block the update. Fetch the current body first and make a minimal additive edit.

If no PR exists, open one. Write the body to a file before creating the PR — lists of changed terms can be long and are prone to repetition-loop degeneration when passed inline:

```bash
# Write body to a temp file first
cat > /tmp/sync-terminology-pr-body.md << 'EOF'
## Terms added
[list each term with definition]

## Terms changed
[list each term with before/after]

## Terms in repo but missing from Notion
[see Step 7 — list here if applicable]

Co-Authored-By: Oz <oz-agent@warp.dev>
EOF

# Verify the body before creating the PR
python3 .agents/skills/create_pr/check_pr_body.py /tmp/sync-terminology-pr-body.md

gh pr create \
  --title "docs: sync terminology from Notion Dictionary" \
  --label documentation \
  --body-file /tmp/sync-terminology-pr-body.md
```

Use `report_pr` to surface the PR link.

### Step 7: Flag orphaned repo terms

If there are terms in the repo that are not in Notion, include a section in the PR body:

```markdown
## Terms in repo but missing from Notion

The following terms exist in `terminology.md` but were not found in the
Notion Dictionary. Please add these to the Dictionary page, or let us
know if they should be removed from the repo.

- **Term 1** — definition
- **Term 2** — definition
```

This ensures the repo doesn't silently accumulate terms that bypass Notion.

## Mapping Notion format to terminology.md format

### Rules section entries (Use / Avoid / Notes)

Notion format:
```
- Agent Mode vs agent mode
  - Use: Agent Mode
  - Avoid: agent mode, Agent mode
  - Notes: Treat as a feature name.
```

Becomes in terminology.md:
```markdown
- **Agent Mode** — The mode where Warp interprets your input as a request to an Agent (not a shell command).
  *Usage note:* Not "agent mode" or "Agent-mode."
```

Keep any existing definition from terminology.md. Only update the usage note / avoid guidance from Notion.

### Terminology section entries (glossary format)

These map directly — both use term + definition + usage note format. Align the wording with Notion.

## Category mapping

Map Notion headings to terminology.md `##` sections:

- "Capitalization and naming" → distribute terms to their matching category (Core product terms, Navigation and UI terms, etc.)
- "UI surface names" → Navigation and UI terms
- "Untraditional or branded terms" → Branded and informal terms
- "Hyphenation and phrasing" → Technical terms
- Direct category matches (e.g., "Oz terminology" → Oz terminology)

If a term doesn't clearly fit an existing category, place it in the most logical section and note the placement in the PR body.

## Schedule

Run weekly (Monday morning) or manually when terminology changes are expected.

## Troubleshooting

### Notion MCP auth failure
If the Notion MCP returns an auth error, report the failure and exit without making changes. Do not fall back to a cached version.

### Merge conflicts
If the branch has merge conflicts with `main`, rebase and resolve. Terminology entries are independent lines, so conflicts are rare.
