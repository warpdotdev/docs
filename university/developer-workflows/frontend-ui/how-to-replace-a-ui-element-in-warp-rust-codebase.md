---
description: >-
  Replace UI elements across a large Rust codebase using Warp's agentic
  workflow with live diff review.
metaLinks:
  alternates:
    - >-
      https://app.gitbook.com/s/c5dAwvMCRiTxUOdDicqy/developer-workflows/frontend-ui/how-to-replace-a-ui-element-in-warp-rust-codebase
---

# How To: Replace A UI Element in Warp (Rust Codebase)

Learn how to use Warp’s AI coding features to make live code changes — in this example, replacing an icon throughout Warp’s massive Rust codebase using an agentic workflow.

{% embed url="https://youtu.be/V2pwBN6Vt7k" %}

{% hint style="info" %}
This demo showcases Warp’s ability to safely make intelligent code changes within a multi-million-line codebase by providing structured prompts, reviewing diffs in real time, and letting the agent compile and self-correct.
{% endhint %}

{% stepper %}
{% step %}
#### Define the Task

The goal here is to replace all instances of the **sparkle icon** with the new **agent icon**, especially within the history menu.

Open your project in Warp and start by prompting the agent directly (either by typing or speaking):

```
Please create a new branch for me according to the format in the attached Linear URL.

I’ve attached screenshots of what the agent mode and sparkle icons look like.
I would like you to understand those icons, search for their use in the code,
and wherever we’re using sparkles, replace them with the agent mode icon.
Specifically, make sure this happens in the history menu.
Please give me a plan before making any coding changes.
```

Attach any relevant Linear issue links or screenshots to help the agent identify assets accurately.
{% endstep %}

{% step %}
#### Review the Plan

Warp’s agent parses your request and generates a plan for code edits.\
It identifies files and functions where the sparkle icon is used.

If the plan looks correct, approve it to proceed.

Follow-up prompt example:

```
Yes, proceed — and please rename the function from renderAISparklesIcon
to something like renderAgentModeIcon.
```

Warp automatically updates function names, asset references, and component usage.
{% endstep %}

{% step %}
#### View AI Diffs in Real Time

Warp lets you view live diffs as the agent edits your files.

* Diffs show changes to both render logic and function naming.
* You can choose to auto-accept or manually review diffs.
* These settings can be adjusted under AI Settings → Apply Changes Automatically.

{% hint style="info" %}
Note: The demo runs with “auto-accept” enabled, allowing Warp to apply diffs as soon as they’re validated.
{% endhint %}
{% endstep %}

{% step %}
#### Compilation and Fixes

After editing, Warp’s agent runs:

```bash
cargo check
```

to verify compilation.

If compilation fails (e.g., missing imports), the agent automatically corrects and retries — mimicking a human debugging process.
{% endstep %}

{% step %}
#### Testing the Change

Once compiled:

* Run your project locally to confirm visual changes.
* Check that the agent icon now replaces the sparkle icon in all targeted locations.
{% endstep %}

{% step %}
#### Recap

Warp’s agent completed the full flow:

1. Understood a Linear ticket and visual context
2. Created a new branch
3. Planned and executed the icon replacement
4. Auto-fixed compile issues
5. Verified the final result in-app
{% endstep %}
{% endstepper %}
