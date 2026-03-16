---
description: >-
  Set up and run your first cloud agent via the Oz CLI in less than 5 minutes.
---

# Quick Start

This guide walks you through the essentials to get up and running with the Oz CLI in less than 5 minutes: installing the CLI, authenticating, running your first local agent, and optionally connecting MCP servers to give the agent access to external tools.

## 1. Install the CLI

If you already have the [Warp desktop app installed](https://docs.warp.dev/getting-started/quickstart/installation-and-setup), the **CLI is included** and available in Warp.

If not, see [Installing the CLI](README.md#installing-the-cli) for installation options for all platforms.

## 2. Authenticate

For local development and first-time setup, authenticate interactively using the `oz login` command. Use the appropriate command name based on your installation method. For command names, refer to the table in [Running the CLI](README.md#running-the-cli).

**For example, on macOS:**

```sh
oz login
```

This command prints a sign-in URL in your terminal. Open the URL in your browser to login to Warp. Your credentials will be stored securely for future CLI use.

Interactive login works on both **local** and **remote** machines, and does not require API keys.

## 3. Run an agent

From any directory, run:

```sh
oz agent run --prompt "summarize this directory"
```

This uses the default agent profile, loads any available MCP servers, and executes the run locally. The output appears directly in your terminal.

What happens:

* The agent runs locally in your current working directory.
* The session is tracked on Warp's backend for observability and collaboration.
* The agent autonomously executes commands and streams output to your terminal.

## 4. Add MCP context (optional)

You can connect MCP servers to give the agent access to external tools like GitHub or Linear. Pass MCP configuration inline or from a file using the `--mcp` flag:

```sh
oz agent run --mcp '{"github": {"url": "https://api.githubcopilot.com/mcp/"}}' --prompt "Open a pull request that fixes TODOs in this repo"
```

See [MCP Servers](mcp-servers.md) for all supported formats, including UUID references and multi-server configurations.

## 5. Next steps

Once you've successfully set up and ran your agent, explore other configurations and workflows with the Oz CLI:

* Customize behavior with [agent profiles](agent-profiles.md).
* [Reuse prompts](warp-drive.md) with `--saved-prompt`.
* Connect agents to external systems using [MCP Servers](mcp-servers.md).
* Authenticate with [API keys](api-keys.md) for automated environments or workflows.
* Get up-to-date information about the Oz CLI using the [`oz help` command](troubleshooting.md#getting-help).

{% hint style="info" %}
**Ready for cloud agents?** This quickstart is focused on local runs. For automated workflows with consistent environments, scheduled tasks, and integrations, see the [Cloud Agents Quick Start](https://docs.warp.dev/agent-platform/cloud-agents/quickstart).
{% endhint %}

Continue reading the [Oz CLI reference](README.md) to learn how to install the CLI on different platforms, authenticate in different environments, and configure agents for real-world workflows.
