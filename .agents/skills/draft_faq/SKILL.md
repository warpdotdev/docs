---
name: draft_faq
description: Draft or extend an FAQ documentation page. Use rarely - only for genuinely cross-cutting questions that span several features and have no canonical home on an existing page. Check the admission rules first; most FAQ-shaped content belongs on the page that owns the topic, not on an FAQ page.
---

# Draft FAQ page

Draft an FAQ page with questions grouped by theme and answers that lead with a direct response.

## Check the admission rules first

**Default to "not an FAQ."** An FAQ page pulls answers away from the page that owns the topic. The reader who lands on the owning page does not find the answer, the reader who lands on the FAQ gets an answer without its context, and the two drift apart as the product changes.

All three must hold before you create or extend an FAQ page:

1. **The questions are genuinely cross-cutting** — they span several features or pages, so no single page owns them.
2. **There is no canonical home** — no existing page could answer the question in context. "It would be buried there" means that page needs restructuring, not that the answer needs a second home.
3. **A reader actually asks it**, in their own words, sourced from support tickets, Slack, or community threads — not invented to organize existing content.

This test applies to **adding a question to an existing FAQ page** too. FAQ pages grow by accretion; each addition has to justify itself.

If the rules do not all hold, say so and redirect:

- "What is X / how does X work?" → conceptual page for X
- "What are the limits / which plans include X?" → reference section on the owning page
- "Why did I get error Y?" → troubleshooting section, keyed on the error
- "How do I do Z?" → procedural section on the owning page

## Workflow

Follow the workflow in `.agents/skills/draft_docs/SKILL.md`, using the **FAQ template** at `.agents/templates/faq.md`.

## Frontmatter description

One to two sentences, 50-160 characters, naming the topic area the questions cover.
- ✅ `Answers to common questions about cloud agent billing, credits, and plan limits.`
- ❌ `Frequently asked questions.`

See "Descriptions by content type" under Frontmatter in `AGENTS.md` for the full rules.

## Content type rules

These rules are specific to FAQ pages (from the "Drafting by content type" section of `AGENTS.md`):

- Write questions in the user's voice ("Can I use my own API key?" not "BYOK support").
- Lead with a direct answer, then provide detail.
- Keep answers concise — link to full documentation for deeper topics.
- Group questions by theme (e.g., "General", "Billing", "Errors").
- **Never let an FAQ answer become the only place a fact lives.** It should summarize and link, not own.
- Title convention: "[Feature] FAQs" or "Frequently asked questions"

## Heading case

All headings (H1–H4) must use **sentence case**: capitalize only the first word and proper feature names.

- ✅ `# Cloud Agents FAQs`
- ✅ `## Billing`
- ✅ `### Can I use my own API key?`
- ❌ `# Cloud Agents FAQS`
- ❌ `## Billing And Pricing`

## Existing examples

Read 2-3 of these strong examples to match the existing pattern:
- `src/content/docs/agent-platform/getting-started/faqs.md`
- `src/content/docs/support-and-community/plans-and-billing/pricing-faqs.md`
