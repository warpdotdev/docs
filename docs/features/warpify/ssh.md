---
description: SSH wrapper that enables Warp features in remote sessions.
---

# SSH

{% hint style="warning" %}
This page is dedicated to the upcoming SSH features that may not yet be available to you.

If you are looking to troubleshoot the legacy SSH implementation, see the [SSH (Legacy)](ssh-legacy.md).
{% endhint %}

When you Warpify your SSH session, you get all the features of Warp without any configuration on your part. The input editor, auto-completions, and history search work the same, regardless of machine. We achieve this by running commands like `ls` on the remote machine on your behalf (more on this in the next section).

![SSH](<../../.gitbook/assets/6\_ssh (1) (1).png>)

## Implementation

If you have the `Warpify > SSH > Host Detection` setting enabled and run `ssh` and we detect an interactive session, we will begin our ssh host detection workflow. Once we have confidence you have successfully authenticated (by detecting `Last login:` or something resembling a basic prompt) we will prompt you to Warpify your active SSH session. Accepting Warpification will validate you have `tmux` installed on the remote machine, or ask to install it for you if not found.

[tmux](https://github.com/tmux/tmux/wiki) is a popular open source terminal multiplexer, which lets you switch easily between several programs within one terminal session. Warpifying a remote SSH session uses [tmux Control Mode](https://github.com/tmux/tmux/wiki/Control-Mode) to run adhoc background tasks (like those required to autocomplete a `cd` command, or populate the contents of a custom prompt) without disrupting your session history.

**Warpifying a remote SSH Session will make no lasting changes to your remote machine. The only exception to this is if you do not have `tmux` installed on the remote machine, in which case we will ask if we can install `tmux` on your behalf.**

If Warpification detects `tmux` is not installed, it will explicitly ask for your permission to install `tmux`. The installation of `tmux` is the only possible lasting change to the remote machine.

## User Settings

You can find all settings related to Warpifying SSH sessions in `Warpify > SSH`.

* If `Host Detection` is disabled, both automatic Warpification and the Warpification Prompt will be disabled for SSH sessions. The only way to Warpify an SSH session with `Host Detection` disabled is to manually run `Warpify SSH Session` from the command palette.
* Any host added to `Added hosts` will be automatically Warpified.
* Any host added to `Denylisted hosts` will not be prompted nor automatically Warpified.
* Both `Added hosts` and `Denylisted hosts` settings support regex, and the denylist takes precedence (i.e. a host that matches `Added hosts` and `Denylisted hosts` will not be prompted for Warpification nor automatically Warpify).

Host detection is parsed from the `ssh` command itself. For example:

```bash
ssh localhost
```

Here we're going to use the string literal `localhost` as a unique identifier for your target host.

## Manual Warpification

If you are ever in a remote SSH Session and would like to manually Warpify, you can do so by using the [command palette](../command-palette.md) and search for "Warpify SSH Session".
