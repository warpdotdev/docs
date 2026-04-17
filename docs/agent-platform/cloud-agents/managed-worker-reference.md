---
description: >-
  Reference for the oz-agent-worker daemon, including CLI flags, Docker,
  Kubernetes, and Direct backend configuration, and the Helm chart.
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
* `--backend` — Backend type: `docker` (default), `kubernetes`, or `direct`. See [Kubernetes backend](#kubernetes-backend) and [Direct backend](#direct-backend).
* `--log-level` — Log verbosity. One of `debug`, `info`, `warn`, `error`. Defaults to `info`.
* `--no-cleanup` — Keep task containers, Kubernetes Jobs, or workspace directories after execution instead of removing them. Useful for debugging failed tasks.
* `-v` / `--volumes` — Mount host directories into task containers (Docker backend only). Format: `HOST_PATH:CONTAINER_PATH` or `HOST_PATH:CONTAINER_PATH:MODE` (where MODE is `ro` or `rw`). Can be specified multiple times.
* `-e` / `--env` — Set environment variables for tasks. Format: `KEY=VALUE` (explicit value) or `KEY` (pass through from host environment). Can be specified multiple times.
* `--max-concurrent-tasks` — Maximum number of tasks to run concurrently. Defaults to `0` (unlimited). When set, additional tasks wait until a slot is available.
* `--idle-on-complete` — How long to keep the `oz` process alive after a task's conversation finishes, allowing follow-up interactions via session sharing. Uses duration format (e.g. `45m`, `10m`, `0s`). Defaults to `45m` when not set. Set to `0s` to disable.

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

Once started, the worker connects to Oz, waits for tasks routed to its worker ID, runs each task in an isolated Docker container (Docker backend), a Kubernetes Job (Kubernetes backend), or directly on the host (Direct backend), and reports status and results back. The worker automatically reconnects if the connection drops.

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

### Kubernetes backend config

```yaml
worker_id: "k8s-worker"
max_concurrent_tasks: 4
backend:
  kubernetes:
    namespace: "warp-oz"
    default_image: "my-registry.io/dev-image:latest"
    unschedulable_timeout: "2m"
    pod_template:
      nodeSelector:
        kubernetes.io/os: linux
      containers:
        - name: task
          resources:
            requests:
              cpu: "2"
              memory: 4Gi
          env:
            - name: GITHUB_TOKEN
              valueFrom:
                secretKeyRef:
                  name: my-k8s-secret
                  key: github-token
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
* `backend` — Backend configuration block. Only one backend (`docker`, `kubernetes`, or `direct`) may be specified.

**`backend.docker`:**

* `volumes` — List of volume mounts (same format as `-v` flag).
* `environment` — List of environment variables with `name` and optional `value`. If `value` is omitted, the variable is inherited from the host.

**`backend.kubernetes`:**

* `namespace` — Kubernetes namespace for task Jobs. Defaults to `default`. This selects the namespace inside the chosen cluster; it does not choose the cluster.
* `kubeconfig` — Path to an explicit kubeconfig file. If omitted, the worker uses in-cluster config when running inside Kubernetes, or falls back to the default kubeconfig loading rules.
* `default_image` — Default Docker image for task Jobs when the run has no Warp environment image. Precedence: Warp environment image > `default_image` > `ubuntu:22.04`. Set this to skip creating a Warp environment when all your tasks use the same base image.
* `image_pull_policy` — One of `Always`, `Never`, or `IfNotPresent`. Defaults to `IfNotPresent`.
* `preflight_image` — Image used for the startup preflight Job. Defaults to `busybox:1.36`. Override this if your cluster only allows pulling from an internal or allowlisted registry.
* `setup_command` — Shell command to run before each task.
* `teardown_command` — Shell command to run after each task completes.
* `extra_labels` — Map of additional labels to add to task Jobs and Pods.
* `extra_annotations` — Map of additional annotations to add to task Jobs and Pods.
* `active_deadline_seconds` — Maximum lifetime for a task Job (Kubernetes `activeDeadlineSeconds`).
* `workspace_size_limit` — Size limit for the workspace `emptyDir` volume (e.g., `10Gi`).
* `unschedulable_timeout` — How long a pod may remain unschedulable before the task is failed early. Defaults to `30s`. Set to `0s` to disable the fail-fast behavior.
* `pod_template` — Raw Kubernetes PodSpec YAML merged with the worker's required fields at runtime. Use this to configure task pod scheduling, `serviceAccountName`, `imagePullSecrets`, `nodeSelector`, `tolerations`, resources, and environment variables (including `valueFrom.secretKeyRef` for Kubernetes Secrets). Define a container named `task` to customize the main task container directly; otherwise the worker appends its own.

**`backend.direct`:**

* `workspace_root` — Directory where per-task workspaces are created. Defaults to `/var/lib/oz/workspaces`.
* `oz_path` — Path to the oz CLI binary. If omitted, the worker looks up `oz` in `PATH`.
* `setup_command` — Shell command to run before each task. Receives `OZ_WORKSPACE_ROOT`, `OZ_RUN_ID`, `OZ_ENVIRONMENT_FILE`, and `OZ_WORKER_BACKEND` as environment variables.
* `teardown_command` — Shell command to run after each task completes.
* `environment` — List of environment variables (same format as the Docker backend).

{% hint style="info" %}
Only one backend can be configured at a time. Specifying more than one of `docker`, `kubernetes`, and `direct` in the same config file is an error.
{% endhint %}

***

## Kubernetes backend

The Kubernetes backend runs each agent task as a Kubernetes Job. The worker creates one Job per task in a target namespace and monitors the Job's pod lifecycle using Kubernetes Watch. This is the recommended backend when deploying the worker into an existing Kubernetes cluster.

To use the Kubernetes backend, configure it in the [config file](#config-file) or set `--backend kubernetes`:

```bash
oz-agent-worker --api-key "$WARP_API_KEY" --worker-id "my-worker" --backend kubernetes
```

Or with a config file (recommended for production):

```yaml
worker_id: "my-worker"
backend:
  kubernetes:
    namespace: "warp-oz"
    unschedulable_timeout: "2m"
    pod_template:
      nodeSelector:
        kubernetes.io/os: linux
      containers:
        - name: task
          resources:
            requests:
              cpu: "2"
              memory: 4Gi
```

### How it works

1. The worker connects to the Kubernetes API server (using in-cluster auth by default, or an explicit kubeconfig).
2. On startup, the worker runs a short-lived **preflight Job** to verify that cluster permissions, admission policies, and Pod Security Standards are compatible. If the preflight fails, the worker exits with a diagnostic error before accepting any tasks.
3. For each assigned task, the worker creates a Kubernetes Job in the configured namespace.
4. The worker monitors the Job and Pod status via Kubernetes Watch (with a 30-second safety-net poll for watch disconnects).
5. After the task completes, the Job is cleaned up (unless `--no-cleanup` is set).

### Requirements

* Kubernetes API access from the worker process (in-cluster or via kubeconfig).
* Namespace-scoped RBAC permissions:
  * `create`, `get`, `list`, `watch`, `delete` on `jobs`
  * `get`, `list`, `watch` on `pods`
  * `get` on `pods/log`
  * `list` on `events`
* The task namespace must allow creating Jobs with a **root init container**, as sidecar materialization currently depends on that pattern. Review your Pod Security Standards accordingly.

### Cluster selection

Cluster selection follows Kubernetes client config conventions:

* Set `backend.kubernetes.kubeconfig` to use an explicit kubeconfig file.
* If `kubeconfig` is omitted and the worker runs inside a Kubernetes pod, it uses in-cluster config automatically.
* Otherwise, the worker falls back to the default kubeconfig loading rules and uses the current context.

`namespace` selects the namespace inside the chosen cluster. It defaults to `default` when omitted.

### Pod template

The `pod_template` field accepts standard Kubernetes PodSpec YAML and is the declarative way to configure task pod scheduling, service accounts, image pull secrets, resources, and environment variables.

When using `pod_template`, define a container named `task` to customize the main task container directly. Otherwise, the worker appends its own `task` container to the PodSpec.

Use `valueFrom.secretKeyRef` to inject Kubernetes Secret values into task container environment variables:

```yaml
pod_template:
  serviceAccountName: agent-task-sa
  imagePullSecrets:
    - name: my-registry-creds
  containers:
    - name: task
      resources:
        requests:
          cpu: "2"
          memory: 4Gi
        limits:
          memory: 8Gi
      env:
        - name: GITHUB_TOKEN
          valueFrom:
            secretKeyRef:
              name: my-k8s-secret
              key: github-token
  tolerations:
    - key: "dedicated"
      operator: "Equal"
      value: "agents"
      effect: "NoSchedule"
```

{% hint style="info" %}
The worker Deployment's ServiceAccount is separate from the task Job `serviceAccountName` you configure in `pod_template`. The Deployment ServiceAccount needs RBAC to manage Jobs and Pods. The task ServiceAccount (if any) controls what the agent process can access at runtime.
{% endhint %}

### Preflight check

On startup, the worker creates a short-lived preflight Job to verify that:

* The worker has sufficient RBAC permissions in the target namespace.
* Cluster admission policies (Pod Security Standards, OPA Gatekeeper, Kyverno, etc.) allow the worker's task pod shape.
* The preflight image can be pulled.

If the preflight fails, the worker logs a diagnostic error and exits before accepting any tasks. This surfaces policy and configuration issues at deploy time rather than at task execution time.

The preflight image defaults to `busybox:1.36`. If your cluster restricts allowed registries or images, set `preflight_image` to an allowlisted image. When `imagePullSecrets` is configured in `pod_template`, those secrets apply to the preflight Job as well, so you can point `preflight_image` at an image in your private registry.

### Environment variables for Kubernetes tasks

There are two ways to pass environment variables to Kubernetes task containers:

1. **`pod_template`** (recommended for Kubernetes-native config) — Use standard Kubernetes `env` syntax in the `task` container, including `valueFrom.secretKeyRef` for Kubernetes Secrets.
2. **`-e` / `--env` flags** — Backend-agnostic runtime overrides that work across all backends.

When configuring the Kubernetes backend via YAML or Helm, declarative task-container env belongs in `pod_template` rather than a separate top-level list.

{% hint style="info" %}
If your organization uses an external secrets manager (HashiCorp Vault, AWS Secrets Manager, GCP Secret Manager, etc.), you can inject secrets into task pods via the CSI Secrets Store Driver or a similar operator. Configure the required `volumes`, `volumeMounts`, and annotations in `pod_template` just as you would for any other Kubernetes workload. See your secrets provider's documentation for details.
{% endhint %}

***

## Helm chart

The `oz-agent-worker` repository includes a namespace-scoped Helm chart at `charts/oz-agent-worker`. This is the recommended way to deploy the worker into a Kubernetes cluster.

### What the chart deploys

* A long-lived `Deployment` running `oz-agent-worker` with the Kubernetes backend
* A namespaced `ServiceAccount` for the worker
* A namespaced `Role` / `RoleBinding` with the minimum permissions needed to manage task Jobs and Pods
* A `ConfigMap` containing the worker config YAML
* An optional `Secret` for `WARP_API_KEY` (or a reference to an existing Secret)

The chart does not create CRDs or cluster-scoped RBAC resources.

### Install

```bash
# Clone the worker repository
git clone https://github.com/warpdotdev/oz-agent-worker.git

# Create the namespace
kubectl create namespace warp-oz

# Create a Secret with your API key (if not using an existing Secret)
kubectl create secret generic oz-agent-worker \
  --from-literal=WARP_API_KEY="$WARP_API_KEY" \
  --namespace warp-oz

# Install the chart (replace the image tag with the latest release from the oz-agent-worker repository)
helm install oz-agent-worker ./oz-agent-worker/charts/oz-agent-worker \
  --namespace warp-oz \
  --set worker.workerId=oz-k8s-worker \
  --set image.tag=<version>
```

{% hint style="warning" %}
Set `image.tag` explicitly to pin the worker image. Check the [oz-agent-worker releases](https://github.com/warpdotdev/oz-agent-worker/releases) for the latest version. Do not rely on `latest`.
{% endhint %}

### Key values

**Required:**

* `worker.workerId` — The worker ID (same as `--worker-id`).
* `image.tag` — The worker image tag to deploy.

**Worker configuration:**

* `worker.logLevel` — Log verbosity (`debug`, `info`, `warn`, `error`). Defaults to `info`.
* `worker.cleanup` — Whether to clean up task Jobs after execution. Defaults to `true`.
* `worker.maxConcurrentTasks` — Maximum concurrent tasks. Defaults to `0` (unlimited).
* `worker.idleOnComplete` — Duration to keep the oz process alive after task completion.
* `worker.resources` — Resource requests/limits for the worker Deployment. Defaults to `100m` CPU and `128Mi` memory.
* `worker.livenessProbe` — Liveness probe for the worker Deployment. Defaults to an `exec` probe (`kill -0 1`). Override with a custom probe (e.g., `httpGet` if you add a health endpoint) or set to `null` to disable.
* `worker.nodeSelector`, `worker.tolerations`, `worker.affinity` — Scheduling constraints for the worker Deployment pod.

**Kubernetes backend:**

* `kubernetesBackend.namespace` — Namespace for task Jobs. Defaults to the release namespace.
* `kubernetesBackend.defaultImage` — Default Docker image for task pods when the run has no Warp environment image. Leave empty (default) to fall back to `ubuntu:22.04`.
* `kubernetesBackend.imagePullPolicy` — Image pull policy for task pods. Defaults to `IfNotPresent`.
* `kubernetesBackend.preflightImage` — Image for the startup preflight Job. Set this if your cluster restricts allowed registries.
* `kubernetesBackend.unschedulableTimeout` — How long a pod may remain unschedulable before failing. Defaults to `30s`.
* `kubernetesBackend.setupCommand` — Shell command to run before each task.
* `kubernetesBackend.teardownCommand` — Shell command to run after each task.
* `kubernetesBackend.extraLabels` — Additional labels for task Jobs and Pods.
* `kubernetesBackend.extraAnnotations` — Additional annotations for task Jobs and Pods.
* `kubernetesBackend.activeDeadlineSeconds` — Maximum task Job lifetime.
* `kubernetesBackend.workspaceSizeLimit` — Size limit for workspace `emptyDir` volume.
* `kubernetesBackend.podTemplate` — Raw PodSpec YAML for task Jobs (same as `backend.kubernetes.pod_template` in the config file).

**API key Secret:**

* `warp.apiKeySecret.create` — Set to `true` to have the chart create a Secret from `warp.apiKeySecret.value`. Defaults to `false` (expects a pre-existing Secret).
* `warp.apiKeySecret.value` — The API key value to store in the chart-managed Secret. Only used when `warp.apiKeySecret.create` is `true`.
* `warp.apiKeySecret.name` — Name of the Secret containing `WARP_API_KEY`. Defaults to `oz-agent-worker`.
* `warp.apiKeySecret.key` — Key within the Secret. Defaults to `WARP_API_KEY`.

### Operational notes

* **Scaling**: The chart always deploys a single replica for a given `worker.workerId`. To run multiple workers, deploy multiple Helm releases with distinct worker IDs rather than scaling a single release horizontally.
* **Security context**: The Deployment defaults to a non-root security context (`runAsUser: 10001`) with `allowPrivilegeEscalation: false` and all capabilities dropped.
* **Liveness probe**: The Deployment includes a default `exec` liveness probe (`kill -0 1`). Override `worker.livenessProbe` for a custom probe, or set it to `null` to disable. See [Key values](#key-values) for details.
* **In-cluster auth**: The chart assumes the worker runs inside the target cluster and uses in-cluster Kubernetes auth by default.
* **Root init containers**: The worker Deployment itself is non-root, but task Jobs require a root init container for sidecar materialization. Ensure the task namespace's Pod Security Standards allow this.

***

## Direct backend

The Direct backend runs agent tasks directly on the host machine without Docker or Kubernetes. This is useful when neither Docker nor Kubernetes is available, or when tasks need direct access to host resources.

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
Sidecar images (the `oz` binary and dependencies) are pulled from public registries and do not require authentication.
{% endhint %}

***

## Related resources

* [Self-Hosting](self-hosting.md) — Architecture overview, setup guides, and decision guide
* [Environments](environments.md) — Creating and configuring environments for agent runs
* [Deployment Patterns](deployment-patterns.md) — Common architectures for deploying cloud agents
