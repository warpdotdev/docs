---
metaLinks:
  alternates:
    - >-
      https://app.gitbook.com/s/c5dAwvMCRiTxUOdDicqy/developer-workflows/devops/how-to-analyze-cloud-run-logs-gcloud
---

# How to: Analyze Cloud Run Logs (gcloud)

Learn how to use Warp to retrieve, organize, and analyze production logs from your cloud servers — all with natural language prompts.

{% embed url="https://youtu.be/GJ0NepZmmv8?si=MHhAVD2JeTLYc9rM" %}

{% stepper %}
{% step %}
#### Setting the Context

Open Warp and enable **voice input** (optional) for hands-free prompting.

{% hint style="info" %}
Voice input is optional — only enable it if you prefer hands-free prompting.
{% endhint %}

**Prompt**

```
Use the warp-server-staging gcloud project and pull logs
for the last 10 minutes from the warp-server Cloud Run instance.
Organize them by info, warning, and error levels.
Create a histogram across message types,
and highlight the most concerning errors to investigate.
```
{% endstep %}

{% step %}
#### Warp’s Agent in Action

After you hit Enter:

* Warp detects the command as an **Agent Mode** request.
* It gathers project context (`warp-server-staging`).
* Executes the necessary `gcloud` logging queries automatically.
* Writes retrieved data to a temporary file for processing.
{% endstep %}

{% step %}
#### Automated Analysis

Warp’s agent generates a **Python script** on the fly to:

* Parse logs
* Count messages by severity
* Output summary metrics

Example output:

```
1,000 log entries total
980 info
11 warning
9 errors
```

You can view or fast-forward execution, or stop the process at any point.
{% endstep %}

{% step %}
#### Reviewing Results

Warp outputs a readable histogram and highlights anomalies.\
For example:

> “Gemini AI error messages detected — worth reviewing.”

You can expand each log group interactively or inspect the temporary Python code for debugging.
{% endstep %}
{% endstepper %}
