---
description: >-
  The Code Review panel lets you review, edit, and manage Git diffs in real
  time, with options to attach, revert, or open files directly.
---

# Code Review

When you are working locally in a Git repository with uncommitted changes, the **Code Review panel** lets you inspect, edit, and manage code changes directly inside Warp. It integrates with Git and Warp's Agents, giving you the ability to:

* Review diffs and attach them as context for the Agent
* Apply, edit, or revert changes in real time
* See changes made outside of Warp or by Warp's Agents automatically reflected

Any uncommitted changes appear in the panel (or compare the changes on your branch against `main` or `master` ). Switching branches or saving files updates the panel instantly, so it always reflects the current state of your codebase.

{% embed url="https://www.loom.com/share/96581523168742eb9b95c3973924728c?sid=a3ee9164-4274-4468-ac32-38ce6807f9a8" %}
Code Review Demo
{% endembed %}

<figure><img src="../.gitbook/assets/code review full view.png" alt=""><figcaption><p>Full view of Code Review panel and terminal pane.</p></figcaption></figure>

## Opening the Code Review panel

The Code Review panel can be opened in several ways. Each entry point makes it easy to inspect and manage changes without leaving your workflow.

#### 1. Universal Input: Git diff chip&#x20;

In the [universal-input](../terminal/universal-input/ "mention") editor, when you’re in a Git repository with changes, the chip shows the number of files modified along with lines added and removed. Clicking the chip opens the Code Review panel with the relevant diffs.

<figure><img src="../.gitbook/assets/whole UDI bar.png" alt=""><figcaption></figcaption></figure>

<figure><img src="../.gitbook/assets/git chip tooltip 1.png" alt=""><figcaption></figcaption></figure>

#### 2. Agent Conversation: Review Changes Button

When an Agent makes code edits in an [agent-conversations](../agents/using-agents/agent-conversations/ "mention"), a `Review changes` button appears at the bottom of the conversation. Clicking it opens the code review panel.

<figure><img src="../.gitbook/assets/Blocklist with review changes.png" alt=""><figcaption><p>Review changes at bottom of Agent Conversation.</p></figcaption></figure>

<figure><img src="../.gitbook/assets/review changes in footer.png" alt=""><figcaption></figcaption></figure>

#### 3. Agent Conversation: Toolbelt (Bottom Right)

During an Agent conversation, you can view all changed files in the toolbelt chips at the persistent bottom right. From there, you can open the Code Review panel directly.

<figure><img src="../.gitbook/assets/ai_control_panel_buttons_larger_view.png" alt=""><figcaption></figcaption></figure>

#### 4. Pane Toolbelt Buttons

In the top-left of any pane in a Git-tracked repository, clicking the plus/minus icon opens the Code Review panel for reviewing changes.

<figure><img src="../.gitbook/assets/Code toolbelt buttons in pane header.png" alt=""><figcaption></figcaption></figure>

#### Viewing All Edited Files

Inside the Code Review panel, you can open the file sidebar to browse all changed files in your repository. Clicking on a file will automatically scroll to that file in the panel.

<figure><img src="../.gitbook/assets/whole git diff view with one file collapsed.png" alt=""><figcaption><p>Viewing all edited files in the code review panel, with the file sidebar open.</p></figcaption></figure>

{% hint style="info" %}
By default, the Code Review panel opens as a pane on the right, but you can drag it to reposition wherever you prefer.
{% endhint %}

## Reviewing diffs

By default, the Code Review panel shows all **uncommitted changes** on your current branch, excluding changes to files ignored by `.gitignore`.&#x20;

Warp offers two ways to review changes:

1. **Uncommitted changes**: view all edits you've made locally on the current branch.
2. **Changes vs. main**: compare your branch against `main` or `master` to see what would be included in a pull request to that branch, for instance.
   1. Warp automatically detects the target branch and updates the comparison accordingly.

You can manually switch between the two views either in the Code Review panel or via the unviersal input chip:

<figure><img src="../.gitbook/assets/diff dropdown to change base from the code review pane.png" alt=""><figcaption><p>Changing diff view in the Code Review Panel.</p></figcaption></figure>

<figure><img src="../.gitbook/assets/git diff change base dropdown.png" alt=""><figcaption><p>Changing diff view in the Universal input.</p></figcaption></figure>

Any saved edits made outside of Warp (e.g. in another editor), as well as changes applied by Warp's Agents, appear automatically. The panel updates in real time, ensuring it always reflects the current state of your working file and directory.

#### Attaching diffs as context

The Code Review pane makes it simple to share changes with the Agent. You can attach an entire diff to a prompt so the Agent has full visibility into what was added or removed.&#x20;

<figure><img src="../.gitbook/assets/attaching-diff-as-context.png" alt=""><figcaption><p>Attaching a diff as context from the Code Review panel.</p></figcaption></figure>

This ensures responses are grounded in your latest edits, whether you’re asking for feedback, explanations, or follow-up changes. For more details, see [selection-as-context.md](../agents/using-agents/agent-context/selection-as-context.md "mention").

#### Reverting diffs

The Code Review panel lets you easily undo changes at different levels. In the gutter next to each diff, you’ll see an option to revert a hunk: roll back a specific set of changes (a “diff hunk”) within a file. This removes the added or modified lines and restores the previous version.

<figure><img src="../.gitbook/assets/revert diff hunk.png" alt=""><figcaption></figcaption></figure>

When you revert, the changes are immediately updated in your working directory. The file is restored to match the selected version, so you can continue editing or commit without the reverted code.

### Opening Files from Code Review

In addition to reviewing and editing diffs directly in the Code Review pane, you can open a file directly in Warp’s [code-editor](code-editor/ "mention"). Each file listed in the Code Review pane includes an expand button in the top-right corner of its diff view.

<figure><img src="../.gitbook/assets/Open file in new tab.png" alt=""><figcaption></figcaption></figure>

* Clicking the expand button opens the file in a new editor tab, allowing you to see the full file beyond just the changed lines.
* This is useful when you need additional context around a diff, want to make broader edits, or prefer working in the full editor rather than inline.
* Once opened, the file behaves like any other editor tab: you can scroll, edit, search, and save.
* Any changes made in the editor automatically sync back into the Code Review pane, so the diff view always stays current.

#### Directly editing code diffs

Alternatively, from the Code Review panel, you are able to click and edit the diffs directly:

<figure><img src="../.gitbook/assets/directly-editing-diffs.gif" alt=""><figcaption></figcaption></figure>
