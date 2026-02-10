---
description: >-
  Run Oz cloud agents on your own infrastructure while keeping Oz's
  orchestration and observability.
---

# Self-Hosting

{% hint style="info" %}
**Enterprise feature**: Self-hosted Oz cloud agents are available exclusively to teams on an Enterprise plan. To enable self-hosting for your team, [contact sales](https://warp.dev/contact-sales).
{% endhint %}

Self-hosting allows your team to run Oz cloud agent workloads on your own infrastructure instead of Warp-managed servers. This is ideal for enterprises that need code and execution to remain within their network boundary while still benefiting from Oz's orchestration and visibility model.

<figure><img src="../.gitbook/assets/customer-dedicated-saas.png" alt="Self-hosted Oz architecture showing customer-managed execution with Oz orchestration"><figcaption></figcaption></figure>

***

## How it works

With self-hosting:

* **Oz orchestrator** still manages task lifecycle, observability, and the management experience.
* **Execution happens on your infrastructure**. You run a worker process that connects to Oz and claims tasks routed to it.
* **Your team controls the compute**. The worker runs on machines you provision and manage.

This means you get the same orchestration, session sharing, and team visibility features as Warp-hosted execution, but the agent runs inside your network.

***

## Prerequisites

Before setting up a self-hosted worker, ensure you have:

* **A machine to run the worker** — This can be a VM, a server, or even a local machine. Linux is recommended, but macOS is also supported.
* **Docker installed** — The worker uses Docker to run agent tasks. Verify Docker is installed and running with `docker info`.
* **Enterprise plan with self-hosting enabled** — [Contact sales](https://warp.dev/contact-sales) if self-hosting is not yet enabled for your team.
* **A team API key** — In the Warp app, go to `Settings > Platform` to create a team-scoped API key.

***

## Installation

### 1. Install Docker

If Docker is not already installed, follow the [official Docker installation guide](https://docs.docker.com/get-docker/) for your platform.

Verify Docker is running:

```bash
docker info
```

***

## Running the worker

The worker is open source. See the [oz-agent-worker repository](https://github.com/warpdotdev/oz-agent-worker) for additional configuration options and troubleshooting.

### 1. Set your API key

In the Warp app, go to `Settings > Platform` to create a team API key. Then export it as an environment variable:

```bash
export WARP_API_KEY="your_team_api_key"
```

### 2. Start the worker

Run the worker using Docker with a unique identifier:

```bash
docker run -v /var/run/docker.sock:/var/run/docker.sock \
  -e WARP_API_KEY="$WARP_API_KEY" \
  warpdotdev/oz-agent-worker --worker-id "my-worker"
```

The `--worker-id` can be any string that identifies this worker. Choose something meaningful for your team (for example, `prod-runner-1` or `ci-worker`).

Once started, the worker:

* Connects to Oz
* Waits for tasks routed to this worker ID
* Runs tasks locally using Docker
* Reports status and results back to Oz

You can run multiple workers with the same `--worker-id` for redundancy — tasks are distributed across connected workers.

***

## Routing runs to self-hosted workers

To run an Oz cloud agent on your self-hosted worker, specify the `--host` parameter with your worker ID.

### From the CLI

```bash
oz agent run-cloud --prompt "Refactor the authentication module" --host "my-worker"
```

### From integrations

When creating or updating an integration, specify the host:

```bash
oz integration create slack --host "my-worker" ...
oz integration update linear --host "my-worker" ...
```

All tasks created through that integration will be routed to your self-hosted worker.

### From the web UI

When creating a run or schedule in the [Oz web app](https://oz.warp.dev), select your self-hosted worker from the host dropdown.

***

## Monitoring runs

Self-hosted runs have the same observability as Warp-hosted runs:

* **Management UI** — View task status, history, and metadata in the [Oz dashboard](https://oz.warp.dev).
* **Session sharing** — Authorized teammates can attach to running tasks to monitor progress.
* **APIs and SDKs** — Query task history and build monitoring using the [Oz Agent API](https://docs.warp.dev/reference/api-and-sdk/agent).

***

## Troubleshooting

### Worker won't connect

* Verify your API key is correct and has team scope.
* Ensure the machine has outbound internet access to Oz.
* Check that no firewall rules are blocking WebSocket connections.

### Tasks not being picked up

* Confirm the worker is running and connected (check the worker logs).
* Verify the `--host` parameter matches your `--worker-id` exactly.
* Ensure the worker's team matches the team creating the task.

### Task failures

* Check Docker is running: `docker info`
* Review task logs in the Oz dashboard or via session sharing.
* Ensure the worker machine has sufficient resources (CPU, memory, disk).
