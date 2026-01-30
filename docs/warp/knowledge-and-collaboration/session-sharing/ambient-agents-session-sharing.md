---
description: >-
  Ambient Agent Session Sharing lets you open, inspect, and continue steering
  remote agent runs in real time, all from a shared session viewable in Warp, on
  the web, or by forking into your local env.
---

# Ambient Agents Session Sharing

Ambient Agent Session Sharing lets you open, inspect, and continue interacting with agent tasks that are running on remote virtual machines. Whether an Ambient Agent was triggered from [integrations](https://docs.warp.dev/agent-platform/integrations/integrations-overview) like Slack, Linear, GitHub Actions, or the [Warp CLI](https://docs.warp.dev/reference/cli), you can view its full session, follow along in real time, ask follow-up questions, and even "fork" the work into your local Warp environment.

{% embed url="https://www.loom.com/share/edd662da8de345ae979c4d39eb19c513" %}

This makes Ambient Agent runs observable, steerable, and collaborative — even if they weren’t initiated from your machine.

***

### What it enables

With Ambient Agent Session Sharing, you can view the full remote session for an Ambient Agent run and:

* See every command the agent executed in the virtual environment
* Inspect context, logs, and outputs directly in Warp or the web viewer
* Ask follow-up questions or give additional instructions after the task completes
* Bring the conversation into your local Warp session with Fork to local
* Continue working on remote-generated code locally
* Share links so teammates can view or collaborate on the session

Everything is accessible whether or not Warp is installed on the viewer’s machine.

## How it works

#### 1. Open a remote Ambient Agent run

When an Ambient Agent starts working — for example, from a Slack mention, a Linear issue, or a [CLI](https://docs.warp.dev/reference/cli) trigger — Warp attaches a shareable link to the run.

* From [Slack](https://docs.warp.dev/agent-platform/integrations/slack), click **View Agent** in the agent response to open the session.
* From [Linear](https://docs.warp.dev/agent-platform/integrations/linear), click the ↗ **Warp** button ("Open in Warp") on the ticket to open the session.

You can also open the session directly in your browser without installing Warp. Here, you’ll see the complete agent session running on a cloud VM, including all steps, logs, and context.

#### 2. Inspect the session like it’s your own

Once the session loads, you can:

* Scroll through the Ambient Agent’s actions
* See the prompt, plan, and decisions it made
* Review the code or config changes it produced
* Understand what environment it executed in

You’re viewing a remote VM, but the UI behaves like a local Warp session.

#### 3. Keep chatting with the remote agent

Even if the Ambient Agent has completed its task, you can still ask follow-up questions or request more work. Warp sends your message back to the remote VM and continues the conversation.

Examples:

* “Can you explain which flag you changed?”
* “Give me a summary of what you modified.”
* “Show me the reasoning behind your last step.”

This works as long as the remote environment is still active.

#### 4. Handle inactive or shut-down sessions

Ambient Agent environments automatically shut down after a period of inactivity. When that happens, you’ll see a notice that the virtual machine has been stopped.

If you still want to continue the conversation or work on the code, you can click **Fork to local**.

#### 5. Fork the session to your local Warp

Forking brings the Ambient Agent conversation into your local machine, so you can pick up where the agent left off.

Once forked:

* The session appears as a normal conversation in your local Warp
* You can keep prompting the agent using all your local tools
* You can continue inspecting or modifying the generated code
* The agent responds using your local environment instead of the remote VM

**Note:** If the Ambient Agent created a new git branch or repository in the remote VM, you’ll need to clone that branch locally first so the agent can keep working on the same code. Warp will streamline this workflow in a future release.

### Viewing sessions across devices

Ambient Agent sessions can be viewed from:

* The Warp desktop app
* A browser via the web viewer
* Remote teammates using the shared link
* Local Warp sessions after forking

You get consistent visibility into the work regardless of where you open it.
