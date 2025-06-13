# Agent Permissions

### Command allowlist

Agent Mode comes with default allowlist entries for common read-only commands that can be automatically executed without user confirmation.

* `which .*` - Find executable locations
* `ls(\s.*)?` - List directory contents
* `grep(\s.*)?` - Search file contents
* `find .*` - Search for files
* `echo(\s.*)?` - Print text output

You can add your own regular expressions to this list in `Settings > AI > Autonomy > Command allowlist`. Commands in the allowlist will always auto-execute, even if they are not read-only operations.

{% hint style="info" %}
Mostly any commands are allowed to be auto-executed if they are on the allowlist, with the exception of any commands that contain redirection. e.g. `which warp 2>/dev/null`
{% endhint %}

### Command denylist

Agent Mode comes with default denylist entries for potentially risky commands that always require explicit user permission before execution. A couple of examples include:

* `wget(\s.*)?` - Network downloads
* `curl(\s.*)?` - Network requests
* `rm(\s.*)?` - File deletion
* `eval(\s.*)?` - Shell code execution

The denylist takes precedence over both the allowlist and model-based auto-execution. If a command matches the denylist, user permission will always be required, regardless of other settings. You can add your own regular expressions to this list in `Settings > AI > Autonomy > Command denylist`.

### File read permissions for coding

When performing coding tasks, Agent Mode can automatically read files. This allows Agent Mode to analyze code without requiring explicit permission for each file access.

This behavior can be toggled in `Settings > AI > Autonomy > Coding read permissions`.
