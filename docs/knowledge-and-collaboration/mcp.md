---
description: How to use Model Context Protocol (MCP) servers in Warp
---

# Model Context Protocol

## Model Context Protocol (MCP)

Model Context Protocol (MCP) servers expose data sources or tools to Warp's [Agent Mode](../agents/warp-ai/agent-mode.md) through a standardized interface — essentially acting like plugins for Warp. This allows you to extend the Agent's capabilities in a modular, flexible way.

MCP is an open source protocol. Check out the official [MCP documentation](https://modelcontextprotocol.io/introduction) for more detailed information on how this protocol is engineered.

In these docs, we'll focus on how to use MCP servers in Warp.

### How to access MCP Server settings

You can navigate to the MCP servers page in any of the following ways:

* From [Warp Drive](warp-drive/), under `Personal > MCP Servers`.
* From the [Command Palette](../terminal/command-palette.md), search for `Open MCP Servers`.
* From `Settings > AI > Manage MCP servers`.

Now, you should see a list of all the MCP servers you have added in Warp, including which servers are currently running.

<figure><img src="../.gitbook/assets/mcp-running.png" alt=""><figcaption><p>MCP servers page</p></figcaption></figure>

### Adding an MCP Server

To add a new MCP server, you can click the `+ Add` button. There are two types of MCP servers you can add:

* CLI Server (Command)
  * If you provide a startup command, Warp will execute this command on start and handle stopping the server when Warp shuts down.
* SSE (URL)
  * Warp will expect a valid MCP server to be listening at the provided URL.

<figure><img src="../.gitbook/assets/mcp-add-server-json.png" alt=""><figcaption><p>Adding a CLI MCP Server (Command)</p></figcaption></figure>

<figure><img src="../.gitbook/assets/mcp-sse-json.png" alt=""><figcaption><p>Adding an SSE MCP Server (URL)</p></figcaption></figure>

### Managing MCP servers

After MCP servers are registered in Warp, you can Start or Stop them from the MCP servers page. Each running server will have a list of available tools and resources.

You can rename and edit a server's name, as well as delete the server. To prevent Warp from automatically starting a server when you open Warp, set the `"start_on_launch"` value to `false` in the server's JSON configuration.

### Debugging

If you're having trouble with an MCP server, you can check the logs for any errors or messages to help you diagnose the problem by clicking the `View Logs` button on a server from the MCP servers page.

{% hint style="warning" %}
If you choose to share your MCP server logs with anybody, make sure to remove any sensitive information before sharing, as they may contain API keys. Many SSE based MCP servers will state that your URL should be treated like a password, and can be used with no additional authentication.
{% endhint %}

{% hint style="info" %}
Tip: We've noticed that some models often work better with MCP servers than others. If you're having trouble calling or using an MCP server, try using a different model.
{% endhint %}
