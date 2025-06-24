---
description: >-
  Warp generates a local, privacy-preserving outline of your Git-tracked
  codebase to help Agents understand and answer questions about your code --
  only sharing context when explicitly approved.
---

# Codebase Context

For Warp Agents to answer questions about the code files in your codebase, Warp generates an outline containing relevant information about each file. Agents can then use this outline to identify the most relevant files for a given query.

{% hint style="warning" %}
No code indexed with Codebase Context is ever stored on our servers.
{% endhint %}

### How outline generation works

* When you open a new pane or change directories, Warp checks if the directory is part of a Git repository.
* If it is, Warp extracts metadata from each code file in the repository.
  * Only file types in languages supported by Warp's Agents are processed.
  * Files listed in `.gitignore` are excluded.
  * Metadata currently includes function names, though this may expand in the future.

The first time you open a directory after launching Warp, the outline for the repository is fully generated. This may take a few minutes for large repositories. Warp’s agents will not use codebase context until this outline is available.

### Outline behavior and privacy

Outline generation is completely local. The outline is only sent to the server when an agent request is made and you approve sending codebase context for that directory.

After the outline is generated in full, Warp watches for changes to any file in the directory and the outline is updated as needed.

These outlines can then be used by Warp's Agents to search for relevant files to answer questions about a codebase, or find relevant files to edit.

{% hint style="info" %}
You can disable both outline generation and the use of codebase context by turning off “Codebase index” under `Settings > Code > Codebase` index in Warp.
{% endhint %}

### Codebase context database

Warp saves codebase context outlines as local JSON files. You can view them directly at:

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
