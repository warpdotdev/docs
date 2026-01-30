#!/usr/bin/env python3
"""
Convert cross-folder relative links to absolute URLs in GitBook docs.

Each top-level folder (documentation, platform, support-and-community, changelog, etc.)
is a separate GitBook space, so relative links between them don't work.
This script converts those relative links to absolute docs.warp.dev URLs.
"""

import os
import re
import argparse
from pathlib import Path

DOCS_ROOT = Path(__file__).parent.parent / 'docs'
BASE_URL = 'https://docs.warp.dev'

# Top-level folders that are separate GitBook spaces
TOP_LEVEL_FOLDERS = ['documentation', 'platform', 'support-and-community', 'enterprise', 'developers', 'changelog']

# URL mapping: folder -> URL prefix
# documentation maps to root, others keep their folder name
URL_MAPPING = {
    'documentation': '',  # maps to root
    'platform': '/platform',
    'support-and-community': '/support-and-community',
    'enterprise': '/enterprise',
    'developers': '/developers',
    'changelog': '/changelog',
}

# Pattern to match markdown links: [text](path) or [text](path "mention")
LINK_PATTERN = re.compile(r'(\[[^\]]*\]\()([^)\s]+)(\s*"[^"]*")?(\))')


def get_source_folder(filepath: Path) -> str:
    """Get the top-level folder for a file path relative to docs root."""
    rel_path = filepath.relative_to(DOCS_ROOT)
    return str(rel_path).split('/')[0]


def resolve_relative_path(source_file: Path, relative_link: str) -> tuple[str, str, str]:
    """
    Resolve a relative link to determine the target folder and path.
    
    Returns: (target_folder, resolved_path, anchor)
    """
    # Split anchor from path
    anchor = ''
    path = relative_link
    if '#' in path:
        path, anchor = path.split('#', 1)
        anchor = '#' + anchor
    
    # Handle the relative path
    source_dir = source_file.parent
    
    # Normalize the path by resolving .. and .
    try:
        if path:
            resolved = (source_dir / path).resolve()
            rel_to_docs = resolved.relative_to(DOCS_ROOT.resolve())
            parts = str(rel_to_docs).split('/')
            target_folder = parts[0]
            remaining_path = '/'.join(parts[1:]) if len(parts) > 1 else ''
            return target_folder, remaining_path, anchor
    except (ValueError, FileNotFoundError):
        pass
    
    return None, None, anchor


def convert_path_to_url(target_folder: str, path: str, anchor: str) -> str:
    """Convert a resolved path to an absolute URL."""
    if target_folder not in URL_MAPPING:
        return None
    
    base = URL_MAPPING[target_folder]
    
    # Clean up the path
    # Remove .md extension
    if path.endswith('.md'):
        path = path[:-3]
    
    # README becomes just the directory
    if path.endswith('/README') or path == 'README':
        path = path.rsplit('/README', 1)[0] if '/README' in path else ''
    
    # Build the URL
    if path:
        url = f"{BASE_URL}{base}/{path}"
    else:
        url = f"{BASE_URL}{base}" if base else BASE_URL
    
    # Add anchor
    url += anchor
    
    return url


def is_cross_folder_link(source_folder: str, link_path: str) -> bool:
    """Check if a link crosses folder boundaries."""
    # Must be a relative link with ..
    if not link_path.startswith('..'):
        return False
    
    # Check if it references another top-level folder
    for folder in TOP_LEVEL_FOLDERS:
        if f'/{folder}/' in link_path or f'../{folder}/' in link_path or f'../{folder}' in link_path:
            return folder != source_folder
    
    return False


def process_file(filepath: Path, dry_run: bool = True) -> list[dict]:
    """Process a single markdown file and convert cross-folder links."""
    changes = []
    source_folder = get_source_folder(filepath)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = content
    
    for match in LINK_PATTERN.finditer(content):
        prefix = match.group(1)  # [text](
        link_path = match.group(2)  # the path
        mention = match.group(3) or ''  # "mention" if present
        suffix = match.group(4)  # )
        
        # Skip non-relative links
        if link_path.startswith(('http://', 'https://', '#', 'mailto:')):
            continue
        
        # Skip image assets
        if '.gitbook/assets' in link_path:
            continue
        
        # Check if this is a cross-folder link
        if not is_cross_folder_link(source_folder, link_path):
            continue
        
        # Resolve the relative path
        target_folder, resolved_path, anchor = resolve_relative_path(filepath, link_path)
        
        if target_folder and target_folder in URL_MAPPING:
            # Convert to absolute URL
            new_url = convert_path_to_url(target_folder, resolved_path, anchor)
            
            if new_url:
                old_link = f"{prefix}{link_path}{mention}{suffix}"
                new_link = f"{prefix}{new_url}{mention}{suffix}"
                
                changes.append({
                    'file': str(filepath.relative_to(DOCS_ROOT)),
                    'old': link_path,
                    'new': new_url,
                    'mention': mention.strip() if mention else None
                })
                
                new_content = new_content.replace(old_link, new_link, 1)
    
    if changes and not dry_run:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
    
    return changes


def main():
    parser = argparse.ArgumentParser(description='Convert cross-folder relative links to absolute URLs')
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
    
    all_changes = []
    
    for root, dirs, files in os.walk(DOCS_ROOT):
        for file in files:
            if file.endswith('.md'):
                filepath = Path(root) / file
                changes = process_file(filepath, dry_run=dry_run)
                all_changes.extend(changes)
    
    # Print results grouped by file
    if all_changes:
        current_file = None
        for change in all_changes:
            if change['file'] != current_file:
                current_file = change['file']
                print(f"\n{current_file}:")
            
            mention_str = f' {change["mention"]}' if change['mention'] else ''
            print(f"  - {change['old']}")
            print(f"  + {change['new']}{mention_str}")
    
    print(f"\n{'Would convert' if dry_run else 'Converted'} {len(all_changes)} links")
    
    if dry_run and all_changes:
        print("\nRun with --apply to make changes")


if __name__ == '__main__':
    main()
