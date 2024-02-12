---
description: How to log out from Warp, and how to uninstall Warp
---

# Logging out & Uninstalling

## Logging out

You can log out of Warp through:

* `Settings > Account`, with the "Log out" button
* [Command Palette](../features/command-palette.md), with the "Log Out" item.
* The "Warp" menu bar, "Log out" item.

<figure><img src="../.gitbook/assets/logout.gif" alt=""><figcaption><p>Logout Demo</p></figcaption></figure>

### Known issues:

1. When you log out, you will lose all running processes and all unsaved objects.
2. When you log out and log in to Warp with another account, the following preferences will be preserved from the original account:
   1. Theme
   2. Keybindings
   3. Settings (e.g. autosuggestion, notifications, font size, welcome tips status)
3. Whenever you log in to Warp, you will receive the onboarding survey.

## Uninstalling Warp

Removing Warp from your computer involves uninstalling Warp and then removing any files or data.

{% tabs %}
{% tab title="macOS" %}
#### Uninstalling Warp installed via dmg

* Remove Warp with `sudo rm -r /Applications/Warp.app`

#### Uninstalling Warp installed via Brew

* Remove Warp with `brew uninstall warp`
* Clean up old versions of Warp formulae and small kegs of data with `brew cleanup warp`

#### Removing Warp login, settings, files, log, and database

* [Log out of Warp](uninstalling-warp.md#logging-out).
* Remove Warp settings with `defaults delete dev.warp.Warp-Stable`
* Remove Warp user files and logs with `sudo rm -r $HOME/.warp/ $HOME/Library/Logs/warp.log`
* Remove Warp database with `sudo rm -r "$HOME/Library/Application Support/dev.warp.Warp-Stable"`
{% endtab %}

{% tab title="Linux" %}
#### Uninstalling Warp via package manager

* Uninstall Warp using the same package manager that you used to [install](../getting-started/getting-started-with-warp.md) it.

#### Removing Warp login, settings, files, log, and database

* [Log out of Warp](uninstalling-warp.md#logging-out).
* Remove Warp config files with `rm -r ${XDG_CONFIG_HOME:-$HOME/.config}/warp`
* Remove Warp user files, logs, and database with `rm -r ${XDG_STATE_HOME:-$HOME/.local/state}/warp`
{% endtab %}
{% endtabs %}
