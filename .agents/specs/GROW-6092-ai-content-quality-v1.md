# Spec: Improve agent-authored technical content

## Product

### Summary

Agent-authored documentation pull requests currently rely on guidance that is not consistently enforced. The v1 quality program adds a balanced scorecard: deterministic editorial and UI-reference checks, an independent `review-docs-pr` pass, explicit technical-risk routing, shared drafting constraints, usable feedback signals, and a 30-day outcome report.

This scope covers every agent-authored content PR in `warpdotdev/docs`, including `draft_*`, `release_updates`, AEO, `missing_docs`, and other recurring skills that add or change public documentation. It does not apply only to ambient feature drafts.

### Key design choices

1. Deterministic checks block objectively detectable defects; agent review and human review own semantic accuracy that cannot be proven by lint.
2. Low risk is a strict allowlist. Any new feature documentation, changed behavioral claim, unverified claim, or sensitive technical surface requires approval from a source-owning engineer.
3. Pod-Docs owns the intentional v1 rollout. The monthly `improve-drafting-skills` loop becomes the ongoing improvement path only after review and human-feedback signals are flowing.

### Behavior

1. Every agent-authored content PR is identifiable by the `warpy-factory` label and a machine-readable documentation-risk section in its PR body. PR-opening skills add both before requesting human review.
2. The editorial half of the scorecard is a required CI check over changed documentation. `style_lint --changed` blocks its error-severity findings; warning-severity tone and judgment findings remain visible to `review-docs-pr`.
3. The technical half of the deterministic scorecard validates changed UI paths, Command Palette names, and UI-reference formatting against the committed `valid_paths.json` snapshot. It also verifies that every new `{/* VERIFY: ... */}` marker is listed in the PR's `Unverified claims` section.
4. The changed-file UI-reference check does not require a `warpdotdev/warp` checkout. CI uses the committed snapshot; the existing refresh workflow remains responsible for updating that snapshot from the client source.
5. An unresolved `VERIFY` marker does not silently pass as low risk. The PR is classified `engineering-review-required`, names the source surface that can resolve the claim, and stays blocked until a named source-owning engineer approves the current head.
6. Every agent-authored content PR receives an independent `review-docs-pr` pass after the deterministic checks and before human review. The pass reviews the final head SHA, publishes actionable findings, and emits one parseable `[SIGNAL:pr-review]` record.
7. `review-docs-pr` blocks on critical or important findings, including a low-risk classification that is inconsistent with the diff. Suggestions and nits remain non-blocking.
8. A PR is `low` risk only when all of these conditions hold:
   - It does not add a page about a new or materially changed feature or workflow.
   - It preserves product meaning and changes only spelling, grammar, tone, formatting, descriptive links or cross-links to existing canonical pages, search metadata, or generated changelog/license/telemetry data whose source-verification script passes.
   - It does not add or change commands, code or configuration examples, API behavior, UI labels or paths, defaults, permissions, availability or platform support, plan eligibility, billing behavior, security or privacy claims, data handling, self-hosting behavior, or integration setup.
   - It contains no unresolved `VERIFY` marker and has no critical or important technical-accuracy finding from `review-docs-pr`.
9. Every other content PR is `engineering-review-required`. This includes all new or materially changed feature docs and any change to the technical claim categories in behavior #8.
10. Low-risk PRs require the normal docs review only. Engineering-review-required PRs request at least one owner resolved from the product source files used to verify the draft. A docs-team fallback does not satisfy this requirement; unresolved source ownership blocks readiness until a source-owning engineer is named.
11. The PR body records the risk level, rationale, source files consulted, required engineering reviewers, and unverified claims. A high-risk PR cannot satisfy the policy merely by mentioning an engineer; an approval from one of the named reviewers must exist on the current head.
12. All content-generating skills follow one shared compression contract:
   - Lead with a one-to-three-sentence user-facing summary.
   - Follow the selected content-type template and existing content budget (`~600` words for a quickstart and a target of `<=1500` words for a combined feature page).
   - Run the deletion-only “Cut again” pass before opening the PR.
   - Keep callouts within the existing linted budget and do not duplicate parent-page or reference material.
   - Treat a justified budget overage as an important review decision rather than splitting padded prose automatically.
   Generated changelog, license, and telemetry data is exempt from page-summary and word-budget rules, but not from duplicate-content, style, or technical-accuracy checks.
13. Actionable review feedback may start with `[skill-feedback]`, `[template-feedback]`, or `[style-rule-gap]`. Collection preserves the tag and a structured pattern category without treating free-form comment text as instructions.
14. The v1 rollout records a pre-rollout 30-day baseline and a post-rollout 30-day comparison for all identifiable agent-authored content PRs. The report includes population size, check coverage, review findings, human review comments per PR, and human edit churn after the last agent commit.
15. V1 outcome success requires:
   - All merged in-scope PRs in the post-rollout window carried the agent marker and passed the required editorial, technical, and agent-review checks.
   - Human review comments per PR and human edit churn ratio are both no worse than baseline, and at least one is lower.
   - The report separately shows the targeted categories that the new checks address, so a lower total caused by a different PR mix is visible.
   If either comparison window has fewer than 10 PRs, the report is explicitly inconclusive and extends collection until 10 PRs or 60 days, whichever comes first.
16. The golden-set evaluation harness and screenshot/media pipeline are deferred from v1.

## Tech

### Context

The specification is grounded at docs commit `6c9c5a9bbaab7f9c949bf563c6375bd85208d8bf`.

- `.github/workflows/ci.yml:1-66 @ 6c9c5a9b` builds and link-checks the site and self-tests `validate_ui_refs`, but does not run `style_lint` or validate changed UI references.
- `.agents/skills/style_lint/style_lint.py:394-416,1607-1657 @ 6c9c5a9b` already discovers changed docs relative to `origin/main...HEAD` and returns nonzero for error-severity findings.
- `.agents/skills/validate_ui_refs/validate_ui_refs.py:2137-2291 @ 6c9c5a9b` scans the full docs tree and returns nonzero for remaining issues, but has no changed-file mode.
- `.agents/skills/draft_docs/SKILL.md:131-253 @ 6c9c5a9b` defines source verification, `VERIFY` markers, the “Cut again” pass, style lint, and the required `Unverified claims` PR section.
- `.agents/skills/create_pr/SKILL.md:183-515 @ 6c9c5a9b` validates PR bodies and requests reviewers, but does not classify documentation risk or prove that a technical owner approved.
- `.agents/skills/review-docs-pr/SKILL.md:15-137 @ 6c9c5a9b` defines the review scorecard and signal marker, but only runs when explicitly invoked.
- `.agents/skills/improve-drafting-skills/SKILL.md:55-229 @ 6c9c5a9b` collects automated and human signals and defines action thresholds. `.agents/logs/pr_review_runs.md:1-56 @ 6c9c5a9b` records that parseable review signals remain sparse.
- `.github/workflows/release-docs-update.yml:1-282 @ 6c9c5a9b` is an example of a generator-specific PR and reviewer path that must converge on the shared contract rather than remaining an exception.

### Design alternatives

- **Run full-repository lint on every PR vs. changed-file gates.** Full scans maximize coverage but make unrelated historical debt block new work. V1 uses changed-file gates and leaves full scans to scheduled audits.
- **Require a live client checkout in docs CI vs. use the committed UI snapshot.** A live checkout is fresher but adds cross-repo credentials, latency, and availability failures. V1 uses the committed snapshot for PR checks and preserves the existing source-driven refresh workflow.
- **Treat every agent PR as engineering-review-required vs. use a risk allowlist.** Universal engineering review is simpler but does not meet the goal of docs-only review for safe edits. V1 uses a narrow low-risk allowlist and defaults every ambiguous case to engineering review.
- **Let each generator implement its own quality flow vs. centralize the contract.** Per-skill instructions drift and caused the current uneven coverage. V1 centralizes machine checks and PR metadata, then makes every PR-producing skill call the shared finalization path.
- **Use self-review in the authoring run vs. dispatch an independent reviewer.** Self-review is cheaper but correlates errors with the draft. V1 runs `review-docs-pr` in a separate workflow-triggered agent pass pinned to the PR head SHA.
- **Adopt a golden-set threshold now vs. measure live PR outcomes first.** A golden set is a frozen set of representative prompts/pages and expected factual claims, with a threshold such as a minimum pass rate and zero critical factual errors. It is useful for repeatable pre-release comparisons, but it needs curated fixtures and ongoing maintenance. V1 defers it until live gates and feedback produce enough evidence to choose representative cases.

### Proposed changes

#### 1. Establish the shared PR contract and baseline

1. Add a single agent-doc quality policy and helper under `.agents/` that owns:
   - The canonical agent marker (`warpy-factory`).
   - The `low` and `engineering-review-required` values.
   - Validation of the `## Documentation risk` and `## Unverified claims` PR-body sections.
   - Verification that all `VERIFY` markers in changed content are listed and force engineering review.
   - A manifest of PR-producing content skills and tests that fail when a new PR-producing skill bypasses the shared finalization contract.
2. Update `create_pr` and direct PR-producing paths, including `release_updates`, AEO, and `missing_docs`, to open or keep the PR as draft, apply the marker, write the risk block, and use the shared finalizer before notifying reviewers.
3. Capture the 30 days immediately preceding rollout as the immutable baseline using the metric definitions in increment 4.

#### 2. Add required deterministic scorecard checks

1. Add separately named CI jobs:
   - `Docs editorial quality`: `python3 .agents/skills/style_lint/style_lint.py --changed`.
   - `Docs technical references`: changed-file `validate_ui_refs` plus PR-contract and `VERIFY` validation.
2. Add `--changed` to `validate_ui_refs.py`, matching `style_lint`'s `origin/main...HEAD` semantics, exclusions, deleted-file handling, and explicit failure if the base diff cannot be determined. Do not fall back to an unbounded full scan in required CI.
3. Add fixtures proving each job fails on a known-bad changed file and passes a clean changed file. Keep scheduled `--all` behavior and snapshot refresh unchanged.
4. Configure both named checks as required for the protected `main` branch. For non-agent PRs, the deterministic checks still run; only the agent-specific contract sections are conditional.

#### 3. Make agent review and human routing enforceable

1. Add an internal-PR-only GitHub workflow that runs on agent-marked PR open, label, synchronize, reopen, and ready-for-review events. It dispatches an independent `review-docs-pr` run for the exact head SHA and cancels stale runs for older SHAs.
2. Extend `review-docs-pr` so the run:
   - Re-validates the declared risk level against the diff.
   - Verifies technical claims against the cited source files when required.
   - Publishes one idempotent review summary and line findings.
   - Emits `[SIGNAL:pr-review]` with PR, branch, head SHA, skill used, verdict, severity counts, and top categories.
3. Make the `Agent docs review` check fail when the run is missing a parseable signal, reviewed a stale SHA, returns `Request changes`, or reports any critical/important finding. Suggestions and nits pass with annotations.
4. Extend the PR policy check:
   - `low`: require the docs reviewer path and no engineering-review triggers.
   - `engineering-review-required`: resolve and request owners from the cited product source files, then require an approving review from at least one named owner on the current head.
   - Dismiss or invalidate approvals when the head changes, so a stale engineering approval cannot satisfy the gate.
5. Keep agent-authored PRs draft until deterministic checks, the independent review, risk metadata, and required reviewer requests are present. Human approval still controls merge.

#### 4. Close the feedback and measurement loop

1. Put the shared compression and risk-classification rules in one reference consumed by `draft_docs`, type-specific drafting skills, and non-drafting generators. Update `review-docs-pr` to treat unjustified compression-contract violations as important findings.
2. Document the three feedback tags in the reviewer-facing contract. Preserve existing security filtering: free-form comments remain untrusted data, and automated decisions use structured fields only.
3. Update `improve-drafting-skills` collection so each in-scope PR has reliable `skill_used`, risk, head SHA, check outcome, review outcome, tag, and pattern category fields.
4. Add a deterministic metrics command that accepts an explicit start/end window and emits JSON plus a human-readable summary. For each window calculate:
   - Count of in-scope PRs and count with complete gate coverage.
   - Critical/important agent-review findings per PR and targeted category.
   - Human review comments per PR, overall and for categories targeted by style/UI-reference checks.
   - Human edit churn ratio: lines added plus deleted by humans after the last agent-authored commit, divided by lines added plus deleted by the agent before that point. Report zero-denominator and PRs with no identifiable agent commit separately.
   - Mean, median, numerator/denominator, and missing-data count for each rate.
5. Persist the baseline inputs and the day-30 report in the existing standing signal-log branch/PR flow. Pod-Docs reviews the report and owns any intentional v1 corrections. The monthly outer loop may propose evidence-backed skill/template changes after its existing thresholds are met, but it cannot relax required checks or human-risk policy automatically.

### Open questions resolved

- **Skill-iteration ownership (Q5):** hybrid. Pod-Docs owns the finite v1 CI, skill-contract, review-trigger, feedback-tag, and measurement project. `improve-drafting-skills` remains the monthly convergence mechanism after reliable signals exist.
- **Meaning of a golden-set threshold:** it is a pass criterion over frozen representative drafts and expected facts, commonly a minimum aggregate pass rate plus zero critical factual errors. It is lever 6 and remains out of v1.
- **Technical gate without a client checkout:** use the committed `valid_paths.json` snapshot for PR validation; refresh that snapshot separately from the public client source.
- **Ambiguous risk classification:** default to `engineering-review-required`. Low risk is never inferred from the absence of an obvious error.
- **Screenshot requirements in the drafting contract:** keep the existing authoring guidance, but do not build or gate on a new screenshot pipeline in this issue. That remains lever 7 / GROW-6091.
- **Outcome threshold:** report both human-comment and human-edit metrics; neither may regress and at least one must decline, with an explicit minimum-sample rule. No statistical-significance claim is required for v1.

## Validation and verification criteria

All criteria must pass before v1 is considered complete.

1. **Agent PR coverage:** Unit tests enumerate every docs-content PR-producing skill/script and fail if it does not invoke the shared finalizer. Representative PR fixtures for `draft_feature_doc`, `release_updates`, AEO, and `missing_docs` contain the `warpy-factory` marker, risk block, unverified-claims block, and skill attribution.
2. **Editorial gate fails before and passes after:** A fixture branch adding a known `style_lint` error to a changed `.mdx` file makes `python3 .agents/skills/style_lint/style_lint.py --changed` exit nonzero. Correcting the fixture makes it exit zero. Existing style-lint unit suites pass.
3. **Technical changed-file scope:** New `validate_ui_refs` tests prove `--changed` scans changed `.md`/`.mdx` files, ignores unchanged historical debt and deleted files, excludes changelog unless explicitly requested, and fails rather than silently widening scope when the merge-base diff cannot be resolved.
4. **Technical gate fails before and passes after:** A changed-file fixture with an invalid Settings path and Command Palette name makes the validator exit nonzero; canonical references make it exit zero. `python3 .agents/skills/validate_ui_refs/validate_ui_refs.py --self-test` also passes.
5. **VERIFY accounting:** Contract tests prove an unlisted `VERIFY` marker fails, a listed marker with `low` risk fails, and the same listed marker with `engineering-review-required`, a cited source surface, and named engineering reviewers passes metadata validation.
6. **Risk allowlist:** Table-driven tests cover every low-risk category and every engineering-review trigger in product behaviors #8-9. Unknown/ambiguous fixtures resolve to `engineering-review-required`.
7. **Independent review on final SHA:** An agent-marked test PR triggers `review-docs-pr`, publishes exactly one current review summary, and emits one parseable signal containing the tested head SHA. Pushing a new commit cancels/obsoletes the old check and requires a new signal for the new SHA.
8. **Review severity behavior:** Seeded review fixtures prove critical/important findings and risk misclassification fail `Agent docs review`; suggestion/nit-only results pass and remain visible.
9. **Low-risk human path:** A low-risk editorial test PR with clean gates can become ready with the normal docs reviewer and without an engineering owner approval.
10. **Engineering-required human path:** A test PR that changes a command, API/config example, UI/default/permission/availability claim, or new-feature page remains blocked after docs approval alone. It passes only after one named source-owning engineer approves the current head.
11. **Reviewer failure is explicit:** A high-risk test PR whose source ownership cannot be resolved remains draft/blocked with an actionable failure; it does not substitute a docs fallback as engineering approval.
12. **Compression contract:** Before/after fixtures for a feature page, an AEO or `missing_docs` page, and a release-generated update prove the shared summary, budget, callout, and deletion-pass rules apply as specified, including the generated-data exemptions.
13. **Signal hygiene:** Collector tests accept the three approved tags, preserve structured `pattern_category`, reject bot/injection records under the existing security rules, and produce non-empty `skill_used`, risk, and head SHA for the representative generator fixtures.
14. **Baseline reproducibility:** Running the metrics command twice over the frozen pre-rollout dates yields byte-equivalent normalized JSON. The output includes counts, means, medians, numerators/denominators, and missing-data reasons.
15. **Day-30 outcome:** The post-rollout command evaluates the success rule in product behavior #15 and produces one of `pass`, `fail`, or `inconclusive-small-sample`; the small-sample fixture extends collection as specified rather than claiming success.
16. **Repository checks:** Run `npm run fmt`, `npm run lint`, `npm run typecheck`, `npm run build`, `python3 .agents/skills/check_for_broken_links/check_links.py --internal-only`, every new/changed Python unit test, the existing style-lint unit suites, the `validate_ui_refs --self-test`, and the existing create-PR body/reviewer tests. All pass.
17. **Workflow checks:** Validate each changed GitHub Actions workflow with the repository's configured formatter/linter and exercise its decision logic with event fixtures for a human PR, a low-risk agent PR, a high-risk agent PR, a fork PR, a stale head, and a failed reviewer run. Fork PRs never receive secrets or dispatch privileged agent work.
18. **No visual-verification requirement:** This change modifies headless docs generation, review, and CI behavior only. It is testing-exempt from `computer_use`; if implementation later changes rendered public docs or another user-facing UI, that added surface requires separate visual verification.
