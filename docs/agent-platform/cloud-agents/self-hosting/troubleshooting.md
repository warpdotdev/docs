---
description: >-
  Diagnose and fix common problems with self-hosted Oz worker daemons across
  Docker, Kubernetes, and Direct backends.
---

# Self-hosting troubleshooting

Diagnostic guides for the `oz-agent-worker` daemon and its task execution. Use this page when a worker won't start, won't connect, tasks stay queued, or tasks fail.

{% hint style="info" %}
The steps below apply to the [managed architecture](README.md#managed-architecture) (`oz-agent-worker` daemon). For [unmanaged](unmanaged.md) deployments, refer to the documentation for the environment running `oz agent run` (e.g., GitHub Actions, Kubernetes).
{% endhint %}

***

## Worker won't start

### Docker backend

**Cause:** Docker isn't running, or the daemon platform isn't supported.

**Fix:**

1. Verify Docker is running: `docker info`.
2. Confirm the daemon platform is `linux/amd64` or `linux/arm64`. Windows containers are not supported.
3. If the worker runs inside Docker, confirm the `/var/run/docker.sock` mount is correct and the mounting user has permission to the socket.

### Kubernetes backend

**Cause:** The startup preflight Job failed. Common reasons include insufficient RBAC, restrictive Pod Security policies, or an unreachable Kubernetes API server.

**Fix:**

1. Check the worker logs for the preflight diagnostic message.
2. Confirm the worker's namespace has these permissions: `create`, `get`, `list`, `watch`, `delete` on `jobs`; `get`, `list`, `watch` on `pods`; `get` on `pods/log`; `list` on `events`.
3. Confirm the task namespace allows pods with a **root init container** (required for sidecar materialization).
4. If your cluster restricts image sources, set `preflight_image` in the worker config to an allowlisted image (default is `busybox:1.36`).
5. To pull the preflight image from a private registry, configure `imagePullSecrets` in `pod_template` — these secrets also apply to the preflight Job.

### Direct backend

**Cause:** The `oz` CLI isn't installed or isn't on the worker's `PATH`.

**Fix:**

1. Install the Oz CLI on the worker host. See [Installing the CLI](https://docs.warp.dev/reference/cli#installing-the-cli).
2. If the CLI isn't on `PATH`, set `oz_path` in the config file to the absolute path of the `oz` binary.

***

## Worker won't connect

**Cause:** The API key is invalid, expired, or the host cannot reach Oz's backend.

**Fix:**

1. Confirm your API key is correct, not expired, and has team scope.
2. Regenerate the API key in **Settings** > **Cloud platform** > **Oz Cloud API Keys** if you suspect it's invalid.
3. Ensure the host has outbound internet access to `oz.warp.dev:443`.
4. Check that no firewall rules are blocking WebSocket connections to `wss://oz.warp.dev`.
5. Increase log verbosity with `--log-level debug` to see connection details.

See [Security and networking](security-and-networking.md#network-requirements) for the full list of outbound endpoints the worker needs.

***

## Tasks not being picked up

**Cause:** The worker isn't running, the `--host` value doesn't match the worker's `--worker-id`, or the worker and task belong to different teams.

**Fix:**

1. Confirm the worker is running and connected. Check the worker logs for `Listening for tasks` or similar.
2. Verify the `--host` (or `worker_host`) value you passed matches your `--worker-id` exactly. Case-sensitive.
3. Ensure the worker's team matches the team creating the task.

***

## Task failures

**Cause:** A variety of reasons depending on backend. Start with the diagnostic steps common to all backends, then follow the backend-specific checks.

**Fix (all backends):**

1. Review task logs in the [Oz dashboard](https://oz.warp.dev) or via [session sharing](../../warp-agents/session-sharing.md).
2. Use `--no-cleanup` to keep the container, Job, or workspace around for inspection after failure.
3. Use `--log-level debug` to see detailed execution logs.
4. Ensure the worker machine or cluster has sufficient resources (CPU, memory, disk).

### Docker backend (task failures)

1. Verify Docker is running (`docker info`).
2. If using a custom image, confirm it is **glibc-based** (not Alpine/musl) and that its architecture matches the worker's Docker daemon platform.

### Kubernetes backend (task failures)

1. Check task Job and Pod status: `kubectl get jobs,pods -n <namespace>`.
2. Common issues:
   * **Unschedulable pods** — Check node selectors, tolerations, and resource requests in `pod_template`.
   * **Image pull failures** — Check `imagePullSecrets` in `pod_template`.
   * **Admission policy rejections** — Review Pod Security Standards, OPA Gatekeeper, Kyverno, or similar admission controllers.
3. The worker fails a task early if its pod remains unschedulable beyond `unschedulable_timeout` (default `30s`). Raise the timeout or fix the scheduling issue.

### Direct backend (task failures)

1. Verify the Oz CLI is accessible.
2. Verify the workspace root directory has write permissions for the user running the worker.

***

## Image pull failures

### Docker backend (image pull)

1. If using a private registry, ensure Docker credentials are available to the worker. See [Private Docker registries](managed-docker.md#private-docker-registries).
2. Try pulling the image manually on the worker host: `docker pull <image>`.

### Kubernetes backend (image pull)

1. Configure `imagePullSecrets` in the `pod_template` section of your worker config.
2. Verify the Secret exists in the task namespace and contains valid credentials.

### Both backends (image pull)

* Verify the image exists and the tag is correct.
* Check network connectivity from the worker/cluster to the registry.

***

## Related pages

* [Self-hosting overview](README.md) — Architecture and decision guide.
* [Self-hosted worker reference](reference.md) — CLI flags and config schema, including every flag mentioned here.
* [Security and networking](security-and-networking.md) — Outbound endpoints the worker needs.
* [Agent Session Sharing](../../warp-agents/session-sharing.md) — Attach to running tasks to debug interactively.
