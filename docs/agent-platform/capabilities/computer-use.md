---
description: >-
  Computer Use allows agents to interact with desktop environments by taking
  screenshots, clicking, typing, and controlling the GUI in sandboxed cloud
  environments for testing and automation.
---

# Computer Use

Computer Use is an experimental feature that enables Warp's agents to interact with desktop environments. The agent can see what's displayed on screen, click and drag, type text, use keyboard shortcuts, and perform other GUI interactions—all within a secure, isolated sandbox.

A key use case is **testing UI changes** with a self-contained feedback loop, where the agent can verify that your code changes produce the expected visual and behavioral results without requiring manual testing.

## Overview

With Computer Use, agents can:

* **Take screenshots** - Capture and analyze the current display
* **Interact with applications** - Click buttons, fill forms, navigate interfaces
* **Type and control keyboard** - Enter text and use keyboard shortcuts
* **Automate testing workflows** - Test UI changes end-to-end without manual intervention
* **Work with browser-based interfaces** - Test web apps and navigate the web

Computer Use is only available in Warp's sandboxed cloud environments, not in local interactive terminal sessions.

***

## Enabling Computer Use

Computer Use is **opt-in** and disabled by default. You can enable it through several entry points:

### Warp App Settings

To enable Computer Use for [Cloud Agents](../cloud-agents/overview.md), navigate to **Settings** > **AI** > **Experimental** > **Computer use in Cloud Agents** and toggle to enable.

### CLI

When running agents in the cloud via the [CLI](https://docs.warp.dev/reference/cli), use flags to control Computer Use per run:

```bash
oz agent run-cloud --computer-use --prompt "<task>"
oz agent run-cloud --no-computer-use --prompt "<task>"
```

### API

When calling the Warp API to create agent runs, include the `computer_use_enabled` field in your request:

```json
{
  "prompt": "Build a button component that matches this design, then test it in the browser",
  "computer_use_enabled": true,
  "environment_id": "optional-environment-id"
}
```

For full API documentation, see the [Oz Agent API & SDK](https://docs.warp.dev/reference/api-and-sdk/) reference.

### Web App

In the Warp web app, you can enable or disable Computer Use for:

* **New agent runs** - Configure Computer Use when starting a new agent run from the web app
* **Scheduled agent runs** - Enable Computer Use for scheduled agents managed from the web app
* **Integrations** - Configure Computer Use for Slack, Linear, and other integration-triggered agents

***

## How Computer Use works

### Setup and requirements

Computer Use runs in a containerized sandbox, allowing headless cloud environments to render and interact with graphical applications. The sandbox is fully isolated—it does not have access to your local machine, credentials, or sensitive data outside the sandbox environment.

Your cloud environment must include any applications you want the agent to control. For example, to test a web app in a browser, install Chrome or Firefox in your [environment configuration](../cloud-agents/environments.md).

### Model selection

Computer Use currently uses **Claude Opus 4.6**. Support for choosing your own model is coming soon.

***

## Security considerations

Computer Use is an experimental feature with unique security considerations. These risks are heightened when interacting with the internet.

To minimize risks when using Computer Use:

1. **Avoid sensitive data** - Do not pass API keys, authentication tokens, or personal information to agents using Computer Use
2. **Limit internet access** - If your environment has internet access, consider restricting to an allowlist of known-safe domains
3. **Require human confirmation** - For tasks with real-world consequences (e.g., financial transactions, accepting legal terms), ask a human to confirm before the agent proceeds
4. **Review agent actions** - Regularly review what agents are doing on your behalf, especially when testing new workflows

***

## Example workflows

### Testing UI changes

Verify that code changes produce the expected visual results and behavior:

* **Build from mockups** - Receive a Figma design or mockup image, build the UI, and test it matches
* **Visual regression testing** - After code changes, verify UI renders correctly
* **Form and interaction testing** - Test form submissions, validation, error handling
* **Responsive design validation** - Test layout on different screen sizes

**Example: Testing a React component**

1. You ask the agent: "Build a React button component that matches this design, then test it"
2. Agent takes a screenshot to see the current state
3. Agent opens your dev server in a browser
4. Agent navigates to the component, verifies it renders correctly
5. Agent tests interactions (hover, click) and reports back

**Example: Testing a web form**

1. You provide a form design and ask the agent to build and test it
2. Agent renders your form in the browser
3. Agent fills fields with valid and invalid data
4. Agent verifies validation messages and submission behavior
5. Agent reports which fields worked correctly and which need adjustment

**Example: Verifying UI responsiveness**

1. You ask the agent to test your app on different screen sizes
2. Agent resizes the browser window to mobile, tablet, and desktop widths
3. Agent takes screenshots at each size and verifies layout is correct
4. Agent reports any responsive design issues

### Browsing and web interaction

Computer Use can also help with general web tasks:

* Browse websites and interact with web interfaces
* Fill out and submit web forms
* Navigate multi-step workflows in web applications

***

## Related capabilities

* [Images as Context](../local-agents/agent-context/images-as-context.md) - Pass design mockups and screenshots as context
* [Full Terminal Use](full-terminal-use.md) - Let agents drive interactive terminal apps, see live output, and run commands
