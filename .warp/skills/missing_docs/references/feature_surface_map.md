# Feature Surface Map

Curated mapping of feature flags, CLI commands, and code modules to their expected documentation pages.
The audit script reads this file to reduce false positives — entries here are verified rather than flagged.

Format: `CodeIdentifier -> docs/path/to/page.md` (one per line within each section).
Lines starting with `#` are comments. Blank lines are ignored.

# Maintenance: when a new GA feature flag ships, add a mapping here.
# Run `python3 .warp/skills/missing_docs/scripts/audit_docs.py` to find unmapped flags.
# This audit is also run as a recurring scheduled Oz agent to catch drift.

## Feature flags -> doc pages

AgentMode -> docs/agent-platform/local-agents/agents-overview.md
AgentModeHomepage -> docs/agent-platform/local-agents/agents-overview.md
AgentModeHomepage2 -> docs/agent-platform/local-agents/agents-overview.md
AgentManagementPopup -> docs/agent-platform/cloud-agents/managing-cloud-agents.md
AgentManagementView -> docs/agent-platform/cloud-agents/managing-cloud-agents.md
AgentModeComputerUse -> docs/agent-platform/capabilities/computer-use.md
AgentModeWorkflows -> docs/warp/knowledge-and-collaboration/warp-drive/workflows.md
AgentOnboarding -> docs/agent-platform/getting-started/agents-in-warp.md
AIRules -> docs/agent-platform/capabilities/rules.md
AIResumeButton -> docs/agent-platform/local-agents/interacting-with-agents/agent-modality.md
CodeReviewView -> docs/warp/code/code-review.md
InlineCodeReview -> docs/agent-platform/local-agents/interactive-code-review.md
CodeModeV2 -> docs/warp/code/code-overview.md
FileTree -> docs/warp/code/code-editor/file-tree.md
CodeFindReplace -> docs/warp/code/code-editor/find-and-replace.md
VimCodeEditor -> docs/warp/code/code-editor/code-editor-vim-keybindings.md
McpServer -> docs/agent-platform/capabilities/mcp.md
McpOauth -> docs/agent-platform/capabilities/mcp.md
ImageAsContext -> docs/agent-platform/local-agents/agent-context/images-as-context.md
SelectionAsContext -> docs/agent-platform/local-agents/agent-context/selection-as-context.md
DiffSetAsContext -> docs/agent-platform/local-agents/agent-context/selection-as-context.md
WebSearchUI -> docs/agent-platform/capabilities/web-search.md
CodebaseContext -> docs/agent-platform/capabilities/codebase-context.md
CrossRepoContext -> docs/agent-platform/capabilities/codebase-context.md
FullSourceCodeEmbedding -> docs/agent-platform/capabilities/codebase-context.md
CloudEnvironments -> docs/agent-platform/cloud-agents/environments.md
CloudMode -> docs/agent-platform/cloud-agents/cloud-agents-overview.md
AmbientAgentsCommandLine -> docs/agent-platform/cloud-agents/cloud-agents-overview.md
ScheduledAmbientAgents -> docs/agent-platform/cloud-agents/triggers/scheduled-agents.md
WarpManagedSecrets -> docs/agent-platform/cloud-agents/cloud-agent-secrets.md
IntegrationCommand -> docs/reference/cli/integrations-and-environments.md
ConversationManagement -> docs/agent-platform/local-agents/cloud-conversations.md
ConversationManagementV1 -> docs/agent-platform/local-agents/cloud-conversations.md
ForkConversationFromBlock -> docs/agent-platform/local-agents/interacting-with-agents/conversation-forking.md
Voice -> docs/agent-platform/local-agents/interacting-with-agents/voice.md
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
CreditTransparency -> docs/support-and-community/plans-and-billing/credits.md
APIKeyAuthentication -> docs/reference/cli/api-keys.md
APIKeyManagement -> docs/reference/cli/api-keys.md
SecretRedaction -> docs/support-and-community/privacy-and-security/secret-redaction.md
CreatingSharedSessions -> docs/warp/knowledge-and-collaboration/session-sharing/README.md
AgentSharedSessions -> docs/agent-platform/cloud-agents/agent-session-sharing.md
ProfilesDesignRevamp -> docs/agent-platform/capabilities/agent-profiles-permissions.md
MultiProfile -> docs/agent-platform/capabilities/agent-profiles-permissions.md
ModelChoice -> docs/agent-platform/capabilities/model-choice.md
Skills -> docs/agent-platform/capabilities/skills.md
Planning -> docs/agent-platform/capabilities/planning.md
TaskLists -> docs/agent-platform/capabilities/task-lists.md
SlashCommands -> docs/agent-platform/capabilities/slash-commands.md

## CLI commands -> doc pages

# Top-level Oz CLI commands
oz agent -> docs/reference/cli/README.md
oz environment -> docs/reference/cli/integrations-and-environments.md
oz mcp -> docs/reference/cli/mcp-servers-for-cloud-agents.md
oz run -> docs/reference/cli/README.md
oz model -> docs/reference/cli/README.md
oz login -> docs/reference/cli/README.md
oz logout -> docs/reference/cli/README.md
oz integration -> docs/reference/cli/integrations-and-environments.md
oz schedule -> docs/reference/cli/README.md
oz secret -> docs/reference/cli/README.md
oz provider -> docs/reference/cli/README.md

## API endpoints -> doc pages

# Public API endpoints
POST /agent/run -> docs/reference/api-and-sdk/README.md
GET /agent/runs -> docs/reference/api-and-sdk/README.md
GET /agent/runs/{runId} -> docs/reference/api-and-sdk/README.md

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
