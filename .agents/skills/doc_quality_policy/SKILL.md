---
name: doc_quality_policy
description: Shared reference and helper scripts for the v1 agent-doc quality contract — the warpy-factory marker, the Documentation risk / Unverified claims PR-body sections, the low-risk allowlist, VERIFY marker accounting, and docs-verified/docs-waiver overrides. Not a dispatchable skill; used inline by every PR-producing content skill and by CI.
---

# doc_quality_policy

Shared library for the v1 agent-doc quality program. This is a reference and
helper-script skill, not something dispatched on its own — every content skill
that opens or updates a PR (`create_pr`, `draft_docs` and its type-specific
skills, `release_updates`, `missing_docs`, the AEO skills, `sync_terminology`,
`sync-error-docs`, `sync-openapi-spec`, `docs-seo-audit`, `afdocs-fix`,
`update-changelog`, `improve-drafting-skills`) and CI use it inline.

The full rules live in `.agents/references/doc-quality-policy.md`. This
directory implements them:

- `policy.py` — pure parsing/classification/validation functions (the agent
  marker, risk levels, `## Documentation risk` / `## Unverified claims`
  parsing, `{/* VERIFY: ... */}` marker accounting, the low-risk allowlist via
  `RiskSignals` + `classify_risk`, and the engineering-review human gate via
  `validate_engineering_gate`).
- `check_pr_contract.py` — CI-callable checker: reads a PR body file, finds
  VERIFY markers in the changed docs files (auto-discovered via
  `git diff --diff-filter=d origin/main...HEAD` when not passed explicitly,
  matching `style_lint.py --changed`'s scope and its no-silent-fallback rule),
  and validates the full contract. Exit 0 = pass, 1 = violations, 2 = usage
  error.
- `finalize_pr_contract.py build` — prints the `## Documentation risk` block
  for a PR-producing skill to insert into its PR body. Does not call `gh`
  itself; the invoking skill applies the `warpy-factory` label separately.
- `check_compression_contract.py` — checks the mechanically-checkable parts
  of the shared compression contract (word budget, callout count) for one
  file.
- `authorized_docs_reviewers.json` — the GitHub handles authorized to record
  a `docs-verified`/`docs-waiver` override. Pod-Docs owns this list.

## Using this from a PR-producing skill

Before requesting review:

1. Determine the risk level. Walk the low-risk allowlist in
   `.agents/references/doc-quality-policy.md` — if every condition holds, the
   PR is `low`; otherwise (including any ambiguous case) it is
   `engineering-review-required`.
2. Build the `## Documentation risk` block:
   ```bash
   python3 .agents/skills/doc_quality_policy/finalize_pr_contract.py build \
     --risk low --rationale "One-line reason."
   ```
   Insert the printed block into the PR body, alongside the existing
   `## Unverified claims` section (see `create_pr/SKILL.md`).
3. Apply the marker label:
   ```bash
   gh pr edit <pr> --repo warpdotdev/docs --add-label warpy-factory
   ```
4. Before marking the PR ready, verify the contract locally:
   ```bash
   python3 .agents/skills/doc_quality_policy/check_pr_contract.py --body /tmp/pr-body.md
   ```

## Using this from CI

The `Docs technical references` CI job (see `.github/workflows/ci.yml`) runs
`check_pr_contract.py` against the PR body and the changed docs files on every
pull request, failing on an unlisted `VERIFY` marker, a missing/invalid risk
section, or (once wired to live PR review data) an unsatisfied engineering
gate.
