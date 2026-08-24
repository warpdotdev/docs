# Changelog docs-worthiness decisions

Append-only ledger of every docs-worthiness verdict on a changelog item.

## Why this file exists

`feature_surface_map.md` keys on flags, CLI commands, API routes, slash commands, and settings. A changelog item has no key there, so a rejected item has nowhere to be recorded — and an unrecorded rejection is re-proposed on the next run, forcing the same reviewer to reject the same item again.

This ledger is that missing key. **Triage reads it first and skips any PR number already decided.**

## How to use it

**Before triage:** read this file. Skip any changelog item whose PR number already appears with a `no` or `deferred` verdict, unless the deferral condition has since cleared.

**During triage:** add a row for every item you evaluate — passes and rejections both. Apply `.agents/references/docs-worthiness-criteria.md`.

**Deferred items:** a `deferred` verdict means Gate 0 failed and the item may qualify later. Name the blocking condition in the reason. On each run, re-check only the deferred rows; if the condition has cleared, re-evaluate and update the row in place, moving it to `yes` or `no`.

**Committing:** ledger updates belong in the companion audit-bookkeeping PR alongside `feature_surface_map.md` and `surface_snapshot.json`, per the skill's PR strategy. Never split the ledger across multiple PRs.

## Verdicts

- **yes** — passed a gate; a docs change was made. Name the outcome (new page or the page updated).
- **no** — failed all gates, or a disqualifier applied. Permanent; do not re-evaluate.
- **deferred** — Gate 0 failed. Re-check when the named condition clears.

A row whose only passing gate is **Gate 4** must record an update as its outcome, never a new page — see the outcome cap in `.agents/references/docs-worthiness-criteria.md`. Its reason also has to carry both halves of the gate's evidence: the job that was impossible before, and the in-product surfaces checked and found silent.

## Ledger

Newest first. One row per PR number — usually a `warpdotdev/warp` changelog item, occasionally a `warpdotdev/docs` PR evaluated against the gate after the fact.

| PR | Decided | Verdict | Gate / disqualifier | Reason and outcome |
|---|---|---|---|---|
| [docs#582](https://github.com/warpdotdev/docs/pull/582) | 2026-08-20 | yes | Gate 3 | Factory Dashboard metric definitions (APP-5546). The counting rules are non-obvious and currently live only in hover tooltips: the By-model view caps at eight and folds the rest into Other, there is an Unknown bucket, and opened/merged pull request counts can legitimately disagree. A reader reading the dashboard without them draws wrong conclusions. New reference page justified — no existing page carries per-metric detail. |
| [docs#581](https://github.com/warpdotdev/docs/pull/581) | 2026-08-20 | deferred | Gate 0 | `agentDefaults.computerUseModel` is unreleased — the drafting PR said so in its own title. Real knob, would pass Gate 1, but Gate 0 is a hard prerequisite. Re-check when the setting ships to GA. |
| [#14418](https://github.com/warpdotdev/warp/pull/14418) | 2026-08-20 | yes | Gate 1 | Agent execution profiles configurable from settings files for all users. Named settings-file configuration. Update the existing agent profiles page. |
| [#14344](https://github.com/warpdotdev/warp/pull/14344) | 2026-08-20 | no | Disqualified: pure UI affordance | Armadillo icon replaced with the theme-adaptive Warp "W" logo. Nothing configurable, nothing to get stuck on. |
| [#14298](https://github.com/warpdotdev/warp/pull/14298) | 2026-08-20 | no | Disqualified: small and intuitive | MCP tool confirmations now show the running tool and its source server. Understood on sight. |
| [#14268](https://github.com/warpdotdev/warp/pull/14268) | 2026-08-20 | yes | Gate 1 | Vim `<` and `>` indent and dedent operators. Concrete bindings; add a row to the existing Vim operators reference table. Not a new page. |
| [#14219](https://github.com/warpdotdev/warp/pull/14219) | 2026-08-20 | yes | Gate 2 | Managed secrets validated against the 128 KiB limit (`MAX_SECRET_FIELD_BYTES`). Specific failure at create/update time with a non-obvious workaround. Update the existing secrets page. |
| [#14132](https://github.com/warpdotdev/warp/pull/14132) | 2026-08-20 | yes | Gate 2 | `gcloud` signs in automatically during GCP provider setup. Multi-step credential flow; changes which steps the user performs. Update the existing provider setup page. |
| [#14028](https://github.com/warpdotdev/warp/pull/14028) | 2026-08-20 | no | Disqualified: no user-observable change requiring action | Desktop toast stack capped and expandable. Improves on its own; the user does nothing differently. |
| [#13938](https://github.com/warpdotdev/warp/pull/13938) | 2026-08-20 | yes | Gate 1 | Custom model endpoints can select an OpenAI Chat Completions, OpenAI Responses, or Anthropic Messages schema. Named selector with three values the user must choose between. Update the existing custom endpoints page. |

## Notes

The `warpdotdev/warp` rows come from the `v0.2026.07.29.09.05.stable_02` changelog and double as the calibration set in `.agents/references/docs-worthiness-criteria.md`. Rows marked `yes` record the verdict, not that the docs change has shipped — several are still open PRs.

The two `warpdotdev/docs` rows were the regression cases used to validate the gate when it was introduced: docs#581 must fail Gate 0 because it documents an unreleased setting, and docs#582 must pass, because a gate that rejects everything is as broken as one that accepts everything.
