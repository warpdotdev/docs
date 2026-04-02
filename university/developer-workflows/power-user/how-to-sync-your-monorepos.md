---
description: >-
  Use Warp's Rules to connect interrelated repositories and automate type
  updates across your stack.
metaLinks:
  alternates:
    - >-
      https://app.gitbook.com/s/c5dAwvMCRiTxUOdDicqy/developer-workflows/power-user/how-to-sync-your-monorepos
---

# How To: Sync Your Monorepos

Learn how to use Warp’s Rules system to connect interrelated repositories and automate type updates across your stack.

{% embed url="https://youtu.be/bndY6opaA7w?si=6zZWh4aB8f8kCD5F" %}

***

## Intro

This tutorial teaches you how to define **global Rules** in Warp so your coding agent understands how your projects relate to one another.

By linking monorepos (e.g., server, client, and shared API schemas), Warp automatically updates types and schemas across repos when you make a change in one place.

Although this example uses Warp’s internal repos, the same workflow applies to any multi-repo setup.

***

## The Problem

When projects are split into multiple repos — like backend, client, and shared schema — developers often forget to synchronize type changes manually.

That’s error-prone and time-consuming. Warp solves this by teaching your **agent** the relationships between your repos through a global Rule.

***

## The Rule Setup

Describe each repository and its connection to the others.

### Example Rule

{% code overflow="wrap" %}
```
We have three inter-related projects in ~/Repos:

warp-internal (client-side application)

warp-server (server application)

warp-proto-apis (shared API schemas for each)

When you update the schema types, push to git and update the installed types in the server and client by the commit hash.
```
{% endcode %}

Once defined, Warp automatically follows these instructions when a schema file is changed.

{% stepper %}
{% step %}
#### When the schema updates — update server types

`cd` into the server repository and run the appropriate commands to regenerate/update server-side types based on the changed schema.
{% endstep %}

{% step %}
#### When the schema updates — update client types

`cd` into the client repository and run the appropriate commands to regenerate/update client-side types so the client stays in sync with the schema changes.
{% endstep %}
{% endstepper %}

***

{% hint style="success" %}
Benefits

* Keeps your **schema, server, and client** perfectly in sync
* Reduces merge conflicts and version drift
* Saves manual steps when committing or deploying
{% endhint %}
