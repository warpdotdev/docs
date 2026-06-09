#!/usr/bin/env python3
"""
Audit redirect coverage: extract every URL path that was ever live on the
old GitBook docs and identify which ones are NOT covered by a redirect in
vercel.json (i.e., would return a 404 on the new Astro/Starlight site).

Usage:
    python3 scripts/audit_redirects.py [--gitbook-root PATH]

Output:
    Prints uncovered paths to stdout and writes them to
    scripts/redirect_audit_gaps.txt.
"""

import re
import json
import argparse
from pathlib import Path

# ---------------------------------------------------------------------------
# GitBook space → URL prefix mapping.
# Each key is relative to the gitbook repo root; value is the URL prefix
# (empty string = served at root, no prefix).
# ---------------------------------------------------------------------------
SPACES = {
    "docs/warp":                 "",                  # served at /
    "docs/agent-platform":       "agent-platform",
    "docs/reference":            "reference",
    "docs/support-and-community":"support-and-community",
    "docs/enterprise":           "enterprise",
    "docs/changelog":            "changelog",
    "guides":                    "guides",            # Warp University
}


def extract_paths_from_summary(summary_path: Path) -> list[str]:
    """Extract all .md file paths referenced in a SUMMARY.md."""
    paths = []
    pattern = re.compile(r'\]\(([^)#"]+\.md)[^)]*\)')
    with open(summary_path, encoding="utf-8") as f:
        for line in f:
            for match in pattern.finditer(line):
                raw = match.group(1).strip()
                # Skip external URLs
                if raw.startswith("http"):
                    continue
                paths.append(raw)
    return paths


def md_path_to_url(md_path: str, prefix: str) -> str:
    """Convert a markdown file path to its URL on docs.warp.dev."""
    # Remove .md extension
    url = md_path.removesuffix(".md")

    # README.md at root of space = index page
    if url == "README":
        url = ""
    # README.md in a subdirectory = that directory's index
    elif url.endswith("/README"):
        url = url.removesuffix("/README")

    # Apply space prefix
    if prefix:
        if url:
            url = f"{prefix}/{url}"
        else:
            url = prefix
    
    # Normalise: lowercase, remove trailing slash
    url = url.lower().rstrip("/")
    return url


def load_vercel_redirect_sources(vercel_json_path: Path) -> set[str]:
    """Load all redirect source paths from vercel.json."""
    with open(vercel_json_path, encoding="utf-8") as f:
        data = json.load(f)
    sources = set()
    for r in data.get("redirects", []):
        src = r.get("source", "").lower().rstrip("/")
        # Remove anchor fragments if present
        src = src.split("#")[0].rstrip("/")
        sources.add(src)
    return sources


def load_live_astro_paths(docs_src: Path) -> set[str]:
    """Collect all URL paths that exist as pages in the Astro site."""
    live = set()
    content_root = docs_src / "content" / "docs"
    for mdx_file in content_root.rglob("*.mdx"):
        relative = mdx_file.relative_to(content_root)
        # index.mdx → the directory path; foo.mdx → foo
        parts = list(relative.parts)
        if parts[-1] in ("index.mdx",):
            parts = parts[:-1]
        else:
            parts[-1] = parts[-1].removesuffix(".mdx")
        url = "/".join(parts).lower().rstrip("/")
        live.add(url)
    # Add the site root
    live.add("")
    live.add("quickstart")
    return live


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--gitbook-root",
        default=str(Path(__file__).parent.parent.parent / "gitbook"),
        help="Path to the old GitBook repo root (default: ../gitbook relative to docs/)",
    )
    args = parser.parse_args()

    gitbook_root = Path(args.gitbook_root)
    docs_root = Path(__file__).parent.parent  # the Astro docs repo
    vercel_json_path = docs_root / "vercel.json"

    print(f"GitBook root: {gitbook_root}")
    print(f"Docs (Astro) root: {docs_root}")
    print()

    # 1. Extract all old GitBook URL paths
    all_gitbook_urls: set[str] = set()
    for space_rel, prefix in SPACES.items():
        summary_path = gitbook_root / space_rel / "SUMMARY.md"
        if not summary_path.exists():
            print(f"  [SKIP] {summary_path} not found")
            continue
        md_paths = extract_paths_from_summary(summary_path)
        for mp in md_paths:
            url = md_path_to_url(mp, prefix)
            all_gitbook_urls.add(url)
        print(f"  {space_rel}: {len(md_paths)} paths extracted")

    print(f"\nTotal unique GitBook paths: {len(all_gitbook_urls)}")

    # 2. Load existing vercel.json redirect sources
    redirect_sources = load_vercel_redirect_sources(vercel_json_path)
    print(f"Existing vercel.json redirect sources: {len(redirect_sources)}")

    # 3. Load live Astro pages
    live_astro = load_live_astro_paths(docs_root / "src")
    print(f"Live Astro pages: {len(live_astro)}")

    # 4. Find gaps: paths that are neither live in Astro nor covered by a redirect
    gaps = sorted(
        url for url in all_gitbook_urls
        if url not in live_astro
        and f"/{url}" not in redirect_sources
        and url not in redirect_sources
    )

    print(f"\n{'='*60}")
    print(f"UNCOVERED PATHS (not live in Astro + no redirect): {len(gaps)}")
    print(f"{'='*60}\n")

    for gap in gaps:
        print(f"  /{gap}")

    # 5. Write to file for further processing
    output_path = docs_root / "scripts" / "redirect_audit_gaps.txt"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"# Redirect audit gaps — {len(gaps)} uncovered GitBook paths\n")
        f.write("# These were live on GitBook but have no redirect or live page in the Astro site.\n")
        f.write("# Format: /old-path\n\n")
        for gap in gaps:
            f.write(f"/{gap}\n")

    print(f"\nWrote {len(gaps)} gaps to: {output_path}")


if __name__ == "__main__":
    main()
