---
description: >-
  Technical reference documentation for the Warp CLI, API, and SDK.
---

# API Reference

This section covers the programmatic interfaces for running and managing Warp agents in CI pipelines, scripts, backend services, and custom tooling.

## CLI

The [Warp CLI](cli/README.md) runs agents in non-interactive mode from any environment.

- [Integrations and Environments](cli/integrations-and-environments.md) - configure execution contexts and connect external systems
- [MCP Servers for Cloud Agents](cli/mcp-servers-for-cloud-agents.md) - extend agent capabilities with external tools
- [Troubleshooting](cli/troubleshooting.md) - common issues and solutions

## API & SDK

The [Agent API](https://docs.warp.dev/reference/api-and-sdk/agent) lets you create and monitor Ambient Agent runs over HTTP. Official SDKs for [Python](https://github.com/warpdotdev/warp-sdk-python) and [TypeScript](https://github.com/warpdotdev/warp-sdk-typescript) provide typed clients with built-in retries and error handling.

- [Demo: Sentry monitoring with SDK](api-and-sdk/demo-sentry-monitoring-with-sdk.md) - example integration
