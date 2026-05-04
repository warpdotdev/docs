#!/usr/bin/env python3
"""Apply nav label fixes from curated audit-report.txt.

Parses the human-reviewed audit report and applies:
1. Missing nav labels (section 1) — adds sidebar.label to frontmatter
2. Nav label sentence case fixes (section 3) — adds/updates sidebar.label

Skips:
- Error pages in reference/api-and-sdk/troubleshooting/errors/
- sidebar.ts overrides (those entries are left as-is)

Usage:
    python3 scripts/apply-nav-labels.py          # dry run
    python3 scripts/apply-nav-labels.py --apply   # apply changes
"""

import re
import sys
from pathlib import Path

DOCS_REPO = Path(__file__).resolve().parent.parent
REPORT_PATH = DOCS_REPO / "scripts" / "audit-report.txt"
CONTENT_ROOT = DOCS_REPO / "src" / "content" / "docs"

# Skip error code pages (intentionally lowercase)
SKIP_PATTERNS = [
    "reference/api-and-sdk/troubleshooting/errors/",
]


def parse_report():
    """Parse the curated audit-report.txt into a dict of {file_path: label}."""
    changes = {}  # relative_path -> sidebar_label

    with open(REPORT_PATH) as f:
        content = f.read()

    # Section 1: MISSING NAV LABELS
    # Pattern: lines like '→ Add sidebar.label: "Some label"'
    # preceded by file path lines
    section1_match = re.search(
        r'## MISSING NAV LABELS.*?\n(.*?)(?=\n## TITLE SENTENCE CASE)',
        content, re.DOTALL
    )
    if section1_match:
        block = section1_match.group(1)
        # Parse file + label pairs
        entries = re.findall(
            r'^\s+(src/content/docs/\S+)\s*\n'
            r'.*?\n.*?\n'
            r'\s+→ Add sidebar\.label: "([^"]+)"',
            block, re.MULTILINE
        )
        for filepath, label in entries:
            if not any(skip in filepath for skip in SKIP_PATTERNS):
                changes[filepath] = label

    # Section 3: NAV LABEL SENTENCE CASE ISSUES
    # Pattern: file path, then "Current (source): ...", then "Suggested: ..."
    section3_match = re.search(
        r'## NAV LABEL SENTENCE CASE ISSUES.*?\n(.*?)(?=\n={5,})',
        content, re.DOTALL
    )
    if section3_match:
        block = section3_match.group(1)
        entries = re.findall(
            r'^\s+(src/content/docs/\S+)\s*\n'
            r'\s+Current \(([^)]+)\):.*?\n'
            r'\s+Suggested: (.+)',
            block, re.MULTILINE
        )
        for filepath, source, suggested in entries:
            suggested = suggested.strip()
            # Skip sidebar.ts entries (we don't modify sidebar.ts)
            if source == "sidebar.ts":
                continue
            # Skip error pages
            if any(skip in filepath for skip in SKIP_PATTERNS):
                continue
            # Don't overwrite section 1 entries (they were reviewed first)
            if filepath not in changes:
                changes[filepath] = suggested

    return changes


def apply_sidebar_label(mdx_path, label):
    """Add or update sidebar.label in an MDX file's frontmatter."""
    content = mdx_path.read_text()

    # Find frontmatter bounds
    fm_match = re.match(r'^(---\s*\n)(.*?\n)(---)', content, re.DOTALL)
    if not fm_match:
        return False

    fm_text = fm_match.group(2)
    fm_start = fm_match.start(2)
    fm_end = fm_match.end(2)

    # Case 1: sidebar.label already exists — update it
    # Use [ \t]* instead of \s* to avoid consuming newlines
    existing = re.search(
        r'^(\s+label:\s*)["\']?.*?["\']?[ \t]*$',
        fm_text, re.MULTILINE
    )
    if existing and 'sidebar:' in fm_text:
        new_fm = fm_text[:existing.start()] + f'  label: "{label}"' + fm_text[existing.end():]
        new_content = content[:fm_start] + new_fm + content[fm_end:]
        mdx_path.write_text(new_content)
        return True

    # Case 2: sidebar: block exists but no label
    sidebar_match = re.search(r'^sidebar:\s*$', fm_text, re.MULTILINE)
    if sidebar_match:
        insert_pos = sidebar_match.end()
        new_fm = fm_text[:insert_pos] + f'\n  label: "{label}"' + fm_text[insert_pos:]
        new_content = content[:fm_start] + new_fm + content[fm_end:]
        mdx_path.write_text(new_content)
        return True

    # Case 3: No sidebar block — add before closing ---
    new_fm = fm_text.rstrip('\n') + f'\nsidebar:\n  label: "{label}"\n'
    new_content = content[:fm_start] + new_fm + content[fm_end:]
    mdx_path.write_text(new_content)
    return True


def main():
    dry_run = "--apply" not in sys.argv

    if dry_run:
        print("DRY RUN — pass --apply to make changes\n")

    changes = parse_report()
    print(f"Found {len(changes)} nav label changes to apply.\n")

    applied = 0
    skipped = 0
    for rel_path, label in sorted(changes.items()):
        mdx_path = DOCS_REPO / rel_path
        if not mdx_path.exists():
            print(f"  SKIP (not found): {rel_path}")
            skipped += 1
            continue

        print(f"  {rel_path}")
        print(f"    sidebar.label: \"{label}\"")

        if not dry_run:
            if apply_sidebar_label(mdx_path, label):
                print(f"    ✓ applied")
                applied += 1
            else:
                print(f"    ⚠ failed (no frontmatter?)")
                skipped += 1
        else:
            applied += 1

        print()

    action = "Would apply" if dry_run else "Applied"
    print(f"\n{action}: {applied} | Skipped: {skipped}")


if __name__ == "__main__":
    main()
