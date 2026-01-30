---
description: >-
  Learn how to configure MCP servers in Warp to let ambient agents securely call
  external tools, local services, and internal APIs using the MCP JSON standard.
---

# MCP Servers for Agents

Ambient Agents in Warp can call external tools through [Model Context Protocol (MCP) servers](https://docs.warp.dev/knowledge-and-collaboration/mcp). This enables agents to extend their capabilities beyond the terminal and interact with systems such as GitHub, dbt, or custom internal services.

Warp currently supports the [**MCP JSON configuration standard**](https://gofastmcp.com/integrations/mcp-json-configuration), either inline or via file. This guide explains how to define, load, validate, and troubleshoot MCP configurations when running an Ambient Agent.

***

### When to Use MCP Servers

Use an MCP server when your agent needs access to:

* External tools or APIs wrapped behind an MCP interface
* Local processes that expose MCP endpoints
* Internal developer tools that you want integrated into your ambient workflows

Agents call MCP tools automatically whenever their workflow requires them.

#### 1. Inline JSON

You can pass the full MCP JSON object directly into the `--mcp` flag:

```shellscript
warp agent run \
  --mcp '{"mymcp": { "url": "https://fakemcp.com/mcp" }}' \
  -p "Call the MCP tool"
```

Warp interprets the entire argument as the configuration map for all MCP servers.

#### 2. File Path

Instead of embedding JSON inline, you may supply a path:

```shellscript
warp agent run --mcp ./my-mcp-config.json
```

The file must contain a valid MCP JSON structure as defined by the specification.

### MCP Configuration Schema

Warp accepts any MCP JSON matching the published standard. A typical configuration defines one or more servers:

```json
{
  "github": {
    "url": "https://mcp.example.com/github"
  },
  "dbt": {
    "command": "uvx",
    "args": ["dbt-mcp"],
    "env": {
      "DBT_HOST": "https://example.us1.dbt.com",
      "DBT_SERVICE_TOKEN": "${DBT_SERVICE_TOKEN}"
    }
  }
}
```

Or in YAML:

```yaml
mcp_servers:
  github:
    url: https://mcp.example.com/github
  dbt:
    command: uvx
    args:
      - dbt-mcp
    env:
      DBT_HOST: https://example.us1.dbt.com
      DBT_SERVICE_TOKEN: ${DBT_SERVICE_TOKEN}
```

#### Supported Fields

* `url` – Direct URL to an MCP server endpoint
* `command / args` – Defines a local executable to launch an MCP server
* `env` – Environment variables passed to the command

You may define any number of MCP servers.

If the agent config includes an `mcp_servers` field, it overrides the defaults (empty set).

### Using MCP Servers in a Full Agent Config

Developers typically declare MCP servers inside the broader agent config file (e.g. `warp-agent.json` or `.yaml`). Example:

```json
{
  "name": "my-production-agent",
  "model_id": "claude-4-5-sonnet",
  "system_prompt": "You are a helpful assistant focused on backend development.",
  "environment_id": "SVhg783GBFQHk1OfdPfFU9",
  "mcp_servers": {
    "github": {
      "url": "https://mcp.example.com/github"
    },
    "dbt": {
      "command": "uvx",
      "args": ["dbt-mcp"],
      "env": {
        "DBT_HOST": "https://example.us1.dbt.com",
        "DBT_SERVICE_TOKEN": "${DBT_SERVICE_TOKEN}"
      }
    }
  }
}
```

This file can be passed as the agent’s config file or referenced through `config_file` when creating tasks via API.

### Requirements and Defaults

#### Required

* MCP configuration must follow the MCP JSON specification
* Inline or file-based config must be valid JSON (or YAML inside the agent config)

#### Defaults

* If `mcp_servers` is omitted, the agent runs with no MCP servers enabled.
* MCP permissions default to **allowing calls**, but may inherit profile settings depending on the user’s environment. This default behavior is evolving as Warp plans to phase out profiles for ambient agents.
