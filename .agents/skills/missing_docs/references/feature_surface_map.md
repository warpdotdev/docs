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

AgentMode -> src/content/docs/agent-platform/local-agents/overview.mdx
AgentManagementView -> src/content/docs/platform/managing-cloud-agents.md
AgentManagementDetailsView -> src/content/docs/platform/managing-cloud-agents.md
AgentModeComputerUse -> src/content/docs/agent-platform/capabilities/computer-use.mdx
AgentModeWorkflows -> src/content/docs/knowledge-and-collaboration/warp-drive/workflows.md
AgentOnboarding -> src/content/docs/agent-platform/getting-started/agents-in-warp.md
AIRules -> src/content/docs/agent-platform/capabilities/rules.mdx
AIResumeButton -> src/content/docs/agent-platform/local-agents/interacting-with-agents/terminal-and-agent-modes.mdx
InlineCodeReview -> src/content/docs/agent-platform/local-agents/interactive-code-review.mdx
FileTree -> src/content/docs/code/code-editor/file-tree.md
CodeFindReplace -> src/content/docs/code/code-editor/find-and-replace.md
VimCodeEditor -> src/content/docs/code/code-editor/code-editor-vim-keybindings.md
McpServer -> src/content/docs/agent-platform/capabilities/mcp.mdx
McpOauth -> src/content/docs/agent-platform/capabilities/mcp.mdx
ImageAsContext -> src/content/docs/agent-platform/local-agents/agent-context/images-as-context.mdx
SelectionAsContext -> src/content/docs/agent-platform/local-agents/agent-context/selection-as-context.mdx
DiffSetAsContext -> src/content/docs/agent-platform/local-agents/agent-context/selection-as-context.mdx
WebSearchUI -> src/content/docs/agent-platform/capabilities/web-search.mdx
WebFetchUI -> src/content/docs/agent-platform/capabilities/web-search.mdx
CrossRepoContext -> src/content/docs/agent-platform/capabilities/codebase-context.mdx
FullSourceCodeEmbedding -> src/content/docs/agent-platform/capabilities/codebase-context.mdx
SearchCodebaseUI -> src/content/docs/agent-platform/capabilities/codebase-context.mdx
RemoteCodebaseIndexing -> src/content/docs/agent-platform/capabilities/codebase-context.mdx
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
APIKeyAuthentication -> src/content/docs/reference/cli/api-keys.md
APIKeyManagement -> src/content/docs/reference/cli/api-keys.md
CreatingSharedSessions -> src/content/docs/knowledge-and-collaboration/session-sharing/index.mdx
AgentSharedSessions -> src/content/docs/agent-platform/local-agents/session-sharing.mdx
ProfilesDesignRevamp -> src/content/docs/agent-platform/capabilities/agent-profiles-permissions.mdx
MultiProfile -> src/content/docs/agent-platform/capabilities/agent-profiles-permissions.mdx
InlineProfileSelector -> src/content/docs/agent-platform/capabilities/agent-profiles-permissions.mdx
ListSkills -> src/content/docs/agent-platform/capabilities/skills.mdx
BundledSkills -> src/content/docs/agent-platform/capabilities/skills.mdx
SyncAmbientPlans -> src/content/docs/agent-platform/capabilities/planning.mdx
SuggestedRules -> src/content/docs/agent-platform/capabilities/rules.mdx
RectSelection -> src/content/docs/terminal/more-features/text-selection.md
ContextWindowUsageV2 -> src/content/docs/agent-platform/local-agents/interacting-with-agents/index.mdx
CommandCorrectionKey -> src/content/docs/terminal/entry/command-corrections.md
ClassicCompletions -> src/content/docs/terminal/command-completions/completions.md
DynamicWorkflowEnums -> src/content/docs/knowledge-and-collaboration/warp-drive/workflows.md
SharedWithMe -> src/content/docs/knowledge-and-collaboration/warp-drive/index.mdx
WarpPacks -> src/content/docs/knowledge-and-collaboration/warp-drive/index.mdx
TabbedEditorView -> src/content/docs/code/code-editor/index.mdx
ReadImageFiles -> src/content/docs/agent-platform/local-agents/agent-context/images-as-context.mdx
FileRetrievalTools -> src/content/docs/agent-platform/capabilities/codebase-context.mdx
ConversationArtifacts -> src/content/docs/agent-platform/local-agents/interacting-with-agents/index.mdx
OzChangelogUpdates -> src/content/docs/changelog/index.mdx
ActiveConversationRequiresInteraction -> src/content/docs/agent-platform/local-agents/interacting-with-agents/index.mdx

# Recently shipped GA features
VerticalTabs -> src/content/docs/terminal/windows/vertical-tabs.mdx
VerticalTabsSummaryMode -> src/content/docs/terminal/windows/vertical-tabs.mdx
TabConfigs -> src/content/docs/terminal/windows/tab-configs.mdx
PluggableNotifications -> src/content/docs/terminal/more-features/notifications.md
RevertToCheckpoints -> src/content/docs/agent-platform/capabilities/slash-commands.mdx
RewindSlashCommand -> src/content/docs/agent-platform/capabilities/slash-commands.mdx
ForkFromCommand -> src/content/docs/agent-platform/capabilities/slash-commands.mdx
SummarizationConversationCommand -> src/content/docs/agent-platform/capabilities/slash-commands.mdx
CreateEnvironmentSlashCommand -> src/content/docs/agent-platform/capabilities/slash-commands.mdx
CodeReviewFind -> src/content/docs/code/code-review.md
CodeReviewSaveChanges -> src/content/docs/code/code-review.md
DiscardPerFileAndAllChanges -> src/content/docs/code/code-review.md
AutoOpenCodeReviewPane -> src/content/docs/code/code-review.md
GitOperationsInCodeReview -> src/content/docs/code/code-review.md
RemoteCodeReview -> src/content/docs/code/code-review.md
AgentView -> src/content/docs/agent-platform/local-agents/interacting-with-agents/terminal-and-agent-modes.mdx
AgentViewBlockContext -> src/content/docs/agent-platform/local-agents/agent-context/blocks-as-context.mdx
CloudConversations -> src/content/docs/agent-platform/local-agents/cloud-conversations.mdx
CloudModeFromLocalSession -> src/content/docs/platform/index.mdx
TeamApiKeys -> src/content/docs/reference/cli/api-keys.md
PRCommentsSlashCommand -> src/content/docs/agent-platform/capabilities/slash-commands.mdx
PRCommentsV2 -> src/content/docs/agent-platform/local-agents/interacting-with-agents/index.mdx
CLIAgentRichInput -> src/content/docs/agent-platform/cli-agents/rich-input.md
HOANotifications -> src/content/docs/agent-platform/capabilities/agent-notifications.mdx
OpenCodeNotifications -> src/content/docs/agent-platform/cli-agents/opencode.md
CodexNotifications -> src/content/docs/agent-platform/cli-agents/codex.md
# Codex Warp plugin marketplace integration; documented alongside Codex notifications.
CodexPlugin -> src/content/docs/agent-platform/cli-agents/codex.md
HOARemoteControl -> src/content/docs/agent-platform/cli-agents/remote-control.md
GlobalSearch -> src/content/docs/code/overview.md
FileBasedMcp -> src/content/docs/agent-platform/capabilities/mcp.mdx
ConversationsAsContext -> src/content/docs/agent-platform/local-agents/agent-context/blocks-as-context.mdx
GithubPrPromptChip -> src/content/docs/agent-platform/capabilities/agent-notifications.mdx
AskUserQuestion -> src/content/docs/agent-platform/local-agents/interacting-with-agents/index.mdx
AIContextMenuEnabled -> src/content/docs/agent-platform/local-agents/agent-context/using-to-add-context.mdx
AtMenuOutsideOfAIMode -> src/content/docs/agent-platform/local-agents/agent-context/using-to-add-context.mdx
AIContextMenuCode -> src/content/docs/agent-platform/local-agents/agent-context/using-to-add-context.mdx
DriveObjectsAsContext -> src/content/docs/agent-platform/local-agents/agent-context/using-to-add-context.mdx
KittyKeyboardProtocol -> src/content/docs/terminal/more-features/full-screen-apps.mdx
InlineRepoMenu -> src/content/docs/agent-platform/capabilities/codebase-context.mdx
InlineHistoryMenu -> src/content/docs/agent-platform/local-agents/interacting-with-agents/terminal-and-agent-modes.mdx
SkillArguments -> src/content/docs/agent-platform/capabilities/skills.mdx
ConfigurableToolbar -> src/content/docs/terminal/windows/configurable-toolbar.mdx
SettingsFile -> src/content/docs/terminal/settings/index.mdx
Changelog -> src/content/docs/changelog/index.mdx
Autoupdate -> src/content/docs/support-and-community/troubleshooting-and-support/updating-warp.mdx
ShellSelector -> src/content/docs/getting-started/supported-shells.mdx
WorkflowAliases -> src/content/docs/terminal/entry/yaml-workflows.mdx
KittyImages -> src/content/docs/terminal/more-features/full-screen-apps.mdx
UndoClosedPanes -> src/content/docs/terminal/windows/tabs.mdx
RevertDiffHunk -> src/content/docs/code/code-review.mdx
SshRemoteServer -> src/content/docs/terminal/warpify/ssh.mdx

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
AmbientAgentsImageUpload -> src/content/docs/agent-platform/local-agents/agent-context/images-as-context.mdx
CloudModeImageContext -> src/content/docs/agent-platform/local-agents/agent-context/images-as-context.mdx

# Skills on the Oz platform
OzPlatformSkills -> src/content/docs/agent-platform/capabilities/skills.mdx

# Handoff (local <-> cloud, cloud <-> cloud) and snapshots
OzHandoff -> src/content/docs/platform/handoff/index.mdx
HandoffLocalCloud -> src/content/docs/platform/handoff/local-to-cloud.mdx
HandoffCloudCloud -> src/content/docs/platform/handoff/cloud-to-cloud.mdx

# Orchestration / multi-agent runs
RunAgentsTool -> src/content/docs/platform/orchestration/multi-agent-runs.mdx

# Prompt queueing
QueueSlashCommand -> src/content/docs/agent-platform/local-agents/interacting-with-agents/prompt-queueing.mdx
QueuedPromptsV2 -> src/content/docs/agent-platform/local-agents/interacting-with-agents/prompt-queueing.mdx

# Reusable agents (named agents + agent-scoped API keys)
NamedAgents -> src/content/docs/platform/agents.mdx

# Inference: BYOK and custom endpoints
SoloUserByok -> src/content/docs/agent-platform/inference/bring-your-own-api-key.mdx
CustomInferenceEndpoints -> src/content/docs/agent-platform/inference/custom-inference-endpoint.mdx
# Connect a SuperGrok subscription instead of pasting an xAI API key.
SuperGrok -> src/content/docs/agent-platform/inference/bring-your-own-api-key.mdx
# Custom model routers (Settings > AI > Custom Routers) surface in the model picker.
CustomModelRouters -> src/content/docs/agent-platform/inference/model-choice.mdx

# Billing & Usage settings page (redesigned)
BillingAndUsagePageV2 -> src/content/docs/support-and-community/plans-and-billing/index.mdx

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
oz provider -> src/content/docs/reference/cli/index.mdx
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
DELETE /memory_stores/{uid}/memories/{memoryUid} -> gated:AIMemories
PUT /memory_stores/{uid}/memories/{memoryUid} -> gated:AIMemories
GET /memory_stores/{uid}/memories/{memoryUid}/versions -> gated:AIMemories

## Slash commands -> doc pages

# Most documented commands are matched automatically against the
# slash-commands page content; add entries here only for exceptions.
# Gated by the dogfood-only LocalDockerSandbox flag — not user-facing yet.
/docker-sandbox -> internal

## Settings -> doc pages

# Settings are matched automatically against the all-settings reference
# (terminal/settings/all-settings.mdx) by section + key; add entries here only
# for exceptions: settings documented on another page (`section.key -> path`)
# or intentionally undocumented (`section.key -> internal`).

# One-time internal state for the deprecated tmux SSH wrapper migration banner;
# not a user-configurable setting.
warpify.ssh.ssh_tmux_deprecation_notice_pending -> internal

## Unlisted docs pages to ignore

# Pages intentionally absent from src/sidebar.ts (one slug per line, e.g.
# `guides/some-page`). Everything else on disk must be reachable via the sidebar.
# Per the page's frontmatter comment: not in the Guides sidebar yet, pending
# team feedback.
guides/agent-workflows/warp-vs-claude-code

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
GetStartedTab
CreateProjectFlow
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
OpenWarpNewSettingsModes
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
# Internal SSE streaming infrastructure for orchestration viewers/owners.
OrchestrationViewerStreamer
OwnerOrchestrationAncestorStreamer

# Sub-feature toggles and pre-launch flags. Section placement does NOT assert
# rollout status (the audit computes that from code); entries here are ignored
# because the toggle itself isn't a documentable surface, or because the
# feature isn't user-facing yet — the snapshot diff flags promotions.
# Grouped Tabs is a macOS-only Preview feature (organize tabs into named,
# collapsible groups); public docs are pending GA promotion, which the snapshot
# diff will flag.
GroupedTabs
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
DragTabsToWindows
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
