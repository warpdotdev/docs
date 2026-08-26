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
from typing import Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

# Astro Starlight content lives under src/content/docs/, not a top-level docs/.
# This used to be `Path("docs")`, which silently scanned 0 files in the
# Astro layout — running --all reported "No issues found" without auditing
# anything.
DOCS_ROOT = Path("src/content/docs")
CHANGELOG_DIR = DOCS_ROOT / "changelog"
EXCLUDED_DIRS = {"_book", "node_modules", ".docs"}

# Feature names that are correctly Title Case (exceptions to sentence-case rule)
PROPER_FEATURE_NAMES = {
    "Admin Panel", "Agent Management Panel", "Agent Mode", "Agent Profiles",
    "Auto-detection Mode", "Cloud Agents",
    "Codebase Context", "Code Review", "Command Palette", "Global Rules",
    "Oz CLI", "Oz Platform", "Project Rules",
    "Slash Commands", "Terminal Mode", "Universal Input", "Warp Drive",
    "Warp Platform", "Automation Platform", "Warp Factories", "Factory MCP",
}

# Terminology: wrong → right (case-sensitive checks)
PRODUCT_CASING = {
    "Warp Terminal": ("Warp", "Use 'Warp' unless specifically distinguishing from Oz"),
    "Cloud Agent Credits": ("cloud agent credits", "Use lowercase 'cloud agent credits' (host-context) or 'compute credits' (bucket-context); capitalize first letter only at start of a sentence/bullet"),
    "Platform Credits": ("platform credits", "Use lowercase 'platform credits'; capitalize first letter only at start of a sentence/bullet/heading"),
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

# Rename-sensitive product name strings that should use src/data/vars.ts variables
# instead of being hardcoded. Keep this list in sync with vars.ts: only include
# entries whose values are expected to change at a product rename. Stable feature
# names (AGENT_MODE, WARP_DRIVE, etc.) are intentionally excluded.
#
# The bare "Oz" entries do double duty after the 8/18 rename. They no longer
# only mean "this should have been tokenized" -- a hardcoded "Oz" in prose is
# now a *stale* product name as well. Both readings want the same fix, so the
# entries stay. The "Automation Platform" entry is the mirror image: it catches
# the new name being hardcoded, which would silently miss the 9/15 changes and
# any later rename.
#
# Each entry: (literal_string, var_key, suggestion)
RENAME_SENSITIVE_VAR_STRINGS: List[Tuple[str, str, str]] = [
    ("Oz CLI",       "WARP_AGENT_CLI",           "{VARS.WARP_AGENT_CLI} in prose or {{WARP_AGENT_CLI}} in frontmatter"),
    ("Oz web app",   "WEB_APP",                  "{VARS.WEB_APP} in prose or {{WEB_APP}} in frontmatter"),
    ("oz.warp.dev",  "WEB_APP_URL",              "{VARS.WEB_APP_URL} in prose or {{WEB_APP_URL}} in frontmatter"),
    ("Oz dashboard", "DASHBOARD",                "{VARS.DASHBOARD} in prose or {{DASHBOARD}} in frontmatter"),
    ("Oz run",       "PLATFORM_RUN",             "{VARS.PLATFORM_RUN} in prose or {{PLATFORM_RUN}} in frontmatter"),
    ("Oz API & SDK", "API_SDK_NAME",             "{VARS.API_SDK_NAME} in prose or {{API_SDK_NAME}} in frontmatter"),
    ("Oz Platform",  "WARP_AUTOMATION_PLATFORM", "{VARS.WARP_AUTOMATION_PLATFORM} in prose or {{WARP_AUTOMATION_PLATFORM}} in frontmatter"),
    ("Automation Platform", "WARP_AUTOMATION_PLATFORM", "{VARS.WARP_AUTOMATION_PLATFORM} in prose or {{WARP_AUTOMATION_PLATFORM}} in frontmatter"),
    ("Oz",           "WARP_AUTOMATION_PLATFORM", "{VARS.WARP_AUTOMATION_PLATFORM} in prose or {{WARP_AUTOMATION_PLATFORM}} in frontmatter"),
]

# Phrasings that deliberately name the old product. A transition callout has to
# say "Oz" to do its job, so without this the guard would fight the very copy
# that explains the rename -- and the author's only workaround would be to
# backtick a product name, which is semantically wrong.
#
# Keyed on explicit transition phrasings rather than a per-file or per-page
# opt-out, so an unrelated stale "Oz" elsewhere on the same page is still
# caught. Only old-name literals are suppressed; a hardcoded *new* name on the
# same line still gets flagged, since nothing about a transition sentence
# excuses that.
RENAME_TRANSITION_MARKERS: Tuple[str, ...] = (
    "formerly Oz",
    "formerly called Oz",
    "formerly the Oz",
    "Oz is now",
    "was called Oz",
    "renamed from Oz",
    # Explains why "Oz" still appears in commands and URLs before 9/15.
    "the Oz name",
)

# Product names that merely contain "Oz" but are not the platform name, so they
# do not change when it does. "Oz by Warp" is the GitHub App as it appears in
# GitHub's own UI, at github.com/apps/oz-by-warp, and is what PRs and commits
# are attributed to. Renaming it in the docs would make them disagree with what
# the reader sees on GitHub. Same reasoning as the `@oz-agent` handle.
#
# "Oz Cloud API Keys" is the literal Settings label the Warp client still
# renders (`SettingsSection::OzCloudAPIKeys`, per terminology.md's "What still
# says Oz"). It changes only when the app renames that page, not at the
# Automation Platform rename, so it must stay hardcoded rather than tokenized.
#
# Matched as a suffix on the literal rather than added as its own entry,
# because the goal is to suppress rather than redirect: there is no variable
# these should be using instead.
#
# Keyed per-literal (not a single flat tuple shared by every entry) because
# the exemption must not bleed into other rename-sensitive literals. A flat
# tuple would suppress a hardcoded "Automation Platform Cloud API Keys" too --
# exactly the new-name literal this check exists to catch -- since that
# string also ends in " Cloud API Keys". Only the "Oz" literal gets these
# suffix exemptions.
RENAME_EXEMPT_SUFFIXES_BY_LITERAL: Dict[str, Tuple[str, ...]] = {
    "Oz": (" by Warp", " Cloud API Keys"),
}

# Determiner check for WARP_AUTOMATION_PLATFORM. See check_platform_determiner.
#
# "Oz" was a proper noun and read correctly bare. "Automation Platform" is a
# common-noun phrase and needs a definite article in referential positions. The
# defect is invisible in source -- `The {{WARP_AUTOMATION_PLATFORM}} provides`
# looks fine in the .mdx and only reads wrong once rendered -- so it needs a
# lint rule rather than review attention.
PLATFORM_TOKEN = re.compile(r"\{VARS\.WARP_AUTOMATION_PLATFORM\}|\{\{WARP_AUTOMATION_PLATFORM\}\}")
PLATFORM_DETERMINER = re.compile(r"\b(the|a|an|its|their|your|our|this|that)\s*(\*\*|\*|\[)?\s*$", re.IGNORECASE)
# Prepositions that take a noun phrase, so a bare platform name after one reads
# as a proper noun and is wrong under the new name.
PLATFORM_PREPOSITIONS = re.compile(
    r"\b(with|to|in|on|by|from|for|into|across|via|using|of|about|through|within)\s*(\*\*|\*|\[)?\s*$",
    re.IGNORECASE,
)
# Verbs that mark the token as a clause subject.
PLATFORM_SUBJECT_VERBS = re.compile(
    r"^\s*(\*\*|\*)?\s*(is|are|was|were|can|will|provides|gives|uses|reads|detects|supports|posts|runs|orchestrates|handles|manages|creates|lets|exposes|routes|tracks)\b"
)
# A lowercase word directly after the token usually means the token is
# modifying it -- "{...} orchestration", "automated {...} runs", "{...} cloud
# environments" -- which is attributive and correctly bare. Function words are
# excluded because they continue the sentence rather than extend the noun
# phrase, so "with {...} for cloud runs" is still referential.
PLATFORM_FUNCTION_WORDS = {
    "a", "an", "and", "are", "as", "at", "be", "blocks", "but", "by", "can",
    "for", "from", "if", "in", "is", "of", "on", "or", "so", "than", "that",
    "the", "then", "to", "was", "were", "when", "which", "while", "will", "with",
}
PLATFORM_NEXT_WORD = re.compile(r"^\s+([a-z][a-z-]*)")
# Several subject verbs double as nouns -- "runs", "uses", "reads". Requiring
# the token to actually begin a clause keeps "automated {...} runs" (a noun
# phrase) from being read as "{...} runs" (a subject and its verb).
PLATFORM_CLAUSE_START = re.compile(
    r"(^|[.:!?]\s+|[-\u2013\u2014]\s+|^\s*[*-]\s+)(\*\*|\*|\[)?\s*$"
)

# Oz terms to avoid (case-insensitive patterns)
OZ_TERMS_TO_AVOID = [
    (r"\bagent identities\b", "Use 'agents' or 'cloud agents' unless referring to legacy API names in code"),
    (r"\bagent identity\b", "Use 'agent' or 'cloud agent' unless referring to legacy API names in code"),
    (r"\bOzzies\b", "Use 'agents', 'instances', or 'subagents'"),
    (r"\bDeploying an Oz\b", "Use 'Deploying an agent'"),
    (r"\bThe Oz Agent\b", "Use 'the agent' or 'the Warp Agent'"),
    (r"\bOz is running\b", "Use 'An agent is running' or 'A run is in progress'"),
    (r"\bAI agents?\b", "Use 'agents' (the 'AI' prefix is redundant)"),
    (r"\bOz cloud agents?\b", "Use 'cloud agent(s)'"),
    (r"\bOz subagents?\b", "Use 'subagent(s)'"),
    (r"\bOz conversation\b", "Use 'conversation'"),
    (r"\bOz agents?\b", "Use 'agent(s)' or 'Warp Agent(s)' depending on context"),
    (r"\b[Aa]mbient [Aa]gents?\b", "Use 'cloud agent(s)' — 'ambient' is no longer a product term"),
]

# Tone: AI-generated-sounding words from AGENTS.md → Voice & tone → "Words to
# avoid". Report-only (never auto-fixed): every hit needs a human rewrite that
# names the specific capability, not a mechanical substitution.
#
# Deliberately narrower than the prose guidance. Words with legitimate
# technical uses in these docs are excluded so warnings stay trustworthy:
# "harness" (agent harness), "unlock" (login/keychain unlock), "elevate(d)"
# (elevated permissions), and "journey" stay out of the lint and are covered
# by AGENTS.md only.
TONE_BUZZWORDS: List[Tuple[str, str]] = [
    (r"\bseamless(?:ly)?\b", "Marketing adjective; describe the specific behavior instead"),
    (r"\beffortless(?:ly)?\b", "Marketing adjective; describe the specific behavior instead"),
    (r"\bpowerful\b", "Marketing adjective; name what the feature does instead"),
    (r"\brobust\b", "Marketing adjective; name what the feature does instead"),
    (r"\bcomprehensive(?:ly)?\b", "Marketing adjective; say what is included instead"),
    (r"\bcutting-edge\b", "Marketing adjective; delete it or name the capability"),
    (r"\bgame-chang\w+\b", "Marketing adjective; delete it or name the capability"),
    (r"\bsupercharg\w+\b", "Marketing verb; name the specific improvement instead"),
    (r"\bleverag(?:e|es|ed|ing)\b", "Use 'use'"),
    (r"\bstreamlin(?:e|es|ed|ing)\b", "Say what gets shorter or removed instead"),
    (r"\bempower(?:s|ed|ing)?\b", "Use 'let' or name the capability"),
    (r"\bdelv(?:e|es|ed|ing)\b", "Use 'cover' or name the topic directly"),
    (r"\blandscape\b", "Abstract metaphor; name the concrete thing"),
    (r"\brealm\b", "Abstract metaphor; name the concrete thing"),
    (r"\btapestry\b", "Abstract metaphor; name the concrete thing"),
    (r"\btestament to\b", "Filler phrase; state the fact directly"),
    (r"\b(?:it'?s|it is) (?:important to note|worth noting)\b", "Filler frame; cut it and state the fact directly"),
    (r"\bdesigned to\b", "Filler frame; say what it actually does instead"),
    (r"\bensur(?:e|es|ed|ing) that\b", "Filler frame; state the fact directly"),
    (r"\ballow(?:s|ed|ing)? you to\b", "Filler frame; use 'lets' or rewrite as a direct instruction"),
    (r"\bin order to\b", "Use 'to'"),
]

# Tone: meta-text that narrates the page instead of stating the thing itself.
# AGENTS.md → Voice & tone → "Every sentence earns its place".
META_OPENER = re.compile(
    r"\bThis (?:page|guide|section|article|document) (?:covers|explains|describes|walks(?: you)? through)\b"
)

# Starlight aside fences, for the callout-budget checks.
CALLOUT_OPEN = re.compile(r"^\s*:::(note|tip|caution|danger)\b")
CALLOUT_CLOSE = re.compile(r"^\s*:::\s*$")
# More callouts than this on one page almost always means caveats that belong
# in body prose. AGENTS.md allows at most one callout per section.
CALLOUT_PAGE_BUDGET = 4

# Action verbs that precede UI elements (should be bold, not backtick)
UI_ACTION_VERBS = r"(?:click|select|toggle|enable|disable|choose|check|uncheck|expand|collapse|open|close|tap)"

DEFAULT_SLACK_CHANNEL = os.environ.get("GROWTH_DOCS_SLACK_CHANNEL_ID", "")

TERMINOLOGY_FILE = Path(".agents/references/terminology.md")

# Standard figure widths for screenshots. See AGENTS.md § "Screenshot sizing
# standards".
#
# 736px is full content width: it matches `.main-pane .sl-container`'s
# `max-width: 46rem` in src/styles/custom.css. Because the container already
# caps at that width, 736px renders identically to omitting maxWidth entirely.
# It is listed explicitly so authors can signal "this screenshot is
# deliberately full width" and so this check can tell that apart from a figure
# that is simply missing a width. If the content column in custom.css ever
# changes, update this value to match.
STANDARD_SCREENSHOT_WIDTHS = {"300px", "350px", "375px", "563px", "736px"}

# Rendered as "300px, 350px, 375px, 563px, or 736px" in check messages, derived
# from the set above so the two can never drift apart.
_SORTED_WIDTHS = sorted(STANDARD_SCREENSHOT_WIDTHS)
STANDARD_WIDTHS_PHRASE = f"{', '.join(_SORTED_WIDTHS[:-1])}, or {_SORTED_WIDTHS[-1]}"

SCREENSHOT_PATH_HINTS = (
    "/assets/",
    "../../assets/",
    "../../../assets/",
    "../../../../assets/",
    "../../../../../assets/",
    ".png",
    ".gif",
    ".jpg",
    ".jpeg",
    ".webp",
)

NON_SCREENSHOT_HINTS = (
    "architecture",
    "diagram",
    "flowchart",
    "infra",
    "infrastructure",
    "logo",
    "use-cases",
)

GENERIC_LINK_ANCHORS = {
    "click here",
    "documentation",
    "docs",
    "here",
    "learn more",
    "link",
    "more",
    "page",
    "read more",
    "this article",
    "this documentation",
    "this guide",
    "this link",
    "this page",
    "website",
}

GENERIC_VIDEO_TITLES = {
    "demo",
    "demo video",
    "overview video",
    "tutorial video",
    "video",
    "walkthrough video",
}

RAW_URL_ANCHOR = re.compile(
    r"^(?:https?://|www\.|(?:[a-z0-9-]+\.)+(?:ai|app|co|com|dev|edu|gov|io|net|org)(?:/|$))",
    re.IGNORECASE,
)
MARKDOWN_LINK = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")
VIDEO_EMBED_TITLE = re.compile(r"\btitle\s*=\s*([\"'])(.*?)\1", re.DOTALL)
# JSX expression titles, e.g. title={`${VARS.WEB_APP} walkthrough`} — used when
# the title includes a rename-sensitive {VARS.KEY} reference. Content can't be
# statically evaluated, so these are treated as present but skipped by the
# generic-title check below.
VIDEO_EMBED_TITLE_EXPR = re.compile(r"\btitle\s*=\s*\{(.*?)\}", re.DOTALL)

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
    for f in [*DOCS_ROOT.rglob("*.md"), *DOCS_ROOT.rglob("*.mdx")]:
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
            ["git", "diff", "--name-only", "origin/main...HEAD", "--", str(DOCS_ROOT)],
            capture_output=True, text=True, check=True,
        )
        files = []
        for line in result.stdout.strip().split("\n"):
            if (line.endswith(".md") or line.endswith(".mdx")) and os.path.exists(line):
                p = Path(line)
                if not any(part in EXCLUDED_DIRS for part in p.parts) and not p.is_relative_to(CHANGELOG_DIR):
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


def _strip_markdown_formatting(text: str) -> str:
    """Remove lightweight Markdown/HTML formatting from link text."""
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = re.sub(r"\*\*([^*]*)\*\*", r"\1", text)
    text = re.sub(r"__([^_]*)__", r"\1", text)
    text = re.sub(r"\*([^*]*)\*", r"\1", text)
    text = re.sub(r"_([^_]*)_", r"\1", text)
    text = re.sub(r"<[^>]+>", "", text)
    return text


def _normalize_link_text(text: str) -> str:
    """Normalize link text for generic-anchor comparisons."""
    text = _strip_markdown_formatting(text)
    text = re.sub(r"\s+", " ", text).strip().lower()
    return text.strip(" \t\n\r.,:;!?()[]{}\"'")


def _meaningful_words(text: str) -> List[str]:
    """Return lowercase words that carry semantic meaning for comparisons."""
    stopwords = {"a", "an", "and", "for", "in", "of", "on", "the", "to", "with", "x"}
    words = re.findall(r"[a-z0-9]+", text.lower())
    return [word for word in words if len(word) > 2 and word not in stopwords]


def check_link_quality(lines: List[str], filepath: str) -> List[Issue]:
    """Check Markdown links for descriptive, contextual anchor text."""
    issues = []
    in_code_block = False
    article_pattern = re.compile(
        r"\b(go to|open|visit|navigate to|view)\s+\[((?:Runs|Integrations|Schedules|Environments|Secrets) page in the Oz web app)\]",
        re.IGNORECASE,
    )
    redundant_prefix = re.compile(
        r"^\s*[-*]\s+\*\*([^*]+)\*\*\s*[:—-]\s*\[([^\]]+)\]\([^)]+\)\.?\s*$"
    )

    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue

        for m in MARKDOWN_LINK.finditer(line):
            # Skip Markdown images.
            if m.start() > 0 and line[m.start() - 1] == "!":
                continue

            anchor = m.group(1).strip()
            normalized = _normalize_link_text(anchor)
            if not normalized:
                issues.append(Issue(
                    filepath, i, "link-anchor",
                    "Markdown link has empty anchor text; use descriptive link text that explains the destination",
                    "error",
                ))
                continue

            if RAW_URL_ANCHOR.match(normalized):
                issues.append(Issue(
                    filepath, i, "link-anchor",
                    f"Raw URL used as link text: \"{anchor}\". Name the destination instead.",
                    "warning",
                ))
            elif normalized in GENERIC_LINK_ANCHORS:
                issues.append(Issue(
                    filepath, i, "link-anchor",
                    f"Generic link text: \"{anchor}\". Use descriptive anchor text that explains what users will find.",
                    "warning",
                ))

        for m in article_pattern.finditer(line):
            action = m.group(1)
            page_name = m.group(2)
            issues.append(Issue(
                filepath, i, "link-context",
                f"Add \"the\" before named destination page: \"{action} the [{page_name}]\"",
                "warning",
            ))

        m = redundant_prefix.match(line)
        if m:
            prefix = _normalize_link_text(m.group(1))
            anchor = _normalize_link_text(m.group(2))
            prefix_words = _meaningful_words(prefix)
            anchor_words = set(_meaningful_words(anchor))
            if prefix_words and all(word in anchor_words for word in prefix_words):
                issues.append(Issue(
                    filepath, i, "link-context",
                    f"Link text repeats the bold prefix \"{m.group(1)}\". Remove the prefix or add distinct context.",
                    "warning",
                ))

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


def _is_likely_screenshot(markdown_image_line: str) -> bool:
    """Return True for UI/product screenshots while avoiding diagrams/logos."""
    lower = markdown_image_line.lower()
    if not any(hint in lower for hint in SCREENSHOT_PATH_HINTS):
        return False
    if any(hint in lower for hint in NON_SCREENSHOT_HINTS):
        return False
    return True


def _figure_width(line: str) -> Optional[str]:
    """Extract a maxWidth value from an MDX figure opening tag."""
    match = re.search(r"maxWidth:\s*[\"']([^\"']+)[\"']", line)
    if match:
        return match.group(1)
    return None


def check_screenshot_widths(lines: List[str], filepath: str) -> List[Issue]:
    """Check that screenshot images use standardized width-controlled figures.

    The docs style guide asks screenshots to use consistent widths. This check
    flags likely UI/product screenshots that are standalone Markdown images or
    figure-wrapped images missing a standard maxWidth. Architecture diagrams,
    logos, and broad conceptual illustrations are intentionally excluded by
    filename/alt-text hints because they often need default content width.
    """
    issues = []
    in_code_block = False
    figure_start_line: Optional[int] = None
    figure_opening = ""
    figure_has_likely_screenshot = False

    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue

        if "<figure" in line:
            figure_start_line = i
            figure_opening = line
            figure_has_likely_screenshot = False

        if "![" in line and _is_likely_screenshot(line):
            if figure_start_line is None:
                issues.append(Issue(
                    filepath, i, "screenshot-width",
                    f"Likely screenshot image should be wrapped in a <figure> with a standard maxWidth ({STANDARD_WIDTHS_PHRASE})",
                    "warning",
                ))
            else:
                figure_has_likely_screenshot = True

        if "</figure>" in line and figure_start_line is not None:
            if figure_has_likely_screenshot:
                width = _figure_width(figure_opening)
                if width is None:
                    issues.append(Issue(
                        filepath, figure_start_line, "screenshot-width",
                        f"Screenshot figure is missing a standard maxWidth ({STANDARD_WIDTHS_PHRASE})",
                        "warning",
                    ))
                elif width not in STANDARD_SCREENSHOT_WIDTHS:
                    issues.append(Issue(
                        filepath, figure_start_line, "screenshot-width",
                        f"Screenshot figure uses non-standard maxWidth \"{width}\"; use one of {STANDARD_WIDTHS_PHRASE}",
                        "warning",
                    ))
            figure_start_line = None
            figure_opening = ""
            figure_has_likely_screenshot = False

    return issues


def _iter_video_embed_tags(lines: List[str]) -> List[Tuple[int, str]]:
    """Return (line_number, tag_text) for VideoEmbed components."""
    tags: List[Tuple[int, str]] = []
    in_code_block = False
    collecting = False
    start_line = 0
    tag_parts: List[str] = []

    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue

        if not collecting and "<VideoEmbed" in line:
            collecting = True
            start_line = i
            tag_parts = [line]
            if ">" in line:
                tags.append((start_line, "\n".join(tag_parts)))
                collecting = False
                tag_parts = []
            continue

        if collecting:
            tag_parts.append(line)
            if ">" in line:
                tags.append((start_line, "\n".join(tag_parts)))
                collecting = False
                tag_parts = []

    if collecting and tag_parts:
        tags.append((start_line, "\n".join(tag_parts)))
    return tags


def _is_generic_video_title(title: str) -> bool:
    """Return True when a VideoEmbed title is too generic for SEO/accessibility."""
    normalized = re.sub(r"\s+", " ", title).strip().lower()
    normalized = normalized.strip(" \t\n\r.,:;!?()[]{}\"'")
    if normalized in GENERIC_VIDEO_TITLES:
        return True
    if re.search(r"\b(?:video|demo)\s+\d+\b", normalized):
        return True
    words = re.findall(r"[a-z0-9]+", normalized)
    if normalized.endswith(" video") and len(words) <= 3:
        return True
    return False


def check_video_embed_titles(lines: List[str], filepath: str) -> List[Issue]:
    """Check VideoEmbed components for specific title props."""
    issues = []
    for line_number, tag in _iter_video_embed_tags(lines):
        title_match = VIDEO_EMBED_TITLE.search(tag)
        if title_match and title_match.group(2).strip():
            title = title_match.group(2).strip()
            if _is_generic_video_title(title):
                issues.append(Issue(
                    filepath, line_number, "video-title",
                    f"Generic VideoEmbed title: \"{title}\". Use a specific title that describes what the video shows.",
                    "warning",
                ))
            continue

        # Not a quoted string literal — check for a JSX expression title, e.g.
        # title={`${VARS.WEB_APP} walkthrough`}. Content isn't statically
        # evaluable, so skip the generic-title check but still confirm a
        # non-empty title prop is present.
        expr_match = VIDEO_EMBED_TITLE_EXPR.search(tag)
        if expr_match and expr_match.group(1).strip():
            continue

        issues.append(Issue(
            filepath, line_number, "video-title",
            "VideoEmbed missing title prop. Add a specific title that describes the integration, workflow, feature, or task shown.",
            "error",
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
    """Check for Oz terms to avoid.

    Skips fenced code blocks and strips inline code (backtick-wrapped text)
    so that legitimate CLI commands like `oz agent run` are not flagged.
    """
    issues = []
    in_code_block = False
    for i, line in enumerate(lines, 1):
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue
        # Strip inline code spans so `oz agent run` is not matched
        prose_line = re.sub(r"`[^`]+`", "", line)
        for pattern, suggestion in OZ_TERMS_TO_AVOID:
            for m in re.finditer(pattern, prose_line, re.IGNORECASE):
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


def check_hardcoded_vars(lines: List[str], filepath: str) -> List[Issue]:
    """Flag hardcoded product name strings that should use the vars system.

    Strings listed in RENAME_SENSITIVE_VAR_STRINGS are expected to change at
    product rename time. Using them as literals (instead of {VARS.KEY} in prose
    or {{TOKEN}} in frontmatter) means they won't update when vars.ts changes.

    Skips fenced code blocks and inline code spans so that CLI examples like
    `oz.warp.dev` in a code fence are not flagged.

    Literals are checked longest-first and matches are deduplicated by span so
    overlapping rename-sensitive names are not double-flagged.

    Matches use word boundaries (`\b`) rather than plain substring search, so
    literals don't false-positive inside unrelated tokens such as URL query
    params, hashes, or other identifiers.

    An "@"-prefixed occurrence is skipped because mention handles are literal
    strings that do not necessarily change with product names. Variabilizing
    a handle could silently rewrite it into an invalid value at rename time.

    Old-name literals are also skipped on lines carrying a phrase from
    RENAME_TRANSITION_MARKERS, so "formerly Oz" copy can name the old product
    without the guard objecting. New-name literals on those lines still flag.
    """
    issues = []
    in_code_block = False
    sorted_strings = sorted(RENAME_SENSITIVE_VAR_STRINGS, key=lambda entry: -len(entry[0]))
    compiled = [
        (literal, var_key, suggestion, re.compile(r"\b" + re.escape(literal) + r"\b"))
        for literal, var_key, suggestion in sorted_strings
    ]
    for i, line in enumerate(lines, 1):
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue
        # Text that describes an image must match the image, so it cannot be
        # tokenized. Two separate reasons, same conclusion:
        #
        # Alt text is markdown, not JSX -- `![... {VARS.WEB_APP}](...)` renders
        # the literal "VARS.WEB_APP" on the page, so tokenizing it is simply
        # broken. Figcaptions *are* JSX and would substitute correctly, but a
        # caption that auto-flips ahead of the screenshot it captions is worse
        # than one that stays stale: the page would claim a name the image
        # visibly contradicts. Both have to be updated by hand, together with
        # the images, when the screenshots are retaken.
        if line.lstrip().startswith("![") or "<figcaption" in line:
            continue
        # Strip inline code spans so backtick-wrapped references are not flagged
        prose_line = re.sub(r"`[^`]+`", "", line)
        # Deliberate historical reference on this line. See docstring.
        is_transition_line = any(
            marker in prose_line for marker in RENAME_TRANSITION_MARKERS
        )
        matched_spans: List[Tuple[int, int]] = []
        for literal, var_key, suggestion, pattern in compiled:
            for m in pattern.finditer(prose_line):
                span = m.span()
                if any(span[0] >= s and span[1] <= e for s, e in matched_spans):
                    continue
                # Mention handles are literal strings, not prose. See docstring.
                if span[0] > 0 and prose_line[span[0] - 1] == "@":
                    continue
                # Only the old name is excused by transition phrasing; a
                # hardcoded new name is still a bug on the same line.
                if is_transition_line and literal.startswith(("Oz", "oz")):
                    continue
                # Distinct product names that happen to contain "Oz", or the
                # literal "Oz Cloud API Keys" Settings label. Looked up by the
                # exact literal that matched, so this never suppresses a
                # different rename-sensitive literal (e.g. "Automation
                # Platform") that happens to share the same suffix.
                if any(
                    prose_line[span[1]:].startswith(suffix)
                    for suffix in RENAME_EXEMPT_SUFFIXES_BY_LITERAL.get(literal, ())
                ):
                    continue
                matched_spans.append(span)
                issues.append(Issue(
                    filepath, i, "hardcoded-var",
                    f'Hardcoded "{literal}" should use {suggestion} (see src/data/vars.ts)',
                    "warning",
                ))
    return issues


def check_platform_determiner(lines: List[str], filepath: str) -> List[Issue]:
    """Flag {VARS.WARP_AUTOMATION_PLATFORM} used referentially without an article.

    "Oz" was a proper noun and read correctly bare: "with Oz", "Oz provides",
    "Oz's backend". "Automation Platform" is a common-noun phrase, so the same
    positions need a definite article: "with the ...", "The ... provides",
    "the ...'s backend".

    This is worth a lint rule rather than review attention because the defect is
    invisible in the source file. `The {{WARP_AUTOMATION_PLATFORM}} provides`
    looks correct in the .mdx and only reads wrong once the variable is
    substituted at build time.

    Only high-confidence positions are flagged, so that attributive uses stay
    quiet:
      * possessive   -- token followed by 's
      * prepositional -- token directly after "with", "to", "in", and friends
      * subject      -- token directly before a finite verb

    Deliberately NOT flagged, because bare is correct there:
      * attributive compounds  -- "{{...}} settings", "{{...}}-hosted", and any
        token directly followed by a lowercase noun it modifies
      * frontmatter title/label values -- "{{...}} overview"
      * bold term leads in definition lists -- "* **{VARS....}** - ..."

    A determiner on the previous line still counts, so a soft-wrapped sentence
    or a wrapped frontmatter description is not falsely flagged.
    """
    issues = []
    in_code_block = False
    in_frontmatter = False
    # Frontmatter is not uniformly exempt. `title` and `sidebar.label` are
    # headline-style and correctly bare, but `description` is a sentence, and it
    # becomes the meta description -- the text search engines and AI engines
    # read before deciding whether to cite the page. Skipping all of
    # frontmatter left exactly that field unguarded against the defect this
    # check exists to catch.
    in_description = False
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if i == 1 and stripped == "---":
            in_frontmatter = True
            continue
        if in_frontmatter:
            if stripped == "---":
                in_frontmatter = False
                in_description = False
                continue
            # A description can be inline or a folded block (`description: >-`)
            # continuing over several indented lines. Track which key we are
            # inside so the continuation lines are scanned too.
            key = re.match(r"([a-zA-Z_]+):", stripped)
            if key:
                in_description = key.group(1) == "description"
            if not in_description:
                continue
            # fall through and scan this line
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block or not PLATFORM_TOKEN.search(line):
            continue
        for m in PLATFORM_TOKEN.finditer(line):
            before = line[:m.start()]
            after = line[m.end():]
            # A wrapped line can leave the determiner on the previous line.
            lookback = before if before.strip() else (lines[i - 2] if i >= 2 else "")
            if PLATFORM_DETERMINER.search(lookback):
                continue
            if after[:1] == "-":  # attributive compound, e.g. "{{...}}-hosted"
                continue
            if re.match(r"^\s*[*-]\s+\*\*\s*$", before):  # bold term lead
                continue

            # Order matters. Possessive and subject positions are unambiguous,
            # so they are classified first. The attributive exemption applies
            # only to the prepositional case, which is the one that is genuinely
            # ambiguous: "with {...} orchestration" modifies a noun and is fine
            # bare, while "with {...}." is referential and needs the article.
            # Applying the exemption earlier would swallow "{...} provides ...",
            # since "provides" is just a lowercase word to a regex.
            if after.startswith("'s") or after.startswith("\u2019s"):
                position = "possessive"
            elif PLATFORM_SUBJECT_VERBS.match(after) and PLATFORM_CLAUSE_START.search(before):
                position = "as a clause subject"
            elif PLATFORM_PREPOSITIONS.search(lookback):
                nxt = PLATFORM_NEXT_WORD.match(after)
                if nxt and nxt.group(1) not in PLATFORM_FUNCTION_WORDS:
                    continue  # attributive: the token modifies the next noun
                position = "after a preposition"
            else:
                continue

            issues.append(Issue(
                filepath, i, "platform-determiner",
                f"{{VARS.WARP_AUTOMATION_PLATFORM}} used {position} without a "
                f"determiner. The value is a common-noun phrase, so this renders "
                f'as e.g. "with Automation Platform". Add "the" before it.',
                "warning",
            ))
    return issues


# "Warp Factories" is the product; a "factory" is an instance. A bare
# capitalized "Factory" is never a proper noun, with two classes of exception:
# the feature's own name (Factory MCP) and verbatim product strings the docs
# quote from the app. Both are matched on the word that FOLLOWS "Factory".
FACTORY_ALLOWED_NEXT_WORDS = {
    # Feature name, shipped as such: the server registers as `warp-factory`.
    "MCP",
    # Verbatim UI strings. Changing these would make the docs disagree with the
    # screen, so they are quoted as-is until the app copy changes.
    "name",        # **Factory name** field in the setup wizard
    "definition",  # **Factory definition** sidebar tab
    "integrations",  # **Factory integrations** section in Settings
    "running",     # "Factory running!" on the setup summary screen
}
# Whole phrases that are correct despite containing a bare "Factory": verbatim
# UI strings the docs quote, and references to unrelated products that happen to
# be named Factory.
FACTORY_ALLOWED_PHRASES = (
    "Add your Factory to your team",  # verbatim setup wizard heading
    "Factory's CLI coding agent",     # Factory.ai, the company behind Droid
)
FACTORY_BARE = re.compile(r"\bFactory\b")
# Markup that can sit between the start of a sentence and the word itself:
# heading hashes, list bullets, blockquotes, emphasis, link text, quotes, and
# table cell pipes. Stripped before deciding whether the position is initial.
FACTORY_LEADING_MARKUP = re.compile(r"[\s*_\[\(\"'|>#\-\u2014\u2013]+$")


def check_factory_proper_noun(lines: List[str], filepath: str) -> List[Issue]:
    """Flag a bare capitalized "Factory" used as a proper noun.

    The rule works like GitHub Actions: "Warp Factories" is the product and is
    always written in full, an individual "factory" is a lowercase common noun,
    and there is no product called "Factory". See AGENTS.md -> Warp Factories
    terminology.

    Quiet by construction, because most capitalized "Factory" occurrences are
    legitimate:
      * sentence-, heading-, bullet-, link-, quote-, and cell-initial position,
        where the capital is positional rather than a proper noun
      * fenced code blocks, inline code, link targets, and HTML attributes
      * frontmatter, whose titles and sidebar labels are headline-style
      * the exceptions in FACTORY_ALLOWED_NEXT_WORDS and
        FACTORY_ALLOWED_PHRASES

    The singular "Warp Factory" is NOT exempt. The product is "Warp Factories",
    always plural, and one deployment of it is a lowercase "factory", so the
    singular is wrong in both senses. It gets its own message because the fix
    differs from the bare-"Factory" case. "Warp Factory MCP" still passes, via
    FACTORY_ALLOWED_NEXT_WORDS. The plural never reaches this check at all:
    FACTORY_BARE is \\bFactory\\b, which cannot match "Factories".
    """
    issues = []
    in_code_block = False
    in_frontmatter = False
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if i == 1 and stripped == "---":
            in_frontmatter = True
            continue
        if in_frontmatter:
            if stripped == "---":
                in_frontmatter = False
            continue
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block or "Factory" not in line:
            continue
        if any(phrase in line for phrase in FACTORY_ALLOWED_PHRASES):
            continue
        # Strip inline code, link targets, and HTML/JSX attributes: a slug like
        # `/factories/factory-as-code/` or an `alt="..."` value is not prose.
        prose = re.sub(r"`[^`]*`", "", line)
        prose = re.sub(r"\]\([^)]*\)", "]", prose)
        prose = re.sub(r'\w+="[^"]*"', "", prose)
        for m in FACTORY_BARE.finditer(prose):
            before = prose[:m.start()]
            after = prose[m.end():]
            preceded_by_warp = before.rstrip().endswith("Warp")
            # Strip the markup between the sentence start and the word, then ask
            # whether anything is left. Nothing left means the capital is
            # positional; a preceding clause means it is being used as a name.
            # "Warp" is itself a preceding clause, so the singular product name
            # is caught here even at the start of a sentence or heading.
            prefix = FACTORY_LEADING_MARKUP.sub("", before)
            if not prefix or prefix.endswith((".", "!", "?", ":", "|", "—")):
                continue
            nxt = re.match(r"\s+(\w+)", after)
            if nxt and nxt.group(1) in FACTORY_ALLOWED_NEXT_WORDS:
                continue
            if preceded_by_warp:
                message = (
                    'Singular "Warp Factory" used as a product name. The '
                    'product is "Warp Factories", always plural and written in '
                    'full; one deployment of it is a lowercase "factory". '
                    'Write "Warp Factories" for the product, or "a factory" '
                    "for an instance."
                )
            else:
                message = (
                    'Bare "Factory" used as a proper noun. "Warp Factories" is '
                    'the product and is written in full; an individual factory '
                    'is lowercase. Write "factory" (or "Warp Factories" if you '
                    "mean the product)."
                )
            issues.append(Issue(
                filepath, i, "factory-proper-noun", message, "warning",
            ))
    return issues


# ---------------------------------------------------------------------------
# Tone checks (report-only, never auto-fixed)
# ---------------------------------------------------------------------------

def _strip_inline_code(line: str) -> str:
    """Remove inline code spans so CLI flags and API fields never trip tone checks."""
    return re.sub(r"`[^`]*`", "", line)


def check_tone_buzzwords(lines: List[str], filepath: str) -> List[Issue]:
    """Flag AI-ism buzzwords (AGENTS.md → Voice & tone → Words to avoid).

    Report-only: the fix is a rewrite that names the specific capability,
    which cannot be automated. Frontmatter is scanned too — a buzzword in a
    description is still a buzzword in search results.
    """
    issues = []
    in_code_block = False
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue
        prose = _strip_inline_code(line)
        for pattern, suggestion in TONE_BUZZWORDS:
            for m in re.finditer(pattern, prose, re.IGNORECASE):
                issues.append(Issue(
                    filepath, i, "tone-buzzword",
                    f'"{m.group(0)}": {suggestion}',
                    "warning",
                ))
    return issues


def check_meta_openers(lines: List[str], filepath: str) -> List[Issue]:
    """Flag meta-text that narrates the page ("This page covers...").

    The title and description already frame the page; body prose should state
    the thing itself. AGENTS.md → Voice & tone → Every sentence earns its place.
    """
    issues = []
    in_code_block = False
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue
        if META_OPENER.search(_strip_inline_code(line)):
            issues.append(Issue(
                filepath, i, "tone-meta-opener",
                "Meta-text that narrates the page ('This page covers...'). "
                "Cut it and state the thing itself",
                "warning",
            ))
    return issues


def check_callout_density(lines: List[str], filepath: str) -> List[Issue]:
    """Flag back-to-back callouts and pages over the callout budget.

    AGENTS.md → Callouts and hints: never consecutive, at most one per
    section. Per-page count is the lintable proxy for the per-section rule.
    """
    issues = []
    in_code_block = False
    in_callout = False
    open_lines: List[int] = []
    last_close_line: Optional[int] = None
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue
        if not in_callout and CALLOUT_OPEN.match(line):
            open_lines.append(i)
            if last_close_line is not None and all(
                not lines[j].strip() for j in range(last_close_line, i - 1)
            ):
                issues.append(Issue(
                    filepath, i, "callout-consecutive",
                    "Two callouts back to back; merge them or move one into "
                    "body prose (AGENTS.md → Callouts and hints)",
                    "warning",
                ))
            in_callout = True
            continue
        if in_callout and CALLOUT_CLOSE.match(line):
            in_callout = False
            last_close_line = i
    if len(open_lines) > CALLOUT_PAGE_BUDGET:
        issues.append(Issue(
            filepath, open_lines[CALLOUT_PAGE_BUDGET], "callout-density",
            f"{len(open_lines)} callouts on one page; keep to at most one per "
            "section and move the rest into body prose",
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
    issues.extend(check_link_quality(lines, str(filepath)))
    issues.extend(check_header_case(lines, str(filepath)))
    issues.extend(check_image_alt_text(lines, str(filepath)))
    issues.extend(check_screenshot_widths(lines, str(filepath)))
    issues.extend(check_video_embed_titles(lines, str(filepath)))
    issues.extend(check_callout_syntax(lines, str(filepath)))
    issues.extend(check_tone_buzzwords(lines, str(filepath)))
    issues.extend(check_meta_openers(lines, str(filepath)))
    issues.extend(check_callout_density(lines, str(filepath)))
    issues.extend(check_product_casing(lines, str(filepath)))
    issues.extend(check_oz_terms(lines, str(filepath)))
    issues.extend(check_deprecated_terms(lines, str(filepath)))
    issues.extend(check_hardcoded_vars(lines, str(filepath)))
    issues.extend(check_platform_determiner(lines, str(filepath)))
    issues.extend(check_factory_proper_noun(lines, str(filepath)))
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
    subprocess.run(["git", "add", str(DOCS_ROOT)], check=True)
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
