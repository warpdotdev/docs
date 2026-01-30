#!/usr/bin/env python3
"""
Fix filename-style link display text and remove "mention" syntax.

This script:
1. Builds a mapping of file paths to H1 titles
2. Finds all links with .md in the display text
3. Replaces the filename with the proper title
4. Removes "mention" syntax from these links
"""

import os
import re
import argparse
from pathlib import Path
from typing import Optional

DOCS_ROOT = Path(__file__).parent.parent / 'docs'

# Pattern to match markdown links with .md in display text
# Captures: [filename.md](path "mention") or [filename.md](path)
LINK_PATTERN = re.compile(r'\[([^\]]*\.md)\]\(([^)\s]+)(\s*"mention")?\)')

# Pattern to extract H1 title from markdown
H1_PATTERN = re.compile(r'^#\s+(.+)$', re.MULTILINE)


def build_title_map():
    """Build a mapping of file paths to their H1 titles."""
    title_map = {}
    
    for root, dirs, files in os.walk(DOCS_ROOT):
        for file in files:
            if file.endswith('.md'):
                filepath = Path(root) / file
                rel_path = filepath.relative_to(DOCS_ROOT)
                
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    match = H1_PATTERN.search(content)
                    if match:
                        title = match.group(1).strip()
                        # Store with multiple key formats for easier lookup
                        title_map[str(rel_path)] = title
                        title_map[file] = title
                        # Also store without .md extension
                        if file.endswith('.md'):
                            title_map[file[:-3]] = title
                except Exception as e:
                    print(f"Warning: Could not read {filepath}: {e}")
    
    return title_map


def humanize_filename(filename: str) -> str:
    """Convert a filename to a human-readable title as fallback."""
    # Remove .md extension
    name = filename.replace('.md', '')
    # Replace hyphens with spaces and title case
    name = name.replace('-', ' ').replace('_', ' ')
    # Title case each word
    return ' '.join(word.capitalize() for word in name.split())


def resolve_link_path(source_file: Path, link_path: str) -> Optional[Path]:
    """Resolve a relative link path to an absolute path."""
    try:
        source_dir = source_file.parent
        resolved = (source_dir / link_path).resolve()
        return resolved
    except Exception:
        return None


def get_title_for_link(source_file: Path, link_path: str, title_map: dict) -> Optional[str]:
    """Get the proper title for a link."""
    # Try to resolve the path
    resolved = resolve_link_path(source_file, link_path)
    
    if resolved and resolved.exists():
        try:
            rel_to_docs = resolved.relative_to(DOCS_ROOT.resolve())
            
            # Look up in title map
            if str(rel_to_docs) in title_map:
                return title_map[str(rel_to_docs)]
            
            # Try just the filename
            filename = resolved.name
            if filename in title_map:
                return title_map[filename]
        except ValueError:
            pass
    
    # Fallback: humanize the filename from the link text
    return None


def process_file(filepath: Path, title_map: dict, dry_run: bool = True):
    """Process a single markdown file and fix link titles."""
    changes = []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = content
    
    for match in LINK_PATTERN.finditer(content):
        old_text = match.group(1)  # The display text (e.g., "file-tree.md")
        link_path = match.group(2)  # The path
        mention = match.group(3)  # " \"mention\"" or None
        
        # Get the proper title
        title = get_title_for_link(filepath, link_path, title_map)
        
        if title is None:
            # Fallback to humanizing the filename
            title = humanize_filename(old_text)
        
        # Build old and new link strings
        old_link = match.group(0)
        new_link = f"[{title}]({link_path})"
        
        if old_link != new_link:
            changes.append({
                'file': str(filepath.relative_to(DOCS_ROOT)),
                'old_text': old_text,
                'new_text': title,
                'had_mention': mention is not None
            })
            
            new_content = new_content.replace(old_link, new_link, 1)
    
    if changes and not dry_run:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
    
    return changes


def main():
    parser = argparse.ArgumentParser(description='Fix filename-style link display text')
    parser.add_argument('--dry-run', action='store_true', default=True,
                        help='Preview changes without modifying files (default: True)')
    parser.add_argument('--apply', action='store_true',
                        help='Actually apply the changes')
    args = parser.parse_args()
    
    dry_run = not args.apply
    
    if dry_run:
        print("DRY RUN - No files will be modified\n")
    else:
        print("APPLYING CHANGES\n")
    
    # Build title map
    print("Building title map...")
    title_map = build_title_map()
    print(f"Found {len(title_map)} title mappings\n")
    
    all_changes = []
    
    for root, dirs, files in os.walk(DOCS_ROOT):
        for file in files:
            if file.endswith('.md'):
                filepath = Path(root) / file
                changes = process_file(filepath, title_map, dry_run=dry_run)
                all_changes.extend(changes)
    
    # Print results grouped by file
    if all_changes:
        current_file = None
        for change in all_changes:
            if change['file'] != current_file:
                current_file = change['file']
                print(f"\n{current_file}:")
            
            mention_note = " (removed mention)" if change['had_mention'] else ""
            print(f"  [{change['old_text']}] → [{change['new_text']}]{mention_note}")
    
    print(f"\n{'Would fix' if dry_run else 'Fixed'} {len(all_changes)} links")
    
    if dry_run and all_changes:
        print("\nRun with --apply to make changes")


if __name__ == '__main__':
    main()
