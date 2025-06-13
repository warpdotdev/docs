---
description: >-
  Agent Mode’s autonomy settings let you control when commands are auto-executed
  by configuring allowlists, denylists, and model-based safety checks.
---

# Autonomy

Agent Mode supports configurable autonomous command execution under `Settings > AI > Autonomy`. You can customize this by:

1. Using a command allowlist to specify which commands can auto-execute
2. Using a command denylist to specify which commands require confirmation
3. Letting the Agent Mode model automatically determine if a command is safe to execute based on whether it's read-only

<figure><img src="../../.gitbook/assets/autonomy.gif" alt="Agent Mode connects to a docker container and checks for error logs with autonomy enabled."><figcaption><p>Agent Mode connects to a docker container and checks for error logs with autonomy enabled.</p></figcaption></figure>
