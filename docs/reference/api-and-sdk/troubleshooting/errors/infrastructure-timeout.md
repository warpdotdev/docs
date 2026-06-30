---
description: >-
  The task was forcibly terminated after exceeding the maximum allowed duration.
  This is a platform-side timeout, not a task failure.
---

# infrastructure\_timeout

The `infrastructure_timeout` error occurs when a task remains in a non-terminal state past the maximum allowed duration and is forcibly terminated by the platform's stale-task cleanup job.

{% hint style="info" %}
This is classified as a **platform error** (task state → ERROR) rather than a user error, because the termination is caused by an infrastructure-enforced time limit, not by the task's logic or input.
{% endhint %}

***

## Details

* **HTTP Status:** `500 Internal Server Error`
* **Retryable:** No
* **Task State:** ERROR

***

## When does this occur?

This error is returned when:

* A task has been running for longer than the platform's maximum task age and is terminated by the periodic stale-task cleanup job
* The agent process became unresponsive and the task was never marked as completed or failed
* A long-running operation inside the agent (e.g., a large clone, slow build, or multi-hour computation) exceeded the wall-clock time limit

***

## Example response

```json
{
  "type": "https://docs.warp.dev/reference/api-and-sdk/troubleshooting/errors/infrastructure-timeout",
  "title": "Task has timed out",
  "status": 500,
  "instance": "/api/v1/agent/tasks",
  "error": "Task has timed out",
  "retryable": false,
  "trace_id": "abc123..."
}
```

***

## How to resolve

1. Review whether the task's workload can be completed within the platform's time limits. Break large tasks into smaller, faster subtasks if needed.
2. Retry the task with a more focused prompt or a smaller scope.
3. If you believe the timeout was unexpected (e.g., the task should have completed quickly), contact [Warp support](https://docs.warp.dev/support-and-community/troubleshooting-and-support/sending-us-feedback) and include the `trace_id` from the error response.

***

## Related

* [Cloud Agents Overview](https://docs.warp.dev/agent-platform/cloud-agents/overview) — How cloud agent tasks work
* [Oz Agent API & SDK](https://docs.warp.dev/reference/api-and-sdk/agent) — API reference
