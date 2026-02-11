---
description: >-
  Access your Warp Drive objects and shared sessions from any browser or touch
  screen device, including mobile phones, tablets, and touch-enabled laptops.
---

# Warp Drive on the Web

## What is Warp Drive on the Web?

Warp Drive on the Web lets you view and edit your Warp Drive objects and shared sessions directly in the browser, on any device.

<figure><img src="../../.gitbook/assets/wd-web-team-workflow.png" alt="" width="375"><figcaption><p>A web-based rendering of a Team Workflow</p></figcaption></figure>

## Accessing Warp Drive on the Web

Warp's web-based viewing experience can currently be accessed via:

* The [`app.warp.dev/app` homepage](https://app.warp.dev/app)
* [Drive Object](./#sharing-your-drive-objects) Links
* [Session Sharing](../session-sharing/#how-to-allow-access-to-collaborators-in-your-session) Links

{% hint style="warning" %}
You can edit and view web-based objects and sessions as normal. The one exception is executing a command from a workflow or notebook since there is no shell session running on the web.
{% endhint %}

## Managing your view preferences - web or desktop

If the Warp app is installed, links will open on the desktop by default. You can manage whether Warp links open in Warp's desktop app or the browser in multiple ways:

{% hint style="info" %}
The desktop option is only presented if Warp's web service is able to detect the Warp app installed locally. Warp desktop opens localhost port 9277 to accomplish this detection. This is done in a separate process that does not have access to your terminal contents.\
\
If you would like to use Warp locally and do not have it installed, please visit our [installation guide.](<../../README (1).md>)
{% endhint %}

1. The first time you follow a link, if Warp is not installed, you will be prompted to download it. You can dismiss the popup to stay on the web.

<figure><img src="../../.gitbook/assets/wd-popup-message.png" alt="" width="563"><figcaption></figcaption></figure>

2.  This preference can be changed at any point in _Settings > Features > General > Open links in desktop app._ Note that this setting is only available while on the web-based version of Warp.

    <figure><img src="../../.gitbook/assets/wd-open-links-preference.png" alt="" width="563"><figcaption><p>Setting managing how to open links</p></figcaption></figure>
3. You can always switch between web and desktop views on a case-by-case basis.
   1.  To switch from a web-view to Desktop for a given object, open the _overflow menu > Open link on Desktop._

       <figure><img src="../../.gitbook/assets/wd-switch-viewer.png" alt="" width="563"><figcaption></figcaption></figure>
   2.  To stay on the web for a given object despite a global Desktop preference, follow the _View on the web_ option that is part of the redirect screen to Desktop.

       <figure><img src="../../.gitbook/assets/wd-view-on-web.png" alt="" width="375"><figcaption></figcaption></figure>

## Supported Browsers

Warp on the web supports all modern browsers, including:

**Desktop**

* Chrome
* Firefox
* Safari

**Mobile**

* iOS Safari 15+
* Android Chrome 58+
* Samsung Internet 7.2+

{% hint style="info" %}
These mobile browser versions are the minimum required for WebGL 2.0 support. Most up-to-date devices meet these requirements.
{% endhint %}

## Touch screen and mobile support

Warp supports all touch screen devices, including mobile phones, tablets, and touch-enabled laptops. Touch input works on both the web and the desktop app.

### Supported gestures

* **Touch and scroll** - Vertical and horizontal scrolling work as expected
* **Double tap** - Select text or elements
* **Long press (hold)** - Open context menu (equivalent to right-click)

## Related features

* [Warp Drive](./) - Store and share workflows, prompts, and environment variables
* [Session Sharing](../session-sharing/) - Collaborate with others in real-time terminal sessions
