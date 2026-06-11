#!/usr/bin/env python3
"""
Missing Docs Audit Script for Warp Astro Starlight Documentation

Compares documentation coverage against code surfaces in warp-internal and
warp-server to identify gaps, and (in --diff mode) detects surface changes
since the last committed snapshot. Produces a structured JSON report.

Usage:
    python3 .agents/skills/missing_docs/scripts/audit_docs.py
    python3 .agents/skills/missing_docs/scripts/audit_docs.py --category features
    python3 .agents/skills/missing_docs/scripts/audit_docs.py --output report.json
    python3 .agents/skills/missing_docs/scripts/audit_docs.py --diff
    python3 .agents/skills/missing_docs/scripts/audit_docs.py --update-snapshot

Exit codes:
    0 — all requested audits ran (findings may still exist; check the report)
    1 — fatal setup error (docs directory not found, bad arguments)
    2 — one or more audits were SKIPPED (missing repo paths). Never treat a
        run that exits 2 as a clean audit.
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

# Mutable holder for the docs repo root, set by main()
DOCS_REPO_ROOT: list = [None]

# Paths to reference files (relative to this script)
SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
SURFACE_MAP_PATH = SKILL_DIR / "references" / "feature_surface_map.md"
STALE_TERMS_PATH = SKILL_DIR / "references" / "stale_terms.md"
DEFAULT_SNAPSHOT_PATH = SKILL_DIR / "references" / "surface_snapshot.json"

SNAPSHOT_SCHEMA_VERSION = 1

# ---------------------------------------------------------------------------
# Surface map parser
# ---------------------------------------------------------------------------

def parse_surface_map(path: Path) -> dict:
    """Parse the feature_surface_map.md into structured data."""
    result = {
        "feature_to_doc": {},
        "cli_to_doc": {},
        "api_to_doc": {},
        "slash_to_doc": {},
        "ignore_flags": set(),
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
            elif line.startswith("## Flags to ignore"):
                current_section = "ignore"
            continue

        if current_section == "ignore":
            result["ignore_flags"].add(line)
            continue

        if " -> " in line:
            key, doc_path = line.split(" -> ", 1)
            key = key.strip()
            doc_path = doc_path.strip()
            if current_section == "features":
                result["feature_to_doc"][key] = doc_path
            elif current_section == "cli":
                result["cli_to_doc"][key] = doc_path
            elif current_section == "api":
                result["api_to_doc"][key] = doc_path
            elif current_section == "slash":
                result["slash_to_doc"][key] = doc_path

    return result


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
# Helpers
# ---------------------------------------------------------------------------

def find_repo(name: str, explicit_path: str | None, repo_root: Path) -> Path | None:
    """Find a source repo by explicit path or as a sibling of the docs repo root.

    e.g. docs at /workspace/docs -> look for /workspace/<name>.
    """
    if explicit_path:
        p = Path(explicit_path).resolve()
        if p.exists():
            return p
        print(f"Warning: explicit path {explicit_path} does not exist", file=sys.stderr)
        return None

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


def strip_code_spans(text: str) -> str:
    """Remove fenced code blocks, inline code spans, and <code> elements.

    Used by the staleness audit so CLI examples (e.g. `oz agent run`) don't
    trigger terminology findings meant for prose.
    """
    text = _FENCED_CODE_RE.sub(" ", text)
    text = _HTML_CODE_RE.sub(" ", text)
    text = _INLINE_CODE_RE.sub(" ", text)
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
# Extraction: feature flags (warp-internal)
# ---------------------------------------------------------------------------

def _features_lib_rs(warp_internal: Path) -> Path | None:
    candidates = [
        warp_internal / "crates" / "warp_features" / "src" / "lib.rs",
        warp_internal / "crates" / "warp_core" / "src" / "features.rs",
        warp_internal / "app" / "src" / "features.rs",
        warp_internal / "warp_core" / "src" / "features.rs",
    ]
    return next((c for c in candidates if c.exists()), None)


def parse_feature_flags(warp_internal: Path) -> list[str]:
    """Parse FeatureFlag enum variants from the features lib."""
    features_rs = _features_lib_rs(warp_internal)
    if features_rs is None:
        print("Warning: FeatureFlag enum source not found in warp-internal", file=sys.stderr)
        return []

    content = features_rs.read_text()
    in_enum = False
    flags = []
    for line in content.splitlines():
        stripped = line.strip()
        if "enum FeatureFlag" in stripped:
            in_enum = True
            continue
        if in_enum:
            if stripped == "}":
                break
            if stripped.startswith("//") or stripped.startswith("#[") or not stripped:
                continue
            match = re.match(r"^([A-Z]\w+)", stripped)
            if match:
                flags.append(match.group(1))
    return flags


def parse_flag_list_const(warp_internal: Path, const_name: str) -> set[str]:
    """Parse a `pub const <NAME>: &[FeatureFlag] = &[...]` block into flag names."""
    features_rs = _features_lib_rs(warp_internal)
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


def parse_features_bridge(warp_internal: Path) -> dict[str, dict]:
    """Parse the cargo-feature -> FeatureFlag bridge from app/src/features.rs.

    The authoritative mapping is the `enabled_features()` extend block:

        #[cfg(feature = "am_workflows")]
        FeatureFlag::AgentModeWorkflows,

    Names frequently differ from a naive snake_case conversion, so this
    bridge (not string transformation) decides which cargo feature gates a
    flag. Entries gated on `debug_assertions` are never GA.

    Returns {flag_name: {"cargo_feature": str, "debug_only": bool}}.
    """
    bridge_rs = warp_internal / "app" / "src" / "features.rs"
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


def parse_default_features(warp_internal: Path) -> set[str]:
    """Parse the default feature list from app/Cargo.toml."""
    candidates = [
        warp_internal / "app" / "Cargo.toml",
        warp_internal / "crates" / "warp_features" / "Cargo.toml",
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


def compute_flag_statuses(warp_internal: Path) -> dict[str, str]:
    """Classify every FeatureFlag by rollout status.

    - "ga": gating cargo feature is in app/Cargo.toml default features, or the
      flag is in RELEASE_FLAGS (enabled for all release builds).
    - "preview": in PREVIEW_FLAGS (Preview builds; launching soon).
    - "dogfood": in DOGFOOD_FLAGS (dev team only).
    - "other": none of the above (runtime/experiment-gated or unused). These
      may still be enabled via server-side experiments; the docs changelog
      cross-check covers those launches.
    """
    flags = parse_feature_flags(warp_internal)
    bridge = parse_features_bridge(warp_internal)
    default_features = parse_default_features(warp_internal)
    release_flags = parse_flag_list_const(warp_internal, "RELEASE_FLAGS")
    preview_flags = parse_flag_list_const(warp_internal, "PREVIEW_FLAGS")
    dogfood_flags = parse_flag_list_const(warp_internal, "DOGFOOD_FLAGS")

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
# Extraction: CLI command tree (warp-internal)
# ---------------------------------------------------------------------------

def _extract_enum_block(content: str, enum_name: str) -> str | None:
    """Return the body of `pub enum <enum_name> { ... }` using brace matching."""
    match = re.search(rf"pub enum {enum_name}\s*\{{", content)
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
    """Parse top-level variants of a clap enum body.

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


def parse_cli_commands(warp_internal: Path) -> list[dict]:
    """Parse the full `oz` CLI command tree (top-level + one level of subcommands).

    Returns [{"command": "oz agent", "hidden": bool, "source_file": str,
              "subcommands": [{"command": "oz agent run", "hidden": bool}]}]
    """
    src_candidates = [
        warp_internal / "crates" / "warp_cli" / "src",
        warp_internal / "warp_cli" / "src",
    ]
    src_dir = next((c for c in src_candidates if c.exists()), None)
    if src_dir is None:
        print("Warning: warp_cli/src not found in warp-internal", file=sys.stderr)
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
            "subcommands": [],
        }
        ref = variant["referenced_type"]
        if ref and "::" in ref:
            module = ref.split("::")[0]
            module_file = src_dir / f"{module}.rs"
            if module_file.exists():
                entry["source_file"] = f"warp_cli/src/{module}.rs"
                module_content = module_file.read_text()
                sub_body = _resolve_subcommand_enum(module_content, ref)
                if sub_body is not None:
                    for sub in _parse_enum_variants(sub_body):
                        entry["subcommands"].append({
                            "command": f"oz {cmd_name} {kebab_case(sub['name'])}",
                            "hidden": sub["hidden"] or variant["hidden"],
                        })
        commands.append(entry)
    return commands

# ---------------------------------------------------------------------------
# Extraction: public API routes (warp-server)
# ---------------------------------------------------------------------------

_GO_FUNC_RE = re.compile(r"^func (\w+)\(([^)]*)\)", re.MULTILINE)
_GO_GROUP_ASSIGN_RE = re.compile(r"(\w+)\s*:?=\s*(\w+)\.Group\(\s*\"([^\"]*)\"")
_GO_ROUTE_RE = re.compile(r"(\w+)\.(GET|POST|PUT|DELETE|PATCH)\(\s*\"([^\"]*)\"")
_GO_REGISTER_CALL_RE = re.compile(
    r"(Register\w+)\(\s*(\w+)(?:\.Group\(\s*\"([^\"]*)\"\s*\))?\s*,"
)


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


def parse_public_api_routes(warp_server: Path) -> list[dict]:
    """Extract public API routes from router/handlers/public_api/*.go.

    Routes are registered via nested gin groups, e.g.:

        group := router.Group("/api/v1")              (public_api.go)
        RegisterAgentMessagingRoutes(group.Group("/agent"), ...)
        messages := group.Group("/messages")          (agent_messaging.go)
        messages.POST("", SendMessageHandler(...))    -> POST /api/v1/agent/messages

    This walks group-variable assignments per registration function and
    resolves caller-passed prefixes via Register* call sites, starting from
    RegisterPublicAPIRoutes. Gin `:param` segments are normalized to
    OpenAPI-style `{param}`.
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
        params = fn["params"]
        group_param = None
        router_param = None
        for param_match in re.finditer(r"(\w+)(?:\s*,\s*\w+)*\s+\*gin\.(RouterGroup|Engine)", params):
            if param_match.group(2) == "RouterGroup" and group_param is None:
                group_param = param_match.group(1)
            elif param_match.group(2) == "Engine" and router_param is None:
                router_param = param_match.group(1)

        # var name -> (base, prefix); base is "PARAM" (caller group) or
        # "ROUTER" (engine root)
        var_bases: dict[str, tuple] = {}
        if group_param:
            var_bases[group_param] = ("PARAM", "")
        if router_param:
            var_bases[router_param] = ("ROUTER", "")

        routes = []
        calls = []
        events = []
        for assign in _GO_GROUP_ASSIGN_RE.finditer(fn["body"]):
            events.append(("assign", assign.start(), assign.groups()))
        for route in _GO_ROUTE_RE.finditer(fn["body"]):
            events.append(("route", route.start(), route.groups()))
        for call in _GO_REGISTER_CALL_RE.finditer(fn["body"]):
            events.append(("call", call.start(), call.groups()))
        events.sort(key=lambda e: e[1])

        for kind, _pos, groups in events:
            if kind == "assign":
                target, parent, prefix = groups
                base = var_bases.get(parent)
                if base is not None:
                    var_bases[target] = (base[0], base[1] + prefix)
            elif kind == "route":
                var, method, path = groups
                base = var_bases.get(var)
                if base is not None:
                    routes.append((base[0], method, base[1] + path))
            else:  # call
                callee, arg_var, arg_prefix = groups
                base = var_bases.get(arg_var)
                if base is not None:
                    calls.append((callee, base[0], base[1] + (arg_prefix or "")))
        return {"routes": routes, "calls": calls, "file": fn["file"]}

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
        for callee, base, prefix in info["calls"]:
            callee_prefix = (param_prefix + prefix) if base == "PARAM" else prefix
            emit(callee, callee_prefix)

    if "RegisterPublicAPIRoutes" in analyzed:
        emit("RegisterPublicAPIRoutes", "")
    # Any registration function not reachable from the entry point is assumed
    # to hang off the /api/v1 group (conservative default so routes are never
    # silently dropped).
    for fn_name in sorted(analyzed):
        if fn_name.startswith("Register") and fn_name not in emitted_fns:
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

# ---------------------------------------------------------------------------
# Extraction: slash commands (warp-internal)
# ---------------------------------------------------------------------------

def parse_slash_commands(warp_internal: Path) -> list[str]:
    """Parse static slash command names from the registry."""
    registry_dir = (
        warp_internal / "app" / "src" / "search" / "slash_command_menu" / "static_commands"
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
# Extraction: docs changelog entries
# ---------------------------------------------------------------------------

_CHANGELOG_HEADER_RE = re.compile(r"^### (\d{4}\.\d{2}\.\d{2})", re.MULTILINE)
_CHANGELOG_TRACKED_SECTIONS = ("new features", "improvements")


def parse_changelog_entries(repo_root: Path) -> list[dict]:
    """Parse release entries from src/content/docs/changelog/<year>.mdx.

    Returns [{"version": "2026.06.03", "file": str, "items":
              [{"category": "new features", "text": str}]}] sorted newest first.
    Only "New features" and "Improvements" bullets are tracked — those are the
    sections that may represent undocumented feature launches.
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

def audit_features(warp_internal: Path, docs_root: Path, surface_map: dict,
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
        flag_statuses = compute_flag_statuses(warp_internal)
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

def audit_cli(warp_internal: Path, docs_root: Path, surface_map: dict,
              docs_text: dict[str, str]) -> list[dict]:
    """Audit CLI command and subcommand coverage in docs."""
    commands = parse_cli_commands(warp_internal)
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
            if resolve_doc_path(doc_path, repo_root) is not None:
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
              docs_text: dict[str, str]) -> list[dict]:
    """Audit public API endpoint coverage in the OpenAPI spec and API docs.

    The public docs API reference (docs.warp.dev/api) renders
    developers/agent-api-openapi.yaml, so a route missing from the spec is a
    docs gap. Use the warp-server `update-open-api-spec` skill / docs
    `sync-openapi-spec` skill to fix spec drift rather than hand-editing.
    """
    routes = parse_public_api_routes(warp_server)
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

    findings = []
    for route in routes:
        route_str = route["route"]

        # Surface-map entries use the path relative to /api/v1 (e.g.
        # "POST /agent/run"); also accept the full path for compatibility.
        rel_path = route["path"]
        if rel_path.startswith("/api/v1"):
            rel_path = rel_path[len("/api/v1"):] or "/"
        rel_route_str = f"{route['method']} {rel_path}"
        if route_str in api_to_doc or rel_route_str in api_to_doc:
            continue

        # Search the OpenAPI spec and API docs for the path
        found = False
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


def audit_slash_commands(warp_internal: Path, docs_root: Path, surface_map: dict,
                         docs_text: dict[str, str]) -> list[dict]:
    """Audit static slash command coverage in docs."""
    names = parse_slash_commands(warp_internal)
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
# Audit 5: Docs staleness
# ---------------------------------------------------------------------------

def audit_staleness(warp_internal: Path, docs_root: Path,
                    docs_text: dict[str, str],
                    stale_terms_path: Path = STALE_TERMS_PATH) -> list[dict]:
    """Check existing docs for stale terminology.

    Code spans are stripped first (CLI examples like `oz agent run` are
    legitimate command syntax, not terminology) and terms match on word
    boundaries only. Broader terminology enforcement is owned by the
    style_lint skill; this audit only flags terms tied to renamed/removed
    features.
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
# Audit 6: Surface map hygiene
# ---------------------------------------------------------------------------

def audit_map_hygiene(surface_map: dict, flag_statuses: dict[str, str],
                      cli_commands: list[dict], api_routes: list[dict],
                      slash_commands: list[str], docs_root: Path) -> list[dict]:
    """Flag surface-map entries that reference code surfaces that no longer exist.

    Dead entries usually mean a feature was renamed or removed — verify the
    target doc page is still accurate, then prune or update the entry.
    """
    findings = []
    repo_root = DOCS_REPO_ROOT[0] or docs_root.parent.parent.parent
    known_flags = set(flag_statuses)

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

    # Mapped doc targets that no longer exist (any section).
    for section, mapping in (
        ("Feature flags", surface_map.get("feature_to_doc", {})),
        ("CLI commands", surface_map.get("cli_to_doc", {})),
        ("API endpoints", surface_map.get("api_to_doc", {})),
        ("Slash commands", surface_map.get("slash_to_doc", {})),
    ):
        for key, doc_path in sorted(mapping.items()):
            if doc_path == "internal":
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
                   api_routes: list[dict], slash_commands: list[str],
                   changelog_entries: list[dict]) -> dict:
    """Assemble the surface snapshot (deterministic ordering for clean diffs)."""
    cli_flat = []
    for cmd in cli_commands:
        cli_flat.append({"command": cmd["command"], "hidden": cmd["hidden"]})
        for sub in cmd["subcommands"]:
            cli_flat.append({"command": sub["command"], "hidden": sub["hidden"]})
    cli_flat.sort(key=lambda c: c["command"])

    return {
        "schema_version": SNAPSHOT_SCHEMA_VERSION,
        "flags": dict(sorted(flag_statuses.items())),
        "cli_commands": cli_flat,
        "api_routes": sorted(r["route"] for r in api_routes),
        "slash_commands": sorted(slash_commands),
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

    old_api = set(old.get("api_routes", []))
    new_api = set(new.get("api_routes", []))
    for route in sorted(new_api - old_api):
        findings.append({
            "change": "api_added",
            "surface": route,
            "severity": "medium",
            "reason": (
                f"New public API route '{route}' — add it to the OpenAPI spec "
                "(sync-openapi-spec skill) or map it as internal"
            ),
        })
    for route in sorted(old_api - new_api):
        findings.append({
            "change": "api_removed",
            "surface": route,
            "severity": "medium",
            "reason": (
                f"Public API route '{route}' was removed — verify the OpenAPI "
                "spec and API docs no longer document it"
            ),
        })

    old_slash = set(old.get("slash_commands", []))
    new_slash = set(new.get("slash_commands", []))
    for name in sorted(new_slash - old_slash):
        findings.append({
            "change": "slash_added",
            "surface": name,
            "severity": "medium",
            "reason": (
                f"New slash command '{name}' — add it to the slash-commands docs "
                "page or map it as internal"
            ),
        })
    for name in sorted(old_slash - new_slash):
        findings.append({
            "change": "slash_removed",
            "surface": name,
            "severity": "medium",
            "reason": (
                f"Slash command '{name}' was removed — update the slash-commands "
                "docs page and surface map"
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
    ("surface_changes", "SURFACE CHANGES SINCE SNAPSHOT",
     lambda i: f"{i.get('change', '')}: {i.get('surface', '')}"),
    ("changelog_review", "CHANGELOG ITEMS TO VERIFY",
     lambda i: f"{i.get('version', '')} [{i.get('category', '')}] {i.get('text', '')[:100]}"),
    ("map_hygiene", "SURFACE MAP HYGIENE",
     lambda i: f"{i.get('section', '')}: {i.get('entry', '')}"),
    ("potentially_stale_docs", "POTENTIALLY STALE DOCS",
     lambda i: i.get("doc_path", "")),
]


def generate_report(findings_by_category: dict[str, list], audits_run: list[str],
                    audits_skipped: list[dict], mode: str) -> dict:
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
        "--warp-internal",
        help="Path to warp-internal repo (auto-detected as a sibling of the docs repo)",
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
        choices=["features", "cli", "api", "slash", "staleness", "map"],
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

    warp_internal = find_repo("warp-internal", args.warp_internal, repo_root)
    warp_server = find_repo("warp-server", args.warp_server, repo_root)

    # Parse surface map
    surface_map = parse_surface_map(SURFACE_MAP_PATH)

    # Read all docs
    print("Scanning documentation...", file=sys.stderr)
    docs_text = read_all_docs_text(docs_root)
    print(f"  Found {len(docs_text)} markdown files", file=sys.stderr)

    findings: dict[str, list] = {}
    audits_run: list[str] = []
    audits_skipped: list[dict] = []

    needs_internal = args.category in (None, "features", "cli", "slash", "staleness", "map") \
        or args.diff or args.update_snapshot
    needs_server = args.category in (None, "api", "map") \
        or args.diff or args.update_snapshot

    flag_statuses: dict[str, str] = {}
    cli_commands: list[dict] = []
    slash_commands: list[str] = []
    api_routes: list[dict] = []

    if warp_internal and needs_internal:
        print(f"Using warp-internal: {warp_internal}", file=sys.stderr)
        flag_statuses = compute_flag_statuses(warp_internal)
        cli_commands = parse_cli_commands(warp_internal)
        slash_commands = parse_slash_commands(warp_internal)

        if args.category in (None, "features"):
            print("Running feature flag coverage audit...", file=sys.stderr)
            findings["undocumented_features"] = audit_features(
                warp_internal, docs_root, surface_map, docs_text,
                flag_statuses=flag_statuses, weak_coverage=args.weak_coverage,
            )
            audits_run.append("features")

        if args.category in (None, "cli"):
            print("Running CLI command coverage audit...", file=sys.stderr)
            findings["undocumented_cli_commands"] = audit_cli(
                warp_internal, docs_root, surface_map, docs_text)
            audits_run.append("cli")

        if args.category in (None, "slash"):
            print("Running slash command coverage audit...", file=sys.stderr)
            findings["undocumented_slash_commands"] = audit_slash_commands(
                warp_internal, docs_root, surface_map, docs_text)
            audits_run.append("slash")

        if args.category in (None, "staleness"):
            print("Running docs staleness audit...", file=sys.stderr)
            findings["potentially_stale_docs"] = audit_staleness(
                warp_internal, docs_root, docs_text)
            audits_run.append("staleness")
    elif needs_internal:
        for audit in ("features", "cli", "slash", "staleness"):
            if args.category in (None, audit):
                audits_skipped.append({
                    "audit": audit,
                    "reason": "warp-internal repo not found (pass --warp-internal)",
                })

    if warp_server and needs_server:
        print(f"Using warp-server: {warp_server}", file=sys.stderr)
        api_routes = parse_public_api_routes(warp_server)
        if args.category in (None, "api"):
            print("Running API endpoint coverage audit...", file=sys.stderr)
            findings["undocumented_api_endpoints"] = audit_api(
                warp_server, docs_root, surface_map, docs_text)
            audits_run.append("api")
    elif needs_server:
        if args.category in (None, "api"):
            audits_skipped.append({
                "audit": "api",
                "reason": "warp-server repo not found (pass --warp-server)",
            })

    if args.category in (None, "map"):
        if warp_internal and warp_server:
            print("Running surface map hygiene audit...", file=sys.stderr)
            findings["map_hygiene"] = audit_map_hygiene(
                surface_map, flag_statuses, cli_commands, api_routes,
                slash_commands, docs_root)
            audits_run.append("map")
        else:
            audits_skipped.append({
                "audit": "map",
                "reason": "requires both warp-internal and warp-server",
            })

    # Change detection (diff + snapshot update)
    changelog_entries = parse_changelog_entries(repo_root)
    snapshot_path = Path(args.snapshot)
    if args.diff or args.update_snapshot:
        if warp_internal and warp_server:
            current_snapshot = build_snapshot(
                flag_statuses, cli_commands, api_routes, slash_commands,
                changelog_entries)
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
                "reason": "requires both warp-internal and warp-server",
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
    report = generate_report(findings, audits_run, audits_skipped, mode)

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
