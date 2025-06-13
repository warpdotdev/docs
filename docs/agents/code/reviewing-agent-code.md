# Reviewing Agent Code

### **Navigating diffs within text-editor view**

When Agent Mode generates a code diff, it automatically triggers a built-in text editor diff view, which visually displays the changes as distinct hunks.

You can navigate through the highlighted hunks using the `UP` and `DOWN` arrow keys or mouse clicks. Agent Mode also supports multi-file changes, enabling you to view and manage hunks across several files. To switch between files, use the `LEFT` and `RIGHT` arrow keys.

Once satisfied with the changes, you can apply them by pressing `ENTER` or selecting the “Accept Changes” button. These modifications will not be applied to the files until you explicitly accept them.

### **Refining and editing diffs in text-editor view**

For refining or customizing the changes, Agent Mode allows for further interaction. You can refine the query (and diff) using natural language by pressing `R` or the “Refine” button, which will generate an updated diff based on your follow-up input.

If you wish to make direct edits within the text editor, press `E` or the “Edit” button to open the editor view. You can exit the editor by pressing `ESC`.

To cancel a pending action, use `CTRL-C` (on both Mac and Linux systems).

{% hint style="info" %}
You can open up code files in Warp by clicking on the link and selecting "Open in Warp"
{% endhint %}
