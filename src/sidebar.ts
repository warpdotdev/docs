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
							items: [
								{ slug: 'terminal/command-completions', label: 'Overview' },
								{ slug: 'terminal/command-completions/completions', label: 'Tab completions' },
								'terminal/command-completions/autosuggestions',
							],
						},
						{
							label: 'Windows and Tabs',
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
							items: [
								{ slug: 'terminal/sessions', label: 'Overview' },
								{ slug: 'terminal/sessions/session-navigation', label: 'Session navigation' },
								{ slug: 'terminal/sessions/session-restoration', label: 'Session restoration' },
							],
						},
						{
							label: 'Terminal appearance',
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
							items: [
								{ slug: 'terminal/settings', label: 'Overview' },
								{ slug: 'terminal/settings/all-settings', label: 'All settings reference' },
							],
						},
						{
							label: 'Warpify overview',
							items: [
								{ slug: 'terminal/warpify', label: 'Overview' },
								{ slug: 'terminal/warpify/subshells', label: 'Warpify subshells' },
								{ slug: 'terminal/warpify/ssh', label: 'SSH with Warp features' },
								{ slug: 'terminal/warpify/ssh-legacy', label: 'Legacy SSH wrapper' },
							],
						},
						{
							label: 'More Features',
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
			link: '/agent-platform/',
			icon: 'puzzle',
			items: [
				{
					label: 'Getting started',
					items: [
						{ slug: 'agent-platform', label: 'Agents overview' },
						'agent-platform/getting-started/agents-in-warp',
						'agent-platform/getting-started/faqs',
					],
				},
				{
					label: 'Warp Agents',
					items: [
						{ slug: 'agent-platform/local-agents/overview', label: 'Warp Agents overview' },
						{
							label: 'Capabilities',
							items: [
								{ slug: 'agent-platform/capabilities', label: 'Overview' },
								{ slug: 'agent-platform/capabilities/slash-commands', label: 'Slash commands' },
								'agent-platform/capabilities/skills',
								'agent-platform/capabilities/planning',
								{ slug: 'agent-platform/capabilities/task-lists', label: 'Task lists' },
								'agent-platform/capabilities/model-choice',
								'agent-platform/capabilities/rules',
								{ slug: 'agent-platform/capabilities/agent-notifications', label: 'Agent notifications' },
								{ slug: 'agent-platform/capabilities/full-terminal-use', label: 'Full terminal use' },
								{ slug: 'agent-platform/capabilities/computer-use', label: 'Computer use' },
								'agent-platform/capabilities/codebase-context',
								{ slug: 'agent-platform/capabilities/agent-profiles-permissions', label: 'Profiles & permissions' },
								{ slug: 'agent-platform/capabilities/web-search', label: 'Web search' },
								{ slug: 'agent-platform/local-agents/session-sharing', label: 'Session sharing' },
								'agent-platform/local-agents/cloud-conversations',
							],
						},
						{
							label: 'Interacting with agents',
							items: [
								{ slug: 'agent-platform/local-agents/interacting-with-agents', label: 'Overview' },
								'agent-platform/local-agents/interacting-with-agents/terminal-and-agent-modes',
								{ slug: 'agent-platform/local-agents/interacting-with-agents/conversation-forking', label: 'Conversation forking' },
								{ slug: 'agent-platform/local-agents/code-diffs', label: 'Code diffs' },
								'agent-platform/local-agents/interacting-with-agents/voice',
							],
						},
						{
							label: 'Agent context',
							items: [
								{ slug: 'agent-platform/local-agents/agent-context', label: 'Overview' },
								{ slug: 'agent-platform/local-agents/agent-context/blocks-as-context', label: 'Blocks as context' },
								{ slug: 'agent-platform/local-agents/agent-context/images-as-context', label: 'Images as context' },
								{ slug: 'agent-platform/local-agents/agent-context/urls-as-context', label: 'URLs as context' },
								{ slug: 'agent-platform/local-agents/agent-context/selection-as-context', label: 'Selection as context' },
								{ slug: 'agent-platform/local-agents/agent-context/using-to-add-context', label: 'Using @ to add context' },
								'agent-platform/capabilities/mcp',
							],
						},
						{ slug: 'agent-platform/local-agents/interactive-code-review', label: 'Interactive code review' },
						{ slug: 'agent-platform/local-agents/active-ai', label: 'Active AI recommendations' },
						'agent-platform/local-agents/generate',
					],
				},
				{
					label: 'Third-Party CLI Agents',
					items: [
						{ slug: 'agent-platform/cli-agents/overview', label: 'Overview' },
						'agent-platform/cli-agents/claude-code',
						'agent-platform/cli-agents/codex',
						'agent-platform/cli-agents/opencode',
						'agent-platform/cli-agents/rich-input',
						'agent-platform/cli-agents/remote-control',
					],
				},
				{
					label: 'Oz Cloud Agents & Orchestration',
					items: [
						{ slug: 'agent-platform/cloud-agents/overview', label: 'Cloud agents overview' },
						{ slug: 'agent-platform/cloud-agents/quickstart', label: 'Quickstart' },
						{ slug: 'agent-platform/cloud-agents/platform', label: 'Oz platform' },
						{
							label: 'Triggers',
							items: [
								{ slug: 'agent-platform/cloud-agents/triggers', label: 'Overview' },
								{ slug: 'agent-platform/cloud-agents/triggers/scheduled-agents-quickstart', label: 'Quickstart' },
								{ slug: 'agent-platform/cloud-agents/triggers/scheduled-agents', label: 'Scheduled agents' },
							],
						},
						{
							label: 'Integrations',
							items: [
								{ slug: 'agent-platform/cloud-agents/integrations', label: 'Overview' },
								{ slug: 'agent-platform/cloud-agents/integrations/quickstart', label: 'Quickstart' },
								'agent-platform/cloud-agents/integrations/slack',
								'agent-platform/cloud-agents/integrations/linear',
								{
									label: 'GitHub Actions',
									items: [
										{ slug: 'agent-platform/cloud-agents/integrations/github-actions', label: 'Overview' },
										{ slug: 'agent-platform/cloud-agents/integrations/quickstart-github-actions', label: 'Quickstart' },
									],
								},
								'agent-platform/cloud-agents/integrations/azure-devops',
								'agent-platform/cloud-agents/integrations/bitbucket',
								'agent-platform/cloud-agents/integrations/gitlab',
								{ slug: 'agent-platform/cloud-agents/integrations/cloud-providers', label: 'AWS, GCP, and other cloud providers' },
								{ slug: 'agent-platform/cloud-agents/integrations/demo-issue-triage-bot', label: 'Demo: Issue triage bot' },
							],
						},
						'agent-platform/cloud-agents/environments',
						{ slug: 'agent-platform/cloud-agents/managing-cloud-agents', label: 'Managing cloud agents' },
						{ slug: 'agent-platform/cloud-agents/oz-web-app', label: 'Oz web app' },
						{ slug: 'agent-platform/cloud-agents/skills-as-agents', label: 'Skills as agents' },
						{ slug: 'agent-platform/cloud-agents/viewing-cloud-agent-runs', label: 'Viewing cloud agent runs' },
						'agent-platform/cloud-agents/secrets',
						{ slug: 'agent-platform/cloud-agents/mcp', label: 'MCP servers' },
						{ slug: 'agent-platform/cloud-agents/deployment-patterns', label: 'Deployment patterns' },
						{
							label: 'Self-hosting',
							items: [
								{ slug: 'agent-platform/cloud-agents/self-hosting', label: 'Overview' },
								{ slug: 'agent-platform/cloud-agents/self-hosting/quickstart', label: 'Quickstart' },
								{ slug: 'agent-platform/cloud-agents/self-hosting/managed-docker', label: 'Managed: Docker' },
								{ slug: 'agent-platform/cloud-agents/self-hosting/managed-kubernetes', label: 'Managed: Kubernetes' },
								{ slug: 'agent-platform/cloud-agents/self-hosting/managed-direct', label: 'Managed: Direct' },
								{ slug: 'agent-platform/cloud-agents/self-hosting/unmanaged', label: 'Unmanaged' },
								'agent-platform/cloud-agents/self-hosting/monitoring',
								{ slug: 'agent-platform/cloud-agents/self-hosting/reference', label: 'Self-hosted worker reference' },
								'agent-platform/cloud-agents/self-hosting/security-and-networking',
								{ slug: 'agent-platform/cloud-agents/self-hosting/troubleshooting', label: 'Troubleshooting' },
							],
						},
						{ slug: 'agent-platform/cloud-agents/team-access-billing-and-identity', label: 'Access, billing, and identity' },
						{ slug: 'agent-platform/cloud-agents/faqs', label: 'Cloud agent FAQs' },
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
							items: [
								{ slug: 'reference/api-and-sdk/troubleshooting', label: 'API Troubleshooting' },
								{
									label: 'Errors',
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
			link: '/changelog/',
			icon: 'document',
			items: [
				{ slug: 'changelog', label: 'Changelog' },
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
						'support-and-community/plans-and-billing/bring-your-own-api-key',
						'support-and-community/plans-and-billing/overages-legacy',
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
			icon: 'star',
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
			icon: 'puzzle',
			items: [
				{ slug: 'guides', label: 'Guides' },
				{
					label: 'Getting started',
					items: [
						'guides/getting-started/welcome-to-warp',
						{ slug: 'guides/getting-started/10-coding-features-you-should-know', label: '10 Warp Coding Features You Should Know' },
						{ slug: 'guides/getting-started/how-to-customize-warps-appearance', label: 'Customize Warp\'s Appearance' },
						{ slug: 'guides/getting-started/how-to-make-warps-ui-more-minimal', label: 'Make Warp\'s UI More Minimal' },
						{ slug: 'guides/getting-started/how-to-master-warps-code-review-panel', label: 'Master Warp\'s Code Review Panel' },
					],
				},
				{
					label: 'Agent workflows',
					items: [
						{ slug: 'guides/agent-workflows/how-to-review-ai-generated-code', label: 'Review AI-Generated Code' },
						{ slug: 'guides/agent-workflows/how-to-run-multiple-ai-coding-agents', label: 'Run Multiple AI Coding Agents' },
						{ slug: 'guides/agent-workflows/how-to-use-voice-and-images-to-prompt-coding-agents', label: 'Use Voice and Images to Prompt Agents' },
						{ slug: 'guides/agent-workflows/how-to-explain-your-codebase-using-warp-rust-codebase', label: 'Explain Your Codebase with Agents' },
						{ slug: 'guides/agent-workflows/warp-for-product-managers', label: '5 AI Agent Workflows for Product Managers' },
						{ slug: 'guides/agent-workflows/how-to-run-3-agents-in-parallel-summarize-logs-analyze-pr-modify-ui', label: 'Run Tasks in Parallel' },
						{ slug: 'guides/agent-workflows/how-to-edit-agent-code-in-warp', label: 'Edit Agent-Generated Code in Warp' },
						{ slug: 'guides/agent-workflows/how-to-review-prs-like-a-senior-dev', label: 'Review PRs Like a Senior Dev' },
						{ slug: 'guides/agent-workflows/using-images-as-context-with-warp', label: 'Use Images as Context for Agents' },
						{ slug: 'guides/agent-workflows/understanding-your-codebase', label: 'Understand a Large Codebase with Agents' },
						{ slug: 'guides/agent-workflows/running-multiple-agents-at-once-with-warp', label: 'Coordinate Agents on Separate Tasks' },
					],
				},
				{
					label: 'Configuration',
					items: [
						{ slug: 'guides/configuration/how-to-create-project-rules-for-an-existing-project-astro-typescript-tailwind', label: 'Create Project Rules' },
						{ slug: 'guides/configuration/how-to-set-coding-best-practices', label: 'Set Coding Best Practices with Rules' },
						{ slug: 'guides/configuration/how-to-set-tech-stack-preferences-with-rules', label: 'Set Tech Stack Preferences with Rules' },
						{ slug: 'guides/configuration/how-to-set-coding-preferences-with-rules', label: 'Set Coding Preferences with Rules' },
						{ slug: 'guides/configuration/how-to-configure-yolo-and-strategic-agent-profiles', label: 'Configure Agent Profiles (YOLO & Strategic)' },
						{ slug: 'guides/configuration/how-to-use-agent-profiles-efficiently', label: 'Use Agent Profiles Efficiently' },
						{ slug: 'guides/configuration/creating-rules-for-agents', label: 'Create Reusable Rules for Your Team' },
						{ slug: 'guides/configuration/trigger-reusable-actions-with-saved-prompts', label: 'Trigger Reusable Actions with Saved Prompts' },
						{ slug: 'guides/configuration/how-to-set-up-self-serve-data-analytics-with-skills', label: 'Set Up Self-Serve Data Analytics with Skills' },
						{ slug: 'guides/configuration/how-to-sync-your-monorepos', label: 'Sync Your Monorepos' },
					],
				},
				{
					label: 'External tools & integrations',
					items: [
						{ slug: 'guides/external-tools/how-to-set-up-claude-code', label: 'Set Up Claude Code' },
						{ slug: 'guides/external-tools/how-to-set-up-codex-cli', label: 'Set Up Codex CLI' },
						{ slug: 'guides/external-tools/how-to-set-up-opencode', label: 'Set Up OpenCode' },
						{ slug: 'guides/external-tools/how-to-set-up-gemini-cli', label: 'Set Up Gemini CLI' },
						{ slug: 'guides/external-tools/how-to-set-up-ollama', label: 'Set Up Ollama for Local Models' },
						{ slug: 'guides/external-tools/sentry-mcp-fix-sentry-error-in-empower-website', label: 'Sentry MCP: Fix Errors' },
						{ slug: 'guides/external-tools/figma-remote-mcp-create-a-website-from-a-figma-file-from-scratch', label: 'Figma Remote MCP: Create a Website from a Figma File' },
						{ slug: 'guides/external-tools/linear-mcp-retrieve-issue-data', label: 'Linear MCP: Retrieve Issue Data' },
						{ slug: 'guides/external-tools/linear-mcp-updating-tickets-with-a-lean-build-approach', label: 'Linear MCP: Updating Tickets' },
						{ slug: 'guides/external-tools/github-mcp-summarizing-open-prs-and-creating-gh-issues', label: 'GitHub MCP: Summarizing PRs & Creating Issues' },
						{ slug: 'guides/external-tools/puppeteer-mcp-scraping-amazon-web-reviews', label: 'Puppeteer MCP: Scraping Web Reviews' },
						{ slug: 'guides/external-tools/context7-mcp-update-astro-project-with-best-practices', label: 'Context7 MCP: Update with Best Practices' },
						{ slug: 'guides/external-tools/sqlite-and-stripe-mcp-basic-queries-you-can-make-after-set-up', label: 'SQLite and Stripe MCP: Basic Queries' },
						{ slug: 'guides/external-tools/using-mcp-servers-with-warp', label: 'Connect Agents to MCP Servers' },
					],
				},
				{
					label: 'Build an app in Warp',
					items: [
						{ slug: 'guides/build-an-app-in-warp/building-a-real-time-chat-app-github-mcp-railway', label: 'Build a Real-time Chat App' },
						{ slug: 'guides/build-an-app-in-warp/building-a-chrome-extension-d3js-javascript-html-css', label: 'Build a Chrome Extension' },
						{ slug: 'guides/build-an-app-in-warp/building-warps-input-with-warp', label: 'Build Warp\'s Own Input Component' },
						'guides/build-an-app-in-warp/building-a-slackbot',
					],
				},
				{
					label: 'DevOps & infrastructure',
					items: [
						{ slug: 'guides/devops/how-to-analyze-cloud-run-logs-gcloud', label: 'Analyze Cloud Run Logs (gcloud)' },
						{ slug: 'guides/devops/how-to-create-a-production-ready-docker-setup', label: 'Create a Production-Ready Docker Setup' },
						{ slug: 'guides/devops/improve-your-kubernetes-workflow-kubectl-helm', label: 'Improve Your Kubernetes Workflow' },
						{ slug: 'guides/devops/how-to-prevent-secrets-from-leaking', label: 'Prevent Secrets from Leaking' },
						{ slug: 'guides/devops/how-to-generate-unit-and-security-tests-to-debug-faster', label: 'Generate Unit and Security Tests' },
						{ slug: 'guides/devops/how-to-write-sql-commands-inside-a-postgres-repl', label: 'Write SQL Commands in a Postgres REPL' },
						{ slug: 'guides/devops/how-to-create-priority-matrix-for-database-optimization', label: 'Create a Priority Matrix for Database Optimization' },
					],
				},
				{
					label: 'Frontend & UI',
					items: [
						{ slug: 'guides/frontend/how-to-replace-a-ui-element-in-warp-rust-codebase', label: 'Replace a UI Element (Rust Codebase)' },
						{ slug: 'guides/frontend/how-to-actually-code-ui-that-matches-your-mockup-react-tailwind', label: 'Code UI That Matches Your Mockup (React + Tailwind)' },
					],
				},
			],
		},
];
