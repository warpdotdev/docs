*Proposed change: Configure third-party harnesses for factory agents*

*Summary:* Expand the Factory agents page with a concrete Claude Code and Codex setup workflow, link to reusable harness authentication details, and weave stable constraints into the steps that trigger them.

*Key design choices:*
- Make `src/content/docs/factories/factory-agents.mdx` the primary workflow rather than duplicating a full Factory procedure across the Claude Code and Codex pages.
- Cover both supported Factory authentication sources: a compatible team-owned Warp-managed secret, or credentials from a self-hosted worker environment.
- Keep caveats beside the affected step instead of adding a generic limitations section.

*Design alternatives:* Repeating a complete Factory workflow on each harness page would improve direct discoverability, but it would duplicate Factory UI instructions and increase drift. Keep one procedure on the Factory agents page and link to `src/content/docs/platform/harnesses/authentication.mdx`, `claude-code.mdx`, and `codex.mdx` for provider-specific credential and model details.

*Root cause / approach:* `src/content/docs/factories/factory-agents.mdx` names the available harnesses and plan requirement, but it does not tell a factory administrator how to select a harness, configure authentication, choose a compatible model, save the agent, or recognize an unavailable option. It also says harness and credential strategy are file-only even though Warp-managed factories expose editable **Harness**, **Auth**, **Model**, and **Host** controls. Add a focused procedure to that page and correct adjacent harness-reference claims where the codebase pass found drift.

Ground the instructions in these current behaviors:
- The Factory editor exposes **Harness**, **Auth**, **Model**, and **Host** per agent, and exposes the same selection group under factory agent defaults (`warpdotdev/warp-server/client/packages/factory/src/components/harness-config/HarnessConfigRows.tsx:115 @ 4a4d429d1982f34c340a467380e9ec8f9d0c1121`, `client/packages/factory/src/pages/FactorySettings/AgentDefaultsSettings.tsx:145 @ 4a4d429d1982f34c340a467380e9ec8f9d0c1121`).
- Factory-managed auth pickers list only compatible, team-owned typed secrets. Claude Code supports Anthropic API key, Anthropic Bedrock API key, and Anthropic Bedrock access key types; Codex supports OpenAI API keys (`client/packages/factory/src/components/harness-auth-secret/HarnessAuthPicker.tsx:98 @ 4a4d429d1982f34c340a467380e9ec8f9d0c1121`, `model/types/enums/managed_secret_type.go:50 @ 4a4d429d1982f34c340a467380e9ec8f9d0c1121`).
- **From worker environment** is offered only for a self-hosted host. Switching to Warp-hosted compute clears that selection (`client/packages/factory/src/components/harness-config/HarnessConfigRows.tsx:57 @ 4a4d429d1982f34c340a467380e9ec8f9d0c1121`).
- Changing harness clears the previous harness's model, reasoning level, and auth selection. The user must select compatible replacements (`client/packages/factory/src/components/harness-config/HarnessConfigRows.tsx:168 @ 4a4d429d1982f34c340a467380e9ec8f9d0c1121`).
- Third-party harnesses require the plan's third-party-harness entitlement. An admin-disabled or no-longer-entitled stored harness remains visible but unavailable so the user can switch back to Warp (`logic/agent_entitlements.go:97 @ 4a4d429d1982f34c340a467380e9ec8f9d0c1121`, `logic/harness_availability.go:121 @ 4a4d429d1982f34c340a467380e9ec8f9d0c1121`).
- File-managed factories display these settings read-only in the dashboard; their `agentDefaults` or per-agent frontmatter must use the nested `harness` form documented in `src/content/docs/factories/factory-as-code.mdx` (`client/packages/factory/src/access/factory-access-presentation.ts:6 @ 4a4d429d1982f34c340a467380e9ec8f9d0c1121`, `logic/factoryfile/schema/common.go:258 @ 4a4d429d1982f34c340a467380e9ec8f9d0c1121`).
- Model choices are harness-specific. Codex entries pair a model ID with a reasoning level, and the current server catalog has no `default` Codex option (`config/harness_models.go:51 @ 4a4d429d1982f34c340a467380e9ec8f9d0c1121`).

*Affected files:*
- `src/content/docs/factories/factory-agents.mdx` — primary setup procedure, paid-plan note, inline caveats, and correction of the file-only statement.
- `src/content/docs/platform/harnesses/authentication.mdx` — clarify that factory configurations use team-owned typed auth secrets, while personal secrets apply to other cloud-run flows.
- `src/content/docs/platform/harnesses/claude-code.mdx` and `src/content/docs/platform/harnesses/codex.mdx` — only the minimum provider/model corrections and cross-links needed to keep the Factory workflow accurate, including removing the unsupported Codex `default` model claim.

*Open questions resolved:*
- The Factory agents page owns the end-to-end workflow; individual harness pages remain provider-specific references.
- Document all supported authentication paths rather than only one happy path.
- Weave stable, user-actionable gotchas into the relevant steps; do not add a standalone limitations section or expose internal feature-flag details.
- Treat the public `03-multi-harness` factory example and the existing factory-as-code page as the maintained source for YAML examples instead of duplicating a second full configuration block.

*Risks / blast radius:* The main risk is documenting UI or model details that drift. Use current UI labels, avoid copying the full model catalogs, and link to the model picker and provider pages for the live list. Keep internal experiment and feature-flag behavior out of public prose. Limit changes to existing pages; do not add navigation or new pages.

*Validation & verification criteria* (must ALL pass before merge):
1. `src/content/docs/factories/factory-agents.mdx` gives a reader a complete, ordered path to configure one agent with Claude Code or Codex: open the agent, choose **Harness**, choose or create **Auth**, choose **Model** (including Codex reasoning level where shown), save, and recognize the configured result.
2. The Factory procedure states that third-party harnesses require a paid Build plan or higher and links “Warp pricing” to `https://warp.dev/pricing` (or the repository's canonical equivalent). It also explains inline that a harness disabled by plan or workspace policy cannot be selected and that switching back to Warp is the recovery path.
3. Authentication guidance distinguishes Factory behavior from ad hoc cloud runs: a Warp-hosted factory agent uses a compatible team-owned typed secret; Claude Code lists the three supported Anthropic credential types; Codex uses an OpenAI API key; raw secrets and personal auth secrets are not presented as valid Factory selections.
4. The worker-environment path appears only in self-hosted-host instructions, and the prose explains inline that changing to Warp-hosted compute requires selecting a managed auth secret.
5. The model step explains that model options belong to the selected harness and that changing harness requires reselecting the model and auth. The docs do not hardcode a complete model list, do not claim Codex offers a `default` option, and do not imply a Warp model ID can be reused across harnesses.
6. The dashboard/file-management distinction is accurate: Warp-managed factory agents can edit harness/auth/model in the dashboard; file-managed factories edit `agentDefaults.harness` or per-agent `harness` frontmatter and link to [factory definitions as code](/factories/factory-as-code/) and the `03-multi-harness` example.
7. Claude Code, Codex, authentication, Factory-as-code, pricing, and example-repository links resolve. Run `python3 .agents/skills/check_for_broken_links/check_links.py --internal-only` and confirm no new broken links or anchors are introduced.
8. The changed prose follows the feature-doc and procedural conventions: second-person imperative steps, exact bold UI labels, sentence-case headings, expected outcome, no standalone gotchas appendix, and no duplicated provider setup. Run `python3 .agents/skills/style_lint/style_lint.py --changed` with no new warnings attributable to the change.
9. This is a pure data/copy change, so a regression test is testing-exempt: a string-presence test would be tautological and brittle. Run the checks available in this environment: `python3 .agents/skills/check_for_broken_links/check_links.py`, `python3 .agents/skills/style_lint/style_lint.py --changed`, and `npm run build` from the docs root. `trunk` is not vendored in this sandbox per the repository's own README note, so `trunk fmt`/`trunk check` are not run locally; the repository's CI runs them on every PR.
10. This change edits prose within an existing numbered-list procedure and introduces no new component, layout, or interactive element, so a computer-use pass over the rendered page adds no verification beyond item 7's link check and item 9's build. Skip the computer-use capture for this change; the internal link check and `npm run build` confirm the rendered MDX compiles with no link, anchor, or structural regressions.
