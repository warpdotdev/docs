---
description: >-
  Reference documentation for the oz-agent-worker daemon, including CLI flags,
  Docker connectivity, private registries, and load balancing.
---

# Managed worker reference

This page covers operational details for running the `oz-agent-worker` daemon. For an overview of the managed architecture and when to use it, see [Self-Hosting](self-hosting.md#managed-architecture).

***

## Worker flags reference

The following flags are available when starting the worker:

**Required:**

* `--worker-id` — A string identifying this worker. This is the value you pass to `--host` when routing tasks. Choose something meaningful for your team (e.g., `prod-runner-1` or `ci-worker`). Multiple workers can share the same ID for load balancing (see below).
* `--api-key` or `WARP_API_KEY` env var — Your team API key for authentication. When running via Docker, pass it as `-e WARP_API_KEY="..."`. When running the binary directly, use `--api-key` or the environment variable.

**Optional:**

* `--log-level` — Log verbosity. One of `debug`, `info`, `warn`, `error`. Defaults to `info`.
* `--no-cleanup` — Do not remove task containers after execution. Useful for debugging failed tasks—you can inspect the container's filesystem and logs after the run.
* `-v` / `--volumes` — Mount host directories into task containers. Format: `HOST_PATH:CONTAINER_PATH` or `HOST_PATH:CONTAINER_PATH:MODE` (where MODE is `ro` or `rw`). Can be specified multiple times.
* `-e` / `--env` — Set environment variables in task containers. Format: `KEY=VALUE` (explicit value) or `KEY` (pass through from host environment). Can be specified multiple times.

{% hint style="info" %}
Worker IDs starting with `warp` are reserved and cannot be used. The worker will refuse to start if `--worker-id` begins with `warp`.
{% endhint %}

**Example with all flags:**

```bash
docker run -v /var/run/docker.sock:/var/run/docker.sock \
  -e WARP_API_KEY="$WARP_API_KEY" \
  warpdotdev/oz-agent-worker \
  --worker-id "prod-runner-1" \
  --log-level debug \
  --no-cleanup \
  -v /opt/shared-cache:/cache:ro \
  -e NPM_TOKEN=your_token \
  -e GITHUB_TOKEN
```

{% hint style="warning" %}
When running the worker via Docker, there are two levels of `-e` flags. Docker's `-e` passes env vars to the **worker container** (e.g., `WARP_API_KEY`). The worker's `-e` / `--env` flags pass env vars into the **task containers** that the worker spawns. Keep these distinct:

```bash
# Docker -e: passes WARP_API_KEY to the worker container
# Worker -e: passes MY_SECRET to task containers
docker run \
  -e WARP_API_KEY="$WARP_API_KEY" \
  warpdotdev/oz-agent-worker \
  --worker-id "my-worker" \
  -e MY_SECRET=hunter2
```
{% endhint %}

Once started, the worker connects to Oz, waits for tasks routed to its worker ID, runs each task in an isolated Docker container, and reports status and results back. The worker automatically reconnects if the connection drops.

You can run multiple workers with the same `--worker-id` for redundancy — tasks are distributed across connected workers.

***

## Docker connectivity

The worker uses the standard Docker client discovery mechanism to find the Docker daemon:

1. **`DOCKER_HOST`** environment variable (e.g., `unix:///var/run/docker.sock`, `tcp://localhost:2375`)
2. **Default socket** (`/var/run/docker.sock` on Linux, `~/.docker/run/docker.sock` for rootless Docker)
3. **Docker context** via `DOCKER_CONTEXT` environment variable
4. **Config file** (`~/.docker/config.json`) for context settings

Additional Docker environment variables:

* `DOCKER_API_VERSION` — Specify Docker API version
* `DOCKER_CERT_PATH` — Path to TLS certificates
* `DOCKER_TLS_VERIFY` — Enable TLS verification

{% hint style="info" %}
If the worker itself runs in Docker, you must mount any relevant config files (e.g., `~/.docker/config.json`) into the worker container for Docker context and credential discovery to work.
{% endhint %}

**Example: Connecting to a remote Docker daemon**

```bash
export DOCKER_HOST="tcp://remote-host:2376"
export DOCKER_TLS_VERIFY=1
export DOCKER_CERT_PATH="/path/to/certs"
oz-agent-worker --api-key "$WARP_API_KEY" --worker-id "my-worker"
```

***

## Private Docker registries

The worker automatically uses credentials from your Docker config (`~/.docker/config.json`) when pulling task images. If your [environments](environments.md) use images from a private registry, make sure the worker's host has been authenticated:

```bash
docker login your-registry.example.com
```

When running the worker via Docker, mount the Docker config into the container:

```bash
docker run \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v ~/.docker/config.json:/root/.docker/config.json:ro \
  -e WARP_API_KEY="$WARP_API_KEY" \
  warpdotdev/oz-agent-worker --worker-id "my-worker"
```

{% hint style="info" %}
Sidecar images (the Oz agent binary and dependencies) are pulled from public registries and do not require authentication.
{% endhint %}

***

## Related resources

* [Self-Hosting](self-hosting.md) — Architecture overview, setup guides, and decision guide
* [Environments](environments.md) — Creating and configuring environments for agent runs
* [Deployment Patterns](deployment-patterns.md) — Common architectures for deploying cloud agents
