---
metaLinks:
  alternates:
    - >-
      https://app.gitbook.com/s/c5dAwvMCRiTxUOdDicqy/mcp-servers/sentry-mcp-fix-sentry-error-in-empower-website
---

# Sentry MCP: Fix Sentry Error in Empower Website

{% hint style="info" %}
This tutorial is based solely on the provided transcript. It teaches how to use the **Sentry MCP Server** within Warp to fetch live error data from Sentry, analyze stack traces, and automatically generate fixes for issues in your codebase.
{% endhint %}

{% embed url="https://youtu.be/rrxfS9u1XRA?si=fVUfjQJSOlyLFBJT" %}

### Overview

The **Sentry MCP server** gives Warp’s AI agents access to authenticated Sentry error data.\
This enables detailed diagnostics and automated fixes that would otherwise be impossible using AI alone.

You’ll learn how to:

* Connect the Sentry MCP server inside Warp.
* Trigger live error retrieval from Sentry.
* Diagnose code issues and generate patches automatically.
* Integrate Sentry debugging into your daily development loop.

{% stepper %}
{% step %}
#### Set Up the Sentry MCP Server

Open the MCP panel in Warp:

* Mac: Cmd + Shift + P
* Windows/Linux: Ctrl + Shift + P\
  Search for “MCP” and select the **MCP Panel**.

Click **Add**, then paste your configuration:

{% code title="sentry-mcp-config.json" %}
```json
{
  "sentry": {
    "command": "npx",
    "args": [
      "-y",
      "mcp-remote@latest",
      "https://mcp.sentry.dev/mcp"
    ],
    "env": {},
    "working_directory": null
  }
}
```
{% endcode %}

Save the configuration and ensure it appears in the MCP panel.
{% endstep %}

{% step %}
#### Run Your App and Trigger an Error

We're using the [**Empower Plant** repository](https://github.com/sentry-demos/empower) — Sentry’s official demo project. This fake e-commerce app includes a React frontend and multiple backends, each containing intentional bugs for testing.

Run the app locally:

```bash
npm install
npm start
```

Open the site in your browser and trigger a few known errors.
{% endstep %}

{% step %}
#### Capture the Error in Sentry

1. Go to your **Sentry Dashboard**.
2. Locate the triggered issue (for example, a `TypeError`).
3. Copy the issue’s URL from the Sentry interface.

Example:

```
https://sentry.io/organizations/demo/issues/12345/
```
{% endstep %}

{% step %}
#### Diagnose the Error Using Warp

Back in Warp, prompt the AI agent to fetch and analyze the issue:

```
Diagnose this Sentry error and show where it’s coming from in my code.
Create a fix.
```

The Sentry MCP calls `getIssueDetails`, fetching the stack trace and error metadata directly from Sentry. Warp then scans your local codebase, cross-references the error location, and identifies the root cause.

From this example:

> The issue was caused by calling `.toUpperCase()` on an array instead of a string.

Warp’s agent automatically writes a fix — changing the code to handle the array properly.
{% endstep %}

{% step %}
#### Apply the Generated Fix

Warp produces a suggested code change inline. Review the diff and apply it automatically with one click.
{% endstep %}

{% step %}
#### Integrate Into Your Workflow

Use Sentry MCP whenever you encounter production or staging errors. Warp can pull the latest issues, analyze them, and suggest patches.

Ideal for:

* Debugging live production errors.
* Triaging complex stack traces.
* Creating immediate hot-fixes without switching tools.

{% hint style="success" %}
With Sentry MCP, Warp becomes a live debugging console — connecting your code editor, terminal, and Sentry into a single intelligent feedback loop.
{% endhint %}
{% endstep %}
{% endstepper %}
