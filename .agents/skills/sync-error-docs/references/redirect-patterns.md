# Redirect Patterns

How an API error's `type` URI resolves to its documentation page, and what (if anything) a new error code needs.

## Background

The `platformerrors` package defines `ProblemTypeBaseURI = "https://docs.warp.dev/errors/"`. API error responses include a `type` field like:

```
https://docs.warp.dev/errors/insufficient_credits
```

The documentation page lives at:

```
https://docs.warp.dev/reference/api-and-sdk/troubleshooting/errors/insufficient-credits
```

Two gaps separate them:

1. **Path prefix** — `/errors/{code}` versus the full `/reference/api-and-sdk/troubleshooting/errors/{code}` path.
2. **Separator** — error codes are underscored (`insufficient_credits`); page slugs are hyphenated (`insufficient-credits`).

Both are handled by entries in `vercel.json` at the repo root. All redirects for the site live in that one file.

## 1. Prefix redirect (already generic — no per-code work)

A catch-all already covers every error code, current and future:

```json
{
  "source": "/errors/:code",
  "destination": "/reference/api-and-sdk/troubleshooting/errors/:code/",
  "statusCode": 308
}
```

`:code` is forwarded unchanged, so `/errors/insufficient_credits` lands on the underscored path, which the separator redirect below then resolves.

Because this rule is generic, **adding a new error code requires no change here.** Just confirm it still exists:

```bash
grep -F '"/errors/:code"' vercel.json
```

If it is missing, restore this single rule rather than adding one entry per code.

There is also a bare `/errors` redirect pointing at the errors index, which likewise needs no per-code maintenance.

## 2. Separator redirect (one entry per code)

This is the only redirect a new error code needs. It maps the underscored form to the hyphenated page slug:

```json
{
  "source": "/reference/api-and-sdk/troubleshooting/errors/{underscore_code}",
  "destination": "/reference/api-and-sdk/troubleshooting/errors/{hyphen-code}/",
  "statusCode": 308
}
```

Example for `insufficient_credits`:

```json
{
  "source": "/reference/api-and-sdk/troubleshooting/errors/insufficient_credits",
  "destination": "/reference/api-and-sdk/troubleshooting/errors/insufficient-credits/",
  "statusCode": 308
}
```

Rules:

- `source` has a **leading slash**, no trailing slash, and no file extension.
- `destination` has a **trailing slash**. Every existing error redirect uses one.
- Always set `"statusCode": 308`.
- Add the entry near the other `/reference/api-and-sdk/troubleshooting/errors/` redirects so they stay grouped.
- Check for an existing entry before adding, so re-runs stay idempotent:

  ```bash
  grep -F '/reference/api-and-sdk/troubleshooting/errors/{underscore_code}"' vercel.json
  ```

## Note on the former GitBook flow

Earlier versions of this reference created the prefix redirect through the GitBook API using `scripts/docs_redirects.py` and a `GITBOOK_TOKEN` secret. That approach no longer applies: the docs moved from GitBook to Astro Starlight on Vercel, redirects are plain JSON in `vercel.json`, and the prefix case is now covered by the generic `/errors/:code` rule. Neither the script nor the token is needed.
