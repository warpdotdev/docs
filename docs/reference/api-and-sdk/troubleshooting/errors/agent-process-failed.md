---
description: >-
  The agent process exited unexpectedly during task execution. This is a
  platform-side error unrelated to the task's logic or input.
---

# agent\_process\_failed

The `agent_process_failed` error occurs when the agent process running inside the sandbox exits unexpectedly with a non-setup failure — for example, due to an out-of-memory condition, an unhandled crash, or a harness-reported error.

{% hint style="info" %}
This is classified as a **platform error** (task state → ERROR) rather than a user error, because the failure originates in the agent infrastructure rather than the task's prompt or configuration.
{% endhint %}

***

## Details

* **HTTP Status:** `500 Internal Server Error`
* **Retryable:** No
* **Task State:** ERROR

***

## When does this occur?

This error is returned when:

* The agent process was killed by the operating system (e.g., out-of-memory)
* The agent harness crashed or exited with a non-zero exit code before completing the task
* The harness explicitly reported a non-setup terminal failure via the shutdown report endpoint

***

## Example response

```json
{
  "type": "https://docs.warp.dev/reference/api-and-sdk/troubleshooting/errors/agent-process-failed",
  "title": "The agent process exited unexpectedly.",
  "status": 500,
  "instance": "/api/v1/agent/tasks",
  "error": "The agent process exited unexpectedly.",
  "retryable": false,
  "trace_id": "abc123..."
}
```

***

## How to resolve

1. Retry the task — transient failures such as OOM kills often do not recur on a subsequent attempt.
2. If the error persists, check whether the task involves unusually memory- or compute-intensive operations that may be overwhelming the agent sandbox.
3. Contact [Warp support](https://docs.warp.dev/support-and-community/troubleshooting-and-support/sending-us-feedback) and include the `trace_id` from the error response if the problem continues.

***

## Related

* [Cloud Agents Overview](https://docs.warp.dev/agent-platform/cloud-agents/overview) — How cloud agent tasks work
* [Oz Agent API & SDK](https://docs.warp.dev/reference/api-and-sdk/agent) — API reference
