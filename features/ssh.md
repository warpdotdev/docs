# SSH

When you SSH into a remote box, you get all the features of Warp without any configuration on your part.
The input editor, autocompletions, and history search work the same, regardless of machine.

Limitations of SSH (as of February 2022):
* Warp specific features like Blocks are currently supported only for bash or zsh.
* If you're using a different shell, you'll want to use `/usr/bin/ssh` directly (see below for more details).
* For zsh, xxd is required to bootstrap warp.
* For zsh, if locales are not set, it currently won't work (e.g. run `locale-gen en_US.UTF-8`).

If you're using zsh on the remote host, we create a temp folder to act as the ZDOTDIR during the bootstrapping process and remove it when the shell is setup.

![SSH](../.gitbook/assets/ssh.png)

## Implementation

We create a wrapper (around `/usr/bin/ssh`) to setup the shell for Warp's feature set. We authenticate normally using `/usr/bin/ssh`, and bootstrap the remote shell to work with Warp Blocks and the Input Editor. You can opt-out of this functionality by invoking `/usr/bin/ssh` directly.

* Warp takes over the prompt which enables us to build a modern input editor.
* Warp configures histcontrol to ignore commands with leading spaces. We do this so our bootstrapping code does not clutter the history.

```sh
function warp_ssh_helper() {
command ssh -o ControlMaster=yes -o ControlPath=~/.ssh/%C -o PermitLocalCommand=yes \
                -o LocalCommand="printf '$DCS_START{\"hook\": \"SSH\", \"value\": {\"socket_path\": \"~/.ssh/%C\", \"user\": \"%r\", \"machine\": \"%h\"}}$DCS_END'" \
                -t ${*:1} "case "'${SHELL##*/}'" in
  bash) exec -a bash bash --rcfile <(echo 'WARP_FEATURE_FLAG_HONOR_PS1=\"$WARP_FEATURE_FLAG_HONOR_PS1\"; set -o vi; set +o vi; HISTCONTROL=ignorespace; printf '\''$DCS_START{\"hook\": \"InitShell\", \"value\": {\"shell\": \"bash\"}}$DCS_END'\''')
      ;;
  zsh) WARP_TMP_DIR="'$(mktemp -d warptmp.XXXXXX)'"
if [[ "'$?'" == 0 ]]; then
echo $'"$( cat << 'EOF' | xxd -ps
unset RCS; unset GLOBAL_RCS; unset PS1; unset PS2; unset PROMPT; printf '\x1b\x50\x24\x64{"hook": "InitShell", "value": {"shell": "zsh"}}\x9c'
EOF
)"' | xxd -ps -r > "'$WARP_TMP_DIR'"/.zshenv
else
echo \"Failed to bootstrap warp. Continuing with a non-bootstrapped shell.\"
fi
WARP_SSH_RCFILES="'${ZDOTDIR:-$HOME}'" ZDOTDIR="'$WARP_TMP_DIR'" WARP_FEATURE_FLAG_HONOR_PS1=\"$WARP_FEATURE_FLAG_HONOR_PS1\" exec -a zsh zsh -g
      ;;
esac"
}
```
