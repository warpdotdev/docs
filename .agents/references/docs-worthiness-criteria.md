# Documentation-worthiness criteria

Decide whether a shipped change should produce documentation at all.

Read this before drafting, and before proposing a doc gap as actionable. Every docs agent that can create or update a page must apply it: `missing_docs`, `draft_docs`, and any drafting skill they call.

This reference answers one question: **should this doc exist?** Once a change passes, `.agents/references/content-design-plan.md` answers the next question — what the doc should be. Never write a content design plan for a change that has not passed these gates.

## The default is no docs

Not every shipped change warrants documentation. The docs repo competes for reader attention with itself: every page added makes every other page harder to find, and a page nobody needs is a page someone still has to maintain, review, and keep accurate through the next three renames.

So the default answer is **no**, and the burden is on the change to earn a page. Do not look for a reason to document something. Look for concrete evidence that a reader will be stuck, surprised, or unable to configure something without it — and if you cannot find that evidence, the answer is no.

A changelog entry is not evidence. Neither is a merged spec, a Linear ticket, or the fact that a feature is new. Those establish that something happened, not that a reader needs help with it.

## Scope

These criteria govern the **weekly release stream** — changes that reached users in a stable release, and the continuously shipped server and platform surfaces behind them.

Major launches (Warp Factories, for example) are planned in advance and documented by the docs team on a proactive, human-led path. They do not run through these gates. If you encounter a change that is clearly part of an announced launch, defer it rather than gating it.

## Decision procedure

Work through the gates in order. Gate 0 is a hard prerequisite. Gates 1 through 3 are alternatives — passing any one is enough. Then check the disqualifiers, which override a pass on any gate.

### Gate 0 — Is it shipped and public?

A hard prerequisite. If this fails, stop.

- Is the feature GA to users, not dogfood, preview, or research preview?
- Is the surface public? The `warpdotdev/warp` client repo is public. **`warp-server` is private**, and its surfaces are not documentable until released; the exception is the public Agent API, whose released surface is exactly what is already in `developers/agent-api-openapi.yaml`.
- Is it gated behind a non-GA feature flag?

See the "Public vs. private surfaces" section of the `missing_docs` skill for the full rollout and exposure rules — this gate reuses them rather than restating them.

**Failing Gate 0 means defer, not reject.** The change may qualify later. Record it as deferred with the blocking reason so it re-surfaces when the flag goes GA or the endpoint reaches the spec. Do not draft "ready for when it ships" pages — an unreleased page that sits in a PR goes stale before it merges, and a merged one is wrong the day it publishes.

### Gate 1 — Is it configurable?

Can a user change its behavior? Name the concrete knob:

- A setting (give the `toml_path` key)
- A CLI flag or command
- An API parameter or request field
- A file-format field
- A toggle they can actually reach in the UI

If you cannot name the specific knob, this gate does not pass. "Users can configure the new behavior" is not a knob. `agents.warp_agent.profile` is a knob.

### Gate 2 — Can a user get stuck?

Either of these:

- **Error-prone setup.** A multi-step or technically detailed process where mistakes are likely — credentials, permissions, external service configuration, environment prerequisites. Name the steps.
- **A specific error message that demands a specific, different action.** Not a generic failure the user can reason about, but a message whose correct response is non-obvious. Quote the error string.

A limit or constraint qualifies here when hitting it produces a distinct failure the user must respond to differently.

### Gate 3 — Would a user be surprised?

Underlying logic changed in a way with a non-obvious user-visible effect. Typically one of:

- A default changed
- A permission or access boundary changed
- A billing or credit consequence changed
- Data handling, retention, or residency changed
- An existing workflow now behaves differently than it did before

The test is surprise, not novelty. Would a reasonable user, doing what they did last week, get a different result and not understand why?

### Disqualifiers

These override a pass on any gate. If one applies, the answer is no.

- **Pure UI affordance.** We do not document the UI. A new button, an icon change, a relocated control, a restyled panel.
- **Small and intuitive.** A reader who opens the surface would understand it in under thirty seconds without help.
- **No user-observable change.** Internal refactors, telemetry, performance work, CI, release mechanics, dependency bumps.
- **Bug fix restoring intended behavior.** The docs already describe how it is supposed to work; the fix made reality match. Document only if the docs described the broken behavior.

## Required justification

Every verdict must be recorded with a one-paragraph justification that names:

1. **The gate it passed**, or the disqualifier that stopped it.
2. **The concrete evidence** — the setting key, CLI flag, quoted error string, changed default, API field, or named setup steps.
3. **The source** — the changelog entry and PR number, or the surface and file you verified against.

**No concrete evidence means the answer is no.** A justification that restates the changelog entry in different words is not a justification. If the strongest thing you can say is "this is a new capability users should know about," the gate did not pass.

This rule exists because it is the only part of the procedure that cannot be satisfied by rephrasing. Gates can be argued into; naming a specific `toml_path` key or quoting a real error string cannot.

## Three outcomes, not two

Every passing change resolves to one of these. Choose explicitly:

1. **Update an existing page** — the default when any page already covers the surface. Prefer this. Most shipped changes are a paragraph, a row in a reference table, or a new subsection on a page that already exists.
2. **New page** — only when no existing page covers the surface and the change needs more than a section. A new page must be justified against the existing information architecture, not just against the change.
3. **No docs** — record the verdict so it is not re-litigated.

The bias toward updating is deliberate. New-page sprawl is the main way an automated pipeline degrades a docs set: each page is defensible alone, and collectively they fragment a topic across places no reader will assemble.

## Recording the verdict

Write every decision to `.agents/skills/missing_docs/references/changelog_decisions.md`, including the rejections. A decision that is not recorded gets re-proposed on the next run, and the reviewer who rejected it has to reject it again.

## Worked examples

Drawn from the `v0.2026.07.29.09.05.stable_02` changelog. These calibrate the boundary — the point is the reasoning, not the specific features.

### Passes

**Custom model endpoints can select an API schema** ([#13938](https://github.com/warpdotdev/warp/pull/13938)) — **Gate 1, update existing page.** The knob is the schema selector on a custom inference endpoint, with three named values: OpenAI Chat Completions, OpenAI Responses, and Anthropic Messages. A user configuring a custom endpoint must pick one and cannot guess which their provider expects.

**Managed secrets validated against the 128 KiB limit** ([#14219](https://github.com/warpdotdev/warp/pull/14219)) — **Gate 2, update existing page.** `MAX_SECRET_FIELD_BYTES` in `crates/managed_secrets/src/secret_value.rs` caps a secret at 128 KiB, validated at create and update time. The failure is specific, it surfaces at a different moment than the user expects, and the workaround is non-obvious. Belongs on the existing secrets page, not a new one.

**Automatic `gcloud` sign-in during GCP provider setup** ([#14132](https://github.com/warpdotdev/warp/pull/14132)) — **Gate 2, update existing page.** Provider setup is a multi-step credential flow where errors are likely, and this changes which steps the user performs.

**Vim indent and dedent operators** ([#14268](https://github.com/warpdotdev/warp/pull/14268)) — **Gate 1, update existing page.** `<` and `>` are concrete, nameable bindings, and the editor already has a reference table of supported Vim operators. This is a row in that table. It would *not* justify a new page.

**Agent execution profiles configurable from settings files** ([#14418](https://github.com/warpdotdev/warp/pull/14418)) — **Gate 1, update existing page.** Named settings-file configuration, previously unavailable to all users.

### Fails

**Replace the armadillo icon with the theme-adaptive Warp "W" logo** ([#14344](https://github.com/warpdotdev/warp/pull/14344)) — **Disqualified: pure UI affordance.** Nothing configurable, nothing to get stuck on, nothing surprising. We do not document the UI.

**Cap and expand the shared desktop toast stack** ([#14028](https://github.com/warpdotdev/warp/pull/14028)) — **Disqualified: no user-observable change requiring action.** Behavior improves on its own; the user does nothing differently.

**MCP tool confirmations show the tool and source server** ([#14298](https://github.com/warpdotdev/warp/pull/14298)) — **Disqualified: small and intuitive.** The confirmation dialog now shows more context. A reader encountering it understands it immediately.

**`agentDefaults.computerUseModel`** (docs PR [#581](https://github.com/warpdotdev/docs/pull/581)) — **Gate 0 failure: deferred, not documented.** This is the regression case. A drafting agent wrote the page and labeled it "(unreleased feature)" in the PR title, which is the gate failing out loud. An unreleased setting key is a real knob and would pass Gate 1 — but Gate 0 comes first and is a hard prerequisite. Defer with the blocking reason and re-surface it when the feature ships.

## Related references

- `.agents/references/content-design-plan.md` — what to decide once a change passes these gates
- `.agents/references/terminology.md` — canonical product terms
- `.agents/skills/missing_docs/references/changelog_decisions.md` — the recorded verdict ledger
