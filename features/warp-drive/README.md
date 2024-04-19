---
description: >-
  Warp Drive is a workspace in your terminal where you can save workflows for
  personal use or to share with a team.
---

# Warp Drive

## What is Warp Drive?

All objects stored in Warp Drive sync immediately as they’re updated, so you and your team will always have access to the latest versions.

{% embed url="https://www.youtube.com/watch?v=8UmreUTTrkg" %}
Warp Drive, Teams, and Workflows Demo
{% endembed %}

## How to access it

{% tabs %}
{% tab title="macOS" %}
Warp Drive is accessible from the status bar in the Warp terminal or you can toggle the Warp Drive side panel with `CMD-\`.
{% endtab %}

{% tab title="Linux" %}
Warp Drive is accessible from the status bar in the Warp terminal or you can toggle the Warp Drive side panel with `CTRL-SHIFT-\`.
{% endtab %}
{% endtabs %}

<figure><img src="../../.gitbook/assets/Open_Warp_Drive.png" alt="Warp Drive icon on top left corner of Warp"><figcaption><p>Warp Drive Icon</p></figcaption></figure>

## Workspaces in Warp Drive

When you open the Warp Drive panel, you will find a personal workspace where you can store your workflows and organize them into folders.

<figure><img src="../../.gitbook/assets/Warp_Drive_Zero_State.png" alt=""><figcaption></figcaption></figure>

If you are a member of a team using Warp Drive, your team’s workspace will also be available in the side panel.

<figure><img src="../../.gitbook/assets/Warp_Drive_with_Team.png" alt=""><figcaption></figcaption></figure>

## Organizing workflows in Warp Drive with your team

* Objects (e.g. Workflows) and folders in Warp Drive can be sorted alphabetically and by the last updated
* Any objects moved from your personal workspace into a team’s workspace will be shared with all members of your team
* It is not currently possible to move an item back from a team’s workspace into a personal workspace; if you shared something inadvertently, you should copy the contents of the object to your clipboard, recreate it in your personal workspace, and then delete the object from your team workspace
* It is not currently possible to drag a folder of personal workflows into a team workspace; you will need to move objects one at a time

## Using Warp Drive offline

In offline mode, some files will be read-only. You can still create and edit files while offline in your personal space. They will only be saved locally and will not be synced. They cannot be moved into a team or deleted until you are back online.

<figure><img src="../../.gitbook/assets/warp_drive_offline.png" alt=""><figcaption><p>Warp Drive offline mode</p></figcaption></figure>

## Navigating Warp Drive with your keyboard

To avoid going back and forth between your mouse and keyboard, you can use your keyboard to navigate through Warp Drive once you have either opened Warp Drive or switched focus to the Warp Drive panel. (You can also click on a blank area within Warp Drive.) The object you are navigating with your keyboard will be highlighted in an accented color.

You can take these keyboard actions within Warp Drive:

{% tabs %}
{% tab title="macOS" %}
* Press `UP` or `DOWN` to navigate to the object you want.
* Press `Enter` to 1) execute an object or 2) open/collapse a workspace or folder.
* Press `CMD-ENTER` to open an object’s context menu.
* Press `CMD-SHIFT-(` and `CMD-SHIFT-)` to switch focus on Warp Drive and [Warp AI](../warp-ai/).
* Press `LEFT-ARROW` to collapse a workspace or folder
* Press `RIGHT-ARROW` to open a workspace or folder
{% endtab %}

{% tab title="Linux" %}
* Press `UP` or `DOWN` to navigate to the object you want.
* Press `Enter` to 1) execute an object or 2) open/collapse a space or folder.
* Press `CTRL-ENTER` to open an object’s context menu.
* Press `CTRL-SHIFT-(` and `CTRL-SHIFT-)` to switch focus on Warp Drive and [Warp AI](../warp-ai/).
{% endtab %}
{% endtabs %}

<figure><img src="../../.gitbook/assets/warp_drive_nav1.png" alt=""><figcaption><p>Warp Drive navigation states</p></figcaption></figure>

To switch between panels (e.g. jump from command line to Warp Drive to Warp AI) using your keyboard, you can use the “Switch Focus to Left Panel” and “Switch Focus to Right Panel” commands in the [Command Palette](../command-palette.md).

<figure><img src="../../.gitbook/assets/warp_drive_nav2.png" alt=""><figcaption></figcaption></figure>

## Import and Export

Every object in Warp Drive can be exported to a local file. To export, right-click on an object in Warp Drive and choose "Export" from the menu. This will prompt you for a directory to export into.

To import a local file or directory, right-click on a folder or workspace and choose "Import." If importing a directory, supported files in the directory and its sub-directories will be imported into a matching folder structure.

When importing or exporting, objects are converted as follows:
* [Workflows](./workflows.md) import from and export to [YAML workflows](../entry/yaml-workflows.md)
* [Notebooks](./notebooks.md) import from and export to Markdown files

## Troubleshooting Warp Drive

* If you were previously using Warp on your own and were later invited to join a team, you may need to exit, update, and restart the Warp app to gain access to your team’s shared drive and commands
* Navigating to Settings > Teams in Warp should also force a metadata update for you, which will ensure you have access to the latest versions of workflows in your team's drive
