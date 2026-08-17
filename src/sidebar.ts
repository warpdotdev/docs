import type { StarlightSidebarTopicsUserConfig } from 'starlight-sidebar-topics';

/**
 * Top-level sidebar topics, one per "tab" the docs site exposes.
 *
 * `starlight-sidebar-topics` reads this array and renders each entry as a
 * pill in the header + a sidebar tree below. Slugs are relative to
 * `src/content/docs/`. Object form (`{ slug, label }`) lets us override
 * the link label without renaming the underlying MDX file.
 *
 * Lifted out of `astro.config.mjs` so content reorgs land here instead of
 * lengthening the integration config — `git blame` on a moved page now
 * points at this file.
 *
 * Item order and section grouping follows the source GitBook SUMMARY.md
 * files in ~/Projects/gitbook so the migrated site preserves the original
 * navigation structure.
 */
export const sidebarTopics: StarlightSidebarTopicsUserConfig = [
		{
			label: 'Terminal',
			link: '/',
			icon: 'laptop',
			items: [
				{
					label: 'Getting started',
					items: [
						{ label: 'Getting started with Warp and Oz', link: '/' },
						{ slug: 'quickstart', label: 'Warp quickstart' },
						'getting-started/quickstart/installation-and-setup',
						'getting-started/quickstart/coding-in-warp',
						'getting-started/quickstart/customizing-warp',
						{
							label: 'Migrate to Warp',
							collapsed: true,
							items: [
								{ slug: 'getting-started/migrate-to-warp', label: 'Overview' },
								'getting-started/migrate-to-warp/migrate-to-warp-from-claude-code',
								'getting-started/migrate-to-warp/migrate-to-warp-from-cursor',
								'getting-started/migrate-to-warp/migrate-to-warp-from-ghostty',
								'getting-started/migrate-to-warp/migrate-to-warp-from-iterm2',
								'getting-started/migrate-to-warp/migrate-to-warp-from-macos-terminal',
								'getting-started/migrate-to-warp/migrate-to-warp-from-vs-code-terminal',
								'getting-started/migrate-to-warp/migrate-to-warp-from-windows-terminal',
							],
						},
						{ slug: 'getting-started/supported-shells', label: 'Supported shells' },
						{ slug: 'getting-started/keyboard-shortcuts', label: 'Keyboard shortcuts' },
					],
				},
				{
					label: 'Terminal',
					items: [
						'terminal/input/universal-input',
						'terminal/input/classic-input',
						{
							label: 'Blocks',
							collapsed: true,
							items: [
								{ slug: 'terminal/blocks', label: 'Overview' },
								{ slug: 'terminal/blocks/block-basics', label: 'Block basics' },
								{ slug: 'terminal/blocks/block-actions', label: 'Block actions' },
								{ slug: 'terminal/blocks/block-sharing', label: 'Block sharing' },
								{ slug: 'terminal/blocks/find', label: 'Block find' },
								{ slug: 'terminal/blocks/block-filtering', label: 'Block filtering' },
								{ slug: 'terminal/blocks/background-blocks', label: 'Background blocks' },
								'terminal/blocks/sticky-command-header',
							],
						},
						{
							label: 'Modern text editing',
							collapsed: true,
							items: [
								{ slug: 'terminal/editor', label: 'Overview' },
								{ slug: 'terminal/editor/alias-expansion', label: 'Alias expansion' },
								{ slug: 'terminal/editor/command-inspector', label: 'Command inspector' },
								{ slug: 'terminal/editor/syntax-error-highlighting', label: 'Syntax & error highlighting' },
								{ slug: 'terminal/editor/vim', label: 'Vim keybindings' },
							],
						},
						{
							label: 'Command entry',
							collapsed: true,
							items: [
								{ slug: 'terminal/entry', label: 'Overview' },
								{ slug: 'terminal/entry/command-corrections', label: 'Command corrections' },
								{ slug: 'terminal/entry/command-search', label: 'Command search' },
								{ slug: 'terminal/entry/command-history', label: 'Command history' },
								{ slug: 'terminal/entry/synchronized-inputs', label: 'Synchronized inputs' },
								{ slug: 'terminal/entry/yaml-workflows', label: 'YAML workflows' },
							],
						},
						{
							label: 'Command completions',
							collapsed: true,
							items: [
								{ slug: 'terminal/command-completions', label: 'Overview' },
								{ slug: 'terminal/command-completions/completions', label: 'Tab completions' },
								'terminal/command-completions/autosuggestions',
							],
						},
						{
							label: 'Windows and Tabs',
							collapsed: true,
							items: [
								{ slug: 'terminal/windows', label: 'Overview' },
								'terminal/windows/tabs',
								{ slug: 'terminal/windows/vertical-tabs', label: 'Vertical Tabs' },
								'terminal/windows/split-panes',
								'terminal/windows/tab-configs',
								'terminal/windows/configurable-toolbar',
								{ slug: 'terminal/windows/global-hotkey', label: 'Global hotkey' },
								{ slug: 'terminal/sessions/launch-configurations', label: 'Launch Configurations (Legacy)' },
							],
						},
						{
							label: 'Sessions',
							collapsed: true,
							items: [
								{ slug: 'terminal/sessions', label: 'Overview' },
								{ slug: 'terminal/sessions/session-navigation', label: 'Session navigation' },
								{ slug: 'terminal/sessions/session-restoration', label: 'Session restoration' },
							],
						},
						{
							label: 'Terminal appearance',
							collapsed: true,
							items: [
								{ slug: 'terminal/appearance', label: 'Overview' },
								{ slug: 'terminal/appearance/themes', label: 'Themes' },
								{ slug: 'terminal/appearance/custom-themes', label: 'Custom themes' },
								{ slug: 'terminal/appearance/prompt', label: 'Prompt' },
								'terminal/appearance/input-position',
								{ slug: 'terminal/appearance/text-fonts-cursor', label: 'Text, fonts, & cursor' },
								{ slug: 'terminal/appearance/size-opacity-blurring', label: 'Size, opacity, & blurring' },
								{ slug: 'terminal/appearance/pane-dimming', label: 'Pane dimming & focus' },
								{ slug: 'terminal/appearance/blocks-behavior', label: 'Blocks behavior' },
								{ slug: 'terminal/appearance/tabs-behavior', label: 'Tabs behavior' },
								{ slug: 'terminal/appearance/app-icons', label: 'Custom app icons' },
							],
						},
						{
							label: 'Settings file',
							collapsed: true,
							items: [
								{ slug: 'terminal/settings', label: 'Overview' },
								{ slug: 'terminal/settings/all-settings', label: 'All settings reference' },
								{ slug: 'terminal/settings/file-locations', label: 'File locations' },
							],
						},
						{
							label: 'Warpify overview',
							collapsed: true,
							items: [
								{ slug: 'terminal/warpify', label: 'Overview' },
								{ slug: 'terminal/warpify/subshells', label: 'Warpify subshells' },
								{ slug: 'terminal/warpify/ssh', label: 'SSH with Warp features' },
								{ slug: 'terminal/warpify/ssh-legacy', label: 'Legacy SSH wrapper' },
							],
						},
						{
							label: 'More Features',
							collapsed: true,
							items: [
								{ slug: 'terminal/more-features', label: 'Overview' },
								'terminal/more-features/accessibility',
								{ slug: 'terminal/more-features/files-and-links', label: 'Files, links, & scripts' },
								{ slug: 'terminal/more-features/markdown-viewer', label: 'Markdown viewer' },
								{ slug: 'terminal/more-features/working-directory', label: 'Working directory' },
								'terminal/more-features/text-selection',
								'terminal/more-features/full-screen-apps',
								{ slug: 'terminal/more-features/notifications', label: 'Desktop notifications' },
								{ slug: 'terminal/more-features/audible-bell', label: 'Audible terminal bell' },
								{ slug: 'terminal/more-features/settings-sync', label: 'Settings Sync (Beta)' },
								{ slug: 'terminal/more-features/quit-warning', label: 'Terminal quit warning' },
								{ slug: 'terminal/more-features/uri-scheme', label: 'Warp URI scheme' },
								{ slug: 'terminal/more-features/linux', label: 'Warp for Linux' },
							],
						},
						'terminal/command-palette',
						{
							label: 'Terminal comparisons',
							collapsed: true,
							items: [
								{ slug: 'terminal/comparisons', label: 'Overview' },
								{ slug: 'terminal/comparisons/performance', label: 'Performance benchmarks' },
							],
						},
						{ slug: 'terminal/comparisons/terminal-features', label: 'Terminal features' },
						{ slug: 'terminal/integrations-and-plugins', label: 'Terminal integrations' },
					],
				},
				{
					label: 'Code',
					items: [
						{ slug: 'code/overview', label: 'Code overview' },
						{
							label: 'Built-in code editor',
							collapsed: true,
							items: [
								{ slug: 'code/code-editor', label: 'Overview' },
								{ slug: 'code/code-editor/language-server-protocol', label: 'Language Server Protocol (LSP)' },
								{ slug: 'code/code-editor/file-tree', label: 'File Tree (Project Explorer)' },
								{ slug: 'code/code-editor/find-and-replace', label: 'Find & replace' },
								{ slug: 'code/code-editor/code-editor-vim-keybindings', label: 'Code editor Vim keybindings' },
							],
						},
						{ slug: 'code/code-review', label: 'Code Review panel' },
						{ slug: 'code/git-worktrees', label: 'Git Worktrees' },
						{ slug: 'code/ssh-feature-support', label: 'Feature support over SSH' },
					],
				},
				{
					label: 'Knowledge and collaboration',
					items: [
						{
							label: 'Warp Drive overview',
							collapsed: true,
							items: [
								{ slug: 'knowledge-and-collaboration/warp-drive', label: 'Overview' },
								{ slug: 'knowledge-and-collaboration/warp-drive/notebooks', label: 'Notebooks' },
								{ slug: 'knowledge-and-collaboration/warp-drive/workflows', label: 'Workflows' },
								{ slug: 'knowledge-and-collaboration/warp-drive/prompts', label: 'Prompts' },
								'knowledge-and-collaboration/warp-drive/environment-variables',
								{ slug: 'knowledge-and-collaboration/warp-drive/ai-objects', label: 'AI-Integrated Objects' },
								{ slug: 'knowledge-and-collaboration/warp-drive/web', label: 'Warp Drive on the web' },
								{ slug: 'knowledge-and-collaboration/warp-drive/agent-mode-context', label: 'Agent Mode context' },
							],
						},
						{ slug: 'knowledge-and-collaboration/teams', label: 'Team management' },
						{ slug: 'knowledge-and-collaboration/admin-panel', label: 'Team Admin Panel' },
						{ slug: 'knowledge-and-collaboration/session-sharing', label: 'Session sharing' },
					],
				},
			],
		},
		{
			label: 'Agents',
			link: '/agents/',
			icon: 'puzzle',
			items: [
				{
					label: 'Getting started',
					items: [
						{ slug: 'agents', label: 'Agents overview' },
						'agents/getting-started/agents-in-warp',
						'agents/getting-started/faqs',
					],
				},
				{
					label: 'Warp Agents',
					items: [
						{ slug: 'agents/local-agents/overview', label: 'Overview' },
						{
							label: 'Capabilities',
							collapsed: true,
							items: [
								{ slug: 'agents/capabilities', label: 'Overview' },
								{ slug: 'agents/capabilities/slash-commands', label: 'Slash commands' },
								'agents/capabilities/skills',
								'agents/capabilities/planning',
								{ slug: 'agents/capabilities/task-lists', label: 'Task lists' },
								'agents/capabilities/rules',
								{ slug: 'agents/capabilities/agent-notifications', label: 'Agent notifications' },
								{ slug: 'agents/capabilities/full-terminal-use', label: 'Full terminal use' },
								{
									label: 'Computer Use',
									collapsed: true,
									items: [
										{ slug: 'agents/capabilities/computer-use', label: 'Overview' },
										{ slug: 'agents/capabilities/computer-use/browser-use', label: 'Browser use' },
										{ slug: 'agents/capabilities/computer-use/testing-and-recordings', label: 'Testing and recordings' },
										{ slug: 'agents/capabilities/computer-use/artifacts-in-prs', label: 'Screenshots and videos in PRs' },
									],
								},
								'agents/capabilities/codebase-context',
								{ slug: 'agents/capabilities/agent-profiles-permissions', label: 'Profiles & permissions' },
								{ slug: 'agents/capabilities/web-search', label: 'Web search' },
								{ slug: 'agents/local-agents/session-sharing', label: 'Session sharing' },
								'agents/local-agents/cloud-conversations',
							],
						},
						{
							label: 'Interacting with agents',
							collapsed: true,
							items: [
								{ slug: 'agents/local-agents/interacting-with-agents', label: 'Overview' },
								'agents/local-agents/interacting-with-agents/terminal-and-agent-modes',
								{ slug: 'agents/local-agents/interacting-with-agents/prompt-queueing', label: 'Prompt queueing' },
                { slug: 'agents/local-agents/interacting-with-agents/agent-questions', label: 'Agent questions' },
								{ slug: 'agents/local-agents/interacting-with-agents/conversation-forking', label: 'Conversation forking' },
								{ slug: 'agents/local-agents/code-diffs', label: 'Code diffs' },
								'agents/local-agents/interacting-with-agents/voice',
							],
						},
						{
							label: 'Agent context',
							collapsed: true,
							items: [
								{ slug: 'agents/local-agents/agent-context', label: 'Overview' },
								{ slug: 'agents/local-agents/agent-context/blocks-as-context', label: 'Blocks as context' },
								{ slug: 'agents/local-agents/agent-context/images-as-context', label: 'Images as context' },
								{ slug: 'agents/local-agents/agent-context/urls-as-context', label: 'URLs as context' },
								{ slug: 'agents/local-agents/agent-context/selection-as-context', label: 'Selection as context' },
								{ slug: 'agents/local-agents/agent-context/using-to-add-context', label: 'Using @ to add context' },
								'agents/capabilities/mcp',
							],
						},
						{
							label: 'Inference & providers',
							collapsed: true,
							items: [
								{ slug: 'agents/inference/model-choice', label: 'Model choice' },
								{ slug: 'agents/inference/custom-routers', label: 'Custom routers' },
								'agents/inference/bring-your-own-api-key',
								{ slug: 'agents/inference/custom-inference-endpoint', label: 'Custom inference endpoint' },
								{ slug: 'agents/inference/grok-subscription', label: 'SuperGrok subscription' },
							],
						},
						{ slug: 'agents/local-agents/interactive-code-review', label: 'Interactive code review' },
						{ slug: 'agents/local-agents/active-ai', label: 'Active AI recommendations' },
						'agents/local-agents/generate',
					],
				},
				{
					label: 'Warp Agent CLI',
					items: [
						{ slug: 'agents/cli', label: 'Overview' },
						{ slug: 'agents/cli/quickstart', label: 'Quickstart' },
						{
							label: 'Using the agent',
							collapsed: true,
							items: [
								{ slug: 'agents/cli/agent-conversations', label: 'Agent conversations' },
								{ slug: 'agents/cli/input-and-shell-commands', label: 'Input & shell commands' },
								{ slug: 'agents/cli/permissions-and-profiles', label: 'Permissions & profiles' },
								{ slug: 'agents/cli/cloud-and-orchestration', label: 'Cloud & orchestration' },
							],
						},
						{
							label: 'Context & customization',
							collapsed: true,
							items: [
								{ slug: 'agents/cli/configuration', label: 'Configuration' },
								{ slug: 'agents/cli/models-and-usage', label: 'Models & usage' },
							],
						},
						{ slug: 'agents/cli/reference', label: 'CLI reference' },
					],
				},
				{
					label: 'Third-Party CLI Agents',
					items: [
						{ slug: 'agents/cli-agents/overview', label: 'Overview' },
						'agents/cli-agents/claude-code',
						'agents/cli-agents/codex',
						'agents/cli-agents/opencode',
						'agents/cli-agents/rich-input',
						'agents/cli-agents/remote-control',
					],
				},
				{
					label: 'Memory (Research Preview)',
					items: [
						{ slug: 'agents/agent-memory', label: 'Agent Memory' },
					],
				},
			],
		},
		{
			label: 'Oz',
			link: '/platform/',
			icon: 'cloud-download',
			items: [
				{ slug: 'platform', label: 'Cloud agents overview' },
				{
					label: 'Getting started',
					items: [
						{ slug: 'platform/quickstart', label: 'Quickstart' },
						{ slug: 'platform/overview', label: 'Oz platform' },
					],
				},
				{
					label: 'Triggers',
					items: [
						{ slug: 'platform/triggers', label: 'Overview' },
						{ slug: 'platform/triggers/scheduled-agents-quickstart', label: 'Quickstart' },
						{ slug: 'platform/triggers/scheduled-agents', label: 'Scheduled agents' },
					],
				},
				{
					label: 'Integrations',
					items: [
						{ slug: 'platform/integrations', label: 'Overview' },
						{ slug: 'platform/integrations/quickstart', label: 'Quickstart' },
						'platform/integrations/slack',
						'platform/integrations/linear',
						'platform/integrations/jira',
						'platform/integrations/github',
						{
							label: 'GitHub Actions',
							collapsed: true,
							items: [
								{ slug: 'platform/integrations/github-actions', label: 'Overview' },
								{ slug: 'platform/integrations/quickstart-github-actions', label: 'Quickstart' },
							],
						},
						'platform/integrations/azure-devops',
						'platform/integrations/bitbucket',
						'platform/integrations/gitlab',
						{ slug: 'platform/integrations/cloud-providers', label: 'AWS, GCP, and other cloud providers' },
					],
				},
				{
					label: 'Managing agents',
					items: [
						'platform/environments',
						{ slug: 'platform/runners', label: 'Runners' },
						{ slug: 'platform/managing-cloud-agents', label: 'Managing cloud agents' },
						{ slug: 'platform/agents', label: 'Agents' },
						{ slug: 'platform/viewing-cloud-agent-runs', label: 'Viewing cloud agent runs' },
						{ slug: 'platform/oz-web-app', label: 'Oz web app' },
					],
				},
				{
					label: 'Orchestration',
					items: [
						{ slug: 'platform/orchestration', label: 'Multi-agent orchestration' },
						{ slug: 'platform/orchestration/multi-agent-runs', label: 'Running orchestrated agents' },
						{ slug: 'platform/software-factory', label: 'Software factory' },
					],
				},
				{
					label: 'Handoff',
					items: [
						{ slug: 'platform/handoff', label: 'Overview' },
						{ slug: 'platform/handoff/local-to-cloud', label: 'Local to cloud' },
						{ slug: 'platform/handoff/cloud-to-cloud', label: 'Cloud to cloud' },
						{ slug: 'platform/handoff/snapshots', label: 'Snapshots' },
					],
				},
				{
					label: 'Harnesses',
					items: [
						{ slug: 'platform/harnesses', label: 'Overview' },
						{ slug: 'platform/harnesses/warp-agent', label: 'Warp Agent' },
						{ slug: 'platform/harnesses/claude-code', label: 'Claude Code' },
						{ slug: 'platform/harnesses/codex', label: 'Codex' },
						{ slug: 'platform/harnesses/authentication', label: 'Authentication' },
					],
				},
				{
					label: 'Extending agents',
					items: [
						{ slug: 'platform/skills-as-agents', label: 'Skills as agents' },
						{ slug: 'platform/mcp', label: 'MCP servers' },
						'platform/secrets',
					],
				},
				{
					label: 'Deployment & hosting',
					items: [
						{ slug: 'platform/deployment-patterns', label: 'Deployment patterns' },
						{ slug: 'platform/warp-hosting', label: 'Warp-hosted agents' },
						{
							label: 'Self-hosting',
							collapsed: true,
							items: [
								{ slug: 'platform/self-hosting', label: 'Overview' },
								{ slug: 'platform/self-hosting/quickstart', label: 'Quickstart' },
								{ slug: 'platform/self-hosting/managed-docker', label: 'Managed: Docker' },
								{ slug: 'platform/self-hosting/managed-kubernetes', label: 'Managed: Kubernetes' },
								{ slug: 'platform/self-hosting/managed-direct', label: 'Managed: Direct' },
								{ slug: 'platform/self-hosting/unmanaged', label: 'Unmanaged' },
								'platform/self-hosting/monitoring',
								{ slug: 'platform/self-hosting/reference', label: 'Self-hosted worker reference' },
								'platform/self-hosting/security-and-networking',
								{ slug: 'platform/self-hosting/troubleshooting', label: 'Troubleshooting' },
							],
						},
					],
				},
				{
					label: 'Access & support',
					items: [
						{ slug: 'platform/team-access-billing-and-identity', label: 'Access, billing, and identity' },
						{ slug: 'platform/faqs', label: 'Cloud agent FAQs' },
					],
				},
			],
		},
		{
			label: 'Reference',
			link: '/reference/',
			icon: 'open-book',
			items: [
				{ slug: 'reference', label: 'Technical reference' },
				{
					label: 'CLI',
					items: [
						{ slug: 'reference/cli', label: 'Oz CLI' },
						{ slug: 'reference/cli/quickstart', label: 'Quickstart' },
						{ slug: 'reference/cli/api-keys', label: 'API Keys' },
						{ slug: 'reference/cli/agent-profiles', label: 'Agent Profiles' },
						{ slug: 'reference/cli/mcp-servers', label: 'MCP Servers' },
						{ slug: 'reference/cli/skills', label: 'Skills' },
						{ slug: 'reference/cli/warp-drive', label: 'Warp Drive Context' },
						{ slug: 'reference/cli/integration-setup', label: 'Integration Setup' },
						{ slug: 'reference/cli/artifacts', label: 'Artifacts' },
						{ slug: 'reference/cli/federate', label: 'Federated identity' },
						'reference/cli/troubleshooting',
					],
				},
				{
					label: 'API & SDK',
					items: [
						{ slug: 'reference/api-and-sdk', label: 'Oz API & SDK' },
						{ slug: 'reference/api-and-sdk/quickstart', label: 'Quickstart' },
						{ label: 'API Reference', link: '/api' },
						'reference/api-and-sdk/demo-sentry-monitoring-with-sdk',
						{
							label: 'API Troubleshooting',
							collapsed: true,
							items: [
								{ slug: 'reference/api-and-sdk/troubleshooting', label: 'API Troubleshooting' },
								{
									label: 'Errors',
									collapsed: true,
									items: [
										{ slug: 'reference/api-and-sdk/troubleshooting/errors', label: 'Errors' },
										'reference/api-and-sdk/troubleshooting/errors/insufficient-credits',
										'reference/api-and-sdk/troubleshooting/errors/feature-not-available',
										'reference/api-and-sdk/troubleshooting/errors/external-authentication-required',
										'reference/api-and-sdk/troubleshooting/errors/not-authorized',
										'reference/api-and-sdk/troubleshooting/errors/invalid-request',
										'reference/api-and-sdk/troubleshooting/errors/resource-not-found',
										'reference/api-and-sdk/troubleshooting/errors/budget-exceeded',
										'reference/api-and-sdk/troubleshooting/errors/integration-disabled',
										'reference/api-and-sdk/troubleshooting/errors/integration-not-configured',
										'reference/api-and-sdk/troubleshooting/errors/operation-not-supported',
										'reference/api-and-sdk/troubleshooting/errors/environment-setup-failed',
										'reference/api-and-sdk/troubleshooting/errors/content-policy-violation',
										'reference/api-and-sdk/troubleshooting/errors/conflict',
										'reference/api-and-sdk/troubleshooting/errors/authentication-required',
										'reference/api-and-sdk/troubleshooting/errors/resource-unavailable',
										'reference/api-and-sdk/troubleshooting/errors/internal-error',
										'reference/api-and-sdk/troubleshooting/errors/infrastructure-timeout',
										'reference/api-and-sdk/troubleshooting/errors/agent-process-failed',
									],
								},
							],
						},
					],
				},
			],
		},
		{
			// Link-only topic: navigates straight to the standalone Scalar API
			// reference at `/api`. Uses the plugin's `sidebarTopicLinkSchema`
			// shape (no `items`) since `/api` isn't a Starlight route and
			// doesn't have a per-topic sidebar tree. The `seti:json` icon is a
			// graceful fallback for the mobile drawer; the desktop
			// `WarpTopicNav` overrides this with a custom `</>` inline SVG via
			// its `CUSTOM_TOPIC_ICONS` map.
			label: 'API',
			link: '/api',
			icon: 'seti:json',
		},
	{
		label: 'Changelog',
		link: '/changelog/2026/',
		icon: 'document',
		items: [
			{ slug: 'changelog', label: 'All years' },
			{ slug: 'changelog/2026', label: '2026' },
			{ slug: 'changelog/2025', label: '2025' },
			{ slug: 'changelog/2024', label: '2024' },
			{ slug: 'changelog/2023', label: '2023' },
			{ slug: 'changelog/2022', label: '2022' },
			{ slug: 'changelog/2021', label: '2021' },
		],
	},
		{
			label: 'Support & Community',
			link: '/support-and-community/',
			icon: 'comment',
			items: [
				{ slug: 'support-and-community', label: 'Support and Community' },
				{
					label: 'Community',
					items: [
						'support-and-community/community/contributing',
						'support-and-community/community/warp-preview-and-alpha-program',
						{ slug: 'support-and-community/community/refer-a-friend', label: 'Refer a Friend & Earn Rewards' },
						'support-and-community/community/open-source-partnership',
					],
				},
				{
					label: 'Troubleshooting and support',
					items: [
						{ slug: 'support-and-community/troubleshooting-and-support/sending-us-feedback', label: 'Sending Feedback & Logs' },
						'support-and-community/troubleshooting-and-support/known-issues',
						'support-and-community/troubleshooting-and-support/troubleshooting-login-issues',
						'support-and-community/troubleshooting-and-support/using-warp-offline',
						'support-and-community/troubleshooting-and-support/updating-warp',
						{ slug: 'support-and-community/troubleshooting-and-support/logging-out-and-uninstalling', label: 'Logging Out & Uninstalling' },
					],
				},
				{
					label: 'Plans and billing',
					items: [
						{ slug: 'support-and-community/plans-and-billing', label: 'Overview' },
						{ slug: 'support-and-community/plans-and-billing/plans-pricing-refunds', label: 'Plans, Pricing, & Refunds' },
						'support-and-community/plans-and-billing/credits',
						'support-and-community/plans-and-billing/add-on-credits',
						{ slug: 'support-and-community/plans-and-billing/platform-credits', label: 'Platform credits' },
						'support-and-community/plans-and-billing/pricing-faqs',
					],
				},
				{
					label: 'Privacy, security, and licensing',
					items: [
						'support-and-community/privacy-and-security/privacy',
						'support-and-community/privacy-and-security/secret-redaction',
						'support-and-community/privacy-and-security/network-log',
						{ slug: 'support-and-community/community/open-source-licenses', label: 'Open Source Licenses' },
					],
				},
			],
		},
		{
		label: 'Enterprise',
		link: '/enterprise/',
		icon: 'setting',
			items: [
				{
					label: 'Getting started',
					items: [
						{ slug: 'enterprise', label: 'Overview' },
						{ slug: 'enterprise/getting-started/quickstart', label: 'Quick start' },
						{ slug: 'enterprise/getting-started/getting-started-enterprise', label: 'Getting started for admins' },
						{ slug: 'enterprise/getting-started/getting-started-developers', label: 'Getting started for developers' },
						{ slug: 'enterprise/getting-started/faq', label: 'FAQ' },
					],
				},
				{
					label: 'Security and compliance',
					items: [
						{ slug: 'enterprise/security-and-compliance/security-overview', label: 'Security overview' },
						{ slug: 'enterprise/security-and-compliance/sso', label: 'Single Sign-On (SSO)' },
						{ slug: 'enterprise/security-and-compliance/trust-center', label: 'Trust Center' },
					],
				},
				{
					label: 'Team management',
					items: [
						'enterprise/team-management/teams',
						{ slug: 'enterprise/team-management/admin-panel', label: 'Admin panel' },
						{ slug: 'enterprise/team-management/roles-and-permissions', label: 'Roles and permissions' },
					],
				},
				{
					label: 'Enterprise features',
					items: [
					{ slug: 'enterprise/enterprise-features/architecture-and-deployment', label: 'Architecture and deployment' },
						{ slug: 'enterprise/enterprise-features/bring-your-own-llm', label: 'Bring your own LLM' },
						{ slug: 'enterprise/enterprise-features/byollm-aws-bedrock', label: 'BYOLLM: AWS Bedrock' },
						{ slug: 'enterprise/enterprise-features/byollm-gemini-enterprise', label: 'BYOLLM: Gemini Enterprise' },
						{ slug: 'enterprise/enterprise-features/team-managed-keys-and-endpoints', label: 'Team-managed LLM keys and endpoints' },
						{ slug: 'enterprise/enterprise-features/analytics-api', label: 'Analytics API' },
					],
				},
				{
					label: 'Support and resources',
					items: [
						'enterprise/support-and-resources/billing',
						{ slug: 'enterprise/support-and-resources/troubleshooting-login', label: 'Troubleshooting login' },
						{ slug: 'enterprise/support-and-resources/feedback-and-feature-requests', label: 'Feedback and feature requests' },
					],
				},
			],
		},
		{
		id: 'guides',
		label: 'Guides',
		link: '/guides/',
		icon: 'rocket',
			items: [
				{ slug: 'guides', label: 'Guides' },
				{
					label: 'Getting started',
					items: [
						'guides/getting-started/welcome-to-warp',
				{ slug: 'guides/getting-started/10-coding-features-you-should-know', label: '10 coding features you should know' },
						{ slug: 'guides/getting-started/how-to-customize-warps-appearance', label: 'Customize Warp\'s appearance' },
						{ slug: 'guides/getting-started/how-to-make-warps-ui-more-minimal', label: 'Make Warp\'s UI more minimal' },
						{ slug: 'guides/getting-started/how-to-master-warps-code-review-panel', label: 'Master Warp\'s Code Review panel' },
					],
				},
				{
					label: 'Agent workflows',
					items: [
						{ slug: 'guides/agent-workflows/how-to-review-ai-generated-code', label: 'Review AI-generated code' },
						{ slug: 'guides/agent-workflows/how-to-attach-agent-session-context-to-github-prs', label: 'Attach agent context to PRs' },
						{ slug: 'guides/agent-workflows/how-to-run-unattended-agents', label: 'Run agents unattended' },
						{ slug: 'guides/agent-workflows/how-to-run-multiple-ai-coding-agents', label: 'Run multiple AI coding agents' },
						{ slug: 'guides/agent-workflows/how-to-use-voice-and-images-to-prompt-coding-agents', label: 'Use voice and images to prompt agents' },
						{ slug: 'guides/agent-workflows/how-to-explain-your-codebase-using-warp-rust-codebase', label: 'Explain your codebase with agents' },
						{ slug: 'guides/agent-workflows/warp-for-product-managers', label: '5 agent workflows for product managers' },
						{ slug: 'guides/agent-workflows/how-to-run-3-agents-in-parallel-summarize-logs-analyze-pr-modify-ui', label: 'Run tasks in parallel' },
						{ slug: 'guides/agent-workflows/how-to-edit-agent-code-in-warp', label: 'Edit agent-generated code in Warp' },
						{ slug: 'guides/agent-workflows/how-to-review-prs-like-a-senior-dev', label: 'Review PRs like a senior dev' },
						{ slug: 'guides/agent-workflows/using-images-as-context-with-warp', label: 'Use images as context for agents' },
						{ slug: 'guides/agent-workflows/understanding-your-codebase', label: 'Understand a large codebase with agents' },
					],
				},
				{
					label: 'Build a software factory',
					items: [
						{ slug: 'guides/agent-workflows/build-a-triage-agent', label: 'Build a triage agent' },
						{ slug: 'guides/agent-workflows/write-product-and-tech-specs-with-agents', label: 'Write specs with agents' },
						{ slug: 'guides/agent-workflows/set-up-a-software-factory', label: 'Set up your software factory' },
						{ slug: 'guides/agent-workflows/run-a-software-factory-in-the-cloud', label: 'Run a software factory in the cloud' },
						{ slug: 'guides/agent-workflows/build-a-self-improving-agent', label: 'Build a self-improving agent' },
					],
				},
				{
					label: 'Configuration',
					items: [
						{ slug: 'guides/configuration/how-to-create-project-rules-for-an-existing-project-astro-typescript-tailwind', label: 'Create project Rules' },
						{ slug: 'guides/configuration/how-to-set-coding-best-practices', label: 'Set coding best practices with Rules' },
						{ slug: 'guides/configuration/how-to-set-tech-stack-preferences-with-rules', label: 'Set tech stack preferences with Rules' },
						{ slug: 'guides/configuration/how-to-set-coding-preferences-with-rules', label: 'Set coding preferences with Rules' },
						{ slug: 'guides/configuration/how-to-configure-yolo-and-strategic-agent-profiles', label: 'Configure Agent Profiles (YOLO & strategic)' },
						{ slug: 'guides/configuration/how-to-use-agent-profiles-efficiently', label: 'Use Agent Profiles efficiently' },
						{ slug: 'guides/configuration/how-to-use-tokens-efficiently-with-ai-coding-agents', label: 'Use tokens efficiently' },
						{ slug: 'guides/configuration/creating-rules-for-agents', label: 'Create reusable Rules for your team' },
						{ slug: 'guides/configuration/trigger-reusable-actions-with-saved-prompts', label: 'Trigger reusable actions with saved prompts' },
						{ slug: 'guides/configuration/how-to-set-up-self-serve-data-analytics-with-skills', label: 'Set up self-serve data analytics with Skills' },
						{ slug: 'guides/configuration/how-to-sync-your-monorepos', label: 'Sync your monorepos' },
					],
				},
				{
					label: 'External tools & integrations',
					items: [
						{ slug: 'guides/external-tools/how-to-set-up-claude-code', label: 'Set up Claude Code' },
						{ slug: 'guides/external-tools/how-to-set-up-codex-cli', label: 'Set up Codex CLI' },
						{ slug: 'guides/external-tools/how-to-set-up-opencode', label: 'Set up OpenCode' },
						{ slug: 'guides/external-tools/how-to-set-up-gemini-cli', label: 'Set up Gemini CLI' },
						{ slug: 'guides/external-tools/how-to-set-up-ollama', label: 'Set up Ollama for local models' },
						{ slug: 'guides/external-tools/sentry-mcp-fix-sentry-error-in-empower-website', label: 'Sentry MCP: fix errors' },
						{ slug: 'guides/external-tools/figma-remote-mcp-create-a-website-from-a-figma-file-from-scratch', label: 'Figma remote MCP: create a website from a Figma file' },
						{ slug: 'guides/external-tools/linear-mcp-retrieve-issue-data', label: 'Linear MCP: retrieve issue data' },
						{ slug: 'guides/external-tools/linear-mcp-updating-tickets-with-a-lean-build-approach', label: 'Linear MCP: update tickets' },
						{ slug: 'guides/external-tools/github-mcp-summarizing-open-prs-and-creating-gh-issues', label: 'GitHub MCP: summarize PRs and create issues' },
						{ slug: 'guides/external-tools/puppeteer-mcp-scraping-amazon-web-reviews', label: 'Puppeteer MCP: scrape web reviews' },
						{ slug: 'guides/external-tools/context7-mcp-update-astro-project-with-best-practices', label: 'Context7 MCP: update with best practices' },
						{ slug: 'guides/external-tools/sqlite-and-stripe-mcp-basic-queries-you-can-make-after-set-up', label: 'SQLite and Stripe MCP: basic queries' },
						{ slug: 'guides/external-tools/using-mcp-servers-with-warp', label: 'Connect agents to MCP servers' },
					],
				},
				{
					label: 'Build an app in Warp',
					items: [
						{ slug: 'guides/build-an-app-in-warp/building-a-real-time-chat-app-github-mcp-railway', label: 'Build a real-time chat app' },
						{ slug: 'guides/build-an-app-in-warp/building-a-chrome-extension-d3js-javascript-html-css', label: 'Build a Chrome extension' },
						{ slug: 'guides/build-an-app-in-warp/building-warps-input-with-warp', label: 'Build Warp\'s input component' },
					],
				},
				{
					label: 'DevOps & infrastructure',
					items: [
						{ slug: 'guides/devops/how-to-analyze-cloud-run-logs-gcloud', label: 'Analyze Cloud Run logs (gcloud)' },
						{ slug: 'guides/devops/how-to-create-a-production-ready-docker-setup', label: 'Create a production-ready Docker setup' },
						{ slug: 'guides/devops/improve-your-kubernetes-workflow-kubectl-helm', label: 'Improve your Kubernetes workflow' },
						{ slug: 'guides/devops/how-to-prevent-secrets-from-leaking', label: 'Prevent secrets from leaking' },
						{ slug: 'guides/devops/how-to-generate-unit-and-security-tests-to-debug-faster', label: 'Generate unit and security tests' },
						{ slug: 'guides/devops/how-to-write-sql-commands-inside-a-postgres-repl', label: 'Write SQL commands in a Postgres REPL' },
						{ slug: 'guides/devops/how-to-create-priority-matrix-for-database-optimization', label: 'Create a priority matrix for database optimization' },
					],
				},
				{
					label: 'Frontend & UI',
					items: [
						{ slug: 'guides/frontend/how-to-replace-a-ui-element-in-warp-rust-codebase', label: 'Replace a UI element in Warp (Rust codebase)' },
						{ slug: 'guides/frontend/how-to-actually-code-ui-that-matches-your-mockup-react-tailwind', label: 'Code UI that matches your mockup (React + Tailwind)' },
					],
				},
			],
		},
];
