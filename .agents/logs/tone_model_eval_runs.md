# Tone/concision model eval run log

Written whenever `.agents/skills/tone_model_eval/` runs a full comparison
(GROW-6139 and any later re-run). Records the actual per-model scores and the
recommendation verdict, plus a pointer to the raw rows/report for the
regression-comparison uses cited in `out_of_repo_handoff.md` step 6.

Newest entries first. Prepend, do not append.

Entry format:

```markdown
## YYYY-MM-DD — [adopt | no-difference | cheaper-model-recommended]
- **Fixtures**: N (ids)
- **Candidates**: model-id (role), ...
- **Judge model**: model-id
- **Composite scores**: model-id N.NN/5, ...
- **Verdict**: one line per recommendation arm
- **Data**: paths to rows.jsonl / report.json / report.md / per-row candidate output files
- **Oz run**: [URL]
- **Notes**: anything unusual (assumptions, retries, judge disagreements)
```

---

## 2026-09-10 — no-difference

- **Fixtures**: 3 (`cli-agent-conversations-resume-menu-label` — feature-doc, `byollm-gemini-enterprise-google-cloud-setup` — procedural, `quickstart-synthetic-verbose-seed` — synthetic quickstart)
- **Candidates**: `claude-5-1-fable-high` (Fable 5.1), `claude-4-5-sonnet` (current-default stand-in — **documented assumption**, see Notes), `claude-4-5-haiku` (cheaper), `gpt-5-mini` (cheaper)
- **Judge model**: `gemini-3.1-pro` (distinct family from every candidate; no same-family bias)
- **Composite scores**: `claude-5-1-fable-high` 4.33/5 (concision 4.67, avoids-over-explaining 4.67, technical-fidelity 3.67); `claude-4-5-sonnet` 4.11/5 (4.33 / 4.33 / 3.67); `claude-4-5-haiku` 3.89/5 (4.33 / 4.33 / 3.00); `gpt-5-mini` 3.44/5 (4.33 / 4.33 / 1.67). Combined mechanical violations (tone-buzzword + tone-meta-opener): 0 for every candidate.
- **Verdict**:
  - Adopt Fable-5.1-derived guidance: **no meaningful difference found** — concision-dimension margin over the default was 0.33 (need ≥1.0), mechanical-violation reduction was 0% (need ≥30%).
  - Recommend a cheaper model for production copy passes: **no candidate met the threshold** — `claude-4-5-sonnet` (judge gap 0.22, technical fidelity 3.67 < 4.0 min), `claude-4-5-haiku` (gap 0.44, fidelity 3.00 < 4.0), `gpt-5-mini` (gap 0.89, fidelity 1.67 < 4.0) all fail on technical fidelity.
- **Data**: `.agents/logs/tone_model_eval/2026-09-10-rows.jsonl`, `.agents/logs/tone_model_eval/2026-09-10-report.json`, `.agents/logs/tone_model_eval/2026-09-10-report.md`, and the 12 raw candidate rewrites (all 4 candidates × all 3 fixtures) under `.agents/logs/tone_model_eval/outputs/<fixture-id>__<model-id>.txt`
- **Oz run**: see GROW-6139
- **Notes**: First run (GROW-6139). `claude-4-5-sonnet` stands in for "the current production default model for docs drafting skills" as a **documented assumption**: live `oz-dev schedule list`/`schedule get` discovery against every schedule referencing docs drafting/audit skills found no explicit `model_id` in any schedule config — model selection for ad hoc/event-triggered drafting runs lives in the Warp app's Agent Profile UI (per `out_of_repo_handoff.md`), which isn't inspectable from this environment. `auto` was considered and rejected as the stand-in because it's a router that can resolve to different underlying models across calls, which would break the fixed-model comparison this eval depends on.

  Every technical-fidelity score below 5 was manually spot-checked against the source text and reflects a real defect, not judge noise. Two examples, each verifiable against the committed output file:
  - `gpt-5-mini` introduced an unsupported claim not present in the original quickstart draft ("Signing in also lets your Warp session mint short-lived credentials for integrations.") — see `.agents/logs/tone_model_eval/outputs/quickstart-synthetic-verbose-seed__gpt-5-mini.txt` line 11, scored in the `technical_fidelity: 1` row for `(quickstart-synthetic-verbose-seed, gpt-5-mini)` in `2026-09-10-rows.jsonl`.
  - `claude-4-5-haiku` dropped the original's "The priority is fixed and not admin-configurable" qualifier on host-priority order — compare `.agents/logs/tone_model_eval/outputs/byollm-gemini-enterprise-google-cloud-setup__claude-4-5-haiku.txt` ("### Host priority" section, no configurability qualifier) against the fixture's before text at commit `ca39ad1a0db873221fabf4bfc1f0e2417724b83a`, scored in the `technical_fidelity: 1` row for `(byollm-gemini-enterprise-google-cloud-setup, claude-4-5-haiku)` in `2026-09-10-rows.jsonl`.

  Per this outcome, `out_of_repo_handoff.md`'s checklist is skipped — no model/schedule/Agent Profile change to make.
