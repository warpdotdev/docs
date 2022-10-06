# Using Warp with \[bash|zsh|fish]

Warp currently supports popular existing shells like Bash, Zsh, and Fish. If your default shell is set to any other shell, you would see a banner notifying you that the shell is not supported, and Warp will fall back to Zsh.


### Using Fish shell with Warp

#### Step 1: Install Fish&#x20;

While Bash, and Zsh come pre-installed on macOS, Fish shell does not. So before using the Fish shell with Warp, you must install it on your computer. You can do that using one of the methods listed below -

1. Using Homebrew: If you already have homebrew installed, you can simply type `brew install fish`, and follow the instructions.&#x20;
2. Download the installer at fishshell.com.

#### Step 2: Switch to Fish as the default shell&#x20;

Once you’ve installed Fish on your computer, you can set it as your default shell, so Warp would use it every time a new tab, pane, or window is opened. To do that, you need to run two commands, depending on how you installed Fish -

**If you used Homebrew to install Fish on a Mac with an Intel Processor**, type the following two commands in Warp:

`echo /usr/local/bin/fish | sudo tee -a /etc/shells`&#x20;

`chsh -s /usr/local/bin/fish`

``

**`or,if` you used Homebrew to install Fish on a Mac with Apple Silicon**, type the following two commands in Warp:

`echo /opt/homebrew/bin/fish | sudo tee -a /etc/shells`&#x20;

`chsh -s /opt/homebrew/bin/fish`

``

**or**, **If you used the Mac installer** available on fishshell.com to install Fish, type the following two commands in Warp:

`echo /usr/local/bin/fish | sudo tee -a /etc/shells`&#x20;

`chsh -s /usr/local/bin/fish`

``

{% hint style="info" %}
If you prefer, you can also manually edit the /etc/shells file using the editor of your choice (you may need sudo privileges). See screenshot below.
{% endhint %}

<figure><img src="https://lh5.googleusercontent.com/LcJXwtPKL713XxfXAQ6VXBiXun_NnqAU1I1uUHr64_KPLY9sc94k8jo5e-KFEYyVGMaInlw-XCyqlnk-gj-YTsaM4DpufhaYHMiqJYoEpls_Iu8PkHE8nvD0bR0j6ny3hd6h3k0rossOrioA233wvdbWgV248qEu9p2vzqhvflZPktDE2a-X-afF8A" alt=""><figcaption><p>Edit the </p></figcaption></figure>

{% hint style="info" %}
**Why the different locations?** The location of Fish depends on how it was installed. Homebrew installs programs under `/usr/local` on Macs running Intel processors, but under `/opt/homebrew` for Macs running Apple Silicon. So, if you used Homebrew to install Fish on a Mac with Apple Silicon, the location of the executable is - `/opt/homebrew/bin/fish`
{% endhint %}

### Zsh is the default shell for Warp

Zsh is the default login and interactive shell on macOS (starting with macOS Catalina in 2019), replacing bash shell which had been the default until then. It is also the default shell for Warp. If your default system is set to Zsh, Warp will automatically start with that.

You can switch your default shell to any other shell supported by Warp (bash, zsh, fish).&#x20;

[Zsh](https://zsh.sourceforge.io/Doc/Release/zsh\_toc.html) is a Unix shell built as an extension of [Bourne shell](https://en.wikipedia.org/wiki/Bourne_shell) with many improvements around customization e.g. support for plugins, themes, syntax highlighting, and auto-correction..&#x20;

#### Setting up Zsh on Warp

&#x20;By default, macOS ships with zsh located in `/bin/zsh`. You can confirm this location by typing `which zsh` in your Warp terminal. You can also check the version of zsh installed on your system by simply typing the following:

`$ zsh --version`

#### Customize Your Zsh Shell Environment&#x20;

You can customize your Zsh shell environment by modifying the .zshrc file, which is a configuration file that is automatically created when zsh is installed in your system. It is typically located in the home directory of the user using the shell.

You can think of the zshrc file as a startup file, which gets executed every time a new instance of Zsh is launched (new window, new tab/pane etc.)

You can use the .zshrc file to customize the basic behavior of the shell, like setting environment variables, adding aliases, changing the [prompt](https://docs.warp.dev/features/prompt), and more. It can also be used to set up scripts, and key bindings that will execute when a new instance of Zsh is launched.

#### Editing the .zshrc file

The .zshrc file is located in the home directory, and can be opened with any text editor.

Note that the dot (.) before the file’s name indicates that the file is hidden, won’t be visible by default, and may not show in Finder. You can still edit the file from within the terminal by typing `nano ~/.zshrc` or `vi ~/.zshrc`.



<figure><img src="https://lh5.googleusercontent.com/z6kqYKxNMDMLSbhIO0nps7EXb5zXt3NeOJ7cto2C4NXd6-LIOsXSyL0hBpIjaV9mJ8wG0HgcZygjn7zHmljEI11xeX8FBAWRtOR221QaMghRepqc4Pnwqp4mdh2CBWYrqqE5TPmODdJg7go0E2ocCBtQ71Ok0qYPy6o6xLhbAr0yAb-ukk_SZuf0iQ" alt=""><figcaption></figcaption></figure>

#### Reloading the zshrc file after making changes to it

When you make a change to the zshrc file, it needs to be reloaded or sourced again for the changes to take effect. You can do this by either restarting Warp, or by simply typing - `source ~/.zshrc`.



### **Changing default shell**

**To change the default shell to bash**&#x20;

`chsh -s /bin/bash`

Enter your password when prompted to complete the switch. Every new tab, and window you now open will start with bash (note that the current session however, will remain with whatever shell you started with).

****

**To change the default shell to zsh**&#x20;

`chsh -s /bin/zsh`

Enter your password when prompted to complete the switch. Every new tab, and window you now open will start with zsh (note that the current session however, will remain with whatever shell you started with).

