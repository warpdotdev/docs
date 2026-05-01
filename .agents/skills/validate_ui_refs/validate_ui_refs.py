#!/usr/bin/env python3
"""Validate UI paths and Command Palette names in Warp Astro Starlight documentation.

Scans markdown files for references to Warp UI paths (Settings > ..., File > ..., etc.)
and Command Palette command names, then validates them against a snapshot of known-valid
paths extracted from the warp-internal codebase.

Usage:
    python3 validate_ui_refs.py --all
    python3 validate_ui_refs.py --check-paths
    python3 validate_ui_refs.py --check-commands
    python3 validate_ui_refs.py --all --fix --create-pr --slack-notify
    python3 validate_ui_refs.py --refresh-valid-paths --warp-internal-path /path/to/warp-internal
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_VALID_PATHS_FILE = SCRIPT_DIR / "valid_paths.json"
DEFAULT_DOCS_DIR = SCRIPT_DIR.parents[2] / "docs"
DEFAULT_SLACK_CHANNEL = os.environ.get("SLACK_CHANNEL_ID", "")

# Known Warp UI roots — paths starting with these are Warp UI paths
WARP_UI_ROOTS = {"Settings", "File", "View", "Warp", "Warp Drive", "Personal"}

# Roots that belong to external products (not Warp)
EXTERNAL_ROOTS = {
    "Mac", "System", "System Preferences", "Windows", "Linux",
    "Chrome", "Firefox", "Safari", "VS Code", "Visual Studio",
}

# Context keywords that indicate a non-Warp UI path even if root matches
EXTERNAL_CONTEXT_KEYWORDS = {
    "github", "gitlab", "bitbucket", "organization", "org settings",
    "slack", "linear", "notion", "jira", "figma",
    "raycast", "vs code", "vscode", "visual studio",
}

# Known external/OS Settings paths that look like Warp paths but aren't.
# These are matched as prefixes of the normalized path.
EXTERNAL_SETTINGS_PATHS = {
    "Settings > Privacy & Security",
    "Settings > Secrets and variables",
    "Settings > Extensions",
    "Settings > Notifications",
    "Settings > System",
    "Settings > People",
    "Settings > General",
}

# Minimum fuzzy match score to suggest an alternative
FUZZY_MATCH_THRESHOLD = 0.6

# Minimum fuzzy match score for auto-fix
AUTO_FIX_THRESHOLD = 0.9


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_valid_paths(path: Path) -> Dict[str, Any]:
    """Load the valid_paths.json snapshot."""
    with open(path, "r") as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# Extraction: UI paths from docs
# ---------------------------------------------------------------------------

# Regex patterns for UI paths in various markdown formats
# Backtick: `Settings > AI > Active AI`
RE_BACKTICK_PATH = re.compile(
    r"`((?:" + "|".join(re.escape(r) for r in WARP_UI_ROOTS) + r")\s*>\s*[^`]+)`"
)
# Bold: **Settings > AI > Active AI**
RE_BOLD_PATH = re.compile(
    r"\*\*((?:" + "|".join(re.escape(r) for r in WARP_UI_ROOTS) + r")\s*>\s*[^*]+)\*\*"
)
# Italic: _Settings > AI > Active AI_ or *Settings > AI*
RE_ITALIC_PATH = re.compile(
    r"(?:_|\*)((?:" + "|".join(re.escape(r) for r in WARP_UI_ROOTS) + r")\s*>\s*[^_*]+)(?:_|\*)"
)
# Bare (no formatting): Settings > AI > Active AI (at start of line or after common punctuation)
RE_BARE_PATH = re.compile(
    r"(?:^|[(\s])((?:" + "|".join(re.escape(r) for r in WARP_UI_ROOTS) + r")\s*>\s*\S[^.)\n\[,]*)",
    re.MULTILINE,
)
# Per-segment backtick: `Settings` > `AI` > `Active AI`
RE_SEG_BACKTICK_PATH = re.compile(
    r"(`(?:" + "|".join(re.escape(r) for r in WARP_UI_ROOTS) + r")`\s*>\s*`[^`]+`(?:\s*>\s*`[^`]+`)*)"
)
# Canonical format: **Settings** > **AI** > **Active AI**
RE_CANONICAL_PATH = re.compile(
    r"(\*\*(?:" + "|".join(re.escape(r) for r in WARP_UI_ROOTS) + r")\*\*\s*>\s*\*\*[^*]+\*\*(?:\s*>\s*\*\*[^*]+\*\*)*)"
)


def _normalize_path(raw: str) -> str:
    """Normalize whitespace around > separators and strip artifacts."""
    path = " > ".join(seg.strip() for seg in raw.split(">"))
    # Strip trailing punctuation that gets captured by bare-path regex
    path = path.rstrip(".,;:!?")
    # Strip formatting wrappers from individual segments
    segments = path.split(" > ")
    segments = [s.strip("`").strip("*") for s in segments]
    return " > ".join(segments)


def _to_canonical_format(normalized: str) -> str:
    """Convert a normalized path to canonical bold format: **Seg** > **Seg**."""
    segments = normalized.split(" > ")
    return " > ".join(f"**{seg}**" for seg in segments)


def _is_external_path(path: str, line: str) -> bool:
    """Check if a path belongs to an external product, not Warp."""
    root = path.split(">")[0].strip()
    if root in EXTERNAL_ROOTS:
        return True
    # Check against known external Settings paths
    for ext_path in EXTERNAL_SETTINGS_PATHS:
        if path.startswith(ext_path):
            return True
    # Check surrounding line for external product keywords
    line_lower = line.lower()
    for kw in EXTERNAL_CONTEXT_KEYWORDS:
        if kw in line_lower:
            return True
    return False


def extract_ui_paths(file_path: Path) -> List[Dict[str, Any]]:
    """Extract all Warp UI path references from a markdown file."""
    results = []
    try:
        text = file_path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return results

    for line_num, line in enumerate(text.splitlines(), start=1):
        for pattern, fmt in [
            (RE_CANONICAL_PATH, "canonical"),
            (RE_SEG_BACKTICK_PATH, "seg_backtick"),
            (RE_BACKTICK_PATH, "backtick"),
            (RE_BOLD_PATH, "bold"),
            (RE_ITALIC_PATH, "italic"),
            (RE_BARE_PATH, "bare"),
        ]:
            for match in pattern.finditer(line):
                raw = match.group(1).strip()
                normalized = _normalize_path(raw)
                if _is_external_path(normalized, line):
                    continue
                # Skip bare paths that look like they captured a full sentence
                # (e.g. "Settings > Features so that the completions menu opens")
                if fmt == "bare":
                    segments = normalized.split(" > ")
                    if len(segments) >= 2 and len(segments[1].split()) > 5:
                        continue
                # Skip if this span was already matched by an earlier pattern
                match_span = (line_num, match.start(), match.end())
                if any(
                    r["_span"] == match_span or
                    (r["line"] == line_num and r["normalized"] == normalized)
                    for r in results
                ):
                    continue
                results.append({
                    "file": str(file_path),
                    "line": line_num,
                    "raw": raw,
                    "normalized": normalized,
                    "format": fmt,
                    "match_text": match.group(0),
                    "line_text": line,
                    "_span": match_span,
                })
    return results


# ---------------------------------------------------------------------------
# Extraction: Command Palette names from docs
# ---------------------------------------------------------------------------

# Patterns for Command Palette references:
#   - "Open Theme Picker" near "Command Palette"
#   - Command Palette > Open Theme Picker
RE_CMD_PALETTE_QUOTED = re.compile(
    r'["\u201c]([^"\u201d\n]{4,})["\u201d]'
)
RE_CMD_PALETTE_ARROW = re.compile(
    r"Command Palette\s*>\s*[`\"]*([^`\"\n>]+)[`\"]*"
)


# Common words that appear quoted near Command Palette but aren't commands
_CMD_PALETTE_STOPWORDS = {
    "macos", "windows", "linux", "mac", "appearance", "export", "share",
    "prompt", "a11y", "settings", "preferences",
}

# UI action keywords that precede toggle/button labels, not CP commands.
# If a quoted string is preceded by one of these on the same line, skip it.
_RE_UI_LABEL_PREFIX = re.compile(
    r'\b(toggle|click|clicking|enable|disable|select|check|uncheck)\b',
    re.IGNORECASE,
)


def _is_plausible_command_name(name: str) -> bool:
    """Filter false positives for command palette names."""
    name = name.strip()
    # Too short
    if len(name) < 4:
        return False
    # Too long — likely a sentence or alt text, not a command name
    if len(name) > 80:
        return False
    # Pure numbers or special chars
    if re.match(r"^[\d\s.,:;!?]+$", name):
        return False
    # Trailing colon (likely a label, not a command)
    if name.endswith(":"):
        return False
    # Single word (unlikely to be a command name, which are usually multi-word)
    if re.match(r"^[A-Za-z]+$", name) and name.lower() in _CMD_PALETTE_STOPWORDS:
        return False
    # Single lowercase word
    if re.match(r"^[a-z]+$", name):
        return False
    # URLs
    if name.startswith("http") or name.startswith("www."):
        return False
    # File paths or anchors
    if "/" in name or "\\" in name or name.startswith("#"):
        return False
    # Kebab-case strings (URL fragments like "using-forked-conversations")
    if re.match(r"^[a-z][a-z0-9-]+$", name):
        return False
    # HTML/markdown artifacts
    if name.startswith("width=") or name.startswith("height="):
        return False
    if "**" in name or "__" in name:
        return False
    # Image alt text patterns (long descriptive phrases)
    description_indicators = [
        "showing", "displayed", "with the", "interface", "screenshot",
        "circled", "button", "view of", "image of",
        " ago",  # status text like "Completed 10 minutes ago"
    ]
    name_lower = name.lower()
    if any(ind in name_lower for ind in description_indicators):
        return False
    # OS names that appear near Command Palette mentions
    if name_lower in _CMD_PALETTE_STOPWORDS:
        return False
    # Settings toggle label patterns — typically lowercase descriptive phrases
    # that describe a behavior rather than an action command.
    # Real commands typically start with a verb: Open, Toggle, Set, Copy, etc.
    _settings_toggle_phrases = {
        "autocomplete quotes", "autosuggestions", "block dividers",
        "compact mode", "copy on select", "cursor blink",
        "error underlining for commands", "expand aliases as you type",
        "help improve warp", "input hint text", "send crash reports",
        "show tab indicators", "show warning before quitting",
        "syntax highlighting for commands", "syntax highlighting",
        "tab indicators", "show sticky command header",
        "settings sync", "empty session", "secret redaction",
        "sticky command header", "vim keybindings",
    }
    if name_lower in _settings_toggle_phrases:
        return False
    # Ends with common non-command suffixes
    if name.endswith(".") or name.endswith("…"):
        return False
    return True


def extract_command_palette_refs(file_path: Path) -> List[Dict[str, Any]]:
    """Extract Command Palette command name references from a markdown file."""
    results = []
    try:
        text = file_path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return results

    lines = text.splitlines()
    for line_num, line in enumerate(lines, start=1):
        # Check if "Command Palette" is mentioned nearby (within 2 lines)
        context_start = max(0, line_num - 3)
        context_end = min(len(lines), line_num + 1)
        context = " ".join(lines[context_start:context_end])
        has_palette_context = "command palette" in context.lower()

        # Pattern: Command Palette > CommandName
        for match in RE_CMD_PALETTE_ARROW.finditer(line):
            name = match.group(1).strip()
            if _is_plausible_command_name(name):
                results.append({
                    "file": str(file_path),
                    "line": line_num,
                    "name": name,
                    "pattern": "arrow",
                    "line_text": line,
                })

        # Pattern: quoted strings near Command Palette mention
        if has_palette_context:
            for match in RE_CMD_PALETTE_QUOTED.finditer(line):
                name = match.group(1).strip()
                if _is_plausible_command_name(name):
                    # Skip if preceded by a UI action keyword (toggle, click, etc.)
                    # — these are toggle/button labels, not CP commands
                    prefix = line[:match.start()]
                    if _RE_UI_LABEL_PREFIX.search(prefix):
                        continue
                    # Skip if already captured by arrow pattern
                    if not any(
                        r["line"] == line_num and r["name"] == name
                        for r in results
                    ):
                        results.append({
                            "file": str(file_path),
                            "line": line_num,
                            "name": name,
                            "pattern": "quoted",
                            "line_text": line,
                        })

    return results


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def _best_fuzzy_match(needle: str, haystack: List[str]) -> Tuple[Optional[str], float]:
    """Find the best fuzzy match for needle in haystack."""
    best_match = None
    best_score = 0.0
    needle_lower = needle.lower()
    for candidate in haystack:
        score = SequenceMatcher(None, needle_lower, candidate.lower()).ratio()
        if score > best_score:
            best_score = score
            best_match = candidate
    return best_match, best_score


def validate_ui_path(path: str, valid_paths: Dict[str, Any]) -> Dict[str, Any]:
    """Validate a single UI path against valid_paths data.

    Returns a dict with keys: valid, issue, suggestion, confidence, fix_type.
    """
    segments = [s.strip() for s in path.split(">")]
    root = segments[0]

    settings = valid_paths.get("settings_sections", {})
    menu_bar = valid_paths.get("macos_menu_bar", {})
    warp_drive = valid_paths.get("warp_drive", {})

    # --- Settings paths ---
    if root == "Settings" and len(segments) >= 2:
        section = segments[1]
        section_names = list(settings.keys())

        # Check section (case-insensitive)
        exact = section in section_names
        if not exact:
            ci_match = next(
                (s for s in section_names if s.lower() == section.lower()), None
            )
            if ci_match:
                return {
                    "valid": False,
                    "issue": f"Case mismatch: \"{section}\" should be \"{ci_match}\"",
                    "suggestion": " > ".join(["Settings", ci_match] + segments[2:]),
                    "confidence": 0.95,
                    "fix_type": "case_mismatch",
                }
            best, score = _best_fuzzy_match(section, section_names)
            if score >= FUZZY_MATCH_THRESHOLD:
                return {
                    "valid": False,
                    "issue": f"\"{section}\" is not a known Settings section",
                    "suggestion": f"Did you mean \"{best}\"? (score: {score:.2f})",
                    "confidence": score,
                    "fix_type": "fuzzy" if score >= AUTO_FIX_THRESHOLD else None,
                }
            return {
                "valid": False,
                "issue": f"\"{section}\" is not a known Settings section",
                "suggestion": f"Valid sections: {', '.join(sorted(section_names))}",
                "confidence": 0.0,
                "fix_type": None,
            }

        # Sub-section validation: only check case mismatches for known sub-sections.
        # Individual toggle/setting names beyond the section level are not captured in
        # valid_paths.json, so we skip validation for unrecognized sub-sections.
        if len(segments) >= 3:
            section_data = settings.get(section, {})
            sub_sections = section_data.get("sub_sections", [])
            sub = segments[2]

            # Exact match — valid
            if sub in sub_sections:
                return {"valid": True, "issue": None, "suggestion": None, "confidence": 1.0, "fix_type": None}

            # Case mismatch against a known sub-section — still flag these
            if sub_sections:
                ci_match = next(
                    (s for s in sub_sections if s.lower() == sub.lower()), None
                )
                if ci_match:
                    return {
                        "valid": False,
                        "issue": f"Case mismatch: \"{sub}\" should be \"{ci_match}\"",
                        "suggestion": " > ".join(["Settings", section, ci_match] + segments[3:]),
                        "confidence": 0.95,
                        "fix_type": "case_mismatch",
                    }

            # Unrecognized sub-section — skip (likely a toggle/setting name)
            return {"valid": True, "issue": None, "suggestion": None, "confidence": 0.8, "fix_type": None}

        return {"valid": True, "issue": None, "suggestion": None, "confidence": 1.0, "fix_type": None}

    # --- macOS menu bar paths ---
    if root in ("File", "View", "Warp") and len(segments) >= 2:
        menu_items = menu_bar.get(root, [])
        item = segments[1]
        if item in menu_items:
            return {"valid": True, "issue": None, "suggestion": None, "confidence": 1.0, "fix_type": None}
        best, score = _best_fuzzy_match(item, menu_items)
        if score >= FUZZY_MATCH_THRESHOLD:
            return {
                "valid": False,
                "issue": f"\"{item}\" is not a known {root} menu item",
                "suggestion": f"Did you mean \"{best}\"? (score: {score:.2f})",
                "confidence": score,
                "fix_type": "fuzzy" if score >= AUTO_FIX_THRESHOLD else None,
            }
        return {
            "valid": False,
            "issue": f"\"{item}\" is not a known {root} menu item",
            "suggestion": f"Valid items: {', '.join(menu_items)}" if menu_items else None,
            "confidence": 0.0,
            "fix_type": None,
        }

    # --- Warp Drive paths ---
    if root in ("Warp Drive", "Personal") and len(segments) >= 2:
        spaces = warp_drive.get("spaces", [])
        object_types = warp_drive.get("object_types", [])
        all_valid = spaces + object_types
        item = segments[1]
        if item in all_valid:
            return {"valid": True, "issue": None, "suggestion": None, "confidence": 1.0, "fix_type": None}
        best, score = _best_fuzzy_match(item, all_valid)
        if score >= FUZZY_MATCH_THRESHOLD:
            return {
                "valid": False,
                "issue": f"\"{item}\" is not a known Warp Drive item",
                "suggestion": f"Did you mean \"{best}\"? (score: {score:.2f})",
                "confidence": score,
                "fix_type": "fuzzy" if score >= AUTO_FIX_THRESHOLD else None,
            }
        return {
            "valid": False,
            "issue": f"\"{item}\" is not a known Warp Drive item",
            "suggestion": f"Valid items: {', '.join(sorted(all_valid))}",
            "confidence": 0.0,
            "fix_type": None,
        }

    # Single-segment root — valid if it's a known root
    if root in WARP_UI_ROOTS and len(segments) == 1:
        return {"valid": True, "issue": None, "suggestion": None, "confidence": 1.0, "fix_type": None}

    return {"valid": True, "issue": None, "suggestion": None, "confidence": 0.5, "fix_type": None}


def validate_command_name(name: str, valid_paths: Dict[str, Any]) -> Dict[str, Any]:
    """Validate a Command Palette name against valid_paths data."""
    commands = valid_paths.get("command_palette_commands", [])
    descriptions = [c["description"] for c in commands]

    # Exact match
    if name in descriptions:
        return {"valid": True, "issue": None, "suggestion": None, "confidence": 1.0}

    # Case-insensitive match
    ci_match = next((d for d in descriptions if d.lower() == name.lower()), None)
    if ci_match:
        return {
            "valid": False,
            "issue": f"Case mismatch: \"{name}\" should be \"{ci_match}\"",
            "suggestion": ci_match,
            "confidence": 0.95,
        }

    # Fuzzy match
    best, score = _best_fuzzy_match(name, descriptions)
    if score >= FUZZY_MATCH_THRESHOLD:
        return {
            "valid": False,
            "issue": f"\"{name}\" is not a known Command Palette command",
            "suggestion": f"Did you mean \"{best}\"? (score: {score:.2f})",
            "confidence": score,
        }

    return {
        "valid": False,
        "issue": f"\"{name}\" is not a known Command Palette command",
        "suggestion": None,
        "confidence": 0.0,
    }


# ---------------------------------------------------------------------------
# Format consistency checking
# ---------------------------------------------------------------------------

# Formats that are NOT canonical
_NON_CANONICAL_FORMATS = {"backtick", "seg_backtick", "bold", "italic", "bare"}


def check_format_issues(all_refs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Check extracted UI path refs for non-canonical formatting.

    Canonical format is per-segment bold: **Settings** > **AI** > **Active AI**
    """
    issues = []
    for ref in all_refs:
        fmt = ref["format"]
        if fmt not in _NON_CANONICAL_FORMATS:
            continue
        canonical = _to_canonical_format(ref["normalized"])
        issues.append({
            "file": ref["file"],
            "line": ref["line"],
            "raw": ref.get("match_text", ref["raw"]),
            "normalized": ref["normalized"],
            "format": fmt,
            "canonical": canonical,
            "line_text": ref["line_text"],
        })
    return issues


# ---------------------------------------------------------------------------
# UI element format checking
# ---------------------------------------------------------------------------

# Action keywords that imply a clickable UI element follows.
# "press" and "hit" are excluded — they typically precede keyboard keys.
_UI_ACTION_KEYWORDS = {
    "click", "select", "toggle", "enable", "disable",
    "choose", "check", "uncheck", "expand", "collapse",
    "open", "close", "tap",
}

# Regex: action keyword followed by backtick-wrapped text.
# Allows optional prepositions/articles between keyword and backtick:
#   click `Save`, click on `Save`, click the `Save` button
_RE_ACTION_BACKTICK = re.compile(
    r"\b(" + "|".join(_UI_ACTION_KEYWORDS) + r")(?:\s+(?:on|the|a|an))?\s+`([^`]+)`",
    re.IGNORECASE,
)


# Common keyboard key names that should stay in backticks
_KEYBOARD_KEYS = {
    "enter", "return", "tab", "escape", "esc", "space", "backspace", "delete",
    "up", "down", "left", "right", "home", "end", "pageup", "pagedown",
    "f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10", "f11", "f12",
    "fn",
}


def _is_code_like(text: str) -> bool:
    """Return True if backtick content looks like code rather than a UI element."""
    t = text.strip()
    # Known keyboard key names
    if t.lower() in _KEYBOARD_KEYS:
        return True
    # CLI flags and options
    if t.startswith("-") or t.startswith("--"):
        return True
    # Slash commands, file paths
    if t.startswith("/") or t.startswith("."):
        return True
    # Environment variables
    if t.startswith("$"):
        return True
    # Contains code-like characters: (), {}, [], =
    if re.search(r"[(){}\[\]=]", t):
        return True
    # Contains underscores (identifiers) or dots (file extensions, methods)
    if "_" in t or ("." in t and not t.endswith(".")):
        return True
    # Contains backtick-unfriendly patterns: looks like a command or path
    if re.search(r"\S+/\S+", t):  # e.g. owner/repo
        return True
    # All-uppercase with no spaces likely a key or env var (e.g. RIGHT-CLICK, CMD-ENTER)
    if t.replace("-", "").replace("+", "").isupper() and " " not in t:
        return True
    # Keyboard shortcuts: modifier combos (⌘, ⌥, ⌃, Ctrl+, Cmd+, etc.)
    if re.search(r"[⌘⌥⌃⇧↩↑↓←→]", t):
        return True
    if re.search(r"(?i)(ctrl|cmd|alt|shift|option|meta)[+\-]", t):
        return True
    # Single character (likely a key)
    if len(t) == 1:
        return True
    # Looks like inline code: contains :: or ->  (Rust/C++ style)
    if "::" in t or "->" in t:
        return True
    # CamelCase without spaces (e.g. CloudEnvironment, myFunction)
    if " " not in t and re.search(r"[a-z][A-Z]", t):
        return True
    return False


def check_ui_element_format(md_files: List[Path]) -> List[Dict[str, Any]]:
    """Find clickable UI elements in backticks that should be bold.

    Detects patterns like: Click `Save` → should be Click **Save**
    Excludes code-like content (CLI flags, paths, keyboard shortcuts, etc.).
    """
    issues = []
    for md_file in md_files:
        try:
            text = md_file.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue

        in_code_block = False
        for line_num, line in enumerate(text.splitlines(), start=1):
            # Skip fenced code blocks
            stripped = line.strip()
            if stripped.startswith("```"):
                in_code_block = not in_code_block
                continue
            if in_code_block:
                continue
            # Skip HTML comments and hint blocks
            if stripped.startswith("<!--") or stripped.startswith("{%"):
                continue

            for m in _RE_ACTION_BACKTICK.finditer(line):
                element_text = m.group(2).strip()
                if _is_code_like(element_text):
                    continue
                raw = f"`{m.group(2)}`"
                canonical = f"**{element_text}**"
                issues.append({
                    "file": str(md_file),
                    "line": line_num,
                    "raw": raw,
                    "normalized": element_text,
                    "format": "ui_element_backtick",
                    "canonical": canonical,
                    "line_text": line,
                })
    return issues


def apply_format_fixes(format_issues: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Apply auto-fixes to convert non-canonical UI path formats to canonical bold."""
    fixes_by_file: Dict[str, List[Dict[str, Any]]] = {}
    applied = []

    for issue in format_issues:
        file_path = issue["file"]
        fixes_by_file.setdefault(file_path, []).append(issue)

    for file_path, file_issues in fixes_by_file.items():
        try:
            text = Path(file_path).read_text(encoding="utf-8")
            for issue in file_issues:
                old = issue["raw"]
                new = issue["canonical"]
                if old in text:
                    text = text.replace(old, new, 1)
                    applied.append({
                        "file": file_path,
                        "line": issue["line"],
                        "old": old,
                        "new": new,
                    })
            Path(file_path).write_text(text, encoding="utf-8")
        except OSError as e:
            print(f"  Warning: could not fix {file_path}: {e}", file=sys.stderr)

    return applied


# ---------------------------------------------------------------------------
# File scanning
# ---------------------------------------------------------------------------

SKIP_DIRS = {"_book", "node_modules", ".git", "__pycache__"}


def scan_docs(
    docs_dir: Path,
    include_changelog: bool = False,
) -> List[Path]:
    """Collect all .md files under docs_dir, excluding skip dirs."""
    files = []
    for md_file in sorted(docs_dir.rglob("*.md")):
        # Skip directories
        parts = set(md_file.relative_to(docs_dir).parts)
        if parts & SKIP_DIRS:
            continue
        if not include_changelog and "changelog" in parts:
            continue
        files.append(md_file)
    return files


# ---------------------------------------------------------------------------
# Auto-fix
# ---------------------------------------------------------------------------

def apply_fixes(issues: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Apply auto-fixes for high-confidence issues. Returns list of applied fixes."""
    fixes_by_file: Dict[str, List[Dict[str, Any]]] = {}
    applied = []

    for issue in issues:
        fix_type = issue.get("validation", {}).get("fix_type")
        confidence = issue.get("validation", {}).get("confidence", 0)
        suggestion = issue.get("validation", {}).get("suggestion")

        if fix_type == "case_mismatch" and confidence >= AUTO_FIX_THRESHOLD and suggestion:
            file_path = issue["file"]
            fixes_by_file.setdefault(file_path, []).append(issue)

    for file_path, file_issues in fixes_by_file.items():
        try:
            text = Path(file_path).read_text(encoding="utf-8")
            for issue in file_issues:
                old = issue["raw"]
                new = issue["validation"]["suggestion"]
                if old in text:
                    text = text.replace(old, new, 1)
                    applied.append({
                        "file": file_path,
                        "line": issue["line"],
                        "old": old,
                        "new": new,
                    })
            Path(file_path).write_text(text, encoding="utf-8")
        except OSError as e:
            print(f"  Warning: could not fix {file_path}: {e}", file=sys.stderr)

    return applied


# ---------------------------------------------------------------------------
# PR creation
# ---------------------------------------------------------------------------

def create_pr(fixes: List[Dict[str, Any]], repo_root: Path) -> Optional[str]:
    """Create a branch and PR with the applied fixes using gh CLI."""
    if not fixes:
        print("No fixes to commit.")
        return None

    branch = f"fix/ui-refs-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}"
    try:
        subprocess.run(["git", "checkout", "-b", branch], cwd=repo_root, check=True)
        subprocess.run(["git", "add", "-A"], cwd=repo_root, check=True)

        files_changed = {f["file"] for f in fixes}
        commit_msg = (
            f"docs: fix {len(fixes)} UI reference issue(s)\n\n"
            f"Auto-fixed by validate_ui_refs skill.\n"
            f"Files changed: {', '.join(sorted(str(Path(f).relative_to(repo_root)) for f in files_changed))}\n\n"
            f"Co-Authored-By: Oz <oz-agent@warp.dev>"
        )
        subprocess.run(["git", "commit", "-m", commit_msg], cwd=repo_root, check=True)
        subprocess.run(["git", "push", "-u", "origin", branch], cwd=repo_root, check=True)

        # Write PR body to a temp file to avoid shell argument length limits
        pr_body = (
            f"## Summary\n"
            f"Auto-fixed {len(fixes)} UI reference issue(s) found by the `validate_ui_refs` skill.\n\n"
            f"## Changes\n"
            + "\n".join(f"- `{Path(f['file']).relative_to(repo_root)}` line {f['line']}: "
                        f"`{f['old']}` → `{f['new']}`" for f in fixes)
            + f"\n\nCo-Authored-By: Oz <oz-agent@warp.dev>"
        )
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as tmp:
            tmp.write(pr_body)
            body_file = tmp.name

        try:
            result = subprocess.run(
                [
                    "gh", "pr", "create",
                    "--title", f"docs: fix {len(fixes)} UI reference issue(s)",
                    "--body-file", body_file,
                ],
                cwd=repo_root,
                capture_output=True,
                text=True,
            )
        finally:
            os.unlink(body_file)
        if result.returncode == 0:
            pr_url = result.stdout.strip()
            print(f"PR created: {pr_url}")
            return pr_url
        else:
            print(f"Failed to create PR: {result.stderr}", file=sys.stderr)
            return None

    except subprocess.CalledProcessError as e:
        print(f"Git error: {e}", file=sys.stderr)
        return None


# ---------------------------------------------------------------------------
# Slack notification
# ---------------------------------------------------------------------------

def notify_slack(
    report: Dict[str, Any],
    channel: str,
    pr_url: Optional[str] = None,
) -> bool:
    """Post a summary to Slack. Requires SLACK_BOT_TOKEN env var."""
    token = os.environ.get("SLACK_BOT_TOKEN")
    if not token:
        print("Warning: SLACK_BOT_TOKEN not set, skipping Slack notification.", file=sys.stderr)
        return False

    try:
        import requests
    except ImportError:
        print("Warning: requests not installed, skipping Slack notification.", file=sys.stderr)
        return False

    path_issues = report.get("path_issues", [])
    cmd_issues = report.get("command_issues", [])
    fixes = report.get("fixes_applied", [])

    blocks = [
        {
            "type": "header",
            "text": {"type": "plain_text", "text": "📋 UI Reference Validation Report"},
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": (
                    f"*Files scanned:* {report.get('files_scanned', 0)}\n"
                    f"*Path issues:* {len(path_issues)}\n"
                    f"*Command issues:* {len(cmd_issues)}\n"
                    f"*Auto-fixes applied:* {len(fixes)}"
                ),
            },
        },
    ]

    if pr_url:
        blocks.append({
            "type": "section",
            "text": {"type": "mrkdwn", "text": f"*PR:* <{pr_url}|View PR>"},
        })

    if path_issues:
        top_issues = path_issues[:5]
        issue_text = "\n".join(
            f"• `{Path(i['file']).name}:{i['line']}` — {i['validation']['issue']}"
            for i in top_issues
        )
        if len(path_issues) > 5:
            issue_text += f"\n_...and {len(path_issues) - 5} more_"
        blocks.append({
            "type": "section",
            "text": {"type": "mrkdwn", "text": f"*Top path issues:*\n{issue_text}"},
        })

    resp = requests.post(
        "https://slack.com/api/chat.postMessage",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json={"channel": channel, "blocks": blocks},
        timeout=10,
    )
    data = resp.json()
    if resp.ok and data.get("ok"):
        print(f"Slack notification sent to channel {channel}.")
        return True
    else:
        error = data.get("error", resp.status_code)
        print(f"Slack notification failed: {error}", file=sys.stderr)
        return False


# ---------------------------------------------------------------------------
# Refresh valid_paths.json from warp-internal
# ---------------------------------------------------------------------------

def refresh_valid_paths(warp_internal_path: Path, output_path: Path) -> None:
    """Re-extract valid paths from warp-internal Rust sources and save to JSON."""
    print(f"Refreshing valid_paths.json from {warp_internal_path}...")

    settings_sections = _extract_settings_sections(warp_internal_path)
    command_palette = _extract_command_palette_commands(warp_internal_path)

    # Load existing for menu bar and warp drive (manual lists)
    existing = {}
    if output_path.exists():
        existing = load_valid_paths(output_path)

    data = {
        "settings_sections": settings_sections,
        "macos_menu_bar": existing.get("macos_menu_bar", {}),
        "warp_drive": existing.get("warp_drive", {}),
        "command_palette_commands": command_palette,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }

    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Wrote {output_path} ({len(settings_sections)} sections, {len(command_palette)} commands)")


def _extract_settings_sections(warp_internal: Path) -> Dict[str, Any]:
    """Parse SettingsSection enum and sub-sections from Rust source files."""
    mod_rs = warp_internal / "app" / "src" / "settings_view" / "mod.rs"
    sections = {}

    # Parse Display impl for section display names
    display_map = {}
    try:
        mod_text = mod_rs.read_text(encoding="utf-8")
    except OSError:
        print(f"Warning: could not read {mod_rs}", file=sys.stderr)
        return sections

    # Extract SettingsSection variants
    enum_match = re.search(
        r"pub enum SettingsSection\s*\{([^}]+)\}",
        mod_text,
        re.DOTALL,
    )
    if enum_match:
        for variant in re.findall(r"(\w+)", enum_match.group(1)):
            if variant in ("Copy", "Clone", "Debug", "Default", "PartialEq", "default"):
                continue
            display_map[variant] = variant  # default: use variant name

    # Parse Display impl for overrides
    display_impl = re.search(
        r"impl Display for SettingsSection\s*\{.*?fn fmt.*?\{(.*?)\}\s*\}",
        mod_text,
        re.DOTALL,
    )
    if display_impl:
        for m in re.finditer(
            r'SettingsSection::(\w+)\s*=>\s*write!\(f,\s*"([^"]+)"\)',
            display_impl.group(1),
        ):
            display_map[m.group(1)] = m.group(2)

    # Map of source files for sub-sections
    page_files = {
        "AI": "ai_page.rs",
        "Appearance": "appearance_page.rs",
        "Features": "features_page.rs",
        "Warpify": "warpify_page.rs",
        "Code": "code_page.rs",
        "Privacy": "privacy_page.rs",
        "Platform": "platform_page.rs",
    }

    settings_dir = warp_internal / "app" / "src" / "settings_view"

    for variant, display_name in display_map.items():
        source_file = page_files.get(variant, "mod.rs")
        sub_sections = []

        page_path = settings_dir / source_file
        if page_path.exists() and source_file != "mod.rs":
            try:
                page_text = page_path.read_text(encoding="utf-8")
                # Extract Category::new("Name", ...) calls
                for m in re.finditer(r'Category::new\(\s*"([^"]*)"', page_text):
                    name = m.group(1)
                    if name:  # skip empty category names
                        sub_sections.append(name)
                # Extract build_sub_header(appearance, "Name", ...) calls
                for m in re.finditer(r'build_sub_header\(\s*\w+,\s*"([^"]+)"', page_text):
                    name = m.group(1)
                    if name not in sub_sections:
                        sub_sections.append(name)
            except OSError:
                pass

        sections[display_name] = {
            "display_name": display_name,
            "sub_sections": sub_sections,
            "source_file": f"app/src/settings_view/{source_file}",
        }

    return sections


def _extract_command_palette_commands(warp_internal: Path) -> List[Dict[str, str]]:
    """Parse EditableBinding registrations to extract command palette commands."""
    commands = []
    seen_descriptions = set()

    source_files = [
        warp_internal / "app" / "src" / "terminal" / "view" / "init.rs",
        warp_internal / "app" / "src" / "workspace" / "mod.rs",
    ]

    for source_file in source_files:
        if not source_file.exists():
            continue
        try:
            text = source_file.read_text(encoding="utf-8")
        except OSError:
            continue

        # Pattern: EditableBinding::new("name", "description", ...)
        for m in re.finditer(
            r'EditableBinding::new\(\s*"([^"]+)",\s*"([^"]+)"',
            text,
        ):
            name, desc = m.group(1), m.group(2)
            if desc not in seen_descriptions and not desc.startswith("[Debug]"):
                commands.append({"name": name, "description": desc})
                seen_descriptions.add(desc)

        # Pattern: EditableBinding::new("name", BindingDescription::new("description"), ...)
        for m in re.finditer(
            r'EditableBinding::new\(\s*"([^"]+)",\s*BindingDescription::new\("([^"]+)"\)',
            text,
        ):
            name, desc = m.group(1), m.group(2)
            if desc not in seen_descriptions and not desc.startswith("[Debug]"):
                commands.append({"name": name, "description": desc})
                seen_descriptions.add(desc)

    return commands


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------

def generate_report(
    path_issues: List[Dict[str, Any]],
    command_issues: List[Dict[str, Any]],
    format_issues: List[Dict[str, Any]],
    files_scanned: int,
    fixes: List[Dict[str, Any]],
) -> str:
    """Generate a human-readable text report."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    lines = [
        f"=== UI REFERENCE VALIDATION REPORT ===",
        f"Generated: {now}",
        f"Files scanned: {files_scanned}",
        "",
    ]

    if fixes:
        lines.append(f"### AUTO-FIXES APPLIED ({len(fixes)})")
        for fix in fixes:
            rel = Path(fix["file"]).name
            lines.append(f"  ✅ {rel}:{fix['line']}")
            lines.append(f"     {fix['old']} → {fix['new']}")
        lines.append("")

    if path_issues:
        lines.append(f"### SETTINGS PATH ISSUES ({len(path_issues)} found)")
        for issue in path_issues:
            rel = Path(issue["file"]).name
            validation = issue["validation"]
            confidence = validation.get("confidence", 0)
            icon = "⚠️" if confidence >= FUZZY_MATCH_THRESHOLD else "❌"
            lines.append(f"{icon} {validation['issue']}")
            lines.append(f"  {rel}:{issue['line']}")
            lines.append(f"  Path: {issue['normalized']}")
            if validation.get("suggestion"):
                lines.append(f"  Suggestion: {validation['suggestion']}")
            lines.append("")
    else:
        lines.append("### SETTINGS PATH ISSUES (0 found) ✅")
        lines.append("")

    if command_issues:
        lines.append(f"### COMMAND PALETTE ISSUES ({len(command_issues)} found)")
        for issue in command_issues:
            rel = Path(issue["file"]).name
            validation = issue["validation"]
            lines.append(f"❌ UNMATCHED COMMAND")
            lines.append(f"  {rel}:{issue['line']}")
            lines.append(f"  Reference: \"{issue['name']}\"")
            if validation.get("suggestion"):
                lines.append(f"  {validation['suggestion']}")
            lines.append("")
    else:
        lines.append("### COMMAND PALETTE ISSUES (0 found) ✅")
        lines.append("")

    if format_issues:
        lines.append(f"### FORMAT ISSUES ({len(format_issues)} found)")
        for issue in format_issues:
            rel = Path(issue["file"]).name
            lines.append(f"🔧 Non-canonical format ({issue['format']})")
            lines.append(f"  {rel}:{issue['line']}")
            lines.append(f"  Found:    {issue['raw']}")
            lines.append(f"  Expected: {issue['canonical']}")
            lines.append("")
    else:
        lines.append("### FORMAT ISSUES (0 found) ✅")
        lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate UI paths and Command Palette names in Warp docs."
    )
    parser.add_argument("--check-paths", action="store_true", help="Validate Settings menu paths")
    parser.add_argument("--check-commands", action="store_true", help="Validate Command Palette names")
    parser.add_argument("--check-format", action="store_true", help="Check UI path formatting consistency")
    parser.add_argument("--all", action="store_true", help="Run all checks (default)")
    parser.add_argument("--fix", action="store_true", help="Auto-fix high-confidence issues")
    parser.add_argument("--create-pr", action="store_true", help="Create a PR with fixes")
    parser.add_argument("--slack-notify", action="store_true", help="Post results to Slack")
    parser.add_argument("--slack-channel", default=DEFAULT_SLACK_CHANNEL, help="Slack channel ID")
    parser.add_argument("--include-changelog", action="store_true", help="Include changelog/ in scan")
    parser.add_argument("--refresh-valid-paths", action="store_true", help="Re-extract from warp-internal")
    parser.add_argument(
        "--warp-internal-path",
        default=os.environ.get("WARP_INTERNAL_PATH", str(SCRIPT_DIR.parents[2].parent / "warp-internal")),
        help="Path to warp-internal repo",
    )
    parser.add_argument("--valid-paths", default=str(DEFAULT_VALID_PATHS_FILE), help="Path to valid_paths.json")
    parser.add_argument("--docs-dir", default=str(DEFAULT_DOCS_DIR), help="Path to docs directory")
    parser.add_argument("--output", help="Save results to JSON file")

    args = parser.parse_args()

    # Default to --all if no check flags specified
    if not args.check_paths and not args.check_commands and not args.check_format and not args.refresh_valid_paths:
        args.all = True

    valid_paths_file = Path(args.valid_paths)
    warp_internal = Path(args.warp_internal_path)

    # Refresh valid paths if requested
    if args.refresh_valid_paths:
        if not warp_internal.exists():
            print(f"Error: warp-internal not found at {warp_internal}", file=sys.stderr)
            return 1
        refresh_valid_paths(warp_internal, valid_paths_file)
        if not args.all and not args.check_paths and not args.check_commands:
            return 0

    # Load valid paths
    if not valid_paths_file.exists():
        print(f"Error: {valid_paths_file} not found. Run with --refresh-valid-paths first.", file=sys.stderr)
        return 1
    valid_paths = load_valid_paths(valid_paths_file)

    # Scan docs
    docs_dir = Path(args.docs_dir)
    if not docs_dir.exists():
        print(f"Error: docs directory not found at {docs_dir}", file=sys.stderr)
        return 1

    md_files = scan_docs(docs_dir, include_changelog=args.include_changelog)
    print(f"Scanning {len(md_files)} markdown files...")

    path_issues = []
    command_issues = []
    format_issues = []
    all_path_refs = []  # All extracted path refs (for format checking)

    for md_file in md_files:
        # Extract UI paths (needed for both path validation and format checking)
        if args.all or args.check_paths or args.check_format:
            refs = extract_ui_paths(md_file)
            all_path_refs.extend(refs)

            # Check path validity
            if args.all or args.check_paths:
                for ref in refs:
                    validation = validate_ui_path(ref["normalized"], valid_paths)
                    if not validation["valid"]:
                        ref["validation"] = validation
                        path_issues.append(ref)

        # Check Command Palette names
        if args.all or args.check_commands:
            for ref in extract_command_palette_refs(md_file):
                validation = validate_command_name(ref["name"], valid_paths)
                if not validation["valid"]:
                    ref["validation"] = validation
                    command_issues.append(ref)

    # Check format consistency
    if args.all or args.check_format:
        format_issues = check_format_issues(all_path_refs)
        format_issues.extend(check_ui_element_format(md_files))

    # Auto-fix
    fixes = []
    if args.fix:
        if path_issues:
            fixes = apply_fixes(path_issues)
            fixed_keys = {(f["file"], f["line"]) for f in fixes}
            path_issues = [i for i in path_issues if (i["file"], i["line"]) not in fixed_keys]
        if format_issues:
            format_fixes = apply_format_fixes(format_issues)
            fixes.extend(format_fixes)
            fixed_keys = {(f["file"], f["line"]) for f in format_fixes}
            format_issues = [i for i in format_issues if (i["file"], i["line"]) not in fixed_keys]

    # Generate report
    report_text = generate_report(path_issues, command_issues, format_issues, len(md_files), fixes)
    print(report_text)

    # Create PR
    pr_url = None
    if args.create_pr and fixes:
        repo_root = SCRIPT_DIR.parents[2]
        pr_url = create_pr(fixes, repo_root)

    # Save JSON output
    report_data = {
        "files_scanned": len(md_files),
        "path_issues": path_issues,
        "command_issues": command_issues,
        "format_issues": format_issues,
        "fixes_applied": fixes,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
    if args.output:
        with open(args.output, "w") as f:
            json.dump(report_data, f, indent=2, default=str)
        print(f"Results saved to {args.output}")

    # Count remaining (unfixed) issues — used for Slack notification and exit code
    total_issues = len(path_issues) + len(command_issues) + len(format_issues)

    # Slack notification (only when issues found)
    if args.slack_notify and total_issues > 0:
        notify_slack(report_data, args.slack_channel, pr_url)
    elif args.slack_notify:
        print("No issues found — skipping Slack notification.")
    return 1 if total_issues > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
