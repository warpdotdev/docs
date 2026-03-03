---
description: >-
  Technical reference documentation for the Oz CLI, API, and SDK.
---

# API Reference

This section covers the programmatic interfaces for running and managing Oz agents in CI pipelines, scripts, backend services, and custom tooling.

## CLI

The [Oz CLI](cli/README.md) lets you run and configure agents from any environment — locally, in CI pipelines, or on remote machines.

- [API Keys](cli/api-keys.md) - Create and manage API keys to authenticate the Oz CLI without human interaction, ideal for CI pipelines, headless servers, and containers.
- [Agent Profiles](cli/agent-profiles.md) - Use agent profiles to control what the agent can access, how it behaves, and where it can act, including file access, command execution, and MCP server usage.
- [MCP Servers](cli/mcp-servers.md) - Pass MCP server configuration to agent runs using the `--mcp` flag, by UUID, inline JSON, or file path.
- [Skills](cli/skills.md) - Run agents from reusable instruction sets stored in your repositories using the `--skill` flag.
- [Warp Drive Context](cli/warp-drive.md) - Reference saved prompts, notebooks, workflows, and rules from Warp Drive directly in CLI agent commands.
- [Integration Setup](cli/integration-setup.md) - Configure environments and connect external tools like Slack and Linear so you can trigger Oz agents from outside the terminal.
- [Troubleshooting](cli/troubleshooting.md) - Find solutions to common CLI errors, including authentication issues, agent failures, environment problems, and Docker image issues.

## API & SDK

The [Oz Agent API](https://docs.warp.dev/reference/api-and-sdk/agent) lets you create and monitor cloud agent runs over HTTP. Official SDKs for [Python](https://github.com/warpdotdev/oz-sdk-python) and [TypeScript](https://github.com/warpdotdev/oz-sdk-typescript) provide typed clients with built-in retries and error handling.

- [Demo: Sentry monitoring with SDK](api-and-sdk/demo-sentry-monitoring-with-sdk.md) - example integration
