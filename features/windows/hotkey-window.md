# Global Hotkey

## What is it

Warp's Global Hotkey is a configurable shortcut that can show/hide a dedicated window or all windows on your chosen desktop regardless of whether the app is focused. You can customize the dedicated windows' pinned position and its width and height ratio relative to your active screen size.

{% hint style="warning" %}
On Linux, this feature may not work for some X11 window managers which do not implement [Extended Window Manager Hints](https://en.wikipedia.org/wiki/Extended_Window_Manager_Hints). 
{% endhint %}

## How to access it

### Dedicated Window

1. Open `Settings > Features > Keys` and select "Dedicated hotkey window" from the Global Hotkey dropdown to enable the feature.
2. Configure the keybinding, the windows position, screen, and relative size or uncheck "Autohides on the loss of keyboard focus" which will cause the dedicated Hotkey Window to stay on top when triggered regardless of mouse or keyboard focus.

{% hint style="info" %}
Your new customization will apply the **next** time a Dedicated Window is created, not the currently opened one.
{% endhint %}

{% hint style="warning" %}
On Linux, Warp does not support the "Autohides on the loss of keyboard focus" feature.
{% endhint %}

### Show/Hide All Windows

1. Open `Settings > Features > Keys` and select "Show/hide all windows" from the Global Hotkey dropdown to enable the feature.
2. Configure your preferred keybinding.

{% hint style="info" %}
`CMD-ESC, CMD-BACKTICK, CMD-TAB, CMD-PERIOD, and CMD-TILDE` are not supported keyboard shortcuts. There is a request for support you can track it [here #1851](https://github.com/warpdotdev/Warp/issues/1851)
{% endhint %}

## How it works

<figure><img src="../../.gitbook/assets/Dedicated Window.gif" alt=""><figcaption><p>Global Hotkey - Dedicated Window Demo</p></figcaption></figure>

<figure><img src="../../.gitbook/assets/Show-Hide All Windows.gif" alt=""><figcaption><p>Global Hotkey - Show/Hide All Windows Demo</p></figcaption></figure>

## Troubleshooting Hotkey Window

### Mac
If the keybinding doesn't work, check under `System Preferences > Security & Privacy > Accessibility` and tick the checkbox to grant Warp access.

### Linux
The hotkey window may appear on the incorrect monitor under certain window sizes. For example, with GNOME, if the hotkey window is supposed to show on a monitor having the task bar (GNOME Panel), and the window height is 100%, causing an overlap, the hotkey window may fallback to showing on an external monitor if you have one. Try working around this by setting a window height to a lesser percentage, e.g. 90%.
