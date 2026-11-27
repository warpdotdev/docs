# Docs usability automation status

The [Docs usability workflow](../../.github/workflows/docs-usability.yml) is administratively disabled pending a reviewed default-branch definition. When enabled, it records applicability and missing evidence only. Evaluator execution remains disabled: applicable changes receive **Not tested**, even with a current preview. No API key, profile ID, or enable flag activates a walkthrough. Authors and independent reviewers still apply the [reader walkthrough method](docs-usability-validation.md).

## Trusted entry points

The workflow must exist on the default branch before it can record scope. PR events inspect the default target branch without label filtering. Vercel's successful `status` event retries associated open PRs at the exact current head. Maintainer retries use `repository_dispatch` with type `docs-usability-retry`. GitHub selects default-branch definitions for these status and repository dispatch events.

There is no `deployment_status` or `workflow_dispatch` trigger: those can select a topic-owned workflow definition. Before any checkout, a read-only provenance job verifies the workflow ref and run ref against the repository's actual default branch. It resolves an immutable default-branch commit independently of the event and workflow SHAs, then compares the selected workflow blob with that commit's blob. Every helper and instruction checkout, including the separate check-writing publisher, uses the verified commit. A missing or changed definition fails closed. Unmerged workflow changes cannot be tested through a privileged topic-branch dispatch.

No job checks out or runs PR code. Scope recording reads PR metadata through GitHub's API. It executes no evaluator, exposes no Warp credential, and treats filenames as data. Only the publisher has check-write permission. No branch-protection change is required or included.

## Coverage and results

Applicability includes changed, deleted, and previous renamed paths under `src/`, `public/`, `scripts/`, `plugins/`, and `developers/`, plus Astro, Vercel, package, and TypeScript configuration. Governance-only changes are **Not applicable** to a public walkthrough and still need their relevant workflow tests.

For applicable work, the scope record identifies a draft, untrusted fork, incomplete file list, or unavailable preview before recording the missing evaluator isolation. Preview selection requires a successful `Preview` deployment by `vercel[bot]`, an exact head SHA, and an HTTPS `*.vercel.app` origin. An old published page is not substituted. A manual retry does not bypass these checks.

Open **Docs usability validation** in the PR's checks. Every result is neutral and pinned to the inspected head. The only supported outcomes are **Not applicable** and **Not tested**. There is no Clear result or completed walkthrough transport. Fabricated evaluator output cannot change the publisher's independently recomputed decision.

The check records head, base, workflow and helper revisions, selected preview, and run link. The run artifact retains scope and undispatched instructions for 90 days, not an executed agent report. A green Actions job means scope recording completed, not that docs usability passed. Copy evidence needed beyond retention into the PR's validation record.

New commits require new evidence. Publication rechecks scope, head, base, and preview. Per-PR preparation cancels superseded jobs; serialized publication rejects older runs and attempts. Duplicate events reuse matching pending scope only for the same head, base, helper source, preview deployment, and outcome. Maintainer dispatch deliberately refreshes it.

## Retry scope recording

After a reviewed safe definition is merged, a repository administrator must re-enable the disabled workflow before scope recording can run. A maintainer with repository dispatch access can then retry an open PR. Replace `PR_NUMBER` with its number:

```bash
gh api repos/warpdotdev/docs/dispatches --method POST \
  -f event_type=docs-usability-retry -F 'client_payload[pr]=PR_NUMBER'
```

Repository dispatch has no branch selector. Confirm that the run used the default-branch definition and helper revision, that the check identifies the current PR head, and that applicable work remains Not tested. A new commit must not inherit evidence for an older head. Missing artifacts produce Not tested; failure before publication leaves only the failed Actions run, not a usability result. There is no scheduled reconciliation.

## Prerequisite for evaluator activation

Activation requires an approved, supported restrictive execution configuration and credential-isolated document access. Capabilities must be enforced outside the prompt: deny shell commands, writes, product mutations, arbitrary network access, and other tools beyond the approved read operations. The evaluator must not receive GitHub or Warp credentials through its environment, filesystem, or tools. A verified broker must constrain reads to the exact-head source, selected preview, and explicitly allowed linked destinations.

The current local action's `--sandboxed` flag declares an already-sandboxed host; it does not establish read-only tool permissions. GitHub read permissions do not restrict an agent's shell, and instructions alone do not enforce a capability boundary. A profile ID without verified policy and credential isolation is insufficient.

Keep execution disabled until the configuration owner supplies a supported contract that can be checked before launch. A separate implementation and verification must reject unavailable or over-permissive configuration and prove prompt-injected content cannot gain shell, write, or credential access. Then test an actual substantive current-head preview journey, retain its question-level report, and independently follow a representative primary path. Deterministic tests prove orchestration behavior, not deployed isolation or semantic evaluator reliability.
