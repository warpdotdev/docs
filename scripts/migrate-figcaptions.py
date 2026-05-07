#!/usr/bin/env python3
"""
Extract non-empty figcaptions from GitBook source and generate a report
of which Astro MDX images need <figure>+<figcaption> wrappers.

Usage:
    python3 scripts/migrate-figcaptions.py

Output:
    Prints a TSV report: astro_file, image_filename, caption_text
    Also prints summary stats.

The script matches GitBook figures to Astro images by image filename
(basename), since the directory structure differs between repos.
"""

import os
import re
import sys
from pathlib import Path
from collections import defaultdict

GITBOOK_ROOT = Path(os.path.expanduser("~/Documents/Warp/gitbook"))
ASTRO_CONTENT = Path(os.path.expanduser("~/Documents/Warp/docs/src/content/docs"))

# Pattern for GitBook's <figure><img ...><figcaption><p>text</p></figcaption></figure>
FIGURE_RE = re.compile(
    r'<figure>'
    r'.*?<img\s+src="([^"]+)"[^>]*>'
    r'.*?<figcaption>(?:<p>)?(.*?)(?:</p>)?</figcaption>'
    r'.*?</figure>',
    re.DOTALL
)

# Pattern for markdown images in Astro MDX: ![alt](path)
MD_IMAGE_RE = re.compile(r'!\[([^\]]*)\]\(([^)]+)\)')


def extract_gitbook_captions():
    """Extract all non-empty figcaptions from GitBook source."""
    captions = {}  # image_basename -> caption_text
    
    for md_file in GITBOOK_ROOT.rglob("*.md"):
        # Skip non-content files
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
            
            # Skip empty captions
            if not caption:
                continue
            
            # Strip any remaining HTML tags from caption
            caption = re.sub(r'<[^>]+>', '', caption).strip()
            if not caption:
                continue
            
            # Use image basename as the key
            basename = os.path.basename(img_src)
            captions[basename] = caption
    
    return captions


def find_astro_images():
    """Find all markdown images in Astro MDX files."""
    images = defaultdict(list)  # image_basename -> [(astro_file, line_num, full_line)]
    
    for mdx_file in ASTRO_CONTENT.rglob("*.mdx"):
        try:
            lines = mdx_file.read_text(encoding="utf-8").splitlines()
        except Exception:
            continue
        
        for i, line in enumerate(lines, 1):
            for match in MD_IMAGE_RE.finditer(line):
                img_path = match.group(2)
                basename = os.path.basename(img_path)
                rel_file = str(mdx_file.relative_to(ASTRO_CONTENT))
                images[basename].append((rel_file, i, line.strip()))
    
    return images


def main():
    print("Scanning GitBook source for figcaptions...", file=sys.stderr)
    captions = extract_gitbook_captions()
    print(f"  Found {len(captions)} non-empty figcaptions", file=sys.stderr)
    
    print("Scanning Astro MDX files for images...", file=sys.stderr)
    astro_images = find_astro_images()
    print(f"  Found {len(astro_images)} unique image filenames", file=sys.stderr)
    
    # Match captions to Astro images
    matched = 0
    unmatched_captions = []
    
    print("\n# Matched figcaptions (astro_file\tline\timage\tcaption)")
    print("# " + "=" * 80)
    
    for basename, caption in sorted(captions.items()):
        if basename in astro_images:
            for astro_file, line_num, _ in astro_images[basename]:
                print(f"{astro_file}\t{line_num}\t{basename}\t{caption}")
                matched += 1
        else:
            unmatched_captions.append((basename, caption))
    
    print(f"\n# Summary:", file=sys.stderr)
    print(f"#   Matched: {matched} images in Astro have captions to restore", file=sys.stderr)
    print(f"#   Unmatched: {len(unmatched_captions)} GitBook captions couldn't be matched to Astro images", file=sys.stderr)
    
    if unmatched_captions:
        print(f"\n# Unmatched captions (image may have been renamed or removed):", file=sys.stderr)
        for basename, caption in unmatched_captions[:20]:
            print(f"#   {basename}: {caption[:60]}...", file=sys.stderr)
        if len(unmatched_captions) > 20:
            print(f"#   ... and {len(unmatched_captions) - 20} more", file=sys.stderr)


if __name__ == "__main__":
    main()
