---
description: >-
  Attach a public webpage link to your prompt to use its content as
  context—letting the agent extract and reference information directly from that
  page in its response.
---

# URLs as Context

## Referencing websites via URLs

You can attach a public URL to any prompt to provide page content as context. Warp will scrape the page and surface the extracted text directly to the model.

* Only publicly accessible pages are supported.
* The full page is added to the model’s context, which may increase credit usage for long documents.
* Only the specific URL you provide is processed. The agent won’t explore the site, follow links, or crawl beyond that page.

{% hint style="info" %}
**Important**: URL attachments are different from web search. If you need the agent to look something up, gather real-time information, or pull in multiple sources, use [Web Search](../../capabilities/web-search.md) instead.
{% endhint %}

<figure><img src="../../.gitbook/assets/url-as-context.png" alt=""><figcaption><p>Example of referencing docs via a URL</p></figcaption></figure>
