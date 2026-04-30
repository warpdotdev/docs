---
name: draft_faq
description: Draft a new FAQ documentation page or update an existing one. Use for pages that collect frequently asked questions about a topic area. Questions are written in the user's voice and grouped by theme.
---

# Draft FAQ page

Draft an FAQ page with questions grouped by theme and answers that lead with a direct response.

## Workflow

Follow the workflow in `.warp/skills/draft_docs/SKILL.md`, using the **FAQ template** at `.warp/templates/faq.md`.

## Content type rules

These rules are specific to FAQ pages (from the "Drafting by content type" section of `AGENTS.md`):

- Write questions in the user's voice ("Can I use my own API key?" not "BYOK support").
- Lead with a direct answer, then provide detail.
- Keep answers concise — link to full documentation for deeper topics.
- Group questions by theme (e.g., "General", "Billing", "Errors").
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
