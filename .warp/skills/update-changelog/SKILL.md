---
name: update-changelog
description: Update the public changelog at docs.warp.dev/changelog with the latest stable release. Fetches changelog data from channel-versions, formats a new entry, and opens a PR. Use after a stable release ships (typically Fridays).
---

# Update Changelog

Adds a new entry to `src/content/docs/changelog/index.mdx` for the latest stable Warp release, then opens a PR.

## Related Skills

- `create_pr` - PR creation guidelines for this repo

## Workflow

### Step 1: Get the latest stable version

Fetch the current stable version from the public channel versions endpoint:

```bash
curl -s "https://releases.warp.dev/channel_versions.json" | python3 -c "
import sys, json
d = json.load(sys.stdin)
print(d['stable']['version'])
"
```

This returns the full version string, e.g. `v0.2026.02.18.08.22.stable_02`.

Parse it into components:
- **Full version**: `v0.2026.02.18.08.22.stable_02` (used to look up the changelog entry in channel-versions)
- **Base version**: `v0.2026.02.18.08.22` (strip everything after the last `.` that starts with a channel name: `stable`, `preview`, `dev`, `canary`, `beta`). The base version is the version without the `{channel}_{patch}` suffix.
- **Display date**: `2026.02.18` (extract `YYYY.MM.DD` from the base version, stripping the leading `v0.`)
- **Display version**: Same as base version (e.g. `v0.2026.02.18.08.22`)

### Step 2: Check if already documented

Read `src/content/docs/changelog/index.mdx` and search for the base version in existing `### ` header lines. If found, report that the changelog is already up to date and stop.

### Step 3: Fetch changelog data from `channel_versions.json` (primary source)

The authoritative source for changelog content is the `channel_versions.json` file in the `warpdotdev/channel-versions` repo. This file contains the final, human-reviewed changelog with all sections — New features, Improvements, Bug fixes, and oz_updates.

**IMPORTANT**: The docs changelog entry MUST match the content in `channel_versions.json` exactly — 1:1, no additions, removals, or rewording. Use `markdown_sections` values directly.

Fetch the stable changelog entry for the current version:

```bash
gh api repos/warpdotdev/channel-versions/contents/channel_versions.json \
  --jq '.content' | base64 -d | python3 -c "
import sys, json
d = json.load(sys.stdin)
entry = d['changelogs']['stable'].get('{full_version}')
if entry:
    print(json.dumps(entry, indent=2))
else:
    print('NOT_FOUND')
"
```

The entry has this structure:

```json
{
  "date": "2026-02-26T08:22:00+0000",
  "markdown_sections": [
    {"title": "New features", "markdown": "* item 1\n* item 2"},
    {"title": "Improvements", "markdown": "* item 1\n* item 2"},
    {"title": "Bug fixes", "markdown": "* item 1\n* item 2"}
  ],
  "sections": [],
  "oz_updates": ["markdown string 1"]
}
```

Key fields:
- `markdown_sections` — pre-formatted bullet lists for ALL sections: New features, Improvements, AND Bug fixes. Use these directly.
- `oz_updates` — optional. Oz-specific update entries. If present and non-empty, include as a separate **Oz updates** section (not merged into Improvements).
- `image_url` — optional. If present, include a `<figure>` element.

**Processing the markdown values**: The `markdown` values may have leading whitespace on lines after the first (e.g. ` * item`). Strip leading whitespace from each line so they become `* item`.

Ignore any `"Coming soon"` section — it's always empty and not used in the public changelog.

### Step 4: Fallback — fetch from GCS and warp-internal PRs

**Only use this step if Step 3 returns `NOT_FOUND`** (e.g. the channel-versions release PR hasn't merged yet).

If falling back, note in the PR description that the entry was generated from fallback sources and should be cross-checked against channel-versions once the release PR merges.

#### 4a. Fetch from GCS

Download the structured changelog from GCS:

```bash
curl -s "https://releases.warp.dev/stable/{full_version}/changelog.json"
```

This file may contain only New features and Improvements (no bug fixes). Use `markdown_sections` and `oz_updates` from it.

#### 4b. Fetch bug fixes from warp-internal PRs

Since the GCS file omits bug fixes, query merged PRs in warp-internal between the current and previous stable release tags.

**Find the previous stable release tag:**

```bash
gh release list --repo warpdotdev/warp-internal --limit 20 --json tagName --jq '.[].tagName' | grep '\.stable_'
```

Group by base version and take the two most recent distinct base versions. The **current** tag matches the version from Step 1; the **previous** tag is the next-oldest base version.

**Find PRs merged between the two tags:**

```bash
gh api "repos/warpdotdev/warp-internal/compare/{previous_tag}...{current_tag}" \
  --paginate --jq '.commits[].commit.message' | grep -oP '\(#\K\d+' | sort -un
```

**Extract CHANGELOG-BUG-FIX entries from PR bodies:**

```bash
gh pr view {pr_number} --repo warpdotdev/warp-internal --json body --jq '.body' | \
  grep -i '^CHANGELOG-BUG-FIX:' | sed -E 's/^[Cc][Hh][Aa][Nn][Gg][Ee][Ll][Oo][Gg]-[Bb][Uu][Gg]-[Ff][Ii][Xx]:[[:space:]]*//'
```

Collect all extracted bug fix entries. Also extract any `CHANGELOG-OZ:` entries the same way if not already covered by `oz_updates` in the JSON.

Strip the `{{text goes here...}}` placeholder template text — only include entries where the author filled in actual content. Deduplicate identical entries.

#### 4c. Review entries for sensitive content

Before including bug fix entries in the public changelog (docs.warp.dev/changelog), review each one for potentially sensitive information. **Do NOT include entries that reference**:
- Security vulnerabilities or exploits (e.g. "Fixed authentication bypass", "Fixed XSS in...")
- Internal infrastructure or architecture details not already public
- Customer-specific issues or data

For security-related fixes, either omit entirely or use a generic description (e.g. "Fixed a security issue" or "Stability and security improvements").

If you're unsure whether an entry is safe to publish, flag it in the PR description for human review.

### Step 5: Format the changelog entry

Build the entry matching the exact format used in `src/content/docs/changelog/index.mdx`. **Read the 2-3 most recent entries in the file** to confirm the current format before writing.

The standard format is:

```markdown
### {display_date} ({display_version})

**New features**

* Entry from markdown_sections
* Another entry

**Improvements**

* Entry from markdown_sections

**Bug fixes**

* Entry from markdown_sections

**Oz updates**

* Entry from oz_updates
```

Formatting rules:

1. **Header**: `### YYYY.MM.DD (vX.YYYY.MM.DD.HH.MM)` — use display_date and display_version from Step 1
2. **Section order**: New features → Improvements → Bug fixes → Oz updates
3. **Only include sections that have entries** — skip any section with no content
4. **Blank lines**: One blank line after the header, one blank line after each `**section title**`, one blank line between sections
5. **Bullet format**: Each entry is `* Entry text` (single asterisk, space, text)
6. **Image handling**: If `image_url` is present in changelog.json, insert a `<figure>` element on its own line after the `**New features**` header and blank line, before the bullet points:

```markdown
**New features**

<figure><img src="{image_url}" alt="description of the image"><figcaption></figcaption></figure>

* First bullet point
```

Reference the `2026.02.10` entry in the existing changelog for the exact `<figure>` format. Use a brief, descriptive alt text.

7. **Markdown from GCS**: The `markdown_sections[].markdown` values are already formatted as `* text\n* text` — use them directly. Split on newlines and include each line as-is.
8. **No trailing whitespace** on any lines.

### Step 6: Insert into the changelog file

Edit `src/content/docs/changelog/index.mdx`:
- Find the first line that starts with `### ` (this is the most recent existing entry)
- Insert the new entry **immediately before** that line
- Ensure there is exactly one blank line between the description paragraph ("Submit bugs and feature requests...") and the new entry's `### ` header
- Ensure there is exactly one blank line between the end of the new entry and the next `### ` header

### Step 7: Create branch, commit, and open PR

```bash
# Create a new branch
git checkout -b changelog/{base_version}

# Stage and commit
git add src/content/docs/changelog/index.mdx
git commit -m "docs: add changelog entry for {base_version}

Co-Authored-By: Oz <oz-agent@warp.dev>"

# Push and create PR
git push origin changelog/{base_version}
gh pr create \
  --title "docs: changelog {base_version}" \
  --body "Adds changelog entry for the {base_version} stable release.

Co-Authored-By: Oz <oz-agent@warp.dev>"
```

## Manual / Backfill Mode

If you need to add entries for a specific version (not necessarily the latest), the user will provide the full version string. Use that instead of fetching from `channel_versions.json` in Step 1, then proceed with Steps 2-7 as normal.

If `gh` access to channel-versions is unavailable, fall back to Step 4 (GCS + warp-internal PRs) and note in the PR description that the entry should be cross-checked against channel-versions.

## Example

For version `v0.2026.02.18.08.22.stable_02`:

1. Base version: `v0.2026.02.18.08.22`
2. Display date: `2026.02.18`
3. Display version: `v0.2026.02.18.08.22`
4. channel-versions key: `changelogs.stable["v0.2026.02.18.08.22.stable_02"]`
5. Header: `### 2026.02.18 (v0.2026.02.18.08.22)`
6. Branch: `changelog/v0.2026.02.18.08.22`
