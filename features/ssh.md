# SSH

When you SSH into a remote box, you get all the features of Warp without any configuration on your part. The input editor, auto-completions, and history search work the same, regardless of machine.

[Limitations of SSH](https://github.com/warpdotdev/Warp/issues/578) (as of February 2022):

* Warp specific features like Blocks are currently supported only for bash or zsh.
* If you're using a different shell, you'll want to use `/usr/bin/ssh` directly (see below for more details).
* For zsh, xxd is required to bootstrap warp.

If you're using zsh on the remote host, we create a temp folder to act as the ZDOTDIR during the bootstrapping process and remove it when the shell is set up.

[Tmux is not currently supported.](https://github.com/warpdotdev/Warp/discussions/501)

{% hint style="warning" %}
The SSH Wrapper only supports bash/zsh/fish shells in remote sessions. If the remote server has another shell, please [change the default shell](../getting-started/using-warp-with-shells.md#changing-default-shell) to enable the SSH Wrapper.
{% endhint %}

![SSH](../.gitbook/assets/ssh.png)

## Implementation

We create a wrapper (around `/usr/bin/ssh`) to set up the shell for Warp's feature set. We authenticate normally using `/usr/bin/ssh`, and bootstrap the remote shell to work with Warp Blocks and the Input Editor. You can opt out of this functionality by invoking `/usr/bin/ssh` directly.

* Warp takes over the prompt which enables us to build a modern input editor.
* Warp configures histcontrol to ignore commands with leading spaces. We do this so our bootstrapping code does not clutter the history.

You can see the SSH wrapper by using `which warp_ssh_helper` in Zsh, `type warp_ssh_helper` in Bash.

_Note:_ The ssh wrapper is only _initialized_ on your local machine. We don’t currently support bootstrapping nested ssh sessions

{% hint style="info" %}
Warp's completions for ssh do respect `~/.ssh/config` as well as `~/.ssh/known_hosts`
{% endhint %}

## Troubleshooting SSH

### channel 2: open failed: connect failed: open failed

If you're seeing these errors, you may have some config on your server (usually in `/etc/ssh/sshd_config`) preventing Warp's ControlMaster connection from working. In this state, completions that require information from your remote host won't work and your history also won't work.

You should ensure that `MaxSessions` is either commented out or is at least `2`.

Write access in `/etc/ssh/` typically requires sudo access. After any edits, you'd also need to restart the `sshd` daemon.
