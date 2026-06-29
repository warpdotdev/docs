#!/usr/bin/env python3
"""
Weekly 404 monitor — data collection script.

Queries the docs_404 Rudderstack track event from stg_website_events via
the Metabase API, diffs against vercel.json redirect sources, and writes:
  - JSON report to stdout (for the agent to parse)
  - CSV artifact to data/404-reports/YYYY-MM-DD.csv

Usage (called by the weekly-404-monitor skill):
    python3 .agents/skills/weekly-404-monitor/run_404_report.py

Required env vars:
    METABASE_API_KEY  — Metabase API key

Optional env vars:
    VERCEL_JSON_PATH  — Path to vercel.json (default: ./vercel.json)
    REPORT_DIR        — Output directory for CSV artifacts (default: ./data/404-reports)
"""

import csv
import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import date, timedelta
from pathlib import Path


BASE = "https://warp.metabaseapp.com/api"
DB_ID = 2  # BigQuery prod


def metabase_headers():
    key = os.environ.get("METABASE_API_KEY")
    if not key:
        print("ERROR: METABASE_API_KEY is not set.", file=sys.stderr)
        sys.exit(1)
    return {"X-API-Key": key, "Content-Type": "application/json"}


def run_query(sql: str) -> list[dict]:
    """Execute a BigQuery SQL query via the Metabase /dataset endpoint."""
    headers = metabase_headers()
    body = json.dumps({
        "database": DB_ID,
        "type": "native",
        "native": {"query": sql},
    }).encode()
    req = urllib.request.Request(f"{BASE}/dataset", data=body, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        print(f"ERROR: Metabase query failed: HTTP {e.code}: {e.read().decode()[:500]}",
              file=sys.stderr)
        sys.exit(1)

    if result.get("error"):
        print(f"ERROR: Metabase query error: {result['error']}", file=sys.stderr)
        sys.exit(1)

    data = result.get("data", {})
    cols = [c["name"] for c in data.get("cols", [])]
    rows = data.get("rows", [])
    return [dict(zip(cols, row)) for row in rows]


def query_404_events(days_start: int, days_end: int) -> list[dict]:
    """
    Return broken_url counts for the window [days_start, days_end) days ago.
    days_start=1, days_end=8  → past 7 days (current week)
    days_start=8, days_end=15 → 8-14 days ago (prior week)
    """
    sql = f"""
SELECT
  REGEXP_REPLACE(
    SPLIT(JSON_VALUE(event_properties, '$.broken_url'), '?')[OFFSET(0)],
    r'#.*$', ''
  ) AS broken_url,
  COUNT(*) AS hits
FROM `warp-data-357114.prod.stg_website_events`
WHERE event_type = 'track'
  AND event_name = 'docs_404'
  AND JSON_VALUE(event_properties, '$.broken_url') IS NOT NULL
  AND event_date >= DATE_SUB(CURRENT_DATE(), INTERVAL {days_end - 1} DAY)
  AND event_date < DATE_SUB(CURRENT_DATE(), INTERVAL {days_start - 1} DAY)
GROUP BY 1
HAVING broken_url IS NOT NULL AND broken_url != ''
ORDER BY 2 DESC
LIMIT 500
"""
    return run_query(sql)


def total_404_count(days_start: int, days_end: int) -> int:
    sql = f"""
SELECT COUNT(*) AS total
FROM `warp-data-357114.prod.stg_website_events`
WHERE event_type = 'track'
  AND event_name = 'docs_404'
  AND event_date >= DATE_SUB(CURRENT_DATE(), INTERVAL {days_end - 1} DAY)
  AND event_date < DATE_SUB(CURRENT_DATE(), INTERVAL {days_start - 1} DAY)
"""
    rows = run_query(sql)
    return int(rows[0]["total"]) if rows else 0


def load_redirect_sources(vercel_json_path: Path) -> set[str]:
    """Load all redirect source paths from vercel.json, normalised."""
    if not vercel_json_path.exists():
        # Try fetching from GitHub
        url = "https://raw.githubusercontent.com/warpdotdev/docs/main/vercel.json"
        try:
            with urllib.request.urlopen(url, timeout=10) as resp:
                data = json.loads(resp.read())
        except Exception as e:
            print(f"ERROR: Could not load vercel.json from disk or GitHub: {e}",
                  file=sys.stderr)
            sys.exit(1)
    else:
        with open(vercel_json_path) as f:
            data = json.load(f)

    redirects = data.get("redirects", [])
    if len(redirects) < 500:
        print(f"WARNING: vercel.json has only {len(redirects)} redirects — "
              "sanity check failed (expected 500+). Data may be incomplete.",
              file=sys.stderr)

    sources = set()
    for r in redirects:
        src = r.get("source", "").lower().rstrip("/").split("#")[0].split("?")[0]
        sources.add(src)
    return sources


def normalise_url(url: str) -> str:
    """Normalise a broken URL for comparison against vercel.json sources."""
    if not url:
        return ""
    # Extract just the path (no scheme/host)
    url = re.sub(r"^https?://[^/]+", "", url)
    # Strip query params and fragments
    url = url.split("?")[0].split("#")[0]
    # Lowercase, strip trailing slash
    url = url.lower().rstrip("/")
    return url or "/"


def main():
    vercel_path = Path(os.environ.get("VERCEL_JSON_PATH", "vercel.json"))
    report_dir = Path(os.environ.get("REPORT_DIR", "data/404-reports"))
    # Minimum weekly hits for an uncovered URL to count as a "gap worth fixing"
    # in the Slack headline. Anything below this is long-tail noise (one-off
    # bot/crawler/old-bookmark traffic) and is rolled up into a single count so
    # it doesn't dominate the report. Tunable via env; see SKILL.md.
    report_min_hits = int(os.environ.get("REPORT_MIN_HITS", "5"))
    today = date.today()

    print(f"Running weekly 404 report for week ending {today}", file=sys.stderr)

    # 1. Query current and prior week
    print("Querying current week (past 7 days)...", file=sys.stderr)
    current_week = query_404_events(1, 8)
    print(f"  {len(current_week)} unique broken URLs found", file=sys.stderr)

    print("Querying prior week (days 8-14)...", file=sys.stderr)
    prior_week = query_404_events(8, 15)

    total_current = total_404_count(1, 8)
    total_prior = total_404_count(8, 15)

    # 2. Load redirect sources
    print("Loading vercel.json redirect sources...", file=sys.stderr)
    redirect_sources = load_redirect_sources(vercel_path)

    # 3. Build prior-week gap set for delta calculation
    prior_gaps: set[str] = set()
    for row in prior_week:
        norm = normalise_url(row["broken_url"])
        if norm and norm not in redirect_sources:
            prior_gaps.add(norm)

    # 4. Build current-week report
    report_rows = []
    for row in current_week:
        raw_url = row.get("broken_url") or ""
        norm = normalise_url(raw_url)
        if not norm:
            continue
        hits_current = int(row.get("hits") or 0)
        hits_prior = next(
            (int(r["hits"]) for r in prior_week
             if normalise_url(r.get("broken_url") or "") == norm),
            0
        )
        is_covered = norm in redirect_sources
        is_new_gap = (not is_covered) and (norm not in prior_gaps)

        report_rows.append({
            "broken_url": norm,
            "hits_this_week": hits_current,
            "hits_last_week": hits_prior,
            "is_covered_by_redirect": is_covered,
            "is_new_gap": is_new_gap,
        })

    # 5. Compute resolved (was a gap last week, is no longer generating hits)
    current_urls = {normalise_url(r["broken_url"]) for r in current_week}
    newly_covered = {
        g for g in prior_gaps
        if g in redirect_sources  # redirect was added
    }
    traffic_stopped = {
        g for g in prior_gaps
        if g not in current_urls and g not in redirect_sources  # stopped naturally
    }
    resolved_count = len(newly_covered) + len(traffic_stopped)

    # 6. Write CSV artifact
    report_dir.mkdir(parents=True, exist_ok=True)
    csv_path = report_dir / f"404-report-{today.isoformat()}.csv"
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "broken_url", "hits_this_week", "hits_last_week",
            "is_covered_by_redirect", "is_new_gap"
        ])
        writer.writeheader()
        writer.writerows(report_rows)
    print(f"Wrote CSV artifact: {csv_path}", file=sys.stderr)

    # 7. Output JSON summary to stdout for the agent
    uncovered = [r for r in report_rows if not r["is_covered_by_redirect"]]
    new_gaps = [r for r in uncovered if r["is_new_gap"]]

    # Split uncovered URLs into "signal" (enough hits to be worth a redirect)
    # and long-tail "noise" (below the reporting threshold). In a low-sample
    # dataset most broken URLs are hit once by bots/old links, so the raw
    # uncovered and new-gap counts churn heavily week-over-week and overstate
    # the problem. The headline leads with volume trend + significant gaps;
    # the long tail is reported only as a single rolled-up count.
    significant = [r for r in uncovered if r["hits_this_week"] >= report_min_hits]
    significant_new_gaps = [r for r in significant if r["is_new_gap"]]
    long_tail_count = len(uncovered) - len(significant)

    trend_pct = (
        round((total_current - total_prior) / total_prior * 100, 1)
        if total_prior else None
    )

    summary = {
        "report_date": today.isoformat(),
        # --- Headline: overall 404 volume trend (the metric that matters) ---
        "total_404s_this_week": total_current,
        "total_404s_last_week": total_prior,
        "trend_delta": total_current - total_prior,
        "trend_pct": trend_pct,
        # --- Signal: uncovered URLs with enough hits to be worth a redirect ---
        "report_min_hits": report_min_hits,
        "significant_uncovered_count": len(significant),
        "significant_new_gaps_count": len(significant_new_gaps),
        "top_significant_uncovered": significant[:10],
        # --- Context only: raw/long-tail counts (do NOT headline these) ---
        "uncovered_count": len(uncovered),
        "new_gaps_count": len(new_gaps),
        "long_tail_count": long_tail_count,
        "resolved_count": resolved_count,
        "csv_path": str(csv_path),
        "has_data": len(current_week) > 0,
    }

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
