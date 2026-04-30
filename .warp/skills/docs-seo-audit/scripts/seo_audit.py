#!/usr/bin/env python3
"""
SEO audit for docs.warp.dev

Crawls the Astro Starlight sitemap index, fetches every page, and checks for common
SEO issues:
  - Duplicate title tags
  - Duplicate meta descriptions
  - Missing or empty title / description
  - Title length outside 20-70 char range
  - Description length outside 50-160 char range
  - Missing or multiple H1 tags
  - OG / Twitter meta mismatches

Outputs a JSON report to stdout (or --output FILE).
"""

import argparse
import json
import os
import sys
import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from html.parser import HTMLParser
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from xml.etree import ElementTree as ET

SITEMAP_INDEX_URL = "https://docs.warp.dev/sitemap.xml"
NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
USER_AGENT = "WarpSEOAudit/1.0"
REQUEST_DELAY = 0.15  # seconds between requests to avoid rate-limiting
MAX_WORKERS = 6

# ---------------------------------------------------------------------------
# Astro Starlight space → local directory mapping
# ---------------------------------------------------------------------------
# Astro Starlight publishes each space at a URL prefix. The "warp" space is the site
# root (no prefix). All others use their directory name as prefix.
SPACE_MAP = {
    "agent-platform": "docs/agent-platform",
    "reference": "docs/reference",
    "changelog": "docs/changelog",
    "support-and-community": "docs/support-and-community",
    "enterprise": "docs/enterprise",
    "university": "university",
}
# The warp space lives at the site root, so pages like /terminal/blocks map
# to src/content/docs/terminal/blocks.
ROOT_SPACE_DIR = "docs/warp"

# ---------------------------------------------------------------------------
# HTML parser
# ---------------------------------------------------------------------------

class SEOHTMLParser(HTMLParser):
    """Lightweight parser that extracts SEO-relevant tags from an HTML page."""

    def __init__(self):
        super().__init__()
        self.title = None
        self.meta_description = None
        self.og_title = None
        self.og_description = None
        self.twitter_title = None
        self.twitter_description = None
        self.canonical = None
        self.h1s = []
        self._in_head = False
        self._in_title = False
        self._title_parts = []
        self._in_h1 = False
        self._h1_parts = []
        self._h1_depth = 0

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        tag_lower = tag.lower()

        if tag_lower == "head":
            self._in_head = True
        elif tag_lower == "title" and self._in_head:
            self._in_title = True
            self._title_parts = []
        elif tag_lower == "meta" and self._in_head:
            name = attrs_dict.get("name", "").lower()
            prop = attrs_dict.get("property", "").lower()
            content = attrs_dict.get("content", "")
            if name == "description":
                self.meta_description = content
            elif prop == "og:title":
                self.og_title = content
            elif prop == "og:description":
                self.og_description = content
            elif name == "twitter:title" or prop == "twitter:title":
                self.twitter_title = content
            elif name == "twitter:description" or prop == "twitter:description":
                self.twitter_description = content
        elif tag_lower == "link" and self._in_head:
            if attrs_dict.get("rel", "").lower() == "canonical":
                self.canonical = attrs_dict.get("href")
        elif tag_lower == "h1":
            self._in_h1 = True
            self._h1_depth = 1
            self._h1_parts = []

    def handle_endtag(self, tag):
        tag_lower = tag.lower()
        if tag_lower == "head":
            self._in_head = False
        elif tag_lower == "title" and self._in_title:
            self._in_title = False
            self.title = "".join(self._title_parts).strip()
        elif tag_lower == "h1" and self._in_h1:
            self._h1_depth -= 1
            if self._h1_depth <= 0:
                self._in_h1 = False
                text = "".join(self._h1_parts).strip()
                if text:
                    self.h1s.append(text)

    def handle_data(self, data):
        if self._in_title:
            self._title_parts.append(data)
        if self._in_h1:
            self._h1_parts.append(data)


# ---------------------------------------------------------------------------
# Fetching helpers
# ---------------------------------------------------------------------------

def fetch(url, retries=2):
    """Fetch a URL and return its body as a string."""
    req = Request(url, headers={"User-Agent": USER_AGENT})
    for attempt in range(retries + 1):
        try:
            with urlopen(req, timeout=15) as resp:
                return resp.read().decode("utf-8", errors="replace")
        except (HTTPError, URLError, OSError) as exc:
            if attempt == retries:
                raise
            time.sleep(1)


def fetch_sitemap_urls(sitemap_index_url):
    """Return a list of all page URLs across all sub-sitemaps."""
    body = fetch(sitemap_index_url)
    root = ET.fromstring(body)
    sub_urls = [loc.text for loc in root.findall(".//sm:sitemap/sm:loc", NS)]

    page_urls = []
    for sub_url in sub_urls:
        try:
            sub_body = fetch(sub_url)
            sub_root = ET.fromstring(sub_body)
            for loc in sub_root.findall(".//sm:url/sm:loc", NS):
                if loc.text:
                    page_urls.append(loc.text.strip())
        except Exception as exc:
            print(f"Warning: could not fetch sub-sitemap {sub_url}: {exc}", file=sys.stderr)
    return page_urls


def extract_seo(url):
    """Fetch a page and return its SEO metadata dict."""
    try:
        html = fetch(url)
    except Exception as exc:
        return {"url": url, "error": str(exc)}

    parser = SEOHTMLParser()
    try:
        parser.feed(html)
    except Exception:
        pass

    return {
        "url": url,
        "title": parser.title,
        "meta_description": parser.meta_description,
        "og_title": parser.og_title,
        "og_description": parser.og_description,
        "twitter_title": parser.twitter_title,
        "twitter_description": parser.twitter_description,
        "canonical": parser.canonical,
        "h1s": parser.h1s,
    }


# ---------------------------------------------------------------------------
# URL → source file mapping
# ---------------------------------------------------------------------------

def url_to_source_path(url, repo_root):
    """Best-effort mapping from a live URL to the local markdown source file.

    Returns the relative path from repo_root, or None if no file is found.
    """
    from urllib.parse import urlparse
    parsed = urlparse(url)
    path = parsed.path.strip("/")  # e.g. "agent-platform/local-agents/overview"

    # Determine which space this URL belongs to
    local_dir = None
    remainder = path
    for prefix, directory in SPACE_MAP.items():
        if path == prefix or path.startswith(prefix + "/"):
            local_dir = directory
            remainder = path[len(prefix):].strip("/")
            break
    if local_dir is None:
        # Root space (warp)
        local_dir = ROOT_SPACE_DIR
        remainder = path

    if not remainder:
        # Space landing page → README.md
        candidate = os.path.join(repo_root, local_dir, "README.md")
        return os.path.relpath(candidate, repo_root) if os.path.isfile(candidate) else None

    # Try direct file match: remainder.md
    candidate = os.path.join(repo_root, local_dir, remainder + ".md")
    if os.path.isfile(candidate):
        return os.path.relpath(candidate, repo_root)

    # Try directory landing page: remainder/README.md
    candidate = os.path.join(repo_root, local_dir, remainder, "README.md")
    if os.path.isfile(candidate):
        return os.path.relpath(candidate, repo_root)

    return None


# ---------------------------------------------------------------------------
# Analysis
# ---------------------------------------------------------------------------

# Title tag length limits (Google typically truncates at ~60 chars).
# The "page title" portion is what we control; the " | Space | Warp" suffix
# is appended by Astro Starlight.  We check the full rendered title.
TITLE_MIN = 20
TITLE_MAX = 70
DESC_MIN = 50
DESC_MAX = 160


def analyse(pages, repo_root=None):
    """Run SEO checks and return a structured report."""
    issues = []

    # Group by title and description for duplicate detection
    titles = defaultdict(list)
    descriptions = defaultdict(list)

    for p in pages:
        if "error" in p:
            issues.append({
                "url": p["url"],
                "severity": "error",
                "type": "fetch_error",
                "message": f"Could not fetch page: {p['error']}",
            })
            continue

        url = p["url"]
        title = p.get("title") or ""
        desc = p.get("meta_description") or ""
        h1s = p.get("h1s", [])

        source_file = url_to_source_path(url, repo_root) if repo_root else None

        base = {"url": url}
        if source_file:
            base["source_file"] = source_file

        # --- Title checks ---
        if not title:
            issues.append({**base, "severity": "error", "type": "missing_title",
                           "message": "Page has no <title> tag"})
        else:
            titles[title].append(url)
            tlen = len(title)
            if tlen < TITLE_MIN:
                issues.append({**base, "severity": "warning", "type": "title_too_short",
                               "message": f"Title is only {tlen} chars (min {TITLE_MIN}): \"{title}\""})
            elif tlen > TITLE_MAX:
                issues.append({**base, "severity": "warning", "type": "title_too_long",
                               "message": f"Title is {tlen} chars (max {TITLE_MAX}): \"{title}\""})

        # --- Description checks ---
        if not desc:
            issues.append({**base, "severity": "warning", "type": "missing_description",
                           "message": "Page has no meta description"})
        else:
            descriptions[desc].append(url)
            dlen = len(desc)
            if dlen < DESC_MIN:
                issues.append({**base, "severity": "info", "type": "description_too_short",
                               "message": f"Description is only {dlen} chars (min {DESC_MIN}): \"{desc[:80]}...\""})
            elif dlen > DESC_MAX:
                issues.append({**base, "severity": "info", "type": "description_too_long",
                               "message": f"Description is {dlen} chars (max {DESC_MAX}): \"{desc[:80]}...\""})

        # --- H1 checks ---
        if len(h1s) == 0:
            issues.append({**base, "severity": "warning", "type": "missing_h1",
                           "message": "Page has no H1 heading"})
        elif len(h1s) > 1:
            issues.append({**base, "severity": "warning", "type": "multiple_h1",
                           "message": f"Page has {len(h1s)} H1 headings: {h1s}"})

        # --- OG / Twitter consistency ---
        og_title = p.get("og_title") or ""
        if title and og_title and title != og_title:
            issues.append({**base, "severity": "info", "type": "og_title_mismatch",
                           "message": f"OG title differs from <title>: \"{og_title}\" vs \"{title}\""})

        og_desc = p.get("og_description") or ""
        if desc and og_desc and desc != og_desc:
            issues.append({**base, "severity": "info", "type": "og_description_mismatch",
                           "message": f"OG description differs from meta description"})

    # --- Duplicate detection ---
    for title, urls in titles.items():
        if len(urls) > 1:
            for u in urls:
                source_file = url_to_source_path(u, repo_root) if repo_root else None
                entry = {"url": u, "severity": "error", "type": "duplicate_title",
                         "message": f"Duplicate title ({len(urls)} pages): \"{title}\"",
                         "duplicate_urls": urls}
                if source_file:
                    entry["source_file"] = source_file
                issues.append(entry)

    for desc, urls in descriptions.items():
        if len(urls) > 1:
            for u in urls:
                source_file = url_to_source_path(u, repo_root) if repo_root else None
                entry = {"url": u, "severity": "warning", "type": "duplicate_description",
                         "message": f"Duplicate description ({len(urls)} pages): \"{desc[:80]}...\"",
                         "duplicate_urls": urls}
                if source_file:
                    entry["source_file"] = source_file
                issues.append(entry)

    # --- Summary ---
    severity_counts = defaultdict(int)
    type_counts = defaultdict(int)
    for i in issues:
        severity_counts[i["severity"]] += 1
        type_counts[i["type"]] += 1

    return {
        "total_pages": len(pages),
        "total_issues": len(issues),
        "by_severity": dict(severity_counts),
        "by_type": dict(type_counts),
        "issues": sorted(issues, key=lambda x: ("error", "warning", "info").index(x["severity"])),
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="SEO audit for docs.warp.dev")
    parser.add_argument("--sitemap", default=SITEMAP_INDEX_URL,
                        help="Sitemap index URL (default: %(default)s)")
    parser.add_argument("--repo-root", default=None,
                        help="Path to the docs repo root for source-file mapping")
    parser.add_argument("--output", "-o", default=None,
                        help="Write JSON report to this file instead of stdout")
    parser.add_argument("--max-pages", type=int, default=0,
                        help="Limit to N pages (0 = all, useful for testing)")
    parser.add_argument("--workers", type=int, default=MAX_WORKERS,
                        help=f"Concurrent fetch workers (default: {MAX_WORKERS})")
    args = parser.parse_args()

    print(f"Fetching sitemap index: {args.sitemap}", file=sys.stderr)
    urls = fetch_sitemap_urls(args.sitemap)
    print(f"Found {len(urls)} pages across all sitemaps", file=sys.stderr)

    if args.max_pages > 0:
        urls = urls[:args.max_pages]
        print(f"Limiting to first {args.max_pages} pages", file=sys.stderr)

    pages = []
    errors = 0

    print(f"Fetching pages with {args.workers} workers...", file=sys.stderr)
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        future_to_url = {}
        for i, url in enumerate(urls):
            future = pool.submit(extract_seo, url)
            future_to_url[future] = url
            # Stagger submissions slightly to avoid burst
            if i % args.workers == 0 and i > 0:
                time.sleep(REQUEST_DELAY)

        for i, future in enumerate(as_completed(future_to_url)):
            result = future.result()
            pages.append(result)
            if "error" in result:
                errors += 1
            if (i + 1) % 25 == 0 or i + 1 == len(urls):
                print(f"  Progress: {i + 1}/{len(urls)} pages fetched ({errors} errors)",
                      file=sys.stderr)

    report = analyse(pages, repo_root=args.repo_root)

    output_json = json.dumps(report, indent=2)
    if args.output:
        with open(args.output, "w") as f:
            f.write(output_json)
        print(f"\nReport written to {args.output}", file=sys.stderr)
    else:
        print(output_json)

    # Print summary to stderr
    print(f"\n=== SEO AUDIT SUMMARY ===", file=sys.stderr)
    print(f"Pages scanned: {report['total_pages']}", file=sys.stderr)
    print(f"Total issues:  {report['total_issues']}", file=sys.stderr)
    for sev in ("error", "warning", "info"):
        count = report["by_severity"].get(sev, 0)
        if count:
            print(f"  {sev}: {count}", file=sys.stderr)
    print(f"\nIssue breakdown:", file=sys.stderr)
    for issue_type, count in sorted(report["by_type"].items(), key=lambda x: -x[1]):
        print(f"  {issue_type}: {count}", file=sys.stderr)


if __name__ == "__main__":
    main()
