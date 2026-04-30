# Feature Surface Map

Curated mapping of feature flags, CLI commands, and code modules to their expected documentation pages.
The audit script reads this file to reduce false positives — entries here are verified rather than flagged.

Format: `CodeIdentifier -> docs/path/to/page.md` (one per line within each section).
Lines starting with `#` are comments. Blank lines are ignored.

# Maintenance: when a new GA feature flag ships, add a mapping here.
# Run `python3 .warp/skills/missing_docs/scripts/audit_docs.py` to find unmapped flags.
# This audit is also run as a recurring scheduled Oz agent to catch drift.

## Feature flags -> doc pages

AgentMode -> src/content/docs/agent-platform/warp-agents/README.md
AgentManagementView -> src/content/docs/agent-platform/cloud-agents/managing-cloud-agents.md
AgentManagementDetailsView -> src/content/docs/agent-platform/cloud-agents/managing-cloud-agents.md
AgentModeComputerUse -> src/content/docs/agent-platform/warp-agents/computer-use.md
AgentModeWorkflows -> src/content/docs/knowledge-and-collaboration/warp-drive/workflows.md
AgentOnboarding -> src/content/docs/agent-platform/getting-started/agents-in-warp.md
AIRules -> src/content/docs/agent-platform/warp-agents/rules.md
AIResumeButton -> src/content/docs/agent-platform/warp-agents/interacting-with-agents/terminal-and-agent-modes.md
CodeReviewView -> src/content/docs/code/code-review.md
InlineCodeReview -> src/content/docs/agent-platform/warp-agents/interactive-code-review.md
FileTree -> src/content/docs/code/code-editor/file-tree.md
CodeFindReplace -> src/content/docs/code/code-editor/find-and-replace.md
VimCodeEditor -> src/content/docs/code/code-editor/code-editor-vim-keybindings.md
McpServer -> src/content/docs/agent-platform/warp-agents/mcp.md
McpOauth -> src/content/docs/agent-platform/warp-agents/mcp.md
ImageAsContext -> src/content/docs/agent-platform/warp-agents/agent-context/images-as-context.md
SelectionAsContext -> src/content/docs/agent-platform/warp-agents/agent-context/selection-as-context.md
DiffSetAsContext -> src/content/docs/agent-platform/warp-agents/agent-context/selection-as-context.md
WebSearchUI -> src/content/docs/agent-platform/warp-agents/web-search.md
WebFetchUI -> src/content/docs/agent-platform/warp-agents/web-search.md
CodebaseContext -> src/content/docs/agent-platform/warp-agents/codebase-context.md
CrossRepoContext -> src/content/docs/agent-platform/warp-agents/codebase-context.md
FullSourceCodeEmbedding -> src/content/docs/agent-platform/warp-agents/codebase-context.md
SearchCodebaseUI -> src/content/docs/agent-platform/warp-agents/codebase-context.md
CloudEnvironments -> src/content/docs/agent-platform/cloud-agents/environments.md
CloudMode -> src/content/docs/agent-platform/cloud-agents/overview.md
AmbientAgentsCommandLine -> src/content/docs/agent-platform/cloud-agents/overview.md
ScheduledAmbientAgents -> src/content/docs/agent-platform/cloud-agents/triggers/scheduled-agents.md
WarpManagedSecrets -> src/content/docs/agent-platform/cloud-agents/secrets.md
IntegrationCommand -> src/content/docs/reference/cli/integration-setup.md
ConversationManagement -> src/content/docs/agent-platform/warp-agents/cloud-conversations.md
ForkConversationFromBlock -> src/content/docs/agent-platform/warp-agents/interacting-with-agents/conversation-forking.md
Voice -> src/content/docs/agent-platform/warp-agents/interacting-with-agents/voice.md
WarpDrive -> src/content/docs/knowledge-and-collaboration/warp-drive/README.md
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
CreatingSharedSessions -> src/content/docs/knowledge-and-collaboration/session-sharing/README.md
AgentSharedSessions -> src/content/docs/agent-platform/warp-agents/session-sharing.md
ProfilesDesignRevamp -> src/content/docs/agent-platform/warp-agents/agent-profiles-permissions.md
MultiProfile -> src/content/docs/agent-platform/warp-agents/agent-profiles-permissions.md
InlineProfileSelector -> src/content/docs/agent-platform/warp-agents/agent-profiles-permissions.md
ModelChoice -> src/content/docs/agent-platform/warp-agents/model-choice.md
Skills -> src/content/docs/agent-platform/warp-agents/skills.md
ListSkills -> src/content/docs/agent-platform/warp-agents/skills.md
BundledSkills -> src/content/docs/agent-platform/warp-agents/skills.md
Planning -> src/content/docs/agent-platform/warp-agents/planning.md
SyncAmbientPlans -> src/content/docs/agent-platform/warp-agents/planning.md
TaskLists -> src/content/docs/agent-platform/warp-agents/task-lists.md
SlashCommands -> src/content/docs/agent-platform/warp-agents/slash-commands.md
SuggestedRules -> src/content/docs/agent-platform/warp-agents/rules.md
RectSelection -> src/content/docs/terminal/more-features/text-selection.md
ContextWindowUsageV2 -> src/content/docs/agent-platform/warp-agents/interacting-with-agents/README.md
ConfigurableBlockLimits -> src/content/docs/terminal/blocks/block-basics.md
CommandCorrectionKey -> src/content/docs/terminal/entry/command-corrections.md
ClassicCompletions -> src/content/docs/terminal/command-completions/completions.md
DynamicWorkflowEnums -> src/content/docs/knowledge-and-collaboration/warp-drive/workflows.md
SharedWithMe -> src/content/docs/knowledge-and-collaboration/warp-drive/README.md
WarpPacks -> src/content/docs/knowledge-and-collaboration/warp-drive/README.md
TabbedEditorView -> src/content/docs/code/code-editor/README.md
ReadImageFiles -> src/content/docs/agent-platform/warp-agents/agent-context/images-as-context.md
FileRetrievalTools -> src/content/docs/agent-platform/warp-agents/codebase-context.md
ConversationArtifacts -> src/content/docs/agent-platform/warp-agents/interacting-with-agents/README.md
OzChangelogUpdates -> src/content/docs/changelog/README.md
ActiveConversationRequiresInteraction -> src/content/docs/agent-platform/warp-agents/interacting-with-agents/README.md

# Recently shipped GA features
VerticalTabs -> src/content/docs/terminal/windows/vertical-tabs.md
TabConfigs -> src/content/docs/terminal/windows/tab-configs.md
PluggableNotifications -> src/content/docs/terminal/more-features/notifications.md
RevertToCheckpoints -> src/content/docs/agent-platform/warp-agents/slash-commands.md
RewindSlashCommand -> src/content/docs/agent-platform/warp-agents/slash-commands.md
ForkFromCommand -> src/content/docs/agent-platform/warp-agents/slash-commands.md
SummarizationConversationCommand -> src/content/docs/agent-platform/warp-agents/slash-commands.md
CodeReviewFind -> src/content/docs/code/code-review.md
CodeReviewSaveChanges -> src/content/docs/code/code-review.md
DiscardPerFileAndAllChanges -> src/content/docs/code/code-review.md
AutoOpenCodeReviewPane -> src/content/docs/code/code-review.md
GitOperationsInCodeReview -> src/content/docs/code/code-review.md
AgentView -> src/content/docs/agent-platform/warp-agents/interacting-with-agents/terminal-and-agent-modes.md
AgentViewBlockContext -> src/content/docs/agent-platform/warp-agents/agent-context/blocks-as-context.md
CloudConversations -> src/content/docs/agent-platform/warp-agents/cloud-conversations.md
CloudModeFromLocalSession -> src/content/docs/agent-platform/cloud-agents/overview.md
TeamApiKeys -> src/content/docs/reference/cli/api-keys.md
PRCommentsSlashCommand -> src/content/docs/agent-platform/warp-agents/slash-commands.md
PRCommentsV2 -> src/content/docs/agent-platform/warp-agents/interacting-with-agents/README.md
CLIAgentRichInput -> src/content/docs/agent-platform/cli-agents/rich-input.md
HOANotifications -> src/content/docs/agent-platform/warp-agents/agent-notifications.md
OpenCodeNotifications -> src/content/docs/agent-platform/cli-agents/opencode.md
CodexNotifications -> src/content/docs/agent-platform/cli-agents/codex.md
HOARemoteControl -> src/content/docs/agent-platform/cli-agents/remote-control.md
GlobalSearch -> src/content/docs/code/overview.md
FileBasedMcp -> src/content/docs/agent-platform/warp-agents/mcp.md
ConversationsAsContext -> src/content/docs/agent-platform/warp-agents/agent-context/blocks-as-context.md
GithubPrPromptChip -> src/content/docs/agent-platform/warp-agents/agent-notifications.md
AskUserQuestion -> src/content/docs/agent-platform/warp-agents/interacting-with-agents/README.md
AIContextMenuEnabled -> src/content/docs/agent-platform/warp-agents/agent-context/using-to-add-context.md
AtMenuOutsideOfAIMode -> src/content/docs/agent-platform/warp-agents/agent-context/using-to-add-context.md
AIContextMenuCode -> src/content/docs/agent-platform/warp-agents/agent-context/using-to-add-context.md
DriveObjectsAsContext -> src/content/docs/agent-platform/warp-agents/agent-context/using-to-add-context.md
KittyKeyboardProtocol -> src/content/docs/terminal/more-features/full-screen-apps.md
InlineRepoMenu -> src/content/docs/agent-platform/warp-agents/codebase-context.md
InlineHistoryMenu -> src/content/docs/agent-platform/warp-agents/interacting-with-agents/terminal-and-agent-modes.md
SkillArguments -> src/content/docs/agent-platform/warp-agents/skills.md

## CLI commands -> doc pages

# Top-level Oz CLI commands
oz agent -> src/content/docs/reference/cli/README.md
oz environment -> src/content/docs/reference/cli/integration-setup.md
oz mcp -> src/content/docs/reference/cli/mcp-servers.md
oz run -> src/content/docs/reference/cli/README.md
oz model -> src/content/docs/reference/cli/README.md
oz login -> src/content/docs/reference/cli/README.md
oz logout -> src/content/docs/reference/cli/README.md
oz integration -> src/content/docs/reference/cli/integration-setup.md
oz schedule -> src/content/docs/reference/cli/README.md
oz secret -> src/content/docs/reference/cli/README.md
oz provider -> src/content/docs/reference/cli/README.md

## API endpoints -> doc pages

# Public API endpoints
POST /agent/run -> src/content/docs/reference/api-and-sdk/README.md
GET /agent/runs -> src/content/docs/reference/api-and-sdk/README.md
GET /agent/runs/{runId} -> src/content/docs/reference/api-and-sdk/README.md

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
