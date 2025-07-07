---
description: Using Warp offline and what features are supported.
---

# Using Warp Offline

The first time you download and open Warp, you will need to be online for the initial setup. After the initial setup Warp’s core terminal features will work as expected when you’re offline, regardless of whether you are logged in or logged out.

Requiring all users, logging in or logged out, to be online when first accessing Warp is required to allow use of Warp's AI and cloud features. When you first open the app, we create a unique user-ID to meter AI-usage and attach cloud objects to specific accounts. If you opt to use Warp logged-out, this unique ID is attached to an anonymous user account.

{% hint style="info" %}
Warp is "Offline" when you aren't connected to the internet, or if you're blocking calls `app.warp.dev` on your network. There is no explicit Offline Mode in Warp.
{% endhint %}

### Cloud-based features require online access

Warp’s cloud-based features which require an internet connection will not work in offline mode. Those features include:

* [Warp Drive](../knowledge-and-collaboration/warp-drive/#using-warp-drive-offline) (Some files may be read-only in offline mode)
* [Warp AI](../agents/overview.md)
  * [Agent Mode](../agents/using-agents/)
  * [Generate](../agents/generate.md)
  * [AI Autofill](../knowledge-and-collaboration/warp-drive/workflows.md#warp-ai-autofill)
  * [Prompts](../knowledge-and-collaboration/warp-drive/prompts.md)
  * [Active AI](../agents/active-ai.md)
  * [Voice](../agents/voice.md)
  * [Rules](../knowledge-and-collaboration/rules.md)
  * [Model Context Protocol](../knowledge-and-collaboration/mcp.md)
* [Teams](../knowledge-and-collaboration/teams.md)
* [Session Sharing](../knowledge-and-collaboration/session-sharing.md)
* [Block Sharing](../terminal/blocks/block-sharing.md)
* [Refer a Friend](../community/refer-a-friend.md)
