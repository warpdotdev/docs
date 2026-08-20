# Content design plan

Before we begin drafting a docs page, we need to be extremely clear on it's purpose, value, and audience. We define these things by completing a content design plan before making any changes to the docs.

Read this after a change has passed `.agents/references/docs-worthiness-criteria.md`, and before opening any template. Every new page and every substantive update to an existing page needs a content design plan — whether the drafting is done by a scheduled agent or by a person invoking a drafting skill directly.

## Why this step exists

Drafting that starts at the template produces pages shaped by the template. The scaffold has a "Key features" section, so the draft gets a key features list; it has a "How it works" section, so the draft explains how it works — whether or not any reader needed either.

The plan inverts that. Start by determining who the reader is and what they are trying to do, and the content type falls out of the answer instead of dictating it.

It is also the artifact a reviewer can actually disagree with. Reviewing a finished draft means arguing about prose. Reviewing a plan means arguing about whether the doc is aimed at the right person solving the right problem, which is the disagreement worth having and the one that is expensive to resolve after the page is written.

## Principles

These come from [GitHub's content design principles](https://docs.github.com/en/contributing/writing-for-github-docs/content-design-principles), which we follow.

- **Create just enough docs.** More content makes everything harder to find, and anything added dilutes everything else. Adding a page has a cost paid by every other page.
- **Document high-impact, high-value scenarios** rather than attempting to comprehensively cover every possible use case. Completeness is not the goal; usefulness is.
- **Prioritize clarity, meaning, correctness, and consistency**, in that order.
- **Decide based on what people are trying to do**, not on what is technically correct or structurally tidy. When a style or structure question is genuinely open, resolve it by asking what best supports the reader's goal.
- **Be user-centered and inclusive.** Respect everyone who visits the docs and make content that works for them.

## Required fields

Fill in every field. "Not applicable" is a valid answer only with a reason.

### Target audience and their JTBD

Who is this for, and what job are they trying to get done?

Name a specific reader in a specific situation, not a demographic. The job is what they are trying to accomplish in their own terms — the outcome they want, not the feature they will use to get it.

- ✅ "A backend engineer setting up their team's first cloud agent, who needs it to reach a private GitLab instance and has not configured Warp credentials before."
- ❌ "Developers who use cloud agents."

If you cannot describe a reader arriving at this page with a problem, that is a signal the page should not exist. Go back to the worthiness criteria.

### Problem statement

What specific difficulty does the reader hit without this doc?

Describe the failure: what they try, where it breaks down, and what it costs them. If the honest answer is "nothing, they just would not know this exists," the change probably failed the worthiness gates and should not have reached this step.

### Goals

What can the reader do after reading it?

Write these as reader capabilities, not page contents. "The reader can decide which credential strategy fits their setup and configure it" is a goal. "Explains the credential strategy options" is a table of contents entry.

Two or three goals. More than that usually means the page is doing several jobs and should be split.

### Purpose and value added

Why does this page earn its place, and what is lost if it does not exist?

This is the "just enough docs" test applied to this specific page. If the value is already delivered by an existing page, the answer is to update that page — go back to the worthiness criteria and pick the update outcome instead.

### Content type and model

Which content type, and why?

Name the type and give a one-line rationale tied to the reader's job. See the "Drafting by content type" section of `AGENTS.md` for the full definitions and rules.

The type should follow from the JTBD:

- Reader is learning what something is → **conceptual**
- Reader is performing a task → **procedural**
- Reader is looking something up mid-task → **reference**
- Reader is stuck on a specific failure → **troubleshooting**
- Reader wants the fastest path to a working result → **quickstart**
- Reader needs both the concept and the task in one place → **feature documentation (combined)**

If two types fit equally well, the reader's job is probably ambiguous. Resolve that before drafting.

### Skills and templates to use

Name the specific drafting skill and the specific template file.

Being explicit here catches type/template mismatches before drafting rather than in review, and it makes the plan reproducible — a reviewer can check that the draft actually used what the plan chose.

### High-impact scenarios

Which core user tasks does this cover, and which edge cases are deliberately excluded?

List the scenarios worth covering, in priority order. Then **name what you are leaving out and why.** The exclusions are the load-bearing half of this field: they are what keeps the page from growing to cover every configuration permutation someone might hit.

- ✅ "Covers: self-hosted GitLab with a personal access token; GitLab.com with OAuth. Excludes: self-managed GitLab behind a corporate proxy — rare, and the proxy configuration is the user's own infrastructure concern, not ours."
- ❌ "Covers all GitLab setups."

## Where the plan lives

**A required section in the docs PR body**, filled in before the diff is reviewed.

Keeping it next to the diff is the point. A plan buried in an agent run log is not reviewable in practice — nobody opens the run to check the reasoning behind a page. In the PR body, the reviewer sees the intent and the execution together and can catch a well-written page aimed at the wrong reader.

Use this structure:

```markdown
## Content design plan

**Audience and JTBD:** [Specific reader in a specific situation, and the outcome they want]

**Problem:** [What breaks down without this doc]

**Goals:**
- [Reader capability]
- [Reader capability]

**Purpose and value:** [Why this page earns its place]

**Content type:** [Type] — [one-line rationale]

**Skill and template:** `[skill]` / `.agents/templates/[template].md`

**High-impact scenarios:**
- Covers: [scenario], [scenario]
- Excludes: [scenario] — [why]
```

For an update to an existing page rather than a new page, the same fields apply, scoped to the change: the audience and job for the section being added or revised, and what the page fails to do for that reader today.

## When a plan can be skipped

Small corrections do not need one. Skip the plan for:

- Typo, grammar, link, and formatting fixes
- Terminology sweeps that do not change meaning
- Mechanical or generated updates (changelog entries, OpenAPI spec sync, snapshot and bookkeeping refreshes)
- Screenshot replacements

If the change adds, removes, or reframes information a reader acts on, it needs a plan. If in doubt, write one — it is four sentences.

## Related references

- `.agents/references/docs-worthiness-criteria.md` — whether the doc should exist, applied before this
- `AGENTS.md` → "Drafting by content type" — the content type definitions and rules
- `.agents/templates/` — the page scaffolds
