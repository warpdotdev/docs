# SSH

When you SSH into a remote box, you get all the features of Warp without any configuration on your part.
The input editor, autocompletions, and history search work the same, regardless of machine.

Note on SSH (October 2021):

Warp specific features like Blocks are not yet supported for SSH on ZSH or Fish.
Blocks are also not supported for neseted SSH sessions.

![SSH](../.gitbook/assets/ssh.png)

## Implementation

We create a wrapper (around `/usr/bin/ssh`) that runs pre-CMD and pre-exec hooks.
We authenticate normally, but bootstrap the remote shell to work with Warp Blocks and the Input Editor.You can opt-out of this functionality by invoking `/usr/bin/ssh` directly.

* Warp takes over the prompt which enables us to build a modern input editor.
* Warp configures histcontrol to ignore commands with leading spaces. We do this so our bootstrapping code does not clutter the history.

`function warp_ssh_helper() { command ssh -o ControlMaster=yes -o ControlPath=/.ssh/%C -o PermitLocalCommand=yes
-o LocalCommand="printf '$DCS_START{"hook": "SSH", "value": {"socket_path": "/.ssh/%C", "user": "%r", "machine": "%h"}}$DCS_END'"
-t ${*:1} "exec -a bash bash --rcfile <(echo 'unset PS1; unset PS2; set -o vi; set +o vi; HISTCONTROL=ignorespace; printf '''$DCS_START{"hook": "InitShell", "value": {"shell": "bash"}}$DCS_END'''')"
}`
