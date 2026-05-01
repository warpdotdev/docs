#!/usr/bin/env python3
"""Style lint for Warp Astro Starlight documentation.

Checks markdown files for formatting and terminology issues defined in the
AGENTS.md style guide. Supports scanning all files or only changed files,
optional auto-fix, PR creation, and Slack notifications.

Usage:
    python3 style_lint.py [--all|--changed] [--fix] [--create-pr] [--output FILE]
                          [--slack-notify] [--slack-channel ID]
"""

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Tuple

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

DOCS_ROOT = Path("docs")
CHANGELOG_DIR = DOCS_ROOT / "changelog"
EXCLUDED_DIRS = {"_book", "node_modules", ".docs"}

# Feature names that are correctly Title Case (exceptions to sentence-case rule)
PROPER_FEATURE_NAMES = {
    "Admin Panel", "Agent Management Panel", "Agent Mode", "Agent Profiles",
    "Ambient Agents", "Auto-detection Mode", "Cloud Agent Credits",
    "Codebase Context", "Code Review", "Command Palette", "Global Rules",
    "Oz CLI", "Oz Platform", "Project Rules", "Slash Commands",
    "Terminal Mode", "Universal Input", "Warp Drive", "Warp Platform",
}

# Terminology: wrong → right (case-sensitive checks)
PRODUCT_CASING = {
    "Warp Terminal": ("Warp", "Use 'Warp' unless specifically distinguishing from Oz"),
    "agent mode": ("Agent Mode", "Capitalize as a feature name"),
    "agent management panel": ("Agent Management Panel", "Capitalize as a UI surface name"),
    "warp drive": ("Warp Drive", "Capitalize as a feature name"),
    "codebase context": ("Codebase Context", "Capitalize as a feature name"),
    "command palette": ("Command Palette", "Capitalize as a feature name"),
    "admin panel": ("Admin Panel", "Capitalize as a feature name"),
}

# External product names (case-sensitive)
EXTERNAL_CASING = {
    "Github": ("GitHub", "Capitalize the H"),
    "github actions": ("GitHub Actions", "Capitalize both words"),
    "MacOS": ("macOS", "Lowercase m"),
    "Mac OS": ("macOS", "Use 'macOS'"),
    "A.I.": ("AI", "Use 'AI' not 'A.I.'"),
}

# Deprecated terminology (case-insensitive)
DEPRECATED_TERMS = [
    (r"\bwhitelist\b", "Use 'allowlist'"),
    (r"\bblacklist\b", "Use 'denylist'"),
    (r"\bblocklist\b", "Use 'denylist'"),
]

# Oz terms to avoid (case-insensitive patterns)
OZ_TERMS_TO_AVOID = [
    (r"\bOzzies\b", "Use 'Oz agents', 'instances', or 'Oz subagents'"),
    (r"\bDeploying an Oz\b", "Use 'Deploying an Oz agent'"),
    (r"\bThe Oz Agent\b", "Use 'An Oz agent' or 'A parent Oz agent'"),
    (r"\bOz is running\b", "Use 'An Oz agent is running' or 'A run is in progress'"),
    (r"\bAI agents?\b", "Use 'agents' (the 'AI' prefix is redundant)"),
]

# Action verbs that precede UI elements (should be bold, not backtick)
UI_ACTION_VERBS = r"(?:click|select|toggle|enable|disable|choose|check|uncheck|expand|collapse|open|close|tap)"

DEFAULT_SLACK_CHANNEL = os.environ.get("SLACK_CHANNEL_ID", "")

TERMINOLOGY_FILE = Path(".warp/references/terminology.md")

# Common bolded words that are NOT product terms (false positive suppression)
COMMON_BOLD_WORDS = {
    # General emphasis words
    "Note", "Important", "Warning", "Example", "Examples", "Step", "Steps",
    "Tip", "Tips", "Required", "Optional", "Default", "Summary", "Overview",
    "Prerequisites", "Prerequisite", "Result", "Results", "Outcome",
    "Next", "Previous", "See", "Related", "Key", "Keys", "Value", "Values",
    "True", "False", "Yes", "No", "None", "All", "Any", "New", "Old",
    "Name", "Type", "Description", "Status", "Action", "Actions",
    "Bold", "Italic", "What", "Why", "How", "When", "Where", "Who",
    "Good", "Bad", "Do", "Don't", "Use", "Avoid", "Before", "After",
    "Phase", "Option", "Options", "Feature", "Features", "Setup",
    "Structure", "Rules", "Template", "Existing", "Heading",
    "IMPORTANT", "PHASE", "COMPLETED",
    # UI labels and status words commonly bolded in docs
    "Start", "Stop", "Save", "Cancel", "Delete", "Edit", "Add", "Remove",
    "Enable", "Disable", "Create", "Update", "Submit", "Apply", "Confirm",
    "Back", "Done", "Close", "Open", "Run", "Test", "Copy", "Paste",
    "Personal", "Global", "Team", "Custom", "Manage", "View", "Preview",
    "Active", "Inactive", "Enabled", "Disabled", "Experimental", "Beta",
    "Failed", "Success", "Error", "Pending", "Complete", "Completed",
    "General", "Advanced", "Basic", "Pro", "Free", "Enterprise",
    "Configuration", "Preferences", "References", "Visibility",
    "Execution", "Task", "Steer", "Templates", "Knowledge",
    "Docker", "Sentry", "Puppeteer",  # Third-party tools commonly mentioned
}


@dataclass
class Issue:
    file: str
    line: int
    check: str
    message: str
    severity: str  # "error" or "warning"
    fixable: bool = False
    fix_from: str = ""
    fix_to: str = ""


@dataclass
class Report:
    files_scanned: int = 0
    issues: List[Issue] = field(default_factory=list)
    fixes_applied: int = 0


# ---------------------------------------------------------------------------
# File discovery
# ---------------------------------------------------------------------------

def find_all_md_files() -> List[Path]:
    """Find all markdown files in docs/, excluding build artifacts and changelog."""
    files = []
    for f in DOCS_ROOT.rglob("*.md"):
        if any(part in EXCLUDED_DIRS for part in f.parts):
            continue
        # Exclude changelog (historical record)
        if f.is_relative_to(CHANGELOG_DIR):
            continue
        files.append(f)
    return sorted(files)


def find_changed_md_files() -> List[Path]:
    """Find markdown files changed in the current branch vs main."""
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", "origin/main...HEAD", "--", "docs/"],
            capture_output=True, text=True, check=True,
        )
        files = []
        for line in result.stdout.strip().split("\n"):
            if line.endswith(".md") and os.path.exists(line):
                p = Path(line)
                if not any(part in EXCLUDED_DIRS for part in p.parts):
                    files.append(p)
        return sorted(files)
    except subprocess.CalledProcessError:
        print("Warning: could not determine changed files. Falling back to --all.")
        return find_all_md_files()


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------

def check_frontmatter(content: str, filepath: str) -> List[Issue]:
    """Check for missing or empty frontmatter description."""
    issues = []
    if not content.startswith("---"):
        issues.append(Issue(filepath, 1, "frontmatter", "Missing YAML frontmatter", "error"))
        return issues
    end = content.find("---", 3)
    if end == -1:
        issues.append(Issue(filepath, 1, "frontmatter", "Malformed YAML frontmatter (no closing ---)", "error"))
        return issues
    fm = content[3:end]
    if "description:" not in fm:
        issues.append(Issue(filepath, 1, "frontmatter", "Frontmatter missing 'description' field", "error"))
    return issues


def check_settings_paths(lines: List[str], filepath: str) -> List[Issue]:
    """Detect backtick-wrapped Settings paths that should be bold per-segment."""
    issues = []
    pattern = re.compile(r"`(Settings\s*>\s*[^`]+)`")
    for i, line in enumerate(lines, 1):
        for m in pattern.finditer(line):
            original = m.group(0)
            inner = m.group(1)
            # Build the bold version
            segments = [s.strip() for s in inner.split(">")]
            bold_version = " > ".join(f"**{s}**" for s in segments)
            issues.append(Issue(
                filepath, i, "settings-path",
                f"Settings path in backticks: {original} → {bold_version}",
                "warning", fixable=True, fix_from=original, fix_to=bold_version,
            ))
    return issues


def check_ui_element_backticks(lines: List[str], filepath: str) -> List[Issue]:
    """Detect UI elements in backticks after action verbs (should be bold)."""
    issues = []
    pattern = re.compile(
        rf"(?:^|\s){UI_ACTION_VERBS}(?:\s+(?:on|the))?\s+`([^`]+)`",
        re.IGNORECASE,
    )
    for i, line in enumerate(lines, 1):
        for m in pattern.finditer(line):
            backtick_text = m.group(1)
            # Skip things that look like code (paths, flags, CamelCase identifiers)
            if "/" in backtick_text or backtick_text.startswith("-") or backtick_text.startswith("$"):
                continue
            issues.append(Issue(
                filepath, i, "ui-backtick",
                f"UI element in backticks after action verb: `{backtick_text}` → **{backtick_text}**",
                "warning", fixable=True,
                fix_from=f"`{backtick_text}`", fix_to=f"**{backtick_text}**",
            ))
    return issues


def _to_sentence_case(text: str) -> str:
    """Convert header text to sentence case, preserving proper feature names and acronyms."""
    skip_words = {"I", "A", "API", "CLI", "SDK", "SSH", "UI", "URL", "PR", "CI", "CD"}
    words = text.split()

    # Mark word positions that are part of a complete proper feature name match.
    # Only protect words when the full multi-word name appears as a sequence.
    protected = [False] * len(words)
    for fn in PROPER_FEATURE_NAMES:
        fn_words = fn.split()
        for start in range(len(words) - len(fn_words) + 1):
            if all(words[start + j].lower() == fn_words[j].lower() for j in range(len(fn_words))):
                for j in range(len(fn_words)):
                    protected[start + j] = True

    result = []
    for idx, w in enumerate(words):
        if idx == 0 or protected[idx]:
            result.append(w)
            continue
        clean = re.sub(r"[^a-zA-Z]", "", w)
        if not clean or clean in skip_words or len(clean) <= 1:
            result.append(w)
            continue
        # Preserve all-caps words (acronyms not in skip_words)
        if clean.isupper() and len(clean) > 1:
            result.append(w)
            continue
        # Lowercase the word
        result.append(w.lower())
    return " ".join(result)


def check_header_case(lines: List[str], filepath: str) -> List[Issue]:
    """Detect Title Case in H2-H4 headers (should be sentence case)."""
    issues = []
    header_pattern = re.compile(r"^(#{2,4})\s+(.+)$")
    for i, line in enumerate(lines, 1):
        m = header_pattern.match(line)
        if not m:
            continue
        hashes = m.group(1)
        text = m.group(2).strip()
        words = text.split()
        if len(words) < 2:
            continue
        # Count capitalized non-first words (excluding proper feature names, short words)
        skip_words = {"I", "A", "API", "CLI", "SDK", "SSH", "UI", "URL", "PR", "CI", "CD"}
        title_case_count = 0
        for w in words[1:]:
            clean = re.sub(r"[^a-zA-Z]", "", w)
            if not clean or clean in skip_words or len(clean) <= 2:
                continue
            # Check if it's part of a known feature name
            is_feature_name = any(clean in fn for fn in PROPER_FEATURE_NAMES)
            if is_feature_name:
                continue
            if clean[0].isupper() and clean[1:].islower():
                title_case_count += 1
        if title_case_count >= 2:
            fixed_text = _to_sentence_case(text)
            original_line = f"{hashes} {text}"
            fixed_line = f"{hashes} {fixed_text}"
            issues.append(Issue(
                filepath, i, "header-case",
                f"Possible Title Case header (should be sentence case): \"{text}\" → \"{fixed_text}\"",
                "warning", fixable=True, fix_from=original_line, fix_to=fixed_line,
            ))
    return issues


def check_image_alt_text(lines: List[str], filepath: str) -> List[Issue]:
    """Detect images without alt text or with generic alt text."""
    issues = []
    img_pattern = re.compile(r'<img\s[^>]*alt="([^"]*)"', re.IGNORECASE)
    img_no_alt = re.compile(r"<img\s(?:(?!alt=)[^>])*>", re.IGNORECASE)
    generic_alts = {"screenshot", "image", "screen", "pic", "photo", ""}

    for i, line in enumerate(lines, 1):
        for m in img_pattern.finditer(line):
            alt = m.group(1).strip().lower()
            if alt in generic_alts:
                issues.append(Issue(
                    filepath, i, "alt-text",
                    f"Generic or empty alt text: alt=\"{m.group(1)}\"",
                    "warning",
                ))
        for m in img_no_alt.finditer(line):
            if "alt=" not in m.group(0).lower():
                issues.append(Issue(
                    filepath, i, "alt-text",
                    "Image tag missing alt attribute",
                    "warning",
                ))
    return issues


def check_callout_syntax(lines: List[str], filepath: str) -> List[Issue]:
    """Check for malformed hint/callout syntax."""
    issues = []
    valid_styles = {"info", "warning", "danger", "success"}
    hint_open = re.compile(r'{%\s*hint\s+style="([^"]*)"')
    hint_close = re.compile(r"{%\s*endhint\s*%}")

    open_count = 0
    for i, line in enumerate(lines, 1):
        for m in hint_open.finditer(line):
            style = m.group(1)
            if style not in valid_styles:
                issues.append(Issue(
                    filepath, i, "callout",
                    f"Invalid hint style: \"{style}\". Valid styles: {', '.join(sorted(valid_styles))}",
                    "error",
                ))
            open_count += 1
        for _ in hint_close.finditer(line):
            open_count -= 1

    if open_count > 0:
        issues.append(Issue(
            filepath, len(lines), "callout",
            f"{open_count} unclosed {{%% hint %%}} tag(s) — missing {{%% endhint %%}}",
            "error",
        ))
    return issues


def check_product_casing(lines: List[str], filepath: str) -> List[Issue]:
    """Check for incorrect product name casing."""
    issues = []
    for i, line in enumerate(lines, 1):
        # Skip code blocks
        if line.strip().startswith("```") or line.strip().startswith("`"):
            continue
        for wrong, (right, note) in PRODUCT_CASING.items():
            # Case-sensitive search
            idx = line.find(wrong)
            while idx != -1:
                issues.append(Issue(
                    filepath, i, "product-casing",
                    f"\"{wrong}\" → \"{right}\" ({note})",
                    "warning", fixable=True, fix_from=wrong, fix_to=right,
                ))
                idx = line.find(wrong, idx + len(wrong))

        for wrong, (right, note) in EXTERNAL_CASING.items():
            idx = line.find(wrong)
            while idx != -1:
                issues.append(Issue(
                    filepath, i, "external-casing",
                    f"\"{wrong}\" → \"{right}\" ({note})",
                    "warning", fixable=True, fix_from=wrong, fix_to=right,
                ))
                idx = line.find(wrong, idx + len(wrong))
    return issues


def check_oz_terms(lines: List[str], filepath: str) -> List[Issue]:
    """Check for Oz terms to avoid."""
    issues = []
    for i, line in enumerate(lines, 1):
        if line.strip().startswith("```") or line.strip().startswith("`"):
            continue
        for pattern, suggestion in OZ_TERMS_TO_AVOID:
            for m in re.finditer(pattern, line, re.IGNORECASE):
                issues.append(Issue(
                    filepath, i, "oz-term",
                    f"Avoid \"{m.group(0)}\" → {suggestion}",
                    "warning",
                ))
    return issues


def check_deprecated_terms(lines: List[str], filepath: str) -> List[Issue]:
    """Check for deprecated terminology (whitelist/blacklist/blocklist)."""
    issues = []
    for i, line in enumerate(lines, 1):
        if line.strip().startswith("```") or line.strip().startswith("`"):
            continue
        for pattern, suggestion in DEPRECATED_TERMS:
            for m in re.finditer(pattern, line, re.IGNORECASE):
                issues.append(Issue(
                    filepath, i, "deprecated-term",
                    f"Avoid \"{m.group(0)}\" → {suggestion}",
                    "warning",
                ))
    return issues


def load_glossary_terms() -> set:
    """Load known term names from terminology.md."""
    terms = set()
    if not TERMINOLOGY_FILE.exists():
        return terms
    content = TERMINOLOGY_FILE.read_text(encoding="utf-8")
    # Match bolded terms: - **Term** or - **Term** / **Variant**
    for m in re.finditer(r"- \*\*([^*]+)\*\*", content):
        raw = m.group(1)
        # Handle "Term / Variant" entries
        for part in raw.split("/"):
            terms.add(part.strip())
    # Also add proper feature names
    terms.update(PROPER_FEATURE_NAMES)
    return terms


def check_unrecognized_terms(lines: List[str], filepath: str, glossary: set) -> List[Issue]:
    """Flag bolded terms that look like product names but aren't in the glossary.

    Reports as warnings — these are candidates for glossary addition, not errors.
    Only flags short, Title-Case terms that resemble product or feature names.
    """
    issues = []
    if not glossary:
        return issues

    bold_pattern = re.compile(r"\*\*([^*]+)\*\*")
    in_code_block = False
    seen_terms: set = set()  # Deduplicate within a file

    for i, line in enumerate(lines, 1):
        # Track code block boundaries
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue

        # Skip list-format definitions (bold term + dash/colon pattern)
        # e.g., "- **Term** — definition" or "**Term**: description"
        if re.match(r"\s*[-*]\s+\*\*", line) and ("—" in line or ": " in line.split("**")[-1][:5] if "**" in line else False):
            continue

        for m in bold_pattern.finditer(line):
            term = m.group(1).strip()

            # --- Strict filters to only catch product/feature names ---

            # Skip if already seen in this file
            if term in seen_terms:
                continue

            # Skip common false positives
            if term in COMMON_BOLD_WORDS:
                continue

            # Max 3 words — product names are short
            words = term.split()
            if len(words) > 3:
                continue

            # Must be Title Case or specific casing pattern (not sentence-case phrases)
            # At least the first word must be capitalized, and for multi-word terms
            # at least 2 words should be capitalized
            if len(words) == 1:
                # Single word: must start uppercase and not be all-caps (acronym)
                if not words[0][0].isupper() or (words[0].isupper() and len(words[0]) <= 5):
                    continue
            else:
                # Multi-word: need at least 2 capitalized words (Title Case signal)
                cap_count = sum(1 for w in words if w[0].isupper() and len(w) > 1)
                if cap_count < 2:
                    continue

            # Skip very short terms
            if len(term) < 3:
                continue

            # Skip things that look like code (paths, flags, camelCase)
            if "/" in term or term.startswith("-") or term.startswith("$"):
                continue
            if re.match(r"^[a-z]+[A-Z]", term):  # camelCase
                continue

            # Skip terms containing punctuation that product names don't have
            if any(c in term for c in ".,;:!?()[]{}\"'"):
                continue

            # Skip UI action patterns ("Click **Save**" — Save is a button, not a term)
            prefix = line[:m.start()].rstrip()
            if re.search(rf"{UI_ACTION_VERBS}\s*$", prefix, re.IGNORECASE):
                continue

            # Check against glossary
            if term not in glossary:
                seen_terms.add(term)
                issues.append(Issue(
                    filepath, i, "unrecognized-term",
                    f"Bolded term not in glossary: \"{term}\" — consider adding to terminology.md",
                    "warning",
                ))
    return issues


# Cache glossary terms once at module level
_glossary_cache: Optional[set] = None

def _get_glossary() -> set:
    global _glossary_cache
    if _glossary_cache is None:
        _glossary_cache = load_glossary_terms()
    return _glossary_cache


def run_all_checks(filepath: Path) -> List[Issue]:
    """Run all checks on a single file."""
    content = filepath.read_text(encoding="utf-8")
    lines = content.split("\n")

    issues = []
    issues.extend(check_frontmatter(content, str(filepath)))
    issues.extend(check_settings_paths(lines, str(filepath)))
    issues.extend(check_ui_element_backticks(lines, str(filepath)))
    issues.extend(check_header_case(lines, str(filepath)))
    issues.extend(check_image_alt_text(lines, str(filepath)))
    issues.extend(check_callout_syntax(lines, str(filepath)))
    issues.extend(check_product_casing(lines, str(filepath)))
    issues.extend(check_oz_terms(lines, str(filepath)))
    issues.extend(check_deprecated_terms(lines, str(filepath)))
    issues.extend(check_unrecognized_terms(lines, str(filepath), _get_glossary()))
    return issues


# ---------------------------------------------------------------------------
# Fix
# ---------------------------------------------------------------------------

def apply_fixes(filepath: Path, issues: List[Issue]) -> int:
    """Apply fixable issues to a file. Returns count of fixes applied."""
    fixable = [i for i in issues if i.fixable and i.fix_from and i.fix_to]
    if not fixable:
        return 0

    content = filepath.read_text(encoding="utf-8")
    count = 0
    for issue in fixable:
        if issue.fix_from in content:
            content = content.replace(issue.fix_from, issue.fix_to, 1)
            count += 1

    if count > 0:
        filepath.write_text(content, encoding="utf-8")
    return count


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

def print_report(report: Report) -> None:
    """Print human-readable report to stdout."""
    print(f"\n=== STYLE LINT REPORT ===")
    print(f"Files scanned: {report.files_scanned}")
    print(f"Issues found: {len(report.issues)}")
    if report.fixes_applied > 0:
        print(f"Fixes applied: {report.fixes_applied}")

    if not report.issues:
        print("\n✅ No issues found.")
        return

    # Group by check type
    by_check: dict = {}
    for issue in report.issues:
        by_check.setdefault(issue.check, []).append(issue)

    for check, issues in sorted(by_check.items()):
        print(f"\n### {check.upper()} ({len(issues)} found)")
        for issue in issues[:20]:  # Cap display at 20 per category
            marker = "⚠️" if issue.severity == "warning" else "❌"
            print(f"  {marker} {issue.file}:{issue.line}")
            print(f"     {issue.message}")
        if len(issues) > 20:
            print(f"  ... and {len(issues) - 20} more")


def save_json(report: Report, output_path: str) -> None:
    """Save report as JSON."""
    data = {
        "files_scanned": report.files_scanned,
        "total_issues": len(report.issues),
        "fixes_applied": report.fixes_applied,
        "issues": [
            {
                "file": i.file, "line": i.line, "check": i.check,
                "message": i.message, "severity": i.severity, "fixable": i.fixable,
            }
            for i in report.issues
        ],
    }
    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"\nResults saved to {output_path}")


def send_slack(report: Report, channel: str) -> None:
    """Send report summary to Slack."""
    token = os.environ.get("SLACK_BOT_TOKEN")
    if not token:
        print("Warning: SLACK_BOT_TOKEN not set, skipping Slack notification.")
        return
    if not report.issues:
        return  # Don't notify on clean runs

    try:
        import requests
    except ImportError:
        print("Warning: 'requests' not installed, skipping Slack notification.")
        return

    by_check: dict = {}
    for issue in report.issues:
        by_check.setdefault(issue.check, []).append(issue)

    lines = [f"*Style Lint Report* — {len(report.issues)} issues in {report.files_scanned} files"]
    for check, issues in sorted(by_check.items()):
        lines.append(f"• *{check}*: {len(issues)}")

    text = "\n".join(lines)
    resp = requests.post(
        "https://slack.com/api/chat.postMessage",
        headers={"Authorization": f"Bearer {token}"},
        json={"channel": channel, "text": text},
    )
    if resp.ok and resp.json().get("ok"):
        print(f"Slack notification sent to {channel}")
    else:
        print(f"Warning: Slack notification failed: {resp.text}")


def create_pr_with_fixes() -> None:
    """Create a branch and PR with the auto-fixes."""
    branch = "fix/style-lint-auto-fixes"
    subprocess.run(["git", "checkout", "-b", branch], check=True)
    subprocess.run(["git", "add", "docs/"], check=True)
    result = subprocess.run(["git", "diff", "--cached", "--quiet"])
    if result.returncode == 0:
        print("No changes to commit.")
        return
    subprocess.run([
        "git", "commit", "-m",
        "docs: auto-fix style lint issues\n\nCo-Authored-By: Oz <oz-agent@warp.dev>",
    ], check=True)
    subprocess.run(["git", "push", "origin", branch], check=True)
    subprocess.run([
        "gh", "pr", "create",
        "--title", "docs: auto-fix style lint issues",
        "--body", "Automated fixes from `style_lint.py --fix`.\n\nCo-Authored-By: Oz <oz-agent@warp.dev>",
    ], check=True)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Style lint for Warp Astro Starlight docs")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--all", action="store_true", default=True, help="Scan all docs (default)")
    mode.add_argument("--changed", action="store_true", help="Scan only changed files")
    parser.add_argument("--fix", action="store_true", help="Auto-fix high-confidence issues")
    parser.add_argument("--create-pr", action="store_true", help="Create PR with fixes")
    parser.add_argument("--output", type=str, help="Save JSON report to file")
    parser.add_argument("--slack-notify", action="store_true", help="Send results to Slack")
    parser.add_argument("--slack-channel", type=str, default=DEFAULT_SLACK_CHANNEL)
    args = parser.parse_args()

    if args.create_pr:
        args.fix = True

    # Discover files
    files = find_changed_md_files() if args.changed else find_all_md_files()
    report = Report(files_scanned=len(files))

    # Run checks
    for filepath in files:
        issues = run_all_checks(filepath)
        if args.fix:
            fixed = apply_fixes(filepath, issues)
            report.fixes_applied += fixed
            # Re-check after fixes to get remaining issues
            issues = run_all_checks(filepath)
        report.issues.extend(issues)

    # Output
    print_report(report)
    if args.output:
        save_json(report, args.output)
    if args.slack_notify:
        send_slack(report, args.slack_channel)
    if args.create_pr and report.fixes_applied > 0:
        create_pr_with_fixes()

    # Exit code: 1 if errors found, 0 otherwise
    errors = [i for i in report.issues if i.severity == "error"]
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
