---
description: >-
  Configure how the Coding agent behaves and fine-tune when it should act on its
  own or ask for your approval.
---

# Code Permissions

Code Permissions let you define how your code agent operates—control its ability to apply diffs.

### Code Diff Permission

You can control how much autonomy the Coding agent has when applying diffs under `Settings > AI > Agents > Permissions` .&#x20;

<figure><img src=".gitbook/assets/agent-permissions.png" alt=""><figcaption><p>Fine-tuning agent control: This permissions panel lets users customize how much autonomy the Agent has when applying code diffs, reading files, creating plans, and executing commands—balancing safety with automation.</p></figcaption></figure>

**Code diff permission has three levels of autonomy:**

<table><thead><tr><th width="196.3369140625">Autonomy level</th><th>Description</th></tr></thead><tbody><tr><td>Agent Decides</td><td>Agent will act autonomously when it's confident, but prompt for approval when uncertain. This option balances speed with control, allowing the Agent to go ahead with common workflows while keeping you in the loop for more complex or risky steps.</td></tr><tr><td>Always ask</td><td>Agent will request explicit user approval before taking any action. Choose this for sensitive actions.</td></tr><tr><td>Always allow</td><td>Agent will perform the action without ever requesting explicit conformation. Use this for tasks you fully trust the Agent to handle on its own.</td></tr></tbody></table>

{% hint style="info" %}
_When all diff permissions are set to Always allow, the Coding agent gains full autonomy (“YOLO mode”) to applying diffs. Please use source control (i.e. `git`) to maintain the ability to revert any changes._
{% endhint %}
