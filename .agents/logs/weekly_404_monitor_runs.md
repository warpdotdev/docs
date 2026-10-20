# Weekly 404 monitor run log
## 2026-10-20 — No PR (controlled manual test)
- **Total 404s this week**: 263
- **Total 404s last week**: 268
- **Trend**: ▼ 5 (-1.9%)
- **Significant gaps (≥5 hits)**: 2 (2 new)
- **Redirect candidates processed**: 2  (hits ≥ 5)
- **HIGH-confidence redirects**: 0
- **PR**: none
- **Oz run**: https://staging.warp.dev/conversation/ee739e34-eeed-4626-8600-6e783779a9e9
- **Validation**: Log structure and byte-preserved historical entries passed; `git diff --check` passed; `python3 .agents/skills/check_for_broken_links/check_links.py --internal-only` exited 0 (398 files, 4482 internal links, 0 broken). Ordered public-site typecheck/build/render checks not exercised because no public docs or redirects changed. Trunk not exercised (not installed); no tooling repairs attempted.
- **Notes**: Controlled manual test; not a scheduled weekly baseline. Required config commit `55cf09f3aeded3e8311a96492f763aac6bd946f0` verified; API-verified manual guard exit 0 (CLI source, user creator, service-account executor, matching run identity). Unchanged report script exit 0. Current/prior UTC windows are October 13–19 and October 6–12; all 263/268 events have usable captures, with 190/151 normalized paths below the top-500 cap. Current main `569b20c6f6582cba7d87000b8a80509e3956a4c2` has 1373 redirects (sanity passed). Phase 2: 0 HIGH, 1 MEDIUM suggestion reserved for human review in the final report, 1 LOW embedded-URL capture artifact rejected. No redirect edits or redirect PR warranted. 163 long-tail uncovered, 0 colon-segment malformed paths, 104 resolved. CSV attached only as run artifact `01a15b39-817c-7562-9945-613cbabfa023` (190 rows; query/fragment stripping and two additional identifier-like path redactions; SHA-256 `99f2751fd0b03b637494af9ba6d69c19a5d946dbd44c786dfc78aba9a689dc1c`). Historical entries preserved; absent standing log branch recreated from current main in an isolated worktree. Final Slack test delivery follows durable logging; its receipt is retained in run output. Native cron dispatch was not exercised. No merges, deployments, secret changes, or schedule changes.

## 2026-10-19 — No PR
- **Total 404s this week**: 241
- **Total 404s last week**: 284
- **Trend**: ▼ 43 (-15.1%)
- **Significant gaps (≥5 hits)**: 1 (1 new)
- **Redirect candidates processed**: 1  (hits ≥ 5)
- **HIGH-confidence redirects**: 0
- **PR**: none
- **Oz run**: https://app.warp.dev/conversation/ecb8cf70-6ee1-493d-a508-d8cd031e17b4
- **Notes**: Volume down 15.1% week-over-week. Sole significant gap is a URL-smash capture artifact: `/agents/cli/https:/docs.warp.dev/agents/cli/quickstarthttps:/formulae.brew.sh` (7 hits, new). Contains embedded `https:` hosts (docs.warp.dev + formulae.brew.sh) glued into a docs path — not a real page and not safe/useful as a vercel.json source. No HIGH/MEDIUM redirects. 147 long-tail uncovered; 0 unroutable by `:`-segment rule; 110 resolved since last week. vercel.json redirects count 1371 (sanity OK). Posted summary to #growth-docs.

## 2026-10-12 — PR opened
- **Total 404s this week**: 284
- **Total 404s last week**: 313
- **Trend**: ▼ 29 (-9.3%)
- **Significant gaps (≥5 hits)**: 4 (4 new)
- **Redirect candidates processed**: 4  (hits ≥ 5)
- **HIGH-confidence redirects**: 4
- **PR**: https://github.com/warpdotdev/docs/pull/906
- **Oz run**: https://app.warp.dev/conversation/b7967894-caa5-4d3e-a8a2-e312027509da
- **Notes**: Volume down 9.3% week-over-week. Significant gaps: `/reference/cli/api-keys` (11), `/reference/api-and-sdk/troubleshooting/errors/invalid-request` (9), `/reference/cli/skills` (7), `/performance/terminal-features` (5) — all new. Live checks: `/reference/cli/:path*` and `/reference/api-and-sdk/:path*` splats 308 the no-slash form, but trailing-slash variants still 404; `/performance/terminal-features` had no redirect. Added explicit `(/?)` HIGH redirects for all four. 128 long-tail uncovered; 0 unroutable; 113 resolved since last week. No MEDIUM suggestions. vercel.json redirects count 1370 pre-edit / 1374 post-edit (sanity OK).

## 2026-10-05 — PR opened
- **Total 404s this week**: 313
- **Total 404s last week**: 231
- **Trend**: ▲ 82 (35.5%)
- **Significant gaps (≥5 hits)**: 2 (1 new)
- **Redirect candidates processed**: 2  (hits ≥ 5)
- **HIGH-confidence redirects**: 2
- **PR**: https://github.com/warpdotdev/docs/pull/825
- **Oz run**: https://app.warp.dev/conversation/27651680-657e-4a5c-a058-408b3c4f5d36
- **Notes**: Significant gaps were `/agents/overview` (6 hits) and GitBook revision `/~/revisions/.../features/smart-select` (6 hits, new). 132 long-tail uncovered URLs rolled up. 142 resolved since last week. No unroutable paths. No MEDIUM suggestions.

New entries are prepended by each scheduled agent run. Most recent entry first.

This log tracks every run of the `weekly-404-monitor` skill — both runs that opened a redirect PR and runs that wrote a no-PR report — so the team and the `improve-404-monitor-skill` outer loop can evaluate threshold effectiveness, redirect accuracy, and coverage trends over time.

**Format**: see the `## Run log format` section in `.agents/skills/weekly-404-monitor/SKILL.md`.

---

## 2026-09-28 — No PR
- **Total 404s this week**: 231
- **Total 404s last week**: 321
- **Trend**: ▼ 90 (-28.0%)
- **Significant gaps (≥5 hits)**: 3 (3 new)
- **Redirect candidates processed**: 3  (hits ≥ 5)
- **HIGH-confidence redirects**: 0
- **PR**: none
- **Oz run**: https://app.warp.dev/conversation/96dec96c-6bf7-4910-90d9-5555fdf9f5b7
- **Notes**: Volume down 28% week-over-week. All 3 significant gaps are markdown-link capture artifacts ending in literal `).` — `/terminal/settings/file-locations/).` (8), `/terminal/settings/all-settings/).` (7), `/agent-platform/capabilities/skills/).` (5). Underlying pages exist (`terminal/settings/file-locations`, `terminal/settings/all-settings`, `agents/capabilities/skills` via existing agent-platform→agents redirect). No HIGH PR: a bare `)` in a Vercel `source` is path-to-regexp group syntax (same class of issue as prior `:` exclusions), so automated redirects would either mis-parse or over-match. Posted destinations as MEDIUM suggestions for human review. 149 long-tail uncovered; 0 unroutable; 126 resolved. vercel.json redirects count 1298 (sanity OK).

## 2026-09-21 — PR opened
- **Total 404s this week**: 321
- **Total 404s last week**: 327
- **Trend**: ▼ 1.8%
- **Significant gaps (≥5 hits)**: 1 (0 new)
- **Redirect candidates processed**: 1  (hits ≥ 5)
- **HIGH-confidence redirects**: 1
- **PR**: https://github.com/warpdotdev/docs/pull/777
- **Oz run**: https://app.warp.dev/conversation/dd5a93a8-dadd-4255-a9ea-90fa21aeb332
- **Notes**: Significant gap `/agent-platform/inference/bring-your-own-api-key.md` (5 hits). HIGH redirect to `/agents/inference/bring-your-own-api-key/` via existing agent-platform→agents migration pattern (slash form already covered; `.md` suffix was not). 141 long-tail uncovered; 1 unroutable malformed path; 133 resolved since last week. No MEDIUM suggestions.

## 2026-09-14 — PR opened
- **Total 404s this week**: 327
- **Total 404s last week**: 258
- **Trend**: ▲ 69 (26.7%)
- **Significant gaps (≥5 hits)**: 4 (3 new)
- **Redirect candidates processed**: 1  (hits ≥ 5; excluded 2 malformed captures + 1 already-covered false positive)
- **HIGH-confidence redirects**: 1
- **PR**: https://github.com/warpdotdev/docs/pull/743
- **Oz run**: https://app.warp.dev/conversation/28de86d1-5d63-4a6f-b819-bca298a6601b
- **Notes**: 184 pages had SQL-normalised hits; 152 uncovered (148 below threshold). HIGH: `/agents/cli-agents` (5 hits) → `/agents/cli-agents/overview/` (section path has no index; overview is the landing page). `/features/session_management/launch-configuration` (5 hits) is a **false positive** — already covered by existing `vercel.json` source `/features/session_management/launch-configuration(/?)` from PR #715; `load_redirect_sources` does not strip the `(/?)` optional-slash pattern, so coverage detection misses it (follow-up: normalize `(/?)` when loading sources). Two recurring malformed gaps — `/support-and-community/troubleshooting-and-support/logging-out-and-uninstalling/:*logging` (10) and `/agents/local-agents/interacting-with-agents/voice/:)%3cb%3evoice` (9) — excluded again: underlying pages exist, and `:`-containing suffixes are path-to-regexp-unsafe + look like `docs_404` capture artifacts. 128 resolved since last week. Volume up 26.7% vs last week — worth watching. Posted summary to #growth-docs.

## 2026-09-09 — PR opened
- **Total 404s this week**: 270
- **Total 404s last week**: 299
- **Trend**: ▼ 29 (-9.7%)
- **Significant gaps (≥5 hits)**: 5 (3 new)
- **Redirect candidates processed**: 3  (hits ≥ 5, excluding 2 malformed captures)
- **HIGH-confidence redirects**: 2
- **PR**: https://github.com/warpdotdev/docs/pull/715
- **Oz run**: https://app.warp.dev/conversation/0d43fcb7-95f8-4b8e-9b9a-8fccf962631b
- **Notes**: `METABASE_API_KEY` now a valid `mb_...` key, but every query failed with `ValueError: Invalid header value` because the env-injected secret carries a trailing newline that urllib rejects in an HTTP header. Patched `run_404_report.py` to strip the key before use (PR #716) and re-ran successfully. 161 pages had SQL-normalised hits; 134 uncovered (129 below threshold). `/agents/agent-mode` (6 hits) → `/agents/` and `/features/session_management/launch-configuration` (5 hits) → `/terminal/sessions/launch-configurations/` added as HIGH-confidence redirects, mirroring existing analogous patterns already in `vercel.json`. `/agents/inference` (6 hits) posted to Slack as a MEDIUM-confidence suggestion (no exact index page under that directory). Two top gaps — `/support-and-community/troubleshooting-and-support/logging-out-and-uninstalling/:*logging` (10 hits) and `/agents/local-agents/interacting-with-agents/voice/:)%3cb%3evoice` (9 hits) — excluded from the redirect PR: their underlying pages already exist, and the malformed `:`-containing suffixes look like a `docs_404` capture/encoding artifact (a literal `:` is also unsafe as a vercel.json route source, since path-to-regexp treats it as a named parameter). Recommend the docs team check the `broken_url` capture for links with raw punctuation. 135 resolved since last week. Posted summary to #growth-docs.

## 2026-09-09 — No data
- **Total 404s this week**: n/a
- **Total 404s last week**: n/a
- **Trend**: n/a
- **Significant gaps (≥5 hits)**: n/a
- **Redirect candidates processed**: 0  (hits ≥ 5)
- **HIGH-confidence redirects**: 0
- **PR**: none
- **Oz run**: https://app.warp.dev/conversation/2f9e8558-518f-4943-b7b7-5854ac1309dd
- **Notes**: Metabase query failed with HTTP 401 Unauthenticated. `METABASE_API_KEY` is present in environment K5KStCm5aYvhfBJb8cHol6 but is a short placeholder/invalid value (len=16, not an `mb_` key), not a real Metabase API key for https://warp.metabaseapp.com. Posted failure notice to #growth-docs. Action needed: replace the secret with a valid Metabase API key and re-run. Same failure mode as 2026-08-10, 2026-08-17, 2026-08-24, 2026-08-31, and 2026-09-07.

## 2026-09-07 — No data
- **Total 404s this week**: n/a
- **Total 404s last week**: n/a
- **Trend**: n/a
- **Significant gaps (≥5 hits)**: n/a
- **Redirect candidates processed**: 0  (hits ≥ 5)
- **HIGH-confidence redirects**: 0
- **PR**: none
- **Oz run**: https://app.warp.dev/conversation/614247d9-e8a0-4628-9e1b-76b0db43b02b
- **Notes**: Metabase query failed with HTTP 401 Unauthenticated. `METABASE_API_KEY` is present in environment K5KStCm5aYvhfBJb8cHol6 but is a short placeholder/invalid value (len=16, not an `mb_` key), not a real Metabase API key for https://warp.metabaseapp.com. Posted failure notice to #growth-docs. Action needed: replace the secret with a valid Metabase API key and re-run. Same failure mode as 2026-08-10, 2026-08-17, 2026-08-24, and 2026-08-31.

## 2026-08-31 — No data
- **Total 404s this week**: n/a
- **Total 404s last week**: n/a
- **Trend**: n/a
- **Significant gaps (≥5 hits)**: n/a
- **Redirect candidates processed**: 0  (hits ≥ 5)
- **HIGH-confidence redirects**: 0
- **PR**: none
- **Oz run**: https://app.warp.dev/conversation/b421fdd1-e5eb-479c-a5f4-37e2c1c9b2fb
- **Notes**: Metabase query failed with HTTP 401 Unauthenticated. `METABASE_API_KEY` is present in environment K5KStCm5aYvhfBJb8cHol6 but is a short placeholder/invalid value (len=16, not an `mb_` key), not a real Metabase API key for https://warp.metabaseapp.com. Posted failure notice to #growth-docs. Action needed: replace the secret with a valid Metabase API key and re-run. Same failure mode as 2026-08-10, 2026-08-17, and 2026-08-24.

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
