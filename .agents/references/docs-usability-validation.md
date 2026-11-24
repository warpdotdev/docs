# Docs usability validation

Validate whether readers can find and use an answer for their job to be done (JTBD). A correct sentence on an unexpected page does not establish a usable journey. This is an expert walkthrough, not evidence from testing with actual readers.

For example, a developer without admin access follows an integration quickstart. Check whether they discover the access requirement before setup and know who must act next, rather than finding the requirement later in an unrelated permissions table.

## Scope and timing

Run a bounded pass after drafting and mechanical checks, before handing off substantive public content as ready for review. Include changed prerequisites, decisions, task handoffs, and recovery paths, even when no new page was added. A small factual correction affecting permissions or billing can change a journey.

For spelling, formatting, meaning-preserving terminology, metadata, generated data, and mechanical link changes, check only affected navigation and links. State the reduced scope and reason in the handoff. Internal governance-only changes need relevant workflow tests, not a public-product walkthrough.

Opening a draft PR to obtain a preview is allowed before validation finishes. Record pending work rather than calling the draft validated. Independent review repeats representative high-impact journeys at the evaluated head instead of accepting the author's results as its own.

## Prepare questions before walking pages

1. Read the content design plan for the audience, JTBD, goals, and exclusions. For corrections without a plan, use the existing page's purpose. Resolve an unclear primary task with the requester before evaluating it.
2. Write a bounded set of questions in the reader's words. Label primary tasks before testing. Cover choosing, starting, configuring, verifying, understanding consequences, and recovering where relevant. Use support or reviewer evidence when available. Label inferred scenarios as editorial choices, not observed demand.
3. Consider novice readers, non-admin readers, browser-only access, existing configurations, and blocked actions. Record a question for each applicable dimension, or mark it inapplicable with a reason. These are prompts to tailor the pass, not a universal test bank.
4. Define what a sufficient answer would let the reader understand, decide, do, or verify. A conceptual or reference question need not end in a procedure. Do not expand the page's agreed purpose to satisfy an unrelated scenario.

## Walk the reader's path

Start from a plausible public entry point: navigation, a quickstart, a related page, or an actual search result. Record the entry URL and why it is plausible. Follow actual links and headings before using a known canonical destination. For a direct-arrival scenario, record how the reader obtained that URL.

Prefer interactive browser navigation whenever available. When no browser tool is available, read rendered text and follow its actual links. Missing browser tooling is not itself a blocker. Record search, menus, visual layout, responsive behavior, accessibility, authentication, and product interactions that this fallback did not test.

If no rendered version is available, perform a source-only preliminary inspection and mark navigation Not tested. Repository search, internal glossaries, the PR's content map, and backend source can diagnose a gap after the walkthrough, but cannot establish reader findability.

Identify the tested docs revision, local dirty changes if any, preview URL or build, and test time. An old published page cannot validate a changed preview. Note links that leave the preview, including absolute cross-space links, and which version the destination actually represents. Check redirects and anchors rather than treating HTTP 200 as a successful arrival.

For each question, check:

* **Findability** - The entry point and link labels lead to the answer without knowledge of internal terminology.
* **Direct answer** - The page answers the question rather than mentioning its topic.
* **Applicability** - The answer identifies the relevant product, plan, role, platform, and existing or new configuration where they affect the task.
* **Action and verification** - Instructions identify the actor, surface, action, and expected result. Required prerequisites appear before the action that needs them.
* **Consequences and recovery** - The reader learns consequences before committing to a choice and has an actionable next step when blocked.
* **Connected pages** - Linked procedures preserve prerequisites and context, and sibling answers do not conflict.

Browser-only completion is a scenario, not a requirement that every product task support a browser. A clearly explained product limitation with a supported alternative or responsible next actor can be a complete answer. Missing instructions are a docs gap, not evidence of a product limitation.

Do not execute purchases, membership changes, configuration changes, or other product mutations merely to test docs. Live product testing requires separate authorization and evidence. Keep usability findings separate from technical accuracy, shipped availability, compliance approval, documentation risk, and engineering review under the [quality policy](doc-quality-policy.md).

## Record results and decide readiness

Use one result per question, with separate notes for findability and completeness:

* **Clear** - The plausible path yields a sufficient, applicable answer.
* **Found with friction** - The answer is complete, but an avoidable detour or unclear label makes it harder to find. If the detour prevents the primary task, use Missing or Partial instead.
* **Partial** - An answer exists but lacks information needed for the question's outcome.
* **Missing** - The tested path provides no answer. Record the search boundary rather than claiming the answer exists nowhere.
* **Conflicting** - Connected answers disagree in a way that changes what the reader should do.
* **Not tested** - Required evidence was unavailable or the question was not attempted. State why and what remains to be tested.

Missing, Conflicting, or Partial results that prevent a primary task block readiness for review. Minor friction is non-blocking. An untested primary journey requires an explicit limitation and recorded human acceptance before readiness. Do not invent that acceptance. Lack of interactive browser testing alone does not make a rendered-link walkthrough Not tested.

Record the decision and next action per finding. Do not average results into a usability score or use successful secondary questions to cancel a primary-task failure. If a product limitation is clearly documented, do not classify it as a documentation failure simply because the desired action is unsupported.

## Fix, retest, and hand off

Fix gaps at the page that owns the answer or at the task-local handoff. Link shared policy rather than copying tables across pages. In a review-only or governance-only task, report the fix and its owning page without editing public docs.

After authorized fixes, rerun the same affected questions and connected journeys on the new version. Retain the initial finding and append the retest result and evidence. Do not weaken a question or redefine a primary task to improve the outcome. Record a legitimate scope change separately with the requester's decision.

Use the [validation record template](../templates/usability-validation.md) for a concise `## Usability validation` section in the PR body, or in the interactive handoff when no PR is requested. Include question-level evidence inline or link a durable record reviewers can access. Do not leave the only evidence in an unlinked temporary file or publish private support details, credentials, or internal source excerpts.

The record identifies scope, tested version and method, question results, findings, retests, limitations, and any human acceptance. For reduced-scope changes, state the reason and the navigation or link checks actually performed. Preserve existing PR sections and independent-review output formats.

V1 has no record-completeness checker, new required CI gate, or automated semantic grading. The [calibration fixtures](../skills/validate_docs_usability/evals/evals.json) describe expected judgments for synthetic journeys. They are not product facts or proof that an agent reliably makes those judgments.

## Related references

* [Content design plan](content-design-plan.md) - Establish the reader and task before drafting
* [Agent-doc quality policy](doc-quality-policy.md) - Preserve source verification and review requirements
* [Validation skill](../skills/validate_docs_usability/SKILL.md) - Run a bounded walkthrough
