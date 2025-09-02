---
description: >-
  Extend Warp’s agents with custom tools and data sources using MCP servers —
  modular plugins powered by a standardized interface.
---

# Model Context Protocol

## Model Context Protocol (MCP)

MCP servers extend Warp’s [agents](../agents/using-agents/) in a modular, flexible way by exposing custom tools or data sources through a standardized interface — essentially acting as plugins for Warp.

MCP is an open source protocol. Check out the official [MCP documentation](https://modelcontextprotocol.io/introduction) for more detailed information on how this protocol is engineered.

### How to access MCP Server settings

You can navigate to the MCP servers page in any of the following ways:

* From [Warp Drive](warp-drive/): under `Personal > MCP Servers`
* From the [Command Palette](../terminal/command-palette.md): search for `Open MCP Servers`
* From the settings tab: `Settings > AI > Manage MCP servers`

This will show a list of all configured MCP servers, including which are currently running. If you close Warp with an MCP server running, it will run again on next start of Warp. MCP servers that are stopped will remain so on next launch of Warp.

<figure><img src="../.gitbook/assets/mcp-running.png" alt=""><figcaption><p>MCP servers page</p></figcaption></figure>

### Adding an MCP Server

To add a new MCP server, you can click the `+ Add` button. MCP server types you can add:

{% tabs %}
{% tab title="CLI Server (Command)" %}
Provide a startup command. Warp will launch this command when starting up and shut it down on exit.

<figure><img src="../.gitbook/assets/mcp-add-server-json.png" alt=""><figcaption><p>Adding a CLI MCP Server (Command)</p></figcaption></figure>

{% hint style="info" %}
Always set `working_directory` explicitly when your MCP server command or args include relative paths. This ensures consistent and predictable behavior across machines and sessions.
{% endhint %}

**CLI Server (Command) MCP Configuration Properties**

| Property            | Type      | Required | Description                                                                         |
| ------------------- | --------- | -------- | ----------------------------------------------------------------------------------- |
| `command`           | string    | Yes      | The executable to launch (e.g., `npx`).                                             |
| `args`              | string\[] | Yes      | Array of command-line arguments passed to `command` (e.g., module name, paths).     |
| `env`               | object    | No       | Key-value object of environment variables (e.g., tokens).                           |
| `working_directory` | string    | No       | Working directory path where the command is run, used for resolving relative paths. |
{% endtab %}

{% tab title="SSE Server (URL)" %}
Provide a URL where Warp can reach an already-running MCP server that supports Server-Sent Events.

<figure><img src="../.gitbook/assets/mcp-sse-json.png" alt=""><figcaption><p>Adding an SSE MCP Server (URL)</p></figcaption></figure>

**SSE Server (URL) MCP Configuration Properties**

| Property | Type   | Required | Description                                                                    |
| -------- | ------ | -------- | ------------------------------------------------------------------------------ |
| `url`    | string | Yes      | The HTTP endpoint URL to connect to via Server-Sent Events (SSE).              |
| `env`    | object | No       | Optional key-value object for environment variables or headers (e.g., tokens). |
{% endtab %}
{% endtabs %}

### Adding multiple MCP Servers

Warp supports configuring **multiple MCP servers** using a JSON snippet. Each entry under `mcpServers` is keyed by a unique name (`filesystem`, `github`, `notes`, etc). All servers defined in the example are added automatically — no manual setup required.

To add a multiple MCP servers, you can click the `+ Add` button then paste in a JSON snippet like the example below:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/allowed/files"]
    },
    "notes": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-notes", "--notes-dir", "/Users/you/Documents/notes"]
    },
    "externalDocs": {
      "url": "http://localhost:4000/mcp/stream"
    }
  }
}
```

### Managing MCP servers

After MCP servers are registered in Warp, you can **Start** or **Stop** them from the MCP servers page. Each running server will have a list of available tools and resources.

You can rename and edit a server's name, as well as delete the server. To prevent Warp from automatically starting a server when you open Warp, set the `"start_on_launch"` value to `false` in the server's JSON configuration.

### Debugging MCP

If you're having trouble with an MCP server, you can check the logs for any errors or messages to help you diagnose the problem by clicking the `View Logs` button on a server from the MCP servers page.

{% hint style="warning" %}
If you choose to share your MCP server logs with anybody, **make sure to remove any sensitive information before sharing**, as they may contain API keys.

Many SSE based MCP servers will state that your URL should be treated like a password, and can be used with no additional authentication.
{% endhint %}

{% hint style="info" %}
Tip: We've noticed that some models often work better with MCP servers than others. If you're having trouble calling or using an MCP server, try using a different model.
{% endhint %}

#### Debugging MCP Authentication issues

In some cases you may need to reset the auth token for some MCP servers. To do this delete the local mcp auth files by running the following: `rm -rf ~/.mcp-auth`

{% hint style="warning" %}
Note this will delete all your MCP auth tokens stored locally so you will need to login and re-authenticate.
{% endhint %}

If the above doesn't help and you need to reset or change authentication, you may need to switch to a CLI-based MCP server configuration and provide the token via environment variables. See [Sentry CLI MCP Example](mcp.md#sentry).

### Where MCP Logs Are Stored

Warp saves the MCP logs locally on your computer. You can open the files directly and inspect the full contents in the following location:

{% tabs %}
{% tab title="macOS" %}
```bash
cd "$HOME/Library/Application Support/dev.warp.Warp-Stable/mcp"
```
{% endtab %}

{% tab title="Windows" %}
```powershell
Set-Location $env:LOCALAPPDATA\warp\Warp\data\logs\mcp
```
{% endtab %}

{% tab title="Linux" %}
```bash
cd "${XDG_STATE_HOME:-$HOME/.local/state}/warp-terminal/mcp"
```
{% endtab %}
{% endtabs %}

### MCP Server Configuration Examples

Below are examples for popular Model Context Protocol (MCP) servers, presented in tabs with:

* **CLI Server (Command)** — local `npx` launches (requires MCP package and API credentials).
* **SSE Server (URL)** — remote-hosted MCP endpoint.

**🔧 Engineering & Ops Tools**

{% tabs %}
{% tab title="GitHub" %}
[GitHub MCP Docs](https://github.com/github/github-mcp-server)

#### **GitHub CLI Server (Command)**

```json
{
  "GitHub": {
    "command": "docker",
    "args": ["run","-i","--rm","-e","GITHUB_PERSONAL_ACCESS_TOKEN","ghcr.io/github/github-mcp-server"],
    "env": {
      "GITHUB_PERSONAL_ACCESS_TOKEN": "<your_github_token>"
    }
  }
}
```

#### **GitHub SSE Server (URL)**

```json
{
  "GitHub": {
    "url": "https://api.githubcopilot.com/mcp/"
  }
}
```
{% endtab %}

{% tab title="Sentry" %}
[Sentry MCP Docs](https://docs.sentry.io/product/sentry-mcp/)

#### **Sentry CLI Server (Command)**

```json
{
  "Sentry": {
    "command": "npx",
    "args": ["-y","mcp-remote@latest","https://mcp.sentry.dev/mcp"]
  }
}
```

#### **Sentry SSE Server (URL)**

```json
{
  "Sentry": {
    "url": "https://mcp.sentry.dev/sse"
  }
}
```
{% endtab %}

{% tab title="Grafana" %}
[Grafana MCP Docs](https://github.com/grafana/mcp-grafana)

#### **Grafana CLI Server (Command)**

```json
{
  "Grafana": {
    "command": "docker",
    "args": ["run","--rm","-i","-e","GRAFANA_URL","-e","GRAFANA_API_KEY","mcp/grafana","-t","stdio","-debug"],
    "env": {
      "GRAFANA_URL": "http://localhost:3000",
      "GRAFANA_API_KEY": "<your_grafana_key>"
    }
  }
}
```

#### **Grafana SSE Server (URL)**

```json
{
  "Grafana": {
    "url": "https://your-mcp-host.com/api/mcp/grafana/sse"
  }
}
```
{% endtab %}

{% tab title="Linear" %}
[Linear MCP Docs](https://linear.app/docs/mcp)

#### **Linear CLI Server (Command)**

```json
{
  "Linear": {
    "command": "npx",
    "args": ["-y","mcp-remote","https://mcp.linear.app/sse"]
  }
}
```

#### **Linear SSE Server (URL)**

```json
{
  "Linear": {
    "url": "https://mcp.linear.app/sse"
  }
}
```
{% endtab %}
{% endtabs %}

**💬 Collaboration & Design Tools**

{% tabs %}
{% tab title="Atlassian" %}
[Atlassian MCP Docs](https://support.atlassian.com/rovo/docs/setting-up-ides/)

#### **Atlassian CLI Server (Command)**

```json
{
  "Atlassian": {
    "command": "npx",
    "args": ["-y", "mcp-remote", "https://mcp.atlassian.com/v1/sse"]
  }
}
```
{% endtab %}

{% tab title="Notion" %}
[Notion MCP Docs](https://notion.notion.site/Beta-Overview-Notion-MCP-206efdeead058060a59bf2c14202bd0a)

#### **Notion CLI Server (Command)**

```json
{
  "Notion": {
    "command": "npx",
    "args": ["-y", "mcp-remote", "https://mcp.notion.com/mcp"]
  }
}
```

#### **Notion SSE Server (URL)**

```json
{
  "Notion": {
    "url": "https://mcp.notion.com/sse"
  }
}
```
{% endtab %}

{% tab title="Slack" %}
[Slack MCP Docs](https://github.com/korotovsky/slack-mcp-server/)

#### **Slack CLI Server (Command)**

```json
{
  "Slack": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-slack"],
    "env": {
      "SLACK_BOT_TOKEN": "xoxb-<your-bot-token>",
      "SLACK_APP_TOKEN": "xapp-<your-app-token>",
      "SLACK_TEAM_ID": "T<your_workspace_id>",
      "SLACK_CHANNEL_IDS": "<your_channel_id-1>, <your_channel_id-2>",
      "MCP_MODE": "stdio"
    }
  }
}
```

#### **Slack SSE Server (URL)**

```json
{
  "Slack": {
    "url": "https://your-mcp-host.com/api/mcp/slack/sse"
  }
}
```
{% endtab %}

{% tab title="Figma" %}
#### **Official Figma SSE Server (URL)**

1. Enable the Official Figma MCP Server. [Figma MCP Docs](https://help.figma.com/hc/en-us/articles/32132100833559-Guide-to-the-Dev-Mode-MCP-Server)
2. Open the [Figma desktop app](https://www.figma.com/downloads/) and make sure you’ve [updated to the latest version](https://help.figma.com/hc/en-us/articles/5601429983767-Guide-to-the-Figma-desktop-app#h_01HE5QD60DG6FEEDTZVJYM82QW).
3. Create or open a Figma Design file.
4. In the upper-left corner, open the Figma menu.
5. Under **Preferences**, select **Enable local MCP Server**.
6. Enter the following configuration into Warp > Warp Drive > MCP Servers > +.

```json
{
  "Official Figma MCP (SSE)": {
    "url": "http://localhost:3845/sse"
  }
}
```

#### **3rd Party Figma CLI Server (Command)**

1. Download and run the 3rd party Figma Context MCP server. [Figma-Context-MCP](https://github.com/GLips/Figma-Context-MCP)
2. Generate a token with full read-only access in Figma > Settings > Security > Personal Access Token. [See steps](https://www.warp.dev/university/mcp/using-the-figma-mcp-server-to-code-designs)
3. Enter the following configuration into Warp > Warp Drive > MCP Servers > +.

```json
{
 "3rd Party Figma Context MCP (CLI)": {
   "command": "npx",
   "args": [
     "-y",
     "figma-developer-mcp",
     "--stdio"
     ],
     "env": {
       "FIGMA_API_KEY": "<YOUR_FIGMA_TOKEN>"
    }
  }
}
```
{% endtab %}
{% endtabs %}
