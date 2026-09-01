---
title: [Sentence case. Use "[Feature] FAQs" or "Frequently asked questions". This renders as the page H1 — do not add an H1 in the body.]
description: >-
  [One to two sentences, 50-160 characters: name the topic area these questions cover. Not just
  "Frequently asked questions". Example: "Answers to common questions about cloud agent
  billing, credits, and plan limits."
  Use {{TOKEN}} syntax for product names in src/data/vars.ts.]
---
[BEFORE PUBLISHING: Delete every bracketed instruction in this file, including this one. They are guidance for the author, not page content.]
[VARS: If this page names a product from src/data/vars.ts, add `import { VARS } from '@data/vars';` on the line directly below the frontmatter, then use {VARS.KEY} in prose. See AGENTS.md → Content variables.]

[STOP — check the admission rules before using this template. The default is "not an FAQ". An FAQ page pulls answers away from the page that owns the topic: the reader on the owning page does not find the answer, the reader on the FAQ gets one without context, and the two drift apart as the product changes.

All three must hold:
1. The questions are genuinely cross-cutting — they span several features, so no single page owns them.
2. There is no canonical home. If any existing page could answer it in context, answer it there. "It would be buried there" means that page needs restructuring, not that the answer needs a second home.
3. A reader actually asks it, in their own words, sourced from support tickets, Slack, or community threads — not invented to organize existing content.

This test applies to adding a question to an existing FAQ page too. These grow by accretion.

If the rules do not all hold: "What is X?" → conceptual page. "What are the limits?" → reference section on the owning page. "Why did I get error Y?" → troubleshooting. "How do I do Z?" → procedural section on the owning page.]

[Opening: what this FAQ covers and who it is for. 1-2 sentences.]

[BREVITY: Delete any section below you don't need — a short page is a finished page. See AGENTS.md → Voice & tone → Cut again.]

## [Theme — sentence case, e.g. "Billing", "Configuration"]

[Group by theme so readers can scan to their topic.]

### [Question in the reader's own words, ending in a question mark]

[QUESTION PHRASING: "Can I use my own API key?" not "BYOK support". Write what a person would type, not the feature name.]

[Lead with a direct answer in the first sentence, then detail. Keep it short and link out for depth — an FAQ answer should summarize and link, never be the only place a fact lives.]

### [Another question]

[Direct answer first, then detail.]

## Related pages

[Cross-links to the pages that own these topics. Use descriptive link text that names the destination.]

* [Feature documentation](path/to/page.md)
* [Reference](path/to/page.md)
