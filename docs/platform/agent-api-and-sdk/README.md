# Agent API & SDK

### Agent API

Warp's Public Agent API lets you create and inspect [Ambient Agent](../../ambient-agents/ambient-agents-overview.md) runs over HTTP from any system (CI, cron, backend services, internal tools), without requiring the Warp desktop app.

**With the API you can:**

* Run an agent by submitting a prompt plus optional config (model, environment, MCP servers, base prompt, etc.)
* Monitor execution by listing runs and tracking state transitions over time (queued → in progress → succeeded/failed)
* Inspect results and provenance by fetching a run's full details, including the original prompt, source/creator metadata, session link, and resolved agent configuration

{% hint style="warning" %}
This page is a high-level overview.\
\
For full API endpoint details, please refer to the [**Agents API**](https://docs.warp.dev/platform/agent-api-and-sdk/agent)**.** For schema definitions, see the [**Models reference**](https://docs.warp.dev/platform/agent-api-and-sdk/models).
{% endhint %}

### Agent SDK

Warp provides official [Python](https://github.com/warpdotdev/warp-sdk-python) and [TypeScript](https://github.com/warpdotdev/warp-sdk-typescript) SDKs that wrap the Public Agent API with:

* **Typed requests and responses** (editor autocomplete, fewer schema mistakes)
* **Built-in retries and timeouts** (with per-request overrides)
* **Consistent error type**s that map to API status codes
* **Helpers for raw responses** when you need headers/status or custom parsing

If you’re building an integration (CI, Slack bots, internal tooling, orchestrators), the SDKs are typically the quickest and safest starting point.

{% embed url="https://www.youtube.com/watch?v=0cf7383MZSk" %}

**SDK vs raw REST**

* Use the SDK when you want strong typing, standardized error handling, and easy concurrency patterns.
* Use raw REST when you want minimal dependencies or full control over your HTTP client (the SDKs also support calling undocumented endpoints when needed).

{% hint style="warning" %}
For the full SDK surface area and latest usage, refer to the GitHub repos: [**Python SDK**](https://github.com/warpdotdev/warp-sdk-python) and [**TypeScript SDK**](https://github.com/warpdotdev/warp-sdk-typescript).
{% endhint %}

***

## Agent API

### REST API Base URL

All endpoints are served over HTTPS:

```http
https://app.warp.dev/api/v1
```

### Core Concepts

#### **Agent runs**

An agent run represents a single execution of an Ambient Agent, created with a prompt and optional configuration. Each run has:

* A unique `run_id`
* A human-readable `title`
* A `prompt` that the agent executes
* A `state` (for example `QUEUED`, `INPROGRESS`, `SUCCEEDED`, `FAILED`)
* Timestamps (`created_at`, `updated_at`)
* Optional session information (`session_id`, `session_link`)
* Optional resolved configuration (`agent_config`)

See the [**Agents API**](https://docs.warp.dev/platform/agent-api-and-sdk/agent) for details on how runs are created and listed.

#### **Agent configuration**

You can influence how an agent runs using AmbientAgentConfig, including:

* `name` for traceability and filtering
* `model_id` for LLM selection
* `base_prompt` to shape behavior
* `environment_id` to choose a `CloudEnvironment`
* `mcp_servers` to enable specific tools via MCP

See the [**Models reference**](https://docs.warp.dev/platform/agent-api-and-sdk/models) for the full configuration schema.

***

### Key Endpoints

**The Agents API exposes three primary endpoints:**

*   `POST /agent/run`

    Create a new agent run with a prompt and optional config and title. Returns run\_id and initial state.
*   `GET /agent/runs`

    List runs with pagination and filters for state, config\_name, model\_id, creator, source, and creation time.
*   `GET /agent/runs/{runId}`

    Fetch full details for a single run, including session link and resolved configuration.

All endpoint semantics, query parameters, and error codes are documented on the [Agents API](https://docs.warp.dev/platform/agent-api-and-sdk/agent).

***

#### Models Reference

The API shares a set of reusable models across endpoints. Detailed JSON schemas, types, and enums are documented on the [Models reference](https://docs.warp.dev/platform/agent-api-and-sdk/models), including:

* `RunAgentRequest`
* `RunAgentResponse`
* `ListRunsResponse`
* `RunItem`
* `PageInfo`
* `RunStatusMessage`
* `RunCreatorInfo`
* `RunState`
* `RunSourceType`
* `AmbientAgentConfig`
* `MCPServerConfig`
* `Error`

***

## Agent SDKs

### Python SDK

The Python SDK is the recommended way to call the Agent API from Python services and scripts. It provides:

* Sync + async clients
* Typed request/response models
* Configurable retries/timeouts and structured errors

See the [**Python SDK GitHub repo**](https://github.com/warpdotdev/warp-sdk-python) for installation, full API reference (api.md), and up-to-date examples.

### TypeScript SDK

The TypeScript SDK is the recommended way to call the Agent API from Node.js services and modern TS/JS runtimes. It provides:

* Fully typed params/responses
* First-class error handling, retries/timeouts
* Support across common runtimes where fetch is available or polyfilled

See the [**TypeScript SDK GitHub repo**](https://github.com/warpdotdev/warp-sdk-typescript) for installation, full API reference (api.md), and up-to-date examples.
