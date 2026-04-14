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

* [Warp Drive](https://docs.warp.dev/knowledge-and-collaboration/warp-drive/#using-warp-drive-offline) (Some files may be read-only in offline mode)
* [Oz agent](https://docs.warp.dev/agent-platform/warp-agents)
  * [Agent Mode](https://docs.warp.dev/agent-platform/warp-agents/interacting-with-agents/)
  * [Generate](https://docs.warp.dev/agent-platform/warp-agents)
  * [AI Autofill](https://docs.warp.dev/knowledge-and-collaboration/warp-drive/workflows#warp-ai-autofill)
  * [Prompts](https://docs.warp.dev/knowledge-and-collaboration/warp-drive/prompts)
  * [Active AI Recommendations](https://docs.warp.dev/agent-platform/warp-agents/active-ai)
  * [Voice](https://docs.warp.dev/agent-platform/warp-agents/interacting-with-agents/voice)
  * [Rules](https://docs.warp.dev/knowledge-and-collaboration/rules)
  * [Model Context Protocol](https://docs.warp.dev/knowledge-and-collaboration/mcp)
* [Teams](https://docs.warp.dev/knowledge-and-collaboration/teams)
* [Session Sharing](https://docs.warp.dev/knowledge-and-collaboration/session-sharing/)
* [Block Sharing](https://docs.warp.dev/terminal/blocks/block-sharing)
* [Refer a Friend](../community/refer-a-friend.md)