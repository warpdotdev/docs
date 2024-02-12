---
description: >-
  We would love to get your feedback on Warp: bugs, feature requests, novel
  ideas, etc.
---

# Sending Feedback & Logs

### Sending Warp feedback:

* Open a new issue or feature request in our [GitHub repository](https://github.com/warpdotdev/warp/issues/new/choose).
* Through macOS Menu: Help > Send Feedback.
* Through in-app Menu: Warp Essentials:bulb: > Feedback.
* Join our [Discord](https://www.warp.dev/discord?utm\_source=docs-sending\_us\_feedback) server. Send a message in `#questions-and-feedback`.

<figure><img src="../.gitbook/assets/send-feedback-demo.gif" alt="sending feedback from the mac menu and warp essentials"><figcaption><p>Send Feedback</p></figcaption></figure>

### Sending WarpPreview feedback:

WarpPreview is an early access build given to Warp Ambassadors. You can join this insider program through our application. Learn more about the [Warp Ambassadors](https://warpdev.notion.site/Warp-Ambassadors-7aeacbc565694985a64710871470af67#68a28367517042a0aeaa472b2f29cea5) program.

* Join our [Discord](https://www.warp.dev/discord?utm\_source=docs-sending\_us\_feedback) server. Send a message in `#questions-and-feedback`.

## Gathering Warp Logs

In some cases, we may also ask for your Warp logs. You can retrieve them by following the instructions for your platform below. Locate the log file and attach it to your GitHub issue comment, feedback email, or discord message.

{% hint style="info" %}
Warp’s logs do _not_ contain any console input or output. See more on how we handle [Crash Reports and Telemetry](../getting-started/privacy.md#what-telemetry-data-are-you-collecting-and-why).
{% endhint %}

{% tabs %}
{% tab title="macOS" %}
The log file is located at `~/Library/Logs/warp.log`.

**Using Console**

1. Launch Console, found in Mac’s `Applications > Utilities` folder.
2. In the left pane, select Log Reports.
3. In the right pane, find the `warp` log.
{% endtab %}

{% tab title="Linux" %}
The log file is located at `${XDG_STATE_HOME:-$HOME/.local/state}/warp/warp.log`.
{% endtab %}
{% endtabs %}
