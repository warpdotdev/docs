---
name: check_for_broken_links
description: Check the Warp Astro Starlight documentation for broken links by scanning source markdown files. Run the diagnostic script, review the output, fix broken links, and optionally notify Slack.
---

# Check for Broken Links

This skill checks the Warp Astro Starlight documentation for broken links by scanning source markdown files directly. It can optionally send results to a Slack channel.

## Running the Check

From the docs repo root:

```bash
python3 .warp/skills/check_for_broken_links/check_links.py
```

### Options

- `--internal-only`: Only check internal links (fast, no HTTP requests)
- `--external-only`: Only check external links
- `--timeout N`: HTTP timeout in seconds (default: 10)
- `--output FILE`: Save results to JSON file
- `--slack-notify`: Send results to Slack (requires `SLACK_BOT_TOKEN` and `SLACK_CHANNEL_ID` env vars)
- `--slack-channel ID`: Override the default Slack channel

### Quick internal-only check:

```bash
python3 .warp/skills/check_for_broken_links/check_links.py --internal-only
```

## Output Format

The script outputs a report like:

```
=== BROKEN LINK REPORT ===
Files scanned: 174
Internal links checked: 800
External links checked: 360
Broken links found: 5

### INTERNAL (3 broken)

src/content/docs/code/code-overview.md:77
  Link: ../agents/slash-commands.md
  Error: File not found
  Suggestion: Try ../agent-platform/agent/slash-commands.md

### EXTERNAL (2 broken)

src/content/docs/getting-started/what-is-warp.md:42
  Link: https://example.com/old-page
  Error: HTTP 404
```

## Fixing Broken Links

After running the script, fix each broken link based on the error type:

### Internal Links

1. **File not found**: The target file doesn't exist
   - Check if the file was moved/renamed and update the path
   - If content was removed, remove the link or find an alternative
   - Check for typos in the path

2. **Case mismatch**: Path exists but with different casing
   - Fix the case to match the actual filename (Astro Starlight is case-sensitive)

3. **Missing .mdx extension**: Directory link doesn't resolve
   - Add `.mdx` extension or ensure `index.mdx` exists in the directory

4. **Cross-space links**: Links between Astro Starlight spaces (warp/, agent-platform/, support-and-community/, reference/)
   - **Relative paths do NOT work across spaces** — use absolute URLs instead
   - **IMPORTANT: `src/content/docs/` is the docs homepage, so "warp" is NOT included in URLs**
     - Files in `src/content/docs/code/code-review.mdx` → `https://docs.warp.dev/code/code-review`
     - Files in `src/content/docs/terminal/command-palette.mdx` → `https://docs.warp.dev/terminal/command-palette`
   - For other spaces, include the folder name in the URL:
     - Files in `src/content/docs/agent-platform/...` → `https://docs.warp.dev/agent-platform/...`
     - Files in `src/content/docs/support-and-community/...` → `https://docs.warp.dev/support-and-community/...`
   - Example cross-space link: From `agent-platform/` linking to `code/code-review.mdx`:
     - ❌ Wrong: `https://docs.warp.dev/warp/code/code-review`
     - ✅ Correct: `https://docs.warp.dev/code/code-review`
   - **Note**: Old folder names may be outdated (e.g., `support-and-billing` → `support-and-community/troubleshooting-and-support`). Search for the actual file location before constructing the URL.

### External Links

1. **HTTP 404**: Page no longer exists
   - Find the new URL if the resource moved
   - Remove the link if the resource is gone
   - Consider linking to an archived version if appropriate

2. **Timeout/Connection Error**: Temporary issue or site blocking bots
   - Re-run the check to confirm it's persistent
   - Visit the URL manually to verify

### Adding Redirects

If content moved, you can add a redirect in the appropriate `vercel.json (redirects)`:

```json
{
  "redirects": [
    { "source": "/old/path", "destination": "/new/path" }
  ]
}
```

## Creating a PR with Fixes

1. Create a branch: `git checkout -b fix/broken-links`
2. Fix the broken links identified by the script
3. Re-run the script to verify all fixes: `python3 .warp/skills/check_for_broken_links/check_links.py`
4. Commit and create a PR

## Slack Notifications

To send results to Slack (useful for CI/CD or ambient agents):

### Setup (one-time)

Create a Warp team secret for the Slack bot token:

```bash
warp secret create SLACK_BOT_TOKEN --team --description "Slack bot token for broken link reports"
```

You'll be prompted to enter the token securely. The token needs `chat:write` scope.

### Usage

```bash
python3 .warp/skills/check_for_broken_links/check_links.py --internal-only --slack-notify
```

For ambient agent runs, the `SLACK_BOT_TOKEN` secret is automatically injected as an environment variable.

### Custom channel

To post to a different channel:

```bash
python3 .warp/skills/check_for_broken_links/check_links.py --slack-notify --slack-channel YOUR_CHANNEL_ID
```

## Dependencies

Requires Python 3.7+ with `requests`:

```bash
pip3 install requests
```

## Link Types Checked

- Markdown links: `[text](path/to/file.md)`
- Directory links: `[text](code-editor/)` → resolved to `index.mdx`
- Anchor links: `[text](file.md#section)` → file existence checked, anchor not validated
- External URLs: `[text](https://example.com)`
- Video embeds: `<VideoEmbed url="..." />`
- Image references: `<img src="...">` and `![alt](path)`

## Limitations

- Anchor links (#section) are not validated for heading existence
- Some external sites block automated requests (Twitter, LinkedIn)
- Astro Starlight-specific includes/partials are not followed
