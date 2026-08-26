# Content design plan

Before we begin drafting a docs page, we need to be extremely clear on its purpose, value, and audience. We define these things by completing a content design plan before making any changes to the docs.

Read this after a change has passed `.agents/references/docs-worthiness-criteria.md`, and before opening any template. This applies whether the drafting is done by a scheduled agent or by a person invoking a drafting skill directly.

How much plan a change needs depends on what it is. A new page gets the full form; an update that adds a concept gets a three-line short form; a correction gets none.

## Why this step exists

Drafting that starts at the template produces pages shaped by the template. The scaffold has a "Key features" section, so the draft gets a key features list; it has a "How it works" section, so the draft explains how it works — whether or not any reader needed either.

The plan inverts that. Start by determining who the reader is and what they are trying to do, and the content type falls out of the answer instead of dictating it.

That benefit does not depend on when a human reads the plan. Writing it is what shapes the draft.

**What the plan is for depends on where it is reviewed**, and the two cases are genuinely different:

- **Interactive drafting — a real checkpoint.** When a person invoked the drafting skill, present the plan and wait before writing any prose. Here the plan is cheap to disagree with: redirecting the audience or the content type costs a conversation instead of a rewrite. `write-feature-docs` already works this way with its Step 3 outline confirmation.
- **Automated runs — a record and a consistency check.** A scheduled run opens a draft PR without a pre-draft checkpoint, so by the time anyone reads the plan the prose exists. It is not saving the reviewer a rewrite. What it does is make the reasoning inspectable next to the diff, so a reviewer can catch drift — the plan says "backend engineer configuring self-hosted GitLab" and the page reads like a conceptual overview — and can reject on aim rather than on prose.

Do not claim the automated path buys early disagreement. It does not, and pretending otherwise obscures a real tradeoff: the pipeline was deliberately built to open draft PRs rather than propose first, accepting late review in exchange for not gating every candidate on a human.

## Principles

These come from [GitHub's content design principles](https://docs.github.com/en/contributing/writing-for-github-docs/content-design-principles), which we follow.

- **Create just enough docs.** More content makes everything harder to find, and anything added dilutes everything else. Adding a page has a cost paid by every other page.
- **Document high-impact, high-value scenarios** rather than attempting to comprehensively cover every possible use case. Completeness is not the goal; usefulness is.
- **Prioritize clarity, meaning, correctness, and consistency**, in that order.
- **Decide based on what people are trying to do**, not on what is technically correct or structurally tidy. When a style or structure question is genuinely open, resolve it by asking what best supports the reader's goal.
- **Be user-centered and inclusive.** Respect everyone who visits the docs and make content that works for them.

## Which form to write

Route on what the change is, not on how important it feels:

- **New page** → **full form**. Fill in `.agents/templates/content-design-plan.md`, every field.
- **Update that adds a new concept or section to an existing page** → **short form**, below.
- **Correction or extension of existing content** → **no plan**. See "When a plan can be skipped".

### The short form

Three lines. An update inherits the page's content type, never opens a template, and does not have to justify the page's existence — so the full form's Content type, Skills and templates, and Purpose and value fields have no work to do.

- **Reader and job:** who arrives at this page, and what they are trying to accomplish
- **Gap today:** what the page fails to do for that reader right now
- **Change:** the section or paragraph being added, and what it deliberately leaves out

Filled in, for adding the secret size limit to the existing secrets page:

- **Reader and job:** A platform engineer storing a service-account JSON key as a team secret so cloud agents can authenticate to GCP.
- **Gap today:** The page covers creating a secret but never mentions that values are capped, so an oversized key fails at save time and the page offers no explanation.
- **Change:** One paragraph under "Creating a secret" naming the 128 KiB limit and the error it produces. Excludes per-plan quota differences, which belong on the billing page.

That is the entire artifact. A short form running long usually means the change is a new page in disguise — go back to the routing rule.

## Required fields (full form)

These are the fields of the full form, for a new page. Fill in every one — "not applicable" is a valid answer only with a reason. For an update, use the short form above.

### Target audience and their JTBD

Who is this for, and what job are they trying to get done?

Name a specific reader in a specific situation, not a demographic. The job is what they are trying to accomplish in their own terms — the outcome they want, not the feature they will use to get it.

- ✅ "A backend engineer setting up their team's first cloud agent, who needs it to reach a private GitLab instance and has not configured Warp credentials before."
- ❌ "Developers who use cloud agents."

If you cannot describe a reader arriving at this page with a problem, that is a signal the page should not exist. Go back to the worthiness criteria.

### Problem statement

What specific difficulty does the reader hit without this doc?

Describe the failure: what they try, where it breaks down, and what it costs them.

"They would not know this exists" is a legitimate answer only when the change passed **Gate 4**, and then the problem statement has to carry that gate's evidence: the job the reader could not do before, and the in-product surfaces that stay silent about it. Without those, the change did not pass the worthiness gates and should not have reached this step.

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

## Where the inputs come from

Audience, problem, and goals are the fields most often invented, because code cannot answer
them. A setting registration tells you what a toggle does, never who needed it. Work through
these before falling back on your own reasoning:

- **The product spec** — warp-server `specs/<id>/PRODUCT.md`, the closest thing to a direct
  answer. Its `Problem`, `Goals`, `Non-goals`, and `User experience` sections line up with this
  plan's Problem, Goals, Excludes, and high-impact scenarios. Only some specs have one, and
  `TECH.md` is not a substitute.
- **The page you are updating** — for an update, the audience is usually already established.
  Match it instead of re-deriving it.
- **Support and community signal** — a reported failure is stronger evidence for the Problem
  field than a plausible one you reasoned your way to.

Three limits on spec use, because specs are private and forward-looking:

- Framing only. Labels, flags, and defaults get verified against code, never against the spec.
- Never evidence that a feature shipped — that is Gate 0, settled before this plan.
- Never quoted into a public page.

If no source answers a field, say so rather than inventing an answer. "No spec exists; audience
inferred from the setting's placement under **Settings** > **AI**" is a claim a reviewer can
check. An invented reader is not.

## Where the plan lives

Either form:

- **Present it to the requester before drafting** when a person invoked the drafting skill. This is the checkpoint, and skipping it forfeits the only cheap chance to redirect.
- **Include it in the PR body** as a `## Content design plan` section, in every case. A plan that lives only in an agent run log is not reviewable in practice — nobody opens the run to check the reasoning behind a page.

## When a plan can be skipped

Corrections and mechanical edits do not need one. Skip the plan for:

- Typo, grammar, link, and formatting fixes
- **Docs bug fixes** — the page describes the product incorrectly and you are making it match reality
- **Factual corrections** — a renamed setting, a changed default, a stale Settings path, an outdated screenshot
- **Adding a missing entry to an existing reference table or list** — a flag, endpoint, shortcut, or setting, where the surrounding page already establishes the reader and the format
- Terminology sweeps that do not change meaning
- Mechanical or generated updates (changelog entries, OpenAPI spec sync, snapshot and bookkeeping refreshes)
- Redirect and navigation-only changes

The test is whether the reader gains information or has information corrected. Correcting is a skip. Adding a concept is a short form. A new page is the full form.

## Related references

- `.agents/templates/content-design-plan.md` — the full form, for new pages. The short form lives in this reference, under "Which form to write".
- `.agents/references/docs-worthiness-criteria.md` — whether the doc should exist, applied before this
- `AGENTS.md` → "Drafting by content type" — the content type definitions and rules
- `.agents/templates/` — the page scaffolds
