# Docs page feedback

Footer thumbs on every Starlight page (`PageHelpfulness.astro` via
`FeedbackFooter.astro`) and on `/api` record whether a page helped.

## Storage (no app database)

### RudderStack (primary)

- Event: `docs_page_feedback`
- Lands in the same website events pipeline as `docs_404`
  (`stg_website_events`)
- Use for agent queries, Metabase, and weekly improvement rollups

### Vercel Web Analytics

- Event: `DocsPageFeedback`
- Lands in Vercel project → Analytics → Custom Events
- Fast product glance; custom events need Pro/Enterprise

Do **not** introduce Vercel KV/Postgres for this signal. Thumbs are high-volume
and low-value per row; analytics events already power docs ops (see
`weekly-404-monitor`).

### Event properties (RudderStack)

- `page_path` — pathname, e.g. `/factories/troubleshooting/`
- `page_url` — absolute URL
- `vote` — `up` or `down`
- `comment` — optional free text on downvote (max 500 chars)
- `referrer` — `document.referrer` origin path when present

### Vercel custom event data

- `pagePath`, `vote`, `hasComment` (`true`/`false` strings)

## Rolling feedback into improvements

When improving Factories accuracy or running a docs quality pass:

1. **Kapa** — Docs + Front top questions, coverage gaps, and
   `confidence_filter=uncertain` threads (see
   `.agents/references/factories-accuracy.md`).
2. **Page feedback** — Query RudderStack/Metabase for
   `event_name = 'docs_page_feedback'` and `vote = 'down'`, group by
   `page_path`, prefer paths with comments.
3. **Cross-check** — Match downvoted factories paths against Kapa themes and
   the high-risk claims list before drafting fixes.
4. **Record** — Update the “Themes documented…” section in
   `factories-accuracy.md` (or a dated log under `.agents/logs/`) with the
   page path, vote counts, and whether a docs PR closed the gap.

### Example Metabase-shaped filter

```sql
SELECT
  event_properties:page_path::string AS page_path,
  event_properties:vote::string AS vote,
  event_properties:comment::string AS comment,
  COUNT(*) AS n
FROM stg_website_events
WHERE event_name = 'docs_page_feedback'
  AND received_at >= DATEADD('day', -28, CURRENT_TIMESTAMP())
GROUP BY 1, 2, 3
ORDER BY n DESC
```

Adjust table/column names to the live warehouse schema used by
`weekly-404-monitor`.

## Implementation files

- `src/components/PageHelpfulness.astro` — UI + track calls
- `src/components/FeedbackFooter.astro` — Starlight footer mount
- `src/pages/api.astro` — API reference mount + analytics loaders
