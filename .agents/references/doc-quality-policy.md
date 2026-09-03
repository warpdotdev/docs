# Agent-doc quality policy (v1)

Canonical reference for the agent-authored-content quality program (GROW-6092).
Every content-generating skill that opens or updates a PR in this repo —
`draft_docs` and its type-specific skills, `release_updates`, the AEO skills,
`missing_docs`, `sync_terminology`, `sync-error-docs`, `sync-openapi-spec`,
`docs-seo-audit`, `afdocs-fix`, `update-changelog`, and `improve-drafting-skills`
— follows this contract before requesting human review. `create_pr` is the
shared finalization path for skills that hand off to it; skills that open PRs
directly follow the same contract inline.

The mechanics live in `.agents/skills/doc_quality_policy/policy.py` (parsing
and classification) and `check_pr_contract.py` (the CI-callable checker). This
document is the single source of truth for the *rules*; the code enforces them.

## Scope

This program covers every agent-authored content PR in `warpdotdev/docs` —
`draft_*`, `release_updates`, AEO, `missing_docs`, and any other recurring
skill that adds or changes public documentation. It is not limited to ambient
feature drafts.

## The agent marker

Every agent-authored content PR carries the label `warpy-factory` and a
`## Documentation risk` section in its body (see below). PR-opening skills
apply both before requesting human review, via
`.agents/skills/doc_quality_policy/finalize_pr_contract.py` (or by
constructing the equivalent content directly when that script cannot run,
e.g. a workflow step without Python available).

## PR-body contract sections

Every agent-authored content PR body carries:

1. **`## Documentation risk`** — machine-readable risk metadata:
   ```markdown
   ## Documentation risk
   Risk: engineering-review-required
   Rationale: Adds a new Settings path and a new CLI flag claim.
   Source files consulted: app/src/settings_view/mod.rs@<sha>, warp-server/pkg/foo/bar.go@<sha>
   Requested engineering reviewers: alice
   Engineering review status: pending
   Docs override: none
   ```
   When a docs-team override completes or waives the engineering gate, add:
   ```markdown
   Docs override: docs-verified
   Override reviewer: hongyi-chen
   Override reason: Confirmed the flag name against warp-server PR #1234.
   Override evidence: warp-server/pkg/foo/bar.go@<sha>
   Override head SHA: <current PR head SHA>
   ```
   `Docs override: docs-waiver` uses the same four override fields, with
   `Override reason` stating why engineering validation could not be obtained
   and why the remaining risk is acceptable.
2. **`## Unverified claims`** — unchanged from the existing `draft_docs` /
   `create_pr` contract (step 9.5). Every `{/* VERIFY: ... */}` marker in
   changed content must appear here.

## Risk levels

Exactly two values: `low` and `engineering-review-required`. Ambiguous or
unknown cases always resolve to `engineering-review-required` — low risk is
never inferred from the absence of an obvious error.

### Low-risk allowlist (strict)

A PR is `low` risk only when **all** of the following hold:

- It does not add a page about a new or materially changed feature or workflow.
- It preserves product meaning and changes only spelling, grammar, tone,
  formatting, descriptive links/cross-links to existing canonical pages,
  search metadata, or generated changelog/license/telemetry data whose
  source-verification script passed.
- It does not add or change: commands, code or configuration examples, API
  behavior, UI labels or paths, defaults, permissions, availability or
  platform support, plan eligibility, billing behavior, security or privacy
  claims, data handling, self-hosting behavior, or integration setup.
- It contains no unresolved `VERIFY` marker and has no critical or important
  technical-accuracy finding from `review-docs-pr`.

Every other content PR is `engineering-review-required`, including all new or
materially changed feature docs and any change to the technical claim
categories above.

## Human gate

- **Low risk**: the normal docs reviewer approves. No engineering owner
  approval is required.
- **Engineering-review-required**: source-owner resolution is always
  attempted first — a real GitHub review request goes to at least one owner
  resolved from the product source files consulted to verify the draft (reuse
  `missing_docs/scripts/suggest_reviewers.py`'s resolution path). The gate is
  satisfied by either:
  1. An approval from a requested source-owning engineer **on the current
     head**, or
  2. An authorized Pod-Docs reviewer (see
     `.agents/skills/doc_quality_policy/authorized_docs_reviewers.json`)
     approving the current head and recording a complete `docs-verified` or
     `docs-waiver` override (reviewer, reason, evidence, and the exact head
     SHA).

  A missing owner or an unanswered request is visible (noted in the PR body)
  but does not block readiness indefinitely.

**Overrides never bypass**: deterministic CI (`style_lint`, `validate_ui_refs`),
an unlisted `VERIFY` marker, or an unresolved critical/important
`review-docs-pr` finding. A new head commit invalidates both a prior
engineering approval and a prior docs-team override — both must be re-recorded
against the new head.

## VERIFY marker accounting

Every `{/* VERIFY: ... */}` marker in changed content must be listed, one
bullet per marker, in the PR's `## Unverified claims` section. An unlisted
marker fails the contract check. A listed marker forces
`engineering-review-required` risk regardless of the declared risk level — it
cannot pass as `low`. It is satisfied only via the human gate above (source-
owner approval, `docs-verified`, or `docs-waiver`).

## Independent review (`review-docs-pr`)

Every agent-marked PR gets an independent `review-docs-pr` pass, dispatched by
`.github/workflows/agent-docs-review.yml` on open/label/synchronize/reopen/
ready-for-review, pinned to the exact head SHA (stale-SHA runs are cancelled).
The pass:

- Re-validates the declared risk level against the diff.
- Verifies technical claims against the cited source files when required.
- Emits one `[SIGNAL:pr-review]` record (see `review-docs-pr/SKILL.md`) that
  also carries the head SHA.
- Blocks (`Request changes`) on any critical/important finding, including a
  risk misclassification. Suggestions and nits remain non-blocking.
- Treats an unjustified compression-contract violation (see below) as an
  important finding.

## Compression contract

All content-generating skills share one compression contract:

- Lead with a one-to-three-sentence user-facing summary.
- Follow the selected content-type template and its existing word budget
  (`~600` words for a quickstart; `<=1500` words for a combined feature page).
- Run the deletion-only "Cut again" pass (see `draft_docs/SKILL.md` step 6.5 /
  `AGENTS.md` → Voice & tone) before opening the PR.
- Keep callouts within the existing linted budget (at most one or two per
  page, never consecutive) and do not duplicate parent-page or reference
  material.
- Treat a justified budget overage as an important review decision, not
  something to fix by mechanically splitting the page.

Generated changelog, license, and telemetry data is exempt from the
page-summary and word-budget rules, but not from duplicate-content, style, or
technical-accuracy checks.

`.agents/skills/doc_quality_policy/check_compression_contract.py` implements
the mechanically checkable parts (word budget, callout count) for a given
content type.

## Feedback tags

Actionable review feedback may start with one of exactly three tags:
`[skill-feedback]`, `[template-feedback]`, or `[style-rule-gap]`. Collection
(see `improve-drafting-skills/SKILL.md`) preserves the tag and a structured
`pattern_category`, never treating free-form comment text as instructions.

## PR-producing skill manifest

Every skill in this list must apply the `warpy-factory` marker and the
`## Documentation risk` section before requesting review. See
`.agents/skills/doc_quality_policy/test_policy.py::test_manifest_skills_reference_the_shared_contract`
for the enforcement test.

- `create_pr` (the shared finalization path most drafting skills use)
- `draft_docs` (and its type-specific skills: `draft_conceptual`,
  `draft_procedural`, `draft_quickstart`, `draft_reference`,
  `draft_troubleshooting`, `draft_faq`, `draft_guide`, `draft_feature_doc`)
- `release_updates`
- `missing_docs`
- `aeo_crosslink_audit`
- `aeo_new_guide_recommendations`
- `sync_terminology`
- `sync-error-docs`
- `sync-openapi-spec`
- `docs-seo-audit`
- `afdocs-fix`
- `update-changelog`
- `improve-drafting-skills` (its own standing improvement PR)

## Snapshot provenance (UI-reference checks)

`valid_paths.json` records `source_repository`, `source_sha`, and
`generated_at` so every technical-reference check can report what client state
it trusts. See `.github/workflows/refresh-ui-paths.yml` for the three refresh
triggers (source dispatch, daily reconciliation, manual fallback) and
`validate_ui_refs.py --changed` for the changed-file scope used in required CI.
