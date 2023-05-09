# Quit Warning

## What is it

Warp's quit warning feature is a valuable precaution to prevent unintentional data loss or lost progress on long-running jobs. When working with multiple tabs and windows, there is a risk of forgetting about a still-running process and accidentally quitting the app by pressing `CMD-Q` without saving data. The quit warning feature ensures that you receive a warning before quitting the app with a running process, giving you an opportunity to save your work and avoid any unintended data loss. If you quit the app or close a window containing a session with a running process, you'll see the alert and need to confirm the action before proceeding. If you aren't sure which processes you have running, there is also an option to show those processes.

## How to access it

* Open `Settings > Features > General`, there you can toggle the "Show warning before quitting".
* You can also toggle the quit warning feature in the Command Palette, by searching for \`Quit Warning'.
* If enabled, when you try and close Warp with `CMD-Q` you will see a pop-up window with a few options listed below:
  * Yes, quit, which will close all the Warps sessions and running processes.
  * Show running processes, which will bring up the [Session Navigation](sessions/session-navigation.md) panel with a filter for running processes `@running`.
  * Cancel, which will prevent Warp from closing.
  * Don't ask again, which is a box you can check to disable the quit warning feature.

## How it Works

{% embed url="https://www.loom.com/share/bacb9d1c1e3947dca8365e15231cfcd3?hide_owner=true&hide_share=true&hide_title=true&hideEmbedTopBar=true" %}
Quit Warning Modal Demo
{% endembed %}
