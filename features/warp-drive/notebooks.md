---
description: Save interactive playbooks to simplify onboarding and development
---

# Notebooks

### What is a Notebook?

Notebooks are runnable documentation consisting of markdown text and list elements, code blocks, and runnable shell snippets that can be automatically executed in your terminal session. Notebooks are searchable and accessible through the [Command Palette](https://docs.warp.dev/features/command-palette) so you can access and run your documentation without ever leaving the terminal.&#x20;

### How to save and edit notebooks

You can create a new notebook from various entry points in Warp

* From Warp Drive, + > New notebook
* From the Command Palette, CMD + P, create a new team or personal notebook.
* With a keyboard shortcut, Shift + CMD +J

Any of these entry points will open the notebook editor where you can:

* Title your notebook.
* Start adding text and code elements.

{% hint style="info" %}
Note: The notebook will not be saved until either title or body text is added.&#x20;
{% endhint %}

<figure><img src="https://lh7-us.googleusercontent.com/gff35vEbh1ZQK1w-v8YhmAmoACEIeDdbxAF_IK46gCMDgrp-rdGpdXZ2Tw6vju9BaZWmYNbiN4TI9IRY4tdlqyczcpEAHrsoIBhIym8FOoRB3sxiRddM9FUxNQ74ObaAYHCZpJkcp4_wGUX3onbl-pg" alt=""><figcaption><p>Empty Notebook befores saving.</p></figcaption></figure>

\


### Import existing documentation

Existing markdown (.md) documentation can also be directly imported into Warp Drive. To import your markdown file(s):

* From Warp Drive, + > Import > then follow the file selection dialog.&#x20;

<figure><img src="https://lh7-us.googleusercontent.com/egr80PmzqDz6qRt6rSbL_o7Vtt0u846eF5QinJ3JFLnyQwkBMmYngbhYaip13ngWb89vmLWQ0br7Wa_lDEpykksDhCY9TRieQ9l3UmCdjlnrQZJ0pXvS7OKV0uFD10xbcypso5zddiOgym9rvCO50Ig" alt=""><figcaption><p>Notebook import modal.</p></figcaption></figure>

\


### Working with Notebooks

#### Adding new elements

Notebook elements (text, code, list items) can be added in a number of ways:

* Using the appropriate markdown shortcut (e.g. ### for Heading 3).
* Typing /, which will open up a selection menu of supported elements.
* Pressing the + icon which appears when hovering over a line and selecting from the menu of supported elements.

<figure><img src="https://lh7-us.googleusercontent.com/b_gWDWdsknhKT73Wpg5U46gMErCMmplahV7jYFGTmphG6jbWcgyovdaZmVPTDYp7tD7zjjmYySIfzHO6--N0ED45mIPkSI11-d1EPpHPX7n1_u-BfsF5_6IYCQ140l2TiXYfItVZoBZndCLdkOWR_9I" alt=""><figcaption><p>Markdown element types.</p></figcaption></figure>

#### Styling existing elements

Existing notebooks elements can be styled in several ways:

* Selecting an existing element and using keyboard shortcuts like CMD+B to bold.
* Selecting an existing element and selecting text decorations (like bold, italics, or inline code) from the hover menu.
* Using markdown syntax for text stylings like \*\*bold\*\* or \*italic\*.
* Selecting an existing element and changing the overall type of the element via the dropdown element menu.

<figure><img src="https://lh7-us.googleusercontent.com/_gcXiJ0AWaDPj9P4XwCUYsPKkhwMWH95NWnNpr7tIJ7vM-hdrUXtxQH4GKrgGTiicP-A85Z7G_nC20iU9C15AMBYCITS_TVeTWYU5Dy-QRukUTUxltgPLtZ-tPfIHUYJWYpKJkdiz5JmJRHUm9Gokpg" alt=""><figcaption><p>Styling menu</p></figcaption></figure>

#### Using Command and Code Blocks

Command and code blocks have several unique properties such as syntax-highlighting and quick actions that make working with code-based documentation simple. You can create a code or command block by either:

* Selecting Command or Code from the new element menu
* Typing \`\`\` (triple backticks)

Once you’ve inserted your code block you can select the language at the bottom of the block from numerous options which will apply the appropriate syntax highlighting if available (or default to Code if your language is not found). All code and command blocks will apply syntax highlighting and provide a quick copy button for easy access.

<figure><img src="https://lh7-us.googleusercontent.com/P5SQh2ATRrn5d-VqXIAjsJgRZ22ge79kczbuL1mvhKHWsbAu1fy2RpRFxqUAh4WUrcbNa5BAH1xPUhTLxePDI7jRpHbAv8RMUbbII61eQOGtBrnl2Ih9LzYxJd0RslzvLMsdW_kLnx2qsLKu_yXCPVk" alt=""><figcaption><p>Example code block.</p></figcaption></figure>

#### Special Properties of Command Blocks&#x20;

If you insert a Command block or specify the language as “Shell”, Warp provides extra functionality to simplify terminal work.&#x20;

#### Executing Command Blocks

Developers can execute shell command blocks by:

* Using the insert button at the bottom of the block
* Pressing CMD+Enter while the block is selected (a blue highlight will appear)

The command text will be inserted into the developer’s active terminal session, or into a new session if none are active.

<figure><img src="https://lh7-us.googleusercontent.com/mHKjC5btK6tyNSURjRTMwWG6J8bpeutCjr3POkYoc9uPrZGIbau8hj2LyOqbNuI8mDaP6XwVevunYIL0QhjMFxNtV1WBLt5JP89fJFliIdZpH0x2ZFOPolIvuM7VsPfcR41PUg20kLZzwQOTDHjzYzY" alt=""><figcaption><p>Run option for command block.</p></figcaption></figure>

#### &#x20;Adding arguments to Command Blocks

Command blocks accept parameters in the [same format as workflows](https://docs.warp.dev/features/warp-drive/workflows#working-with-arguments). To add an argument to your command block, use \{{double\_curly\_brackets\}} to specify your argument term.

<figure><img src="https://lh7-us.googleusercontent.com/f5Irl1-6HZoH6mMTz5bLbUjs-l5RI6JzlyPqJELR9Z8b8RXZ-G99NegApG8QAr8QhejAKWcTGmg6DAaEOCsVFH5Cg0Sh4m3FN3gfT1OtmTElS7Ovf4sbbAa5urq7QkGphuVt0XFL3Mxf07n_558zce0" alt=""><figcaption><p>Command block with parameter.</p></figcaption></figure>

#### Navigating command blocks with the keyboard

Command Blocks also support keyboard navigation. There are two ways to enter the keyboard navigation mode:

* Clicking on a shell block.
* Pressing `CMD-UP` or `CMD-DOWN.`

Once a command block is selected, press `CMD-ENTER` to insert it into the terminal input. You can also use `UP, DOWN, CMD-UP,` and `CMD-DOWN` to navigate between command blocks. While the Notebook is focused, press `CMD-L` to switch focus back to the terminal without inserting a command.

#### Adding existing workflows to Notebooks

If you have existing [workflows](https://docs.warp.dev/features/warp-drive/workflows#working-with-arguments) that you’d like to insert into your notebook rather than duplicating their content, you can select Embedded Workflow from the new element menu and select from the available workflows. Once embedded in a notebook, the workflow will be executable like a regular command block. To edit the content of the embedded workflow, you will need to edit the source workflow which can be found via searching for the title in the Command Palette.

<figure><img src="https://lh7-us.googleusercontent.com/fFlwgY0nRNkeptsid5mch_0Rww7G0EA8Y1tFSkon5cDyfuCrrV0HtglO4B_ddyWeQhEzdbdimF2l1EzvZy9aNXNaDWoujJomIQft_nIApQGBt1YXGolBFek1qg1b51y4qVLxndmrbCAHGUmRYci1NSA" alt=""><figcaption><p>Embedding an existing workflow in a notebook.</p></figcaption></figure>

### Working with Notebooks in a team

If the notebook is shared with a team, all team members will have access to edit the notebook and updates will sync immediately for all members of the team.&#x20;

{% hint style="info" %}
&#x20;Note that only one editor is allowed at a given time. Opening the notebook while there is an active editor will open the notebook in Viewing mode. Your mode (view vs edit) can be toggled above the notebook’s title.
{% endhint %}

<figure><img src="https://lh7-us.googleusercontent.com/tYp_RiFBa8qX01CHeDYWPrR_UqaDhkTEjQTOUGUvL8Y3pim8e9nZy8paHQuZXbSzJDIHrZHkyo6BBUnbyRKpnxNPXW9oEfmKn-qHfP_wGX23DlK6sKN9zsula_A987BBQ2qK8tmXw4ysCQAYGM6zfhg" alt=""><figcaption><p>View mode example.</p></figcaption></figure>

\
