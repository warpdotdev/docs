---
description: >-
  Summarize open pull requests and create GitHub issues from TODO comments using
  the GitHub MCP server.
metaLinks:
  alternates:
    - >-
      https://app.gitbook.com/s/c5dAwvMCRiTxUOdDicqy/mcp-servers/github-mcp-summarizing-open-prs-and-creating-gh-issues
---

# GitHub MCP: Summarize PRs & Create Issues

{% embed url="https://youtu.be/rrxfS9u1XRA?si=wDU42iXPhGlVn2RM&t=30" %}

The GitHub MCP Server lets Warp agents read, write, and automate tasks in your GitHub repositories directly — no manual tab-switching required.

***

### 2. Setup

#### Step 1. Get a GitHub Personal Access Token

1. Go to **GitHub → Settings → Developer Settings → Personal Access Tokens**
2. Create a new token and enable:
   * ✅ `repo`
   * ✅ `read:user`

***

#### Step 2. Add the Server in Warp

1. Open the **MCP Panel** via Command Palette (`Cmd + P`)
2. Click **Add Server**
3. Paste in your JSON config and the access token
4. Save — and you’ll see the available endpoints immediately

***

### 3. Workflow 1 — Summarize All Open PRs

Use Warp’s agent to summarize pull requests:

Behind the scenes, the MCP server:

* Lists PRs
* Fetches comments and reviews
* Compiles summaries with clickable links

Perfect for daily PR triage or stand-ups.

***

### 4. Workflow 2 — Create GitHub Issues from TODOs

Use a saved prompt to automate issue creation.

Warp:

1. Scans your codebase for TODO comments
2. Calls `create_issue` for each one via MCP
3. Generates a linked list of new issues

This turns scattered notes into trackable tickets instantly.

***

### 5. Why It’s Useful

* Save 20–30 minutes per session
* Keep repos synchronized automatically
* Enable PR summaries, issue tracking, and automation — all inside Warp.
