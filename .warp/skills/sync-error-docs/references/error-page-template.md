# Error Page Template

Use this template when creating a new error documentation page. Replace all `{PLACEHOLDER}` values.

## Template

```markdown
---
description: >-
  {SHORT_DESCRIPTION_TWO_LINES}
---

# {underscore\_code}

The `{underscore_code}` error occurs when {PLAIN_ENGLISH_EXPLANATION}.

***

## Details

* **HTTP Status:** `{STATUS_CODE} {STATUS_TEXT}`
* **Retryable:** {Yes/No}
* **Task State:** {FAILED/ERROR}

***

## When does this occur?

This error is returned when:

* {CONDITION_1}
* {CONDITION_2}
* {CONDITION_3}

***

## Example response

\```json
{
  "type": "https://docs.warp.dev/reference/api-and-sdk/troubleshooting/errors/{hyphen-code}",
  "title": "{USER_FACING_MESSAGE}",
  "status": {STATUS_CODE_INT},
  "instance": "/api/v1/agent/tasks",
  "error": "{USER_FACING_MESSAGE}",
  "retryable": {true/false},
  "trace_id": "abc123..."
}
\```

***

## How to resolve

1. {RESOLUTION_STEP_1}
2. {RESOLUTION_STEP_2}
3. {RESOLUTION_STEP_3}

***

## Related

* [Oz Agent API & SDK](https://docs.warp.dev/reference/api-and-sdk/agent) — API reference
* [Cloud Agents Overview](https://docs.warp.dev/agent-platform/cloud-agents/overview) — How cloud agents work
```

## Placeholder reference

- `{underscore_code}` — The error code as defined in `platformerrors.go` (e.g., `insufficient_credits`)
- `{underscore\_code}` — Same but with underscores escaped for Astro Starlight H1 headings (e.g., `insufficient\_credits`)
- `{hyphen-code}` — The code with hyphens for URLs/filenames (e.g., `insufficient-credits`)
- `{SHORT_DESCRIPTION_TWO_LINES}` — A 1–2 line description for the YAML frontmatter `description` field
- `{STATUS_CODE}` / `{STATUS_TEXT}` — HTTP status (e.g., `403 Forbidden`). Get from `FromError()` or the constructor in `platformerrors.go`
- `{FAILED/ERROR}` — `FAILED` for user errors (`IsUserError() == true`), `ERROR` for platform errors
- `{USER_FACING_MESSAGE}` — The message from `FromError()` or the constructor's `userFacingMessage` field
- `{true/false}` for retryable — From the `Retryable()` method or `retryable` field
- `"trace_id"` — Include this field only when the resolution steps direct users to contact Warp support (support needs it to investigate). Omit entirely for self-serve resolutions.

## Conventions

- The H1 title uses the underscore form with `\_` escaping (Astro Starlight renders underscores as italics otherwise)
- The opening paragraph uses backtick-wrapped underscore form: `` `insufficient_credits` ``
- The example JSON `type` field uses the full doc page URL (not the short `/errors/` redirect)
- Include `trace_id` in the example JSON only when the resolution steps direct users to contact Warp support — support needs it to investigate. Omit entirely for self-serve resolutions (e.g. buy credits, update API key, wait and retry).
- Platform errors should include a `:::note` callout explaining the ERROR vs FAILED distinction (see `authentication-required.md` for an example)
- Keep resolution steps actionable and numbered
- Related links should be relevant to the specific error (billing page for credit errors, environment page for setup errors, etc.)
