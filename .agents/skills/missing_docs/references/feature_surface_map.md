# Feature Surface Map

Curated mapping of feature flags, CLI commands, API endpoints, slash commands,
and settings to their expected documentation pages, plus an allowlist for
intentionally unlisted docs pages.
The audit script reads this file to reduce false positives — entries here are
verified rather than flagged.

Format: `CodeIdentifier -> src/content/docs/path/to/page.md` (one per line within each section).
Lines starting with `#` are comments. Blank lines are ignored.
The sentinel target `internal` marks surfaces that intentionally have no public docs.
The sentinel target `gated:<Flag>` (CLI commands and API routes) ties a surface to
its gating FeatureFlag's rollout: it is deferred while the flag is non-GA and
auto-surfaces for docs once the flag goes GA.

# Maintenance policy:
# - When a feature ships (GA or Preview), add a mapping here in the same PR that
#   adds/updates its doc page.
# - When a flag/command/route is removed from code, the audit's map-hygiene check
#   flags the dead entry — verify the doc page is still accurate, then prune it.
# - Run `python3 .agents/skills/missing_docs/scripts/audit_docs.py` to find unmapped
#   surfaces, and `--update-snapshot` to refresh references/surface_snapshot.json.
# - This audit also runs as a recurring scheduled cloud agent to catch drift
#   (see the drift-watch workflow in SKILL.md).

## Feature flags -> doc pages

# The local-agents overview page was folded into the agents landing page
# (/agents/local-agents/overview now 308s to /agents/ in vercel.json).
AgentMode -> src/content/docs/agents/index.mdx
AgentManagementView -> src/content/docs/platform/managing-cloud-agents.md
AgentManagementDetailsView -> src/content/docs/platform/managing-cloud-agents.md
AgentModeComputerUse -> src/content/docs/agents/capabilities/computer-use/index.mdx
AgentModeWorkflows -> src/content/docs/knowledge-and-collaboration/warp-drive/workflows.md
# agents-in-warp was folded into the agents landing page as well
# (/agents/getting-started/agents-in-warp now 308s to /agents/).
AgentOnboarding -> src/content/docs/agents/index.mdx
AIRules -> src/content/docs/agents/capabilities/rules.mdx
AIResumeButton -> src/content/docs/agents/local-agents/interacting-with-agents/terminal-and-agent-modes.mdx
InlineCodeReview -> src/content/docs/agents/local-agents/interactive-code-review.mdx
FileTree -> src/content/docs/code/code-editor/file-tree.md
CodeFindReplace -> src/content/docs/code/code-editor/find-and-replace.md
VimCodeEditor -> src/content/docs/code/code-editor/code-editor-vim-keybindings.md
McpServer -> src/content/docs/agents/capabilities/mcp.mdx
McpOauth -> src/content/docs/agents/capabilities/mcp.mdx
ImageAsContext -> src/content/docs/agents/local-agents/agent-context/images-as-context.mdx
SelectionAsContext -> src/content/docs/agents/local-agents/agent-context/selection-as-context.mdx
DiffSetAsContext -> src/content/docs/agents/local-agents/agent-context/selection-as-context.mdx
WebSearchUI -> src/content/docs/agents/capabilities/web-search.mdx
WebFetchUI -> src/content/docs/agents/capabilities/web-search.mdx
CrossRepoContext -> src/content/docs/agents/capabilities/codebase-context.mdx
FullSourceCodeEmbedding -> src/content/docs/agents/capabilities/codebase-context.mdx
SearchCodebaseUI -> src/content/docs/agents/capabilities/codebase-context.mdx
RemoteCodebaseIndexing -> src/content/docs/agents/capabilities/codebase-context.mdx
CloudEnvironments -> src/content/docs/platform/environments.md
CloudMode -> src/content/docs/platform/index.mdx
AmbientAgentsCommandLine -> src/content/docs/platform/index.mdx
ScheduledAmbientAgents -> src/content/docs/platform/triggers/scheduled-agents.md
WarpManagedSecrets -> src/content/docs/platform/secrets.md
IntegrationCommand -> src/content/docs/reference/cli/integration-setup.md
CommandPaletteFileSearch -> src/content/docs/terminal/command-palette.md
Ligatures -> src/content/docs/terminal/appearance/text-fonts-cursor.md
UIZoom -> src/content/docs/terminal/appearance/size-opacity-blurring.md
UsageBasedPricing -> src/content/docs/support-and-community/plans-and-billing/credits.md
# The APIKeyAuthentication flag was removed after the public API key auth feature
# stabilized (GA / flag cleanup). API key auth remains documented at
# reference/cli/api-keys.mdx via APIKeyManagement / TeamApiKeys, so no separate
# entry is needed.
APIKeyManagement -> src/content/docs/reference/cli/api-keys.md
CreatingSharedSessions -> src/content/docs/knowledge-and-collaboration/session-sharing/index.mdx
AgentSharedSessions -> src/content/docs/agents/local-agents/session-sharing.mdx
ProfilesDesignRevamp -> src/content/docs/agents/capabilities/agent-profiles-permissions.mdx
MultiProfile -> src/content/docs/agents/capabilities/agent-profiles-permissions.mdx
InlineProfileSelector -> src/content/docs/agents/capabilities/agent-profiles-permissions.mdx
ListSkills -> src/content/docs/agents/capabilities/skills.mdx
BundledSkills -> src/content/docs/agents/capabilities/skills.mdx
SyncAmbientPlans -> src/content/docs/agents/capabilities/planning.mdx
SuggestedRules -> src/content/docs/agents/capabilities/rules.mdx
RectSelection -> src/content/docs/terminal/more-features/text-selection.md
ContextWindowUsageV2 -> src/content/docs/agents/local-agents/interacting-with-agents/index.mdx
CommandCorrectionKey -> src/content/docs/terminal/entry/command-corrections.md
ClassicCompletions -> src/content/docs/terminal/command-completions/completions.md
DynamicWorkflowEnums -> src/content/docs/knowledge-and-collaboration/warp-drive/workflows.md
SharedWithMe -> src/content/docs/knowledge-and-collaboration/warp-drive/index.mdx
WarpPacks -> src/content/docs/knowledge-and-collaboration/warp-drive/index.mdx
TabbedEditorView -> src/content/docs/code/code-editor/index.mdx
ReadImageFiles -> src/content/docs/agents/local-agents/agent-context/images-as-context.mdx
FileRetrievalTools -> src/content/docs/agents/capabilities/codebase-context.mdx
ConversationArtifacts -> src/content/docs/agents/local-agents/interacting-with-agents/index.mdx
OzChangelogUpdates -> src/content/docs/changelog/index.mdx
ActiveConversationRequiresInteraction -> src/content/docs/agents/local-agents/interacting-with-agents/index.mdx

# Recently shipped GA features
VerticalTabs -> src/content/docs/terminal/windows/vertical-tabs.mdx
VerticalTabsSummaryMode -> src/content/docs/terminal/windows/vertical-tabs.mdx
TabConfigs -> src/content/docs/terminal/windows/tab-configs.mdx
PluggableNotifications -> src/content/docs/terminal/more-features/notifications.md
RevertToCheckpoints -> src/content/docs/agents/capabilities/slash-commands.mdx
RewindSlashCommand -> src/content/docs/agents/capabilities/slash-commands.mdx
ForkFromCommand -> src/content/docs/agents/capabilities/slash-commands.mdx
SummarizationConversationCommand -> src/content/docs/agents/capabilities/slash-commands.mdx
CreateEnvironmentSlashCommand -> src/content/docs/agents/capabilities/slash-commands.mdx
CodeReviewFind -> src/content/docs/code/code-review.md
CodeReviewSaveChanges -> src/content/docs/code/code-review.md
DiscardPerFileAndAllChanges -> src/content/docs/code/code-review.md
AutoOpenCodeReviewPane -> src/content/docs/code/code-review.md
GitOperationsInCodeReview -> src/content/docs/code/code-review.md
RemoteCodeReview -> src/content/docs/code/code-review.md
AgentView -> src/content/docs/agents/local-agents/interacting-with-agents/terminal-and-agent-modes.mdx
AgentViewBlockContext -> src/content/docs/agents/local-agents/agent-context/blocks-as-context.mdx
CloudConversations -> src/content/docs/agents/local-agents/cloud-conversations.mdx
CloudModeFromLocalSession -> src/content/docs/platform/index.mdx
TeamApiKeys -> src/content/docs/reference/cli/api-keys.md
# The PRCommentsSlashCommand flag was removed: the /pr-comments slash command was
# replaced by the bundled PR Comments skill (invoked via /skills), so the slash
# command was dropped from the docs.
PRCommentsV2 -> src/content/docs/agents/local-agents/interacting-with-agents/index.mdx
CLIAgentRichInput -> src/content/docs/agents/cli-agents/rich-input.mdx
HOANotifications -> src/content/docs/agents/capabilities/agent-notifications.mdx
OpenCodeNotifications -> src/content/docs/agents/cli-agents/opencode.mdx
CodexNotifications -> src/content/docs/agents/cli-agents/codex.mdx
# Codex Warp plugin marketplace integration; documented alongside Codex notifications.
CodexPlugin -> src/content/docs/agents/cli-agents/codex.mdx
HOARemoteControl -> src/content/docs/agents/cli-agents/remote-control.mdx
GlobalSearch -> src/content/docs/code/overview.md
FileBasedMcp -> src/content/docs/agents/capabilities/mcp.mdx
ConversationsAsContext -> src/content/docs/agents/local-agents/agent-context/blocks-as-context.mdx
GithubPrPromptChip -> src/content/docs/agents/capabilities/agent-notifications.mdx
AskUserQuestion -> src/content/docs/agents/local-agents/interacting-with-agents/index.mdx
AIContextMenuEnabled -> src/content/docs/agents/local-agents/agent-context/using-to-add-context.mdx
AtMenuOutsideOfAIMode -> src/content/docs/agents/local-agents/agent-context/using-to-add-context.mdx
AIContextMenuCode -> src/content/docs/agents/local-agents/agent-context/using-to-add-context.mdx
DriveObjectsAsContext -> src/content/docs/agents/local-agents/agent-context/using-to-add-context.mdx
KittyKeyboardProtocol -> src/content/docs/terminal/more-features/full-screen-apps.mdx
InlineRepoMenu -> src/content/docs/agents/capabilities/codebase-context.mdx
InlineHistoryMenu -> src/content/docs/agents/local-agents/interacting-with-agents/terminal-and-agent-modes.mdx
SkillArguments -> src/content/docs/agents/capabilities/skills.mdx
ConfigurableToolbar -> src/content/docs/terminal/windows/configurable-toolbar.mdx
SettingsFile -> src/content/docs/terminal/settings/index.mdx
Changelog -> src/content/docs/changelog/index.mdx
Autoupdate -> src/content/docs/support-and-community/troubleshooting-and-support/updating-warp.mdx
ShellSelector -> src/content/docs/getting-started/supported-shells.mdx
WorkflowAliases -> src/content/docs/terminal/entry/yaml-workflows.mdx
KittyImages -> src/content/docs/terminal/more-features/full-screen-apps.mdx
UndoClosedPanes -> src/content/docs/terminal/windows/tabs.mdx
# Tab groups (organize tabs into named, collapsible groups) — GA (in the default
# feature set).
GroupedTabs -> src/content/docs/terminal/windows/tabs.mdx
# Pin individual tabs and whole tab groups to the front of the tab bar — GA.
PinnedTabs -> src/content/docs/terminal/windows/tabs.mdx
# Drag a tab out to its own window or between windows. GA on macOS and Windows
# (RELEASE_FLAGS, cfg-gated), documented with that platform caveat.
DragTabsToWindows -> src/content/docs/terminal/windows/tabs.mdx
RevertDiffHunk -> src/content/docs/code/code-review.mdx
SshRemoteServer -> src/content/docs/terminal/warpify/ssh.mdx

# Computer use: session recording (VideoRecording gates the start/stop recording
# tools) and window-targeted background capture (BackgroundComputerUse). Both are
# GA and documented on the computer use capability pages (the page was split from
# a flat computer-use.mdx into a computer-use/ directory).
VideoRecording -> src/content/docs/agents/capabilities/computer-use/testing-and-recordings.mdx
BackgroundComputerUse -> src/content/docs/agents/capabilities/computer-use/index.mdx

# Feature flags whose only user-facing surface is a documented setting in the
# all-settings reference (terminal/settings/all-settings.mdx).
# - FullScreenZenMode: the "zen mode" tab-bar visibility knob appearance.tabs.workspace_decoration_visibility
# - AsyncFind: experimental.async_find_enabled
FullScreenZenMode -> src/content/docs/terminal/settings/all-settings.mdx
AsyncFind -> src/content/docs/terminal/settings/all-settings.mdx

# Session sharing (viewing + ACLs are part of the documented session sharing feature)
ViewingSharedSessions -> src/content/docs/knowledge-and-collaboration/session-sharing/index.mdx
SessionSharingAcls -> src/content/docs/knowledge-and-collaboration/session-sharing/index.mdx
SharedSessionWriteToLongRunningCommands -> src/content/docs/knowledge-and-collaboration/session-sharing/index.mdx

# CLI-gated features documented in the CLI reference
ArtifactCommand -> src/content/docs/reference/cli/artifacts.mdx
OzIdentityFederation -> src/content/docs/reference/cli/federate.mdx

# Third-party harness support
AgentHarness -> src/content/docs/platform/harnesses/index.mdx

# Image context for cloud agents
AmbientAgentsImageUpload -> src/content/docs/agents/local-agents/agent-context/images-as-context.mdx
CloudModeImageContext -> src/content/docs/agents/local-agents/agent-context/images-as-context.mdx

# Skills on the Oz platform
OzPlatformSkills -> src/content/docs/agents/capabilities/skills.mdx

# Handoff (local <-> cloud, cloud <-> cloud) and snapshots
OzHandoff -> src/content/docs/platform/handoff/index.mdx
HandoffLocalCloud -> src/content/docs/platform/handoff/local-to-cloud.mdx
HandoffCloudCloud -> src/content/docs/platform/handoff/cloud-to-cloud.mdx

# Orchestration / multi-agent runs is documented at
# platform/orchestration/multi-agent-runs.mdx. The RunAgentsTool flag was removed
# after the feature stabilized (GA), so it no longer needs a map entry.

# Prompt queueing
QueueSlashCommand -> src/content/docs/agents/local-agents/interacting-with-agents/prompt-queueing.mdx
QueuedPromptsV2 -> src/content/docs/agents/local-agents/interacting-with-agents/prompt-queueing.mdx

# Reusable agents (named agents + agent-scoped API keys)
NamedAgents -> src/content/docs/platform/agents.mdx

# Inference: BYOK and custom endpoints
SoloUserByok -> src/content/docs/agents/inference/bring-your-own-api-key.mdx
# CustomInferenceEndpoints flag was removed after the feature stabilized (GA);
# the feature remains documented at inference/custom-inference-endpoint.mdx.
# Connect a SuperGrok subscription instead of pasting an xAI API key.
SuperGrok -> src/content/docs/agents/inference/bring-your-own-api-key.mdx
# Custom model routers (Settings > AI > Custom Routers) surface in the model picker.
CustomModelRouters -> src/content/docs/agents/inference/model-choice.mdx

# Billing & Usage settings page (redesigned)
BillingAndUsagePageV2 -> src/content/docs/support-and-community/plans-and-billing/index.mdx

# Cloud agent runners (reusable compute configs). CloudRunners gates the
# `--runner` flag on `run-cloud`; CloudAgentRunners gates the `oz runner` CRUD
# commands and the runner dropdown in the orchestration card. Both are GA
# (default cargo features).
CloudRunners -> src/content/docs/platform/runners.mdx
CloudAgentRunners -> src/content/docs/platform/runners.mdx

# Per-segment context window usage breakdown (system prompt, tool definitions,
# conversation history, latest input, images, other) in the conversation usage
# summary. Promoted dogfood -> GA; documented alongside the context window usage
# indicator it drills into (paired with ContextWindowUsageV2 above).
ContextWindowUsageBreakdown -> src/content/docs/agents/local-agents/interacting-with-agents/index.mdx

# BYOLLM routing through Gemini Enterprise Agent Platform (Vertex AI). Promoted
# dogfood -> GA; documented on the enterprise BYOLLM page for that host.
GeminiEnterprise -> src/content/docs/enterprise/enterprise-features/byollm-gemini-enterprise.mdx

# OSC 8 terminal hyperlinks (clickable link text emitted by CLI tools). Promoted
# preview -> GA; documented with the rest of Warp's link handling.
OscHyperlinks -> src/content/docs/terminal/more-features/files-and-links.mdx

# Well-known managed MCP ids: accepts short integration ids (linear, slack,
# jira) wherever a Warp MCP server UUID is accepted — bare `--mcp` arguments and
# `warp_id` values in MCP configs. Promoted dogfood -> GA; documented in the CLI
# MCP reference (and the cloud agent MCP schema page).
WellKnownMcpIds -> src/content/docs/reference/cli/mcp-servers.mdx

# Auto-attaches the Warp-hosted Factory MCP server to agent sessions with no
# manual setup. Promoted dogfood -> GA; that zero-config behavior is documented
# in the "Connect and authenticate" section of the Factory MCP page.
FactoryMcp -> src/content/docs/factories/factory-mcp.mdx

## CLI commands -> doc pages

# Top-level Oz CLI commands
oz agent -> src/content/docs/reference/cli/index.mdx
oz environment -> src/content/docs/reference/cli/integration-setup.mdx
oz mcp -> src/content/docs/reference/cli/mcp-servers.mdx
oz run -> src/content/docs/reference/cli/index.mdx
oz model -> src/content/docs/reference/cli/index.mdx
oz login -> src/content/docs/reference/cli/index.mdx
oz logout -> src/content/docs/reference/cli/index.mdx
oz whoami -> src/content/docs/reference/cli/index.mdx
oz integration -> src/content/docs/reference/cli/integration-setup.mdx
oz schedule -> src/content/docs/reference/cli/index.mdx
oz secret -> src/content/docs/reference/cli/index.mdx
oz federate -> src/content/docs/reference/cli/federate.mdx
oz artifact -> src/content/docs/reference/cli/artifacts.mdx
oz api-key -> src/content/docs/reference/cli/api-keys.mdx

# Scheduled-agent CLI subcommands are fully documented in the scheduled-agents feature page.
oz schedule create -> src/content/docs/platform/triggers/scheduled-agents.mdx
oz schedule list -> src/content/docs/platform/triggers/scheduled-agents.mdx
oz schedule get -> src/content/docs/platform/triggers/scheduled-agents.mdx
oz schedule update -> src/content/docs/platform/triggers/scheduled-agents.mdx
oz schedule pause -> src/content/docs/platform/triggers/scheduled-agents.mdx
oz schedule unpause -> src/content/docs/platform/triggers/scheduled-agents.mdx
oz schedule delete -> src/content/docs/platform/triggers/scheduled-agents.mdx

# Warp-managed secret CLI subcommands are documented in the secrets feature page.
oz secret create -> src/content/docs/platform/secrets.mdx
oz secret list -> src/content/docs/platform/secrets.mdx
oz secret update -> src/content/docs/platform/secrets.mdx
oz secret delete -> src/content/docs/platform/secrets.mdx

# Agent Memory is research preview (gating flag AIMemories is non-GA), so its CLI
# is deferred via `gated:` — it auto-surfaces for docs when AIMemories goes GA.
# See "Public vs. private surfaces" in SKILL.md.
oz memory -> gated:AIMemories
oz memory create -> gated:AIMemories
oz memory delete -> gated:AIMemories
oz memory list -> gated:AIMemories
oz memory update -> gated:AIMemories
oz memory versions -> gated:AIMemories
oz memory-store -> gated:AIMemories
oz memory-store get -> gated:AIMemories
oz memory-store list -> gated:AIMemories
oz memory-store list-store-agents -> gated:AIMemories
oz memory-store update -> gated:AIMemories

# `oz provider` (link third-party services like Slack and Linear) is gated by
# ProviderCommand, which is non-GA (dogfood), so the whole command group is
# deferred via `gated:` — it auto-surfaces for docs when ProviderCommand goes
# GA. See "Public vs. private surfaces" in SKILL.md.
oz provider -> gated:ProviderCommand
oz provider setup -> gated:ProviderCommand
oz provider list -> gated:ProviderCommand

# `oz runner` (manage cloud agent runners) is GA (gated by CloudAgentRunners, a
# default cargo feature) and documented on the runners page. The old gating flag
# CloudAgentRunnerCLICommands was removed after the feature stabilized.
oz runner -> src/content/docs/platform/runners.mdx
oz runner list -> src/content/docs/platform/runners.mdx
oz runner create -> src/content/docs/platform/runners.mdx
oz runner update -> src/content/docs/platform/runners.mdx
oz runner delete -> src/content/docs/platform/runners.mdx

# Internal/hidden command — not a user-facing surface, so no public docs.
oz harness-support -> internal

## API endpoints -> doc pages

# Paths are relative to /api/v1 and use OpenAPI-style {param} segments.
# Public API endpoints documented via the OpenAPI spec (developers/agent-api-openapi.yaml).
#
# POLICY: warp-server is a private repo. Only endpoints that are part of the
# released public Oz Agent API (already in the OpenAPI spec) may be documented.
# Endpoints not in the spec are NOT auto-documentable: confirm release status and
# route released ones through the sync-openapi-spec skill, or mark `-> internal`
# (unreleased/internal). Never document an unreleased endpoint. See SKILL.md
# "Public vs. private surfaces".
POST /agent/run -> src/content/docs/reference/api-and-sdk/index.mdx
GET /agent/runs -> src/content/docs/reference/api-and-sdk/index.mdx
GET /agent/runs/{runId} -> src/content/docs/reference/api-and-sdk/index.mdx

# OAuth device-flow / OIDC plumbing used by `oz login` — not a public REST surface.
GET /oauth/authorize -> internal
POST /oauth/device/auth -> internal
POST /oauth/session -> internal
POST /oauth/token -> internal
GET /oauth/jwks.json -> internal
GET /.well-known/openid-configuration -> internal

# RFC 8414 / RFC 9728 OAuth discovery documents that MCP clients fetch
# automatically before authenticating against the hosted Factory MCP endpoint
# (router/handlers/public_api/oauth2.go, registered by registerMCPDiscoveryRoutes
# only when the dogfood-only factory_mcp flag is on). They are machine-facing
# protocol metadata for an unreleased product, absent from warp-server's
# canonical public spec, so they are not a documentable public API surface. The
# path-suffixed variants implement RFC 8414 section 5 path-aware discovery for
# the /api/v1/mcp/factory resource.
GET /.well-known/oauth-authorization-server -> internal
GET /.well-known/oauth-authorization-server/api/v1/mcp/factory -> internal
GET /.well-known/openid-configuration/api/v1/mcp/factory -> internal
GET /.well-known/oauth-protected-resource/api/v1/mcp/factory -> internal

# OAuth consent screen, connected-apps (grant) management, token revocation, and
# RFC 7591 dynamic client registration backing the MCP harness OAuth flows
# (router/handlers/public_api/oauth2.go; registration is additionally
# flag-gated). Like the device-flow endpoints above, these are protocol and web
# plumbing rather than a released public REST surface, and they are absent from
# warp-server's canonical public spec.
GET /oauth/consent/info -> internal
POST /oauth/consent -> internal
GET /oauth/grants -> internal
DELETE /oauth/grants/{client_id} -> internal
POST /oauth/register -> internal
POST /oauth/revoke -> internal

# Anonymous-viewer redirect probes (documented exceptions to auth, not API surfaces).
GET /agent/sessions/{session_uuid}/redirect -> internal
GET /agent/conversations/{conversation_id}/redirect -> internal

# Legacy aliases of /agent/runs kept for compatibility.
GET /agent/tasks -> internal
GET /agent/tasks/{id} -> internal
POST /agent/tasks/{id}/cancel -> internal

# Handoff/worker attachment plumbing (driven by clients and workers, not end users).
POST /agent/runs/{runId}/attachments/prepare -> internal
POST /agent/runs/{runId}/attachments/download -> internal
GET /agent/runs/{runId}/handoff/attachments -> internal
POST /agent/handoff/upload-snapshot -> internal
PATCH /agent/runs/{runId}/event-sequence -> internal
POST /agent/runs/{runId}/client-events -> internal
# Records the repositories and revisions a run checked out, written by the run's
# own cloud agent before setup commands run. Marked `x-internal: true` upstream
# and guarded by RequireCloudAgent, so it is never callable by an API consumer.
POST /agent/runs/{runId}/environment-snapshot -> internal
GET /agent/conversations/{conversation_id}/block-snapshot -> internal

# Support endpoints for third-party harnesses (hidden `oz harness-support` CLI).
POST /harness-support/external-conversation -> internal
POST /harness-support/block-snapshot -> internal
POST /harness-support/transcript -> internal
GET /harness-support/transcript -> internal
POST /harness-support/resolve-prompt -> internal
POST /harness-support/report-artifact -> internal
POST /harness-support/notify-user -> internal
POST /harness-support/finish-task -> internal
POST /harness-support/report-shutdown -> internal
POST /harness-support/upload-snapshot -> internal
POST /harness-support/commit-snapshot -> internal

# Oz Factory REST API (router/handlers/public_api/factory*.go). Warp Factories
# is now documented publicly (src/content/docs/factories/) as an Early Access
# product, but its REST API is a different question: these routes are defined in
# warp-server's canonical spec but marked `x-internal: true`, so the publish
# filter strips them from the public docs copy and they are not part of the
# released public Oz Agent API. They must not be hand-documented and stay
# internal; revisit and route through the sync-openapi-spec skill if/when those
# `x-internal` markers come off. See SKILL.md "Public vs. private surfaces".
GET /factory -> internal
GET /factory/access -> internal
GET /factory-alias/{alias} -> internal
POST /factory -> internal
POST /factory/avatar -> internal
GET /factory/{uid} -> internal
PATCH /factory/{uid} -> internal
DELETE /factory/{uid} -> internal
POST /factory/{uid}/apply -> internal
POST /factory/{uid}/plan -> internal
# Opens/refreshes the throwaway branch and PR that verify a factory's GitHub
# connection during onboarding.
POST /factory/{uid}/github-onboarding-pr -> internal
GET /factory/{uid}/source -> internal
PUT /factory/{uid}/source -> internal
DELETE /factory/{uid}/source -> internal
# Factory-as-code source browsing, editing, export, and merge plumbing backing
# the factory definition editor in the Oz web app.
GET /factory/{uid}/source/tree -> internal
GET /factory/{uid}/source/file -> internal
PUT /factory/{uid}/source/files -> internal
GET /factory/{uid}/source/export -> internal
POST /factory/{uid}/source/clone-url -> internal
GET /factory/{uid}/source/link-readiness -> internal
# Integrating production drift into, and discarding, a warp/code/* working
# branch behind the factory definition editor.
POST /factory/{uid}/source/branch/sync -> internal
DELETE /factory/{uid}/source/branch -> internal
POST /factory/{uid}/merges -> internal
POST /factory/{uid}/merges/check -> internal
GET /factory/{uid}/merges/{merge_uid} -> internal
# Factory file JSON schemas and validation, consumed by the factory definition
# editor and the factory-files authoring tooling.
GET /factory-files/schemas -> internal
GET /factory-files/schemas/{schema_version} -> internal
GET /factory-files/schemas/{schema_version}/{document} -> internal
POST /factory-files/validate -> internal
# Factory review (AI review of a factory definition) and its refine loop.
GET /factory/{uid}/review -> internal
POST /factory/{uid}/review/refine -> internal
# Factory outbound webhooks: CRUD, delivery history, and secret rotation.
GET /factory/webhooks -> internal
POST /factory/webhooks -> internal
POST /factory/webhooks/dry-run -> internal
GET /factory/webhooks/{uid} -> internal
PUT /factory/webhooks/{uid} -> internal
DELETE /factory/webhooks/{uid} -> internal
GET /factory/webhooks/{uid}/deliveries -> internal
GET /factory/webhooks/{uid}/deliveries/{delivery_id} -> internal
POST /factory/webhooks/{uid}/rotate -> internal
GET /factory/{uid}/syncs -> internal
GET /factory/{uid}/task-by-conversation -> internal
GET /factory/{uid}/tasks -> internal
POST /factory/{uid}/tasks -> internal
GET /factory/{uid}/tasks/{task_uid} -> internal
PATCH /factory/{uid}/tasks/{task_uid} -> internal
DELETE /factory/{uid}/tasks/{task_uid} -> internal
POST /factory/{uid}/tasks/{task_uid}/cancel -> internal
GET /factory/{uid}/task-by-run -> internal
# Dispatching a run to a factory. Unlike its neighbours this operation is NOT
# marked `x-internal: true` upstream, so warp-server's own publish filter would
# keep it. It stays out of the docs copy because the whole `/factory` namespace
# is excluded by the sync-openapi-spec policy (`factory` in EXCLUDED_TAGS plus
# the `/factory` prefix) while the Factory REST API is unreleased. Revisit
# together with that exclusion when the Factory API ships publicly.
POST /factory/{uid}/runs -> internal
# Also marked `x-internal: true` in warp-server's canonical spec, so the publish
# filter strips it from the public docs copy.
GET /factory/{uid}/metrics -> internal
GET /factory/{uid}/metrics/cost-by-pr-size -> internal
GET /factory/{uid}/metrics/run-breakdown -> internal
GET /factory/{uid}/metrics/top-prs -> internal
GET /factory/{uid}/integrations/linear/teams -> internal
GET /factory/{uid}/integrations/linear/teams/{team_id}/labels -> internal
PUT /factory/{uid}/integrations/linear/teams/{team_id}/labels -> internal
GET /factory/{uid}/integrations/jira/projects -> internal
GET /factory/{uid}/integrations/jira/labels -> internal
GET /factory/{uid}/integrations/jira/statuses -> internal
GET /factory/{uid}/integration-activations -> internal
GET /factory/{uid}/integration-destinations -> internal
GET /factory/{uid}/gitlab-automation-capability -> internal
POST /factory/{uid}/gitlab-automation-capability/refresh -> internal
# Integration pickers used during factory setup, before a factory exists.
GET /factory-setup/integrations/jira/projects -> internal
GET /factory-setup/integrations/linear/teams -> internal
GET /factory/automations -> internal
POST /factory/automations -> internal
GET /factory/automations/events/{provider} -> internal
GET /factory/automations/{id} -> internal
PUT /factory/automations/{id} -> internal
DELETE /factory/automations/{id} -> internal
PUT /factory/automations/{id}/subscriptions -> internal
DELETE /factory/automations/{id}/subscriptions/{subscription_id} -> internal
# Fires an automation's cron trigger immediately; `x-internal: true` upstream.
POST /factory/automations/{id}/run -> internal
GET /factory/scorers -> internal
POST /factory/scorers -> internal
PATCH /factory/scorers/{scorer_id} -> internal
DELETE /factory/scorers/{scorer_id} -> internal
GET /factory/scorers/{scorer_id}/results -> internal
GET /factory/scorers/{scorer_id}/results/reasons -> internal
GET /factory/scorers/{scorer_id}/metrics/pass-rate -> internal
# The scorer pause/resume routes and the autofix-config trio were replaced by
# the self-improvement-config routes below; their dead map entries were pruned.
GET /factory/scorers/{scorer_id}/self-improvement-config -> internal
PUT /factory/scorers/{scorer_id}/self-improvement-config -> internal
DELETE /factory/scorers/{scorer_id}/self-improvement-config -> internal
GET /factory/runs/{run_id}/scores -> internal
POST /factory/run-scoring/dispatches -> internal
PUT /factory/automations/{id}/subscriptions/{subscription_id} -> internal
GET /factory/{uid}/integrations/github/branches -> internal
GET /factory/{uid}/integrations/github/labels -> internal
GET /factory/{uid}/integrations/github/teams -> internal
GET /factory/{uid}/integrations/github/users -> internal
GET /factory/{uid}/integrations/github/workflows -> internal
GET /factory/{uid}/integrations/linear/issues -> internal
GET /factory/{uid}/integrations/linear/projects -> internal
GET /factory/{uid}/integrations/linear/users -> internal
GET /factory/{uid}/integrations/linear/workflow-states -> internal
GET /factory/{uid}/integrations/slack/conversations -> internal
GET /factory/{uid}/integrations/slack/users -> internal
# Issue-tracker issue picker and Slack connection-test greeting used by the
# factory integrations UI. Same unreleased `/factory` namespace as siblings above.
GET /factory/{uid}/integrations/issue-tracker/issues -> internal
POST /factory/{uid}/integrations/slack/connection-test-greeting -> internal
# Factory benchmark suites and benchmark runs
# (router/handlers/public_api/benchmarks.go). Same unreleased Factory product as
# the routes above, and absent from warp-server's canonical public spec.
GET /factory/{uid}/benchmarks/suites -> internal
POST /factory/{uid}/benchmarks/suites -> internal
GET /factory/{uid}/benchmarks/suites/{suite_uid} -> internal
PATCH /factory/{uid}/benchmarks/suites/{suite_uid} -> internal
DELETE /factory/{uid}/benchmarks/suites/{suite_uid} -> internal
POST /factory/{uid}/benchmarks/suites/{suite_uid}/runs -> internal
POST /factory/{uid}/benchmarks/suites/{suite_uid}/tasks -> internal
# Moved out from under /suites/{suite_uid} in warp-server: composing a benchmark
# task from a production run no longer requires a target suite up front.
POST /factory/{uid}/benchmarks/tasks/compose-from-run -> internal
GET /factory/{uid}/benchmarks/runs -> internal
GET /factory/{uid}/benchmarks/runs/{run_uid} -> internal
GET /factory/{uid}/benchmarks/runs/{run_uid}/results -> internal
POST /factory/{uid}/benchmarks/runs/{run_uid}/cancel -> internal

# Orchestration messaging and lifecycle-event endpoints. These are marked
# `x-internal: true` in warp-server's canonical spec (public_api/openapi.yaml),
# so the publish filter deliberately strips them from the public docs copy.
# They back the agent-to-agent messaging tools and the documented
# `oz run message` CLI, but the REST surface itself is not part of the released
# public Oz Agent API. Revisit if warp-server drops the x-internal marker.
POST /agent/messages -> internal
GET /agent/messages/{run_id} -> internal
POST /agent/messages/{id}/read -> internal
POST /agent/messages/{id}/delivered -> internal
GET /agent/events -> internal
POST /agent/events/{run_id} -> internal

# SSE lifecycle-event stream consumed by the Warp client and the Oz web app.
# Absent from warp-server's canonical public spec entirely, and registered only
# on the RTC host, so it is not a released public API operation.
GET /agent/events/stream -> internal

# Agent Memory REST API — research preview (gating flag AIMemories is non-GA),
# deferred via `gated:` and auto-surfaces when AIMemories goes GA. See
# "Public vs. private surfaces" in SKILL.md.
GET /memory_stores -> gated:AIMemories
POST /memory_stores -> gated:AIMemories
GET /memory_stores/{uid} -> gated:AIMemories
PUT /memory_stores/{uid} -> gated:AIMemories
DELETE /memory_stores/{uid} -> gated:AIMemories
GET /memory_stores/{uid}/agents -> gated:AIMemories
GET /memory_stores/{uid}/memories -> gated:AIMemories
POST /memory_stores/{uid}/memories -> gated:AIMemories
GET /memory_stores/{uid}/memories/{memoryUid} -> gated:AIMemories
DELETE /memory_stores/{uid}/memories/{memoryUid} -> gated:AIMemories
PUT /memory_stores/{uid}/memories/{memoryUid} -> gated:AIMemories
GET /memory_stores/{uid}/memories/{memoryUid}/versions -> gated:AIMemories

## Slash commands -> doc pages

# Most documented commands are matched automatically against the
# slash-commands page content; add entries here only for exceptions.
# Gated by the dogfood-only LocalDockerSandbox flag — not user-facing yet.
/docker-sandbox -> internal
# Warp Agent CLI-only (crates/warp_tui) slash commands — added only when the
# settings mode is the Warp Agent CLI (see static_commands/commands.rs). They
# aren't present in the GUI desktop app, so they aren't documented on the public
# slash-commands page. Consistent with the general.autoupdate_enabled Warp Agent
# CLI-only setting mapped to `internal` above.
/exit -> internal
/view-logs -> internal
/auto-approve -> internal
/logout -> internal
# The paired /enable- and /disable-natural-language-detection commands were
# replaced by a single toggle, /natural-language-detection. Like the other Warp
# Agent CLI-only commands above, it isn't in the GUI, so it stays internal.
/natural-language-detection -> internal
# TUI-only voice input command (Warp Agent CLI surface). The /version command was
# removed from code; its entry has been pruned.
/voice -> internal
# TUI-only team switcher (SlashCommandSurfaces::TuiOnly in static_commands/
# commands.rs). The GUI switches teams from the title-bar pill instead, so this
# isn't documented on the public slash-commands page.
/team -> internal
# More Warp Agent CLI-only (SlashCommandSurfaces::TuiOnly in static_commands/
# commands.rs) commands. None are present in the GUI desktop app, so they aren't
# documented on the public slash-commands page:
# - /status: show session and account status
# - /clear: clear the transcript and start a new conversation
# - /statusline: configure the Warp Agent CLI statusline (agents.statusline, internal)
# - /reset-statusline: restore the statusline to its default items and ordering
# - /api-keys: view and manage model-provider API keys. It replaced the removed
#   /add-api-key and /clear-provider-api-key pair, whose entries were pruned.
# - /vim-mode: toggle Vim keybindings in the Warp Agent CLI input
/status -> internal
/clear -> internal
/statusline -> internal
/reset-statusline -> internal
/api-keys -> internal
/vim-mode -> internal
# TUI-only color-theme picker (Warp Agent CLI surface, SlashCommandSurfaces::TuiOnly
# in static_commands/commands.rs). It sets the Warp Agent CLI theme
# (appearance.theme, mapped internal below) and isn't present in the GUI, so it
# stays internal like the other Warp Agent CLI-only commands.
/theme -> internal

## Settings -> doc pages

# Settings are matched automatically against the all-settings reference
# (terminal/settings/all-settings.mdx) by section + key; add entries here only
# for exceptions: settings documented on another page (`section.key -> path`)
# or intentionally undocumented (`section.key -> internal`).

# One-time internal state for the deprecated tmux SSH wrapper migration banner;
# not a user-configurable setting.
warpify.ssh.ssh_tmux_deprecation_notice_pending -> internal

# Warp Agent CLI-only (crates/warp_tui) background auto-updater toggle (surface:
# Warp Agent CLI). It isn't present in the GUI settings UI, so it isn't
# documented in the all-settings reference.
general.autoupdate_enabled -> internal

# Warp Agent CLI-only (crates/warp_tui) statusline configuration (surface:
# SettingSurfaces::TUI in app/src/settings/ai.rs; controls the order and
# visibility of the Warp Agent CLI bottom statusline items). It isn't present in
# the GUI settings UI, so it isn't documented in the all-settings reference.
# Paired with the /statusline Warp Agent CLI slash command mapped internal above.
agents.statusline -> internal

# Warp Agent CLI-only (crates/warp_tui) color theme (surface: Warp Agent CLI,
# SettingSurfaces::TUI in tui_theme.rs; "auto|light|dark" matching the host
# terminal background). It isn't present in the GUI settings UI, so it isn't
# documented in the all-settings reference. The GUI theme setting is the separate
# appearance.themes.theme, which is documented. Paired with the /theme Warp Agent
# CLI slash command mapped internal above.
appearance.theme -> internal

# Warp Agent CLI-only (crates/warp_tui) zero-state animation knobs (surface: Warp
# Agent CLI, SettingSurfaces::TUI). They tune the rotating object shown in the
# empty Warp Agent CLI state and aren't present in the GUI settings UI, so they
# aren't documented in the all-settings reference.
appearance.zero_state.object -> internal
appearance.zero_state.rotation_period_seconds -> internal
appearance.zero_state.extrusion_depth -> internal

# Warp Agent CLI-only (crates/warp_tui) per-section visibility toggles for the
# zero state (surface: SettingSurfaces::TUI in app/src/settings/tui_zero_state.rs).
# Each hides one section of the Warp Agent CLI empty state. They aren't present in
# the GUI settings UI, so they aren't documented in the all-settings reference.
appearance.zero_state.show_signed_in_user -> internal
appearance.zero_state.show_changelog -> internal
appearance.zero_state.show_project_info -> internal
appearance.zero_state.show_mcp -> internal
appearance.zero_state.show_animation -> internal

# Warp Agent CLI-only toggle that stops the zero-state animation from repainting
# while the terminal is unfocused (app/src/settings/tui_zero_state.rs). Like the
# other zero-state knobs it isn't in the GUI settings UI, so it's documented on
# the Warp Agent CLI configuration page instead of the all-settings reference.
appearance.zero_state.freeze_animation_when_unfocused -> src/content/docs/agents/cli/configuration.mdx

# Warp Agent CLI-only (crates/warp_tui) push-to-talk key for voice input (surface:
# SettingSurfaces::TUI in app/src/settings/tui_voice.rs). The GUI equivalent is the
# separate agents.voice.voice_input_toggle_key, which is documented.
agents.voice.voice_input_hold_key -> internal

## Unlisted docs pages to ignore

# Pages intentionally absent from src/sidebar.ts (one slug per line, e.g.
# `guides/some-page`). Everything else on disk must be reachable via the sidebar.
# Per the page's frontmatter comment: not in the Guides sidebar yet, pending
# team feedback.
guides/agent-workflows/warp-vs-claude-code
# Custom Starlight 404 page (template: splash). Starlight renders it through its
# own prerendered /404 route, so it is intentionally not in the sidebar.
404
# The Jira integration page left draft status and is now listed in src/sidebar.ts,
# so its allowlist entry was pruned.

## Flags to ignore (internal-only, not user-facing)

# These flags are internal implementation details and don't need documentation
CocoaSentry
CrashReporting
DebugMode
LogExpensiveFramesInSentry
WithSandboxTelemetry
RecordAppActiveEvents
RuntimeFeatureFlags
FetchChannelVersionsFromWarpServer
SequentialStorage
InBandGeneratorsForSSH
RunGeneratorsWithCmdExe
RecordPtyThroughput
FetchGenericStringObjects
IntegratedGPU
LazySceneBuilding
MaximizeFlatStorage
SharedBlockTitleGeneration
RetryTruncatedCodeResponses
ReloadStaleConversationFiles
SendTelemetryToFile
FileGlobV2Warnings
ExpandEditToPane
MCPGroupedServerContext
AgentDecidesCommandExecution
AgentModePrimaryXML
AgentModePrePlanXML
AgentModeAnalytics
GlobalAIAnalyticsBanner
GlobalAIAnalyticsCollection
FastForwardAutoexecuteButton
LinkedCodeBlocks
V4AFileDiffs
SummarizationViaMessageReplacement
SummarizationCancellationConfirmation
TabCloseButtonOnLeft
RemoveAutosuggestionDuringTabCompletions
ResizeFix
ForceClassicCompletions
DefaultWaterfallMode
DefaultAdeberryTheme
AutoupdateUIRevamp
MinimalistUI
AvatarInTabBar
ImeMarkedText
NewTabStyling
AmbientAgentsRTC
OzLaunchModal
# One-time launch modal announcing Warp going open-source.
# The announcement itself is covered in the 2026 changelog ("Warp is now open source.")
# and the modal has no recurring user-facing surface that warrants its own doc page.
OpenWarpLaunchModal
# One-time launch modal announcing multi-agent orchestration; the feature itself
# is documented via RunAgentsTool -> orchestration/multi-agent-runs.mdx.
OrchestrationLaunchModal
# One-time launch modal announcing the Warp Agent CLI. Its "Get started" button
# links to the CLI quickstart, and the CLI itself is documented under
# agents/cli/, so the modal has no separate documentable surface.
AgentCliLaunchModal
GetStartedTab
CreateProjectFlow
# Account-first onboarding is an internal login/onboarding flow variant with no
# distinct user-facing surface to document (like HOAOnboardingFlow below).
AccountFirstOnboarding
CodeLaunchModal
ValidateAutosuggestions
ClearAutosuggestionOnEscape
# Rendering details for markdown tables/Mermaid in notebooks/AI output; no dedicated doc surface.
MarkdownTables
MarkdownMermaid

# UI implementation details (not user-facing features)
FallbackModelLoadOutputMessaging
IncrementalAutoReload
CodeReviewScrollPreservation
WarpifyFooter
TransferControlTool
TrimTrailingBlankLines
InlineMenuHeaders
BlocklistMarkdownImages
BlocklistMarkdownTableRendering
PendingUserQueryIndicator
RememberFastForwardState
HoaCodeReview
AgentToolbarEditor
SkipFirebaseAnonymousUser
HOAOnboardingFlow
AgentViewConversationListView
BuildPlanAutoReloadBannerToggle
BuildPlanAutoReloadPostPurchaseModal
ForceLogin
SimulateGithubUnauthed
ConversationApi
McpDebuggingIds
ContextLineReviewComments
RichTextMultiselect
# Redux iterations of the cloud mode setup/input UI; the cloud agents feature
# itself is documented via CloudMode -> platform/index.mdx.
CloudModeSetupV2
CloudModeInputV2
# Internal GitHub credential refresh during task runs (changelog-only behavior fix).
GitCredentialRefresh
# State-mutating recovery for abnormal terminal lifecycle sequences — an internal
# reliability mechanism with no user-facing configuration or UI, so it needs no docs.
TerminalLifecycleRecovery
# When Ctrl-C is forwarded to a third-party harness PTY, synthesize Cancelled for
# the CLI agent session if the plugin never reports the interrupt. No setting,
# menu, or CLI flag; Ctrl-C behavior is already documented.
CtrlCCancelsThirdPartyHarness
# Orchestration plumbing promoted dogfood -> GA. Neither changes what a user sees
# or configures, so both are internal implementation details of the documented
# multi-agent orchestration feature (platform/orchestration/multi-agent-runs.mdx):
# - WaitForEventsParentRegistration: on `wait_for_events`, confirms parent status
#   with the server and registers an orchestrator for the ancestor event stream so
#   children created out-of-band (CLI/API) still deliver events.
# - OrchestrationUnifiedStack: consolidates child-state tracking behind a single
#   tracker, one ancestor SSE per parent family, and one remote-child placeholder.
WaitForEventsParentRegistration
OrchestrationUnifiedStack
# Internal persistence-backend detail: gates storing execution profiles in a
# file-backed settings collection (agents.execution_profiles) versus the legacy
# per-profile Warp Drive cloud objects. It changes where profiles are stored, not
# any user-facing behavior — execution profiles are documented via
# ProfilesDesignRevamp/MultiProfile -> agent-profiles-permissions.mdx — so it needs no docs.
FileBackedExecutionProfiles

# Sub-feature toggles and pre-launch flags. Section placement does NOT assert
# rollout status (the audit computes that from code); entries here are ignored
# because the toggle itself isn't a documentable surface, or because the
# feature isn't user-facing yet — the snapshot diff flags promotions.
LSPAsATool
EmbeddedCodeReviewComments
InteractiveConversationManagementView
MarkdownImages
EditableMarkdownMermaid
# Directory-based tab colors: the user-facing knob is the setting
# appearance.tabs.directory_tab_colors, documented in the all-settings reference.
DirectoryTabColors
CloudModeHostSelector
CodebaseIndexSpeedbump
CodebaseIndexPersistence
AgentTips
AgentViewPromptChip
AllowOpeningFileLinksUsingEditorEnv
AllowIgnoringInputSuggestions
CodeModeChip
# Internal agent file-search tool plumbing (read tools are not individually documented).
GrepTool
NativeShellCompletions
SshDragAndDrop
ITermImages
AIGeneratedOnboardingSuggestions
PartialNextCommandSuggestions
CycleNextCommandSuggestion
AIBlockOverflowMenu
PromptSuggestionsViaMAA
SelectablePrompt
PredictAMQueries
UseTantivySearch
CommandCorrectionsHistoryRule
SuggestedAgentModeWorkflows
# Implementation toggle choosing skill-based vs slash-command PR comments;
# the user-facing /pr-comments command is mapped via PRCommentsSlashCommand.
PRCommentsSkill
FigmaDetection
# OSC 8 hyperlink support was promoted preview -> GA and is now documented at
# terminal/more-features/files-and-links.mdx, so its ignore entry was pruned in
# favor of the mapping in "Feature flags -> doc pages" above.
