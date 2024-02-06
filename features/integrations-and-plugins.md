---
description: Warp extends and integrates with popular development tools.
---

# Integrations

## Docker

{% hint style="info" %}
Currently, the Docker extension is only available on macOS.
{% endhint %}

[Warp’s Docker extension](https://hub.docker.com/extensions/warpdotdev/warp) makes it more convenient to open Docker containers in Warp. With the extension, you can click to open any Docker container in [a Warpified subshell](https://docs.warp.dev/features/subshells), without manually running `docker exec` or typing out lengthy container IDs.

Select a container from the list and specify a shell type. Note, that only `bash|zsh|fish` are supported shells for docker containers. Then, select a user (optional) and finally click “Open in Warp” to run commands within the Docker container.&#x20;

<figure><img src="../.gitbook/assets/docker-extension.png" alt=""><figcaption><p>Warp's extension for Docker lists available containers.</p></figcaption></figure>

## Raycast

Warp + Raycast extension helps you open new Windows, Tabs, or Launch Configurations with [ease](https://twitter.com/warpdotdev/status/1678432353461637121).

{% embed url="https://www.raycast.com/warpdotdev/warp" %}
Warp + Raycast Extension Link
{% endembed %}

## VSCode

Press `SHIFT-CMD-C` while in VSCode to open a new session in Warp.

![VSCode New Session Shortcut](../.gitbook/assets/vscode\_new\_session.gif)

{% tabs %}
{% tab title="macOS" %}
To configure this, use the Apple Menu. Click on `Code` -> `Settings` -> `Settings`. Type in "terminal" and change _Terminal > External: Osx Exec_ to `Warp.app`.
{% endtab %}

{% tab title="Linux" %}
To configure this, navigate to Settings in VSCode and search for `Terminal › External: Linux Exec`. Change this to `warp` if you've installed Warp with your distribution's package manager. Otherwise, put in the full path to the executable (e.g. if it is an AppImage).
{% endtab %}
{% endtabs %}

![VSCode External Terminal Configuration](../.gitbook/assets/vscode-integration-settings.gif)

## JetBrains IDEs

{% hint style="info" %}
Currently, the JetBrains IDE configuration is only available on macOS.
{% endhint %}

Press a keyboard shortcut of choice while in a JetBrains IDE to open a new session in Warp.

To configure this, use the Apple Menu. Click on `Preferences`, go to `External Tools` and click `Add`. In this menu, put the following information:

* _Name_: Open Warp
* _Program_: `/Applications/Warp.app`
* _Arguments_: `$ProjectFileDir$`
* _Working Directory_: `/Applications`

Then press `Ok`. Now you will be able to `Open Warp` from the Apple Menu under `Tools` -> `External Tools`.

![JetBrains New Session Shortcut](../.gitbook/assets/jetbrains\_external\_terminal\_config.gif)

To attach this configuration to a keyboard shortcut, you must go to the Apple Menu -> `Preferences`. Then go to `Keymap` -> `External Tools`. You will find `Open Warp`. Right click on it, and select `Add Keyboard Shortcut`. Type your desired shortcut and click save! You're ready to open Warp with a keyboard shortcut.

![JetBrains Configure Keyboard Shortcut](../.gitbook/assets/jetbrains\_external\_window\_keymap\_config.gif)
