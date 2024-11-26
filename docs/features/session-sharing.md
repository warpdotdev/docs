---
description: Collaborate with anybody in a Warp terminal session, in real-time
---

# Session Sharing (Beta)

{% hint style="warning" %}
This action sends command information to Warp’s servers and is explicitly opt-in. Read more about privacy for cloud features in the [privacy overview](https://www.warp.dev/privacy/overview).
{% endhint %}

<figure><img src="../.gitbook/assets/session_sharing_preview.png" alt=""><figcaption><p>Session Sharing allows multiple teammates to edit the input at the same time</p></figcaption></figure>

### Share a session

Users on a [Team](teams.md) plan and users on the Beta will find a Share button in the Warp top-bar navigation.

To start sharing:

1. Click Share
2. Select the option to share a current session or start a new session

#### How to control a starting point for sharing

If you select to share a current session, you will be given the option to share without scrollback or from the start of the session. When you share access from the start of a session (with scrollback), collaborators will be able to view and interact with your entire session history including command outputs from before sharing was initiated.

If you initiate a shared session using Block actions, you will be given the option to start sharing from the selected block onwards. This option gives you the precision to select a specific block of output in your session history as the starting point, excluding all previous scrollback before that block.

<figure><img src="../.gitbook/assets/start-session-sharing.png" alt=""><figcaption><p>Start sharing from a selected block onward or an entire session with or without scrollback</p></figcaption></figure>

#### How to invite collaborators to your session

Warp will copy a link to your clipboard that you can share with anyone. Share links open the Warp's native app on MacOS, Linux, or the Web.

{% hint style="warning" %}
It's important to understand these are open links. During the Beta, it’s critical you only share your session links in private channels with known teammates and approved collaborators. Do not include your session-sharing links in any public forums.
{% endhint %}

When somebody who is logged into Warp accesses your shared session, they will be able to:

* View your session in Warp including your command line input and output
* Highlight text in your session
* Request control to edit and enter commands in the sharer’s session

If granted access, collaborators can edit the input together in real-time and execute commands.

You can also:

* Reference avatars and usernames for every collaborator who has access to your session
* Jump to a collaborator’s selection by clicking on their avatar
* Revoke edit access from collaborators at any time during a session

<figure><img src="../.gitbook/assets/session-sharing-native-web-demo.gif" alt=""><figcaption><p>Session Sharing Native to Web Demo</p></figcaption></figure>

#### How to end a shared session

When you’re ready to end a shared session, click Share → Stop sharing to wrap up and close access for all collaborators.

#### Multiple shared sessions

You may share multiple sessions simultaneously. If you have multiple shared sessions, you will find _Other shared sessions_ listed in the Share dropdown menu. You may also end multiple shared sessions at the same time with Share → Stop sharing all.

<figure><img src="../.gitbook/assets/switch-stop-session-sharing.png" alt=""><figcaption><p>Switch between shared sessions or stop all shared sessions at once</p></figcaption></figure>

### Known limitations

* [Agent Mode blocks](warp-ai/agent-mode.md) are not shareable during session sharing. Participants will be able to share regular shell commands that are run, but will not be able to share AI interactions (requested commands, AI blocks, etc.)
* [Secret redaction](secret-redaction.md) is not applied during session sharing.
* While this feature is in Beta, anybody who has access to a share link and an active Warp account will be able to view and collaborate on a session. In the future, Session Sharing will have Team-based access controls and permission restrictions.

There is a session size limit of 100MB per session, 1GB per user per day, and a maximum of 10 participants per session (excluding the sharer). These limits are subject to change.

{% hint style="info" %}
If you have any questions or want to be added to the Beta, please reach out at [feedback+ss@warp.dev](mailto:feedback+ss@warp.dev).
{% endhint %}
