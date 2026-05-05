# Redirect Patterns

Two types of redirects are needed for each error code to ensure the API's `type` URI resolves to the correct documentation page.

## Background

The `platformerrors` package defines `ProblemTypeBaseURI = "https://docs.warp.dev/errors/"`. API error responses include a `type` field like:

```
https://docs.warp.dev/errors/insufficient_credits
```

But the actual documentation page lives at:

```
https://docs.warp.dev/reference/api-and-sdk/troubleshooting/errors/insufficient-credits
```

Two redirects bridge this gap:
1. A **site-level redirect** from `/errors/{underscore_code}` to the full doc page URL
2. A **Astro Starlight space redirect** from the underscore filename to the hyphen filename (within the reference space)

## 1. Site-level redirect (Astro Starlight API)

<!-- TODO: Post-migration, update this to use vercel.json redirects instead of the GitBook API. -->
This redirect is created via the GitBook API using `scripts/docs_redirects.py`. It requires the `GITBOOK_TOKEN` environment variable.

### Create a redirect

```bash
python3 docs/scripts/docs_redirects.py create \
  --source "/errors/{underscore_code}" \
  --destination-json '{"kind": "url", "url": "https://docs.warp.dev/reference/api-and-sdk/troubleshooting/errors/{hyphen-code}"}'
```

### Check if a redirect already exists

```bash
python3 docs/scripts/docs_redirects.py get-by-source \
  --source "/errors/{underscore_code}"
```

### List existing error redirects

```bash
python3 docs/scripts/docs_redirects.py list --search "/errors/"
```

### Notes

- The script uses hardcoded org ID (`-MbqIZLCtzerswjFm7mh`) and site ID (`site_FKhQ8`) which are the Warp docs defaults
- If `GITBOOK_TOKEN` is not set, skip this step and report it — the redirect can be created manually later
- The destination `kind` is `"url"` (external URL redirect), not `"site-page"`

## 2. Astro Starlight space redirect (vercel.json (redirects))

This redirect lives in `docs/src/content/docs/reference/vercel.json (redirects)` and handles in-space navigation where someone might visit the underscore form of the path.

### Format

Add an entry under the `redirects:` key:

```yaml
redirects:
    # ... existing redirects ...

    # Error code underscore→hyphen redirects
    api-and-sdk/troubleshooting/errors/{underscore_code}: api-and-sdk/troubleshooting/errors/{hyphen-code}.md
```

### Example

For `insufficient_credits`:

```yaml
    api-and-sdk/troubleshooting/errors/insufficient_credits: api-and-sdk/troubleshooting/errors/insufficient-credits.md
```

### Notes

- Paths are relative to the space root (defined by `root: ./` in the yaml)
- The source path has NO leading slash and NO `.md` extension
- The destination path includes the `.md` extension
- Group error redirect entries together with a comment for clarity
