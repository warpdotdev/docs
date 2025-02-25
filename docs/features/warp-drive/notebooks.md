---
description: Save interactive playbooks to simplify onboarding and development.
---

# Notebooks

## What is a notebook?

Notebooks are runnable documentation consisting of markdown text and list elements, code blocks, and runnable shell snippets that can be automatically executed in your terminal session. Notebooks are searchable and accessible through the [Command Palette](../command-palette.md) so you can access and run your documentation without ever leaving the terminal. You can also export Notebooks in .md format at any time.

## How to save and edit notebooks

You can create a new notebook from various entry points in Warp

{% tabs %}
{% tab title="macOS" %}
* From Warp Drive, + > New notebook
* From the [Command Palette](../command-palette.md), create a new team or personal notebook.
* With a keyboard shortcut, `SHIFT-CMD-J`
{% endtab %}

{% tab title="Linux" %}
* From Warp Drive, + > New notebook
* From the [Command Palette](../command-palette.md), create a new team or personal notebook.
* With a keyboard shortcut, `SHIFT-CTRL-J`
{% endtab %}
{% endtabs %}

Any of these entry points will open the notebook editor where you can:

* Title your notebook.
* Start adding text and code elements.

{% hint style="info" %}
Note: The notebook will not be saved until either title or body text is added.
{% endhint %}

<figure><img src="../../.gitbook/assets/notebooks_editor.gif" alt=""><figcaption><p>Editing a Notebook</p></figcaption></figure>

### Import existing documentation

Existing markdown `.md` documentation can also be directly imported into Warp Drive. To import your markdown file(s):

* From Warp Drive, + > Import > then follow the file selection dialog.

<figure><img src="../../.gitbook/assets/notebook-import-modal.png" alt=""><figcaption><p>Notebook import modal</p></figcaption></figure>

### Export notebooks from Warp Drive

From Warp Drive, select the overflow menu for the Notebook you'd like to export and then Export. You will then be prompted to open the file in .md format.

## Working with notebooks

### Adding new elements

Notebook elements (text, code, list items) can be added in several ways:

* Using the appropriate markdown shortcut (e.g. ### for Heading 3).
* Typing /, which will open up a selection menu of supported elements.
* Pressing the + icon which appears when hovering over a line and selecting from the menu of supported elements.

<figure><img src="../../.gitbook/assets/markdown-element-types.png" alt=""><figcaption><p>Markdown element types</p></figcaption></figure>

### Styling existing elements

Existing notebook elements can be styled in several ways:

* Selecting an existing element and selecting text decorations (like bold, italics, or inline code) from the hover menu.
* Using markdown syntax for text stylings like \*\*bold\*\* or \*italic\*.
* Selecting an existing element and changing the overall type of the element via the dropdown element menu.

<div data-full-width="true"><figure><img src="../../.gitbook/assets/styling-menu.png" alt=""><figcaption><p>Styling menu</p></figcaption></figure></div>

### Using command and code blocks

Command and code blocks have several unique properties such as syntax highlighting and quick actions that make working with code-based documentation simple. You can create a code or command block by either:

* Selecting Command or Code from the new element menu
* Typing ` ``` ` (triple backticks)

Once you’ve inserted your code block you can select the language at the bottom of the block from numerous options which will apply the appropriate syntax highlighting if available (or default to Code if your language is not found). All code and command blocks will apply syntax highlighting and provide a quick copy button for easy access.

<figure><img src="../../.gitbook/assets/notebook-code-block.png" alt=""><figcaption><p>Example code block</p></figcaption></figure>

### Special properties of command blocks

If you insert a Command block or specify the language as “Shell”, Warp provides extra functionality to simplify terminal work.

### Executing command blocks

Developers can execute shell command blocks by:

{% tabs %}
{% tab title="macOS" %}
* Using the insert button at the bottom of the block
* Pressing `CMD-ENTER` while the block is selected (a blue highlight will appear)
{% endtab %}

{% tab title="Linux" %}
* Using the insert button at the bottom of the block
* Pressing `CTRL-ENTER` while the block is selected (a blue highlight will appear)
{% endtab %}
{% endtabs %}

The command text will be inserted into the developer’s active terminal session, or a new session if none are active.

<figure><img src="../../.gitbook/assets/notebook-cmd-block-run.png" alt=""><figcaption><p>Run option for command block</p></figcaption></figure>

### Adding arguments to command blocks

Command blocks accept parameters in the same format as [Workflows](workflows.md). To add an argument to your command block, use \{{double\_curly\_brackets\}} to specify your argument term.

<figure><img src="../../.gitbook/assets/notebook-cmd-with-params.png" alt=""><figcaption><p>Command block with parameters</p></figcaption></figure>

### Navigating command blocks with the keyboard

Command Blocks also support keyboard navigation. There are two ways to enter the keyboard navigation mode:

{% tabs %}
{% tab title="macOS" %}
* Clicking on a shell block.
* Pressing `CMD-UP` or `CMD-DOWN.`

Once a command block is selected, press `CMD-ENTER` to insert it into the terminal input. You can also use `UP, DOWN, CMD-UP`, and `CMD-DOWN` to navigate between command blocks. While the Notebook is focused, press `CMD-L` to switch focus back to the terminal without inserting a command.
{% endtab %}

{% tab title="Linux" %}
* Clicking on a shell block.
* Pressing `CTRL-UP` or `CTRL-DOWN.`

Once a command block is selected, press `CTRL-ENTER` to insert it into the terminal input. You can also use `UP, DOWN, CTRL-UP,` and `CTRL-DOWN` to navigate between command blocks. While the Notebook is focused, press `CTRL-L` to switch focus back to the terminal without inserting a command.
{% endtab %}
{% endtabs %}

### Adding existing workflows to notebooks

If you have existing [Workflows](workflows.md) that you’d like to insert into your notebook rather than duplicating their content, you can select Embedded Workflow from the new element menu and select from the available workflows. Once embedded in a notebook, the workflow will be executable like a regular command block. To edit the content of the embedded workflow, you will need to edit the source workflow which can be found by searching for the title in the [Command Palette](../command-palette.md).

<figure><img src="../../.gitbook/assets/embedding-a-workflow.png" alt=""><figcaption><p>Embedding an existing workflow in a notebook.</p></figcaption></figure>

## Working with notebooks in a team

If the notebook is shared with a team, all team members will have access to edit the notebook and updates will sync immediately for all members of the team.

{% hint style="info" %}
Note that only one editor is allowed at a given time. Opening the notebook while there is an active editor will open the notebook in Viewing mode. Your mode (view vs edit) can be toggled above the notebook’s title.
{% endhint %}

<figure><img src="../../.gitbook/assets/notebook-view-mode.png" alt=""><figcaption><p>View mode example</p></figcaption></figure>
