---
description: >-
  Warp supports popular shells like bash, zsh, and fish. If your default shell
  is set to any other shell, you will see a banner indicating the shell is not
  supported and Warp will default to zsh.
---

# Using Warp with \[zsh|bash|fish]

## Warp default shell

Warp tries to load your login shell by default. Currently, Warp supports bash, fish, and zsh; if your login shell is set to something else (e.g. Nushell) Warp will load zsh instead.

Zsh is the default login and interactive shell on macOS (starting with macOS Catalina in 2019), replacing the bash shell. For most Linux distributions, the default shell is bash.

### **Changing what shell Warp uses**

There are two ways to change the shell that Warp uses for new tabs, windows, and panes:

1. We recommend you choose a shell in Warp by going to `Settings > Features` and scrolling to the `Session` section, then select the "Startup shell for new sessions"
2. You can also change your [login shell](https://en.wikipedia.org/wiki/Chsh) by following the [instructions below](using-warp-with-shells.md#changing-your-system's-default-shell) (or the [macOS documentation](https://support.apple.com/en-us/HT208050)).

{% hint style="info" %}
The changes to your shell will only take effect when you start a new session.
{% endhint %}

### Changing your system's default shell

**To change the default shell to bash**

`chsh -s $(which bash)`

Enter your password when prompted to complete the switch. Every new tab, and window you now open will start with bash.

**To change the default shell to zsh**

`chsh -s $(which zsh)`

Enter your password when prompted to complete the switch. Every new tab, and window you now open will start with zsh.

[**To change the default shell to fish**](using-warp-with-shells.md#step-2-switch-to-fish-as-the-default-shell)

## Customizing your shell environment

#### Customize Your zsh Shell Environment

You can customize your zsh shell environment by modifying the `.zshrc` file, which is a configuration file that is automatically created when zsh is installed in your system. It is typically located in your home directory (`~/.zshrc`). You can think of the `zshrc` file as a startup file that gets executed when a new session of zsh is launched (a new window, tab, or pane is opened).

You can use the `.zshrc` file to customize behavior like setting environment variables, adding aliases, changing the [prompt](https://docs.warp.dev/features/prompt), and more. It can also be used to set up key bindings, and scripts that will automatically execute when a new instance of zsh is launched.

#### Editing the .zshrc file

The `.zshrc` file is located in the home directory, and can be opened with any text editor. You can edit the file from the terminal by typing `nano ~/.zshrc` or `vi ~/.zshrc`.

{% hint style="info" %}
Note that the dot (`.`) before the file’s name indicates that the file is hidden, won’t be visible by default, and may not show up in Finder, Explorer, or other file managers. Please reference your file explorers' documentation to see how to show hidden files.
{% endhint %}

#### Reloading the zshrc file after making changes to it

When you make a change to the `zshrc` file, it needs to be sourced again for the changes to take effect. You can do this by either restarting Warp or opening a new session (window, tab, or pane).

### Using bash shell with Warp

Macs come with bash pre-installed, typically located at the `/bin/bash` directory. You can customize bash by editing its configuration files (`.bashrc` file for non-login interactive shell and `.bash_profile` for login shells).

{% hint style="info" %}
If you run into issues configuring these files with Warp, please see [Configuring and debugging your RC files](https://docs.warp.dev/help/known-issues#configuring-and-debugging-your-rc-files).
{% endhint %}

#### Customize Your bash Shell Environment

You can customize your bash shell environment by modifying the `.bashrc` file, which is a configuration file that is automatically created when bash is installed in your system. It is typically located in your home directory (`~/.bashrc`).

You can use the `.bashrc` file to customize behavior like: setting environment variables, adding aliases, changing the [prompt](https://docs.warp.dev/features/prompt), and more. It can also be used to set up key-bindings, and scripts that will automatically execute when a new instance of bash is launched.

You can think of the `bashrc` file as a startup file that gets executed when a new session of bash is launched (a new window, tab, or pane is opened). You can edit the file from the terminal by typing `nano ~/.bashrc` or `vi ~/.bashrc`.

When you make a change to your `bashrc` file, it needs to be reloaded or sourced again for the changes to take effect. You can do this by either restarting Warp or opening a new session (window, tab, or pane).

{% hint style="info" %}
Dot (`.`) before the file’s name indicates that the file is hidden, won’t be visible by default, and may not show up in Finder, Explorer, or other file managers. Please reference your file explorers' documentation to see how to show hidden files.
{% endhint %}

## Additional shell guidance for macOS

#### Setting up zsh on Warp

By default, macOS ships with [zsh](https://zsh.sourceforge.io/Doc/Release/zsh\_toc.html) located in `/bin/zsh`. You can confirm this location by typing `which zsh` in your Warp terminal. You can also check the version of zsh installed on your system by simply typing the following:

`$ zsh --version`

### Using fish shell with Warp on macOS

#### Step 1: Install fish

While bash, and zsh come pre-installed on macOS systems, fish shell does not. So before using fish with Warp, you will need to install it. Install fish 3.6 or above using one of the methods listed below -

1. With Homebrew: If you already have homebrew installed, you can simply type `brew install fish`, and follow the instructions.
2. Download the installer at [fishshell.com](https://fishshell.com/)

#### Step 2: Switch to fish as the default shell

Once you’ve installed fish on your computer, you can set it as your default shell, so Warp will use it every time a new tab, pane, or window is opened. You can either make fish the default shell for only Warp, from the session settings (`Settings > Features > Session`), or for your user account. To change your account's default shell, you need to run two commands.

**If you used Homebrew to install fish on a macOS or if you used the Mac installer** available on fishshell.com to install fish, type the following two commands in Warp:

```
echo $(which fish) | sudo tee -a /etc/shells
chsh -s $(which fish)
```

{% hint style="info" %}
If you prefer, you can also manually edit the `/etc/shells` file using the editor of your choice (you may need sudo privileges).
{% endhint %}

{% hint style="info" %}
**Why the different locations?** The location of fish depends on how it was installed. Homebrew installs programs under `/usr/local` on Macs running Intel processors, but under `/opt/homebrew` for Macs running Apple Silicon. So, if you used Homebrew to install fish on a Mac with Apple Silicon, the location of the executable is - `/opt/homebrew/bin/fish`.\
You can identify where fish is installed by running `echo $(which fish)`.
{% endhint %}
