---
description: >-
  Warp Scheduled Agents run ambient agents automatically on a cron schedule,
  enabling repeatable maintenance and cleanup tasks to execute reliably in the
  background without manual triggers.
---

# Scheduled Agents

Warp's Scheduled Agents let you run Ambient Agents automatically on a **recurring schedule**. They are designed for routine, repeatable tasks that should happen without manual intervention, such as dead code cleanup, dependency maintenance, issue triage, or periodic refactors.

{% embed url="https://www.youtube.com/watch?feature=youtu.be&v=wX9cDbsRXHs" %}

Scheduled Agents run in the background on Warp’s infrastructure. Each run starts from a clean session, executes a fixed prompt, and produces its own task and session history that can be inspected after the fact.

***

### What are Scheduled Agents?

A Scheduled Agent is an [Ambient Agent](../ambient-agents-overview.md) that runs on a cron-based schedule.

**Key characteristics:**

* Runs automatically based on a cron expression.
* Uses a fixed prompt defined at schedule creation time.
* Starts a fresh agent session for every run.
* Executes in a specific Warp Environment, if provided.
* Consumes AI credits when it runs.
* Can be paused, updated, or deleted at any time.

Scheduled Agents are ideal for work that should happen regularly and predictably, without needing a human to trigger the agent manually.

### Common Use Cases

Scheduled Agents are best suited for maintenance-style workflows, including:

* Dead code or unused feature flag cleanup.
* Dependency updates or security scans.
* Issue or PR triage on a recurring cadence.
* Periodic documentation refreshes.
* Repository hygiene tasks like formatting or lint checks.
* Scheduled reporting or audits.

Because each run is isolated, Scheduled Agents are safe to use for tasks that benefit from a clean, repeatable execution environment.

***

### Scheduling Agents with the Warp CLI

Warp Scheduled Agents are managed through the warp schedule family of CLI commands.

All scheduling operations require the Warp CLI and an authenticated session

#### Creating a Schedule

Use `warp schedule create` (with required flags) to define a new Scheduled Agent.

**Each schedule requires:**

* A name, for identification.
* A cron schedule.
* A prompt that the agent will execute.
* An optional environment in which the agent will run.
* An optional [model selection](https://docs.warp.dev/reference/cli/README#using-agent-profiles).
* [Optional MCP server configuration](../mcp-servers-for-agents.md).

```bash
warp schedule create \
  --name=NAME \
  --cron=SCHEDULE \
  --prompt=PROMPT \
  [--environment=ENVIRONMENT_ID]
```

{% hint style="info" %}
Currently, environments are never required - if you don't specify one, the scheduled agent runs in a barebones sandbox.
{% endhint %}

**Example**

The following command schedules an agent to clean up old feature flags every four days:

```bash
warp schedule create \
  --name "Feature Flag Cleanup" \
  --cron "0 10 */4 * *" \
  --prompt "Scan the repository for stale feature flags and remove any that are no longer referenced. Open a PR with the changes and include a summary." \
  --environment "KB1ndNMQAs5kjPdX2jatA8"
```

Once created, the agent will automatically run at the specified times without further action.

Scheduled Agents support the same [model selection](https://docs.warp.dev/reference/cli/) and [MCP server configuration](../mcp-servers-for-agents.md) as other Ambient Agent triggers. This allows you to control which model is used for scheduled runs and to equip agents with external tools via MCP, such as issue trackers, CI systems, or internal services.

#### Cron Schedule Format

Warp uses standard cron syntax to define schedules.

A cron expression consists of five fields:

```
minute hour day-of-month month day-of-week
```

For example:

* `0 10 * * *` runs every day at 10:00 AM.
* `0 10 */4 * *` runs every four days at 10:00 AM.
* `0 8 1 * *` runs at 8:00 AM on the first day of every month.

Make sure your cron expression reflects the cadence you want, as Scheduled Agents will run exactly according to this schedule.

### Listing Scheduled Agents

To view all Scheduled Agents for your team, use:

```bash
warp schedule list
```

This command prints a table with details about each schedule, including:

* Schedule ID
* Name
* Cron schedule
* Paused
* Last run time
* Next scheduled run
* Current status (active or paused)
* Scope

| ID     | Name                 | Schedule       | Last Ran                                     | Next Run              | Scope | Paused |
| ------ | -------------------- | -------------- | -------------------------------------------- | --------------------- | ----- | ------ |
| abc123 | Feature Flag Cleanup | `10 0 */4 * *` | `2025-11-24 10:00 AM<task id><session link>` | `2025-11-28 10:00 AM` | Team  | No     |
| def456 | Issue Triage         | `8 0 0 1 * *`  | `2025-11-24 10:00 AM<task id><session link>` | Paused                | -     | Yes    |

Each completed run also includes links to:

* The task created by the agent.
* The full agent session, including logs and outputs.

This makes it easy to audit what ran, when it ran, and what the agent did.

#### Viewing a Specific Scheduled Agent

Use `warp schedule get` to view detailed information about a single Scheduled Agent.

```bash
warp schedule get SCHEDULE_ID
```

This command returns additional details not shown in the list view, including:

* Full schedule configuration
* Prompt and model configuration
* Environment and MCP settings
* Recent runs and execution metadata
* Links to related tasks and agent sessions

This is useful when auditing behavior, debugging failures, or reviewing how a Scheduled Agent is configured.

### Pausing and Unpausing Schedules

Scheduled Agents can be temporarily disabled without deleting them.

```bash
warp schedule pause SCHEDULE_ID
```

When paused, the agent will not run at its scheduled times.

**Example**

```bash
warp schedule pause abc123
```

#### Unpausing a Schedule

```bash
Unpausing a Schedule
```

Once unpaused, the agent resumes running according to its original cron schedule.

### Editing Scheduled Agents

You can modify an existing schedule using warp schedule update.

You may update one or more properties at a time, including:

* The schedule name.
* The cron schedule.
* The prompt used for future runs.
* The environment used for execution.
* The model and MCP configuration used for future runs.

#### Command

```bash
warp schedule update SCHEDULE_ID \
  [--name=NAME] \
  [--schedule=SCHEDULE] \
  [--prompt=PROMPT] \
  [--environment=ENVIRONMENT_ID]
```

#### Examples

Change when a scheduled agent runs, leaving everything else unchanged:

```bash
warp schedule update abc123 --schedule "0 9 */4 * *"
```

Update the environment used for future runs:

```bash
warp schedule update abc123 --environment=jkl789
```

Changes apply only to future runs. Past runs and their session history remain unchanged.

### Deleting a Scheduled Agent

To permanently remove a schedule, use:

```bash
warp schedule delete SCHEDULE_ID
```

**Example**

```bash
warp schedule delete abc123
```

Deleting a schedule immediately stops all future runs. Previous runs and their session history remain accessible for auditing and review.

***

### Execution Model and Behavior

Each scheduled run behaves like a standard Ambient Agent run, with a few important guarantees:

* Every run starts a fresh session.
* No state is carried over between runs unless your environment explicitly persists data.
* Runs execute automatically without human intervention.
* All usage is billed to the team’s shared AI credit balance.

If a scheduled run fails, it does not block future runs. Each execution is independent.

### Permissions and Responsibility

Scheduled Agents are created and managed by authorized users on a Warp team.

By creating a Scheduled Agent, you are responsible for:

* The cron schedule and how often the agent runs.
* The instructions provided in the prompt.
* The environment and integrations the agent has access to.
* The AI credits consumed by scheduled executions.

Carefully review prompts and schedules before deploying them broadly, especially for agents that can modify production code or infrastructure.

### When to Use Scheduled Agents vs Triggers

Scheduled Agents are best when work should happen on a predictable cadence.

If you want an agent to run in response to an event, such as a Slack mention, PR update, or issue change, use triggered Ambient Agents instead.

Many teams use both together: triggers for reactive workflows, and Scheduled Agents for proactive maintenance.
