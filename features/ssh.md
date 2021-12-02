# SSH

**Note on SSH**: For now, our SSH features only work if the default shell on your remote host is Bash. We also do not support recursive SSH, where you SSH from within another SSH session.

The team at Warp believes that terminal experience should not degrade between machines. This is why, when you SSH into a remote box, _you get all the features of Warp without any configuration on your part_.

![SSH in Warp: you get all our features without any extra configuration](../.gitbook/assets/6\_ssh.png)

That means our Blocks, input editor, autocomplete and suggestions, history (scoped to the machine), find, among all other features work exactly the same regardless of what machine you are on.

## How it Works

Under the hood we are using a wrapper around the real SSH. To enable Warp features on your remote machine, we wrap `/usr/bin/ssh` with a function that messages the Warp terminal to install our pre-cmd and pre-exec hooks. The normal SSH is still used to authenticate. If you would like to opt out of this behavior, you can invoke `/usr/bin/ssh` directly.
