#!/usr/bin/env python3
"""
Missing Docs Audit Script for Warp Astro Starlight Documentation

Compares documentation coverage against code surfaces in the warp client
repo (the public warpdotdev/warp checkout; a warp-internal checkout also
works) and warp-server to identify gaps, and (in --diff mode) detects surface changes
since the last committed snapshot. Produces a structured JSON report.

Audited surfaces:
  - Feature flags (rollout status via the app/src/features.rs cargo bridge)
  - CLI commands, subcommands (recursive), and per-module long flags
  - Public API routes (router/handlers/public_api gin groups vs OpenAPI spec)
  - Slash commands (static registry)
  - Settings (define_setting! toml_path registry vs all-settings.mdx)
  - Oz web app routes (AgentsApp.tsx) [snapshot/diff only]
  - Server-side agent tools (multi_agent ToolName constants) [snapshot/diff only]
  - Bundled + channel-gated skills [snapshot/diff only]
  - Docs structure (pages missing from the sidebar)
  - Stale doc references (documented settings/keybinding actions removed from code)
  - Docs staleness terminology and surface-map hygiene

Usage:
    python3 .agents/skills/missing_docs/scripts/audit_docs.py
    python3 .agents/skills/missing_docs/scripts/audit_docs.py --category features
    python3 .agents/skills/missing_docs/scripts/audit_docs.py --output report.json
    python3 .agents/skills/missing_docs/scripts/audit_docs.py --diff
    python3 .agents/skills/missing_docs/scripts/audit_docs.py --update-snapshot

Exit codes:
    0 — all requested audits ran (findings may still exist; check the report)
    1 — fatal setup error (docs directory not found, bad arguments)
    2 — one or more audits were SKIPPED (missing repo paths) or an extraction
        sanity guard tripped (a parser returned implausibly few surfaces,
        meaning the code layout changed). Never treat an exit-2 run as a
        clean audit.
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SKIP_DIRECTORIES = {"_book", "node_modules", ".git", ".docs"}

# Directories pruned when walking Rust/Go source trees.
SOURCE_SKIP_DIRECTORIES = {"target", "node_modules", ".git", "vendor", "dist", "build"}

# Mutable holder for the docs repo root, set by main()
DOCS_REPO_ROOT: list = [None]

# Paths to reference files (relative to this script)
SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
SURFACE_MAP_PATH = SKILL_DIR / "references" / "feature_surface_map.md"
STALE_TERMS_PATH = SKILL_DIR / "references" / "stale_terms.md"
DEFAULT_SNAPSHOT_PATH = SKILL_DIR / "references" / "surface_snapshot.json"

SNAPSHOT_SCHEMA_VERSION = 2

# Heading that starts the machine-generated telemetry table in privacy.mdx.
# Matches TELEMETRY_TABLE_HEADING in the release_updates skill's
# update_telemetry.py, which rewrites everything below it. Lowercased because
# the staleness audit reads lowercased doc text.
GENERATED_SECTION_MARKER = "### exhaustive telemetry table"

# Extraction sanity floors: if a parser returns fewer surfaces than this, the
# code layout probably changed and the parser is broken. The audit fails loud
# (exit 2) instead of silently under-reporting.
EXTRACTION_FLOORS = {
    "feature flags": 50,
    "CLI commands": 5,
    "slash commands": 10,
    "API routes": 10,
    "settings": 100,
}

# ---------------------------------------------------------------------------
# Surface map parser
# ---------------------------------------------------------------------------

def parse_surface_map(path: Path) -> dict:
    """Parse the feature_surface_map.md into structured data.

    Duplicate keys within a section are recorded in `duplicates` so map
    hygiene can flag them (the last occurrence silently wins otherwise).
    """
    result = {
        "feature_to_doc": {},
        "cli_to_doc": {},
        "api_to_doc": {},
        "slash_to_doc": {},
        "settings_to_doc": {},
        "ignore_flags": set(),
        "unlisted_ignore": set(),
        "duplicates": [],
    }
    if not path.exists():
        return result

    current_section = None
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            if line.startswith("## Feature flags"):
                current_section = "features"
            elif line.startswith("## CLI commands"):
                current_section = "cli"
            elif line.startswith("## API endpoints"):
                current_section = "api"
            elif line.startswith("## Slash commands"):
                current_section = "slash"
            elif line.startswith("## Settings"):
                current_section = "settings"
            elif line.startswith("## Flags to ignore"):
                current_section = "ignore"
            elif line.startswith("## Unlisted docs pages"):
                current_section = "unlisted"
            continue

        if current_section == "ignore":
            if line in result["ignore_flags"]:
                result["duplicates"].append(("Flags to ignore", line))
            result["ignore_flags"].add(line)
            continue
        if current_section == "unlisted":
            if line in result["unlisted_ignore"]:
                result["duplicates"].append(("Unlisted docs pages", line))
            result["unlisted_ignore"].add(line)
            continue

        if " -> " in line:
            key, doc_path = line.split(" -> ", 1)
            key = key.strip()
            doc_path = doc_path.strip()
            section_targets = {
                "features": ("Feature flags", result["feature_to_doc"]),
                "cli": ("CLI commands", result["cli_to_doc"]),
                "api": ("API endpoints", result["api_to_doc"]),
                "slash": ("Slash commands", result["slash_to_doc"]),
                "settings": ("Settings", result["settings_to_doc"]),
            }
            if current_section in section_targets:
                section_name, mapping = section_targets[current_section]
                if key in mapping:
                    result["duplicates"].append((section_name, key))
                mapping[key] = doc_path

    return result


# Gating statuses that mean "not publicly released" — a `gated:<Flag>` surface
# whose flag has one of these statuses is intentionally deferred (undocumented).
_NON_GA_STATUSES = ("preview", "dogfood", "other")


def _gated_flag(value) -> str | None:
    """Return the gating FeatureFlag name for a `gated:<Flag>` surface-map target.

    `gated:<Flag>` ties a CLI command or API route to its gating feature flag's
    rollout: while the flag is non-GA the surface is intentionally undocumented
    (private/unreleased), and once the flag goes GA the surface auto-surfaces as
    a normal coverage finding. Returns None for plain doc paths and `internal`.
    """
    if isinstance(value, str) and value.startswith("gated:"):
        return value[len("gated:"):].strip()
    return None


def parse_stale_terms(path: Path) -> list[tuple[str, str]]:
    """Parse stale_terms.md into a list of (term, reason) tuples."""
    terms = []
    if not path.exists():
        return terms

    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if " -> " in line:
            term, reason = line.split(" -> ", 1)
            terms.append((term.strip().lower(), reason.strip()))
    return terms

# ---------------------------------------------------------------------------
# Generic helpers
# ---------------------------------------------------------------------------

def find_repo(names: list[str], explicit_path: str | None, repo_root: Path) -> Path | None:
    """Find a source repo by explicit path or as a sibling of the docs repo root.

    Candidate names are tried in order, e.g. docs at /workspace/docs with
    names ["warp", "warp-internal"] -> prefer /workspace/warp (the public
    warpdotdev/warp checkout) and fall back to /workspace/warp-internal.
    """
    if explicit_path:
        p = Path(explicit_path).resolve()
        if p.exists():
            return p
        print(f"Warning: explicit path {explicit_path} does not exist", file=sys.stderr)
        return None

    for name in names:
        sibling = repo_root.parent / name
        if sibling.exists():
            return sibling
    return None


def find_markdown_files(docs_root: Path) -> list[Path]:
    """Recursively find all markdown files under docs_root."""
    files = []
    for root, dirs, filenames in os.walk(docs_root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRECTORIES]
        for f in filenames:
            if f.endswith(".md") or f.endswith(".mdx"):
                files.append(Path(root) / f)
    return sorted(files)


def iter_source_files(roots: list[Path], suffix: str):
    """Yield source files under the given roots, pruning build directories."""
    for root_dir in roots:
        if not root_dir.exists():
            continue
        for root, dirs, filenames in os.walk(root_dir):
            dirs[:] = [d for d in dirs if d not in SOURCE_SKIP_DIRECTORIES
                       and not d.startswith(".")]
            for f in sorted(filenames):
                if f.endswith(suffix):
                    yield Path(root) / f


def read_all_docs_text(docs_root: Path) -> dict[str, str]:
    """Read all doc files into a dict of {relative_path: content} (lowercased)."""
    result = {}
    for f in find_markdown_files(docs_root):
        try:
            rel = str(f.relative_to(docs_root.parent))  # relative to docs root
            result[rel] = f.read_text(encoding="utf-8").lower()
        except Exception:
            pass
    return result


_FENCED_CODE_RE = re.compile(r"```.*?```", re.DOTALL)
_INLINE_CODE_RE = re.compile(r"`[^`\n]*`")
_HTML_CODE_RE = re.compile(r"<code>.*?</code>", re.DOTALL | re.IGNORECASE)
# The `(...)` destination of a markdown link or image. The `[...]` label is
# left alone — that half is prose.
_LINK_TARGET_RE = re.compile(r"\]\([^)\s]*\)")


def strip_code_spans(text: str) -> str:
    """Remove code spans and link destinations, leaving prose behind.

    Used by the staleness audit so CLI examples (e.g. `oz agent run`) don't
    trigger terminology findings meant for prose. Link and image destinations
    are stripped for the same reason: a URL slug or an asset filename is an
    identifier, not wording a writer can fix. Renaming a published page to
    chase a terminology change would break every inbound link, and image
    filenames are not reader-visible at all, so
    `](/knowledge-and-collaboration/warp-drive/agent-mode-context/)` and
    `](../../assets/terminal/agent-mode-suggestion-1.png)` are noise here.
    Genuinely stale slugs are the `check_for_broken_links` skill's job.
    """
    text = _FENCED_CODE_RE.sub(" ", text)
    text = _HTML_CODE_RE.sub(" ", text)
    text = _INLINE_CODE_RE.sub(" ", text)
    text = _LINK_TARGET_RE.sub("] ", text)
    return text


def resolve_doc_path(doc_path: str, repo_root: Path) -> Path | None:
    """Return the first existing variant of a mapped doc path.

    The surface map historically used `.md` and `README.md`, but the live
    repo is Astro Starlight (`.mdx` files, `index.mdx` landing pages).
    Treat those variants as equivalent so the audit doesn't flag pages that
    exist under a sibling extension.
    """
    candidates = [repo_root / doc_path]
    if doc_path.endswith(".md"):
        candidates.append(repo_root / (doc_path[:-3] + ".mdx"))
    if doc_path.endswith("README.md"):
        candidates.append(repo_root / doc_path.replace("README.md", "index.mdx"))
        candidates.append(repo_root / doc_path.replace("README.md", "index.md"))
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def camel_to_search_terms(flag_name: str) -> list[str]:
    """Convert a CamelCase flag name into searchable terms.

    e.g. AgentModeComputerUse -> ['agent mode computer use', 'computer use', 'agentmodecomputeruse']
    """
    # Split on camel case boundaries
    words = re.sub(r"([a-z])([A-Z])", r"\1 \2", flag_name).split()
    terms = []

    # Full phrase
    full = " ".join(w.lower() for w in words)
    terms.append(full)

    # Last 2-3 words (the most distinctive part)
    if len(words) > 2:
        terms.append(" ".join(w.lower() for w in words[-2:]))
        terms.append(" ".join(w.lower() for w in words[-3:]))

    # Lowercase concatenated (matches code references)
    terms.append(flag_name.lower())

    # snake_case version
    snake = "_".join(w.lower() for w in words)
    terms.append(snake)

    return list(dict.fromkeys(terms))  # dedupe preserving order


def search_docs_for_terms(docs_text: dict[str, str], terms: list[str]) -> list[str]:
    """Search all docs for any of the given terms. Return matching file paths."""
    matches = []
    for path, content in docs_text.items():
        for term in terms:
            if term in content:
                matches.append(path)
                break
    return matches


def kebab_case(name: str) -> str:
    """PascalCase -> kebab-case: RunCloud -> run-cloud, MCP -> mcp."""
    return re.sub(r"([a-z0-9])([A-Z])", r"\1-\2", name).lower()

# ---------------------------------------------------------------------------
# Rust parsing helpers
# ---------------------------------------------------------------------------

def _extract_enum_block(content: str, enum_name: str) -> str | None:
    """Return the body of `[pub] enum <enum_name> { ... }` using brace matching."""
    match = re.search(rf"(?:pub\s+)?enum {enum_name}\s*\{{", content)
    if not match:
        return None
    start = match.end()
    depth = 1
    i = start
    while i < len(content) and depth > 0:
        if content[i] == "{":
            depth += 1
        elif content[i] == "}":
            depth -= 1
        i += 1
    return content[start:i - 1]


def _parse_enum_variants(enum_body: str) -> list[dict]:
    """Parse top-level variants of a Rust enum body.

    Returns [{"name", "hidden", "subcommand", "referenced_type"}].
    Tracks brace/paren depth so struct-variant fields aren't mistaken for
    variants, and reads `hide = true` / `#[command(subcommand)]` from the
    attributes stacked above each variant.
    """
    variants = []
    depth = 0
    pending_attrs: list[str] = []
    for raw_line in enum_body.splitlines():
        line = raw_line.strip()
        if depth == 0:
            if line.startswith("#["):
                pending_attrs.append(line)
            elif line.startswith("///") or line.startswith("//") or not line:
                pass
            else:
                match = re.match(r"^([A-Z]\w*)\s*(\(|\{|,|$)", line)
                if match:
                    name = match.group(1)
                    attrs = " ".join(pending_attrs)
                    ref_match = re.search(r"\(\s*(?:crate::)?([\w:]+)\s*\)", line)
                    variants.append({
                        "name": name,
                        "hidden": "hide = true" in attrs,
                        "subcommand": "subcommand" in attrs,
                        "referenced_type": ref_match.group(1) if ref_match else None,
                    })
                    pending_attrs = []
        depth += raw_line.count("{") - raw_line.count("}")
        depth += raw_line.count("(") - raw_line.count(")")
        depth = max(depth, 0)
    return variants


def _enclosing_brace_block(content: str, idx: int) -> str:
    """Return the innermost `{...}` block containing the given index.

    Heuristic brace matching (does not understand string literals), good
    enough for the macro-invocation blocks it is used on.
    """
    depth = 0
    start = None
    i = idx
    while i >= 0:
        c = content[i]
        if c == "}":
            depth += 1
        elif c == "{":
            if depth == 0:
                start = i
                break
            depth -= 1
        i -= 1
    if start is None:
        return content[max(0, idx - 500):idx + 500]
    depth = 0
    j = start
    while j < len(content):
        if content[j] == "{":
            depth += 1
        elif content[j] == "}":
            depth -= 1
            if depth == 0:
                return content[start:j + 1]
        j += 1
    return content[start:]


def _iter_attr_blocks(content: str, names: tuple[str, ...]):
    """Yield full `#[name(...)]` attribute blocks, paren-matched."""
    pattern = re.compile(r"#\[(" + "|".join(names) + r")\(")
    for match in pattern.finditer(content):
        start = match.end()
        depth = 1
        i = start
        while i < len(content) and depth > 0:
            if content[i] == "(":
                depth += 1
            elif content[i] == ")":
                depth -= 1
            i += 1
        yield content[match.start():i]

# ---------------------------------------------------------------------------
# Extraction: feature flags (warp client repo)
# ---------------------------------------------------------------------------

def _features_lib_rs(warp_repo: Path) -> Path | None:
    candidates = [
        warp_repo / "crates" / "warp_features" / "src" / "lib.rs",
        warp_repo / "crates" / "warp_core" / "src" / "features.rs",
        warp_repo / "app" / "src" / "features.rs",
        warp_repo / "warp_core" / "src" / "features.rs",
    ]
    return next((c for c in candidates if c.exists()), None)


def parse_feature_flags(warp_repo: Path) -> list[str]:
    """Parse FeatureFlag enum variants from the features lib (brace-safe)."""
    features_rs = _features_lib_rs(warp_repo)
    if features_rs is None:
        print("Warning: FeatureFlag enum source not found in the warp client repo", file=sys.stderr)
        return []

    enum_body = _extract_enum_block(features_rs.read_text(), "FeatureFlag")
    if enum_body is None:
        print("Warning: FeatureFlag enum not found", file=sys.stderr)
        return []
    return [v["name"] for v in _parse_enum_variants(enum_body)]


def parse_flag_list_const(warp_repo: Path, const_name: str) -> set[str]:
    """Parse a `pub const <NAME>: &[FeatureFlag] = &[...]` block into flag names."""
    features_rs = _features_lib_rs(warp_repo)
    if features_rs is None:
        return set()
    content = features_rs.read_text()
    match = re.search(
        rf"const\s+{const_name}\s*:\s*&\[FeatureFlag\]\s*=\s*&\[(.*?)\];",
        content,
        re.DOTALL,
    )
    if not match:
        return set()
    return set(re.findall(r"FeatureFlag::(\w+)", match.group(1)))


def parse_features_bridge(warp_repo: Path) -> dict[str, dict]:
    """Parse the cargo-feature -> FeatureFlag bridge from the warp client repo\'s app/src/features.rs.

    The authoritative mapping is the `enabled_features()` extend block:

        #[cfg(feature = "am_workflows")]
        FeatureFlag::AgentModeWorkflows,

    Names frequently differ from a naive snake_case conversion, so this
    bridge (not string transformation) decides which cargo feature gates a
    flag. Entries gated on `debug_assertions` are never GA.

    Returns {flag_name: {"cargo_feature": str, "debug_only": bool}}.
    """
    bridge_rs = warp_repo / "app" / "src" / "features.rs"
    if not bridge_rs.exists():
        print(f"Warning: {bridge_rs} not found; GA detection will be incomplete",
              file=sys.stderr)
        return {}

    content = bridge_rs.read_text()
    bridge: dict[str, dict] = {}
    for match in re.finditer(
        r"#\[cfg\(([^]]*?feature\s*=\s*\"(\w+)\"[^]]*?)\)\]\s*FeatureFlag::(\w+)",
        content,
    ):
        cfg_expr, cargo_feature, flag = match.group(1), match.group(2), match.group(3)
        bridge[flag] = {
            "cargo_feature": cargo_feature,
            "debug_only": "debug_assertions" in cfg_expr,
        }
    return bridge


def parse_default_features(warp_repo: Path) -> set[str]:
    """Parse the default feature list from app/Cargo.toml."""
    candidates = [
        warp_repo / "app" / "Cargo.toml",
        warp_repo / "crates" / "warp_features" / "Cargo.toml",
    ]
    cargo_toml = next((c for c in candidates if c.exists()), None)
    if cargo_toml is None:
        print(f"Warning: app/Cargo.toml not found. Tried: {[str(c) for c in candidates]}",
              file=sys.stderr)
        return set()

    content = cargo_toml.read_text()
    match = re.search(r'default\s*=\s*\[(.*?)\]', content, re.DOTALL)
    if not match:
        return set()

    features_block = match.group(1)
    return set(re.findall(r'"(\w+)"', features_block))


def compute_flag_statuses(warp_repo: Path) -> dict[str, str]:
    """Classify every FeatureFlag by rollout status.

    - "ga": gating cargo feature is in app/Cargo.toml default features, or the
      flag is in RELEASE_FLAGS (enabled for all release builds).
    - "preview": in PREVIEW_FLAGS (Preview builds; launching soon).
    - "dogfood": in DOGFOOD_FLAGS (dev team only).
    - "other": none of the above (runtime/experiment-gated or unused). These
      may still be enabled via server-side experiments; the docs changelog
      cross-check covers those launches.
    """
    flags = parse_feature_flags(warp_repo)
    bridge = parse_features_bridge(warp_repo)
    default_features = parse_default_features(warp_repo)
    release_flags = parse_flag_list_const(warp_repo, "RELEASE_FLAGS")
    preview_flags = parse_flag_list_const(warp_repo, "PREVIEW_FLAGS")
    dogfood_flags = parse_flag_list_const(warp_repo, "DOGFOOD_FLAGS")

    statuses: dict[str, str] = {}
    for flag in flags:
        info = bridge.get(flag)
        is_ga = flag in release_flags
        if info and not info["debug_only"] and info["cargo_feature"] in default_features:
            is_ga = True
        if is_ga:
            statuses[flag] = "ga"
        elif flag in preview_flags:
            statuses[flag] = "preview"
        elif flag in dogfood_flags:
            statuses[flag] = "dogfood"
        else:
            statuses[flag] = "other"
    return statuses

# ---------------------------------------------------------------------------
# Extraction: CLI command tree + flags (warp client repo)
# ---------------------------------------------------------------------------

def _resolve_subcommand_enum(module_content: str, referenced_type: str | None) -> str | None:
    """Find the enum body holding a variant's subcommands within a module file.

    Handles both direct enum references (AgentCommand) and the struct-wrapper
    pattern (ScheduleCommand struct containing `Option<ScheduleSubcommand>`).
    """
    if referenced_type:
        type_name = referenced_type.split("::")[-1]
        body = _extract_enum_block(module_content, type_name)
        if body is not None:
            return body
    # Struct wrapper: look for any Subcommand-derived enum in the module.
    for match in re.finditer(r"#\[derive\([^)]*Subcommand[^)]*\)\]", module_content):
        tail = module_content[match.end():]
        enum_match = re.search(r"pub enum (\w+)", tail[:300])
        if enum_match:
            return _extract_enum_block(module_content, enum_match.group(1))
    return None


def _collect_subcommands(src_dir: Path, module_content: str, enum_body: str,
                         prefix: str, parent_hidden: bool, depth: int) -> list[dict]:
    """Recursively collect subcommands (e.g. `oz environment image list`)."""
    subs = []
    for sub in _parse_enum_variants(enum_body):
        command = f"{prefix} {kebab_case(sub['name'])}"
        hidden = sub["hidden"] or parent_hidden
        subs.append({"command": command, "hidden": hidden})
        if depth >= 3 or not sub["subcommand"]:
            continue
        ref = sub["referenced_type"]
        target_content = module_content
        if ref and "::" in ref:
            module = ref.split("::")[0]
            module_file = src_dir / f"{module}.rs"
            if not module_file.exists():
                continue
            target_content = module_file.read_text()
        nested_body = _resolve_subcommand_enum(target_content, ref)
        if nested_body is not None and nested_body != enum_body:
            subs.extend(_collect_subcommands(
                src_dir, target_content, nested_body, command, hidden, depth + 1))
    return subs


def _cli_src_dir(warp_repo: Path) -> Path | None:
    candidates = [
        warp_repo / "crates" / "warp_cli" / "src",
        warp_repo / "warp_cli" / "src",
    ]
    return next((c for c in candidates if c.exists()), None)


def parse_cli_commands(warp_repo: Path) -> list[dict]:
    """Parse the full `oz` CLI command tree (recursive subcommands).

    Returns [{"command": "oz agent", "hidden": bool, "source_file": str,
              "module": str|None,
              "subcommands": [{"command": "oz agent run", "hidden": bool}]}]
    """
    src_dir = _cli_src_dir(warp_repo)
    if src_dir is None:
        print("Warning: warp_cli/src not found in the warp client repo", file=sys.stderr)
        return []

    lib_rs = src_dir / "lib.rs"
    if not lib_rs.exists():
        print(f"Warning: {lib_rs} not found", file=sys.stderr)
        return []

    content = lib_rs.read_text()
    enum_body = _extract_enum_block(content, "CliCommand")
    if enum_body is None:
        print("Warning: CliCommand enum not found in warp_cli/src/lib.rs", file=sys.stderr)
        return []

    commands = []
    for variant in _parse_enum_variants(enum_body):
        cmd_name = kebab_case(variant["name"])
        entry = {
            "command": f"oz {cmd_name}",
            "hidden": variant["hidden"],
            "source_file": None,
            "module": None,
            "subcommands": [],
        }
        ref = variant["referenced_type"]
        if ref and "::" in ref:
            module = ref.split("::")[0]
            module_file = src_dir / f"{module}.rs"
            if module_file.exists():
                entry["source_file"] = f"warp_cli/src/{module}.rs"
                entry["module"] = module
                module_content = module_file.read_text()
                sub_body = _resolve_subcommand_enum(module_content, ref)
                if sub_body is not None:
                    entry["subcommands"] = _collect_subcommands(
                        src_dir, module_content, sub_body,
                        entry["command"], variant["hidden"], depth=1)
        commands.append(entry)
    return commands


def parse_cli_flags(warp_repo: Path, cli_commands: list[dict]) -> dict[str, list[str]]:
    """Extract visible `--long` flags per CLI module for change tracking.

    Attribution of flags to specific subcommands would require full clap
    resolution; per-module sets are stable and sufficient to detect that a
    flag was added or removed (the drift agent then reads the module to see
    which command it belongs to).
    """
    src_dir = _cli_src_dir(warp_repo)
    if src_dir is None:
        return {}

    flags_by_module: dict[str, list[str]] = {}
    modules = sorted({c["module"] for c in cli_commands if c.get("module") and not c["hidden"]})
    for module in modules:
        module_file = src_dir / f"{module}.rs"
        if not module_file.exists():
            continue
        content = module_file.read_text()
        flags: set[str] = set()
        for attr in _iter_attr_blocks(content, ("arg", "clap", "command")):
            if "hide = true" in attr:
                continue
            for m in re.finditer(r'long(?:_flag)?\s*=\s*"([a-z0-9][a-z0-9-]*)"', attr):
                flags.add(f"--{m.group(1)}")
            for m in re.finditer(r'long(?:_flag)?\("([a-z0-9][a-z0-9-]*)"\)', attr):
                flags.add(f"--{m.group(1)}")
        if flags:
            flags_by_module[module] = sorted(flags)
    return flags_by_module

# ---------------------------------------------------------------------------
# Extraction: public API routes (warp-server)
# ---------------------------------------------------------------------------

_GO_FUNC_RE = re.compile(r"^func (\w+)\(([^)]*)\)", re.MULTILINE)
_GO_GROUP_ASSIGN_RE = re.compile(r"(\w+)\s*:?=\s*(\w+)\.Group\(\s*\"([^\"]*)\"")
_GO_ROUTE_RE = re.compile(r"(\w+)\.(GET|POST|PUT|DELETE|PATCH)\(\s*\"([^\"]*)\"")


def _parse_go_functions(content: str) -> dict[str, dict]:
    """Split a Go file into {func_name: {"params": str, "body": str}}."""
    functions = {}
    matches = list(_GO_FUNC_RE.finditer(content))
    for i, match in enumerate(matches):
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(content)
        functions[match.group(1)] = {
            "params": match.group(2),
            "body": content[start:end],
        }
    return functions


def _split_top_level_args(s: str) -> list[str]:
    """Split a Go argument list on top-level commas."""
    args = []
    depth = 0
    cur: list[str] = []
    for ch in s:
        if ch in "([{":
            depth += 1
        elif ch in ")]}":
            depth -= 1
        if ch == "," and depth == 0:
            args.append("".join(cur).strip())
            cur = []
        else:
            cur.append(ch)
    tail = "".join(cur).strip()
    if tail:
        args.append(tail)
    return args


def _is_route_registrar(name: str) -> bool:
    """Whether a Go function name looks like a route-registration helper.

    Matches both the exported `RegisterFooRoutes` entry points and unexported
    helpers like `registerMCPDiscoveryRoutes`, which real handlers use to split
    a large registration function up. Missing the unexported ones silently
    dropped their routes from the audit universe.
    """
    return name.startswith(("Register", "register"))


def _iter_register_calls(body: str):
    """Yield (callee, start_pos, args) for [Rr]egister*(...) calls, paren-matched."""
    for match in re.finditer(r"\b([Rr]egister\w+)\(", body):
        start = match.end()
        depth = 1
        i = start
        while i < len(body) and depth > 0:
            if body[i] == "(":
                depth += 1
            elif body[i] == ")":
                depth -= 1
            i += 1
        yield match.group(1), match.start(), _split_top_level_args(body[start:i - 1])


def _go_param_positions(params: str) -> tuple[int | None, int | None]:
    """Return (router_group_param_index, engine_param_index) for a Go param list."""
    group_idx = None
    engine_idx = None
    for idx, param in enumerate(_split_top_level_args(params)):
        if "*gin.RouterGroup" in param and group_idx is None:
            group_idx = idx
        elif "*gin.Engine" in param and engine_idx is None:
            engine_idx = idx
    return group_idx, engine_idx


def parse_public_api_routes(warp_server: Path) -> list[dict]:
    """Extract public API routes from router/handlers/public_api/*.go.

    Routes are registered via nested gin groups, e.g.:

        group := router.Group("/api/v1")              (public_api.go)
        RegisterAgentMessagingRoutes(group.Group("/agent"), ...)
        messages := group.Group("/messages")          (agent_messaging.go)
        messages.POST("", SendMessageHandler(...))    -> POST /api/v1/agent/messages

    This walks group-variable assignments per registration function and
    resolves caller-passed prefixes via Register* call sites, starting from
    RegisterPublicAPIRoutes. The RouterGroup argument is matched positionally
    against the callee's parameter list (so `RegisterOAuthRoutes(router,
    group, ...)` resolves `group`, not `router`). Gin `:param` segments are
    normalized to OpenAPI-style `{param}`.
    """
    api_dir = warp_server / "router" / "handlers" / "public_api"
    if not api_dir.exists():
        print(f"Warning: {api_dir} not found", file=sys.stderr)
        return []

    functions: dict[str, dict] = {}
    for go_file in sorted(api_dir.glob("*.go")):
        if go_file.name.endswith("_test.go"):
            continue
        for name, fn in _parse_go_functions(go_file.read_text()).items():
            fn["file"] = f"router/handlers/public_api/{go_file.name}"
            functions[name] = fn

    def analyze(fn: dict) -> dict:
        """Resolve a function body to routes/calls relative to its params."""
        group_idx, engine_idx = _go_param_positions(fn["params"])
        param_names = _split_top_level_args(fn["params"])

        def param_name(idx):
            if idx is None or idx >= len(param_names):
                return None
            return param_names[idx].split()[0] if param_names[idx].split() else None

        group_param = param_name(group_idx)
        router_param = param_name(engine_idx)

        # var name -> (base, prefix); base is "PARAM" (caller group) or
        # "ROUTER" (engine root)
        var_bases: dict[str, tuple] = {}
        if group_param:
            var_bases[group_param] = ("PARAM", "")
        if router_param:
            var_bases[router_param] = ("ROUTER", "")

        def resolve_expr(expr: str):
            m = re.fullmatch(r"(\w+)", expr)
            if m:
                return var_bases.get(m.group(1))
            m = re.fullmatch(r"(\w+)\.Group\(\s*\"([^\"]*)\"\s*\)", expr)
            if m:
                base = var_bases.get(m.group(1))
                if base is not None:
                    return (base[0], base[1] + m.group(2))
            return None

        events = []
        for assign in _GO_GROUP_ASSIGN_RE.finditer(fn["body"]):
            events.append(("assign", assign.start(), assign.groups()))
        for route in _GO_ROUTE_RE.finditer(fn["body"]):
            events.append(("route", route.start(), route.groups()))
        for callee, pos, args in _iter_register_calls(fn["body"]):
            events.append(("call", pos, (callee, args)))
        events.sort(key=lambda e: e[1])

        routes = []
        calls = []
        for kind, _pos, payload in events:
            if kind == "assign":
                target, parent, prefix = payload
                base = var_bases.get(parent)
                if base is not None:
                    var_bases[target] = (base[0], base[1] + prefix)
            elif kind == "route":
                var, method, path = payload
                base = var_bases.get(var)
                if base is not None:
                    routes.append((base[0], method, base[1] + path))
            else:  # call
                callee, args = payload
                resolved_args = [resolve_expr(a) for a in args]
                calls.append((callee, resolved_args))
        return {
            "routes": routes,
            "calls": calls,
            "file": fn["file"],
            "group_param_index": group_idx,
        }

    analyzed = {name: analyze(fn) for name, fn in functions.items()}

    # Resolve absolute route prefixes by walking the call graph from
    # RegisterPublicAPIRoutes. ROUTER-based paths are absolute already.
    resolved: list[dict] = []
    visited: set[tuple] = set()
    emitted_fns: set[str] = set()

    def emit(fn_name: str, param_prefix: str):
        info = analyzed.get(fn_name)
        if info is None:
            return
        key = (fn_name, param_prefix)
        if key in visited:
            return
        visited.add(key)
        emitted_fns.add(fn_name)
        for base, method, path in info["routes"]:
            full = (param_prefix + path) if base == "PARAM" else path
            resolved.append({"method": method, "path": full, "file": info["file"]})
        for callee, args in info["calls"]:
            callee_info = analyzed.get(callee)
            if callee_info is None:
                continue
            # Pick the argument that maps to the callee's RouterGroup param;
            # fall back to the first resolvable argument.
            idx = callee_info.get("group_param_index")
            arg = None
            if idx is not None and idx < len(args):
                arg = args[idx]
            if arg is None:
                arg = next((a for a in args if a is not None), None)
            if arg is None:
                continue
            base, prefix = arg
            callee_prefix = (param_prefix + prefix) if base == "PARAM" else prefix
            emit(callee, callee_prefix)

    if "RegisterPublicAPIRoutes" in analyzed:
        emit("RegisterPublicAPIRoutes", "")
    # Any registration function not reachable from the entry point is assumed
    # to hang off the /api/v1 group (conservative default so routes are never
    # silently dropped).
    for fn_name in sorted(analyzed):
        if _is_route_registrar(fn_name) and fn_name not in emitted_fns:
            emit(fn_name, "/api/v1")

    routes = []
    seen = set()
    for route in resolved:
        path = re.sub(r":(\w+)", r"{\1}", route["path"])
        path = re.sub(r"/{2,}", "/", path) or "/"
        key = (route["method"], path)
        if key in seen:
            continue
        seen.add(key)
        routes.append({
            "method": route["method"],
            "path": path,
            "route": f"{route['method']} {path}",
            "file": route["file"],
        })
    routes.sort(key=lambda r: (r["path"], r["method"]))
    return routes


def _normalize_path_params(path: str) -> str:
    """`/agent/runs/{runId}` -> `/agent/runs/{}` (param-name-insensitive)."""
    return re.sub(r"\{[^}]+\}", "{}", path)


def parse_openapi_paths(openapi_text: str) -> set[str]:
    """Extract normalized path keys from the OpenAPI YAML text.

    Path keys containing `{param}` are usually emitted quoted (YAML treats a
    leading `{` as a flow mapping), so both `  /agent/runs:` and
    `  '/agent/runs/{runId}':` must be recognized. Missing the quoted form made
    every parameterized endpoint look absent from the spec.
    """
    paths = set()
    for match in re.finditer(r"""(?m)^\s{2}(?:'(/[^']+)'|"(/[^"]+)"|(/[^\s:'"]+)):""", openapi_text):
        path = match.group(1) or match.group(2) or match.group(3)
        paths.add(_normalize_path_params(path))
    return paths

# ---------------------------------------------------------------------------
# Extraction: slash commands (warp client repo)
# ---------------------------------------------------------------------------

def parse_slash_commands(warp_repo: Path) -> list[str]:
    """Parse static slash command names from the registry."""
    registry_dir = (
        warp_repo / "app" / "src" / "search" / "slash_command_menu" / "static_commands"
    )
    if not registry_dir.exists():
        print(f"Warning: {registry_dir} not found", file=sys.stderr)
        return []

    names: set[str] = set()
    for rs_file in sorted(registry_dir.glob("*.rs")):
        if rs_file.name.endswith("_tests.rs"):
            continue
        for match in re.finditer(r'name:\s*"(/[a-z0-9][a-z0-9-]*)"', rs_file.read_text()):
            names.add(match.group(1))
    return sorted(names)

# ---------------------------------------------------------------------------
# Extraction: settings (warp client repo)
# ---------------------------------------------------------------------------

_SETTING_TOML_PATH_RE = re.compile(r'toml_path:\s*"([^"]+)"')


def _is_test_rs(path: Path) -> bool:
    return path.name.endswith("_tests.rs") or path.name == "tests.rs" or "/tests/" in str(path)


def parse_settings(warp_repo: Path) -> dict[str, dict]:
    """Parse user-facing settings from `define_setting!`-style registrations.

    Every settings.toml-backed setting declares `toml_path: "section.key"`
    in its registration block, alongside `private:` and (optionally)
    `feature_flag:`. This is the same metadata the JSON-schema generator
    (app/src/bin/generate_settings_schema.rs) consumes via inventory.

    Returns {toml_path: {"private": bool, "feature_flag": str|None}}.
    """
    settings: dict[str, dict] = {}
    roots = [warp_repo / "app" / "src", warp_repo / "crates"]
    for rs_file in iter_source_files(roots, ".rs"):
        if _is_test_rs(rs_file):
            continue
        # The macro definition file contains `toml_path:` in doc examples.
        if rs_file.name == "macros.rs" and rs_file.parent.name == "src" \
                and rs_file.parent.parent.name == "settings":
            continue
        try:
            content = rs_file.read_text(encoding="utf-8")
        except Exception:
            continue
        if "toml_path:" not in content:
            continue
        for match in _SETTING_TOML_PATH_RE.finditer(content):
            toml_path = match.group(1)
            block = _enclosing_brace_block(content, match.start())
            flag_match = re.search(
                r"feature_flag:\s*(?:Some\()?\s*(?:[\w:]*::)?FeatureFlag::(\w+)", block)
            entry = {
                "private": re.search(r"private:\s*true", block) is not None,
                "feature_flag": flag_match.group(1) if flag_match else None,
            }
            existing = settings.get(toml_path)
            if existing:
                # Same setting registered per-platform: private if any
                # registration is private; keep the first flag seen.
                entry["private"] = entry["private"] or existing["private"]
                entry["feature_flag"] = existing["feature_flag"] or entry["feature_flag"]
            settings[toml_path] = entry
    return settings


def setting_status(info: dict, flag_statuses: dict[str, str]) -> str:
    """Classify a setting: private | always_on | ga | preview | dogfood | other | unknown_flag."""
    if info["private"]:
        return "private"
    flag = info["feature_flag"]
    if flag is None:
        return "always_on"
    return flag_statuses.get(flag, "unknown_flag")


def parse_settings_doc(docs_root: Path) -> tuple[dict[str, set[str]], Path | None]:
    """Parse all-settings.mdx into {toml_section: {keys}}.

    The reference page lists `**Section**: `[a.b]`` headers followed by
    `* `key` — ...` bullets.
    """
    page = docs_root / "terminal" / "settings" / "all-settings.mdx"
    sections: dict[str, set[str]] = {}
    if not page.exists():
        return sections, None
    current = ""
    for line in page.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        header = re.match(r"\*\*Section\*\*:\s*`\[([^\]]+)\]`", stripped)
        if header:
            current = header.group(1)
            sections.setdefault(current, set())
            continue
        bullet = re.match(r"^\*\s+`([A-Za-z0-9_]+)`", stripped)
        if bullet:
            sections.setdefault(current, set()).add(bullet.group(1))
    return sections, page

# ---------------------------------------------------------------------------
# Extraction: snapshot-only surfaces (web app, tools, bundled skills)
# ---------------------------------------------------------------------------

def parse_webapp_routes(warp_server: Path) -> list[str]:
    """Parse Oz web app route paths from the agents package router."""
    app_tsx = warp_server / "client" / "packages" / "agents" / "src" / "AgentsApp.tsx"
    if not app_tsx.exists():
        print(f"Warning: {app_tsx} not found", file=sys.stderr)
        return []
    paths = set(re.findall(r'path="([^"]+)"', app_tsx.read_text(encoding="utf-8")))
    paths.discard("*")
    return sorted(paths)


def parse_server_tools(warp_server: Path) -> list[str]:
    """Parse agent tool names from the multi_agent tool registries.

    Two definition styles exist:
    - `xToolName = "tool_name"` constants
    - `native_tools.Create*NativeTool[...]("tool_name", ...)` registrations
      (the canonical registry in native_tools/shared/shared_tools.go)
    """
    base = warp_server / "logic" / "ai" / "multi_agent"
    if not base.exists():
        print(f"Warning: {base} not found", file=sys.stderr)
        return []
    names: set[str] = set()
    native_tool_re = re.compile(
        r'Create\w*NativeTool\[[^\]]*\]\(\s*"([a-z0-9_]+)"', re.DOTALL)
    for go_file in iter_source_files([base], ".go"):
        if go_file.name.endswith("_test.go"):
            continue
        try:
            content = go_file.read_text(encoding="utf-8")
        except Exception:
            continue
        for match in re.finditer(r'ToolName\s*=\s*"([a-z0-9_]+)"', content):
            names.add(match.group(1))
        for match in native_tool_re.finditer(content):
            names.add(match.group(1))
    return sorted(names)


def parse_bundled_skills(warp_repo: Path) -> dict[str, str]:
    """List bundled skills shipped with the client, keyed by channel gating.

    resources/bundled/skills/<name> ships on all channels ("bundled");
    resources/channel-gated-skills/<channel>/<name> ships per channel.
    """
    skills: dict[str, str] = {}
    bundled = warp_repo / "resources" / "bundled" / "skills"
    if bundled.exists():
        for entry in sorted(bundled.iterdir()):
            if entry.is_dir():
                skills[entry.name] = "bundled"
    gated = warp_repo / "resources" / "channel-gated-skills"
    if gated.exists():
        for channel_dir in sorted(gated.iterdir()):
            if not channel_dir.is_dir():
                continue
            for entry in sorted(channel_dir.iterdir()):
                if entry.is_dir():
                    skills[entry.name] = channel_dir.name
    return skills

# ---------------------------------------------------------------------------
# Extraction: docs sidebar + changelog
# ---------------------------------------------------------------------------

def parse_sidebar_slugs(repo_root: Path) -> set[str] | None:
    """Parse referenced page slugs from src/sidebar.ts.

    Entries appear either as bare string items ('terminal/blocks/find'),
    `slug: '...'` objects, or topic `link: '/...'` values.
    Returns None when the sidebar file cannot be found (callers should skip
    the structure audit rather than reporting everything unlisted).
    """
    sidebar = repo_root / "src" / "sidebar.ts"
    if not sidebar.exists():
        return None
    slugs: set[str] = set()
    for line in sidebar.read_text(encoding="utf-8").splitlines():
        stripped = line.strip().rstrip(",")
        bare = re.fullmatch(r"'([a-z0-9][a-z0-9/-]*)'", stripped)
        if bare:
            slugs.add(bare.group(1))
            continue
        for match in re.finditer(r"slug:\s*'([^']+)'", line):
            slugs.add(match.group(1).strip("/"))
        for match in re.finditer(r"link:\s*'([^']*)'", line):
            slugs.add(match.group(1).strip("/"))
    return slugs


def page_slug(md_file: Path, docs_root: Path) -> str:
    """Compute the Starlight slug for a docs page (frontmatter override aware)."""
    try:
        head = md_file.read_text(encoding="utf-8")[:2000]
        override = re.search(r"(?m)^slug:\s*['\"]?([^'\"\n]+)['\"]?\s*$", head)
        if override:
            return override.group(1).strip().strip("/")
    except Exception:
        pass
    rel = md_file.relative_to(docs_root)
    slug = str(rel)
    for ext in (".mdx", ".md"):
        if slug.endswith(ext):
            slug = slug[: -len(ext)]
    if slug.endswith("/index"):
        slug = slug[: -len("/index")]
    elif slug == "index":
        slug = ""
    return slug


_CHANGELOG_HEADER_RE = re.compile(r"^### (\d{4}\.\d{2}\.\d{2})", re.MULTILINE)
# "Bug fixes" is deliberately untracked: fix bullets rarely create doc surface
# and would double the weekly triage volume.
_CHANGELOG_TRACKED_SECTIONS = ("new features", "improvements", "oz updates")


def parse_changelog_entries(repo_root: Path) -> list[dict]:
    """Parse release entries from src/content/docs/changelog/<year>.mdx.

    Returns [{"version": "2026.06.03", "file": str, "items":
              [{"category": "new features", "text": str}]}] sorted newest first.
    "New features", "Improvements", and "Oz updates" bullets are tracked —
    the sections that may represent undocumented feature launches.
    """
    changelog_dir = repo_root / "src" / "content" / "docs" / "changelog"
    if not changelog_dir.exists():
        return []

    entries = []
    for mdx in sorted(changelog_dir.glob("*.mdx")):
        if not re.fullmatch(r"\d{4}", mdx.stem):
            continue
        content = mdx.read_text(encoding="utf-8")
        headers = list(_CHANGELOG_HEADER_RE.finditer(content))
        for i, header in enumerate(headers):
            end = headers[i + 1].start() if i + 1 < len(headers) else len(content)
            body = content[header.end():end]
            items = []
            current_section = None
            for line in body.splitlines():
                stripped = line.strip()
                section_match = re.match(r"^\*\*(.+?)\*\*$", stripped)
                if section_match:
                    current_section = section_match.group(1).strip().lower()
                    continue
                if current_section in _CHANGELOG_TRACKED_SECTIONS and stripped.startswith("* "):
                    items.append({
                        "category": current_section,
                        "text": stripped[2:].strip(),
                    })
            entries.append({
                "version": header.group(1),
                "file": str(mdx.relative_to(repo_root)),
                "items": items,
            })
    entries.sort(key=lambda e: e["version"], reverse=True)
    return entries

# ---------------------------------------------------------------------------
# Audit 1: Feature flag coverage
# ---------------------------------------------------------------------------

def audit_features(warp_repo: Path, docs_root: Path, surface_map: dict,
                   docs_text: dict[str, str],
                   flag_statuses: dict[str, str] | None = None,
                   weak_coverage: bool = False) -> list[dict]:
    """Audit feature flag coverage in docs.

    GA flags must be mapped in the surface map (with an existing target page)
    or appear in docs prose. Preview flags produce low-severity "docs needed
    soon" findings when uncovered. Dogfood/other flags are skipped (tracked by
    the snapshot diff instead).
    """
    if flag_statuses is None:
        flag_statuses = compute_flag_statuses(warp_repo)
    ignore_flags = surface_map.get("ignore_flags", set())
    feature_to_doc = surface_map.get("feature_to_doc", {})
    repo_root = DOCS_REPO_ROOT[0] or docs_root.parent.parent.parent

    findings = []
    for flag, status in flag_statuses.items():
        if flag in ignore_flags:
            continue
        if status not in ("ga", "preview"):
            continue

        # Check if mapped in surface map
        if flag in feature_to_doc:
            doc_path = feature_to_doc[flag]
            resolved = resolve_doc_path(doc_path, repo_root)
            if resolved is not None:
                if not weak_coverage:
                    # Surface-map presence is treated as verified — the
                    # maintainer has confirmed the page covers this flag.
                    continue
                # Optional weak-coverage check: verify the target page
                # actually mentions feature keywords.
                try:
                    doc_content = resolved.read_text(encoding="utf-8").lower()
                except Exception:
                    doc_content = ""
                terms = camel_to_search_terms(flag)
                check_terms = [t for t in terms if " " in t or t.startswith("/")]
                if check_terms and not any(t in doc_content for t in check_terms):
                    findings.append({
                        "flag": flag,
                        "status": status,
                        "search_terms": terms,
                        "severity": "low",
                        "suggested_doc_path": doc_path,
                        "reason": (
                            f"Mapped doc {doc_path} exists but does not "
                            "mention feature keywords (weak coverage)"
                        ),
                    })
                continue
            # Mapped path missing — before flagging, fall back to a content
            # search so we don't raise false positives when a doc has merely
            # been moved.
            terms = camel_to_search_terms(flag)
            matches = search_docs_for_terms(docs_text, terms)
            if matches:
                findings.append({
                    "flag": flag,
                    "status": status,
                    "search_terms": terms,
                    "severity": "low",
                    "suggested_doc_path": doc_path,
                    "matched_docs": matches[:3],
                    "reason": (
                        f"Mapped doc {doc_path} does not exist but docs mention the "
                        "feature — update the surface map entry to the new location"
                    ),
                })
                continue
            findings.append({
                "flag": flag,
                "status": status,
                "search_terms": terms,
                "severity": "high",
                "suggested_doc_path": doc_path,
                "reason": f"Mapped doc {doc_path} does not exist",
            })
            continue

        # Not in surface map — search docs for mentions
        terms = camel_to_search_terms(flag)
        matches = search_docs_for_terms(docs_text, terms)
        if matches:
            # Mentioned somewhere but unmapped. The fuzzy match may be a false
            # negative (generic fragments like "slash command" match anything),
            # so surface it as low-severity map work instead of passing silently.
            findings.append({
                "flag": flag,
                "status": status,
                "search_terms": terms,
                "severity": "low",
                "suggested_doc_path": None,
                "matched_docs": matches[:3],
                "reason": (
                    f"{'GA' if status == 'ga' else 'Preview'} flag is unmapped; docs "
                    "may mention it (fuzzy match) — verify coverage and add a surface "
                    "map entry (or move to the ignore list)"
                ),
            })
            continue
        findings.append({
            "flag": flag,
            "status": status,
            "search_terms": terms,
            "severity": "medium" if status == "ga" else "low",
            "suggested_doc_path": None,
            "reason": (
                "GA feature with no doc mentions found"
                if status == "ga"
                else "Preview feature with no doc mentions found — docs needed soon"
            ),
        })

    return findings

# ---------------------------------------------------------------------------
# Audit 2: CLI command coverage
# ---------------------------------------------------------------------------

def audit_cli(warp_repo: Path, docs_root: Path, surface_map: dict,
              docs_text: dict[str, str],
              cli_commands: list[dict] | None = None,
              flag_statuses: dict[str, str] | None = None) -> list[dict]:
    """Audit CLI command and subcommand coverage in docs."""
    commands = cli_commands if cli_commands is not None else parse_cli_commands(warp_repo)
    cli_to_doc = surface_map.get("cli_to_doc", {})
    repo_root = DOCS_REPO_ROOT[0] or docs_root.parent.parent.parent

    # Read all CLI docs content
    cli_docs_dir = docs_root / "reference" / "cli"
    cli_docs_text = {}
    if cli_docs_dir.exists():
        for f in find_markdown_files(cli_docs_dir):
            try:
                cli_docs_text[str(f)] = f.read_text(encoding="utf-8").lower()
            except Exception:
                pass

    def is_covered(cmd_str: str, search_phrase: str) -> bool:
        if cmd_str in cli_to_doc:
            doc_path = cli_to_doc[cmd_str]
            # `internal` is a sentinel for hidden/internal commands that
            # intentionally have no public docs (matches API audit semantics).
            if doc_path == "internal":
                return True
            gflag = _gated_flag(doc_path)
            if gflag is not None:
                # Defer while the gating flag is non-GA; once GA, fall through so
                # the command must be documented (auto-surfaces as a finding).
                if (flag_statuses or {}).get(gflag) in _NON_GA_STATUSES:
                    return True
            elif resolve_doc_path(doc_path, repo_root) is not None:
                return True
        return any(search_phrase in content for content in cli_docs_text.values())

    findings = []
    for cmd in commands:
        if cmd["hidden"]:
            continue
        cmd_str = cmd["command"]
        # e.g. "agent" from "oz agent"
        top_phrase = cmd_str.split(" ", 1)[1]
        if not is_covered(cmd_str, top_phrase):
            findings.append({
                "command": cmd_str,
                "source_file": cmd.get("source_file"),
                "severity": "high",
                "reason": f"CLI command '{cmd_str}' not mentioned in CLI reference docs",
            })
            continue  # Subcommand findings would be redundant noise.
        for sub in cmd["subcommands"]:
            if sub["hidden"]:
                continue
            sub_str = sub["command"]
            sub_phrase = sub_str.split(" ", 1)[1]  # e.g. "agent run-cloud"
            if not is_covered(sub_str, sub_phrase):
                findings.append({
                    "command": sub_str,
                    "source_file": cmd.get("source_file"),
                    "severity": "medium",
                    "reason": (
                        f"CLI subcommand '{sub_str}' not mentioned in CLI "
                        "reference docs"
                    ),
                })

    return findings

# ---------------------------------------------------------------------------
# Audit 3: API endpoint coverage
# ---------------------------------------------------------------------------

def audit_api(warp_server: Path, docs_root: Path, surface_map: dict,
              docs_text: dict[str, str],
              api_routes: list[dict] | None = None,
              flag_statuses: dict[str, str] | None = None) -> list[dict]:
    """Audit public API endpoint coverage in the OpenAPI spec and API docs.

    The public docs API reference (docs.warp.dev/api) renders
    developers/agent-api-openapi.yaml, so a route missing from the spec is a
    docs gap. Spec matching is param-name-insensitive ({runId} == {run_id}).
    Use the warp-server `update-open-api-spec` skill / docs `sync-openapi-spec`
    skill to fix spec drift rather than hand-editing.
    """
    routes = api_routes if api_routes is not None else parse_public_api_routes(warp_server)
    api_to_doc = surface_map.get("api_to_doc", {})

    # Read API docs
    api_docs_dir = docs_root / "reference" / "api-and-sdk"
    api_docs_text = {}
    if api_docs_dir.exists():
        for f in find_markdown_files(api_docs_dir):
            try:
                api_docs_text[str(f)] = f.read_text(encoding="utf-8").lower()
            except Exception:
                pass

    # Also check OpenAPI spec (lives at repo root, not under content/docs)
    repo_root = DOCS_REPO_ROOT[0] or docs_root.parent
    openapi_candidates = [
        repo_root / "developers" / "agent-api-openapi.yaml",
        docs_root / "developers" / "agent-api-openapi.yaml",
    ]
    openapi_path = next((c for c in openapi_candidates if c.exists()), openapi_candidates[0])
    openapi_text = ""
    if openapi_path.exists():
        try:
            openapi_text = openapi_path.read_text(encoding="utf-8").lower()
        except Exception:
            pass
    spec_paths = parse_openapi_paths(openapi_text)

    findings = []
    for route in routes:
        route_str = route["route"]

        # Surface-map entries use the path relative to /api/v1 (e.g.
        # "POST /agent/run"); also accept the full path for compatibility.
        rel_path = route["path"]
        if rel_path.startswith("/api/v1"):
            rel_path = rel_path[len("/api/v1"):] or "/"
        rel_route_str = f"{route['method']} {rel_path}"
        map_val = api_to_doc.get(route_str)
        if map_val is None:
            map_val = api_to_doc.get(rel_route_str)
        if map_val is not None:
            gflag = _gated_flag(map_val)
            if gflag is None:
                continue  # plain doc path or `internal` sentinel: suppressed
            # Defer while the gating flag is non-GA; once GA, fall through so the
            # endpoint must reach the OpenAPI spec (auto-surfaces as a finding).
            if (flag_statuses or {}).get(gflag) in _NON_GA_STATUSES:
                continue

        # Match against the spec's path keys (param-name-insensitive), then
        # fall back to substring search in API docs prose.
        found = (
            _normalize_path_params(rel_path) in spec_paths
            or _normalize_path_params(route["path"]) in spec_paths
        )
        if not found:
            for candidate in {route["path"].lower(), rel_path.lower()}:
                if candidate in openapi_text:
                    found = True
                    break
                if any(candidate in content for content in api_docs_text.values()):
                    found = True
                    break

        if not found:
            findings.append({
                "route": rel_route_str,
                "handler_file": route.get("file"),
                "severity": "medium",
                "reason": (
                    f"Public API endpoint '{rel_route_str}' is missing from the "
                    "OpenAPI spec (developers/agent-api-openapi.yaml) — run the "
                    "sync-openapi-spec skill, or map it as internal in the "
                    "surface map"
                ),
            })

    return findings

# ---------------------------------------------------------------------------
# Audit 4: Slash command coverage
# ---------------------------------------------------------------------------

def _slash_mention_re(name: str) -> re.Pattern:
    # Boundary-aware: "/new" must not match "issues/new"; require the char
    # before "/" to be a non-word char and the name to end at a word boundary.
    return re.compile(r"(?<!\w)" + re.escape(name) + r"(?![\w-])")


def audit_slash_commands(warp_repo: Path, docs_root: Path, surface_map: dict,
                         docs_text: dict[str, str],
                         slash_commands: list[str] | None = None) -> list[dict]:
    """Audit static slash command coverage in docs."""
    names = slash_commands if slash_commands is not None else parse_slash_commands(warp_repo)
    slash_to_doc = surface_map.get("slash_to_doc", {})
    repo_root = DOCS_REPO_ROOT[0] or docs_root.parent.parent.parent

    findings = []
    for name in names:
        if name in slash_to_doc:
            doc_path = slash_to_doc[name]
            if doc_path == "internal":
                continue
            if resolve_doc_path(doc_path, repo_root) is not None:
                continue
        pattern = _slash_mention_re(name)
        if any(pattern.search(content) for content in docs_text.values()):
            continue
        findings.append({
            "command": name,
            "severity": "medium",
            "reason": (
                f"Slash command '{name}' is not mentioned in any docs page — "
                "document it (slash-commands page) or map it as internal"
            ),
        })
    return findings

# ---------------------------------------------------------------------------
# Audit 5: Settings coverage
# ---------------------------------------------------------------------------

def audit_settings(docs_root: Path, surface_map: dict,
                   settings: dict[str, dict],
                   flag_statuses: dict[str, str]) -> list[dict]:
    """Audit settings.toml coverage in the all-settings reference page.

    Private settings are skipped; settings gated by dogfood/other flags are
    tracked by the snapshot instead. Settings gated by a flag the parser
    cannot resolve are flagged conservatively.
    """
    settings_to_doc = surface_map.get("settings_to_doc", {})
    repo_root = DOCS_REPO_ROOT[0] or docs_root.parent.parent.parent
    doc_sections, doc_page = parse_settings_doc(docs_root)
    if doc_page is None:
        return [{
            "setting": "(all)",
            "severity": "high",
            "reason": (
                "all-settings.mdx not found — the settings reference page moved; "
                "update parse_settings_doc() in the audit script"
            ),
        }]

    findings = []
    for toml_path in sorted(settings):
        status = setting_status(settings[toml_path], flag_statuses)
        if status in ("private", "dogfood", "other"):
            continue

        if toml_path in settings_to_doc:
            target = settings_to_doc[toml_path]
            if target == "internal":
                continue
            if resolve_doc_path(target, repo_root) is not None:
                continue

        hierarchy, _, key = toml_path.rpartition(".")
        if key in doc_sections.get(hierarchy, set()):
            continue
        # Object-typed settings are documented as their own section (e.g. the
        # `notifications.preferences` setting appears as a
        # `**Section**: [notifications.preferences]` block of field bullets).
        if toml_path in doc_sections or any(
                section.startswith(toml_path + ".") for section in doc_sections):
            continue

        findings.append({
            "setting": toml_path,
            "status": status,
            "severity": "medium",
            "suggested_doc_path": "src/content/docs/terminal/settings/all-settings.mdx",
            "reason": (
                f"Setting '{toml_path}' ({status}) is not documented in the "
                "all-settings reference — add it under the "
                f"`[{hierarchy or 'top-level'}]` section, or map it as internal"
            ),
        })
    return findings

# ---------------------------------------------------------------------------
# Audit 6: Stale doc references (docs pointing at removed code surfaces)
# ---------------------------------------------------------------------------

def audit_stale_doc_references(warp_repo: Path, docs_root: Path,
                               settings: dict[str, dict]) -> list[dict]:
    """Find doc references to code surfaces that no longer exist.

    - Settings keys documented in all-settings.mdx but absent from the code
      settings registry (renamed/removed settings).
    - Keybinding action names (`scope:action`) documented on the keyboard
      shortcuts page but absent from the warp client repo source.
    """
    findings = []

    # Documented settings that no longer exist in code.
    doc_sections, doc_page = parse_settings_doc(docs_root)
    if doc_page is not None and settings:
        known = set()
        for toml_path in settings:
            hierarchy, _, key = toml_path.rpartition(".")
            known.add((hierarchy, key))

        def is_object_setting_section(section: str) -> bool:
            # Fields of object-typed settings (e.g. keys under the
            # `[notifications.preferences]` section, where the code setting is
            # `notifications.preferences` itself) cannot be validated
            # statically — skip them.
            return any(
                section == code_path or section.startswith(code_path + ".")
                for code_path in settings
            )

        for section, keys in sorted(doc_sections.items()):
            if is_object_setting_section(section):
                continue
            for key in sorted(keys):
                if (section, key) not in known:
                    findings.append({
                        "kind": "setting",
                        "reference": f"{section}.{key}" if section else key,
                        "doc_page": "src/content/docs/terminal/settings/all-settings.mdx",
                        "severity": "low",
                        "reason": (
                            "Documented setting not found in the code settings "
                            "registry — it was renamed or removed; update the "
                            "all-settings page"
                        ),
                    })

    # Documented keybinding actions that no longer exist in code.
    shortcuts_page = docs_root / "getting-started" / "keyboard-shortcuts.mdx"
    if shortcuts_page.exists():
        text = shortcuts_page.read_text(encoding="utf-8")
        actions = sorted(set(re.findall(r"`([a-z0-9_]+:[a-z0-9_]+)`", text)))
        remaining = set(actions)
        if remaining:
            roots = [warp_repo / "app" / "src", warp_repo / "crates"]
            for rs_file in iter_source_files(roots, ".rs"):
                if not remaining:
                    break
                try:
                    content = rs_file.read_text(encoding="utf-8")
                except Exception:
                    continue
                remaining = {a for a in remaining if a not in content}
        for action in sorted(remaining):
            findings.append({
                "kind": "keybinding_action",
                "reference": action,
                "doc_page": "src/content/docs/getting-started/keyboard-shortcuts.mdx",
                "severity": "low",
                "reason": (
                    "Documented keybinding action not found anywhere in "
                    "the warp client repo source — it was renamed or removed; update "
                    "the keyboard shortcuts page"
                ),
            })

    return findings

# ---------------------------------------------------------------------------
# Audit 7: Docs staleness (terminology)
# ---------------------------------------------------------------------------

def audit_staleness(warp_repo: Path, docs_root: Path,
                    docs_text: dict[str, str],
                    stale_terms_path: Path = STALE_TERMS_PATH) -> list[dict]:
    """Check existing docs for stale terminology.

    Code spans and link destinations are stripped first (CLI examples like
    `oz agent run` are legitimate command syntax, not terminology; a URL slug
    is an identifier) and terms match on word boundaries only. Broader
    terminology enforcement is owned by the style_lint skill; this audit only
    flags terms tied to renamed/removed features.
    """
    stale_terms = parse_stale_terms(stale_terms_path)
    term_patterns = [
        (term, reason, re.compile(r"\b" + re.escape(term) + r"\b"))
        for term, reason in stale_terms
    ]

    findings = []
    for doc_path, content in docs_text.items():
        # Historical changelog entries are records of what shipped at the
        # time — old feature names there are correct, not stale.
        if "/changelog/" in doc_path or doc_path.startswith("changelog/"):
            continue
        # The telemetry table is regenerated wholesale from the client's event
        # definitions by the release_updates skill's update_telemetry.py, so
        # its event names and descriptions are code-derived strings. Editing
        # the wording here is reverted on the next release; the fix belongs
        # upstream in the event definition.
        marker = content.find(GENERATED_SECTION_MARKER)
        if marker != -1:
            content = content[:marker]
        prose = strip_code_spans(content)
        stale_found = []
        for term, reason, pattern in term_patterns:
            if pattern.search(prose):
                stale_found.append({"term": term, "reason": reason})

        if stale_found:
            findings.append({
                "doc_path": doc_path,
                "stale_terms": stale_found,
                "severity": "low",
                "reason": "Doc contains potentially outdated terminology",
            })

    return findings

# ---------------------------------------------------------------------------
# Audit 8: Docs structure (pages missing from the sidebar)
# ---------------------------------------------------------------------------

def audit_unlisted_pages(repo_root: Path, docs_root: Path, surface_map: dict) -> list[dict]:
    """Find docs pages that exist on disk but are not referenced in the sidebar.

    Unlisted pages are built but unreachable through navigation — usually a
    forgotten `src/sidebar.ts` entry after adding a page. Intentionally
    unlisted pages belong in the surface map's "Unlisted docs pages" section.
    """
    slugs = parse_sidebar_slugs(repo_root)
    if slugs is None:
        return [{
            "page": "(all)",
            "severity": "high",
            "reason": (
                "src/sidebar.ts not found — sidebar definition moved; update "
                "parse_sidebar_slugs() in the audit script"
            ),
        }]
    allowlist = surface_map.get("unlisted_ignore", set())

    findings = []
    for md_file in find_markdown_files(docs_root):
        slug = page_slug(md_file, docs_root)
        if slug in slugs or slug in allowlist:
            continue
        findings.append({
            "page": slug or "(root index)",
            "file": str(md_file.relative_to(repo_root)),
            "severity": "low",
            "reason": (
                "Docs page is not referenced in src/sidebar.ts — add it to the "
                "sidebar (and astro.config.mjs topic if new) or allow-list it "
                "in the surface map's 'Unlisted docs pages' section"
            ),
        })
    return findings

# ---------------------------------------------------------------------------
# Audit 9: Surface map hygiene
# ---------------------------------------------------------------------------

def audit_map_hygiene(surface_map: dict, flag_statuses: dict[str, str],
                      cli_commands: list[dict], api_routes: list[dict],
                      slash_commands: list[str], settings: dict[str, dict],
                      docs_root: Path) -> list[dict]:
    """Flag surface-map entries that reference code surfaces that no longer exist.

    Dead entries usually mean a feature was renamed or removed — verify the
    target doc page is still accurate, then prune or update the entry.
    """
    findings = []
    repo_root = DOCS_REPO_ROOT[0] or docs_root.parent.parent.parent
    known_flags = set(flag_statuses)

    # Map integrity: a flag must not be both mapped and ignored (the audit
    # checks the ignore list first, so the mapping would silently lose).
    for flag in sorted(set(surface_map.get("feature_to_doc", {}))
                       & surface_map.get("ignore_flags", set())):
        findings.append({
            "entry": flag,
            "section": "Feature flags + Flags to ignore",
            "severity": "medium",
            "reason": (
                f"'{flag}' appears in BOTH the feature mapping and the ignore "
                "list — the ignore entry wins silently; remove one"
            ),
        })
    # Map integrity: duplicate keys within a section (last occurrence wins).
    for section_name, key in surface_map.get("duplicates", []):
        findings.append({
            "entry": key,
            "section": section_name,
            "severity": "medium",
            "reason": (
                f"Duplicate entry '{key}' in the {section_name} section — the "
                "last occurrence silently wins; remove the extra line"
            ),
        })

    for flag in sorted(surface_map.get("feature_to_doc", {})):
        if flag not in known_flags:
            findings.append({
                "entry": flag,
                "section": "Feature flags",
                "severity": "low",
                "reason": (
                    f"Map entry '{flag}' does not match any FeatureFlag in code "
                    "(flag removed or renamed) — verify the doc page is still "
                    "accurate, then prune or update the entry"
                ),
            })
    for flag in sorted(surface_map.get("ignore_flags", set())):
        if flag not in known_flags:
            findings.append({
                "entry": flag,
                "section": "Flags to ignore",
                "severity": "low",
                "reason": (
                    f"Ignore-list entry '{flag}' does not match any FeatureFlag "
                    "in code — prune it"
                ),
            })

    known_cli = set()
    for cmd in cli_commands:
        known_cli.add(cmd["command"])
        for sub in cmd["subcommands"]:
            known_cli.add(sub["command"])
    for cmd in sorted(surface_map.get("cli_to_doc", {})):
        if cmd not in known_cli:
            findings.append({
                "entry": cmd,
                "section": "CLI commands",
                "severity": "low",
                "reason": (
                    f"Map entry '{cmd}' does not match any CLI command in code — "
                    "verify and prune or update"
                ),
            })

    known_api = set()
    for route in api_routes:
        known_api.add(route["route"])
        rel_path = route["path"]
        if rel_path.startswith("/api/v1"):
            rel_path = rel_path[len("/api/v1"):] or "/"
        known_api.add(f"{route['method']} {rel_path}")
    for key in sorted(surface_map.get("api_to_doc", {})):
        if key not in known_api:
            findings.append({
                "entry": key,
                "section": "API endpoints",
                "severity": "low",
                "reason": (
                    f"Map entry '{key}' does not match any public API route in "
                    "code — verify and prune or update"
                ),
            })

    known_slash = set(slash_commands)
    for name in sorted(surface_map.get("slash_to_doc", {})):
        if name not in known_slash:
            findings.append({
                "entry": name,
                "section": "Slash commands",
                "severity": "low",
                "reason": (
                    f"Map entry '{name}' does not match any static slash command "
                    "in code — verify and prune or update"
                ),
            })

    for key in sorted(surface_map.get("settings_to_doc", {})):
        if key not in settings:
            findings.append({
                "entry": key,
                "section": "Settings",
                "severity": "low",
                "reason": (
                    f"Map entry '{key}' does not match any setting in code — "
                    "verify and prune or update"
                ),
            })

    # Gated surface-map targets must reference a real FeatureFlag.
    for section_name, mapping in (
        ("CLI commands", surface_map.get("cli_to_doc", {})),
        ("API endpoints", surface_map.get("api_to_doc", {})),
    ):
        for key, val in sorted(mapping.items()):
            gflag = _gated_flag(val)
            if gflag is not None and gflag not in known_flags:
                findings.append({
                    "entry": key,
                    "section": section_name,
                    "severity": "medium",
                    "reason": (
                        f"Gated target 'gated:{gflag}' references a FeatureFlag that "
                        "does not exist in code \u2014 fix the flag name or remove the gate"
                    ),
                })

    # Mapped doc targets that no longer exist (any section).
    for section, mapping in (
        ("Feature flags", surface_map.get("feature_to_doc", {})),
        ("CLI commands", surface_map.get("cli_to_doc", {})),
        ("API endpoints", surface_map.get("api_to_doc", {})),
        ("Slash commands", surface_map.get("slash_to_doc", {})),
        ("Settings", surface_map.get("settings_to_doc", {})),
    ):
        for key, doc_path in sorted(mapping.items()):
            if doc_path == "internal" or _gated_flag(doc_path) is not None:
                continue
            if resolve_doc_path(doc_path, repo_root) is None:
                findings.append({
                    "entry": key,
                    "section": section,
                    "severity": "medium",
                    "reason": (
                        f"Mapped doc {doc_path} does not exist — the page was "
                        "moved or deleted; update the map (and redirects)"
                    ),
                })

    return findings

# ---------------------------------------------------------------------------
# Snapshot + change detection
# ---------------------------------------------------------------------------

def build_snapshot(flag_statuses: dict[str, str], cli_commands: list[dict],
                   cli_flags: dict[str, list[str]], api_routes: list[dict],
                   slash_commands: list[str], settings: dict[str, dict],
                   web_routes: list[str], server_tools: list[str],
                   bundled_skills: dict[str, str],
                   changelog_entries: list[dict]) -> dict:
    """Assemble the surface snapshot (deterministic ordering for clean diffs)."""
    cli_flat = []
    for cmd in cli_commands:
        cli_flat.append({"command": cmd["command"], "hidden": cmd["hidden"]})
        for sub in cmd["subcommands"]:
            cli_flat.append({"command": sub["command"], "hidden": sub["hidden"]})
    cli_flat.sort(key=lambda c: c["command"])

    settings_status = {
        path: setting_status(info, flag_statuses)
        for path, info in settings.items()
    }

    return {
        "schema_version": SNAPSHOT_SCHEMA_VERSION,
        "flags": dict(sorted(flag_statuses.items())),
        "cli_commands": cli_flat,
        "cli_flags": {k: sorted(v) for k, v in sorted(cli_flags.items())},
        "api_routes": sorted(r["route"] for r in api_routes),
        "slash_commands": sorted(slash_commands),
        "settings": dict(sorted(settings_status.items())),
        "web_routes": sorted(web_routes),
        "server_tools": sorted(server_tools),
        "bundled_skills": dict(sorted(bundled_skills.items())),
        "changelog_last_version": (
            changelog_entries[0]["version"] if changelog_entries else None
        ),
    }


def load_snapshot(path: Path) -> dict | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"Warning: failed to parse snapshot {path}: {exc}", file=sys.stderr)
        return None


def _diff_sets(findings: list, old: dict, new: dict, field: str, label: str,
               added_reason: str, removed_reason: str, severity: str = "medium"):
    """Generic added/removed diff for a snapshot list field."""
    if field not in old:
        findings.append({
            "change": "surface_type_added",
            "surface": field,
            "severity": "low",
            "reason": (
                f"The snapshot now tracks {label} — baseline established this "
                "run; future runs will diff it (regenerate with --update-snapshot)"
            ),
        })
        return
    old_set = set(old.get(field) or [])
    new_set = set(new.get(field) or [])
    for item in sorted(new_set - old_set):
        findings.append({
            "change": f"{field}_added",
            "surface": item,
            "severity": severity,
            "reason": added_reason.format(item=item),
        })
    for item in sorted(old_set - new_set):
        findings.append({
            "change": f"{field}_removed",
            "surface": item,
            "severity": severity,
            "reason": removed_reason.format(item=item),
        })


def diff_snapshots(old: dict, new: dict) -> list[dict]:
    """Compare two snapshots and report added/removed/promoted surfaces."""
    findings = []

    old_flags = old.get("flags", {})
    new_flags = new.get("flags", {})
    for flag in sorted(set(new_flags) - set(old_flags)):
        status = new_flags[flag]
        severity = {"ga": "high", "preview": "medium"}.get(status, "low")
        findings.append({
            "change": "flag_added",
            "surface": flag,
            "detail": f"status: {status}",
            "severity": severity,
            "reason": (
                f"New feature flag '{flag}' ({status}) — "
                + ("needs docs and a surface map entry"
                   if status in ("ga", "preview")
                   else "track it; no docs needed until promotion")
            ),
        })
    for flag in sorted(set(old_flags) - set(new_flags)):
        findings.append({
            "change": "flag_removed",
            "surface": flag,
            "detail": f"was: {old_flags[flag]}",
            "severity": "medium",
            "reason": (
                f"Feature flag '{flag}' was removed — the feature either "
                "stabilized (flag cleanup) or was killed. Verify docs cover the "
                "final behavior and prune/keep the surface map entry accordingly"
            ),
        })
    for flag in sorted(set(old_flags) & set(new_flags)):
        if old_flags[flag] == new_flags[flag]:
            continue
        promoted_to_user_facing = new_flags[flag] in ("ga", "preview")
        findings.append({
            "change": "flag_status_changed",
            "surface": flag,
            "detail": f"{old_flags[flag]} -> {new_flags[flag]}",
            "severity": "high" if new_flags[flag] == "ga" else (
                "medium" if promoted_to_user_facing else "low"),
            "reason": (
                f"Feature flag '{flag}' moved {old_flags[flag]} -> {new_flags[flag]}"
                + (" — verify docs exist and the surface map is updated"
                   if promoted_to_user_facing else "")
            ),
        })

    old_cli = {c["command"] for c in old.get("cli_commands", []) if not c.get("hidden")}
    new_cli = {c["command"] for c in new.get("cli_commands", []) if not c.get("hidden")}
    for cmd in sorted(new_cli - old_cli):
        findings.append({
            "change": "cli_added",
            "surface": cmd,
            "severity": "medium",
            "reason": f"New CLI command '{cmd}' — document it in the CLI reference",
        })
    for cmd in sorted(old_cli - new_cli):
        findings.append({
            "change": "cli_removed",
            "surface": cmd,
            "severity": "medium",
            "reason": (
                f"CLI command '{cmd}' was removed or hidden — update the CLI "
                "reference docs and surface map"
            ),
        })

    # Per-module CLI flag changes.
    if "cli_flags" not in old:
        findings.append({
            "change": "surface_type_added",
            "surface": "cli_flags",
            "severity": "low",
            "reason": (
                "The snapshot now tracks CLI --flags per module — baseline "
                "established this run; future runs will diff it"
            ),
        })
    else:
        old_flags_by_module = old.get("cli_flags") or {}
        new_flags_by_module = new.get("cli_flags") or {}
        for module in sorted(set(old_flags_by_module) | set(new_flags_by_module)):
            old_set = set(old_flags_by_module.get(module, []))
            new_set = set(new_flags_by_module.get(module, []))
            for flag in sorted(new_set - old_set):
                findings.append({
                    "change": "cli_flag_added",
                    "surface": f"{module}: {flag}",
                    "severity": "low",
                    "reason": (
                        f"New CLI flag '{flag}' in warp_cli/src/{module}.rs — "
                        "verify the CLI reference documents it"
                    ),
                })
            for flag in sorted(old_set - new_set):
                findings.append({
                    "change": "cli_flag_removed",
                    "surface": f"{module}: {flag}",
                    "severity": "low",
                    "reason": (
                        f"CLI flag '{flag}' removed from warp_cli/src/{module}.rs — "
                        "verify the CLI reference no longer documents it"
                    ),
                })

    _diff_sets(
        findings, old, new, "api_routes", "public API routes",
        "New public API route '{item}' — add it to the OpenAPI spec "
        "(sync-openapi-spec skill) or map it as internal",
        "Public API route '{item}' was removed — verify the OpenAPI spec and "
        "API docs no longer document it",
    )
    _diff_sets(
        findings, old, new, "slash_commands", "slash commands",
        "New slash command '{item}' — add it to the slash-commands docs page "
        "or map it as internal",
        "Slash command '{item}' was removed — update the slash-commands docs "
        "page and surface map",
    )
    _diff_sets(
        findings, old, new, "web_routes", "Oz web app routes",
        "New Oz web app route '{item}' — verify the Oz web app docs cover the "
        "new page",
        "Oz web app route '{item}' was removed — verify the Oz web app docs "
        "no longer reference it",
    )
    _diff_sets(
        findings, old, new, "server_tools", "server-side agent tools",
        "New agent tool '{item}' — verify docs cover the new agent capability",
        "Agent tool '{item}' was removed — verify docs no longer describe it",
        severity="low",
    )

    # Settings (dict field: path -> status).
    if "settings" not in old:
        findings.append({
            "change": "surface_type_added",
            "surface": "settings",
            "severity": "low",
            "reason": (
                "The snapshot now tracks settings — baseline established this "
                "run; future runs will diff it"
            ),
        })
    else:
        old_settings = old.get("settings") or {}
        new_settings = new.get("settings") or {}
        for path in sorted(set(new_settings) - set(old_settings)):
            status = new_settings[path]
            user_facing = status in ("always_on", "ga", "preview")
            findings.append({
                "change": "setting_added",
                "surface": path,
                "detail": f"status: {status}",
                "severity": "medium" if user_facing else "low",
                "reason": (
                    f"New setting '{path}' ({status}) — "
                    + ("document it in the all-settings reference"
                       if user_facing else "track it; document on promotion")
                ),
            })
        for path in sorted(set(old_settings) - set(new_settings)):
            findings.append({
                "change": "setting_removed",
                "surface": path,
                "detail": f"was: {old_settings[path]}",
                "severity": "medium",
                "reason": (
                    f"Setting '{path}' was removed or renamed — update the "
                    "all-settings reference"
                ),
            })
        for path in sorted(set(old_settings) & set(new_settings)):
            if old_settings[path] == new_settings[path]:
                continue
            now_user_facing = new_settings[path] in ("always_on", "ga", "preview")
            findings.append({
                "change": "setting_status_changed",
                "surface": path,
                "detail": f"{old_settings[path]} -> {new_settings[path]}",
                "severity": "medium" if now_user_facing else "low",
                "reason": (
                    f"Setting '{path}' moved {old_settings[path]} -> "
                    f"{new_settings[path]}"
                    + (" — verify the all-settings reference documents it"
                       if now_user_facing else "")
                ),
            })

    # Bundled skills (dict field: name -> channel).
    if "bundled_skills" not in old:
        findings.append({
            "change": "surface_type_added",
            "surface": "bundled_skills",
            "severity": "low",
            "reason": (
                "The snapshot now tracks bundled skills — baseline established "
                "this run; future runs will diff it"
            ),
        })
    else:
        old_skills = old.get("bundled_skills") or {}
        new_skills = new.get("bundled_skills") or {}
        for name in sorted(set(new_skills) - set(old_skills)):
            findings.append({
                "change": "bundled_skill_added",
                "surface": name,
                "detail": f"channel: {new_skills[name]}",
                "severity": "medium" if new_skills[name] == "bundled" else "low",
                "reason": (
                    f"New bundled skill '{name}' ({new_skills[name]}) — verify "
                    "the skills docs cover it"
                ),
            })
        for name in sorted(set(old_skills) - set(new_skills)):
            findings.append({
                "change": "bundled_skill_removed",
                "surface": name,
                "severity": "low",
                "reason": (
                    f"Bundled skill '{name}' was removed — verify docs no "
                    "longer reference it"
                ),
            })
        for name in sorted(set(old_skills) & set(new_skills)):
            if old_skills[name] != new_skills[name]:
                findings.append({
                    "change": "bundled_skill_channel_changed",
                    "surface": name,
                    "detail": f"{old_skills[name]} -> {new_skills[name]}",
                    "severity": "medium" if new_skills[name] == "bundled" else "low",
                    "reason": (
                        f"Bundled skill '{name}' moved channel "
                        f"{old_skills[name]} -> {new_skills[name]} — verify docs"
                    ),
                })

    return findings


def changelog_review_findings(changelog_entries: list[dict],
                              last_seen_version: str | None) -> list[dict]:
    """Emit verification findings for changelog entries newer than the snapshot.

    The weekly human-curated changelog is the best signal for launches that no
    static code parse can see (server-side features, Oz web app, experiment
    rollouts). Each bullet should be verified for real docs coverage — a
    changelog mention alone is not documentation.
    """
    findings = []
    for entry in changelog_entries:
        if last_seen_version and entry["version"] <= last_seen_version:
            continue
        for item in entry["items"]:
            findings.append({
                "version": entry["version"],
                "category": item["category"],
                "text": item["text"],
                "severity": "low",
                "reason": (
                    "New changelog item since last audit — verify the feature "
                    "has real docs coverage (not just the changelog mention)"
                ),
            })
    return findings

# ---------------------------------------------------------------------------
# Completeness accounting
# ---------------------------------------------------------------------------

def compute_accounting(docs_root: Path, surface_map: dict, findings: dict,
                       flag_statuses: dict[str, str], cli_commands: list[dict],
                       api_routes: list[dict], slash_commands: list[str],
                       settings: dict[str, dict],
                       docs_text: dict[str, str]) -> dict:
    """Partition every extracted surface item into exactly one accountability
    bucket and prove totality.

    Every item must be mapped, ignored, covered by docs, a visible finding, or
    snapshot-tracked (non-GA). `unaccounted` lists anything that escapes all
    buckets — it must be empty; a non-empty list means the audit logic
    regressed and the run is treated as incomplete (exit 2).
    """
    repo_root = DOCS_REPO_ROOT[0] or docs_root.parent.parent.parent
    acc: dict = {}
    unaccounted: dict[str, list[str]] = {}

    # Feature flags ---------------------------------------------------------
    mapped = set(surface_map.get("feature_to_doc", {}))
    ignored = surface_map.get("ignore_flags", set())
    flag_findings = {f.get("flag") for f in findings.get("undocumented_features", [])}
    fb = {"total": len(flag_statuses), "ga_preview": 0, "ignored": 0,
          "mapped": 0, "finding": 0, "tracked_non_ga": 0}
    missing = []
    for flag, status in flag_statuses.items():
        if status not in ("ga", "preview"):
            fb["tracked_non_ga"] += 1
            continue
        fb["ga_preview"] += 1
        if flag in ignored:
            fb["ignored"] += 1
        elif flag in mapped:
            fb["mapped"] += 1
        elif flag in flag_findings:
            fb["finding"] += 1
        else:
            missing.append(flag)
    if missing:
        unaccounted["feature_flags"] = missing
    acc["feature_flags"] = fb

    # CLI commands -----------------------------------------------------------
    cli_map = surface_map.get("cli_to_doc", {})
    cli_findings = {f.get("command") for f in findings.get("undocumented_cli_commands", [])}
    cli_text = {}
    cli_docs_dir = docs_root / "reference" / "cli"
    if cli_docs_dir.exists():
        for f in find_markdown_files(cli_docs_dir):
            try:
                cli_text[str(f)] = f.read_text(encoding="utf-8").lower()
            except Exception:
                pass
    cb = {"total": 0, "hidden": 0, "mapped": 0, "doc_covered": 0,
          "finding": 0, "parent_flagged": 0, "gated_non_ga": 0}
    missing = []
    for cmd in cli_commands:
        entries = [(cmd["command"], cmd["hidden"], None)] + [
            (s["command"], s["hidden"], cmd["command"]) for s in cmd["subcommands"]]
        for name, hidden, parent in entries:
            cb["total"] += 1
            val = cli_map.get(name)
            gflag = _gated_flag(val)
            deferred = gflag is not None and flag_statuses.get(gflag) in _NON_GA_STATUSES
            if hidden:
                cb["hidden"] += 1
            elif deferred:
                cb["gated_non_ga"] += 1
            elif val is not None and gflag is None:
                cb["mapped"] += 1
            elif any(name.split(" ", 1)[1] in t for t in cli_text.values()):
                cb["doc_covered"] += 1
            elif name in cli_findings:
                cb["finding"] += 1
            elif parent in cli_findings:
                cb["parent_flagged"] += 1
            else:
                missing.append(name)
    if missing:
        unaccounted["cli_commands"] = missing
    acc["cli_commands"] = cb

    # API routes -------------------------------------------------------------
    api_map = surface_map.get("api_to_doc", {})
    api_findings = {f.get("route") for f in findings.get("undocumented_api_endpoints", [])}
    openapi_candidates = [
        repo_root / "developers" / "agent-api-openapi.yaml",
        docs_root / "developers" / "agent-api-openapi.yaml",
    ]
    openapi_path = next((c for c in openapi_candidates if c.exists()), openapi_candidates[0])
    openapi_text = ""
    if openapi_path.exists():
        try:
            openapi_text = openapi_path.read_text(encoding="utf-8").lower()
        except Exception:
            pass
    spec_paths = parse_openapi_paths(openapi_text)
    api_docs_text = {}
    api_docs_dir = docs_root / "reference" / "api-and-sdk"
    if api_docs_dir.exists():
        for f in find_markdown_files(api_docs_dir):
            try:
                api_docs_text[str(f)] = f.read_text(encoding="utf-8").lower()
            except Exception:
                pass
    ab = {"total": len(api_routes), "mapped": 0, "spec_covered": 0,
          "docs_covered": 0, "finding": 0, "gated_non_ga": 0}
    missing = []
    for route in api_routes:
        rel = route["path"]
        if rel.startswith("/api/v1"):
            rel = rel[len("/api/v1"):] or "/"
        rel_str = f"{route['method']} {rel}"
        map_val = api_map.get(route["route"])
        if map_val is None:
            map_val = api_map.get(rel_str)
        gflag = _gated_flag(map_val)
        deferred = gflag is not None and flag_statuses.get(gflag) in _NON_GA_STATUSES
        if deferred:
            ab["gated_non_ga"] += 1
        elif map_val is not None and gflag is None:
            ab["mapped"] += 1
        elif (_normalize_path_params(rel) in spec_paths
              or _normalize_path_params(route["path"]) in spec_paths):
            ab["spec_covered"] += 1
        elif any(c in openapi_text or any(c in t for t in api_docs_text.values())
                 for c in {route["path"].lower(), rel.lower()}):
            ab["docs_covered"] += 1
        elif rel_str in api_findings:
            ab["finding"] += 1
        else:
            missing.append(rel_str)
    if missing:
        unaccounted["api_routes"] = missing
    acc["api_routes"] = ab

    # Slash commands ----------------------------------------------------------
    slash_map = surface_map.get("slash_to_doc", {})
    slash_findings = {f.get("command") for f in findings.get("undocumented_slash_commands", [])}
    sb = {"total": len(slash_commands), "mapped": 0, "doc_covered": 0, "finding": 0}
    missing = []
    for name in slash_commands:
        if name in slash_map:
            sb["mapped"] += 1
        elif any(_slash_mention_re(name).search(t) for t in docs_text.values()):
            sb["doc_covered"] += 1
        elif name in slash_findings:
            sb["finding"] += 1
        else:
            missing.append(name)
    if missing:
        unaccounted["slash_commands"] = missing
    acc["slash_commands"] = sb

    # Settings ----------------------------------------------------------------
    settings_map = surface_map.get("settings_to_doc", {})
    setting_findings = {f.get("setting") for f in findings.get("undocumented_settings", [])}
    doc_sections, _ = parse_settings_doc(docs_root)
    tb = {"total": len(settings), "private": 0, "tracked_non_ga": 0,
          "mapped": 0, "doc_covered": 0, "finding": 0}
    missing = []
    for path, info in settings.items():
        status = setting_status(info, flag_statuses)
        if status == "private":
            tb["private"] += 1
            continue
        if status in ("dogfood", "other"):
            tb["tracked_non_ga"] += 1
            continue
        hierarchy, _, key = path.rpartition(".")
        if path in settings_map:
            tb["mapped"] += 1
        elif (key in doc_sections.get(hierarchy, set()) or path in doc_sections
              or any(s.startswith(path + ".") for s in doc_sections)):
            tb["doc_covered"] += 1
        elif path in setting_findings:
            tb["finding"] += 1
        else:
            missing.append(path)
    if missing:
        unaccounted["settings"] = missing
    acc["settings"] = tb

    acc["unaccounted"] = unaccounted
    return acc

# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------

REPORT_CATEGORIES = [
    ("undocumented_features", "UNDOCUMENTED FEATURES",
     lambda i: i.get("flag", "")),
    ("undocumented_cli_commands", "UNDOCUMENTED CLI COMMANDS",
     lambda i: i.get("command", "")),
    ("undocumented_api_endpoints", "UNDOCUMENTED API ENDPOINTS",
     lambda i: i.get("route", "")),
    ("undocumented_slash_commands", "UNDOCUMENTED SLASH COMMANDS",
     lambda i: i.get("command", "")),
    ("undocumented_settings", "UNDOCUMENTED SETTINGS",
     lambda i: i.get("setting", "")),
    ("surface_changes", "SURFACE CHANGES SINCE SNAPSHOT",
     lambda i: f"{i.get('change', '')}: {i.get('surface', '')}"),
    ("changelog_review", "CHANGELOG ITEMS TO VERIFY",
     lambda i: f"{i.get('version', '')} [{i.get('category', '')}] {i.get('text', '')[:100]}"),
    ("map_hygiene", "SURFACE MAP HYGIENE",
     lambda i: f"{i.get('section', '')}: {i.get('entry', '')}"),
    ("stale_doc_references", "STALE DOC REFERENCES",
     lambda i: f"{i.get('kind', '')}: {i.get('reference', '')}"),
    ("unlisted_pages", "PAGES MISSING FROM SIDEBAR",
     lambda i: i.get("page", "")),
    ("potentially_stale_docs", "POTENTIALLY STALE DOCS",
     lambda i: i.get("doc_path", "")),
]


def generate_report(findings_by_category: dict[str, list], audits_run: list[str],
                    audits_skipped: list[dict], mode: str,
                    accounting: dict | None = None) -> dict:
    """Assemble the full audit report."""
    total = sum(len(v) for v in findings_by_category.values())
    report = {
        "summary": {
            "mode": mode,
            "total_gaps": total,
            "audits_run": audits_run,
            "audits_skipped": audits_skipped,
            "by_category": {
                key: len(findings_by_category.get(key, []))
                for key, _, _ in REPORT_CATEGORIES
            },
        },
    }
    if accounting is not None:
        report["summary"]["accounting"] = accounting
    for key, _, _ in REPORT_CATEGORIES:
        report[key] = findings_by_category.get(key, [])
    return report


def print_report(report: dict) -> None:
    """Print a human-readable report to stdout."""
    summary = report["summary"]
    print("=" * 60)
    print("MISSING DOCS AUDIT REPORT")
    print("=" * 60)
    print(f"Mode: {summary['mode']}")
    print(f"Audits run: {', '.join(summary['audits_run']) or 'none'}")
    if summary["audits_skipped"]:
        print("!! AUDITS SKIPPED (results are incomplete):")
        for skipped in summary["audits_skipped"]:
            print(f"  - {skipped['audit']}: {skipped['reason']}")
    print(f"Total gaps found: {summary['total_gaps']}")
    for category, count in summary["by_category"].items():
        if count:
            print(f"  {category}: {count}")
    print()

    accounting = summary.get("accounting")
    if accounting:
        print("-" * 60)
        print("COMPLETENESS ACCOUNTING (every item in exactly one bucket)")
        print("-" * 60)
        for surface, buckets in accounting.items():
            if surface == "unaccounted":
                continue
            parts = ", ".join(f"{k}={v}" for k, v in buckets.items())
            print(f"  {surface}: {parts}")
        if accounting.get("unaccounted"):
            print("  !! UNACCOUNTED ITEMS (audit logic regression):")
            for surface, items in accounting["unaccounted"].items():
                print(f"    {surface}: {items}")
        else:
            print("  unaccounted: none — every extracted surface item is accounted for")
        print()

    severity_order = {"high": 0, "medium": 1, "low": 2}

    for key, title, describe in REPORT_CATEGORIES:
        items = report.get(key, [])
        if not items:
            continue
        print("-" * 60)
        print(f"{title} ({len(items)})")
        print("-" * 60)
        for item in sorted(items, key=lambda x: severity_order.get(x.get("severity", "low"), 3)):
            sev = item.get("severity", "?").upper()
            print(f"\n  [{sev}] {describe(item)}")
            if item.get("reason"):
                print(f"    Reason: {item['reason']}")
            if item.get("suggested_doc_path"):
                print(f"    Suggested: {item['suggested_doc_path']}")
            if item.get("matched_docs"):
                print(f"    Mentioned in: {', '.join(item['matched_docs'])}")
            if item.get("search_terms"):
                print(f"    Search terms: {', '.join(item['search_terms'][:3])}")
            if item.get("source_file"):
                print(f"    Source: {item['source_file']}")
            if item.get("handler_file"):
                print(f"    Handler: {item['handler_file']}")
            if item.get("doc_page"):
                print(f"    Doc page: {item['doc_page']}")
            if item.get("file"):
                print(f"    File: {item['file']}")
            if item.get("detail"):
                print(f"    Detail: {item['detail']}")
            for t in item.get("stale_terms", []):
                print(f"    - \"{t['term']}\": {t['reason']}")
        print()

    print("=" * 60)

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Audit Warp documentation coverage against code surfaces"
    )
    parser.add_argument(
        "--warp",
        dest="warp_repo",
        help="Path to the public warp client repo (auto-detected as a sibling "
             "of the docs repo named 'warp', with 'warp-internal' as fallback)",
    )
    parser.add_argument(
        "--warp-internal",
        dest="warp_repo",
        help="Deprecated alias for --warp",
    )
    parser.add_argument(
        "--warp-server",
        help="Path to warp-server repo (auto-detected as a sibling of the docs repo)",
    )
    parser.add_argument(
        "--output", "-o",
        help="Save JSON report to file",
    )
    parser.add_argument(
        "--category",
        choices=["features", "cli", "api", "slash", "settings", "structure",
                 "staleness", "map"],
        help="Run only a specific audit category",
    )
    parser.add_argument(
        "--severity",
        choices=["high", "medium", "low"],
        help="Filter results by minimum severity",
    )
    parser.add_argument(
        "--weak-coverage",
        action="store_true",
        help="Also flag features whose mapped doc exists but doesn't mention "
             "feature keywords (noisy; produces low-severity findings)",
    )
    parser.add_argument(
        "--diff",
        action="store_true",
        help="Compare current surfaces against the committed snapshot and report "
             "added/removed/promoted surfaces plus new changelog items",
    )
    parser.add_argument(
        "--update-snapshot",
        action="store_true",
        help="Regenerate the surface snapshot from current code (commit it with "
             "the docs PR). Requires a full run (no --category)",
    )
    parser.add_argument(
        "--snapshot",
        default=str(DEFAULT_SNAPSHOT_PATH),
        help=f"Path to the surface snapshot (default: {DEFAULT_SNAPSHOT_PATH})",
    )
    args = parser.parse_args()

    if args.update_snapshot and args.category:
        print("Error: --update-snapshot requires a full run (drop --category)",
              file=sys.stderr)
        sys.exit(1)

    # Find repos.
    # SKILL_DIR is at <repo>/.agents/skills/missing_docs (or legacy <repo>/.warp/skills/...)
    repo_root = SKILL_DIR.parent.parent.parent
    # Astro Starlight docs live at src/content/docs
    candidates = [
        repo_root / "src" / "content" / "docs",
        repo_root / "docs",
    ]
    docs_root = next((c for c in candidates if c.exists()), None)
    if docs_root is None:
        print(f"Error: docs directory not found. Tried: {[str(c) for c in candidates]}",
              file=sys.stderr)
        sys.exit(1)
    # repo_root carries the developers/ openapi spec etc.
    DOCS_REPO_ROOT[0] = repo_root

    warp_repo = find_repo(["warp", "warp-internal"], args.warp_repo, repo_root)
    warp_server = find_repo(["warp-server"], args.warp_server, repo_root)

    # Parse surface map
    surface_map = parse_surface_map(SURFACE_MAP_PATH)

    # Read all docs
    print("Scanning documentation...", file=sys.stderr)
    docs_text = read_all_docs_text(docs_root)
    print(f"  Found {len(docs_text)} markdown files", file=sys.stderr)

    findings: dict[str, list] = {}
    audits_run: list[str] = []
    audits_skipped: list[dict] = []
    extraction_ok = True

    def guard(label: str, count: int) -> bool:
        nonlocal extraction_ok
        floor = EXTRACTION_FLOORS.get(label, 1)
        if count < floor:
            extraction_ok = False
            audits_skipped.append({
                "audit": f"extraction:{label}",
                "reason": (
                    f"only {count} {label} extracted (expected >= {floor}) — "
                    "the source layout likely changed; fix the parser in "
                    "audit_docs.py before trusting any results"
                ),
            })
            return False
        return True

    internal_categories = ("features", "cli", "slash", "settings", "staleness", "map")
    needs_internal = args.category in (None, *internal_categories) \
        or args.diff or args.update_snapshot
    needs_server = args.category in (None, "api", "map") \
        or args.diff or args.update_snapshot

    flag_statuses: dict[str, str] = {}
    cli_commands: list[dict] = []
    cli_flags: dict[str, list[str]] = {}
    slash_commands: list[str] = []
    settings: dict[str, dict] = {}
    api_routes: list[dict] = []
    web_routes: list[str] = []
    server_tools: list[str] = []
    bundled_skills: dict[str, str] = {}

    if warp_repo and needs_internal:
        print(f"Using warp client repo: {warp_repo}", file=sys.stderr)
        flag_statuses = compute_flag_statuses(warp_repo)
        cli_commands = parse_cli_commands(warp_repo)
        cli_flags = parse_cli_flags(warp_repo, cli_commands)
        slash_commands = parse_slash_commands(warp_repo)
        print("Parsing settings registry...", file=sys.stderr)
        settings = parse_settings(warp_repo)
        bundled_skills = parse_bundled_skills(warp_repo)

        flags_ok = guard("feature flags", len(flag_statuses))
        cli_ok = guard("CLI commands", len(cli_commands))
        slash_ok = guard("slash commands", len(slash_commands))
        settings_ok = guard("settings", len(settings))

        if args.category in (None, "features") and flags_ok:
            print("Running feature flag coverage audit...", file=sys.stderr)
            findings["undocumented_features"] = audit_features(
                warp_repo, docs_root, surface_map, docs_text,
                flag_statuses=flag_statuses, weak_coverage=args.weak_coverage,
            )
            audits_run.append("features")

        if args.category in (None, "cli") and cli_ok:
            print("Running CLI command coverage audit...", file=sys.stderr)
            findings["undocumented_cli_commands"] = audit_cli(
                warp_repo, docs_root, surface_map, docs_text,
                cli_commands=cli_commands, flag_statuses=flag_statuses)
            audits_run.append("cli")

        if args.category in (None, "slash") and slash_ok:
            print("Running slash command coverage audit...", file=sys.stderr)
            findings["undocumented_slash_commands"] = audit_slash_commands(
                warp_repo, docs_root, surface_map, docs_text,
                slash_commands=slash_commands)
            audits_run.append("slash")

        if args.category in (None, "settings") and settings_ok and flags_ok:
            print("Running settings coverage audit...", file=sys.stderr)
            findings["undocumented_settings"] = audit_settings(
                docs_root, surface_map, settings, flag_statuses)
            audits_run.append("settings")

        if args.category in (None, "staleness"):
            print("Running docs staleness audit...", file=sys.stderr)
            findings["potentially_stale_docs"] = audit_staleness(
                warp_repo, docs_root, docs_text)
            # The reverse checks compare docs against extracted code surfaces,
            # so they are only meaningful when extraction is healthy.
            if flags_ok and settings_ok:
                print("Running stale doc reference audit...", file=sys.stderr)
                findings["stale_doc_references"] = audit_stale_doc_references(
                    warp_repo, docs_root, settings)
            audits_run.append("staleness")
    elif needs_internal:
        for audit in ("features", "cli", "slash", "settings", "staleness"):
            if args.category in (None, audit):
                audits_skipped.append({
                    "audit": audit,
                    "reason": "warp client repo not found (pass --warp)",
                })

    if warp_server and needs_server:
        print(f"Using warp-server: {warp_server}", file=sys.stderr)
        api_routes = parse_public_api_routes(warp_server)
        web_routes = parse_webapp_routes(warp_server)
        server_tools = parse_server_tools(warp_server)
        api_ok = guard("API routes", len(api_routes))
        if args.category in (None, "api") and api_ok:
            # gated:<Flag> deferral needs flag rollout statuses; compute them if a
            # full run hasn't already (e.g. an isolated `--category api` run).
            if not flag_statuses and warp_repo:
                flag_statuses = compute_flag_statuses(warp_repo)
            print("Running API endpoint coverage audit...", file=sys.stderr)
            findings["undocumented_api_endpoints"] = audit_api(
                warp_server, docs_root, surface_map, docs_text,
                api_routes=api_routes, flag_statuses=flag_statuses)
            audits_run.append("api")
    elif needs_server:
        if args.category in (None, "api"):
            audits_skipped.append({
                "audit": "api",
                "reason": "warp-server repo not found (pass --warp-server)",
            })

    # Docs structure audit needs only the docs repo.
    if args.category in (None, "structure"):
        print("Running docs structure audit (sidebar coverage)...", file=sys.stderr)
        findings["unlisted_pages"] = audit_unlisted_pages(
            repo_root, docs_root, surface_map)
        audits_run.append("structure")

    if args.category in (None, "map"):
        if warp_repo and warp_server and extraction_ok:
            print("Running surface map hygiene audit...", file=sys.stderr)
            findings["map_hygiene"] = audit_map_hygiene(
                surface_map, flag_statuses, cli_commands, api_routes,
                slash_commands, settings, docs_root)
            audits_run.append("map")
        else:
            audits_skipped.append({
                "audit": "map",
                "reason": (
                    "requires both the warp client repo and warp-server with healthy "
                    "extraction (dead-entry checks against empty extraction "
                    "would flag everything)"
                ),
            })

    # Change detection (diff + snapshot update)
    changelog_entries = parse_changelog_entries(repo_root)
    snapshot_path = Path(args.snapshot)
    if args.diff or args.update_snapshot:
        if warp_repo and warp_server and extraction_ok:
            current_snapshot = build_snapshot(
                flag_statuses, cli_commands, cli_flags, api_routes,
                slash_commands, settings, web_routes, server_tools,
                bundled_skills, changelog_entries)
            if args.diff:
                previous = load_snapshot(snapshot_path)
                if previous is None:
                    audits_skipped.append({
                        "audit": "diff",
                        "reason": (
                            f"snapshot {snapshot_path} not found or unreadable — "
                            "run --update-snapshot first"
                        ),
                    })
                else:
                    print("Running surface change detection (diff)...", file=sys.stderr)
                    findings["surface_changes"] = diff_snapshots(previous, current_snapshot)
                    findings["changelog_review"] = changelog_review_findings(
                        changelog_entries, previous.get("changelog_last_version"))
                    audits_run.append("diff")
            if args.update_snapshot:
                snapshot_path.parent.mkdir(parents=True, exist_ok=True)
                snapshot_path.write_text(
                    json.dumps(current_snapshot, indent=2, sort_keys=False) + "\n",
                    encoding="utf-8",
                )
                print(f"Snapshot updated: {snapshot_path}", file=sys.stderr)
        else:
            audits_skipped.append({
                "audit": "diff" if args.diff else "update-snapshot",
                "reason": (
                    "requires both the warp client repo and warp-server with healthy "
                    "extraction (see extraction:* skips above)"
                    if not extraction_ok
                    else "requires both the warp client repo and warp-server"
                ),
            })

    # Completeness accounting: prove every extracted surface item lands in
    # exactly one accountability bucket. Runs on full audits with healthy
    # extraction; any unaccounted item means an audit-logic regression and
    # the run is treated as incomplete.
    accounting = None
    if args.category is None and warp_repo and warp_server and extraction_ok:
        accounting = compute_accounting(
            docs_root, surface_map, findings, flag_statuses, cli_commands,
            api_routes, slash_commands, settings, docs_text)
        if accounting["unaccounted"]:
            audits_skipped.append({
                "audit": "integrity:accounting",
                "reason": (
                    "surface items escaped every accountability bucket "
                    f"(audit logic regression): {accounting['unaccounted']}"
                ),
            })

    # Filter by severity
    if args.severity:
        severity_order = {"high": 0, "medium": 1, "low": 2}
        min_severity = severity_order[args.severity]
        for key in list(findings):
            findings[key] = [
                f for f in findings[key]
                if severity_order.get(f.get("severity"), 3) <= min_severity
            ]

    mode = "diff" if args.diff else "audit"
    report = generate_report(findings, audits_run, audits_skipped, mode,
                             accounting=accounting)

    print_report(report)

    if args.output:
        output_path = Path(args.output)
        output_path.write_text(json.dumps(report, indent=2))
        print(f"\nJSON report saved to {output_path}", file=sys.stderr)

    if audits_skipped:
        print(
            "Error: one or more audits were skipped — this run is INCOMPLETE "
            "and must not be treated as a clean audit.",
            file=sys.stderr,
        )
        sys.exit(2)


if __name__ == "__main__":
    main()
