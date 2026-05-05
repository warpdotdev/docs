#!/usr/bin/env python3
"""
Missing Docs Audit Script for Warp Astro Starlight Documentation

Compares documentation coverage against code surfaces in warp-internal and
warp-server to identify gaps. Produces a structured JSON report.

Usage:
    python3 .warp/skills/missing_docs/scripts/audit_docs.py
    python3 .warp/skills/missing_docs/scripts/audit_docs.py --category features
    python3 .warp/skills/missing_docs/scripts/audit_docs.py --output report.json
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

# Paths to reference files (relative to this script)
SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
SURFACE_MAP_PATH = SKILL_DIR / "references" / "feature_surface_map.md"
STALE_TERMS_PATH = SKILL_DIR / "references" / "stale_terms.md"

# ---------------------------------------------------------------------------
# Surface map parser
# ---------------------------------------------------------------------------

def parse_surface_map(path: Path) -> dict:
    """Parse the feature_surface_map.md into structured data."""
    result = {
        "feature_to_doc": {},
        "cli_to_doc": {},
        "api_to_doc": {},
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

def find_repo(name: str, explicit_path: str | None, docs_root: Path) -> Path | None:
    """Find a sibling repo by name, or use the explicit path."""
    if explicit_path:
        p = Path(explicit_path).resolve()
        if p.exists():
            return p
        print(f"Warning: explicit path {explicit_path} does not exist", file=sys.stderr)
        return None

    # Try sibling directory (docs is at .../code/docs, look for .../code/<name>)
    sibling = docs_root.parent / name
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
    """Read all doc files into a dict of {relative_path: content}."""
    result = {}
    for f in find_markdown_files(docs_root):
        try:
            rel = str(f.relative_to(docs_root.parent))  # relative to docs root
            result[rel] = f.read_text(encoding="utf-8").lower()
        except Exception:
            pass
    return result


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

# ---------------------------------------------------------------------------
# Audit 1: Feature flag coverage
# ---------------------------------------------------------------------------

def parse_feature_flags(warp_internal: Path) -> list[str]:
    """Parse FeatureFlag enum variants from features.rs."""
    # The FeatureFlag enum lives in the warp_features crate
    features_rs = warp_internal / "crates" / "warp_features" / "src" / "lib.rs"
    if not features_rs.exists():
        # Fall back to legacy path
        features_rs = warp_internal / "warp_core" / "src" / "features.rs"
    if not features_rs.exists():
        print(f"Warning: {features_rs} not found", file=sys.stderr)
        return []

    content = features_rs.read_text()
    # Match enum variants (lines like "    AgentMode," or "    AgentMode {")
    # inside the FeatureFlag enum
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
            # Skip comments, attributes, empty lines
            if stripped.startswith("//") or stripped.startswith("#[") or stripped.startswith("///") or not stripped:
                continue
            # Extract variant name
            match = re.match(r"^([A-Z]\w+)", stripped)
            if match:
                flags.append(match.group(1))
    return flags


def parse_default_features(warp_internal: Path) -> set[str]:
    """Parse the default feature list from app/Cargo.toml."""
    cargo_toml = warp_internal / "app" / "Cargo.toml"
    if not cargo_toml.exists():
        print(f"Warning: {cargo_toml} not found", file=sys.stderr)
        return set()

    content = cargo_toml.read_text()
    # Find the default = [...] block
    match = re.search(r'default\s*=\s*\[(.*?)\]', content, re.DOTALL)
    if not match:
        return set()

    features_block = match.group(1)
    # Extract quoted feature names
    return set(re.findall(r'"(\w+)"', features_block))


def snake_to_pascal(snake: str) -> str:
    """Convert snake_case to PascalCase: agent_mode -> AgentMode."""
    return "".join(word.capitalize() for word in snake.split("_"))


def audit_features(warp_internal: Path, docs_root: Path, surface_map: dict,
                   docs_text: dict[str, str]) -> list[dict]:
    """Audit feature flag coverage in docs."""
    flags = parse_feature_flags(warp_internal)
    default_features = parse_default_features(warp_internal)
    ignore_flags = surface_map.get("ignore_flags", set())
    feature_to_doc = surface_map.get("feature_to_doc", {})

    findings = []
    for flag in flags:
        # Skip ignored flags
        if flag in ignore_flags:
            continue

        # Determine if GA (in default features)
        snake = re.sub(r"([a-z])([A-Z])", r"\1_\2", flag).lower()
        is_ga = snake in default_features

        # Skip non-GA features (they're behind flags and may not need docs yet)
        if not is_ga:
            continue

        # Check if mapped in surface map
        if flag in feature_to_doc:
            doc_path = feature_to_doc[flag]
            full_path = docs_root.parent / doc_path
            if full_path.exists():
                continue  # Mapped and doc exists — verified
            else:
                findings.append({
                    "flag": flag,
                    "search_terms": camel_to_search_terms(flag),
                    "severity": "high",
                    "suggested_doc_path": doc_path,
                    "reason": f"Mapped doc {doc_path} does not exist",
                })
                continue

        # Not in surface map — search docs for mentions
        terms = camel_to_search_terms(flag)
        matches = search_docs_for_terms(docs_text, terms)
        if not matches:
            findings.append({
                "flag": flag,
                "search_terms": terms,
                "severity": "medium",
                "suggested_doc_path": None,
                "reason": "GA feature with no doc mentions found",
            })

    return findings

# ---------------------------------------------------------------------------
# Audit 2: CLI command coverage
# ---------------------------------------------------------------------------

def parse_cli_commands(warp_internal: Path) -> list[dict]:
    """Parse CLI subcommands from warp_cli/src/lib.rs."""
    lib_rs = warp_internal / "warp_cli" / "src" / "lib.rs"
    if not lib_rs.exists():
        return []

    content = lib_rs.read_text()
    commands = []

    # Find CliCommand enum variants
    in_enum = False
    for line in content.splitlines():
        stripped = line.strip()
        if "enum CliCommand" in stripped:
            in_enum = True
            continue
        if in_enum:
            if stripped == "}":
                break
            # Match lines like "Agent(crate::agent::AgentCommand),"
            match = re.match(r"^([A-Z]\w+)(?:\(|,|\s*$)", stripped)
            if match:
                name = match.group(1)
                # Convert PascalCase to lowercase command name
                cmd_name = re.sub(r"([a-z])([A-Z])", r"\1-\2", name).lower()
                # Find source file
                source_match = re.search(rf"crate::(\w+)::", stripped)
                source_file = f"warp_cli/src/{source_match.group(1)}.rs" if source_match else None
                commands.append({
                    "name": name,
                    "command": f"oz {cmd_name}",
                    "source_file": source_file,
                })

    return commands


def parse_subcommands_from_file(warp_internal: Path, filename: str) -> list[str]:
    """Parse subcommand names from a CLI command file (e.g., agent.rs)."""
    filepath = warp_internal / "warp_cli" / "src" / filename
    if not filepath.exists():
        return []

    content = filepath.read_text()
    subcommands = []

    # Find enum variants that represent subcommands
    for match in re.finditer(r"///\s*(.+?)\n\s*(?:#\[.*?\]\s*\n\s*)*([A-Z]\w+)", content):
        subcommands.append(match.group(2))

    return subcommands


def audit_cli(warp_internal: Path, docs_root: Path, surface_map: dict,
              docs_text: dict[str, str]) -> list[dict]:
    """Audit CLI command coverage in docs."""
    commands = parse_cli_commands(warp_internal)
    cli_to_doc = surface_map.get("cli_to_doc", {})

    # Read all CLI docs content
    cli_docs_dir = docs_root / "reference" / "cli"
    cli_docs_text = {}
    if cli_docs_dir.exists():
        for f in find_markdown_files(cli_docs_dir):
            try:
                cli_docs_text[str(f)] = f.read_text(encoding="utf-8").lower()
            except Exception:
                pass

    findings = []
    for cmd in commands:
        cmd_str = cmd["command"]

        # Check surface map
        if cmd_str in cli_to_doc:
            doc_path = cli_to_doc[cmd_str]
            if (docs_root.parent / doc_path).exists():
                continue  # Mapped and exists

        # Search CLI docs for the command name
        cmd_name = cmd_str.split()[-1]  # e.g., "agent" from "oz agent"
        found = False
        for content in cli_docs_text.values():
            if cmd_name in content:
                found = True
                break

        if not found:
            findings.append({
                "command": cmd_str,
                "source_file": cmd.get("source_file"),
                "severity": "high",
                "reason": f"CLI command '{cmd_str}' not mentioned in CLI reference docs",
            })

    return findings

# ---------------------------------------------------------------------------
# Audit 3: API endpoint coverage
# ---------------------------------------------------------------------------

def parse_api_routes(warp_server: Path) -> list[dict]:
    """Parse API route definitions from router.go."""
    router_go = warp_server / "router" / "router.go"
    if not router_go.exists():
        return []

    content = router_go.read_text()
    routes = []

    # Match patterns like:
    #   r.GET("/api/v1/agent/runs", ...)
    #   r.POST("/api/v1/agent/run", ...)
    for match in re.finditer(
        r'\.\s*(GET|POST|PUT|DELETE|PATCH)\s*\(\s*"(/[^"]+)"',
        content,
    ):
        method = match.group(1)
        path = match.group(2)
        # Skip internal/debug endpoints
        if "/internal/" in path or "/debug/" in path:
            continue
        routes.append({
            "method": method,
            "path": path,
            "route": f"{method} {path}",
        })

    return routes


def audit_api(warp_server: Path, docs_root: Path, surface_map: dict,
              docs_text: dict[str, str]) -> list[dict]:
    """Audit API endpoint coverage in docs."""
    routes = parse_api_routes(warp_server)
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

    # Also check OpenAPI spec
    openapi_path = docs_root / "developers" / "agent-api-openapi.yaml"
    openapi_text = ""
    if openapi_path.exists():
        try:
            openapi_text = openapi_path.read_text(encoding="utf-8").lower()
        except Exception:
            pass

    findings = []
    for route in routes:
        route_str = route["route"]

        # Check surface map
        if route_str in api_to_doc:
            continue

        # Search API docs and OpenAPI spec for the path
        path_lower = route["path"].lower()
        found = False
        for content in api_docs_text.values():
            if path_lower in content:
                found = True
                break
        if not found and path_lower in openapi_text:
            found = True

        if not found:
            # Determine handler file
            handler_file = None
            handlers_dir = warp_server / "router" / "handlers"
            if handlers_dir.exists():
                # Try to match based on path segments
                path_parts = [p for p in route["path"].split("/") if p and p != "api" and p != "v1"]
                if path_parts:
                    for f in handlers_dir.iterdir():
                        if f.suffix == ".go" and path_parts[0] in f.name:
                            handler_file = f"router/handlers/{f.name}"
                            break

            findings.append({
                "route": route_str,
                "handler_file": handler_file,
                "severity": "medium",
                "reason": f"API endpoint '{route_str}' not documented in API reference",
            })

    return findings

# ---------------------------------------------------------------------------
# Audit 4: Docs staleness
# ---------------------------------------------------------------------------

def audit_staleness(warp_internal: Path, docs_root: Path,
                    docs_text: dict[str, str],
                    stale_terms_path: Path = STALE_TERMS_PATH) -> list[dict]:
    """Check for docs referencing features that no longer exist in code."""
    # Get current feature flags for comparison
    current_flags = set(parse_feature_flags(warp_internal))
    current_flags_lower = {f.lower() for f in current_flags}

    # Load stale terms from external reference file
    stale_terms = parse_stale_terms(stale_terms_path)

    findings = []
    for doc_path, content in docs_text.items():
        stale_found = []
        for term, reason in stale_terms:
            if term in content:
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
# Report generation
# ---------------------------------------------------------------------------

def generate_report(features: list, cli: list, api: list, staleness: list) -> dict:
    """Assemble the full audit report."""
    total = len(features) + len(cli) + len(api) + len(staleness)
    return {
        "summary": {
            "total_gaps": total,
            "by_category": {
                "undocumented_features": len(features),
                "undocumented_cli_commands": len(cli),
                "undocumented_api_endpoints": len(api),
                "potentially_stale_docs": len(staleness),
            },
        },
        "undocumented_features": features,
        "undocumented_cli_commands": cli,
        "undocumented_api_endpoints": api,
        "potentially_stale_docs": staleness,
    }


def print_report(report: dict) -> None:
    """Print a human-readable report to stdout."""
    summary = report["summary"]
    print("=" * 60)
    print("MISSING DOCS AUDIT REPORT")
    print("=" * 60)
    print(f"Total gaps found: {summary['total_gaps']}")
    for category, count in summary["by_category"].items():
        print(f"  {category}: {count}")
    print()

    severity_order = {"high": 0, "medium": 1, "low": 2}

    if report["undocumented_features"]:
        print("-" * 60)
        print(f"UNDOCUMENTED FEATURES ({len(report['undocumented_features'])})")
        print("-" * 60)
        items = sorted(report["undocumented_features"],
                       key=lambda x: severity_order.get(x.get("severity", "low"), 3))
        for item in items:
            sev = item.get("severity", "?").upper()
            print(f"\n  [{sev}] {item['flag']}")
            print(f"    Reason: {item['reason']}")
            if item.get("suggested_doc_path"):
                print(f"    Suggested: {item['suggested_doc_path']}")
            print(f"    Search terms: {', '.join(item['search_terms'][:3])}")

    if report["undocumented_cli_commands"]:
        print()
        print("-" * 60)
        print(f"UNDOCUMENTED CLI COMMANDS ({len(report['undocumented_cli_commands'])})")
        print("-" * 60)
        for item in report["undocumented_cli_commands"]:
            sev = item.get("severity", "?").upper()
            print(f"\n  [{sev}] {item['command']}")
            print(f"    Reason: {item['reason']}")
            if item.get("source_file"):
                print(f"    Source: {item['source_file']}")

    if report["undocumented_api_endpoints"]:
        print()
        print("-" * 60)
        print(f"UNDOCUMENTED API ENDPOINTS ({len(report['undocumented_api_endpoints'])})")
        print("-" * 60)
        for item in report["undocumented_api_endpoints"]:
            sev = item.get("severity", "?").upper()
            print(f"\n  [{sev}] {item['route']}")
            print(f"    Reason: {item['reason']}")
            if item.get("handler_file"):
                print(f"    Handler: {item['handler_file']}")

    if report["potentially_stale_docs"]:
        print()
        print("-" * 60)
        print(f"POTENTIALLY STALE DOCS ({len(report['potentially_stale_docs'])})")
        print("-" * 60)
        for item in report["potentially_stale_docs"]:
            sev = item.get("severity", "?").upper()
            print(f"\n  [{sev}] {item['doc_path']}")
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
        help="Path to warp-internal repo (auto-detected if not provided)",
    )
    parser.add_argument(
        "--warp-server",
        help="Path to warp-server repo (auto-detected if not provided)",
    )
    parser.add_argument(
        "--output", "-o",
        help="Save JSON report to file",
    )
    parser.add_argument(
        "--category",
        choices=["features", "cli", "api", "staleness"],
        help="Run only a specific audit category",
    )
    parser.add_argument(
        "--severity",
        choices=["high", "medium", "low"],
        help="Filter results by minimum severity",
    )
    args = parser.parse_args()

    # Find repos
    docs_root = SKILL_DIR.parent.parent.parent  # .warp/skills/missing_docs -> docs root
    docs_root = docs_root / "docs"

    if not docs_root.exists():
        print(f"Error: docs directory not found at {docs_root}", file=sys.stderr)
        sys.exit(1)

    warp_internal = find_repo("warp-internal", args.warp_internal, docs_root)
    warp_server = find_repo("warp-server", args.warp_server, docs_root)

    # Parse surface map
    surface_map = parse_surface_map(SURFACE_MAP_PATH)

    # Read all docs
    print("Scanning documentation...", file=sys.stderr)
    docs_text = read_all_docs_text(docs_root)
    print(f"  Found {len(docs_text)} markdown files", file=sys.stderr)

    # Run audits
    features_findings = []
    cli_findings = []
    api_findings = []
    staleness_findings = []

    if warp_internal:
        print(f"Using warp-internal: {warp_internal}", file=sys.stderr)
        if args.category in (None, "features"):
            print("Running feature flag coverage audit...", file=sys.stderr)
            features_findings = audit_features(warp_internal, docs_root, surface_map, docs_text)

        if args.category in (None, "cli"):
            print("Running CLI command coverage audit...", file=sys.stderr)
            cli_findings = audit_cli(warp_internal, docs_root, surface_map, docs_text)

        if args.category in (None, "staleness"):
            print("Running docs staleness audit...", file=sys.stderr)
            staleness_findings = audit_staleness(warp_internal, docs_root, docs_text)
    else:
        print("Warning: warp-internal not found, skipping feature/CLI/staleness audits",
              file=sys.stderr)

    if warp_server:
        print(f"Using warp-server: {warp_server}", file=sys.stderr)
        if args.category in (None, "api"):
            print("Running API endpoint coverage audit...", file=sys.stderr)
            api_findings = audit_api(warp_server, docs_root, surface_map, docs_text)
    else:
        print("Warning: warp-server not found, skipping API audit", file=sys.stderr)

    # Filter by severity
    if args.severity:
        severity_order = {"high": 0, "medium": 1, "low": 2}
        min_severity = severity_order[args.severity]
        features_findings = [f for f in features_findings
                             if severity_order.get(f.get("severity"), 3) <= min_severity]
        cli_findings = [f for f in cli_findings
                        if severity_order.get(f.get("severity"), 3) <= min_severity]
        api_findings = [f for f in api_findings
                        if severity_order.get(f.get("severity"), 3) <= min_severity]
        staleness_findings = [f for f in staleness_findings
                              if severity_order.get(f.get("severity"), 3) <= min_severity]

    # Generate report
    report = generate_report(features_findings, cli_findings, api_findings, staleness_findings)

    # Output
    print_report(report)

    if args.output:
        output_path = Path(args.output)
        output_path.write_text(json.dumps(report, indent=2))
        print(f"\nJSON report saved to {output_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
