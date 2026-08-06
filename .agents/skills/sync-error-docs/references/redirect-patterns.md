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

Catch-alls already cover every error code, current and future, in both slash forms:

```json
{
  "source": "/errors/:code",
  "destination": "/reference/api-and-sdk/troubleshooting/errors/:code/",
  "statusCode": 308
},
{
  "source": "/errors/:code/",
  "destination": "/reference/api-and-sdk/troubleshooting/errors/:code/",
  "statusCode": 308
}
```

`:code` is forwarded unchanged, so `/errors/insufficient_credits` lands on the underscored path, which the separator redirects below then resolve. Note that the trailing-slash catch-all preserves the slash into the destination, which is why the separator step must also cover the slashed form.

Because these rules are generic, **adding a new error code requires no change here.** Just confirm both still exist:

```bash
grep -F '"/errors/:code"' vercel.json
grep -F '"/errors/:code/"' vercel.json
```

If either is missing, restore that rule rather than adding one entry per code.

There are also bare `/errors` and `/errors/` redirects pointing at the errors index, which likewise need no per-code maintenance.

## 2. Separator redirects (two entries per code)

These are the only redirects a new error code needs. They map the underscored form to the hyphenated page slug, in both slash forms:

```json
{
  "source": "/reference/api-and-sdk/troubleshooting/errors/{underscore_code}",
  "destination": "/reference/api-and-sdk/troubleshooting/errors/{hyphen-code}/",
  "statusCode": 308
},
{
  "source": "/reference/api-and-sdk/troubleshooting/errors/{underscore_code}/",
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
},
{
  "source": "/reference/api-and-sdk/troubleshooting/errors/insufficient_credits/",
  "destination": "/reference/api-and-sdk/troubleshooting/errors/insufficient-credits/",
  "statusCode": 308
}
```

Rules:

- **Add both slash variants.** All 17 codes currently in `vercel.json` have both (34 entries); none has only one. A single variant leaves the new code less covered than every existing one, and the trailing-slash catch-all in section 1 forwards its slash through, so the slashed underscore path would otherwise 404.
- `source` has a **leading slash** and no file extension.
- `destination` has a **trailing slash** in both entries. Every existing error redirect does.
- Always set `"statusCode": 308`.
- Add the entries near the other `/reference/api-and-sdk/troubleshooting/errors/` redirects so they stay grouped.
- Check for existing entries before adding, so re-runs stay idempotent:

  ```bash
  grep -F '"/reference/api-and-sdk/troubleshooting/errors/{underscore_code}"' vercel.json
  grep -F '"/reference/api-and-sdk/troubleshooting/errors/{underscore_code}/"' vercel.json
  ```

## Note on the former GitBook flow

Earlier versions of this reference created the prefix redirect through the GitBook API using `scripts/docs_redirects.py` and a `GITBOOK_TOKEN` secret. That approach no longer applies: the docs moved from GitBook to Astro Starlight on Vercel, redirects are plain JSON in `vercel.json`, and the prefix case is now covered by the generic `/errors/:code` rule. Neither the script nor the token is needed.
