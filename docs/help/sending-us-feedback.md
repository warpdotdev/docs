---
description: 'Submit your feedback on Warp: bugs, feature requests, novel ideas, etc.'
---

# Sending Feedback & Logs

### Sending Warp feedback:

* Open a new issue or feature request in our [GitHub repository](https://github.com/warpdotdev/warp/issues/new/choose).
* [Command Palette](../features/command-palette.md), type and select "Send Feedback".
* Warp Essentials:bulb:, click on Feedback.
* Join our [Discord](https://discord.com/invite/warpdotdev) server. Send a message in [`#questions-and-feedback`](https://discord.com/channels/851854972600451112/1154432424873296012).

{% hint style="info" %}
For security-related issues or questions, please email [security@warp.dev](mailto:security@warp.dev).
{% endhint %}

<figure><img src="../.gitbook/assets/send-feedback-demo.gif" alt="sending feedback from the mac menu and warp essentials"><figcaption><p>Send Feedback</p></figcaption></figure>

## Gathering Warp Logs

In some cases, we may also ask for your Warp logs. You can retrieve them by following the instructions for your platform below. Locate the log file and attach it to your GitHub issue comment, feedback email, or discord message.

{% hint style="info" %}
Warp’s crash reports do _not_ contain any console input or output. See more on how we handle [Crash Reports and Telemetry](../getting-started/privacy.md#what-telemetry-data-are-you-collecting-and-why).
{% endhint %}

{% tabs %}
{% tab title="macOS" %}
The Warp log files are located at `~/Library/Logs/warp.log*`. Zip the logs to your home folder with:

```bash
zip -j ~/Desktop/warp-logs.zip ~/Library/Logs/warp.log*
```

{% hint style="info" %}
If your issue is graphical (e.g. no display of windows, etc), please run Warp with the following command to capture more log information.

```bash
RUST_LOG=wgpu_core=info,wgpu_hal=info /Applications/Warp.app/Contents/MacOS/stable
```
{% endhint %}
{% endtab %}

{% tab title="Windows" %}
The Warp log files are located at `$env:LOCALAPPDATA\warp\Warp\data\logs\warp.log*`. Zip the logs to your home folder with:

```powershell
Compress-Archive -Path $env:LOCALAPPDATA\warp\Warp\data\logs\warp.log*" -DestinationPath "$HOME\Desktop\warp-logs.zip
```

{% hint style="info" %}
If your issue is graphical (e.g. no display of windows, etc), please run Warp with the following command to capture more log information.

```powershell
$env:RUST_LOG="wgpu_core=info,wgpu_hal=info"; & "$env:LOCALAPPDATA\Programs\Warp\warp.exe"
```
{% endhint %}
{% endtab %}

{% tab title="Linux" %}
The Warp log files are located at `${XDG_STATE_HOME:-$HOME/.local/state}/warp-terminal/warp.log*`. Zip the logs to your home folder with:

```bash
zip -j ~/warp-logs.zip ~/.local/state/warp-terminal/warp.log*
```

{% hint style="info" %}
If your issue is graphical (e.g. no display of windows, etc), please run Warp with the following command to capture more log information.

```bash
RUST_LOG=wgpu_core=info,wgpu_hal=info MESA_DEBUG=1 EGL_LOG_LEVEL=debug warp-terminal
```
{% endhint %}
{% endtab %}
{% endtabs %}
