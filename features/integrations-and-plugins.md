# Integrations

Warp has methods of integrating with the most popular development tools. More methods are in the works.

## Raycast

Warp + Raycast extension helps you open new Windows, Tabs, or Launch Configurations with [ease](https://twitter.com/warpdotdev/status/1678432353461637121).

{% embed url="https://www.raycast.com/warpdotdev/warp" %}
Warp + Raycast Extension Link
{% endembed %}

## VSCode

Press `SHIFT-CMD-C` while in VSCode to open a new session in Warp.

![VSCode New Session Shortcut](../.gitbook/assets/vscode\_new\_session.gif)

To configure this, use the Apple Menu. Click on `Code` -> `Preferences` -> `Settings`. Type in "terminal" and change _Terminal > External: Osx Exec_ to `Warp.app`.

![VSCode External Terminal Configuration](../.gitbook/assets/vscode\_external\_terminal\_config.gif)

## JetBrains IDEs

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
