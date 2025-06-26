---
description: >-
  Warp generates a local, privacy-preserving outline of your Git-tracked
  codebase to help Agents understand your code and provide the most relevant,
  tailored responses.
---

# Codebase Context

Codebase Context helps Warp Agents understand your project by indexing your local codebase. This allows Agents to generate more accurate completions, suggest context-aware edits, and answer questions using real knowledge of your code.

{% hint style="warning" %}
Indexing happens locally. Code indexed with Codebase Context is never uploaded or stored on our servers.
{% endhint %}

<figure><img src="../../.gitbook/assets/codebase-context-main.png" alt=""><figcaption><p>Codebase indexing settings in Warp. Easily track sync status and manage which folders are indexed for AI-powered context and suggestions.</p></figcaption></figure>

## Indexing your codebase

When you open a directory in Warp, we check if it is part of a Git repository. If it is, Warp will begin generating a local outline of the project. This outline helps agents:

* Understand your project structure and reference relevant parts of the codebase
* Generate code that matches your style and apply edits in the right places

The outline includes basic metadata such as file paths and function names. It is kept up to date as you make changes to your code.

{% hint style="info" %}
You can view and manage your indexed codebases under `Settings > Code > Codebase Index`. You can also choose whether to automatically index new folders as you navigate them.
{% endhint %}

The first time you open a directory after launching Warp, the codebase outline will be generated from scratch. For larger projects, this may take a few minutes. Warp Agents will not use codebase context until the outline is complete, but **agentic coding features remain fully available during this time.**

### **Codebase indexing states**

When viewing indexed codebases in Warp under `Settings > Code`, you may see different status indicators:

* **Synced** — Indexing is complete and the codebase is ready to be used as context.
* **Discovering files** – Warp is currently scanning and indexing files in the codebase.
* **Failed** – Indexing failed. Common reasons include unreadable `.git` directories or corrupted repositories. Try recloning the repo and syncing again.
* **Codebase too large** – The number of files in the codebase exceeds your current plan’s limit. You can either reduce the number of files being indexed using `.warpindexingignore`, or [contact sales](https://warp.dev/contact-sales) for support with larger codebases.

<figure><img src="../../.gitbook/assets/codebase-context-statuses.png" alt=""><figcaption><p>View and manage the indexing status of your codebases in Warp. Easily see which projects are synced, in progress, or require attention.</p></figcaption></figure>

### When does codebase syncing happen?

Warp automatically triggers a codebase sync periodically and whenever a new Agent conversation begins. However, if many files have changed or the network is slow, the sync may not complete before the Agent tries to access context.

{% hint style="info" %}
In large projects (e.g. after a branch switch), there may be a short delay where the Agent rerefernces stale or outdated files.
{% endhint %}

### Ignore files

For large codebases, Warp supports several ignore files to give you control over what gets indexed. This allows each developer to focus context on the parts of the codebase most relevant to their work.

Warp respects the following ignore files:

* `.gitignore`
* `.warpindexingignore`
* `.cursorignore`
* `.codeiumignore`

Use these files to skip indexing of folders, generated files, or any content you don't want agents to reference. This can improve performance and result quality.

### File and Codebase Limits

The number of codebases you can index and the maximum number of files per codebase vary by plan. All plans support indexing **at least 5,000 files per codebase**, with higher tiers including support for more files and additional codebases.

For full details, visit our [pricing page](https://www.warp.dev/pricing).

## Multi-repo context

Warp supports referencing context across multiple indexed repositories. Note that you don’t need to be inside a specific repo for agents to use its context.&#x20;

**This is especially useful when:**

* Implementing a feature across multiple repos, such as full-stack work across client and server
* Using one repo as a reference while building in another, for example: “copy the implementation from repo A into my repo B”

Agents will only reference other repositories if they are already indexed. During cross-repo tasks, Warp's Agents have access to the file paths of all indexed repos. It is more likely to use cross-repo context when you mention the exact name of the repo in your prompt.

## Privacy and storage

Codebase Context is stored locally on your machine. Warp only sends this context to the server when you trigger an Agent request and explicitly approve using it for that directory.

Once indexing is complete, Warp continuously watches for file changes and updates the outline automatically. Agents use this outline to search for relevant files, answer questions, and determine which files to edit.

You can view these outlines directly as local JSON files at:

{% tabs %}
{% tab title="macOS" %}
```bash
cd "$HOME/Library/Application Support/dev.warp.Warp-Stable/codebase_index_snapshots"
```
{% endtab %}

{% tab title="Windows" %}
```powershell
Set-Location $env:LOCALAPPDATA\warp\Warp\data\codebase_index_snapshots
```
{% endtab %}

{% tab title="Linux" %}
```bash
cd "${XDG_STATE_HOME:-$HOME/.local/state}/warp-terminal/codebase_index_snapshots"
```
{% endtab %}
{% endtabs %}
