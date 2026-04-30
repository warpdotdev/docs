#!/usr/bin/env python3
"""Merge seo/static-assets redirects on top of main's vercel.json.

Run this from the repo root after:
    git checkout seo/static-assets
    git merge --no-commit --no-ff origin/main
    git checkout --theirs vercel.json   # take main's vercel.json into worktree

This script then layers seo's net-new redirects on top, with three rules:

- Group A: drop. seo had 8 entries `/university/X[/]? -> /university/`. Those
  destinations no longer exist on main; main's catch-all
  `/university/(.*) -> /guides/$1` plus its 13 explicit directory entries
  supersede them.

- Group B: rewrite the destination. seo has 107 entries `/old-path ->
  /university/<file>` whose destinations are now gone. Build a map from main's
  67 explicit `/university/X -> /guides/<topic>/X` redirects and use it to
  rewrite the destination. 4 destinations have no explicit main mapping
  (newly-ported guides PR #56 added); supply hardcoded fallbacks.

- Group C: keep as-is. seo has 768 entries that don't touch /university/ on
  either side - the bulk of the SEO work (sitemap-only, GSC, trailing-slash
  variants, getting-started/features renames, agent-platform self-hosting
  renames, etc.).

The catch-all `/university/(.*) -> /guides/$1` is moved to the very end of
the resulting array so it can't shadow more specific rules.

Output: vercel.json is overwritten in place with 2-space indent and a
trailing newline, matching the existing file's formatting.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
VERCEL_JSON = REPO_ROOT / "vercel.json"

# 4 destinations on seo that do not have an explicit /university/X -> /guides/...
# mapping in main, because PR #56 ported these as brand-new guides rather than
# moving an existing university page. Hardcode the canonical /guides/ path.
HARDCODED_FALLBACKS: dict[str, str] = {
    "/university/developer-workflows/power-user/how-to-set-up-self-serve-data-analytics-with-skills": "/guides/configuration/how-to-set-up-self-serve-data-analytics-with-skills/",
    "/university/developer-workflows/power-user/how-to-set-up-self-serve-data-analytics-with-skills/": "/guides/configuration/how-to-set-up-self-serve-data-analytics-with-skills/",
    "/university/developer-workflows/warp-for-product-managers": "/guides/agent-workflows/warp-for-product-managers/",
    "/university/developer-workflows/warp-for-product-managers/": "/guides/agent-workflows/warp-for-product-managers/",
}

CATCHALL_SOURCE = "/university/(.*)"


def load_main_redirects() -> list[dict]:
    """vercel.json in the worktree is currently main's version (taken via --theirs)."""
    return json.loads(VERCEL_JSON.read_text())["redirects"]


def load_seo_redirects() -> list[dict]:
    """Pull seo/static-assets's vercel.json from git directly so we don't lose info."""
    raw = subprocess.check_output(
        ["git", "show", "seo/static-assets:vercel.json"], cwd=REPO_ROOT, text=True
    )
    return json.loads(raw)["redirects"]


def build_univ_to_guides_map(main_redirects: list[dict]) -> dict[str, str]:
    """Return a dict of /university/X (no trailing slash) -> /guides/<topic>/<file>/.

    Only includes entries where main maps an explicit /university/X to a /guides/
    destination. The catch-all and directory-fallback entries are excluded so that
    rewriting prefers a specific destination when one exists.
    """
    mapping: dict[str, str] = {}
    for r in main_redirects:
        s = r["source"].rstrip("/")
        d = r["destination"]
        if (
            s.startswith("/university/")
            and d.startswith("/guides/")
            and d != "/guides/"  # skip directory-fallback entries
            and "(.*)" not in s  # skip catch-all
        ):
            mapping[s] = d
    return mapping


def classify_and_rewrite_seo_only(
    seo_only: list[dict], univ_map: dict[str, str]
) -> tuple[list[dict], dict[str, int]]:
    """Walk seo_only entries; drop/rewrite/keep per the plan."""
    kept: list[dict] = []
    counters = {"group_a_dropped": 0, "group_b_rewritten": 0, "group_c_kept": 0,
                "rewrite_self_dropped": 0, "rewrite_unmapped_kept": 0}
    for r in seo_only:
        s, d = r["source"], r["destination"]
        if s.startswith("/university") and d.startswith("/university"):
            # Group A - drop, main supersedes.
            counters["group_a_dropped"] += 1
            continue
        if d.startswith("/university"):
            # Group B - rewrite destination.
            d_no_slash = d.rstrip("/")
            new_dest = univ_map.get(d_no_slash) or HARDCODED_FALLBACKS.get(d) or HARDCODED_FALLBACKS.get(d_no_slash)
            if new_dest is None:
                # Should not happen given audit, but fail loudly if it does
                print(f"WARN: no /university->/guides mapping for destination {d!r} (source {s!r}); dropping", file=sys.stderr)
                counters["rewrite_unmapped_kept"] += 1
                continue
            if s.rstrip("/") == new_dest.rstrip("/"):
                # Source and rewritten destination collapse - drop self-redirect.
                counters["rewrite_self_dropped"] += 1
                continue
            kept.append({**r, "destination": new_dest})
            counters["group_b_rewritten"] += 1
            continue
        # Group C - keep as-is.
        kept.append(r)
        counters["group_c_kept"] += 1
    return kept, counters


def merge() -> None:
    main_redirects = load_main_redirects()
    seo_redirects = load_seo_redirects()

    main_pairs = {(r["source"], r["destination"]) for r in main_redirects}
    seo_pairs = {(r["source"], r["destination"]) for r in seo_redirects}
    seo_only_pairs = seo_pairs - main_pairs

    # Preserve order from seo: walk seo_redirects, keep only the entries whose
    # (source, destination) pair is in seo_only_pairs.
    seen: set[tuple[str, str]] = set()
    seo_only: list[dict] = []
    for r in seo_redirects:
        key = (r["source"], r["destination"])
        if key in seo_only_pairs and key not in seen:
            seo_only.append(r)
            seen.add(key)

    print(f"main entries:       {len(main_redirects)}")
    print(f"seo entries:        {len(seo_redirects)}")
    print(f"seo-only entries:   {len(seo_only)}")

    univ_map = build_univ_to_guides_map(main_redirects)
    print(f"main /univ->/guides explicit mappings: {len(univ_map)}")

    seo_kept, counters = classify_and_rewrite_seo_only(seo_only, univ_map)
    print(f"\nGroup A dropped (seo /university/* -> /university/*):       {counters['group_a_dropped']}")
    print(f"Group B rewritten (seo /old -> /university/X => /guides/Y):  {counters['group_b_rewritten']}")
    print(f"Group C kept (seo non-university entries):                   {counters['group_c_kept']}")
    print(f"Rewrites collapsed to self-redirect (dropped):               {counters['rewrite_self_dropped']}")
    if counters["rewrite_unmapped_kept"]:
        print(f"WARN: rewrites with no mapping (dropped):                   {counters['rewrite_unmapped_kept']}")

    # Pull main's catch-all aside; we want it to stay at the very end after appending seo entries.
    main_no_catchall: list[dict] = []
    catchall: dict | None = None
    for r in main_redirects:
        if r["source"] == CATCHALL_SOURCE:
            catchall = r
        else:
            main_no_catchall.append(r)
    if catchall is None:
        raise RuntimeError(f"Expected catch-all {CATCHALL_SOURCE!r} in main redirects; not found")

    # Final order: main's explicit redirects (in main's order), then seo additions
    # (in seo's order, deduped against main and against itself), then the catch-all.
    final: list[dict] = list(main_no_catchall)
    final_pairs: set[tuple[str, str]] = {(r["source"], r["destination"]) for r in final}
    for r in seo_kept:
        key = (r["source"], r["destination"])
        if key in final_pairs:
            continue
        final.append(r)
        final_pairs.add(key)
    # Catch-all goes last so it can't shadow more specific rules.
    final.append(catchall)

    print(f"\nfinal redirect count: {len(final)}")

    # Preserve formatting: load full top-level dict, replace redirects, write with 2-space indent + trailing newline.
    full = json.loads(VERCEL_JSON.read_text())
    full["redirects"] = final
    VERCEL_JSON.write_text(json.dumps(full, indent=2) + "\n")
    print(f"wrote {VERCEL_JSON}")


if __name__ == "__main__":
    merge()
