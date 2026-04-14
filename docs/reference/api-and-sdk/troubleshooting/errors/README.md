---
description: >-
  Reference for all error codes returned by the Oz platform API.
  Each error includes an HTTP status, machine-readable code, and actionable resolution steps.
---

# Errors Overview

When the Oz platform API encounters an error, it returns a structured JSON response following [RFC 7807 (Problem Details for HTTP APIs)](https://datatracker.ietf.org/doc/html/rfc7807). Every error response includes a machine-readable error code, a human-readable message, and metadata to help you diagnose and resolve the issue.

***

## Response format

All error responses share this structure:

```json
{
  "type": "https://docs.warp.dev/reference/api-and-sdk/troubleshooting/errors/invalid-request",
  "title": "The request contains invalid or missing parameters.",
  "status": 400,
  "detail": "schedule_id is required",
  "instance": "/api/v1/agent/tasks",
  "error": "The request contains invalid or missing parameters. (schedule_id is required)",
  "retryable": false,
  "trace_id": "abc123def456..."
}
```

Error responses use the `application/problem+json` content type per RFC 7807.

### Field reference

* **`type`** — A URI identifying the error type. Links to the documentation page for that error.
* **`title`** — A short, human-readable summary of the problem.
* **`status`** — The HTTP status code for this response.
* **`detail`** — Additional context specific to this occurrence of the error. Not always present.
* **`instance`** — The request path that produced the error.
* **`error`** — A backward-compatible field combining `title` and `detail` (for older clients). When `detail` is present, formatted as `"title (detail)"`.
* **`retryable`** — Whether this request can be retried. If `true`, the platform may automatically retry the operation.
* **`trace_id`** — An OpenTelemetry trace ID, included when available. Reference this when contacting support.

Some errors include additional metadata fields (for example, `auth_url`, `provider`, or `inaccessible_repos`). These are documented on each error's page.

***

## Error categories

Errors are split into two categories based on what caused the failure:

### User errors

These indicate something the caller needs to fix. When a cloud agent task encounters a user error, the task transitions to the **FAILED** state.

* [`insufficient_credits`](insufficient-credits.md) — Team has no remaining Add-on Credits
* [`feature_not_available`](feature-not-available.md) — Feature not included in your current plan
* [`external_authentication_required`](external-authentication-required.md) — External service authorization needed
* [`not_authorized`](not-authorized.md) — Insufficient permissions for the operation
* [`invalid_request`](invalid-request.md) — Malformed request or invalid parameters
* [`resource_not_found`](resource-not-found.md) — Referenced resource does not exist
* [`budget_exceeded`](budget-exceeded.md) — Spending budget limit reached
* [`integration_disabled`](integration-disabled.md) — Integration is disabled
* [`integration_not_configured`](integration-not-configured.md) — Integration setup is incomplete
* [`operation_not_supported`](operation-not-supported.md) — Operation not supported for this resource or state
* [`environment_setup_failed`](environment-setup-failed.md) — Cloud agent environment failed to initialize
* [`content_policy_violation`](content-policy-violation.md) — Task flagged by content policy checks
* [`conflict`](conflict.md) — Request conflicts with the current resource state (retryable)

### Platform errors

These indicate a Warp-side issue. When a cloud agent task encounters a platform error, the task transitions to the **ERROR** state. Retryable errors are automatically retried before the task is marked as failed.

* [`authentication_required`](authentication-required.md) — Invalid or expired API key
* [`resource_unavailable`](resource-unavailable.md) — Transient infrastructure issue (retryable)
* [`internal_error`](internal-error.md) — Unexpected server-side error (retryable)

***

## Using the `trace_id`

When an error response includes a `trace_id`, you can include it when [contacting Warp support](https://docs.warp.dev/support-and-community/troubleshooting-and-support/sending-us-feedback) to help the team locate the specific request in internal logs. This is especially useful for `internal_error` and `resource_unavailable` errors.

***

## Related

* [Oz API & SDK](https://docs.warp.dev/reference/api-and-sdk/agent) — API reference for creating and managing agent tasks
* [Cloud Agents Overview](https://docs.warp.dev/agent-platform/cloud-agents/overview) — How cloud agents work
* [Access, Billing, and Identity](https://docs.warp.dev/agent-platform/cloud-agents/team-access-billing-and-identity) — Plan requirements and billing details
