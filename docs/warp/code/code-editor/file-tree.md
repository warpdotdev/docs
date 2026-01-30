---
description: >-
  Browse, open, and manage your project with Warp’s native file tree, complete
  with keyboard shortcuts, file icons, and context menu actions for files and
  folders.
---

# File Tree (Project Explorer)

<figure><img src="../../.gitbook/assets/filetree-main.png" alt=""><figcaption></figcaption></figure>

Warp includes a **native file tree** that makes it easy to explore and manage project files. The file tree is available whenever in any directory and it automatically reflects your project structure as files are added, removed, or changed.

### Opening the file tree

You can open the file tree from the tools panel on the left hand side:

* **Tools panel**: Click the Tools sidebar button, then open the File Tree tab (first tab in the panel).
* Press `CMD + \` to open the left panel, then assign your own shortcut for File Tree (and Warp Drive) in `Settings > Keyboard Shortcuts`.

<figure><img src="../../.gitbook/assets/file-tree-project-explorer-tools-panel.png" alt="" width="329"><figcaption></figcaption></figure>

{% hint style="info" %}
Warp supports icons for common file types. If a file type is missing an icon, please [file a GitHub issue](https://github.com/warpdotdev/Warp/issues) so we can review and add support.
{% endhint %}

### Browsing and opening files

Clicking on a file opens it directly in Warp’s [**native Code Editor**](./), where you can view and edit code in a separate pane or tab.

## File and Folder Actions

Right-clicking any **file** opens a context menu with several useful options:

* **Open in new pane**: Open the file in a side-by-side pane.
* **Open in new tab**: Open the file in a new tab.
* **Attach as context**: Insert the file into an agent prompt so the Agent can analyze or reference it.
* **Copy path**: Copy the absolute file path.
* **Copy relative path**: Copy the path relative to your current working directory.

<figure><img src="../../.gitbook/assets/file-tree-context-menu.png" alt=""><figcaption><p>Right-click context menu on a folder in the file tree.</p></figcaption></figure>

Right-clicking any **folder** opens a context menu with the following options:

*   **Create new file**: Add a new file directly from the tree.

    <figure><img src="../../.gitbook/assets/file-tree-new-file.png" alt="" width="375"><figcaption></figcaption></figure>
* **Attach as context**: Insert the selected file into your agent prompt so the Agent can analyze or reference it.
* **Copy path**: Copy the absolute file path to your clipboard.
* **Copy relative path**: Copy the path relative to your current working directory.

