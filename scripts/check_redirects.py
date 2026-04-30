#!/usr/bin/env python3
"""Validate vercel.json redirects.

Static mode (default): for each redirect, check that the `destination`
resolves to a page that actually exists in `src/content/docs/`. External
URLs and special endpoints (`/api`, `/api#...`) are skipped.

Live mode (--live URL): actually hit each `source` against a deployed
preview/production URL and verify it returns the expected status code
with a `location` header pointing at the configured destination.

Usage:

    # Static check (fast, no network)
    python3 scripts/check_redirects.py

    # Live check against a Vercel preview deployment
    python3 scripts/check_redirects.py --live https://docs-git-<branch>.vercel.app

    # Live check, sample only 50 redirects (useful for spot-checks)
    python3 scripts/check_redirects.py --live <URL> --sample 50

    # Static check + live check together
    python3 scripts/check_redirects.py --live <URL>

Exit code is 0 if all checks pass, 1 if any redirect is broken.
"""
from __future__ import annotations

import argparse
import json
import random
import re
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import urlparse

REPO = Path(__file__).resolve().parent.parent
DOCS = REPO / "src" / "content" / "docs"
VERCEL_JSON = REPO / "vercel.json"

# Destinations starting with these prefixes are not Astro Starlight pages and
# should not be checked for file existence.
SKIP_DEST_PREFIXES = (
    "http://",
    "https://",
    "/api",  # OpenAPI reference, served by starlight-openapi
    "/_astro/",
    "/assets/",
)

# Destination paths ending in these extensions are generated assets
# (RSS feeds, sitemaps, etc.), not Starlight content pages.
SKIP_DEST_EXTENSIONS = (
    ".xml",
    ".json",
    ".txt",
    ".png",
    ".jpg",
    ".gif",
    ".svg",
    ".ico",
)


def load_redirects() -> list[dict]:
    with VERCEL_JSON.open() as f:
        data = json.load(f)
    return data.get("redirects", [])


def url_to_content_path(url_path: str) -> Path | None:
    """Map a URL like '/foo/bar/' to a content file path.

    Returns the file Path if it exists, or None if no file matches.
    Tries both `foo/bar.mdx` and `foo/bar/index.mdx` conventions.
    """
    # Strip leading slash, trailing slash, and any anchor/query.
    path = url_path.split("#", 1)[0].split("?", 1)[0]
    path = path.strip("/")
    if not path:
        return DOCS / "index.mdx" if (DOCS / "index.mdx").exists() else None

    candidates = [
        DOCS / f"{path}.mdx",
        DOCS / f"{path}.md",
        DOCS / path / "index.mdx",
        DOCS / path / "index.md",
    ]
    for c in candidates:
        if c.exists():
            return c
    return None


def static_check(redirects: list[dict]) -> tuple[int, int, list[str]]:
    """Verify each destination resolves to a real page.

    Returns (checked, broken, errors).
    """
    checked = 0
    broken = 0
    errors: list[str] = []

    for r in redirects:
        source = r.get("source", "")
        dest = r.get("destination", "")
        if not source or not dest:
            errors.append(f"Missing source/destination: {r!r}")
            broken += 1
            continue

        # Skip wildcard sources/destinations — we can't fully verify these
        # statically since the captured group is dynamic.
        if "(" in source or "$" in dest:
            continue

        # Skip external URLs and special endpoints.
        if dest.startswith(SKIP_DEST_PREFIXES):
            continue

        # Skip generated assets (RSS feeds, sitemaps, etc.).
        dest_path = dest.split("#", 1)[0].split("?", 1)[0]
        if dest_path.endswith(SKIP_DEST_EXTENSIONS):
            continue

        checked += 1
        path = url_to_content_path(dest)
        if path is None:
            errors.append(f"Destination not found: {source!r} -> {dest!r}")
            broken += 1

    return checked, broken, errors


def live_check_one(base_url: str, redirect: dict, timeout: float = 10.0) -> tuple[bool, str]:
    """Hit one source URL and verify the redirect.

    Returns (ok, message). ok=True if the redirect matches, False otherwise.
    """
    import urllib.request
    import urllib.error

    source = redirect["source"]
    expected_dest = redirect["destination"]
    expected_status = redirect.get("statusCode", 308)

    # Skip wildcard redirects in live mode — we'd need to substitute $1 etc.
    if "(" in source or "$" in expected_dest:
        return True, f"SKIP (wildcard): {source}"

    url = base_url.rstrip("/") + source
    req = urllib.request.Request(url, method="HEAD")
    try:
        # Don't follow redirects — we want to inspect the response headers.
        opener = urllib.request.build_opener(NoRedirect())
        with opener.open(req, timeout=timeout) as resp:
            status = resp.status
            location = resp.headers.get("location", "")
    except urllib.error.HTTPError as e:
        status = e.code
        location = e.headers.get("location", "") if e.headers else ""
    except Exception as e:  # noqa: BLE001
        return False, f"ERROR {source}: {e}"

    if status != expected_status:
        return False, f"FAIL {source}: status {status} != {expected_status}"
    # Location may be relative (just the path) or absolute. Compare paths.
    actual_path = urlparse(location).path or location
    if actual_path != expected_dest:
        return False, (
            f"FAIL {source}: location {actual_path!r} != {expected_dest!r}"
        )
    return True, f"OK {source} -> {expected_dest}"


class NoRedirect(__import__("urllib.request").request.HTTPRedirectHandler):
    """An HTTP handler that does NOT follow redirects."""

    def http_error_301(self, req, fp, code, msg, headers):  # noqa: D102
        raise __import__("urllib.error").error.HTTPError(req.full_url, code, msg, headers, fp)

    http_error_302 = http_error_301
    http_error_303 = http_error_301
    http_error_307 = http_error_301
    http_error_308 = http_error_301


def live_check(base_url: str, redirects: list[dict], sample: int = 0, workers: int = 16) -> tuple[int, int, list[str]]:
    """Hit redirects against a live URL. Returns (checked, broken, errors)."""
    if sample and sample < len(redirects):
        redirects = random.sample(redirects, sample)

    checked = 0
    broken = 0
    errors: list[str] = []

    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(live_check_one, base_url, r): r for r in redirects}
        for i, fut in enumerate(as_completed(futures), 1):
            ok, msg = fut.result()
            if msg.startswith("SKIP"):
                continue
            checked += 1
            if not ok:
                broken += 1
                errors.append(msg)
            if i % 50 == 0:
                print(f"  ... {i}/{len(futures)} ({broken} broken so far)", file=sys.stderr)

    return checked, broken, errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--live", metavar="URL", help="Base URL of a deployed site (e.g. Vercel preview) to hit for live checks")
    parser.add_argument("--sample", type=int, default=0, help="Live mode only: check a random sample of N redirects instead of all")
    parser.add_argument("--workers", type=int, default=16, help="Live mode only: concurrent HTTP workers (default 16)")
    parser.add_argument("--skip-static", action="store_true", help="Skip the static check (only meaningful with --live)")
    args = parser.parse_args()

    redirects = load_redirects()
    print(f"Loaded {len(redirects)} redirects from {VERCEL_JSON.relative_to(REPO)}")

    total_broken = 0

    # Static check
    if not args.skip_static:
        print("\n=== Static check (destination existence) ===")
        checked, broken, errors = static_check(redirects)
        print(f"Checked: {checked}, broken: {broken}")
        for err in errors:
            print(f"  {err}")
        total_broken += broken

    # Live check
    if args.live:
        print(f"\n=== Live check against {args.live} ===")
        if args.sample:
            print(f"Sampling {args.sample} of {len(redirects)} redirects")
        checked, broken, errors = live_check(args.live, redirects, sample=args.sample, workers=args.workers)
        print(f"Checked: {checked}, broken: {broken}")
        for err in errors:
            print(f"  {err}")
        total_broken += broken

    print(f"\n{'PASS' if total_broken == 0 else 'FAIL'}: {total_broken} broken")
    return 0 if total_broken == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
