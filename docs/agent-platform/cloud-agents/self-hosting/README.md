---
description: >-
  Run Oz cloud agents on your own infrastructure. Choose between a managed
  worker daemon orchestrated by Oz or unmanaged CLI-based execution you
  control.
---

# Self-hosting

Self-hosting lets your team run Oz cloud agent workloads on your own infrastructure instead of Warp-managed servers. You control the execution environment, compute resources, and network access. Repositories are cloned and stored only on your machines, and agents can reach services behind your VPN or firewall.

**New to self-hosting?** Start with the [Self-hosting quickstart](quickstart.md) to get a managed worker running on Docker in under 10 minutes.

**Want a CLI-only path with no Docker requirement?** Jump straight to the [Unmanaged quickstart](unmanaged.md#unmanaged-quickstart) to run `oz agent run` directly on any host.

{% hint style="info" %}
**Enterprise feature**: Self-hosted Oz agents are available exclusively to teams on an Enterprise plan. To enable self-hosting for your team, [contact sales](https://warp.dev/contact-sales).
{% endhint %}

## Managed vs unmanaged

Self-hosting has two architectures. The core distinction is **who orchestrates agent runs** — not who owns the compute. Both models keep code and execution on your infrastructure.

* **Managed** — Oz orchestrates agent runs. You run the `oz-agent-worker` daemon on your infrastructure; it connects to Oz and waits for work. Slack mentions, Linear comments, schedules, API calls, and `oz agent run-cloud` commands all route tasks to your worker, which executes them in isolated Docker containers, Kubernetes Jobs, or directly on the host. Similar to a [GitHub self-hosted runner](https://docs.github.com/en/actions/hosting-your-own-runners).
* **Unmanaged** — You orchestrate agent runs. You invoke `oz agent run` directly from your existing CI pipeline, Kubernetes pod, VM, or dev box. Oz provides session tracking and observability for each run, but does not start or stop agents for you.

### At a glance

| Aspect | **Managed** | **Unmanaged** |
| --- | --- | --- |
| **Who triggers runs** | Oz (Slack, Linear, schedules, API, `run-cloud`) | Your system (CI, cron, scripts) |
| **What runs on your infra** | Long-lived `oz-agent-worker` daemon | One-shot `oz agent run` invocations |
| **OS support** | Linux (macOS/Windows coming) | Linux, macOS, Windows |
| **Execution isolation** | Docker container, Kubernetes Job, or direct host | Whatever your host provides |
| **Automatic environment setup** | Yes (via Warp [environments](../environments.md)) | No (you manage it) |
| **Session tracking and steering** | Yes | Yes |

The two architectures are not mutually exclusive. Some teams run managed workers for integration-triggered work and unmanaged agents in CI pipelines.

## How self-hosting works

Warp uses a split-plane architecture: **execution happens on your infrastructure**, while **orchestration, session management, and LLM inference route through Warp's backend**. Agent interactions — including code context in session transcripts and LLM prompts — transit Warp's control plane under [Zero Data Retention (ZDR)](https://docs.warp.dev/enterprise/security-and-compliance/security-overview#zero-data-retention-zdr) agreements. Warp does not persistently store your source code or train on it.

<figure><img src="../../.gitbook/assets/customer-dedicated-saas.png" alt="Self-hosted Oz architecture showing customer-managed execution with Oz orchestration"><figcaption></figcaption></figure>

With any self-hosted architecture:

* **Agent runs are tracked and steerable** — View status, metadata, and session transcripts in the [Oz dashboard](https://oz.warp.dev), the Warp app, or via the [API/SDK](https://docs.warp.dev/reference/api-and-sdk/agent). Authorized teammates can attach to running sessions to monitor or steer agents.
* **Connectivity to Warp's backend is required** — Agents need outbound access to Warp for orchestration, session storage, and LLM inference. No inbound ports need to be opened.
* **Resource limits are controlled by your infrastructure** — Concurrency and compute are only limited by the machines you provision, not by Warp.

{% hint style="info" %}
Enterprise teams that need full control over LLM inference routing can use [Bring Your Own LLM (BYOLLM)](https://docs.warp.dev/enterprise/enterprise-features/bring-your-own-llm) to route inference through their own cloud provider accounts. BYOLLM currently applies to interactive (local) agents; cloud agent support is coming.
{% endhint %}

***

## Choosing an architecture

{% hint style="warning" %}
**OS support:** The managed architecture is **Linux-only** today (macOS and Windows support is coming). If you need agents to run on macOS or Windows, use the [unmanaged](unmanaged.md) architecture, which works on any platform Warp supports.
{% endhint %}

Use these questions to decide between managed and unmanaged:

1. **Do you need agents to run on Windows or macOS?**
   * Yes → Use the [unmanaged](unmanaged.md) architecture. Managed is Linux-only today.
   * No, Linux works → Continue to the next question.
2. **Do you want Oz to handle starting and stopping agents** (from Slack, the web interface, the Warp app, schedules, or the API)?
   * Yes → Use the [managed](#managed-architecture) architecture.
   * No, you have your own triggering mechanism → Use the [unmanaged](unmanaged.md) architecture.
3. **Can your development environment run in a Docker container or Kubernetes pod?**
   * Yes, Docker → [Managed: Docker](managed-docker.md) backend.
   * Yes, Kubernetes → [Managed: Kubernetes](managed-kubernetes.md) backend.
   * No (multi-service stacks that don't fit a single container, or environments where container runtimes aren't available) → [Unmanaged](unmanaged.md) or [Managed: Direct](managed-direct.md).
4. **Do you have your own orchestrator** (CI/CD, Kubernetes, internal job scheduler) **that starts agents on demand?**
   * Yes → [Unmanaged](unmanaged.md), using `oz agent run` as a drop-in.
   * No → [Managed](#managed-architecture).

### Choosing a managed backend

The managed architecture supports three backends for task execution:

1. **Are you deploying the worker into a Kubernetes cluster?**
   * Yes → Use the [Kubernetes backend](managed-kubernetes.md). Each task runs as a Kubernetes Job in your cluster; install with the included Helm chart.
   * No → Continue.
2. **Is Docker available on your worker host?**
   * Yes → Use the [Docker backend](managed-docker.md) (default). Tasks run in isolated containers.
   * No → Use the [Direct backend](managed-direct.md). Tasks run directly on the host.
3. **Do you need container-level isolation between tasks?**
   * Yes → [Docker](managed-docker.md) or [Kubernetes](managed-kubernetes.md) backend.
   * No → Any backend works.
4. **Do you need Kubernetes-native scheduling, resource management, or policy enforcement?**
   * Yes → [Kubernetes backend](managed-kubernetes.md).
   * No → [Docker](managed-docker.md) or [Direct](managed-direct.md) is simpler to set up.

***

## Managed architecture

With the managed architecture, you run the `oz-agent-worker` daemon on your infrastructure. The daemon connects to Oz's backend, waits for tasks to be assigned to it, and executes those tasks on its host using one of three backends:

* **[Docker backend](managed-docker.md)** (default) — Runs each task in an isolated Docker container.
* **[Kubernetes backend](managed-kubernetes.md)** — Runs each task as a Kubernetes Job in your cluster.
* **[Direct backend](managed-direct.md)** — Runs each task directly on the host without a container runtime.

The managed architecture enables full orchestration by Oz — it can remotely start agents via Slack, Linear, the [Oz web app](https://oz.warp.dev), the API/SDK, and the `oz agent run-cloud` command. Agents can access host resources through volume mounts (Docker), Kubernetes-native configuration (Kubernetes), and injected environment variables.

## Unmanaged architecture

With the [unmanaged architecture](unmanaged.md), you run `oz agent run` inside your own orchestrator or dev environment. This works on any platform Warp supports (Linux, macOS, Windows), with no dependency on Docker or any other sandboxing platform.

You're responsible for executing `oz agent run` on your infrastructure — similar to how you'd integrate Claude Code or Codex CLI. The agent runs directly on the host, which could itself be a Kubernetes pod, VM, container, or CI runner.

***

## Routing runs to self-hosted workers

This section applies to **all managed backends** (Docker, Kubernetes, and Direct). Once a worker is connected, route Oz cloud agent runs to it by specifying the `--host` flag (or equivalent) with your worker ID. The `--host` value must match the `--worker-id` of a connected worker exactly.

{% hint style="info" %}
Unmanaged runs don't need routing — you invoke `oz agent run` directly on the host where you want the agent to execute. Routing is only relevant for managed workers.
{% endhint %}

### From the CLI

```bash
oz agent run-cloud --prompt "Refactor the authentication module" --host "my-worker"
```

You can combine `--host` with any other `run-cloud` flags, such as `--environment`, `--model`, `--mcp`, `--skill`, `--computer-use`, and `--attach`.

### From scheduled agents

When creating or updating a schedule, specify the host:

```bash
oz schedule create --name "daily-cleanup" \
  --cron "0 9 * * *" \
  --prompt "Run dead code cleanup" \
  --environment ENV_ID \
  --host "my-worker"

oz schedule update SCHEDULE_ID --host "my-worker"
```

### From integrations

When creating or updating an integration, specify the host:

```bash
oz integration create slack --host "my-worker" ...
oz integration update linear --host "my-worker" ...
```

All tasks created through that integration route to your self-hosted worker.

### From the API and SDKs

When creating a run via the [Oz API](https://docs.warp.dev/reference/api-and-sdk/agent), include `worker_host` in the config:

```bash
curl -X POST https://app.warp.dev/api/v1/agent/run \
  --header 'Authorization: Bearer YOUR_API_KEY' \
  --header 'Content-Type: application/json' \
  --data '{
    "prompt": "Refactor the authentication module",
    "config": {
      "environment_id": "ENV_ID",
      "worker_host": "my-worker"
    }
  }'
```

### From the web UI

When creating a run, schedule, or integration in the [Oz web app](https://oz.warp.dev), select your self-hosted worker from the host dropdown.

***

## Environments with self-hosted workers

Self-hosted workers fully support [environments](../environments.md). When a task specifies an environment, the worker resolves the Docker image, clones the repositories, runs setup commands, and executes the agent inside the prepared container or Kubernetes Job.

The same environment can be used for both Warp-hosted and self-hosted runs without modification. See [Environments](../environments.md) for details on creating and configuring them.

{% hint style="info" %}
With the Kubernetes backend, setting a [`default_image`](reference.md#kubernetes-backend-config) on the worker lets you skip creating a Warp environment when all your tasks use the same base image.
{% endhint %}

{% hint style="warning" %}
Musl-based Docker images (such as Alpine Linux) are not supported as task images. The agent runtime requires glibc. Use glibc-based images like Debian, Ubuntu, or the default (non-Alpine) variants of official Docker Hub images.
{% endhint %}

## Monitoring runs

Self-hosted runs have the same observability as Warp-hosted runs:

* **Oz dashboard** — View task status, history, and metadata at [oz.warp.dev](https://oz.warp.dev).
* **Session sharing** — Authorized teammates can attach to running tasks to monitor progress.
* **APIs and SDKs** — Query task history and build monitoring using the [Oz API](https://docs.warp.dev/reference/api-and-sdk/agent).

For infrastructure-level observability, the `oz-agent-worker` daemon can export OpenTelemetry metrics (worker health, task throughput, capacity saturation) to Prometheus, an OTLP collector, or the console. See [Monitoring](monitoring.md) for setup, the full metric catalog, and sample PromQL queries.

***

## Related pages

* [Self-hosting quickstart](quickstart.md) — Get a managed worker running in ~10 minutes.
* [Unmanaged](unmanaged.md) — Run `oz agent run` in your CI, K8s, or dev environment.
* [Managed: Docker](managed-docker.md) — Default managed setup with the Docker backend.
* [Managed: Kubernetes](managed-kubernetes.md) — Managed setup with the Kubernetes backend and Helm chart.
* [Managed: Direct](managed-direct.md) — Managed setup with no container runtime.
* [Self-hosted worker reference](reference.md) — CLI flags and config file schema.
* [Monitoring](monitoring.md) — OpenTelemetry metrics for worker health, task throughput, and capacity.
* [Security and networking](security-and-networking.md) — Data boundaries, network egress, and security considerations.
* [Troubleshooting](troubleshooting.md) — Worker won't start, tasks not picked up, and other common issues.
* [Deployment patterns](../deployment-patterns.md) — How self-hosting compares to CLI-only and Warp-hosted deployment.
* [Environments](../environments.md) — Define the runtime context for agent tasks.
