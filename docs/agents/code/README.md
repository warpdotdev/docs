---
description: >-
  Agent Mode enables intelligent, in-terminal code generation and editing
  through AI-powered diffs, allowing you to review, refine, and apply changes
  seamlessly across your codebase.
---

# Code

## Coding capabilities in Agent Mode

Agent Mode includes advanced coding capabilities directly within your terminal, triggered when it detects an opportunity to generate a code diff. This powerful feature allows for seamless code generation, editing, and management tasks, all within your terminal environment.

<figure><img src="../../.gitbook/assets/agent-mode-coding-capabilities.gif" alt="Agent mode coding capabilities demo of a topological sort in Python."><figcaption><p>Agent mode coding capabilities demo of a topological sort in Python.</p></figcaption></figure>

For a more tailored editing experience, you can attach context blocks directly from the terminal, providing Agent Mode with specific input to guide its diff suggestions.

If you have questions or feedback about this recent feature, feel free to contact us at [feedback@warp.dev](mailto:feedback@warp.dev).

### **Examples of coding capabilities**

Agent Mode responds to prompts related to code generation, editing, and analysis. Here are some examples:

* Code creation: “Write a function in JavaScript to debounce an input”
* Based on error outputs, suggest fixes: “Fix this TypeScript error.”
* Modify code within a file: “Update all instances of ‘var’ to ‘let’ in this file.”
* Apply changes across multiple files: “Add headers to all .py files in this directory”

When Agent Mode generates a code diff, you can review, refine, and decide whether to apply the changes.

### **Navigating diffs within text-editor view**

When Agent Mode generates a code diff, it automatically triggers a built-in text editor diff view, which visually displays the changes as distinct hunks.

You can navigate through the highlighted hunks using the `UP` and `DOWN` arrow keys or mouse clicks. Agent Mode also supports multi-file changes, enabling you to view and manage hunks across several files. To switch between files, use the `LEFT` and `RIGHT` arrow keys.

Once satisfied with the changes, you can apply them by pressing `ENTER` or selecting the “Accept Changes” button. These modifications will not be applied to the files until you explicitly accept them.

### **Refining and editing diffs in text-editor view**

For refining or customizing the changes, Agent Mode allows for further interaction. You can refine the query (and diff) using natural language by pressing `R` or the “Refine” button, which will generate an updated diff based on your follow-up input.

If you wish to make direct edits within the text editor, press `E` or the “Edit” button to open the editor view. You can exit the editor by pressing `ESC`.

To cancel a pending action, use `CTRL-C` (on both Mac and Linux systems).

{% hint style="info" %}
You can open up code files in Warp by clicking on the link and selecting "Open in Warp"\\
{% endhint %}

### **Supported languages for code suggestions in Agent Mode**

Agent Mode’s built-in text editor supports a wide range of programming languages and syntax highlighting, including: Python, JavaScript, TypeScript, Rust, Golang, Java, C, C#, C++, HTML, CSS, Bash, JSON, YAML. We are also continuously working on adding support for more languages.

{% hint style="info" %}
You can also open supported code files in Warp by clicking on the link, then selecting "Open in Warp". To save your changes, press `CMD-S` on macOS or `CTRL-S` on Linux and Windows.
{% endhint %}

<figure><img src="../../.gitbook/assets/open-in-warp-code.gif" alt=""><figcaption><p>Opening code files in Warp</p></figcaption></figure>
