---
description: >-
  Submit your feedback on Warp as well as logs, debugging id, process samples,
  bugs, feature requests, novel ideas, etc.
---

# Sending Feedback & Logs

### Sending Warp feedback

* Open a new issue or feature request in our [GitHub repository](https://github.com/warpdotdev/warp/issues/new/choose).
* [Command Palette](../terminal/command-palette.md), type and select "Send Feedback".
* Warp Essentials:bulb:, click on Feedback.
* Join our [Discord](https://discord.com/invite/warpdotdev) server. Send a message in [`#questions-and-feedback`](https://discord.com/channels/851854972600451112/1154432424873296012).
* Join our [Warp Community Slack](https://go.warp.dev/join-preview) and share feedback in **#feedback-general** (or **#feedback-preview** if it is specific to [Warp Preview](../community/warp-preview-and-alpha-program.md).
* For enterprise clients, please direct all feedback (including bug reports and debugging IDs) to the designated Warp Slack channel.

{% hint style="danger" %}
For security-related issues or questions, please email [security@warp.dev](mailto:security@warp.dev).
{% endhint %}

<figure><img src="../.gitbook/assets/send-feedback-demo.gif" alt="sending feedback from the mac menu and warp essentials"><figcaption><p>Send Feedback</p></figcaption></figure>

## Gathering Warp Logs

In some cases, we may also ask for your Warp logs. You can retrieve them by following the instructions for your platform below. Locate the log file and attach it to your GitHub issue comment, feedback email, or discord message.

{% hint style="info" %}
Warp's logs and crash reports do _not_ contain any console input or output. See more on how we handle [Crash Reports and Telemetry](../privacy/privacy.md#what-telemetry-data-are-you-collecting-and-why).
{% endhint %}

{% tabs %}
{% tab title="macOS" %}
The Warp log files are located at `~/Library/Logs/`.

Close Warp and run the following from another terminal to zip the logs to your Desktop:

```bash
zip -j ~/Desktop/warp-logs.zip ~/Library/Logs/warp.log*
```

{% hint style="warning" %}
If your issue is graphical (e.g. no display of windows) or a crash, please run Warp with the following command to capture more log information:

```bash
RUST_LOG=wgpu_core=info,wgpu_hal=info /Applications/Warp.app/Contents/MacOS/stable
```
{% endhint %}
{% endtab %}

{% tab title="Windows" %}
The Warp log files are located at `$env:LOCALAPPDATA\warp\Warp\data\logs\`.

Close Warp and run the following from another terminal to zip the logs to your Desktop:

```powershell
Compress-Archive -Path "$env:LOCALAPPDATA\warp\Warp\data\logs\warp.log*" -DestinationPath "$HOME\Desktop\warp-logs.zip" -Force
```

{% hint style="warning" %}
If your issue is graphical (e.g. no display of windows) or a crash, please run Warp with the following command to capture more log information:

```powershell
# Run if Warp on Windows is installed for a single user
$env:RUST_LOG="wgpu_core=info,wgpu_hal=info"; & "$env:LOCALAPPDATA\Programs\Warp\warp.exe"

# Run if Warp on Windows is installed for all users
$env:RUST_LOG="wgpu_core=info,wgpu_hal=info"; & "$env:PROGRAMFILES\Warp\warp.exe"
```
{% endhint %}
{% endtab %}

{% tab title="Linux" %}
The Warp log files are located at `~/.local/state/warp-terminal/`.

Close Warp and run the following from another terminal to zip the logs to your home directory:

```bash
tar -czf ~/warp-logs.tar.gz -C ~/.local/state/warp-terminal warp.log*
```

{% hint style="warning" %}
If your issue is graphical (e.g. no display of windows) or a crash, please run Warp with the following command to capture more log information:

```bash
RUST_LOG=wgpu_core=info,wgpu_hal=info MESA_DEBUG=1 EGL_LOG_LEVEL=debug warp-terminal
```
{% endhint %}
{% endtab %}
{% endtabs %}

## Gathering AI debugging ID <a href="#gathering-ai-debugging-id" id="gathering-ai-debugging-id"></a>

In cases where you have issues with the Agent, we may ask for the AI debugging ID to troubleshoot the specific conversation.&#x20;

To gather the debugging ID, `RIGHT-CLICK` on the AI conversation block in question and select "Copy debugging ID", then paste that into the [bug report](sending-us-feedback.md#sending-warp-feedback) that you submit so that our team can investigate the issue.&#x20;

Whenever there is an error in the Agent Conversation, there will also be an option to directly copy the debugging ID for the bug report.

<figure><img src="../.gitbook/assets/send-feedback-debugging-information.png" alt=""><figcaption></figcaption></figure>
