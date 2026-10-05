---
name: docs_consistency_audit
description: >-
  Audit Warp's current public docs for semantic contradictions, stale factual claims,
  conflicting plan or billing rules, security or privacy inconsistencies, CLI and API
  drift, and competing canonical explanations. Use for a manual consistency audit, the
  Monday/Wednesday/Friday scheduled audit, Falconer benchmark validation, or lifecycle
  checks for new, changed, existing, reopened, and resolved findings. This skill detects
  and reports issues only; it never edits docs or opens fix pull requests.
---

# Docs consistency audit

Find conflicting factual claims without sending the full docs corpus to one prompt.
Deterministic code owns inventory, normalization, blocking, authority selection,
fingerprints, lifecycle, and state. Model reasoning is limited to bounded claim
extraction and unresolved semantic adjudication.

## Detection-only boundary

V1 does not edit public docs or open fix pull requests. Do not apply a finding even when
it looks mechanical. Existing skills retain their ownership:

- Exact terminology and style findings go to `style_lint`.
- Settings paths and Command Palette names go to `validate_ui_refs`.
- Surface coverage and code-surface extraction go to `missing_docs`.
- Broken links and redirect gaps go to `check_for_broken_links` or
  `weekly-404-monitor`.
- Public OpenAPI drift goes to `sync-openapi-spec`.

Record delegated findings in the run artifact. Do not duplicate them as consistency
findings.

## Environment and state

Run every command from `/workspace/docs`. The workflow requires:

- `/workspace/docs` at the current default branch for public documentation and the
  released OpenAPI document.
- `/workspace/warp` at its current default branch as the public client and CLI source.
- `/workspace/warp-server` at its current default branch as a read-only authority input.
  Private source is evidence only and must not appear in public reports.
- The connected Slack MCP for the scheduled agent. Post only to `#growth-docs`
  (`C09BVK0PL3Y`) and only under the actionable-only rule below.

Generated state lives on `chore/docs-consistency-audit-state`, under
`.agents/state/docs_consistency_audit/`. Keep exactly one standing pull request titled
`chore: docs consistency audit state`. The state branch also carries
`.agents/logs/docs_consistency_audit_runs.md`.

Never fall back to `main` when the state branch exists but cannot be fetched. A quieter,
stale state can change lifecycle answers and is worse than a blocked run.

## Scheduled guard

The paired schedules cover Pacific daylight and standard time. Before any research, run:

```bash
python3 .agents/skills/docs_consistency_audit/scripts/audit_consistency.py schedule-guard
```

Exit `0` means the local time in `America/Los_Angeles` is Monday, Wednesday, or Friday
at 10:00 a.m. Continue. Exit `10` is the inactive half of the pair: write exactly one run
output line stating that the Pacific-time guard was inactive, then stop without reading
state, changing files, or posting to Slack. Any other exit is a blocked run.

## Workflow

### 1. Preflight sources and state

```bash
python3 .agents/skills/docs_consistency_audit/scripts/audit_consistency.py preflight \
  --docs-repo /workspace/docs \
  --warp-repo /workspace/warp \
  --warp-server /workspace/warp-server \
  --fetch-state-branch \
  --output /tmp/docs-consistency-preflight.json
```

Record all three commits and branches. Do not use a non-default source branch as proof of
released behavior. When the state branch exists, check it out in a temporary worktree or
read its state files through `git show`; never replace the implementation checkout with
the state branch.

If the state branch does not exist, this is a bootstrap. The bootstrap stays manual until
the rollout gate passes.

### 2. Run adjacent deterministic checks

Run the owning checks and save their machine-readable output:

```bash
python3 .agents/skills/style_lint/style_lint.py --all --output /tmp/style-lint.json
python3 .agents/skills/validate_ui_refs/validate_ui_refs.py --all --output /tmp/ui-refs.json
python3 .agents/skills/missing_docs/scripts/test_audit_docs.py
```

Import only relevant ownership and delegation signals. A failure in an adjacent check
blocks only when its missing output can change the audit answer; record other
unavailability in the full artifact and lower confidence.

### 3. Inventory pages and plan extraction

For a bootstrap or deliberate cache invalidation, add `--full`:

```bash
python3 .agents/skills/docs_consistency_audit/scripts/audit_consistency.py inventory \
  --docs-repo /workspace/docs \
  --previous-manifest /tmp/prior-docs-consistency-manifest.json \
  --max-pages 80 \
  --max-characters 750000 \
  --output /tmp/docs-consistency-inventory.json
```

The script excludes changelog history, release notes, the 404 page, redirect stubs, and
reviewed historical migration text before model work. It records route, title, headings,
role, source hash, and candidate factual sections. Only new, changed, deleted, or
invalidated pages enter extraction.

If the configured page or character budget is exhausted, finish the current shard, mark
coverage `partial`, retain the backlog, and do not resolve findings.

### 4. Refresh structured authorities

```bash
python3 .agents/skills/docs_consistency_audit/scripts/audit_consistency.py adapters \
  --docs-repo /workspace/docs \
  --warp-repo /workspace/warp \
  --warp-server /workspace/warp-server \
  --fetch-pricing \
  --output /tmp/docs-consistency-authorities.json
```

This reuses the `missing_docs` CLI and OpenAPI extractors, parses effective self-serve
billing policies with inheritance, records public and server OpenAPI hashes, and records
terminology and content-variable hashes. Generated CLI help, when available, replaces
source parsing as the stronger CLI authority. Record visible feature flags with generated
help.

The released `developers/agent-api-openapi.yaml` is the public API authority.
`warp-server/public_api/openapi.yaml` is only a freshness and provenance check. Never
turn an internal route into a public claim.

### 5. Extract claims from changed sections

Send one bounded candidate section plus page metadata to the model. Require JSON only.
Each claim must contain:

- `source`: repository, path, route, heading, stable heading anchor, exact line range,
  and content SHA-256.
- normalized `topic`, `entity`, and `predicate`;
- typed `value`;
- qualifiers for plans, operating systems, architectures, shells, versions, install
  methods, environments, actors, release status, legacy state, time scope, and explicit
  exceptions;
- polarity, exact quote, extraction confidence, and source class.

Accept value types `boolean`, `integer`, `decimal`, `duration`, `bytes`, `plan`,
`ordered-list`, `enum`, `path`, `flag`, `parameter`, `version`, `date`, `range`,
`support-matrix`, and `free-text`.

Reject a model response when a quote is not an exact substring of the specified source
lines, a line range is invalid, or required fields are missing. Retry schema-invalid
model output at most twice. A third failure blocks the run and preserves prior state.

General explanatory prose is not a claim unless it asserts product behavior,
availability, limits, defaults, requirements, identifiers, or lifecycle state.

### 6. Block and compare

The script compares only claims with the same `topic + entity + predicate`. It splits
blocks by incompatible qualifiers and centers large blocks on the highest compatible
authority. Run exact typed detectors before model adjudication.

Run a comparison prepass with the same `run` arguments shown in step 7, plus
`--no-state-write` and
`--candidate-output /tmp/docs-consistency-candidates.json`. Review every candidate where
`exact_typed_mismatch` is false with the model and the context below. Then add accepted
model decisions to the claims input under `adjudicated_findings` before the state-writing
run. Each adjudicated finding must contain the required finding fields, supported claims,
one allowed verdict, quoted rationale, authority reason, and suggested resolution class.
The script rejects unsupported quotes and schema-incomplete adjudications.

Two narrower claims with disjoint qualifiers do not conflict. A universal claim can
conflict with a narrower counterexample unless the universal claim contains matching
exception language.

Before reporting any surviving semantic suspect, read:

- the complete section for every claim;
- the preceding and following section when either establishes scope;
- page title and frontmatter;
- the applicable authority excerpt; and
- any matching suppression.

The verifier returns exactly one of `contradiction`, `stale`,
`duplicate-canonical`, `gap`, `intentional-exception`, `insufficient-evidence`, or
`not-related`. It must quote the scope language supporting its decision. Unknown
qualifiers reduce confidence.

Security, privacy, data handling, retention, training, telemetry, permission, redaction,
and billing-policy conflicts always require human review. Authority identifies likely
ownership; it never authorizes an automatic resolution.

### 7. Calculate lifecycle and write artifacts

Write validated claims to a JSON file, then run:

```bash
python3 .agents/skills/docs_consistency_audit/scripts/audit_consistency.py run \
  --claims /tmp/docs-consistency-claims.json \
  --inventory /tmp/docs-consistency-inventory.json \
  --repository-root warpdotdev/docs=/workspace/docs \
  --state-dir /tmp/docs-consistency-state \
  --source-commit "$(git rev-parse HEAD)" \
  --coverage complete \
  --model-identifier MODEL_ID \
  --model-calls MODEL_CALL_COUNT \
  --pages PAGE_COUNT \
  --characters CHARACTER_COUNT \
  --candidate-output /tmp/docs-consistency-candidates.json \
  --artifact-json /tmp/docs-consistency-run.json \
  --artifact-markdown /tmp/docs-consistency-run.md
```

The full artifact includes all active findings, lifecycle changes, suppressed
candidates, coverage, source availability, and cost counters. Every reportable finding
includes exact quotes and locations, qualifiers, rationale, likely authority and reason,
suggested resolution, run ID, and source commit.

Lifecycle is deterministic:

- a new identity is `new`;
- an unchanged identity and content fingerprint is `existing`;
- an existing identity with changed content is `changed`;
- a prior active identity absent from complete comparison scope is `resolved`;
- a resolved identity returning is `changed` with `reopened: true`.

Partial and blocked runs never resolve findings.

### 8. Validate and atomically persist state

```bash
python3 .agents/skills/docs_consistency_audit/scripts/audit_consistency.py validate-state \
  --state-dir /tmp/docs-consistency-state
```

The `run` command builds a temporary state tree, validates fingerprint integrity, and
replaces its target only after validation. After that local transaction:

1. Check out or create `chore/docs-consistency-audit-state` from `origin/main`.
2. Replace only `.agents/state/docs_consistency_audit/`.
3. Prepend one compact entry to `.agents/logs/docs_consistency_audit_runs.md`.
4. Verify the manifest, finding index, and new log heading before staging.
5. Stage only `.agents/state/docs_consistency_audit/` and
   `.agents/logs/docs_consistency_audit_runs.md`.
6. Validate state again, commit, and push.
7. Verify the remote SHA matches the pushed commit.
8. Create the standing draft PR if absent; otherwise update the existing branch. Never
   create a second state PR.

If extraction, verification, validation, commit, push, or remote-SHA verification fails,
leave the prior branch authoritative, write the failure to run output, and report a
blocked run.

### 9. Report only actionable changes

Post at most one top-level Slack message for:

- a new, changed, reopened, or resolved high-confidence finding;
- a high-severity medium-confidence finding needing policy review; or
- a blocked run.

Unchanged findings, low-confidence candidates, successful no-change runs, and the
inactive schedule guard do not post. The durable state and run log are their record.

The message includes counts for new, changed, resolved, and unchanged active findings;
up to three highest-severity titles; the standing state PR when it changed; and the
environment-correct run URL. Resolve the run URL from the current run at runtime. Never
hard-code a Warp host. Do not include all quotes or any private source path, symbol,
identifier, configuration value, or secret.

Generate the one decision and payload:

```bash
python3 .agents/skills/docs_consistency_audit/scripts/audit_consistency.py notification \
  --artifact /tmp/docs-consistency-run.json \
  --run-url RUN_URL \
  --state-pr-url STATE_PR_URL \
  --output /tmp/docs-consistency-notification.json
```

Call the connected Slack MCP once only when `should_post` is true, using `message`
verbatim. If posting fails, write the message to run output and report the delivery
failure. Do not retry in a way that can duplicate the top-level message.

## Benchmark and rollout gate

Run:

```bash
python3 .agents/skills/docs_consistency_audit/scripts/audit_consistency.py benchmark \
  --output /tmp/docs-consistency-benchmark.json
```

The scorecard covers all 24 Falconer examples and negative controls for plan, operating
system, version, install method, legacy status, and intentional exceptions. The schedule
must remain disabled until:

- all 24 examples are detected, delegated to their owning deterministic skill, or
  explicitly rejected with a scope reason;
- high-confidence precision is at least 90%;
- precision among all surfaced findings is at least 80%;
- there are no incorrect high-confidence security, privacy, or billing-policy
  conclusions;
- all negative controls pass;
- a human reviews the top 30 current-repo findings;
- three manual incremental audits show stable identities, no duplicate notifications,
  and correct lifecycle transitions; and
- a fresh environment fetches the bootstrap state branch.

Keep detection-only shadow mode for four weeks after activation.

## Verification

Run before changing the schedule:

```bash
python3 .agents/skills/docs_consistency_audit/scripts/test_audit_consistency.py
python3 .agents/skills/docs_consistency_audit/scripts/audit_consistency.py benchmark \
  --output /tmp/docs-consistency-benchmark.json
python3 .agents/skills/style_lint/style_lint.py --all --output /tmp/style-lint.json
python3 .agents/skills/validate_ui_refs/validate_ui_refs.py --all --output /tmp/ui-refs.json
python3 .agents/skills/missing_docs/scripts/test_audit_docs.py
git diff --check
```

Bootstrap twice against identical source commits. The second run must reuse every
unchanged claim shard, report no false lifecycle changes, and make no page-extraction
model calls. Then:

1. Change one fixture claim without changing its identity; verify `changed`.
2. Remove one fixture conflict from a complete run; verify `resolved`.
3. Repeat the removal with a required source unavailable; verify coverage is partial and
   the finding remains active.
4. Simulate a new high-confidence finding; verify the reporting decision produces one
   Slack payload.
5. Simulate only unchanged findings; verify no Slack payload is produced.

Record exact commands and outcomes in the standing state PR. Do not describe an
unavailable check as passing.

## Run log format

Prepend one entry after the file header:

```text
## YYYY-MM-DD — complete | partial | blocked
- Run: environment-correct URL or run ID
- Source commits: docs SHA; warp SHA; warp-server SHA
- Coverage: complete | partial | blocked; PAGES/TOTAL pages
- Findings: NEW new; CHANGED changed; RESOLVED resolved; ACTIVE active
- Suppressed: COUNT; expired: COUNT
- Cost: CHARACTERS characters; CANDIDATES candidates; MODEL_CALLS model calls
- Sources unavailable: none | comma-separated source classes
- State PR: URL | unchanged | unavailable
```

Keep the entry under 10 lines. Never include secrets or private source details.
