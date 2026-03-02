---
description: >-
  Attach screenshots, diagrams, or other images to your prompt so Warp’s Agent
  can use visual context when generating responses.
---

# Images as Context

## **Attaching images as context**

To provide visual context, you can attach images directly to an agent prompt. This is useful for including screenshots, diagrams, or other visual references alongside your query.

You can attach images in the following ways:

* Using the **image upload button** found on the toolbelt (either on the bottom left or right), depending on which input mode you're using:

<figure><img src="../../.gitbook/assets/image-as-context-universal.png" alt=""><figcaption><p>Attaching 5 images on the new "Universal" input (bottom left toolbelt)</p></figcaption></figure>

<figure><img src="../../.gitbook/assets/image-as-context-classic.png" alt=""><figcaption><p>Attaching 4 images on the "Classic" input (bottom right)</p></figcaption></figure>

* Copy and paste images directly (e.g. right-click an image > "Copy image" or copy from a file manager) into Warp.
* Drag and drop images, such as from a file manager or screenshot utility.

{% hint style="info" %}
Warp accepts the following image formats: `.jpg` , `.jpeg` , `.png` , `.gif` , and .`webp` .
{% endhint %}

You can attach up to **5 images per request**, and up to **20 images across a single conversation**. Each image is sent to the model provider and immediately discarded — nothing is stored on Warp's servers.

{% hint style="warning" %}
**Cloud agent conversations do not currently support image attachments.** Image attachment is only available in local agent conversations. If you need to provide visual context to a cloud agent, describe the image contents in your prompt or reference the image file path within the cloud agent's [environment](../../cloud-agents/environments.md).
{% endhint %}

### Model behavior and image handling

All supported models listed in [Model Choice](../../capabilities/model-choice.md) can interpret image input.

Attaching images will consume additional requests, proportional to the number of images added. To stay within model limits, Warp will intelligently resize images before passing it as context, minimizing token usage and respecting the model's maximum image dimensions.

