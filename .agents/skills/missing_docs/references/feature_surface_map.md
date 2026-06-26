# Feature Surface Map

Curated mapping of feature flags, CLI commands, and code modules to their expected documentation pages.
The audit script reads this file to reduce false positives — entries here are verified rather than flagged.

Format: `CodeIdentifier -> docs/path/to/page.md` (one per line within each section).
Lines starting with `#` are comments. Blank lines are ignored.

# Maintenance: when a new GA feature flag ships, add a mapping here.
# Run `python3 .agents/skills/missing_docs/scripts/audit_docs.py` to find unmapped flags.
# This audit is also run as a recurring scheduled cloud agent to catch drift.

## Feature flags -> doc pages

AgentMode -> src/content/docs/agent-platform/local-agents/overview.mdx
AgentManagementView -> src/content/docs/platform/managing-cloud-agents.md
AgentManagementDetailsView -> src/content/docs/platform/managing-cloud-agents.md
AgentModeComputerUse -> src/content/docs/agent-platform/capabilities/computer-use.mdx
AgentModeWorkflows -> src/content/docs/knowledge-and-collaboration/warp-drive/workflows.md
AgentOnboarding -> src/content/docs/agent-platform/getting-started/agents-in-warp.md
AIRules -> src/content/docs/agent-platform/capabilities/rules.mdx
AIResumeButton -> src/content/docs/agent-platform/local-agents/interacting-with-agents/terminal-and-agent-modes.mdx
CodeReviewView -> src/content/docs/code/code-review.md
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
CodebaseContext -> src/content/docs/agent-platform/capabilities/codebase-context.mdx
CrossRepoContext -> src/content/docs/agent-platform/capabilities/codebase-context.mdx
FullSourceCodeEmbedding -> src/content/docs/agent-platform/capabilities/codebase-context.mdx
SearchCodebaseUI -> src/content/docs/agent-platform/capabilities/codebase-context.mdx
CloudEnvironments -> src/content/docs/platform/environments.md
CloudMode -> src/content/docs/platform.md
AmbientAgentsCommandLine -> src/content/docs/platform.md
ScheduledAmbientAgents -> src/content/docs/platform/triggers/scheduled-agents.md
WarpManagedSecrets -> src/content/docs/platform/secrets.md
IntegrationCommand -> src/content/docs/reference/cli/integration-setup.md
ConversationManagement -> src/content/docs/agent-platform/local-agents/cloud-conversations.mdx
ForkConversationFromBlock -> src/content/docs/agent-platform/local-agents/interacting-with-agents/conversation-forking.mdx
Voice -> src/content/docs/agent-platform/local-agents/interacting-with-agents/voice.mdx
WarpDrive -> src/content/docs/knowledge-and-collaboration/warp-drive/index.mdx
EnvVars -> src/content/docs/knowledge-and-collaboration/warp-drive/environment-variables.md
CommandPaletteFileSearch -> src/content/docs/terminal/command-palette.md
Themes -> src/content/docs/terminal/appearance/themes.md
Ligatures -> src/content/docs/terminal/appearance/text-fonts-cursor.md
UIZoom -> src/content/docs/terminal/appearance/size-opacity-blurring.md
SSH -> src/content/docs/terminal/warpify/ssh.md
SplitPanes -> src/content/docs/terminal/windows/split-panes.md
Tabs -> src/content/docs/terminal/windows/tabs.md
GlobalHotkey -> src/content/docs/terminal/windows/global-hotkey.md
LaunchConfigurations -> src/content/docs/terminal/sessions/launch-configurations.md
SessionRestoration -> src/content/docs/terminal/sessions/session-restoration.md
BlockBasics -> src/content/docs/terminal/blocks/block-basics.md
Autosuggestions -> src/content/docs/terminal/command-completions/autosuggestions.md
Completions -> src/content/docs/terminal/command-completions/completions.md
CommandHistory -> src/content/docs/terminal/entry/command-history.md
CommandCorrections -> src/content/docs/terminal/entry/command-corrections.md
UsageBasedPricing -> src/content/docs/support-and-community/plans-and-billing/credits.md
APIKeyAuthentication -> src/content/docs/reference/cli/api-keys.md
APIKeyManagement -> src/content/docs/reference/cli/api-keys.md
SecretRedaction -> src/content/docs/support-and-community/privacy-and-security/secret-redaction.md
CreatingSharedSessions -> src/content/docs/knowledge-and-collaboration/session-sharing/index.mdx
AgentSharedSessions -> src/content/docs/agent-platform/local-agents/session-sharing.mdx
ProfilesDesignRevamp -> src/content/docs/agent-platform/capabilities/agent-profiles-permissions.mdx
MultiProfile -> src/content/docs/agent-platform/capabilities/agent-profiles-permissions.mdx
InlineProfileSelector -> src/content/docs/agent-platform/capabilities/agent-profiles-permissions.mdx
ModelChoice -> src/content/docs/agent-platform/capabilities/model-choice.mdx
Skills -> src/content/docs/agent-platform/capabilities/skills.mdx
ListSkills -> src/content/docs/agent-platform/capabilities/skills.mdx
BundledSkills -> src/content/docs/agent-platform/capabilities/skills.mdx
Planning -> src/content/docs/agent-platform/capabilities/planning.mdx
SyncAmbientPlans -> src/content/docs/agent-platform/capabilities/planning.mdx
TaskLists -> src/content/docs/agent-platform/capabilities/task-lists.mdx
SlashCommands -> src/content/docs/agent-platform/capabilities/slash-commands.mdx
SuggestedRules -> src/content/docs/agent-platform/capabilities/rules.mdx
RectSelection -> src/content/docs/terminal/more-features/text-selection.md
ContextWindowUsageV2 -> src/content/docs/agent-platform/local-agents/interacting-with-agents/index.mdx
ConfigurableBlockLimits -> src/content/docs/terminal/blocks/block-basics.md
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
CodeReviewFind -> src/content/docs/code/code-review.md
CodeReviewSaveChanges -> src/content/docs/code/code-review.md
DiscardPerFileAndAllChanges -> src/content/docs/code/code-review.md
AutoOpenCodeReviewPane -> src/content/docs/code/code-review.md
GitOperationsInCodeReview -> src/content/docs/code/code-review.md
AgentView -> src/content/docs/agent-platform/local-agents/interacting-with-agents/terminal-and-agent-modes.mdx
AgentViewBlockContext -> src/content/docs/agent-platform/local-agents/agent-context/blocks-as-context.mdx
CloudConversations -> src/content/docs/agent-platform/local-agents/cloud-conversations.mdx
CloudModeFromLocalSession -> src/content/docs/platform.md
TeamApiKeys -> src/content/docs/reference/cli/api-keys.md
PRCommentsSlashCommand -> src/content/docs/agent-platform/capabilities/slash-commands.mdx
PRCommentsV2 -> src/content/docs/agent-platform/local-agents/interacting-with-agents/index.mdx
CLIAgentRichInput -> src/content/docs/agent-platform/cli-agents/rich-input.md
HOANotifications -> src/content/docs/agent-platform/capabilities/agent-notifications.mdx
OpenCodeNotifications -> src/content/docs/agent-platform/cli-agents/opencode.md
CodexNotifications -> src/content/docs/agent-platform/cli-agents/codex.md
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
# Internal/hidden command — not a user-facing surface, so no public docs.
oz harness-support -> internal

## API endpoints -> doc pages

# Public API endpoints
POST /agent/run -> src/content/docs/reference/api-and-sdk/index.mdx
GET /agent/runs -> src/content/docs/reference/api-and-sdk/index.mdx
GET /agent/runs/{runId} -> src/content/docs/reference/api-and-sdk/index.mdx

# Internal/infrastructure endpoints (not part of public API, no docs needed)
GET /block/embed/:id -> internal
GET /block/:id -> internal
GET /referral/:id -> internal
GET /client_version -> internal
GET /client_version/daily -> internal
POST /receive_nps_response -> internal
POST /receive_pmf_response -> internal
GET /current_time -> internal
POST /graphql/v2 -> internal
GET /graphql/v2 -> internal
GET /graphiql -> internal
GET /graphiql/v2 -> internal
GET /download -> internal
GET /download/brew -> internal
GET /download/windows -> internal
GET /download/cli -> internal

## Flags to ignore (internal-only, not user-facing)

# These flags are internal implementation details and don't need documentation
CocoaSentry
CrashReporting
CrashRecoveryForceX11
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
RemoveAltScreenPadding
MaximizeFlatStorage
SharedBlockTitleGeneration
RetryTruncatedCodeResponses
ReloadStaleConversationFiles
NLDClassifierModelEnabled
ChangedLinesOnlyApplyDiffResult
SendTelemetryToFile
SendEvalMetadata
FileGlobV2Warnings
ExpandEditToPane
MCPGroupedServerContext
MultiAgentParallelToolCalls
AgentDecidesCommandExecution
AgentModePrimaryXML
AgentModePrePlanXML
AgentModeAnalytics
GlobalAIAnalyticsBanner
GlobalAIAnalyticsCollection
FastForwardAutoexecuteButton
LinkedCodeBlocks
V4AFileDiffs
NewWarpingAnimation
NewDiffModel
SummarizationViaMessageReplacement
SummarizationCancellationConfirmation
TabCloseButtonOnLeft
LessHorizontalTerminalPadding
RemoveAutosuggestionDuringTabCompletions
ResizeFix
ForceClassicCompletions
DefaultWaterfallMode
DefaultAdeberryTheme
AutoupdateUIRevamp
MinimalistUI
AvatarInTabBar
SessionSharingAcls
ImeMarkedText
ConvertLegacyMcps
NewTabStyling
AmbientAgentsRTC
OzBranding
OzLaunchModal
# One-time launch modal announcing Warp going open-source.
# The announcement itself is covered in the 2026 changelog ("Warp is now open source.")
# and the modal has no recurring user-facing surface that warrants its own doc page.
OpenWarpLaunchModal
GetStartedTab
CreateProjectFlow
CodeLaunchModal
ValidateAutosuggestions
ClearAutosuggestionOnEscape
OzPlatformSkills

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
UpgradeToProModal
UpgradeToProModalPromo
FreeUserNoAi
SoloUserByok
ForceLogin
SimulateGithubUnauthed
ConversationApi
McpDebuggingIds
ContextLineReviewComments
RichTextMultiselect
ActiveConversationRequiresInteraction

# Non-GA flags in dogfood/preview only
Orchestration
OrchestrationV2
OrchestrationEventPush
LSPAsATool
SshRemoteServer
EmbeddedCodeReviewComments
AgentManagementDetailsView
InteractiveConversationManagementView
MarkdownImages
MarkdownMermaid
EditableMarkdownMermaid
OzIdentityFederation
AgentHarness
DirectoryTabColors
ArtifactCommand
AgentViewBlockContext
CloudModeImageContext
CloudModeHostSelector
AmbientAgentsImageUpload
NldImprovements
CodebaseIndexSpeedbump
CodebaseIndexPersistence
SharedSessionWriteToLongRunningCommands
AgentTips
AgentViewPromptChip
AllowOpeningFileLinksUsingEditorEnv
AllowIgnoringInputSuggestions
CodeModeChip
UndoClosedPanes
RevertDiffHunk
ViewingSharedSessions
SettingsImport
BlockToolbeltSaveAsWorkflow
ShellSelector
FullScreenZenMode
WorkflowAliases
KittyImages
GrepTool
NativeShellCompletions
WelcomeTab
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
ConversationArtifacts
ConversationApi
PRCommentsSkill
FigmaDetection
