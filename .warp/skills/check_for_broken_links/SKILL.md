---
name: check_for_broken_links
description: Check the Warp GitBook documentation for broken links by scanning source markdown files. Run the diagnostic script, review the output, fix broken links, and create a PR.
---

# Check for Broken Links

This skill checks the Warp GitBook documentation for broken links by scanning source markdown files directly.

## Running the Check

From the gitbook repo root:

```bash
python3 .warp/skills/check_for_broken_links/check_links.py
```

### Options

- `--internal-only`: Only check internal links (fast, no HTTP requests)
- `--external-only`: Only check external links
- `--timeout N`: HTTP timeout in seconds (default: 10)
- `--output FILE`: Save results to JSON file

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

docs/warp/code/code-overview.md:77
  Link: ../agents/slash-commands.md
  Error: File not found
  Suggestion: Try ../agent-platform/agent/slash-commands.md

### EXTERNAL (2 broken)

docs/warp/getting-started/what-is-warp.md:42
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
   - Fix the case to match the actual filename (GitBook is case-sensitive)

3. **Missing .md extension**: Directory link doesn't resolve
   - Add `.md` extension or ensure `README.md` exists in the directory

4. **Cross-space links**: Links between GitBook spaces (warp/, agent-platform/, etc.)
   - Verify the path correctly navigates between spaces using `../`

### External Links

1. **HTTP 404**: Page no longer exists
   - Find the new URL if the resource moved
   - Remove the link if the resource is gone
   - Consider linking to an archived version if appropriate

2. **Timeout/Connection Error**: Temporary issue or site blocking bots
   - Re-run the check to confirm it's persistent
   - Visit the URL manually to verify

### Adding Redirects

If content moved, you can add a redirect in the appropriate `.gitbook.yaml`:

```yaml
redirects:
    old/path/without/extension: new/path/to/file.md
```

## Creating a PR with Fixes

1. Create a branch: `git checkout -b fix/broken-links`
2. Fix the broken links identified by the script
3. Re-run the script to verify all fixes: `python3 .warp/skills/check_for_broken_links/check_links.py`
4. Commit and create a PR

## Dependencies

Requires Python 3.7+ with `requests`:

```bash
pip3 install requests
```

## Link Types Checked

- Markdown links: `[text](path/to/file.md)`
- Directory links: `[text](code-editor/)` → resolved to `README.md`
- Anchor links: `[text](file.md#section)` → file existence checked, anchor not validated
- External URLs: `[text](https://example.com)`
- GitBook embeds: `{% embed url="..." %}`
- Image references: `<img src="...">` and `![alt](path)`

## Limitations

- Anchor links (#section) are not validated for heading existence
- Some external sites block automated requests (Twitter, LinkedIn)
- GitBook-specific includes/partials are not followed
