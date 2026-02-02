---
description: >-
  Warp enables intelligent code generation and editing through AI-powered diffs,
  allowing you to review, refine, and apply changes seamlessly across your
  codebase.
---

# Code Overview

## From Prompt to Production

Warp Code is a suite of features designed to help you take agent-generated code from the initial prompt and project setup all the way to deployment and production. It is powered by Warp’s dedicated coding agent, which consistently ranks among the top results on [SWE-bench Verified](https://www.swebench.com/#verified) and [Terminal-Bench](https://www.tbench.ai/leaderboard).

In addition to Warp’s modern, [native code editor](code-editor/), it includes:

* [Codebase Context](codebase-context.md) for accurate, context-aware agent responses
* [Project Rules](../knowledge-and-collaboration/rules.md) and Commands to tailor agent behavior per repository
* A dedicated [Code Review](code-review/) experience for reviewing and editing diffs
* [Zero-state and setup flows](code-overview.md#getting-started-with-coding-in-warp) to quickly start a new project or initialize an existing one

### Coding Agent

Warp’s coding agent is designed to help you generate, edit, and manage code directly in the [Agentic Development Environment](https://www.warp.dev/blog/reimagining-coding-agentic-development-environment). It detects opportunities to apply code diffs and surfaces them inline, allowing you to review and apply changes without switching to an external IDE. When you need to make manual edits, you can open Warp’s native code editor.

### How It Works

* **Prompt-driven coding**: You write natural language prompts such as _“Add a retry mechanism to this API call”_ or _“Fix the failing unit test in auth.test.ts.”_
* **Inline code diffs**: When the agent proposes changes, it shows them as diffs you can inspect, modify, or reject.
* **Agent steering**: You can refine prompts, interrupt and retry, or attach context (such as a file, diff, or selection) to guide the agent toward better results.

{% embed url="https://screen.studio/share/VwLoR3BE" %}

{% hint style="info" %}
Warp's coding agent only works on local repositories. The agent can make changes on remote or docker repositories, but fallback to using terminal commands (i.e. `sed`, `grep` ) to make the changes.
{% endhint %}

### Examples of Coding Capabilities

Code responds to prompts related to code generation, editing, and analysis. Here are some examples:

* **Code creation**
  * “Write a function in JavaScript to debounce an input”
  * “Generate a Python class for managing user sessions with Redis.”
* **Error-driven fixes**
  * “Fix the TypeScript error shown in the last build output.”
  * “Resolve this merge conflict by keeping backend changes and updating tests accordingly.”
* **Refactoring**
  * “Update all instances of var to let in this file.”
  * “Extract the database logic from app.js into a new db.js module and update imports.”
* **Multi-file and repo-wide changes**
  * “Add headers to all .py files in this directory.”
  * “Replace requests with httpx across the codebase, updating imports and error handling.”
* **Complex workflows** (examples shown below — in practice, prompts should include more detail for best results)
  * “Implement OAuth2 authentication, update affected routes, and add tests.”
  * “Identify functions without test coverage and create Jest test files for them.”
  * “Optimize slow SQL queries in queries.sql and regenerate migrations.”

{% embed url="https://youtu.be/IuFSuOYstfg" %}
How to kick off a coding task
{% endembed %}

{% embed url="https://youtu.be/dm-P63USsVg" %}
How to interpret & edit Warp’s coding output
{% endembed %}

## Getting Started With Coding in Warp

Warp provides multiple entry points to begin coding with agents, whether you are starting a new project, opening an existing one, or cloning from GitHub. Each new tab shows a **zero state** that lets you choose how to proceed.

<figure><img src="../.gitbook/assets/code_mode.png" alt=""><figcaption><p>Zero-state tab with 3 starting points for agentic coding in Warp.</p></figcaption></figure>

#### 1. Starting a New Project

To begin a new project, select `Create a New Project` from the tab. You can start directly with a prompt (Warp will suggest ideas) or configure the project manually. Warp sets up the repository with an `AGENTS.md` file (filename must be in all caps) containing [project rules](../knowledge-and-collaboration/rules.md#project-rules) and enables [codebase indexing](codebase-context.md) to provide the agent with full context.

#### 2. Open an Existing Repo

Select `Open Repository` to use your computer's file picker. If you choose a Git repository, Warp automatically changes into the directory and runs the `/init` setup command (a built-in "[slash command](https://docs.warp.dev/agent-platform/agent/slash-commands)") if the repo has not already been initialized. Warp will detect the repository, index the codebase, and prepare it for coding.

* For non-Git folders, Warp simply changes into the directory without initialization.
* If you have an existing project that is not yet initialized, you can run `/init` manually to bootstrap it with a version-controlled `AGENTS.md` file.
* This view also shows a list of your three most recently used repositories and AI conversations for quick access, as well as a list of recent directories (which behave like running `cd`).

#### 3. Clone a Repo

Select `Clone Repository` to paste in a repo link or clone directly from GitHub. Warp places you in the cloned folder and automatically runs the `/init` flow to set up project rules and indexing.

## Learn More About Code Features:

* [Code Editor](code-editor/) - Warp’s built-in code editor lets you make quick, in-context edits with essentials like syntax highlighting, tabs, find and replace, Vim keybindings, and a file tree.
* [Codebase Context](codebase-context.md) - Warp indexes your Git-tracked codebase to help Agents understand your code and generate accurate, context-aware responses. No code is stored on Warp servers.
* [Code Review](code-review/) - review, edit, and manage Git diffs in real time, with options to attach, revert, or open files directly.
  * You can also enter [Interactive Code Review](code-review/interactive-code-review.md) to comment on changes, guide the agent, or adjust individual edits as they happen.
* [Code Diffs in Agent Conversations](reviewing-code.md) - Learn how to review, refine, and apply code changes generated by Warp’s agents using the built-in visual diff editor.
