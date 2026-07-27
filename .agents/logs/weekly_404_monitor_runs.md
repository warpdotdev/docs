# Weekly 404 monitor run log

New entries are prepended by each scheduled agent run. Most recent entry first.

This log tracks every run of the `weekly-404-monitor` skill — both runs that opened a redirect PR and runs that wrote a no-PR report — so the team and the `improve-404-monitor-skill` outer loop can evaluate threshold effectiveness, redirect accuracy, and coverage trends over time.

**Format**: see the `## Run log format` section in `.agents/skills/weekly-404-monitor/SKILL.md`.

---

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
