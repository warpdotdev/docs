#!/usr/bin/env python3
"""
Apply <figure>+<figcaption> wrappers to Astro MDX images that had captions
in the GitBook source.

Usage:
    python3 scripts/apply-figcaptions.py          # dry run (preview changes)
    python3 scripts/apply-figcaptions.py --apply   # write changes to disk

Transforms:
    ![alt text](path/to/image.png)
  →
    <figure>
    ![alt text](path/to/image.png)
    <figcaption>Caption text from GitBook</figcaption>
    </figure>
"""

import os
import re
import sys
from pathlib import Path
from collections import defaultdict

GITBOOK_ROOT = Path(os.path.expanduser("~/Documents/Warp/gitbook"))
ASTRO_CONTENT = Path(os.path.expanduser("~/Documents/Warp/docs/src/content/docs"))

FIGURE_RE = re.compile(
    r'<figure>'
    r'.*?<img\s+src="([^"]+)"[^>]*>'
    r'.*?<figcaption>(?:<p>)?(.*?)(?:</p>)?</figcaption>'
    r'.*?</figure>',
    re.DOTALL
)

MD_IMAGE_RE = re.compile(r'^(\s*)(!\[[^\]]*\]\([^)]*?/([^/)"]+)\))\s*$')


def extract_gitbook_captions():
    """Extract all non-empty figcaptions from GitBook source."""
    captions = {}
    for md_file in GITBOOK_ROOT.rglob("*.md"):
        rel = str(md_file.relative_to(GITBOOK_ROOT))
        if rel.startswith(".") or "node_modules" in rel:
            continue
        try:
            content = md_file.read_text(encoding="utf-8")
        except Exception:
            continue
        for match in FIGURE_RE.finditer(content):
            img_src = match.group(1)
            caption = match.group(2).strip()
            if not caption:
                continue
            caption = re.sub(r'<[^>]+>', '', caption).strip()
            if not caption:
                continue
            basename = os.path.basename(img_src)
            captions[basename] = caption
    return captions


def apply_figcaptions(captions, dry_run=True):
    """Apply <figure>+<figcaption> wrappers to MDX files."""
    total_applied = 0
    files_modified = set()

    for mdx_file in sorted(ASTRO_CONTENT.rglob("*.mdx")):
        try:
            content = mdx_file.read_text(encoding="utf-8")
        except Exception:
            continue

        lines = content.splitlines(keepends=True)
        new_lines = []
        modified = False

        i = 0
        while i < len(lines):
            line = lines[i]
            match = MD_IMAGE_RE.match(line)

            if match:
                indent = match.group(1)
                full_image = match.group(2)
                img_basename = match.group(3)

                if img_basename in captions:
                    # Check if already wrapped in <figure>
                    prev_line = new_lines[-1].strip() if new_lines else ""
                    if "<figure>" in prev_line:
                        new_lines.append(line)
                        i += 1
                        continue

                    caption = captions[img_basename]
                    new_lines.append(f"{indent}<figure>\n")
                    new_lines.append(line)
                    new_lines.append(f"{indent}<figcaption>{caption}</figcaption>\n")
                    new_lines.append(f"{indent}</figure>\n")
                    modified = True
                    total_applied += 1
                    i += 1
                    continue

            new_lines.append(line)
            i += 1

        if modified:
            rel_file = str(mdx_file.relative_to(ASTRO_CONTENT))
            files_modified.add(rel_file)
            if dry_run:
                print(f"  Would modify: {rel_file}")
            else:
                mdx_file.write_text("".join(new_lines), encoding="utf-8")
                print(f"  Modified: {rel_file}")

    return total_applied, files_modified


def main():
    dry_run = "--apply" not in sys.argv

    if dry_run:
        print("DRY RUN — pass --apply to write changes\n")

    print("Extracting GitBook captions...")
    captions = extract_gitbook_captions()
    print(f"  Found {len(captions)} non-empty figcaptions\n")

    print("Applying figcaptions to Astro MDX files...")
    total, files = apply_figcaptions(captions, dry_run=dry_run)

    print(f"\n{'Would apply' if dry_run else 'Applied'} {total} figcaptions across {len(files)} files")

    if dry_run:
        print("\nRun with --apply to write changes to disk.")


if __name__ == "__main__":
    main()
