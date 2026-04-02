---
description: >-
  Prevent API keys and credentials from leaking using Warp's secret reduction
  and Rules system.
metaLinks:
  alternates:
    - >-
      https://app.gitbook.com/s/c5dAwvMCRiTxUOdDicqy/developer-workflows/testing-and-security/how-to-prevent-secrets-from-leaking
---

# How To: Prevent Secrets from Leaking

Learn how to safeguard credentials and sensitive data using Warp’s secret-reduction and Rule system.

{% embed url="https://youtu.be/2ECPFKtQpVk?si=HHw14Tqj-QyHeByX" %}

This tutorial shows how to use Warp’s **Rules** to prevent AI agents or collaborators from exposing sensitive information while coding or sharing output. Whether you’re pair-programming, streaming, or reviewing code, Warp can automatically redact secrets before they’re ever seen by an agent.

{% stepper %}
{% step %}
#### The Problem

AI assistants often echo API keys, tokens, or credentials in generated code blocks.\
When collaborating or screen-sharing, that can expose secrets publicly.
{% endstep %}

{% step %}
#### The Rule Setup

Define a simple Rule in Warp that instructs the agent to **never display secrets** in outputs or commands.

{% code title="Example Rule" %}
```
Rule: Protect Secrets
Behavior:
- Never include or reveal secrets when generating code or commands.
- Automatically redact sensitive strings before showing output.
```
{% endcode %}

{% hint style="info" %}
Enable Warp’s built-in Secret Reduction:

Settings → AI → Enable Secret Reduction

This automatically masks sensitive values before the agent or output logs can access them.
{% endhint %}
{% endstep %}

{% step %}
#### Benefits

* Protects API keys and credentials from exposure
* Keeps live streams and demos safe
* Works seamlessly with pair-programming or AI debugging
{% endstep %}
{% endstepper %}
