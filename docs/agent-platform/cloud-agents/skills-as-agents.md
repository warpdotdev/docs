---
description: >-
  Run agents based on skills for consistent, repeatable workflows.
  Use skills with local or cloud agents from the CLI, Oz web app, API, or on a schedule.
---

# Skills as Agents

You can start an agent from a [skill](../warp-agents/skills.md)—a reusable set of instructions that defines what the agent should do. When you run an agent based on a skill, the skill provides the base prompt and behavior, while you supply additional context for that specific run.

Skills work with both **local agents** (running on your machine) and **cloud agents** (running in Warp's infrastructure).

This is useful when you want:

* **Consistent behavior** — The same skill produces the same workflow every time, regardless of who triggers it or where it runs.
* **Repeatable automation** — Run skills on schedules for maintenance tasks like code cleanup, dependency updates, or issue triage.
* **Shareable workflows** — Skills live in repositories, so your team can version, review, and collaborate on agent behavior.

***

## How Skills become available

Skill discovery depends on whether you're running a local or cloud agent.

### Local agents

For local agent runs (`oz agent run`), skills are automatically discovered from your current repository. Warp scans these directories in order of precedence:

* **`.warp/skills/`**
* **`.agents/skills/`**
* **`.claude/skills/`**
* **`.codex/skills/`**
* **`.cursor/skills/`**
* **`.gemini/skills/`**
* **`.copilot/skills/`**
* **`.factory/skills/`**
* **`.github/skills/`**
* **`.opencode/skills/`**

You can also specify a skill from any accessible repository using the fully qualified format: `owner/repo:skill-name`.

### Cloud agents

For cloud agent runs (`oz agent run-cloud`), skills are discovered from repositories configured in your [environments](environments.md).

**Discovery workflow:**

1. **Create a skill** in your repository (see [Creating skills](../warp-agents/skills.md#creating-skills))
2. **Add the repository** to an environment
3. **The skill appears** in the Agents list in the Oz web app

{% hint style="info" %}
You can also list available skills programmatically using the `GET /agent` endpoint. See the [Oz API](https://docs.warp.dev/reference/api-and-sdk) reference for details.
{% endhint %}

***

## Running skill-based agents

You can start an agent from a skill using multiple entry points.

### Oz web app

The [Oz web app](oz-web-app.md) at [oz.warp.dev](https://oz.warp.dev) provides a visual interface for running skill-based agents. From the web app, you can:

* Browse all skills available from your environments on the **Agents** page
* View suggested agents from Warp's public [oz-skills repository](https://github.com/warpdotdev/oz-skills)
* Start a new run by selecting a skill, environment, and prompt
* Create scheduled agents that run skills on a cron schedule

For a complete walkthrough of the web app interface, see [Oz Web App](oz-web-app.md).

### CLI

Use the `--skill` flag with the Oz CLI:

```sh
# Run locally with a skill
oz agent run --skill "owner/repo:skill-name" --prompt "additional context"

# Run in the cloud with a skill
oz agent run-cloud \
  --environment <ENV_ID> \
  --skill "owner/repo:skill-name" \
  --prompt "additional context"
```

For full CLI documentation, see [Using skills](https://docs.warp.dev/reference/cli#using-skills) in the CLI reference.

### API & SDK

Use the `skill_spec` parameter when creating a run:

```json
{
  "prompt": "additional context for this run",
  "config": {
    "environment_id": "<ENV_ID>",
    "skill_spec": "owner/repo:skill-name"
  }
}
```

For full API documentation, see [Agent configuration](https://docs.warp.dev/reference/api-and-sdk#agent-configuration) in the API reference.

***

## Running skills on a schedule

One of the most powerful uses for skill-based agents is running them on a schedule. [Scheduled agents](triggers/scheduled-agents.md) execute automatically at specified times, making them ideal for:

* **Dead code cleanup** — Weekly scans for unused code or stale feature flags
* **Dependency updates** — Daily or weekly checks for security updates
* **Issue triage** — Regular categorization and prioritization of open issues
* **Documentation refresh** — Periodic updates to keep docs in sync with code

**Creating a scheduled skill-based agent:**

```sh
oz schedule create \
  --name "Weekly Code Cleanup" \
  --cron "0 10 * * 1" \
  --environment <ENV_ID> \
  --prompt "Scan for dead code and unused feature flags. Open a PR with removals."
```

You can also create schedules from the [Oz web app](oz-web-app.md) using the **New schedule** action.

For full scheduling documentation, see [Scheduled Agents](triggers/scheduled-agents.md).

***

## Suggested Skills

The [Oz web app](oz-web-app.md) displays suggested agents from the public [warpdotdev/oz-skills](https://github.com/warpdotdev/oz-skills) repository. These are pre-built skills that demonstrate common use cases and can be used as starting points for your own workflows.

Suggested skills appear on the Agents page under the **Suggested** filter.

***

## Related resources

* [Skills](../warp-agents/skills.md) — How to create skills and skill file format
* [Environments](environments.md) — Configure repositories and runtime context for cloud agents
* [Scheduled Agents](triggers/scheduled-agents.md) — Run agents automatically on a cron schedule
* [Oz Web App](oz-web-app.md) — Visual interface for managing cloud agents
* [Oz CLI](https://docs.warp.dev/reference/cli) — Command-line interface for running agents
* [Oz API & SDK](https://docs.warp.dev/reference/api-and-sdk) — Programmatic access to cloud agents
