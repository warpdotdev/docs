---
name: validate_docs_usability
description: Validate whether readers can find answers and complete documentation journeys. Use for docs usability checks, reader walkthroughs, task-based validation, and substantive drafting or review handoffs, even when builds and link checks pass.
---

# Validate docs usability

Read `AGENTS.md`, `.agents/references/docs-usability-validation.md`, and `.agents/references/compliance-claims-policy.md` before the walkthrough. The reference owns the method, result definitions, scope exceptions, and readiness rules.

## Workflow

1. Identify the docs root, changed pages, tested version, audience, and primary tasks from the content design plan or existing page purpose. Ask the requester if the task is unclear.
2. Write bounded reader questions and sufficient-answer criteria before walking the pages. Record applicable scenarios and exclusions.
3. Follow the reference's navigation method from plausible entry points. Prefer an interactive browser whenever available. Otherwise follow rendered text and actual links, or label a source-only preliminary inspection with navigation Not tested. Record evidence and coverage limits.
4. Fill `.agents/templates/usability-validation.md` with question results, findings, readiness, and next actions. Keep source accuracy and product availability checks separate under `.agents/references/doc-quality-policy.md`.
5. If fixes are authorized, correct the owning pages and retest affected questions on the new version. Otherwise report proposed fixes without editing docs. Keep initial findings alongside retests.

## Output and boundaries

Return a concise `## Usability validation` record in the interactive handoff or existing PR body when authorized. Report primary-task blockers and pending human acceptance explicitly. Use the reference's reduced scope for mechanical or governance-only changes.

This skill does not itself authorize product mutations, public-doc edits, PR creation, review submission, reviewer notifications, or scheduling. Preserve the caller's output format. For independent PR review, place evidence and limitations in the review rationale and attach actionable findings to changed lines.

Use `evals/evals.json` for synthetic calibration, not as a universal question bank or an automated usability score.
