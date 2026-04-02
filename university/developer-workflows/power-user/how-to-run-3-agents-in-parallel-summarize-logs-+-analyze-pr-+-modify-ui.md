---
description: >-
  Run multiple agents simultaneously in Warp to modify UI, analyze PRs, and
  summarize logs in parallel.
metaLinks:
  alternates:
    - >-
      https://app.gitbook.com/s/c5dAwvMCRiTxUOdDicqy/developer-workflows/power-user/how-to-run-3-agents-in-parallel-summarize-logs-+-analyze-pr-+-modify-ui
---

# Run 3 Agents in Parallel

{% hint style="info" %}
This educational module demonstrates Warp’s multi‑threading features — running coding, debugging, and analysis tasks simultaneously in multiple agent tabs.
{% endhint %}

{% embed url="https://youtu.be/3jwus1bfKv4" %}

***

### 🧠 Overview

Warp allows you to launch several agents at once, each focused on a separate task.\
In the demo, we run three parallel workflows:

* Modify UI behavior
* Analyze team code reviews
* Summarize logs from production

{% stepper %}
{% step %}
#### Launch Agents in Parallel

Each agent runs in its own tab.

{% tabs %}
{% tab title="UI Fix" %}
Remove the background and border from unfocused input panes.

{% code overflow="wrap" %}
```
I'd like to make a coding change. Please create a new branch to do this.

What i want to do is for the Universal Developer Input, remove the border and background if it's being rendered in the same pane that is not focused. Please look at the reference file and at the attached screenshot. In the screenshot, you'll see what it looks like right now - there are two equally prominent input areas, even though one is focused and one is not. What I want to do is make the non-focused one not have a border and not have a background. 

Please check out this linear issue for more information. Also, give me a plan before you make any changes.
```
{% endcode %}
{% endtab %}

{% tab title="Code Review Check" %}
Analyze how many pull requests a team member has assigned.

{% code overflow="wrap" %}
```
Use the Github CLI tool to summarize all open PRs for review that are assigned to user. I'd like to see who is the author of the PR, when was it opened, how long has it been open for, which repo is it in, are there open an dunaddressed commens on it, and is it ready for review?
```
{% endcode %}
{% endtab %}

{% tab title="Log Analysis" %}
Summarize Cloud Run logs by error severity.

{% code overflow="wrap" %}
```
Use the gcloud tool to list all my open projects. Once you've done that, let me select a project. Once I've selected a project, we will want to see all the Cloud Run instances that are available. Then once I've picked a Cloud Run instance, I'd like to get a sumary of the last 2000 logs from that Cloud Run instance to see the history histogram of different types of logging on info, warning, and error levels.
```
{% endcode %}
{% endtab %}
{% endtabs %}
{% endstep %}

{% step %}
#### Monitor All Agents

The **task pane** in Warp shows all running agents.\
You can view plans, progress, and results live without interrupting other tasks.
{% endstep %}

{% step %}
#### Review Results

* **Coding Agent:** Implements UI fixes accurately.
* **Code Review Agent:** Reports 26 open PRs (identifies bottlenecks).
* **Log Agent:** Analyzes 1,000 log entries, categorizing errors and flagging Gemini API issues.
{% endstep %}

{% step %}
#### Why This Matters

Warp multi‑agent execution allows you to:

* Run multiple tasks without context switching.
* Keep coding, debugging, and ops visible simultaneously.
* Use AI assistants collaboratively for faster iteration.

{% hint style="success" %}
Multi‑agent workflows let you debug, code, and analyze in parallel — boosting throughput without leaving the terminal.
{% endhint %}
{% endstep %}
{% endstepper %}
