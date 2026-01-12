# Managing Ambient Agents

Warp provides a centralized management view where you can monitor agent activity across your account and (where applicable) your team. It’s designed to answer, at a glance:

* Which agents have been running recently (and what’s running right now)
* Which runs succeeded, failed, or were canceled
* Where an agent was triggered from (a local agent conversation, the Warp CLI, Slack, etc.)
* How many AI credits those runs consumed

{% embed url="https://www.loom.com/share/679c267ddd2d44519abf79edcb1122c7" %}

This management view includes your **local (interactive) agents** and [Ambient Agent](../ambient-agents-overview.md) runs.&#x20;

***

### What appears in the management view

The management view includes two categories of agent activity.

#### Interactive agents

* Initiated from the Warp desktop app.
* The conversation is owned by you. It opens locally in Warp, and can be shared via a link when needed.
* Credit usage reflects inference.

#### Ambient agent runs

* Background executions initiated by triggers such as integrations and automations (for example: Slack, Linear, schedules, GitHub Actions, or API/CLI invocations).
* Each run produces a shared session that can be inspected after completion (including logs, messages, and outputs).
* Credit usage reflects inference + compute, shown as a single combined value in this view.

{% hint style="warning" %}
All usage rolls up into Warp’s standard [**AI credit**](../../support-and-billing/plans-and-pricing/ai-credits.md) system. There is no separate billing unit for compute versus inference; both contribute to the same credit balance.
{% endhint %}

In the **Personal** tab, you can view all of the interactive and Ambient Agent conversations that you own. In the **All** tab, you can see everything from the personal tab, as well as any ambient sessions that are shared with you by your teammates; right now, this only includes things triggered from integrations.

***

### The agents list

Each row represents a single item in the management view (either an interactive conversation or an ambient run). The list is intended to be scannable: you should be able to understand “what happened” without opening anything.

#### Fields you’ll see

**Source**

Where the agent was launched from. Common sources include:

* **Interactive:** an [agent conversation](../../agents/agents-overview.md) started in the Warp app
* **CLI**: a local run triggered by the [Warp CLI](../../platform/cli/)
* **API**: a run triggered by [Warp’s API](../../platform/agent-api-and-sdk/)
* **Slack / Linear**: runs triggered by [integrations](../../integrations/integrations-overview.md)
* **Scheduled**: runs triggered on a [cron schedule](scheduled-agents.md)

**Status**

Warp uses a small set of statuses to help you quickly identify what needs attention:

<table><thead><tr><th width="173.375">Status</th><th width="78.41973876953125">Icon</th><th>Description</th></tr></thead><tbody><tr><td><code>Working</code></td><td>N/A</td><td>in progress (may include queued / running states)</td></tr><tr><td><code>Blocked</code></td><td>🟨</td><td><p><em>(interactive only)</em></p><p><br>the conversation is waiting on user input or a required step</p></td></tr><tr><td><code>Canceled</code></td><td>⬜️</td><td>(interactive only)<br><br>the interactive conversation was canceled before completion</td></tr><tr><td><code>Failed / Errored</code></td><td>🔺</td><td>something went wrong (applies to both interactive and ambient)</td></tr><tr><td><code>Success</code></td><td>✅</td><td>completed successfully (applies to both interactive and ambient)</td></tr></tbody></table>

**Duration (for Ambient Agent tasks)**

* Shown for ambient runs to indicate how long the task executed.
* Note: Interactive conversations generally don’t map cleanly to a single “run duration,” so this is currently omitted.&#x20;

***

### Inspecting an agent

**The primary interaction is simple:**

* Clicking an ambient row opens the [shared session](../../knowledge-and-collaboration/session-sharing/agent-session-sharing.md) for that run (logs/messages/output).
* Clicking an interactive row opens the conversation locally in the Warp app.

This makes the management view a navigation surface: find the thing you care about, click once, and you’re in the right context to inspect or continue work.

### Filtering

In both _Personal_ and _All_ views, you can open the filter menu and filter by:

* Source (interactive, API, CLI, Slack/Linear, scheduled)
* Day of creation
* Creator
* Status

This is the fastest way to isolate “everything that failed today,” “runs from Slack,” or “what a specific teammate triggered via integrations.”<br>
