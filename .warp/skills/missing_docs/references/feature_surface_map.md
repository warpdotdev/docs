# Feature Surface Map

Curated mapping of feature flags, CLI commands, and code modules to their expected documentation pages.
The audit script reads this file to reduce false positives — entries here are verified rather than flagged.

Format: `CodeIdentifier -> docs/path/to/page.md` (one per line within each section).
Lines starting with `#` are comments. Blank lines are ignored.

# Maintenance: when a new GA feature flag ships, add a mapping here.
# Run `python3 .warp/skills/missing_docs/scripts/audit_docs.py` to find unmapped flags.
# This audit is also run as a recurring scheduled Oz agent to catch drift.

## Feature flags -> doc pages

AgentMode -> docs/agent-platform/warp-agents/README.md
AgentManagementView -> docs/agent-platform/cloud-agents/managing-cloud-agents.md
AgentManagementDetailsView -> docs/agent-platform/cloud-agents/managing-cloud-agents.md
AgentModeComputerUse -> docs/agent-platform/warp-agents/computer-use.md
AgentModeWorkflows -> docs/warp/knowledge-and-collaboration/warp-drive/workflows.md
AgentOnboarding -> docs/agent-platform/getting-started/agents-in-warp.md
AIRules -> docs/agent-platform/warp-agents/rules.md
AIResumeButton -> docs/agent-platform/warp-agents/interacting-with-agents/terminal-and-agent-modes.md
CodeReviewView -> docs/warp/code/code-review.md
InlineCodeReview -> docs/agent-platform/warp-agents/interactive-code-review.md
FileTree -> docs/warp/code/code-editor/file-tree.md
CodeFindReplace -> docs/warp/code/code-editor/find-and-replace.md
VimCodeEditor -> docs/warp/code/code-editor/code-editor-vim-keybindings.md
McpServer -> docs/agent-platform/warp-agents/mcp.md
McpOauth -> docs/agent-platform/warp-agents/mcp.md
ImageAsContext -> docs/agent-platform/warp-agents/agent-context/images-as-context.md
SelectionAsContext -> docs/agent-platform/warp-agents/agent-context/selection-as-context.md
DiffSetAsContext -> docs/agent-platform/warp-agents/agent-context/selection-as-context.md
WebSearchUI -> docs/agent-platform/warp-agents/web-search.md
WebFetchUI -> docs/agent-platform/warp-agents/web-search.md
CodebaseContext -> docs/agent-platform/warp-agents/codebase-context.md
CrossRepoContext -> docs/agent-platform/warp-agents/codebase-context.md
FullSourceCodeEmbedding -> docs/agent-platform/warp-agents/codebase-context.md
SearchCodebaseUI -> docs/agent-platform/warp-agents/codebase-context.md
CloudEnvironments -> docs/agent-platform/cloud-agents/environments.md
CloudMode -> docs/agent-platform/cloud-agents/overview.md
AmbientAgentsCommandLine -> docs/agent-platform/cloud-agents/overview.md
ScheduledAmbientAgents -> docs/agent-platform/cloud-agents/triggers/scheduled-agents.md
WarpManagedSecrets -> docs/agent-platform/cloud-agents/secrets.md
IntegrationCommand -> docs/reference/cli/integration-setup.md
ConversationManagement -> docs/agent-platform/warp-agents/cloud-conversations.md
ForkConversationFromBlock -> docs/agent-platform/warp-agents/interacting-with-agents/conversation-forking.md
Voice -> docs/agent-platform/warp-agents/interacting-with-agents/voice.md
WarpDrive -> docs/warp/knowledge-and-collaboration/warp-drive/README.md
EnvVars -> docs/warp/knowledge-and-collaboration/warp-drive/environment-variables.md
CommandPaletteFileSearch -> docs/warp/terminal/command-palette.md
Themes -> docs/warp/terminal/appearance/themes.md
Ligatures -> docs/warp/terminal/appearance/text-fonts-cursor.md
UIZoom -> docs/warp/terminal/appearance/size-opacity-blurring.md
SSH -> docs/warp/terminal/warpify/ssh.md
SplitPanes -> docs/warp/terminal/windows/split-panes.md
Tabs -> docs/warp/terminal/windows/tabs.md
GlobalHotkey -> docs/warp/terminal/windows/global-hotkey.md
LaunchConfigurations -> docs/warp/terminal/sessions/launch-configurations.md
SessionRestoration -> docs/warp/terminal/sessions/session-restoration.md
BlockBasics -> docs/warp/terminal/blocks/block-basics.md
Autosuggestions -> docs/warp/terminal/command-completions/autosuggestions.md
Completions -> docs/warp/terminal/command-completions/completions.md
CommandHistory -> docs/warp/terminal/entry/command-history.md
CommandCorrections -> docs/warp/terminal/entry/command-corrections.md
UsageBasedPricing -> docs/support-and-community/plans-and-billing/credits.md
APIKeyAuthentication -> docs/reference/cli/api-keys.md
APIKeyManagement -> docs/reference/cli/api-keys.md
SecretRedaction -> docs/support-and-community/privacy-and-security/secret-redaction.md
CreatingSharedSessions -> docs/warp/knowledge-and-collaboration/session-sharing/README.md
AgentSharedSessions -> docs/agent-platform/warp-agents/session-sharing.md
ProfilesDesignRevamp -> docs/agent-platform/warp-agents/agent-profiles-permissions.md
MultiProfile -> docs/agent-platform/warp-agents/agent-profiles-permissions.md
InlineProfileSelector -> docs/agent-platform/warp-agents/agent-profiles-permissions.md
ModelChoice -> docs/agent-platform/warp-agents/model-choice.md
Skills -> docs/agent-platform/warp-agents/skills.md
ListSkills -> docs/agent-platform/warp-agents/skills.md
BundledSkills -> docs/agent-platform/warp-agents/skills.md
Planning -> docs/agent-platform/warp-agents/planning.md
SyncAmbientPlans -> docs/agent-platform/warp-agents/planning.md
TaskLists -> docs/agent-platform/warp-agents/task-lists.md
SlashCommands -> docs/agent-platform/warp-agents/slash-commands.md
SuggestedRules -> docs/agent-platform/warp-agents/rules.md
RectSelection -> docs/warp/terminal/more-features/text-selection.md
ContextWindowUsageV2 -> docs/agent-platform/warp-agents/interacting-with-agents/README.md
ConfigurableBlockLimits -> docs/warp/terminal/blocks/block-basics.md
CommandCorrectionKey -> docs/warp/terminal/entry/command-corrections.md
ClassicCompletions -> docs/warp/terminal/command-completions/completions.md
DynamicWorkflowEnums -> docs/warp/knowledge-and-collaboration/warp-drive/workflows.md
SharedWithMe -> docs/warp/knowledge-and-collaboration/warp-drive/README.md
WarpPacks -> docs/warp/knowledge-and-collaboration/warp-drive/README.md
TabbedEditorView -> docs/warp/code/code-editor/README.md
ReadImageFiles -> docs/agent-platform/warp-agents/agent-context/images-as-context.md
FileRetrievalTools -> docs/agent-platform/warp-agents/codebase-context.md
ConversationArtifacts -> docs/agent-platform/warp-agents/interacting-with-agents/README.md
OzChangelogUpdates -> docs/changelog/README.md
ActiveConversationRequiresInteraction -> docs/agent-platform/warp-agents/interacting-with-agents/README.md

# Recently shipped GA features
VerticalTabs -> docs/warp/terminal/windows/vertical-tabs.md
TabConfigs -> docs/warp/terminal/windows/tab-configs.md
PluggableNotifications -> docs/warp/terminal/more-features/notifications.md
RevertToCheckpoints -> docs/agent-platform/warp-agents/slash-commands.md
RewindSlashCommand -> docs/agent-platform/warp-agents/slash-commands.md
ForkFromCommand -> docs/agent-platform/warp-agents/slash-commands.md
SummarizationConversationCommand -> docs/agent-platform/warp-agents/slash-commands.md
CodeReviewFind -> docs/warp/code/code-review.md
CodeReviewSaveChanges -> docs/warp/code/code-review.md
DiscardPerFileAndAllChanges -> docs/warp/code/code-review.md
AutoOpenCodeReviewPane -> docs/warp/code/code-review.md
GitOperationsInCodeReview -> docs/warp/code/code-review.md
AgentView -> docs/agent-platform/warp-agents/interacting-with-agents/terminal-and-agent-modes.md
AgentViewBlockContext -> docs/agent-platform/warp-agents/agent-context/blocks-as-context.md
CloudConversations -> docs/agent-platform/warp-agents/cloud-conversations.md
CloudModeFromLocalSession -> docs/agent-platform/cloud-agents/overview.md
TeamApiKeys -> docs/reference/cli/api-keys.md
PRCommentsSlashCommand -> docs/agent-platform/warp-agents/slash-commands.md
PRCommentsV2 -> docs/agent-platform/warp-agents/interacting-with-agents/README.md
CLIAgentRichInput -> docs/agent-platform/cli-agents/rich-input.md
HOANotifications -> docs/agent-platform/warp-agents/agent-notifications.md
OpenCodeNotifications -> docs/agent-platform/cli-agents/opencode.md
CodexNotifications -> docs/agent-platform/cli-agents/codex.md
HOARemoteControl -> docs/agent-platform/cli-agents/remote-control.md
GlobalSearch -> docs/warp/code/overview.md
FileBasedMcp -> docs/agent-platform/warp-agents/mcp.md
ConversationsAsContext -> docs/agent-platform/warp-agents/agent-context/blocks-as-context.md
GithubPrPromptChip -> docs/agent-platform/warp-agents/agent-notifications.md
AskUserQuestion -> docs/agent-platform/warp-agents/interacting-with-agents/README.md
AIContextMenuEnabled -> docs/agent-platform/warp-agents/agent-context/using-to-add-context.md
AtMenuOutsideOfAIMode -> docs/agent-platform/warp-agents/agent-context/using-to-add-context.md
AIContextMenuCode -> docs/agent-platform/warp-agents/agent-context/using-to-add-context.md
DriveObjectsAsContext -> docs/agent-platform/warp-agents/agent-context/using-to-add-context.md
KittyKeyboardProtocol -> docs/warp/terminal/more-features/full-screen-apps.md
InlineRepoMenu -> docs/agent-platform/warp-agents/codebase-context.md
InlineHistoryMenu -> docs/agent-platform/warp-agents/interacting-with-agents/terminal-and-agent-modes.md
SkillArguments -> docs/agent-platform/warp-agents/skills.md
AgentToolbarEditor -> docs/agent-platform/cli-agents/overview.md
ConfigurableToolbar -> docs/warp/terminal/windows/configurable-toolbar.md

## CLI commands -> doc pages

# Top-level Oz CLI commands
oz agent -> docs/reference/cli/README.md
oz environment -> docs/reference/cli/integration-setup.md
oz mcp -> docs/reference/cli/mcp-servers.md
oz run -> docs/reference/cli/README.md
oz model -> docs/reference/cli/README.md
oz login -> docs/reference/cli/README.md
oz logout -> docs/reference/cli/README.md
oz integration -> docs/reference/cli/integration-setup.md
oz schedule -> docs/reference/cli/README.md
oz secret -> docs/reference/cli/README.md
oz provider -> docs/reference/cli/README.md

## API endpoints -> doc pages

# Public API endpoints
POST /agent/run -> docs/reference/api-and-sdk/README.md
GET /agent/runs -> docs/reference/api-and-sdk/README.md
GET /agent/runs/{runId} -> docs/reference/api-and-sdk/README.md

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
