# Recurring docs consistency audit
## Summary
Add a reusable `docs_consistency_audit` skill to `warpdotdev/docs` and a dedicated Monday, Wednesday, and Friday automation to `warpdotdev/docs-factory-config`. The audit will find semantic conflicts between related factual claims without sending the full docs corpus to one model prompt. It will persist claim and finding state between runs, verify every reportable suspect against full source context and authoritative sources, and report only actionable lifecycle changes.
## Evidence and current state
The Falconer audit inspected about 51 pages and reported 19 contradictions plus 5 content issues. The examples cover numeric plan limits, billing waterfalls, security defaults, telemetry behavior, feature gating, CLI flags, API paths and parameters, operating-system support, install-method exceptions, migration status, terminology drift, and duplicate canonical explanations. Several examples also show the main false-positive risk: two claims can differ correctly because their plan, operating system, version, install method, legacy status, or time scope differs.

The docs checkout currently contains 389 Markdown or MDX pages and about 4.38 MB of source under `src/content/docs/`. A whole-corpus prompt would be expensive, hard to resume, and difficult to evaluate.

Existing infrastructure already owns adjacent checks:

* `style_lint` owns deterministic terminology and formatting checks (`.agents/skills/style_lint/SKILL.md:75`).
* `validate_ui_refs` owns Settings paths and Command Palette names and already refreshes source-derived snapshots (`.agents/skills/validate_ui_refs/SKILL.md:161`).
* `missing_docs` owns surface coverage and already exposes reusable CLI and API parsers in `.agents/skills/missing_docs/scripts/audit_docs.py:647` and `.agents/skills/missing_docs/scripts/audit_docs.py:810`.
* `check_for_broken_links` and `weekly-404-monitor` own link and redirect health. The new audit must not duplicate those checks.
* The factory already uses dedicated scheduled agents that invoke a repo-local docs skill, for example `automations/tuesday-thursday-missing-docs-drift-watch/automation.md:1` and `agents/Missing Docs Drift Watch Agent/agent.md:1` in `warpdotdev/docs-factory-config`.
* The docs skill-authoring guidance requires durable state on a dedicated branch, one standing PR, explicit write verification, and actionable-only Slack notifications (`.agents/references/skill-authoring-guidelines.md:13`, `.agents/references/skill-authoring-guidelines.md:40`, and `.agents/references/skill-authoring-guidelines.md:143`).
## Product behavior
1. The reusable skill can run manually or from the scheduled factory agent.
2. The default audit covers current public product documentation under `src/content/docs/`.
3. The default audit excludes changelog history, the 404 page, historical release notes, generated redirect stubs, and explicitly allowlisted historical migration text.
4. Generated or structured references are authority inputs, not ordinary peer pages. These inputs include the public OpenAPI document, billing-tier configuration, CLI definitions and generated help, the terminology glossary, content variables, and the public pricing page.
5. The audit extracts factual claims with typed values and explicit qualifiers. It does not treat general explanatory prose as a factual claim unless the prose asserts product behavior, availability, limits, defaults, requirements, identifiers, or lifecycle state.
6. The audit compares only claims that share a normalized topic, entity, and predicate and whose qualifiers overlap. It does not perform all-to-all page comparisons.
7. A universal claim can conflict with a narrower counterexample. Two narrower claims with disjoint qualifiers do not conflict.
8. Every reportable finding includes:
   * title;
   * category;
   * severity;
   * confidence;
   * lifecycle state;
   * exact claim quotes;
   * repository path, heading anchor, and source line range for each quote;
   * normalized qualifiers for each claim;
   * a concise conflict rationale;
   * the likely canonical source and the authority reason;
   * a suggested resolution;
   * the audit run and source commit identifiers.
9. Finding lifecycle values are `new`, `existing`, `changed`, and `resolved`. A recurrence after resolution is reported as `changed` with `reopened: true`.
10. The full run artifact includes all active findings, lifecycle changes, suppressed candidates, coverage, source availability, and cost counters.
11. Slack receives one concise top-level message only when the run has new, changed, or resolved high-confidence findings, a high-severity medium-confidence finding that needs policy review, or a blocking failure. Unchanged findings remain in the run artifact and state.
12. The first release does not edit docs or open fix PRs. A later phase can add mechanical fixes only after a separate approval and measured precision.
13. A partial or degraded run never marks a finding resolved. It carries prior findings forward and records the missing source or unfinished shard.
## Technical design
### Repository placement
The implementation will span two repositories after this specification is approved.

In `warpdotdev/docs`:

* `.agents/skills/docs_consistency_audit/SKILL.md` defines manual and scheduled workflows.
* `.agents/skills/docs_consistency_audit/scripts/audit_consistency.py` provides deterministic inventory, normalization, blocking, fingerprinting, lifecycle, reporting, and state commands.
* `.agents/skills/docs_consistency_audit/scripts/test_audit_consistency.py` provides the standard-library regression suite.
* `.agents/skills/docs_consistency_audit/references/authority_rules.json` defines source classes, category precedence, exclusions, and release-scope constraints.
* `.agents/skills/docs_consistency_audit/references/benchmark_cases.json` stores minimal, source-grounded Falconer and negative-control fixtures. It stores the claim pairs and expected classification, not a copy of the external report.
* `.agents/skills/docs_consistency_audit/references/suppressions.json` stores reviewed intentional exceptions with an owner, reason, source scope, and expiration date.
* `.agents/logs/docs_consistency_audit_runs.md` stores one compact entry per completed or blocked run.
* `.agents/state/docs_consistency_audit/` is generated only on the standing state branch. It contains a manifest, finding index, and per-page claim shards.

In `warpdotdev/docs-factory-config`:

* `agents/Docs Consistency Audit Agent/agent.md` defines a dedicated, high-reasoning audit agent that starts in `/workspace/docs`, treats sibling repos as read-only sources, and posts exactly one result to `#growth-docs` when required.
* `automations/monday-wednesday-friday-docs-consistency-audit/automation.md` defines paired UTC schedules and instructs the agent to apply the Pacific-time guard before work.

The skill is the workflow source of truth. The factory agent and automation remain thin wrappers.
### Stage 1: preflight and inventory
The deterministic script will:

1. Verify `/workspace/docs`, `/workspace/warp`, and `/workspace/warp-server` exist.
2. Record each repository commit and branch. It will not claim a production fact solely from an unreleased source branch.
3. Fetch the standing state branch `chore/docs-consistency-audit-state`. It will fail loudly rather than fall back to stale state when the branch exists but cannot be fetched.
4. Enumerate Markdown and MDX pages and record path, route, title, headings, source hash, and page role.
5. Apply explicit exclusions before model work.
6. Compare source hashes and extractor versions with the prior manifest. Only new, changed, deleted, or invalidated pages enter claim extraction.

The first run is a bootstrap. Later runs are incremental. A manual `--full` mode invalidates all page claim shards without deleting finding history.
### Stage 2: authoritative source adapters
Structured sources should produce typed claims deterministically when possible:

* **Plan gating and limits:** Parse the effective self-serve policies in `warp-server/billing/config/tiers/`, including inheritance. The current source includes `free.yaml`, `build.yaml`, `build_max.yaml`, and `self_serve_business_plan.yaml`. Compare these claims with the live pricing page and docs prose. Record the server ref and public-page fetch time.
* **Public API:** Parse `developers/agent-api-openapi.yaml` as the released public-doc authority. Use `warp-server/public_api/openapi.yaml` only as a freshness and provenance check. Respect `x-internal` and the existing sync policy so internal endpoints never become public claims.
* **CLI:** Reuse the `missing_docs` CLI parser for commands, subcommands, flags, hidden state, and rollout gates. Where a built CLI is available, generated help is stronger than handwritten source parsing. Record the CLI source ref and visible feature flags.
* **Terminology and renames:** Read `.agents/references/terminology.md` and `src/data/vars.ts`. Delegate exact deprecated-term matches to `style_lint`; the consistency audit handles only semantic migration conflicts, such as incompatible end dates or old and new names presented as simultaneous canonical names.
* **Product behavior:** Use public Warp source and existing source-derived snapshots when a behavior has a stable extractor. Do not infer user-visible behavior from a private or non-GA symbol alone.
* **Security and privacy:** Use source-backed settings and public canonical security or privacy pages as evidence. Never auto-resolve policy from source precedence alone. Conflicts about retention, training, telemetry, redaction, permissions, or data handling always require human review.

A missing authority source lowers confidence. It does not cause the model to invent a canonical answer.
### Stage 3: claim extraction
Model-driven extraction runs only for new or changed page sections that contain candidate factual language. A deterministic prefilter selects sections with:

* numbers, limits, dates, ordered steps, or comparison tables;
* plan, billing, pricing, credit, security, privacy, retention, telemetry, or permission terms;
* defaults, requirements, support, availability, or lifecycle language;
* CLI commands, flags, file paths, API routes, methods, parameters, schema fields, or enumerated values;
* migration, legacy, renamed, deprecated, resolved, or end-of-support language.

The model receives one bounded section plus page metadata. It returns schema-valid JSON only. The script rejects unsupported quotes, invalid line ranges, and claims whose evidence is not an exact substring of the source section.

Each claim has this logical shape:

```json
{
  "claim_id": "sha256:...",
  "source": {
    "repository": "warpdotdev/docs",
    "path": "src/content/docs/platform/harnesses/index.mdx",
    "route": "/platform/harnesses/",
    "heading": "Plan requirements",
    "line_start": 42,
    "line_end": 44,
    "content_sha256": "..."
  },
  "topic": "plan-gating",
  "entity": "third-party-cloud-harness",
  "predicate": "minimum-plan",
  "value": {"type": "plan", "normalized": "BUILD"},
  "qualifiers": {
    "plans": ["FREE", "BUILD", "MAX", "BUSINESS", "ENTERPRISE"],
    "operating_systems": [],
    "versions": [],
    "install_methods": [],
    "legacy": false,
    "time_scope": null
  },
  "polarity": "affirmative",
  "quote": "Third-party harnesses require a Build plan or higher.",
  "extraction_confidence": 0.97,
  "source_class": "docs-prose"
}
```

Values use explicit types such as boolean, integer, decimal, duration, bytes, plan, ordered-list, enum, path, flag, parameter, version, date, or free-text. Unit conversion happens deterministically after extraction.
### Stage 4: normalization and blocking
The deterministic index uses `topic + entity + predicate` as its primary block key. It normalizes:

* aliases from the terminology glossary and authority rules;
* plan names and plan ordering;
* operating systems, shells, install methods, and legacy modes;
* numeric units and ranges;
* API path templates and parameter naming;
* CLI commands and flags;
* booleans, defaults, and ordered waterfalls;
* time and version ranges.

Candidate generation uses these rules:

1. Split a block by incompatible qualifiers before comparison.
2. Compare every prose claim to the highest-authority compatible claim when one exists.
3. Compare peer claims only when no authority claim exists or when the authority sources disagree.
4. For large blocks, use an authority-centered star rather than every pair. This changes the common case from quadratic comparisons to linear comparisons per block.
5. Run exact deterministic detectors first for typed mismatches such as `3000 != 5000`, `enabled != disabled`, different ordered credit waterfalls, singular versus plural paths, different parameter names, and incompatible support matrices.
6. Send only unresolved semantic suspects to model adjudication.

Duplicated-canonical candidates use page role, topic ownership, inbound links, and similarity. FAQ and migration pages are not allowed to become canonical merely because they repeat a claim.
### Stage 5: qualifier compatibility and false-positive controls
The classifier must evaluate these dimensions before declaring a contradiction:

* plan or account type;
* operating system, architecture, shell, and host type;
* product and CLI version;
* installation method;
* local, cloud, self-hosted, or managed environment;
* user-triggered, scheduled, API-key, or other actor context;
* legacy, preview, beta, or GA status;
* time range and migration window;
* explicit exception language.

Two specific claims with disjoint qualifiers are compatible. A universal claim conflicts with a supported specific exception unless the universal claim contains matching exception language.

Before a finding becomes reportable, the verifier reads:

* the complete section for every claim;
* the preceding and following section when they define scope;
* frontmatter and page title;
* the applicable authority excerpt;
* any suppression matching the finding identity.

The verifier must quote the scope language that supports its decision. Unknown or missing qualifiers reduce confidence. The verifier can return `contradiction`, `stale`, `duplicate-canonical`, `gap`, `intentional-exception`, `insufficient-evidence`, or `not-related`.
### Stage 6: authority, severity, and confidence
Authority is category-specific and contextual. It is not one global rank.

* **Plan gating and numeric limits:** effective billing policy and the live pricing source outrank general docs prose. A disagreement between those two authorities is a high-severity human-review finding.
* **API:** the released, curated public OpenAPI document outranks handwritten guides. Internal or unreleased server paths are excluded.
* **CLI:** generated visible help outranks CLI source definitions, which outrank prose. Hidden or non-GA definitions do not invalidate public docs.
* **Terminology:** the terminology glossary and content variables outrank ordinary prose. Time-boxed migration guidance can intentionally use a legacy term.
* **Product behavior:** a source-derived public behavior or canonical owning page outranks FAQ summaries and old migration pages.
* **Security, privacy, and billing policy:** authority helps identify likely ownership but never authorizes an automated edit.

Severity values are:

* `high`: a conflict can cause unexpected billing, data handling, access-control, security, failed API or CLI integration, or a materially wrong plan purchase decision;
* `medium`: a conflict changes feature availability, defaults, limits, supported environments, or a primary workflow;
* `low`: stale terminology, migration ambiguity, duplicate explanations, or minor reference drift without an immediate failed action.

Confidence values are:

* `high`: exact typed incompatibility with compatible qualifiers and full-source verification, or an authority-backed direct contradiction;
* `medium`: semantic incompatibility with compatible qualifiers but incomplete authority evidence;
* `low`: plausible ambiguity, weak entity matching, or missing scope. Low-confidence candidates remain in the full artifact but are not Slack findings.
### Stage 7: identity, fingerprints, and lifecycle state
All fingerprints use SHA-256 over canonical JSON with sorted keys.

* `claim_id` hashes repository, path, stable heading anchor, normalized topic, entity, predicate, and qualifier key. It excludes quote text and line numbers so ordinary edits do not create a new identity.
* `claim_content_fingerprint` hashes the normalized value, qualifiers, polarity, and exact quote.
* `finding_id` hashes category, topic, entity, predicate, and the sorted participating claim identities. It excludes severity, confidence, rationale, and line numbers.
* `finding_content_fingerprint` hashes claim content fingerprints, canonical-source choice, severity, confidence, rationale class, and suggested-resolution class.

Lifecycle rules are deterministic:

* No prior `finding_id` means `new`.
* Same ID and same content fingerprint means `existing`.
* Same ID and changed content fingerprint means `changed`.
* A prior active ID absent from a complete comparison scope means `resolved`.
* A prior resolved ID that becomes active means `changed` with `reopened: true`.

A path move can preserve identity through `vercel.json` redirects. Without a verified redirect, it becomes one resolved and one new finding rather than a guessed continuation.
### State schema and atomic updates
The standing branch is `chore/docs-consistency-audit-state`. The standing PR title is `chore: docs consistency audit state`.

The state tree contains:

* `manifest.json`: schema version, extractor version, authority-rules version, model identifier, source repository refs, last completed run, coverage status, and page-shard map;
* `claims/<encoded-page-id>.json`: one page hash and its extracted claims;
* `findings.json`: active and resolved finding metadata, fingerprints, first-seen and last-seen runs, and suppression references;
* `.agents/logs/docs_consistency_audit_runs.md`: compact counts, coverage, source availability, cost, and run URL.

The run writes state to a temporary tree, validates it, then replaces the working state. It stages only state and log paths, verifies the new manifest and commit, pushes, and verifies the remote SHA. If extraction, verification, or state validation fails, the prior branch remains authoritative and the run reports the failure.

Resolved finding tombstones remain in `findings.json` so recurrence can be identified. Deleted-page claim shards remain for one successful full audit, then are removed.

Suppressions are reviewed source files on `main`, not generated state. Each suppression requires:

* finding ID or narrowly-scoped matcher;
* reason;
* owner;
* created date;
* expiration date;
* expected qualifier difference or intentional exception.

Expired suppressions become changed findings that require review.
### Stage 8: cost and scalability controls
The pipeline controls cost through:

* content hashes and incremental per-page claim shards;
* deterministic section prefiltering;
* deterministic extraction for structured authorities;
* topic/entity/predicate blocking;
* authority-centered comparison instead of all-to-all pairs;
* model adjudication only for unresolved suspects;
* full-source rereads only for candidates that survive blocking;
* bounded parallel shards with explicit page, character, candidate, and model-call counters in the run artifact.

A run that exceeds its configured budget finishes the current shard, records a backlog, sets coverage to `partial`, and does not emit resolved findings. The next run resumes from the manifest. Changing the extraction schema, model contract, or authority rules invalidates only affected shards when possible. A manual full audit validates incremental state after such changes.
### Recurring run workflow
The scheduled automation uses two cron triggers:

* `0 17 * * 1,3,5` for Pacific daylight time;
* `0 18 * * 1,3,5` for Pacific standard time.

Before any research, the agent checks `America/Los_Angeles`. It continues only when the local day is Monday, Wednesday, or Friday and the local hour is 10. The inactive DST schedule exits with one explicit run-output line and no Slack post.

An active run performs this sequence:

1. Preflight repositories, source refs, credentials, and state branch.
2. Run adjacent deterministic checks and import only their relevant outputs. Do not reimplement them.
3. Build the inventory and changed-page extraction plan.
4. Extract and validate claims for changed shards.
5. Refresh structured authority claims when their source hash changes.
6. Build blocked candidate groups and run deterministic detectors.
7. Adjudicate surviving suspects with full source context.
8. Apply suppressions and calculate lifecycle deltas.
9. Write JSON and Markdown run artifacts.
10. Atomically update and push the standing state branch and run log.
11. Post at most one Slack message when the actionable-only rule applies.

The Slack message includes counts for new, changed, resolved, and unchanged active findings; the highest-severity titles; the standing state PR when it changed; and the environment-correct run URL. It does not include all quotes or low-confidence candidates.
### Failure behavior
The run is blocked when:

* the docs repository or prior state branch cannot be read;
* a required structured authority cannot be parsed;
* a claim quote cannot be verified against source;
* the state schema or fingerprint integrity check fails;
* model output repeatedly fails schema validation;
* a state push fails.

A non-required authority can be unavailable only when the report records the gap and the missing source cannot change the answer. Otherwise the run is blocked. Blocked and partial runs preserve prior active findings and never mark findings resolved.
## Decisions
### Use indexed comparisons instead of a whole-repo prompt
Options considered:

* Send all docs to one model prompt. This is simple but expensive, non-resumable, context-limited, and hard to evaluate.
* Compare every extracted claim pair. This is complete in theory but quadratic and noisy.
* Build a typed claim index and compare related blocks. This adds schema and normalization work but gives bounded cost, traceable candidates, and deterministic lifecycle state.

Decision: use the typed index and related-claim blocks.
### Use deterministic code for mechanics and models for semantics
Options considered:

* Use only deterministic rules. This has high precision for paths, numbers, and flags but misses paraphrased behavior conflicts.
* Use only model reasoning. This covers paraphrases but makes inventory, state, and reproducibility weak.
* Combine deterministic inventory, normalization, blocking, exact detectors, and lifecycle with model extraction and final semantic adjudication.

Decision: use the combined design. Deterministic code owns every operation that can be made exact.
### Persist state in Git
Options considered:

* Run artifacts only. These are not a reliable input to later runs.
* Add a database or object store. The current factory has no such integration and it adds credentials and operations.
* Use a dedicated branch and standing PR, following the docs repository's existing inner-loop pattern.

Decision: use the dedicated Git branch and standing PR. Keep state machine-readable and sharded to limit routine diffs.
### Treat authority as contextual evidence
Options considered:

* Use one global rank. This is easy but wrong for unreleased code, curated API subsets, and policy text.
* Let the model choose authority with no registry. This is flexible but inconsistent.
* Encode category-specific source classes, release scope, and tie behavior in a reviewed registry.

Decision: use the reviewed authority registry. Escalate conflicts between authorities instead of silently choosing one.
### Make v1 detection-only
Options considered:

* Open automatic fix PRs for every high-confidence finding.
* Auto-fix only mechanical findings in v1.
* Measure detection precision first and add fixes in a later approved phase.

Decision: make v1 detection-only. Existing `style_lint` and `validate_ui_refs` retain their current mechanical auto-fix responsibilities.
## Assumptions
The following choices are pending requester approval:

* **Assumption:** V1 performs detection and reporting only. It does not open docs-fix PRs.
* **Assumption:** The audit indexes all current public docs except changelog/history and redirect stubs. Structured references and selected source files act as authorities.
* **Assumption:** State persists on `chore/docs-consistency-audit-state` with one standing PR in `warpdotdev/docs`.
* **Assumption:** The reporting destination is the top level of `#growth-docs` (`C09BVK0PL3Y`) and notifications are actionable-only.
* **Assumption:** The active cadence is Monday, Wednesday, and Friday at 10:00 a.m. Pacific, implemented with paired UTC schedules and a timezone guard.
* **Assumption:** Rollout begins with a manual bootstrap and Falconer benchmark. The schedule remains disabled until the precision gate passes.
## Out of scope
* Fixing the 24 Falconer findings as part of this work.
* Implementing the skill, scripts, state branch, agent, or automation in this specification PR.
* Replacing existing broken-link, 404, style, UI-reference, missing-docs, OpenAPI-sync, or terminology-sync skills.
* Automatically deciding ambiguous billing, security, privacy, legal, or product policy.
* Automatically editing docs or merging PRs.
* Auditing historical changelog claims as if they describe current behavior.
* Adding a vector database, external state service, or new long-lived credential in v1.
* Comparing private or unreleased source behavior with public docs without a release-scope guard.
## Rollout safeguards
1. Run the bootstrap manually. Do not enable the schedule during bootstrap.
2. Evaluate the classifier against all 24 Falconer examples. Each example must be detected, delegated to an existing deterministic skill, or explicitly rejected with a documented scope reason.
3. Include negative controls for plan, operating-system, version, install-method, legacy, and intentional-exception differences.
4. Review the top 30 current-repo findings manually.
5. Require at least 90% precision among high-confidence findings, at least 80% precision among all surfaced findings, and zero incorrect high-confidence security, privacy, or billing-policy conclusions.
6. Run three manual incremental audits and verify stable finding IDs, no duplicate notifications, and correct new, existing, changed, and resolved transitions.
7. Enable the factory automation only after the bootstrap state PR exists, the state can be fetched in a fresh environment, and the precision gate passes.
8. Keep detection-only shadow mode for four weeks. Review suppressions and cost counters before proposing any auto-fix phase.
## Validation criteria
The implementation is complete only when all checks below pass.

* Run `python3 .agents/skills/docs_consistency_audit/scripts/test_audit_consistency.py`. Tests must cover inventory exclusions, exact quote validation, typed normalization, qualifier compatibility, universal-versus-specific conflicts, authority selection, candidate blocking, stable fingerprints, all lifecycle transitions, suppression expiry, and incomplete-run resolution protection.
* Run the Falconer benchmark command defined by the skill. It must produce a machine-readable scorecard for all 24 examples and negative controls and meet the rollout thresholds.
* Run a bootstrap audit twice on the same source commits. The second run must reuse the claim cache, report no false lifecycle changes, and make no model calls for unchanged page extraction.
* Modify one fixture claim and run an incremental audit. The report must classify the finding as `changed`, not as an unrelated new and resolved pair.
* Remove one fixture conflict and run a complete audit. The report must classify it as `resolved`.
* Repeat the removal with one required source unavailable. The report must remain partial and must not classify it as resolved.
* Run `python3 .agents/skills/style_lint/style_lint.py --all --output /tmp/style-lint.json`, `python3 .agents/skills/validate_ui_refs/validate_ui_refs.py --all --output /tmp/ui-refs.json`, and the relevant `missing_docs` extraction tests. The consistency audit must consume or delegate adjacent results without duplicating their findings.
* Run `git diff --check` in both implementation repositories.
* Run `python3 "/agent/opt/warpdotdev/oz-dev/resources/bundled/skills/factory-files/scripts/validate_factory_files.py" /workspace/docs-factory-config`. Report the validator's exact outcome and do not treat exit 2 as a pass.
* Verify a guarded inactive schedule run exits without state changes or Slack output.
* Verify an active manual run writes the full artifact, updates the standing state branch atomically, and posts no Slack message when only unchanged findings exist.
* Verify a simulated new high-confidence finding produces exactly one Slack message with the correct lifecycle counts and run URL.
* No visual proof is required because this work has no rendered UI change.
