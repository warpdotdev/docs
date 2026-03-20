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

* `--config-file` — Path to a YAML [config file](#config-file). CLI flags take precedence over config file values.
* `--backend` — Backend type: `docker` (default) or `direct`. See [Direct backend](#direct-backend).
* `--log-level` — Log verbosity. One of `debug`, `info`, `warn`, `error`. Defaults to `info`.
* `--no-cleanup` — Keep task containers or workspace directories after execution instead of removing them. Useful for debugging failed tasks.
* `-v` / `--volumes` — Mount host directories into task containers (Docker backend only). Format: `HOST_PATH:CONTAINER_PATH` or `HOST_PATH:CONTAINER_PATH:MODE` (where MODE is `ro` or `rw`). Can be specified multiple times.
* `-e` / `--env` — Set environment variables for tasks. Format: `KEY=VALUE` (explicit value) or `KEY` (pass through from host environment). Can be specified multiple times.
* `--max-concurrent-tasks` — Maximum number of tasks to run concurrently. Defaults to `0` (unlimited). When set, additional tasks wait until a slot is available.
* `--idle-on-complete` — How long to keep the oz agent process alive after a task's conversation finishes, allowing follow-up interactions via session sharing. Uses duration format (e.g. `45m`, `10m`, `0s`). Defaults to `45m` when not set. Set to `0s` to disable.

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
  --max-concurrent-tasks 4 \
  --idle-on-complete 10m \
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

Once started, the worker connects to Oz, waits for tasks routed to its worker ID, runs each task in an isolated Docker container (Docker backend) or directly on the host (direct backend), and reports status and results back. The worker automatically reconnects if the connection drops.

You can run multiple workers with the same `--worker-id` for redundancy — tasks are distributed across connected workers.

***

## Config file

For complex setups, you can use a YAML config file instead of (or in addition to) CLI flags. Pass it with `--config-file`:

```bash
oz-agent-worker --api-key "$WARP_API_KEY" --config-file config.yaml
```

CLI flags always take precedence over config file values.

### Docker backend config

```yaml
worker_id: "my-worker"
cleanup: true
max_concurrent_tasks: 4
idle_on_complete: "10m"
backend:
  docker:
    volumes:
      - "/data:/data:ro"
      - "/cache:/cache"
    environment:
      - name: NPM_TOKEN
        value: "your_token"
      - name: GITHUB_TOKEN  # inherits from host environment
```

### Direct backend config

```yaml
worker_id: "direct-worker"
max_concurrent_tasks: 2
backend:
  direct:
    workspace_root: "/var/lib/oz/workspaces"
    oz_path: "/usr/local/bin/oz"
    setup_command: "/opt/scripts/setup.sh"
    teardown_command: "/opt/scripts/teardown.sh"
    environment:
      - name: MY_VAR
        value: "hello"
```

### Config file fields

**Top-level:**

* `worker_id` — Worker identifier (same as `--worker-id` flag).
* `cleanup` — Whether to clean up after tasks. Defaults to `true`. Set to `false` to keep containers/workspaces for debugging (equivalent to `--no-cleanup`).
* `max_concurrent_tasks` — Maximum concurrent tasks. Defaults to unlimited.
* `idle_on_complete` — Duration to keep the `oz` process alive after task completion (e.g. `"45m"`, `"0s"`).
* `backend` — Backend configuration block. Only one backend (`docker` or `direct`) may be specified.

**`backend.docker`:**

* `volumes` — List of volume mounts (same format as `-v` flag).
* `environment` — List of environment variables with `name` and optional `value`. If `value` is omitted, the variable is inherited from the host.

**`backend.direct`:**

* `workspace_root` — Directory where per-task workspaces are created. Defaults to `/var/lib/oz/workspaces`.
* `oz_path` — Path to the oz CLI binary. If omitted, the worker looks up `oz` in `PATH`.
* `setup_command` — Shell command to run before each task. Receives `OZ_WORKSPACE_ROOT`, `OZ_RUN_ID`, `OZ_ENVIRONMENT_FILE`, and `OZ_WORKER_BACKEND` as environment variables.
* `teardown_command` — Shell command to run after each task completes.
* `environment` — List of environment variables (same format as the Docker backend).

{% hint style="info" %}
Only one backend can be configured at a time. Specifying both `docker` and `direct` in the same config file is an error.
{% endhint %}

***

## Direct backend

The direct backend runs agent tasks directly on the host machine without Docker. This is useful when Docker is unavailable or when tasks need direct access to host resources.

To use the direct backend, set `--backend direct` or configure it in the [config file](#config-file):

```bash
oz-agent-worker --api-key "$WARP_API_KEY" --worker-id "my-worker" --backend direct
```

Or with a config file:

```yaml
worker_id: "my-worker"
backend:
  direct:
    workspace_root: "/var/lib/oz/workspaces"
```

### How it works

1. The worker creates a per-task workspace directory under `workspace_root`.
2. If a `setup_command` is configured, it runs before the task with environment variables pointing to the workspace.
3. The oz CLI runs the agent task inside the workspace directory.
4. After the task completes, the optional `teardown_command` runs and the workspace is cleaned up.

### Requirements

* The **oz CLI** must be installed and available in `PATH` (or specified via `oz_path` in the config file).
* The worker must have write access to the `workspace_root` directory.

### Setup and teardown commands

The `setup_command` runs before each task and receives the following environment variables:

* `OZ_WORKSPACE_ROOT` — The workspace directory for the task.
* `OZ_RUN_ID` — The unique task ID.
* `OZ_ENVIRONMENT_FILE` — Path to a file where the setup script can write additional `KEY=VALUE` environment variables to inject into the task.
* `OZ_WORKER_BACKEND` — Always set to `direct`.

The `teardown_command` runs after each task and receives `OZ_WORKSPACE_ROOT`, `OZ_RUN_ID`, and `OZ_WORKER_BACKEND`.

{% hint style="info" %}
The direct backend starts from a minimal environment (only `HOME`, `TMPDIR`, and `PATH` from the host) to avoid leaking sensitive worker credentials into tasks. Add variables explicitly via `environment` in the config file or `-e` flags.
{% endhint %}

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
