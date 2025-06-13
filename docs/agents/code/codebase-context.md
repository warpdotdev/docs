---
description: >-
  Warp generates a local, privacy-preserving outline of your Git-tracked
  codebase to help Agent Mode understand and answer questions about your code --
  only sharing context when explicitly approved.
---

# Codebase Context

In order for Agent Mode to be able to answer questions about about the code files in your codebase, Warp can generate an outline containing relevant information about each file. This outline can then be used when querying Agent Mode to find relevant files for a requested query.

{% hint style="warning" %}
No code indexed with codebase context is ever stored on our servers.
{% endhint %}

Outline generation works in the following way:

* When opening a new terminal pane or changing to a new directory in the terminal, check if this directory is a part of a Git repository.
* If it is in a Git repository, extract metadata from each code file in the repository.
  * Only file types for languages supported by Agent Mode are processed.
  * Files in `.gitignore` are not processed.
  * This metadata currently includes function names in the file, but this may expand.

The first time that a user opens a directory after the Warp application is opened, the outline for the repository is fully generated. Creating an outline for repositories can take a few minutes for large repositories. Codebase context will not be used in Agent Mode queries until the outline is generated.

Outline generation is completely local. The outline is only sent to the server when an Agent Mode request is made that could use the codebase context and the user approves sending codebase context for that directory.

After the outline is generated in full, Warp watches for changes to any file in the directory and the outline is updated as needed.

These outlines can then be used by Agent Mode to search for relevant files to answer questions about a codebase, or find relevant files to edit.

{% hint style="info" %}
You can disable generating codebase context outlines and using them for Agent Mode requests by disabling the "Codebase Context" setting.
{% endhint %}

#### Codebase context database

Warp saves the data from codebase context to local json files on your computer. You can open the files directly and inspect the full contents in the following location:

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
