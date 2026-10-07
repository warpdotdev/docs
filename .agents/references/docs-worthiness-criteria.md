# Documentation-worthiness criteria

Decide whether a shipped change should produce documentation at all.

Read this before drafting, and before proposing a doc gap as actionable. Every docs agent that can create or update a page must apply it: `missing_docs`, `draft_docs`, and any drafting skill they call.

This reference answers one question: **should this doc exist?** Once a change passes, `.agents/references/content-design-plan.md` answers the next question — what the doc should be. Never write a content design plan for a change that has not passed these gates.

## The default is no docs

Not every shipped change warrants documentation. The docs repo competes for reader attention with itself: every page added makes every other page harder to find, and a page nobody needs is a page someone still has to maintain, review, and keep accurate through the next three renames.

So the default answer is **no**, and the burden is on the change to earn a page. Do not look for a reason to document something. Look for concrete evidence that a reader will be stuck, surprised, unable to configure something, or unable to discover a capability they now have — and if you cannot find that evidence, the answer is no.

A changelog entry is not evidence. Neither is a merged spec, a Linear ticket, or the fact that a feature is new. Those establish that something happened, not that a reader needs help with it.

## Scope

These criteria govern the **weekly release stream** — changes that reached users in a stable release, and the continuously shipped server and platform surfaces behind them.

Major launches (Warp Factories, for example) are planned in advance and documented by the docs team on a proactive, human-led path. They do not run through these gates. If you encounter a change that is clearly part of an announced launch, defer it rather than gating it.

### How much applies depends on who is asking

**Automated runs apply the full gate.** A scheduled agent has no context beyond what it can read, and unattended drafting at scale is what this reference exists to control. Default to no docs; make the change earn the page.

**A person asking directly is subject to Gate 0 only.** Gate 0 is factual — has this shipped, is the surface public — and a requester can be wrong about it, so it is worth verifying no matter who asked. Gates 1 through 4 are judgment, and someone requesting a page usually has context an agent does not: the roadmap, the support queue, a conversation the agent was not in.

So do not decline a person's request on Gates 1-4. Raise the concern once — "an existing page already covers this," "this looks like a UI-only change" — then defer to their answer. An agent arguing with someone who knows more than it does is a worse failure than one extra page.

The gates still shape *how* you draft for a human request: they push toward updating an existing page over creating a new one, and toward naming the concrete thing a reader needs.

## Decision procedure

Work through the gates in order. Gate 0 is a hard prerequisite. Gates 1 through 4 are alternatives — passing any one is enough. Then check the disqualifiers, which override a pass on any gate.

Gates 1 through 3 cover a reader who is already trying to do something and hits friction. Gate 4 covers the reader who does not know the capability exists, and it carries a capped outcome — see "Three outcomes, not two".

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

### Gate 4 — Is it a capability the reader cannot discover on their own?

Gates 1 through 3 all assume a reader who arrives with a problem. This gate covers the reader who does not know the thing is possible at all — the case those gates structurally cannot see.

It is also the easiest gate to talk yourself into, so **both** conditions must hold and both must be stated:

1. **The change makes a user job possible, not merely easier.** Name the job the reader could not do before at all. "Faster", "fewer steps", "more reliable", and "now also works in X" are improvements to an existing job — those belong to Gates 1 through 3, or to no docs.
2. **Nothing in the product surfaces it.** No Command Palette entry, menu item, settings toggle, onboarding hint, or error message points the reader at it. Name the surfaces you checked. If the Command Palette lists it, the product already tells the reader it exists.

The second condition is the discipline. Without it every changelog line passes, which is the failure this whole reference exists to prevent.

A capability that has a knob already passes Gate 1 and does not need this gate. Gate 4 is for capabilities with no knob and no affordance.

### Disqualifiers

These override a pass on any gate. If one applies, the answer is no.

- **Pure UI affordance.** We do not document the UI. A new button, an icon change, a relocated control, a restyled panel.
- **Small and intuitive.** A reader who opens the surface would understand it in under thirty seconds without help.
- **No user-observable change.** Internal refactors, telemetry, performance work, CI, release mechanics, dependency bumps.
- **Bug fix restoring intended behavior.** The docs already describe how it is supposed to work; the fix made reality match. Document only if the docs described the broken behavior.

## Required justification

Every verdict must be recorded with a one-paragraph justification that names:

1. **The gate it passed**, or the disqualifier that stopped it.
2. **The concrete evidence** — the setting key, CLI flag, quoted error string, changed default, API field, named setup steps, or (for Gate 4) the newly possible job plus the in-product surfaces you checked and found silent.
3. **The source** — the changelog entry and PR number, or the surface and file you verified against.

**No concrete evidence means the answer is no.** A justification that restates the changelog entry in different words is not a justification.

"This is a new capability users should know about" is still not a justification — it is the exact sentence Gate 4 exists to replace. Gate 4 does not accept the impression; it asks for two checkable facts instead: the job that was impossible before, and the surfaces you checked and found silent. Supply both or you have a hunch, not a verdict.

This rule exists because it is the only part of the procedure that cannot be satisfied by rephrasing. Gates can be argued into; naming a specific `toml_path` key, quoting a real error string, or listing the surfaces you checked cannot.

## Three outcomes, not two

Every passing change resolves to one of these. Choose explicitly:

1. **Update an existing page** — the default when any page already covers the surface. Prefer this. Most shipped changes are a paragraph, a row in a reference table, or a new subsection on a page that already exists.
2. **New page** — only when no existing page covers the surface and the change needs more than a section. A new page must be justified against the existing information architecture, not just against the change.
3. **No docs** — record the verdict so it is not re-litigated.

The bias toward updating is deliberate. New-page sprawl is the main way an automated pipeline degrades a docs set: each page is defensible alone, and collectively they fragment a topic across places no reader will assemble.

**A Gate 4 pass caps the outcome at an update.** When Gate 4 is the *only* gate a change passed, it resolves to an update to an existing page — never a new page. A capability nobody can stumble onto needs a sentence somewhere findable, not a page of its own. If it genuinely warrants a page, it will also pass Gate 1, 2, or 3; if it passes none of those, a paragraph on the page that owns the surrounding surface is the right size. This cap is what keeps the discoverability gate from reopening new-page sprawl.

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

**Drag and drop image files into an active CLI agent session** ([#9553](https://github.com/warpdotdev/warp/pull/9553)) — **Gate 4, update existing page.** The job — attaching a screenshot to a Claude Code session — was not possible before, not merely slower. There is no knob, so Gate 1 does not fire; nothing fails, so Gate 2 does not; behavior the reader relied on did not change, so Gate 3 does not. Checked for an affordance and found none: no Command Palette entry, no menu item, no toolbar control, no hint in the session UI. A reader who does not already know will never try it. One sentence on the CLI agent page; the Gate 4 cap rules out a new page.

### Fails

**`/continue-locally` slash command** ([#9500](https://github.com/warpdotdev/warp/pull/9500)) — **Fails Gate 4 on the second condition, but passes Gate 1.** Worth including because it shows the discipline working in both directions. The slash command menu lists it, so the product already tells the reader it exists and Gate 4 does not apply. It is also a nameable command, which is a knob, so Gate 1 carries it anyway. Failing Gate 4 is not the same as failing the gate.

**Silent fallback to a regular SSH session on hosts with an incompatible remote-server binary** ([#9681](https://github.com/warpdotdev/warp/pull/9681)) — **Fails Gate 4 on the first condition.** Connecting over SSH was always possible; this makes it more reliable on old glibc. "More reliable" is an improvement to an existing job, not a new capability. No other gate fires either.

**Replace the armadillo icon with the theme-adaptive Warp "W" logo** ([#14344](https://github.com/warpdotdev/warp/pull/14344)) — **Disqualified: pure UI affordance.** Nothing configurable, nothing to get stuck on, nothing surprising. We do not document the UI.

**Cap and expand the shared desktop toast stack** ([#14028](https://github.com/warpdotdev/warp/pull/14028)) — **Disqualified: no user-observable change requiring action.** Behavior improves on its own; the user does nothing differently.

**MCP tool confirmations show the tool and source server** ([#14298](https://github.com/warpdotdev/warp/pull/14298)) — **Disqualified: small and intuitive.** The confirmation dialog now shows more context. A reader encountering it understands it immediately.

**`agentDefaults.computerUseModel`** (docs PR [#581](https://github.com/warpdotdev/docs/pull/581)) — **Gate 0 failure: deferred, not documented.** This is the regression case. A drafting agent wrote the page and labeled it "(unreleased feature)" in the PR title, which is the gate failing out loud. An unreleased setting key is a real knob and would pass Gate 1 — but Gate 0 comes first and is a hard prerequisite. Defer with the blocking reason and re-surface it when the feature ships.

## Related references

- `.agents/references/content-design-plan.md` — what to decide once a change passes these gates
- `.agents/references/terminology.md` — canonical product terms
- `.agents/skills/missing_docs/references/changelog_decisions.md` — the recorded verdict ledger
