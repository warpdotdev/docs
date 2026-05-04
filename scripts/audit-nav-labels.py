#!/usr/bin/env python3
"""Audit nav labels and sentence case across docs.

Compares GitBook SUMMARY.md nav labels against Astro frontmatter titles,
identifies pages that need sidebar.label overrides, and flags sentence case
issues in titles and existing labels.

Usage:
    python3 scripts/audit-nav-labels.py
"""

import os
import re
import sys
import yaml
from pathlib import Path
from typing import Dict, Optional

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

DOCS_REPO = Path(__file__).resolve().parent.parent
GITBOOK_REPO = Path.home() / "Documents" / "Warp" / "gitbook"
ASTRO_CONTENT = DOCS_REPO / "src" / "content" / "docs"

# GitBook spaces and their corresponding Astro prefixes
GITBOOK_SPACES = {
    "docs/warp": "",                    # maps to root-level dirs in Astro
    "docs/agent-platform": "agent-platform",
    "docs/reference": "reference",
    "docs/support-and-community": "support-and-community",
    "docs/enterprise": "enterprise",
    "docs/changelog": "changelog",
}

# Proper nouns that retain capitalization (from terminology.md)
# These are matched case-insensitively and restored to their canonical form.
PROPER_NOUNS = [
    # Multi-word first (order matters for replacement)
    "Agent Management Panel", "Agent Mode", "Agent Profiles",
    "Auto-detection Mode", "Terminal Mode", "Universal Input",
    "Warp Drive", "Admin Panel", "Command Palette",
    "Codebase Context", "Code Review", "Ambient Agents",
    "Slash Commands", "Environment Variables", "Environment Variable",
    "Cloud Agent Credits", "Add-on Credits",
    "Oz cloud agent", "Oz web app", "Oz dashboard",
    "Oz subagent", "Oz agent", "Oz conversation", "Oz run",
    "GitHub Actions", "GitHub App", "Claude Code",
    "AGPL v3", "Azure DevOps", "Windows Terminal", "VS Code",
    "Google Cloud",
    # Single-word proper nouns
    "Warp", "Oz", "Warpify", "Agent", "Agents", "Block", "Blocks",
    "Settings", "Rules", "Notebooks", "Notebook",
    "Workflows", "Workflow", "Prompts", "Prompt",
    "GitHub", "Linear", "Slack", "Codex", "Gemini", "OpenCode",
    "Git", "Vim", "Docker", "Kubernetes", "Vercel", "Figma",
    "Sentry", "Puppeteer", "Ollama", "Railway", "Bitbucket", "GitLab",
    # External product names (not in terminology.md but still proper nouns)
    "Linux", "Windows", "Chrome", "Cursor", "Ghostty", "iTerm2",
    "Postgres", "PostgreSQL", "Astro", "Tailwind", "React",
    "TypeScript", "JavaScript", "Slackbot", "DevOps",
    "Helm", "Stripe", "SQLite", "Amazon", "Context7",
    # Acronyms / always-caps
    "MCP", "SSH", "LSP", "CLI", "API", "SDK", "SSO", "FAQ", "FAQs",
    "UI", "URI", "GCP", "SQL", "PR", "PRs", "DNS", "CSS", "HTML",
    "JSON", "YAML", "AI", "LLM", "REPL", "YOLO",
    # Special casing
    "macOS", "D3.js", "gcloud",
]

# Build a lookup: lowercase -> canonical form
PROPER_NOUN_MAP = {}
for noun in PROPER_NOUNS:
    PROPER_NOUN_MAP[noun.lower()] = noun


# ---------------------------------------------------------------------------
# Parsing helpers
# ---------------------------------------------------------------------------

def parse_summary_md(path: Path) -> Dict[str, str]:
    """Parse a GitBook SUMMARY.md and return {relative_path: nav_label}.

    GitBook format:
        * [Link Text](path/to/file.md)           -> nav label = "Link Text"
        * [Link Text](path/to/file.md "Override") -> nav label = "Override"
    """
    entries = {}
    if not path.exists():
        return entries

    pattern = re.compile(
        r'\*\s+\[([^\]]+)\]'       # [Link Text]
        r'\(([^)"\s]+)'            # (path
        r'(?:\s+"([^"]+)")?'       # optional "Override"
        r'\)'                      # )
    )

    with open(path) as f:
        for line in f:
            m = pattern.search(line)
            if m:
                link_text = m.group(1).strip()
                file_path = m.group(2).strip()
                override = m.group(3)
                nav_label = override.strip() if override else link_text
                entries[file_path] = nav_label

    return entries


def gitbook_path_to_astro(gitbook_path: str, space_prefix: str) -> Optional[Path]:
    """Map a GitBook file path to an Astro MDX file path."""
    # README.md -> index.mdx
    if gitbook_path.endswith("README.md"):
        astro_path = gitbook_path.replace("README.md", "index.mdx")
    else:
        astro_path = gitbook_path.replace(".md", ".mdx")

    if space_prefix:
        full_path = ASTRO_CONTENT / space_prefix / astro_path
    else:
        full_path = ASTRO_CONTENT / astro_path

    if full_path.exists():
        return full_path

    # Try without the space prefix mapping for warp/ space which maps to
    # multiple top-level dirs
    if not space_prefix:
        # The warp space files map directly (terminal/, code/, etc.)
        return full_path if full_path.exists() else None

    return None


def extract_frontmatter(path: Path) -> dict:
    """Extract YAML frontmatter from an MDX file."""
    with open(path) as f:
        content = f.read()

    match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return {}

    try:
        return yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError:
        return {}


def to_sentence_case(text: str) -> str:
    """Convert text to sentence case, preserving proper nouns.

    Strategy: work word-by-word. For each word (or multi-word proper noun),
    check if it matches a known proper noun. If so, use the canonical form.
    Otherwise, lowercase it (except the very first word gets capitalized).
    """
    if not text:
        return text

    # Build a set of multi-word proper nouns for phrase matching
    sorted_nouns = sorted(PROPER_NOUNS, key=len, reverse=True)

    # Step 1: Protect proper nouns by replacing with indexed placeholders.
    # Use § markers that won't appear in real text.
    protected = []  # list of (placeholder, canonical)
    working = text

    for noun in sorted_nouns:
        pattern = re.compile(r'\b' + re.escape(noun) + r'\b', re.IGNORECASE)
        # Find all matches but only replace if the match is clean
        while True:
            m = pattern.search(working)
            if not m:
                break
            idx = len(protected)
            placeholder = f"§{idx}§"
            canonical = PROPER_NOUN_MAP[noun.lower()]
            protected.append((placeholder, canonical))
            working = working[:m.start()] + placeholder + working[m.end():]

    # Step 2: Apply sentence case to the remaining (non-proper-noun) text.
    # Split on placeholders to process only the plain-text segments.
    # Tokenize: split into segments of [text, placeholder, text, placeholder, ...]
    parts = re.split(r'(§\d+§)', working)

    first_alpha_done = False
    result_parts = []
    for part in parts:
        if re.match(r'^§\d+§$', part):
            # This is a placeholder — check if it's the first alphabetic content
            if not first_alpha_done:
                first_alpha_done = True
            result_parts.append(part)
        else:
            # Plain text — lowercase it
            lowered = part.lower()
            if not first_alpha_done:
                # Capitalize the first alpha char in the entire string
                chars = list(lowered)
                for i, ch in enumerate(chars):
                    if ch.isalpha():
                        chars[i] = ch.upper()
                        first_alpha_done = True
                        break
                lowered = ''.join(chars)
            result_parts.append(lowered)

    result = ''.join(result_parts)

    # Step 3: Restore proper nouns
    for placeholder, canonical in protected:
        result = result.replace(placeholder, canonical)

    return result


def has_sentence_case_issues(text: str) -> bool:
    """Check if text has sentence case issues."""
    if not text:
        return False
    corrected = to_sentence_case(text)
    return corrected != text


# ---------------------------------------------------------------------------
# Sidebar.ts label parsing
# ---------------------------------------------------------------------------

def parse_sidebar_ts_labels() -> Dict[str, str]:
    """Parse sidebar.ts to find { slug, label } overrides."""
    sidebar_path = DOCS_REPO / "src" / "sidebar.ts"
    labels = {}

    if not sidebar_path.exists():
        return labels

    with open(sidebar_path) as f:
        content = f.read()

    # Match patterns like: { slug: 'terminal/blocks', label: 'Overview' }
    pattern = re.compile(
        r"slug:\s*'([^']+)'\s*,\s*label:\s*'([^']+)'"
    )
    for m in pattern.finditer(content):
        labels[m.group(1)] = m.group(2)

    return labels


# ---------------------------------------------------------------------------
# Main audit
# ---------------------------------------------------------------------------

def run_audit():
    issues = []
    info_rows = []

    # Load sidebar.ts overrides
    sidebar_ts_labels = parse_sidebar_ts_labels()

    # Parse all GitBook SUMMARY.md files
    gitbook_nav: Dict[str, dict] = {}  # astro_path -> {gitbook_label, gitbook_space}

    for space, prefix in GITBOOK_SPACES.items():
        summary_path = GITBOOK_REPO / space / "SUMMARY.md"
        entries = parse_summary_md(summary_path)

        for gb_path, nav_label in entries.items():
            astro_path = gitbook_path_to_astro(gb_path, prefix)
            if astro_path:
                gitbook_nav[str(astro_path)] = {
                    "label": nav_label,
                    "space": space,
                }

    # Scan all Astro MDX files
    all_mdx = sorted(ASTRO_CONTENT.rglob("*.mdx"))

    for mdx_path in all_mdx:
        fm = extract_frontmatter(mdx_path)
        title = fm.get("title", "")
        sidebar = fm.get("sidebar", {}) or {}
        sidebar_label = sidebar.get("label", "") if isinstance(sidebar, dict) else ""

        # Determine the slug for sidebar.ts lookup
        rel = mdx_path.relative_to(ASTRO_CONTENT)
        slug = str(rel).replace("/index.mdx", "").replace(".mdx", "")
        if slug == "index":
            slug = "index"

        sidebar_ts_label = sidebar_ts_labels.get(slug, "")

        # Effective nav label (what actually shows in the sidebar)
        if sidebar_ts_label:
            effective_label = sidebar_ts_label
            label_source = "sidebar.ts"
        elif sidebar_label:
            effective_label = sidebar_label
            label_source = "frontmatter"
        else:
            effective_label = title
            label_source = "title (fallback)"

        # GitBook nav label
        gb_info = gitbook_nav.get(str(mdx_path))
        gb_label = gb_info["label"] if gb_info else ""

        rel_display = str(mdx_path.relative_to(DOCS_REPO))

        # Check 1: Missing nav label override (GitBook had shorter label)
        needs_label = False
        recommended_label = ""
        if gb_label and gb_label != title and label_source == "title (fallback)":
            # GitBook had a different (usually shorter) label than the current title
            needs_label = True
            recommended_label = gb_label

        # Check 2: Sentence case issues in title
        title_case_issue = has_sentence_case_issues(title)
        corrected_title = to_sentence_case(title) if title_case_issue else ""

        # Check 3: Sentence case issues in effective nav label
        label_case_issue = has_sentence_case_issues(effective_label)
        corrected_label = to_sentence_case(effective_label) if label_case_issue else ""

        has_any_issue = needs_label or title_case_issue or label_case_issue

        if has_any_issue:
            issue = {
                "file": rel_display,
                "title": title,
                "effective_label": effective_label,
                "label_source": label_source,
                "gb_label": gb_label,
                "needs_label": needs_label,
                "recommended_label": recommended_label,
                "title_case_issue": title_case_issue,
                "corrected_title": corrected_title,
                "label_case_issue": label_case_issue,
                "corrected_label": corrected_label,
            }
            issues.append(issue)

    # Print report
    print("=" * 80)
    print("NAV LABEL & SENTENCE CASE AUDIT REPORT")
    print("=" * 80)

    # Section 1: Missing nav label overrides
    missing = [i for i in issues if i["needs_label"]]
    print(f"\n## MISSING NAV LABELS ({len(missing)} pages)")
    print("These pages had shorter nav labels in GitBook that weren't migrated.\n")
    for i in missing:
        print(f"  {i['file']}")
        print(f"    Title (H1):        {i['title']}")
        print(f"    GitBook nav label: {i['gb_label']}")
        print(f"    → Add sidebar.label: \"{i['recommended_label']}\"")
        print()

    # Section 2: Sentence case issues in titles
    title_issues = [i for i in issues if i["title_case_issue"]]
    print(f"\n## TITLE SENTENCE CASE ISSUES ({len(title_issues)} pages)")
    print("These titles don't follow sentence case rules.\n")
    for i in title_issues:
        print(f"  {i['file']}")
        print(f"    Current:   {i['title']}")
        print(f"    Suggested: {i['corrected_title']}")
        print()

    # Section 3: Sentence case issues in nav labels
    label_issues = [i for i in issues if i["label_case_issue"]]
    print(f"\n## NAV LABEL SENTENCE CASE ISSUES ({len(label_issues)} pages)")
    print("These nav labels don't follow sentence case rules.\n")
    for i in label_issues:
        print(f"  {i['file']}")
        print(f"    Current ({i['label_source']}): {i['effective_label']}")
        print(f"    Suggested: {i['corrected_label']}")
        print()

    # Summary
    print("=" * 80)
    print("SUMMARY")
    print(f"  Missing nav labels:          {len(missing)}")
    print(f"  Title sentence case issues:  {len(title_issues)}")
    print(f"  Label sentence case issues:  {len(label_issues)}")
    print(f"  Total pages with issues:     {len(issues)}")
    print(f"  Total pages scanned:         {len(all_mdx)}")
    print("=" * 80)

    return len(issues)


if __name__ == "__main__":
    try:
        import yaml
    except ImportError:
        print("Installing PyYAML...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyyaml"])
        import yaml

    count = run_audit()
    sys.exit(0 if count == 0 else 1)
