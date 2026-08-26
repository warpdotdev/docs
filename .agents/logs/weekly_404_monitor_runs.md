# Weekly 404 monitor run log

New entries are prepended by each scheduled agent run. Most recent entry first.

This log tracks every run of the `weekly-404-monitor` skill — both runs that opened a redirect PR and runs that wrote a no-PR report — so the team and the `improve-404-monitor-skill` outer loop can evaluate threshold effectiveness, redirect accuracy, and coverage trends over time.

**Format**: see the `## Run log format` section in `.agents/skills/weekly-404-monitor/SKILL.md`.

---

## 2026-08-24 — No data
- **Total 404s this week**: n/a
- **Total 404s last week**: n/a
- **Trend**: n/a
- **Significant gaps (≥5 hits)**: n/a
- **Redirect candidates processed**: 0  (hits ≥ 5)
- **HIGH-confidence redirects**: 0
- **PR**: none
- **Oz run**: https://app.warp.dev/conversation/afcb6bda-7cf7-499a-9d75-6a1c30f65097
- **Notes**: Metabase query failed with HTTP 401 Unauthenticated. `METABASE_API_KEY` is present in environment K5KStCm5aYvhfBJb8cHol6 but is a short placeholder/invalid value (len=16, not an `mb_` key), not a real Metabase API key for https://warp.metabaseapp.com. Posted failure notice to #growth-docs. Action needed: replace the secret with a valid Metabase API key and re-run. Same failure mode as 2026-08-10.

## 2026-08-17 — No data
- **Total 404s this week**: n/a
- **Total 404s last week**: n/a
- **Trend**: n/a
- **Significant gaps (≥5 hits)**: n/a
- **Redirect candidates processed**: 0  (hits ≥ 5)
- **HIGH-confidence redirects**: 0
- **PR**: none
- **Oz run**: https://app.warp.dev/conversation/3a498bed-08eb-4a2e-a05d-52a979d997c1
- **Notes**: Metabase query failed with HTTP 401 Unauthenticated. `METABASE_API_KEY` is present in environment K5KStCm5aYvhfBJb8cHol6 but is a short placeholder/invalid value, not a real Metabase API key for https://warp.metabaseapp.com. Same failure mode as 2026-08-10. Posted failure notice to #growth-docs. Action needed: replace the secret with a valid Metabase API key and re-run.

## 2026-08-10 — No data
- **Total 404s this week**: n/a
- **Total 404s last week**: n/a
- **Trend**: n/a
- **Significant gaps (≥5 hits)**: n/a
- **Redirect candidates processed**: 0  (hits ≥ 5)
- **HIGH-confidence redirects**: 0
- **PR**: none
- **Oz run**: https://app.warp.dev/conversation/28103b9a-cbdb-4b07-b73e-555b88656028
- **Notes**: Metabase query failed with HTTP 401 Unauthenticated. `METABASE_API_KEY` is present in environment K5KStCm5aYvhfBJb8cHol6 but is a short placeholder/invalid value, not a real Metabase API key for https://warp.metabaseapp.com. Posted failure notice to #growth-docs. Action needed: replace the secret with a valid Metabase API key and re-run.

## 2026-08-03 — No PR
- **Total 404s this week**: 323
- **Total 404s last week**: 458
- **Trend**: ▼ 135 (-29.5%)
- **Significant gaps (≥5 hits)**: 0 (0 new)
- **Redirect candidates processed**: 0  (hits ≥ 5)
- **HIGH-confidence redirects**: 0
- **PR**: none
- **Oz run**: https://staging.warp.dev/conversation/1703d43c-d6c3-46bc-adf9-d0531cc582ac
- **Notes**: `docs_404` data is flowing now (METABASE_API_KEY set in this run's environment, unlike the earlier same-day "No data" entry below). 257 pages had SQL-normalised hits; 252 uncovered, all below the 5-hit reporting threshold (pure long tail — no significant gaps). 295 resolved since last week. Posted summary to #growth-docs.

## 2026-08-03 — No data
- **Total 404s this week**: n/a
- **Total 404s last week**: n/a
- **Trend**: n/a
- **Significant gaps (≥5 hits)**: n/a
- **Redirect candidates processed**: 0  (hits ≥ 5)
- **HIGH-confidence redirects**: 0
- **PR**: none
- **Oz run**: https://app.warp.dev/conversation/61e9dfd8-e1c0-4d61-a007-9f2d8ea3360d
- **Notes**: Failed fast — METABASE_API_KEY is not set in the current Oz environment (current_environment_id=6qDvDbgkCLF3I0rLFEmiFo). Posted failure notice to #growth-docs. Expected secret on Docs Agent env K5KStCm5aYvhfBJb8cHol6.

## 2026-07-27 — PR opened
- **Total 404s this week**: 458
- **Total 404s last week**: 439
- **Trend**: ▲ 19 (4.3%)
- **Significant gaps (≥5 hits)**: 3 (2 new)
- **Redirect candidates processed**: 1 (hits ≥ 5, excluding `/404` which is the error page itself)
- **HIGH-confidence redirects**: 1
- **PR**: https://github.com/warpdotdev/docs/pull/385
- **Oz run**: https://staging.warp.dev/conversation/5557485e-b9bc-4136-9b3c-0faadde5e1ab
- **Notes**: `/404` gap (6 hits) excluded from redirects — it is the 404 error page path itself, not a content page. `/team/index.md` (5 hits) excluded — raw `.md` extension URL with no clear landing page target; likely a stale link to a markdown file from an external source. 326 pages had SQL-normalised hits; 321 uncovered (318 below threshold). 239 resolved since last week.

---
