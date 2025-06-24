---
hidden: true
---

# Run to completion

### Model based auto-execution

Agent Mode can dynamically analyze command safety for automatic execution of read-only commands. This provides intelligent command safety analysis but follows a strict precedence order.

1. Denylist (highest priority) - Commands always require confirmation
2. Allowlist - Commands always auto-execute
3. Model-based analysis (lowest priority) - Agent Mode determines if a command is read-only safe

This behavior can be toggled in `Settings > AI > Autonomy > Model-based auto-execution`.

## TO DO: rewrite

{% hint style="warning" %}
Dispatch is currently in beta, with ongoing improvements that will expand its capabilities over time.
{% endhint %}

_Dispatch_ is a form of Agent Mode that carries out complex tasks automatically. When you make a Dispatch query, the AI will:

1. Gather context about the task, using your [codebase](run-to-completion.md#codebase-context), [requested commands](run-to-completion.md#agent-mode-requested-commands), and followup questions.
2. Use a reasoning model to create a plan to carry out the task. You can refine the plan with AI, or edit it directly.
3. Automatically carry out the approved plan.

While Dispatch is executing a plan, it automatically runs commands and applies code changes. However, it will still obey your [command denylist](run-to-completion.md#command-denylist). The border along the left of the session will change color to indicate that Dispatch is running autonomously:
