---
description: >-
  Warp supports popular shells like Bash, Zsh, and Fish. If your default shell
  is set to any other shell, you will see a banner indicating the shell is not
  supported and Warp will default to zsh.
---

# Using Warp with \[zsh|bash|fish]

### Zsh is the default shell for Warp

Zsh is the default login and interactive shell on macOS (starting with macOS Catalina in 2019), replacing the Bash shell. Warp tries to load your login shell by default, currently we support Bash, Fish, and Zsh; if your login shell is set to something else e.g. Nushell Warp will load Zsh instead.

You can switch your default shell to any other shell supported by Warp (Bash, Zsh, Fish) using the instructions at the bottom of the page.

[Zsh](https://zsh.sourceforge.io/Doc/Release/zsh\_toc.html) is a Unix shell built as an extension of [Bourne shell](https://en.wikipedia.org/wiki/Bourne\_shell) with many improvements around customization e.g. support for plugins, themes, syntax highlighting, and auto-correction..

#### Setting up Zsh on Warp

By default, macOS ships with Zsh located in `/bin/zsh`. You can confirm this location by typing `which zsh` in your Warp terminal. You can also check the version of Zsh installed on your system by simply typing the following:

`$ zsh --version`

#### Customize Your Zsh Shell Environment

You can customize your Zsh shell environment by modifying the `.zshrc` file, which is a configuration file that is automatically created when Zsh is installed in your system. It is typically located your home directory (`~/.zshrc`).

You can think of the `zshrc` file as a startup file that gets executed when a new instance of Zsh is launched (new window, new tab/pane etc.)

You can use the `.zshrc` file to customize behavior like: setting environment variables, adding aliases, changing the [prompt](https://docs.warp.dev/features/prompt), and more. It can also be used to set up key-bindings, and scripts that will automatically execute when a new instance of Zsh is launched.

#### Editing the .zshrc file

The `.zshrc` file is located in the home directory, and can be opened with any text editor.

Note that the dot (`.`) before the file’s name indicates that the file is hidden, (it) won’t be visible by default, and may not show up in Finder (press `SHIFT-CMD-.` to show hidden files in Finder). You can edit the file from the terminal by typing `nano ~/.zshrc` or `vi ~/.zshrc`.

<figure><img src="https://lh5.googleusercontent.com/z6kqYKxNMDMLSbhIO0nps7EXb5zXt3NeOJ7cto2C4NXd6-LIOsXSyL0hBpIjaV9mJ8wG0HgcZygjn7zHmljEI11xeX8FBAWRtOR221QaMghRepqc4Pnwqp4mdh2CBWYrqqE5TPmODdJg7go0E2ocCBtQ71Ok0qYPy6o6xLhbAr0yAb-ukk_SZuf0iQ" alt=""><figcaption></figcaption></figure>

#### Reloading the zshrc file after making changes to it

When you make a change to the `zshrc` file, it needs to be reloaded or sourced again for the changes to take effect. You can do this by either restarting Warp, or by typing: `source ~/.zshrc`.

### Using Bash shell with Warp

Macs come with Bash pre-installed, typically located at the `/bin/bash` directory. You can customize Bash by editing its configuration files (`.bashrc` file for non-login interactive shell and `.bash_profile` for login shells).

{% hint style="info" %}
If you run into issues configuring these files with Warp, please see [Configuring and debugging your RC files](https://docs.warp.dev/help/known-issues#configuring-and-debugging-your-rc-files).
{% endhint %}

#### Customize Your Bash Shell Environment

You can customize your Bash shell environment by modifying the `.bashrc` file, which is a configuration file that is automatically created when Bash is installed in your system. It is typically located your home directory (`~/.bashrc`).

You can think of the `bashrc` file as a startup file that gets executed when a new instance of Bash is launched (new window, new tab/pane etc.)

Note that the dot (`.`) before the file’s name indicates that the file is hidden, (it) won’t be visible by default, and may not show up in Finder (press `SHIFT-CMD-.` to show hidden files in Finder). You can edit the file from the terminal by typing `nano ~/.bashrc` or `vi ~/.bashrc`.

You can use the `.bashrc` file to customize behavior like: setting environment variables, adding aliases, changing the [prompt](https://docs.warp.dev/features/prompt), and more. It can also be used to set up key-bindings, and scripts that will automatically execute when a new instance of Bash is launched.

When you make a change to your `bashrc` file, it needs to be reloaded or sourced again for the changes to take effect. You can do this by either restarting Warp, or by typing: `source ~/.bashrc`.

```shell
$ source ~/.bashrc
```

{% hint style="info" %}
**Pro Tip**: Instead of typing `source ~/.bashrc`, you can create an alias for it inside the .bashrc file by typing -\
\
`alias reload="source ~/.bashrc"`\
\
So, now you can type \``` reload` ``, to source the latest changes in the `bashrc`
{% endhint %}

### Using Fish shell with Warp

#### Step 1: Install Fish

While Bash, and Zsh come pre-installed on macOS, Fish shell does not. So before using Fish with Warp, you will need to install it. Install Fish using one of the methods listed below -

1. With Homebrew: If you already have homebrew installed, you can simply type `brew install fish`, and follow the instructions.
2. Download the installer at [fishshell.com](https://fishshell.com/)

#### Step 2: Switch to Fish as the default shell

Once you’ve installed Fish on your computer, you can set it as your default shell, so Warp would use it every time a new tab, pane, or window is opened. You can either make Fish the default shell for just Warp, from the session settings (`Settings > Features`, then `Session`), or for your user account. To change your account's default shell, you need to run two commands, depending on how you installed Fish -

**If you used Homebrew to install Fish on a Mac with an Intel Processor**, type the following two commands in Warp:

`echo $(which fish) | sudo tee -a /etc/shells`

`chsh -s $(which fish)`

**If you used Homebrew to install Fish on a Mac with Apple Silicon**, type the following two commands in Warp:

`echo $(which fish) | sudo tee -a /etc/shells`

`chsh -s $(which fish)`

**If you used the Mac installer** available on fishshell.com to install Fish, type the following two commands in Warp:

`echo $(which fish) | sudo tee -a /etc/shells`

`chsh -s $(which fish)`

{% hint style="info" %}
If you prefer, you can also manually edit the /etc/shells file using the editor of your choice (you may need sudo privileges).
{% endhint %}

{% hint style="info" %}
**Why the different locations?** The location of Fish depends on how it was installed. Homebrew installs programs under `/usr/local` on Macs running Intel processors, but under `/opt/homebrew` for Macs running Apple Silicon. So, if you used Homebrew to install Fish on a Mac with Apple Silicon, the location of the executable is - `/opt/homebrew/bin/fish`. \
You can identify which version you have with `echo $(which fish)`.
{% endhint %}

### **Changing default shell**

There are two ways to change the default shell that Warp uses for new tabs, windows, and panes:

1. We recommend you choose a shell in Warp by going to `Settings > Features` and scrolling to the `Session` section, then select the "Startup shell for new sessions"
2. You can also change your [login shell](https://en.wikipedia.org/wiki/Chsh) by following the instructions below (or the [macOS documentation](https://support.apple.com/en-us/HT208050))

{% hint style="info" %}
The changes to your shell will only take effect when you start a new session.
{% endhint %}

**To change the default shell to bash**

`chsh -s $(which bash)`

Enter your password when prompted to complete the switch. Every new tab, and window you now open will start with bash.

**To change the default shell to zsh**

`chsh -s $(which zsh)`

Enter your password when prompted to complete the switch. Every new tab, and window you now open will start with zsh.

[**To change the default shell to fish**](using-warp-with-shells.md#step-2-switch-to-fish-as-the-default-shell)
