## Content design plan

[WRONG FORM? This is the **full form**, for a **new page**. An update that adds a concept to an existing page uses the three-line short form in `.agents/references/content-design-plan.md` instead, and a correction needs no plan at all. Check the routing rule there before filling this in.]

[BEFORE SUBMITTING: Delete every bracketed instruction, including this one. Fill in every field — "not applicable" is a valid answer only with a reason. See `.agents/references/content-design-plan.md` for what each field is asking and why.]

[WHERE THIS GOES: Present it to the requester before drafting when a person invoked the drafting skill. Include it in the PR body either way. This is not a page — it is a section of a PR description, or terminal output during an interactive session.]

**Audience and JTBD:** [A specific reader in a specific situation, and the outcome they want in their own terms. Not a demographic. ✅ "A backend engineer setting up their team's first cloud agent, who needs it to reach a private GitLab instance and has not configured Warp credentials before." ❌ "Developers who use cloud agents."]

**Problem:** [What the reader tries, where it breaks down, and what it costs them. If the honest answer is "nothing, they just would not know this exists," go back to the worthiness criteria.]

**Goals:**

[Two or three, written as reader capabilities rather than page contents. More than three usually means the page is doing several jobs and should be split. ✅ "The reader can decide which credential strategy fits their setup and configure it." ❌ "Explains the credential strategy options."]

- [Reader capability]
- [Reader capability]

**Purpose and value:** [Why this page earns its place, and what is lost without it. If the value is already delivered by an existing page, update that page instead.]

**Content type:** [Type] — [one-line rationale tied to the reader's job, not to the page's shape]

**Skill and template:** `[drafting skill]` / `.agents/templates/[template].md`

**High-impact scenarios:**

[The exclusions are the load-bearing half. They are what keeps the page from growing to cover every configuration permutation someone might hit.]

- Covers: [scenario], [scenario]
- Excludes: [scenario] — [why]
