---
name: sync_terminology
description: >-
  Review and maintain the authoritative docs-repo glossary using verified UI,
  API, CLI, and approved positioning evidence. Use for a weekly terminology
  review or when a shipped name changes. Propose changes for human review;
  never synchronize from an external dictionary.
---

# Maintain the documentation glossary

`.agents/references/terminology.md` is authoritative for documentation.
Read it, `AGENTS.md`, `.agents/rules/warp-positioning.md`, and
`.agents/references/doc-quality-policy.md` before proposing changes.
Keep this skill's existing name for callers; it no longer imports a dictionary.

## Review the evidence

1. Identify the terms affected by the request, a verified shipped rename, or
   repeated reader or reviewer confusion. For a weekly review, use changes
   since the last recorded source revision rather than recertifying every term.
2. Check exact names against the owning UI, API, or CLI source. Record the
   source revision and deployment evidence separately. Code or a schema does
   not establish that a feature has shipped.
3. Compare definitions and usage with the positioning guidance. An example
   page or a marketing claim cannot override it. Preserve exact identifiers,
   role names, commands, quoted UI strings, and necessary historical context.
4. Record conflicts, missing evidence, and unclear ownership as questions for
   human review. Do not invent a preferred term or treat inaccessible evidence
   as a successful no-change review.

## Propose a focused correction

Update the existing glossary entry with its preferred term, short definition,
usage note, and any necessary literal-interface exception. Add a source and
review date for the materially changed section. Update a matching `AGENTS.md`
summary only when needed; do not duplicate the full glossary there.

Keep a newly discovered term as a candidate until its name and definition are
supported. Never remove an entry simply because it is absent from another
source. Changes to positioning intent require the positioning owner's approval;
technical claims require verification from their owning source.

If nothing needs changing, report the reviewed scope, source revisions, and
remaining gaps. Do not create a branch or PR just to record a successful check.

## Continue existing work

First look for an open PR already owning the requested guidance or terminology
changes. Reuse its branch in an isolated worktree. Do not switch a busy checkout,
reset another run's work, rebase a shared branch, or open a duplicate PR.

When no existing PR owns a warranted correction, follow `create_pr` and the
agent-doc quality contract in `.agents/references/doc-quality-policy.md`.
Apply the `warpy-factory` label, classify risk, account for unverified claims,
and use `.agents/skills/create_pr/check_pr_body.py` before delivery.
Definitions that change product meaning are not automatically low risk.

Review the glossary diff and affected summaries, verify links and references,
run the relevant editorial guidance tests, and run `git diff --check`.
Record exact results and unverified claims in the existing PR's body.
Agents propose changes; humans approve and merge them.

## Cadence

Review weekly and when a verified interface or approved term changes.
Inspect existing maintenance callers and schedules before enabling a recurring
run. Reuse a compatible audit path instead of creating a second overlapping job.
This skill does not itself enable a schedule or claim that one is running.
