# Automatic docs usability validation

The [Docs usability workflow](../../.github/workflows/docs-usability.yml) dispatches a read-only agent to apply the [reader walkthrough method](docs-usability-validation.md). It reads the exact PR head as data and follows actual rendered links in a current-head Vercel preview. It does not run fixture calibration, approve PRs, fix content, or grade usability from record completeness.

## Activation and coverage

Automation starts only after the workflow and helper are merged onto the default branch. A repository administrator must make `WARP_API_KEY` available to Actions with access to run the Warp Agent CLI. Existing references to the secret do not prove that it is configured. No branch-protection change is required or included.

Open, synchronize, reopen, readiness, draft conversion, and edit events inspect every PR author without label filtering. Applicability includes changed, deleted, and previous renamed paths under `src/`, `public/`, `scripts/`, `plugins/`, and `developers/`, plus Astro, Vercel, package, and TypeScript configuration. The filter is conservative; the evaluator chooses a full walkthrough or the method's reduced navigation/link scope from the actual diff. Governance-only changes are explicitly not applicable to a public walkthrough and still need their relevant workflow tests.

A draft or missing current-head preview records Not tested. A successful `Preview` deployment by `vercel[bot]` retries the associated open PRs. Preview selection requires an exact head SHA and an HTTPS `*.vercel.app` URL; an old published page is not substituted. A protected preview, unavailable renderer, absent CLI credentials, failed dispatch, cancellation, or invalid result leaves missing evidence explicit.

Fork PRs do not receive the API key or an evaluator run. A manual retry does not override that boundary. A maintainer must review the change and move it to a trusted repository branch before automatic evaluation. Do not execute fork code with privileged credentials to obtain a result. Same-repository PR code is also never checked out, built, or run by this workflow: the evaluator reads it as data with a read-only GitHub token. The separate publisher holds check-write permission and no Warp API key.

## Read the result

Open **Docs usability validation** in the PR's checks. Each check is neutral and pinned to the tested head. Its title distinguishes:

* **Walkthrough reported: clear** - The agent reports a completed walkthrough without unresolved findings.
* **Walkthrough reported: findings** - The walkthrough reports friction or gaps; inspect question-level evidence and readiness.
* **Reduced-scope checks reported** - The agent reports completed mechanical navigation/link checks, not a substantive walkthrough.
* **Not applicable** - No public documentation or rendering path changed.
* **Not tested** - Required evidence or trusted execution was unavailable.

The check includes the agent report, head and base SHAs, trusted workflow revision, selected preview, and run link. The run artifact retains the request, trusted prompt, raw output, and execution outcome for 90 days. Longer reports are truncated in the check; the artifact retains the raw output. Copy evidence needed beyond retention into the PR's validation record.

A green Actions job only confirms orchestration. An agent-reported Clear is advisory evidence, not human acceptance, engineering review, or proof of evaluator reliability. Inspect its entry points, paths, answers, limitations, and primary-task readiness against the method. A transport test that publishes synthetic Clear text does not count as a real walkthrough.

New commits require new evidence. Publication rechecks scope, trust, base, head, and preview; stale output stays in its original artifact rather than validating the new head. Per-PR evaluation concurrency cancels superseded jobs. A serialized publisher prevents older runs from replacing newer evidence. Duplicate events reuse an existing report only for the same head, base, preview deployment, and trusted workflow revision.

## Retry and verify activation

After merge, confirm that the secret is available without displaying its value. Select **Actions** > **Docs usability** > **Run workflow** on the default branch and enter the open PR number, or run `gh workflow run docs-usability.yml --repo warpdotdev/docs --ref main -f pr=PR_NUMBER`. Replace `PR_NUMBER` with the PR number. Manual dispatch deliberately reevaluates the current head even when a prior report exists; it does not bypass draft, preview, or fork restrictions.

Use a trusted substantive docs PR with an available current-head preview for the first activation check. Confirm that the action actually executed, inspect its raw report, follow a representative primary path, and verify that its SHA and preview match the final PR head. Also verify that a new commit invalidates old evidence and that absent preview or credentials yields Not tested. Event/dispatch unit tests do not prove deployed credentials, agent permissions, preview access, or semantic reliability.

If a run fails before it can publish a check, the failed Actions run is the evidence of failure; no usability result exists. Restore the missing service or permission, then dispatch again on the default branch. There is no automatic scheduled reconciliation, so existing PRs need a new listed event or manual retry after activation or recovery.
