// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import starlightSidebarTopics from 'starlight-sidebar-topics';
import vercel from '@astrojs/vercel';

// https://astro.build/config
export default defineConfig({
	site: 'https://docs.warp.dev',
	integrations: [
		starlight({
			title: 'Warp Docs',
			logo: {
				light: './src/assets/warp-logo-light.svg',
				dark: './src/assets/warp-logo-dark.svg',
				replacesTitle: true,
			},
			customCss: ['./src/styles/custom.css'],
			components: {
				Head: './src/components/CustomHead.astro',
			},
			social: [
				{ icon: 'github', label: 'GitHub', href: 'https://github.com/warpdotdev' },
			],
			plugins: [
				starlightSidebarTopics([
					{
						label: 'Terminal',
						link: '/',
						icon: 'laptop',
						items: [
							{
								label: 'Getting Started',
								items: [
									{ slug: 'index', label: 'Overview' },
									'quickstart',
									'getting-started/what-is-warp',
									'getting-started/quickstart/installation-and-setup',
									'getting-started/quickstart/coding-in-warp',
									'getting-started/quickstart/customizing-warp',
									'getting-started/migrate-to-warp',
									'getting-started/supported-shells',
									'getting-started/keyboard-shortcuts',
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
											'terminal/blocks/block-basics',
											'terminal/blocks/block-actions',
											'terminal/blocks/block-sharing',
											'terminal/blocks/find',
											'terminal/blocks/block-filtering',
											'terminal/blocks/background-blocks',
											'terminal/blocks/sticky-command-header',
										],
									},
									{
										label: 'Modern Text Editing',
										items: [
											{ slug: 'terminal/editor', label: 'Overview' },
											'terminal/editor/alias-expansion',
											'terminal/editor/command-inspector',
											'terminal/editor/syntax-error-highlighting',
											'terminal/editor/vim',
										],
									},
									{
										label: 'Command Entry',
										items: [
											{ slug: 'terminal/entry', label: 'Overview' },
											'terminal/entry/command-corrections',
											'terminal/entry/command-search',
											'terminal/entry/command-history',
											'terminal/entry/synchronized-inputs',
											'terminal/entry/yaml-workflows',
										],
									},
									{
										label: 'Command Completions',
										items: [
											{ slug: 'terminal/command-completions', label: 'Overview' },
											'terminal/command-completions/completions',
											'terminal/command-completions/autosuggestions',
										],
									},
									{
										label: 'Session Management',
										items: [
											{ slug: 'terminal/sessions', label: 'Overview' },
											'terminal/sessions/launch-configurations',
											'terminal/sessions/session-navigation',
											'terminal/sessions/session-restoration',
										],
									},
									{
										label: 'Window Management',
										items: [
											{ slug: 'terminal/windows', label: 'Overview' },
											'terminal/windows/global-hotkey',
											'terminal/windows/tabs',
											'terminal/windows/split-panes',
										],
									},
									{
										label: 'Appearance',
										items: [
											{ slug: 'terminal/appearance', label: 'Overview' },
											'terminal/appearance/themes',
											'terminal/appearance/custom-themes',
											'terminal/appearance/prompt',
											'terminal/appearance/input-position',
											'terminal/appearance/text-fonts-cursor',
											'terminal/appearance/size-opacity-blurring',
											'terminal/appearance/pane-dimming',
											'terminal/appearance/blocks-behavior',
											'terminal/appearance/tabs-behavior',
											'terminal/appearance/app-icons',
										],
									},
									{
										label: 'Warpify',
										items: [
											{ slug: 'terminal/warpify', label: 'Overview' },
											'terminal/warpify/subshells',
											'terminal/warpify/ssh',
											'terminal/warpify/ssh-legacy',
										],
									},
									{
										label: 'More Features',
										items: [
											{ slug: 'terminal/more-features', label: 'Overview' },
											'terminal/more-features/accessibility',
											'terminal/more-features/files-and-links',
											'terminal/more-features/markdown-viewer',
											'terminal/more-features/working-directory',
											'terminal/more-features/text-selection',
											'terminal/more-features/full-screen-apps',
											'terminal/more-features/notifications',
											'terminal/more-features/audible-bell',
											'terminal/more-features/settings-sync',
											'terminal/more-features/quit-warning',
											'terminal/more-features/uri-scheme',
											'terminal/more-features/linux',
										],
									},
									'terminal/command-palette',
									{
										label: 'Comparisons',
										items: [
											{ slug: 'terminal/comparisons', label: 'Overview' },
											'terminal/comparisons/performance',
										],
									},
									'terminal/comparisons/terminal-features',
									'terminal/integrations-and-plugins',
								],
							},
							{
								label: 'Code',
								items: [
									'code/overview',
									{
										label: 'Code Editor',
										items: [
											{ slug: 'code/code-editor', label: 'Overview' },
											'code/code-editor/language-server-protocol',
											'code/code-editor/file-tree',
											'code/code-editor/find-and-replace',
											'code/code-editor/code-editor-vim-keybindings',
										],
									},
									'code/code-review',
									'code/git-worktrees',
									'code/ssh-feature-support',
								],
							},
							{
								label: 'Knowledge & Collaboration',
								items: [
									{
										label: 'Warp Drive',
										items: [
											{ slug: 'knowledge-and-collaboration/warp-drive', label: 'Overview' },
											'knowledge-and-collaboration/warp-drive/notebooks',
											'knowledge-and-collaboration/warp-drive/workflows',
											'knowledge-and-collaboration/warp-drive/prompts',
											'knowledge-and-collaboration/warp-drive/environment-variables',
											'knowledge-and-collaboration/warp-drive/ai-objects',
											'knowledge-and-collaboration/warp-drive/web',
											'knowledge-and-collaboration/warp-drive/agent-mode-context',
										],
									},
									'knowledge-and-collaboration/teams',
									'knowledge-and-collaboration/admin-panel',
									{ slug: 'knowledge-and-collaboration/session-sharing', label: 'Session Sharing' },
								],
							},
						],
					},
					{
						label: 'Agent Platform',
						link: '/agent-platform/',
						icon: 'rocket',
						items: [
							{
								label: 'Getting Started',
								items: [
									{ slug: 'agent-platform', label: 'Overview' },
									'agent-platform/getting-started/agents-in-warp',
									'agent-platform/getting-started/faqs',
								],
							},
							{
								label: 'Capabilities',
								items: [
									{ slug: 'agent-platform/capabilities', label: 'Overview' },
									'agent-platform/capabilities/slash-commands',
									'agent-platform/capabilities/skills',
									'agent-platform/capabilities/planning',
									'agent-platform/capabilities/task-lists',
									'agent-platform/capabilities/model-choice',
									'agent-platform/capabilities/rules',
									'agent-platform/capabilities/full-terminal-use',
									'agent-platform/capabilities/computer-use',
									'agent-platform/capabilities/mcp',
									'agent-platform/capabilities/codebase-context',
									'agent-platform/capabilities/agent-profiles-permissions',
									'agent-platform/capabilities/web-search',
								],
							},
							{
								label: 'Local Agents',
								items: [
									'agent-platform/local-agents/overview',
									{
										label: 'Interacting with Agents',
										items: [
											{ slug: 'agent-platform/local-agents/interacting-with-agents', label: 'Agent Conversations' },
											'agent-platform/local-agents/interacting-with-agents/agent-modality',
											'agent-platform/local-agents/interacting-with-agents/conversation-forking',
											'agent-platform/local-agents/code-diffs',
											'agent-platform/local-agents/interacting-with-agents/voice',
										],
									},
									{
										label: 'Agent Context',
										items: [
											{ slug: 'agent-platform/local-agents/agent-context', label: 'Overview' },
											'agent-platform/local-agents/agent-context/blocks-as-context',
											'agent-platform/local-agents/agent-context/images-as-context',
											'agent-platform/local-agents/agent-context/urls-as-context',
											'agent-platform/local-agents/agent-context/selection-as-context',
											'agent-platform/local-agents/agent-context/using-to-add-context',
										],
									},
									'agent-platform/local-agents/interactive-code-review',
									'agent-platform/local-agents/session-sharing',
									'agent-platform/local-agents/third-party-cli-agents',
									'agent-platform/local-agents/active-ai',
									'agent-platform/local-agents/generate',
									'agent-platform/local-agents/cloud-conversations',
								],
							},
							{
								label: 'Cloud Agents & Orchestration',
								items: [
									'agent-platform/cloud-agents/overview',
									'agent-platform/cloud-agents/quickstart',
									'agent-platform/cloud-agents/platform',
									{
										label: 'Triggers',
										items: [
											{ slug: 'agent-platform/cloud-agents/triggers', label: 'Overview' },
											'agent-platform/cloud-agents/triggers/scheduled-agents',
										],
									},
									{
										label: 'Integrations',
										items: [
											{ slug: 'agent-platform/cloud-agents/integrations', label: 'Overview' },
											'agent-platform/cloud-agents/integrations/slack',
											'agent-platform/cloud-agents/integrations/linear',
											'agent-platform/cloud-agents/integrations/github-actions',
											'agent-platform/cloud-agents/integrations/demo-issue-triage-bot',
										],
									},
									'agent-platform/cloud-agents/environments',
									'agent-platform/cloud-agents/managing-cloud-agents',
									'agent-platform/cloud-agents/oz-web-app',
									'agent-platform/cloud-agents/skills-as-agents',
									'agent-platform/cloud-agents/viewing-cloud-agent-runs',
									'agent-platform/cloud-agents/secrets',
									'agent-platform/cloud-agents/mcp',
									'agent-platform/cloud-agents/deployment-patterns',
									{
										label: 'Self-Hosting',
										items: [
											'agent-platform/cloud-agents/self-hosting',
											'agent-platform/cloud-agents/managed-worker-reference',
										],
									},
									'agent-platform/cloud-agents/team-access-billing-and-identity',
									'agent-platform/cloud-agents/faqs',
								],
							},
						],
					},
					{
						label: 'University',
						link: '/university/',
						icon: 'puzzle',
						items: [
							{
								label: 'Getting Started',
								items: [
									{ slug: 'university', label: 'Overview' },
								],
							},
							{
								label: 'Warp Runtime',
								items: [
									{ slug: 'university/warp-runtime', label: 'Overview' },
									'university/warp-runtime/building-a-slackbot',
								],
							},
							{
								label: 'Developer Workflows',
								items: [
									{
										label: 'Beginner',
										items: [
											{ slug: 'university/developer-workflows/beginner', label: 'Overview' },
											'university/developer-workflows/beginner/welcome-to-warp',
											'university/developer-workflows/beginner/how-to-explain-your-codebase-using-warp-rust-codebase',
											'university/developer-workflows/beginner/how-to-create-project-rules-for-an-existing-project-astro-typescript-tailwind',
											'university/developer-workflows/beginner/10-coding-features-you-should-know',
											'university/developer-workflows/beginner/how-to-customize-warps-appearance',
											'university/developer-workflows/beginner/how-to-master-warps-code-review-panel',
											'university/developer-workflows/beginner/trigger-reusable-actions-with-saved-prompts',
											'university/developer-workflows/beginner/how-to-make-warps-ui-more-minimal',
										],
									},
									{
										label: 'Power User',
										items: [
											{ slug: 'university/developer-workflows/power-user', label: 'Overview' },
											'university/developer-workflows/power-user/how-to-run-3-agents-in-parallel-summarize-logs-analyze-pr-modify-ui',
											'university/developer-workflows/power-user/how-to-edit-agent-code-in-warp',
											'university/developer-workflows/power-user/how-to-configure-yolo-and-strategic-agent-profiles',
											'university/developer-workflows/power-user/how-to-sync-your-monorepos',
											'university/developer-workflows/power-user/how-to-review-prs-like-a-senior-dev',
											'university/developer-workflows/power-user/how-to-set-coding-best-practices',
											'university/developer-workflows/power-user/how-to-set-tech-stack-preferences-with-rules',
											'university/developer-workflows/power-user/how-to-set-coding-preferences-with-rules',
											'university/developer-workflows/power-user/how-to-use-agent-profiles-efficiently',
											'university/developer-workflows/power-user/warp-vs-claude-code',
										],
									},
									{
										label: 'DevOps',
										items: [
											{ slug: 'university/developer-workflows/devops', label: 'Overview' },
											'university/developer-workflows/devops/how-to-analyze-cloud-run-logs-gcloud',
											'university/developer-workflows/devops/how-to-create-a-production-ready-docker-setup',
										],
									},
									{
										label: 'Backend',
										items: [
											{ slug: 'university/developer-workflows/backend', label: 'Overview' },
											'university/developer-workflows/backend/how-to-write-sql-commands-inside-a-postgres-repl',
											'university/developer-workflows/backend/how-to-create-priority-matrix-for-database-optimization',
										],
									},
									{
										label: 'Frontend / UI',
										items: [
											{ slug: 'university/developer-workflows/frontend-ui', label: 'Overview' },
											'university/developer-workflows/frontend-ui/how-to-replace-a-ui-element-in-warp-rust-codebase',
											'university/developer-workflows/frontend-ui/how-to-actually-code-ui-that-matches-your-mockup-react-tailwind',
										],
									},
									{
										label: 'Testing & Security',
										items: [
											{ slug: 'university/developer-workflows/testing-and-security', label: 'Overview' },
											'university/developer-workflows/testing-and-security/how-to-generate-unit-and-security-tests-to-debug-faster',
											'university/developer-workflows/testing-and-security/how-to-prevent-secrets-from-leaking',
										],
									},
								],
							},
							{
								label: 'End-to-End Builds',
								items: [
									'university/end-to-end-builds/building-a-real-time-chat-app-github-mcp-railway',
									'university/end-to-end-builds/building-a-chrome-extension-d3js-javascript-html-css',
								],
							},
							{
								label: 'MCP Servers',
								items: [
									'university/mcp-servers/puppeteer-mcp-scraping-amazon-web-reviews',
									'university/mcp-servers/sentry-mcp-fix-sentry-error-in-empower-website',
									'university/mcp-servers/context7-mcp-update-astro-project-with-best-practices',
									'university/mcp-servers/figma-remote-mcp-create-a-website-from-a-figma-file-from-scratch',
									'university/mcp-servers/linear-mcp-retrieve-issue-data',
									'university/mcp-servers/linear-mcp-updating-tickets-with-a-lean-build-approach',
									'university/mcp-servers/sqlite-and-stripe-mcp-basic-queries-you-can-make-after-set-up',
									'university/mcp-servers/github-mcp-summarizing-open-prs-and-creating-gh-issues',
								],
							},
							{
								label: 'How Warp Uses Warp',
								items: [
									'university/how-warp-uses-warp/building-warps-input-with-warp',
									'university/how-warp-uses-warp/creating-rules-for-agents',
									'university/how-warp-uses-warp/understanding-your-codebase',
									'university/how-warp-uses-warp/using-images-as-context-with-warp',
									'university/how-warp-uses-warp/using-mcp-servers-with-warp',
									'university/how-warp-uses-warp/running-multiple-agents-at-once-with-warp',
								],
							},
							{
								label: 'Integrations',
								items: [
									'university/integrations/how-to-set-up-ollama',
								],
							},
							{
								label: 'Terminal / Command Line Tips',
								items: [
									'university/terminal-command-line-tips/improve-your-kubernetes-workflow-kubectl-helm',
								],
							},
						],
					},
					{
						label: 'Reference',
						link: '/reference/',
						icon: 'open-book',
						items: [
							{ slug: 'reference', label: 'Overview' },
							{
								label: 'CLI',
								items: [
									{ slug: 'reference/cli', label: 'Oz CLI' },
									'reference/cli/quickstart',
									'reference/cli/api-keys',
									'reference/cli/agent-profiles',
									'reference/cli/mcp-servers',
									'reference/cli/skills',
									'reference/cli/warp-drive',
									'reference/cli/integration-setup',
									'reference/cli/troubleshooting',
								],
							},
							{
								label: 'API & SDK',
								items: [
									{ slug: 'reference/api-and-sdk', label: 'Oz Agent API & SDK' },
									'reference/api-and-sdk/demo-sentry-monitoring-with-sdk',
									{
										label: 'Troubleshooting',
										items: [
											{ slug: 'reference/api-and-sdk/troubleshooting', label: 'Overview' },
											{
												label: 'Errors',
												items: [
													{ slug: 'reference/api-and-sdk/troubleshooting/errors', label: 'Overview' },
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
						icon: 'heart',
						items: [
							{
								label: 'Troubleshooting & Support',
								items: [
									{ slug: 'support-and-community', label: 'Overview' },
									'support-and-community/troubleshooting-and-support/sending-us-feedback',
									'support-and-community/troubleshooting-and-support/known-issues',
									'support-and-community/troubleshooting-and-support/troubleshooting-login-issues',
									'support-and-community/troubleshooting-and-support/using-warp-offline',
									'support-and-community/troubleshooting-and-support/updating-warp',
									'support-and-community/troubleshooting-and-support/logging-out-and-uninstalling',
									'support-and-community/troubleshooting-and-support/uninstalling-warp',
								],
							},
							{
								label: 'Plans & Billing',
								items: [
									{ slug: 'support-and-community/plans-and-billing', label: 'Overview' },
									'support-and-community/plans-and-billing/plans-pricing-refunds',
									'support-and-community/plans-and-billing/credits',
									'support-and-community/plans-and-billing/add-on-credits',
									'support-and-community/plans-and-billing/bring-your-own-api-key',
									'support-and-community/plans-and-billing/overages-legacy',
									'support-and-community/plans-and-billing/pricing-faqs',
								],
							},
							{
								label: 'Privacy & Security',
								items: [
									'support-and-community/privacy-and-security/privacy',
									'support-and-community/privacy-and-security/secret-redaction',
									'support-and-community/privacy-and-security/network-log',
								],
							},
							{
								label: 'Community',
								items: [
									'support-and-community/community/warp-preview-and-alpha-program',
									'support-and-community/community/refer-a-friend',
									'support-and-community/community/open-source-partnership',
									'support-and-community/community/open-source-licenses',
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
								label: 'Getting Started',
								items: [
									{ slug: 'enterprise', label: 'Overview' },
									'enterprise/getting-started/quickstart',
									'enterprise/getting-started/getting-started-enterprise',
									'enterprise/getting-started/getting-started-developers',
									'enterprise/getting-started/faq',
								],
							},
							{
								label: 'Security and Compliance',
								items: [
									'enterprise/security-and-compliance/security-overview',
									'enterprise/security-and-compliance/sso',
								],
							},
							{
								label: 'Team Management',
								items: [
									'enterprise/team-management/admin-panel',
									'enterprise/team-management/roles-and-permissions',
								],
							},
							{
								label: 'Enterprise Features',
								items: [
									'enterprise/enterprise-features/bring-your-own-llm',
								],
							},
						],
					},
				]),
			],
		}),
	],
	adapter: vercel(),
});
