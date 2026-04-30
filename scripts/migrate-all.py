#!/usr/bin/env python3
"""Master migration: convert ALL GitBook content to Astro Starlight.

Handles the structural remapping between repos:
  - gitbook/docs/warp/*  → docs top-level (terminal/, code/, getting-started/, knowledge-and-collaboration/)
  - gitbook/docs/agent-platform/warp-agents/*  → split into capabilities/ and local-agents/
  - gitbook/docs/agent-platform/cli-agents/*   → agent-platform/cli-agents/
  - gitbook/guides/*  → university/
  - README.md → index.mdx everywhere

Usage:
    python scripts/migrate-all.py /path/to/gitbook
"""

import json
import re
import shutil
import sys
from pathlib import Path

# Import conversion functions from existing script
sys.path.insert(0, str(Path(__file__).parent))
from importlib.machinery import SourceFileLoader
convert_mod = SourceFileLoader("convert_gitbook", str(Path(__file__).parent / "convert-gitbook.py")).load_module()

# Re-export all conversion functions
parse_frontmatter = convert_mod.parse_frontmatter
build_frontmatter = convert_mod.build_frontmatter
strip_first_h1 = convert_mod.strip_first_h1
convert_hints = convert_mod.convert_hints
convert_embeds = convert_mod.convert_embeds
convert_tabs = convert_mod.convert_tabs
convert_code_blocks = convert_mod.convert_code_blocks
convert_steppers = convert_mod.convert_steppers
strip_gitbook_card_tables = convert_mod.strip_gitbook_card_tables
strip_gitbook_content_refs = convert_mod.strip_gitbook_content_refs
convert_figures = convert_mod.convert_figures
convert_inline_images = convert_mod.convert_inline_images
convert_html_comments = convert_mod.convert_html_comments
strip_custom_anchors = convert_mod.strip_custom_anchors
convert_horizontal_rules = convert_mod.convert_horizontal_rules
sanitize_html_tables = convert_mod.sanitize_html_tables
fix_html_void_elements = convert_mod.fix_html_void_elements
convert_autolinks = convert_mod.convert_autolinks
inject_imports = convert_mod.inject_imports
sanitize_asset_filename = convert_mod.sanitize_asset_filename
KEEP_FRONTMATTER_KEYS = convert_mod.KEEP_FRONTMATTER_KEYS

# ---------------------------------------------------------------------------
# Path mapping configuration
# ---------------------------------------------------------------------------

# warp-agents files that go to capabilities/
CAPABILITIES_FILES = {
    "agent-profiles-permissions", "skills", "planning", "task-lists",
    "model-choice", "rules", "full-terminal-use", "computer-use",
    "codebase-context", "web-search", "mcp", "slash-commands",
    "agent-notifications",
}

# warp-agents files that go to local-agents/
LOCAL_AGENTS_FILES = {
    "active-ai", "code-diffs", "session-sharing", "cloud-conversations",
    "interactive-code-review",
}

# warp-agents/README.md → local-agents/overview.mdx
# warp-agents/capabilities-overview.md → capabilities/index.mdx
# warp-agents/interacting-with-agents/* → local-agents/interacting-with-agents/*
# warp-agents/agent-context/* → local-agents/agent-context/*

# Rename map for specific files
RENAME_MAP = {
    "warp-agents/README.md": "local-agents/overview.mdx",
    "warp-agents/capabilities-overview.md": "capabilities/index.mdx",
    # The legacy `agent-modality.mdx` file was renamed to
    # `terminal-and-agent-modes.mdx` in the 2026-04-29 sync to align with
    # AGENTS.md style guidance ("Agent Modality" was an internal name).
    "warp-agents/interacting-with-agents/terminal-and-agent-modes.md": "local-agents/interacting-with-agents/terminal-and-agent-modes.mdx",
}

# Per-space rename map for files that the docs repo intentionally moved away
# from the gitbook layout. Values are paths relative to the docs root
# (`src/content/docs/`).
WARP_RENAME_MAP = {
    # Quickstart pages live under getting-started/quickstart/ in the docs
    # repo even though gitbook keeps them flat under getting-started/.
    "getting-started/coding-in-warp.md": "getting-started/quickstart/coding-in-warp.mdx",
    "getting-started/customizing-warp.md": "getting-started/quickstart/customizing-warp.mdx",
    "getting-started/installation-and-setup.md": "getting-started/quickstart/installation-and-setup.mdx",
    # Top-level landing pages were renamed during the original migration.
    "getting-started/quickstart.md": "quickstart.mdx",
    "README.md": "index.mdx",
}

# Per-space skip set for orphaned/duplicate gitbook files that the docs repo
# intentionally drops. Values are gitbook-relative paths.
SKIP_PATHS = {
    "support-and-community": {
        # Duplicate of logging-out-and-uninstalling.md kept around in gitbook
        # only as a redirect target.
        "troubleshooting-and-support/uninstalling-warp.md",
    },
}


def compute_docs_url_path(gitbook_space: str, gitbook_rel: str) -> str:
    """Given a gitbook space and relative file path, compute the URL path in the docs site.
    
    This is used for link rewriting. Returns a URL path like /agent-platform/capabilities/skills/
    """
    # Apply the structural remapping
    dest = map_gitbook_path(gitbook_space, gitbook_rel)
    # Convert to URL path
    url = dest.replace(".mdx", "/")
    if url.endswith("/index/"):
        url = url[:-6]  # /foo/index/ -> /foo/
    if not url.startswith("/"):
        url = "/" + url
    if not url.endswith("/"):
        url += "/"
    return url


def map_gitbook_path(space: str, rel_path: str) -> str:
    """Map a gitbook file path to its docs destination path.
    
    Args:
        space: One of 'warp', 'agent-platform', 'reference', 'support-and-community', 
               'enterprise', 'changelog', 'guides'
        rel_path: Path relative to the space root (e.g. 'terminal/blocks/block-basics.md')
    
    Returns:
        Path relative to src/content/docs/ (e.g. 'terminal/blocks/block-basics.mdx')
    """
    p = rel_path
    
    if space == "warp":
        # warp/ content strips the prefix and goes to top-level sections.
        # First check the docs-specific rename map for files that landed at
        # different paths during the original migration (e.g. quickstart pages
        # were folded into getting-started/quickstart/).
        if p in WARP_RENAME_MAP:
            return WARP_RENAME_MAP[p]
        # Otherwise the rel_path is already relative to warp/, so just convert
        # the extension below.
        pass
    elif space == "agent-platform":
        # Handle warp-agents/ split
        if p.startswith("warp-agents/"):
            inner = p[len("warp-agents/"):]
            # Check explicit rename map first. RENAME_MAP values are paths
            # relative to the agent-platform/ root, so we still need to add
            # the agent-platform/ prefix and then return early before the
            # README.md → index.mdx normalization runs.
            if p in RENAME_MAP:
                return "agent-platform/" + RENAME_MAP[p]
            # interacting-with-agents/* → local-agents/interacting-with-agents/*
            if inner.startswith("interacting-with-agents/"):
                p = "local-agents/" + inner
            # agent-context/* → local-agents/agent-context/*
            elif inner.startswith("agent-context/"):
                p = "local-agents/" + inner
            else:
                stem = inner.replace(".md", "").replace("/README", "")
                if stem in CAPABILITIES_FILES:
                    p = "capabilities/" + inner
                elif stem in LOCAL_AGENTS_FILES:
                    p = "local-agents/" + inner
                else:
                    # Default to capabilities for unknown
                    p = "capabilities/" + inner
            p = "agent-platform/" + p
        else:
            p = "agent-platform/" + p
    elif space == "guides":
        p = "university/" + p
    else:
        # reference, support-and-community, enterprise, changelog
        p = space + "/" + p
    
    # README.md → index.mdx
    if p.endswith("/README.md"):
        p = p[:-len("/README.md")] + "/index.mdx"
    elif p == "README.md":
        p = "index.mdx"
    else:
        p = p[:-3] + ".mdx"
    
    return p


def map_asset_space(space: str) -> str:
    """Map a gitbook space to an asset directory name."""
    if space == "warp":
        return "terminal"  # warp assets go to terminal/
    elif space == "guides":
        return "university"
    else:
        return space


# ---------------------------------------------------------------------------
# Enhanced link rewriting
# ---------------------------------------------------------------------------

# Cross-space link patterns that need special handling
CROSS_SPACE_LINK_MAP = {
    # From warp space, links to agent-platform
    "../agent-platform/": "/agent-platform/",
    # From agent-platform, links to warp
    "../warp/": "/",
}


def convert_links_enhanced(content: str, file_rel_dir: str, space: str) -> str:
    """Rewrite relative .md links to absolute URL paths with structural remapping."""

    def _rewrite_link(m):
        text = m.group(1)
        href = m.group(2)
        fragment = ""

        # Skip external, absolute, anchor-only, and mailto links
        if href.startswith(("http://", "https://", "/", "#", "mailto:")):
            return m.group(0)

        # Separate fragment
        if "#" in href:
            href, fragment = href.split("#", 1)
            fragment = "#" + fragment

        if not href:
            return f"[{text}](#{fragment[1:]})" if fragment else m.group(0)

        # Handle cross-space links (../agent-platform/, ../warp/, etc.)
        cross_space = None
        cross_rel = href
        for prefix, url_prefix in CROSS_SPACE_LINK_MAP.items():
            if href.startswith(prefix):
                cross_rel = href[len(prefix):]
                if prefix.startswith("../agent-platform"):
                    cross_space = "agent-platform"
                elif prefix.startswith("../warp"):
                    cross_space = "warp"
                break
        
        if cross_space:
            # Resolve the cross-space link
            parts = cross_rel.split("/")
            normalised = [p for p in parts if p and p != "."]
            resolved = []
            for p in normalised:
                if p == "..":
                    if resolved:
                        resolved.pop()
                else:
                    resolved.append(p)
            cross_file = "/".join(resolved)
            if not cross_file.endswith(".md"):
                if not cross_file:
                    cross_file = "README.md"
                else:
                    cross_file += ".md" if "." not in cross_file.split("/")[-1] else ""
            url = compute_docs_url_path(cross_space, cross_file)
            return f"[{text}]({url}{fragment})"

        # Normalise the path relative to the current file's directory
        parts = ((file_rel_dir + "/" + href) if file_rel_dir else href).split("/")
        normalised = []
        for p in parts:
            if p == "..":
                if normalised:
                    normalised.pop()
            elif p and p != ".":
                normalised.append(p)
        rel = "/".join(normalised)

        # Compute URL from the resolved gitbook-relative path
        if rel.endswith(".md"):
            url = compute_docs_url_path(space, rel)
        else:
            # Treat as directory → README.md
            readme = (rel + "/README.md") if rel else "README.md"
            url = compute_docs_url_path(space, readme)

        return f"[{text}]({url}{fragment})"

    # Negative lookbehind to skip image links ![alt](url)
    return re.sub(r"(?<!!)\[([^\]]*)\]\(([^)]+)\)", _rewrite_link, content)


# ---------------------------------------------------------------------------
# Enhanced file conversion
# ---------------------------------------------------------------------------


def compute_rel_asset_prefix(dst_path: Path, docs_root: Path) -> str:
    """Compute relative path from a doc file to its asset directory."""
    try:
        rel_to_content = dst_path.relative_to(docs_root / "src" / "content" / "docs")
    except ValueError:
        return "../../../../assets/terminal/"
    
    # Determine which asset directory to use based on the content path
    parts = rel_to_content.parts
    if len(parts) > 0 and parts[0] == "agent-platform":
        asset_dir = "agent-platform"
    elif len(parts) > 0 and parts[0] == "reference":
        asset_dir = "reference"
    elif len(parts) > 0 and parts[0] == "support-and-community":
        asset_dir = "support-and-community"
    elif len(parts) > 0 and parts[0] == "university":
        asset_dir = "university"
    elif len(parts) > 0 and parts[0] == "enterprise":
        asset_dir = "enterprise"
    else:
        asset_dir = "terminal"
    
    depth = len(rel_to_content.parent.parts)
    # From content/docs/<subdirs> up to src/: 2 + depth (content/docs = 2 levels)
    ups = 2 + depth
    return "../" * ups + f"assets/{asset_dir}/"


def convert_file_enhanced(
    src_path: Path,
    dst_path: Path,
    space: str,
    gitbook_space_root: Path,
    docs_root: Path,
) -> str:
    """Convert a single GitBook markdown file to Starlight MDX with enhanced link rewriting."""
    content = src_path.read_text(encoding="utf-8")

    # Determine relative directory within the space
    try:
        file_rel = src_path.relative_to(gitbook_space_root)
    except ValueError:
        file_rel = Path(src_path.name)
    file_rel_dir = str(file_rel.parent) if str(file_rel.parent) != "." else ""

    # Compute asset prefix from destination path
    rel_asset_prefix = compute_rel_asset_prefix(dst_path, docs_root)

    # 1. Parse and rebuild frontmatter
    fm, body = parse_frontmatter(content)
    for key in list(fm.keys()):
        if key not in KEEP_FRONTMATTER_KEYS:
            del fm[key]
    new_fm = build_frontmatter(fm, body)
    body = strip_first_h1(body)

    # 2. Apply transforms (order matters)
    body = convert_hints(body)
    body = convert_embeds(body)
    body = convert_tabs(body)
    body = convert_code_blocks(body)
    body = convert_steppers(body)
    body = strip_gitbook_card_tables(body)
    body = strip_gitbook_content_refs(body)
    body = convert_figures(body, rel_asset_prefix)
    body = convert_inline_images(body, rel_asset_prefix)
    body = convert_links_enhanced(body, file_rel_dir, space)
    body = convert_html_comments(body)
    body = strip_custom_anchors(body)
    body = convert_horizontal_rules(body)
    body = sanitize_html_tables(body)
    body = fix_html_void_elements(body)
    body = convert_autolinks(body)

    # 3. Reassemble
    result = new_fm + "\n" + body

    # 4. Inject MDX imports
    result = inject_imports(result)

    # 5. Clean up excessive blank lines
    result = re.sub(r"\n{3,}", "\n\n", result)

    if not result.endswith("\n"):
        result += "\n"

    return result


# ---------------------------------------------------------------------------
# Asset collection and copying
# ---------------------------------------------------------------------------


def copy_space_assets(gitbook_space_root: Path, asset_dir: Path) -> int:
    """Copy all referenced assets from a gitbook space to the docs asset directory."""
    gitbook_assets = gitbook_space_root / ".gitbook" / "assets"
    if not gitbook_assets.is_dir():
        return 0
    
    asset_dir.mkdir(parents=True, exist_ok=True)
    
    # Collect all referenced asset filenames
    referenced = {}
    for md_file in gitbook_space_root.rglob("*.md"):
        if md_file.name == "SUMMARY.md":
            continue
        try:
            content = md_file.read_text(encoding="utf-8")
        except Exception:
            continue
        for m in re.finditer(r'\.gitbook/assets/([^")\s]+)', content):
            original = m.group(1).strip()
            if original:
                referenced[original] = sanitize_asset_filename(original)
    
    # Also copy any unreferenced assets (they might be referenced by converted content)
    for asset_file in gitbook_assets.iterdir():
        if asset_file.is_file():
            name = asset_file.name
            if name not in referenced:
                referenced[name] = sanitize_asset_filename(name)
    
    copied = 0
    for original_name, safe_name in sorted(referenced.items()):
        asset_src = gitbook_assets / original_name
        if asset_src.exists():
            dest = asset_dir / safe_name
            if not dest.exists() or asset_src.stat().st_size != dest.stat().st_size:
                shutil.copy2(asset_src, dest)
                copied += 1
    
    return copied


# ---------------------------------------------------------------------------
# Redirect extraction
# ---------------------------------------------------------------------------


def parse_gitbook_yaml_redirects(yaml_path: Path) -> dict:
    """Parse redirects from a .gitbook.yaml file. Returns dict of source->target."""
    if not yaml_path.exists():
        return {}
    
    content = yaml_path.read_text(encoding="utf-8")
    redirects = {}
    in_redirects = False
    
    for line in content.split("\n"):
        stripped = line.strip()
        if stripped == "redirects:":
            in_redirects = True
            continue
        if in_redirects:
            if not line.startswith("    ") and not line.startswith("\t") and stripped and not stripped.startswith("#"):
                break
            m = re.match(r"\s+([^#:][^:]*?):\s+(.+)", line)
            if m:
                source = m.group(1).strip()
                target = m.group(2).strip()
                redirects[source] = target
    
    return redirects


def transform_redirect_target(space: str, target: str) -> str:
    """Transform a gitbook redirect target to a docs URL path."""
    # Remove .md extension and README
    t = target
    if t.endswith(".md"):
        t = t[:-3]
    t = re.sub(r"/README$", "", t)
    if t == "README":
        t = ""
    
    # Handle fragment
    fragment = ""
    if "#" in t:
        t, fragment = t.split("#", 1)
        fragment = "#" + fragment
    
    # Apply space prefix and structural remapping
    if space == "warp":
        # warp space content goes to top level (no prefix)
        url = "/" + t if t else "/"
    elif space == "agent-platform":
        # Handle warp-agents/ split
        if t.startswith("warp-agents/"):
            inner = t[len("warp-agents/"):]
            stem = inner.split("/")[0] if "/" in inner else inner
            if stem in CAPABILITIES_FILES:
                url = "/agent-platform/capabilities/" + inner
            elif stem in LOCAL_AGENTS_FILES:
                url = "/agent-platform/local-agents/" + inner
            elif inner.startswith("interacting-with-agents"):
                url = "/agent-platform/local-agents/" + inner
            elif inner.startswith("agent-context"):
                url = "/agent-platform/local-agents/" + inner
            elif inner == "" or inner == "README":
                url = "/agent-platform/local-agents/overview"
            else:
                url = "/agent-platform/capabilities/" + inner
        elif t.startswith("cli-agents/"):
            url = "/agent-platform/" + t
        else:
            url = "/agent-platform/" + t if t else "/agent-platform/"
    elif space == "guides":
        url = "/university/" + t if t else "/university/"
    else:
        url = "/" + space + "/" + t if t else "/" + space + "/"
    
    # Clean up
    url = url.rstrip("/") + "/"
    while "//" in url:
        url = url.replace("//", "/")
    
    return url + fragment


def generate_all_redirects(gitbook_root: Path) -> list:
    """Parse all .gitbook.yaml files and generate vercel.json redirect entries."""
    spaces = {
        "warp": gitbook_root / "docs" / "warp",
        "agent-platform": gitbook_root / "docs" / "agent-platform",
        "reference": gitbook_root / "docs" / "reference",
        "support-and-community": gitbook_root / "docs" / "support-and-community",
        "enterprise": gitbook_root / "docs" / "enterprise",
        "changelog": gitbook_root / "docs" / "changelog",
        "guides": gitbook_root / "guides",
    }
    
    all_redirects = []
    seen_sources = set()
    
    for space_name, space_dir in spaces.items():
        yaml_path = space_dir / ".gitbook.yaml"
        raw_redirects = parse_gitbook_yaml_redirects(yaml_path)
        
        for source, target in raw_redirects.items():
            # Build the full source URL (space prefix)
            if space_name == "warp":
                full_source = "/" + source
            elif space_name == "agent-platform":
                full_source = "/agent-platform/" + source
            elif space_name == "guides":
                full_source = "/university/" + source
            else:
                full_source = "/" + space_name + "/" + source
            
            # Clean up source
            full_source = full_source.rstrip("/")
            while "//" in full_source:
                full_source = full_source.replace("//", "/")
            
            # Transform target
            dest = transform_redirect_target(space_name, target)
            
            # Skip self-redirects
            if full_source.rstrip("/") == dest.rstrip("/"):
                continue
            
            if full_source not in seen_sources:
                seen_sources.add(full_source)
                all_redirects.append({
                    "source": full_source,
                    "destination": dest,
                    "statusCode": 308,
                })
    
    return sorted(all_redirects, key=lambda r: r["source"])


# ---------------------------------------------------------------------------
# Main migration
# ---------------------------------------------------------------------------


def migrate_space(
    gitbook_space_root: Path,
    docs_root: Path,
    space: str,
) -> tuple[int, int]:
    """Migrate all files from a gitbook space.
    
    Returns (converted_count, asset_count).
    """
    starlight_docs = docs_root / "src" / "content" / "docs"
    
    md_files = sorted(
        p for p in gitbook_space_root.rglob("*.md")
        if p.name != "SUMMARY.md" and "/_book/" not in str(p) and "/.gitbook/" not in str(p)
    )
    
    converted = 0
    for src_path in md_files:
        rel = str(src_path.relative_to(gitbook_space_root))
        dst_rel = map_gitbook_path(space, rel)
        dst_path = starlight_docs / dst_rel
        dst_path.parent.mkdir(parents=True, exist_ok=True)
        
        result = convert_file_enhanced(src_path, dst_path, space, gitbook_space_root, docs_root)
        dst_path.write_text(result, encoding="utf-8")
        converted += 1
        print(f"  ✓ {rel} → {dst_rel}")
    
    # Copy assets
    asset_dir_name = map_asset_space(space)
    asset_dir = docs_root / "src" / "assets" / asset_dir_name
    asset_count = copy_space_assets(gitbook_space_root, asset_dir)
    
    return converted, asset_count


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    gitbook_root = Path(sys.argv[1]).resolve()
    docs_root = Path(__file__).parent.parent.resolve()
    
    if not (gitbook_root / "docs").is_dir():
        print(f"Error: {gitbook_root}/docs is not a directory")
        sys.exit(1)
    
    spaces = [
        ("warp", gitbook_root / "docs" / "warp"),
        ("agent-platform", gitbook_root / "docs" / "agent-platform"),
        ("reference", gitbook_root / "docs" / "reference"),
        ("support-and-community", gitbook_root / "docs" / "support-and-community"),
        ("enterprise", gitbook_root / "docs" / "enterprise"),
        ("changelog", gitbook_root / "docs" / "changelog"),
        ("guides", gitbook_root / "guides"),
    ]
    
    # Also handle the top-level README.md
    top_readme = gitbook_root / "docs" / "README.md"
    
    total_converted = 0
    total_assets = 0
    
    for space_name, space_dir in spaces:
        if not space_dir.is_dir():
            print(f"\n⚠ Skipping {space_name} (not found: {space_dir})")
            continue
        print(f"\n{'='*60}")
        print(f"  Migrating: {space_name}")
        print(f"{'='*60}")
        converted, assets = migrate_space(space_dir, docs_root, space_name)
        total_converted += converted
        total_assets += assets
        print(f"  → {converted} files converted, {assets} assets copied")
    
    # Convert top-level README.md → index.mdx
    if top_readme.exists():
        print(f"\n  Converting top-level README.md → index.mdx")
        starlight_docs = docs_root / "src" / "content" / "docs"
        dst_path = starlight_docs / "index.mdx"
        result = convert_file_enhanced(
            top_readme, dst_path, "warp",
            gitbook_root / "docs", docs_root,
        )
        dst_path.write_text(result, encoding="utf-8")
        total_converted += 1
    
    # Generate redirects
    print(f"\n{'='*60}")
    print(f"  Generating redirects")
    print(f"{'='*60}")
    redirects = generate_all_redirects(gitbook_root)
    
    # Read existing vercel.json and merge
    vercel_json_path = docs_root / "vercel.json"
    if vercel_json_path.exists():
        existing = json.loads(vercel_json_path.read_text(encoding="utf-8"))
    else:
        existing = {}
    
    # Keep non-redirect config, replace redirects entirely
    existing["redirects"] = redirects
    vercel_json_path.write_text(
        json.dumps(existing, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"  → {len(redirects)} redirects written to vercel.json")
    
    print(f"\n{'='*60}")
    print(f"  MIGRATION COMPLETE")
    print(f"  Total files converted: {total_converted}")
    print(f"  Total assets copied: {total_assets}")
    print(f"  Total redirects: {len(redirects)}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
