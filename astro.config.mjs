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
			components: {
				Head: './src/components/CustomHead.astro',
			},
			social: [
				{ icon: 'github', label: 'GitHub', href: 'https://github.com/warpdotdev' },
			],
			plugins: [
				starlightSidebarTopics([
					{
						label: 'Changelog',
						link: '/changelog/',
						icon: 'document',
						items: [
							{ slug: 'changelog', label: 'Changelog' },
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
						label: 'Terminal',
						link: '/terminal/',
						icon: 'laptop',
						items: [
							{
								label: 'Getting Started',
								items: [
									{ slug: 'terminal', label: 'Overview' },
									'terminal/quickstart',
									'terminal/getting-started/what-is-warp',
									'terminal/getting-started/quickstart/installation-and-setup',
									'terminal/getting-started/quickstart/coding-in-warp',
									'terminal/getting-started/quickstart/customizing-warp',
									'terminal/getting-started/migrate-to-warp',
									'terminal/getting-started/supported-shells',
									'terminal/getting-started/keyboard-shortcuts',
								],
							},
							{
								label: 'Terminal',
								items: [
									'terminal/terminal/input/universal-input',
									'terminal/terminal/input/classic-input',
									{
										label: 'Blocks',
										items: [
											{ slug: 'terminal/terminal/blocks', label: 'Overview' },
											'terminal/terminal/blocks/block-basics',
											'terminal/terminal/blocks/block-actions',
											'terminal/terminal/blocks/block-sharing',
											'terminal/terminal/blocks/find',
											'terminal/terminal/blocks/block-filtering',
											'terminal/terminal/blocks/background-blocks',
											'terminal/terminal/blocks/sticky-command-header',
										],
									},
									{
										label: 'Modern Text Editing',
										items: [
											{ slug: 'terminal/terminal/editor', label: 'Overview' },
											'terminal/terminal/editor/alias-expansion',
											'terminal/terminal/editor/command-inspector',
											'terminal/terminal/editor/syntax-error-highlighting',
											'terminal/terminal/editor/vim',
										],
									},
									{
										label: 'Command Entry',
										items: [
											{ slug: 'terminal/terminal/entry', label: 'Overview' },
											'terminal/terminal/entry/command-corrections',
											'terminal/terminal/entry/command-search',
											'terminal/terminal/entry/command-history',
											'terminal/terminal/entry/synchronized-inputs',
											'terminal/terminal/entry/yaml-workflows',
										],
									},
									{
										label: 'Command Completions',
										items: [
											{ slug: 'terminal/terminal/command-completions', label: 'Overview' },
											'terminal/terminal/command-completions/completions',
											'terminal/terminal/command-completions/autosuggestions',
										],
									},
									{
										label: 'Session Management',
										items: [
											{ slug: 'terminal/terminal/sessions', label: 'Overview' },
											'terminal/terminal/sessions/launch-configurations',
											'terminal/terminal/sessions/session-navigation',
											'terminal/terminal/sessions/session-restoration',
										],
									},
									{
										label: 'Window Management',
										items: [
											{ slug: 'terminal/terminal/windows', label: 'Overview' },
											'terminal/terminal/windows/global-hotkey',
											'terminal/terminal/windows/tabs',
											'terminal/terminal/windows/split-panes',
										],
									},
									{
										label: 'Appearance',
										items: [
											{ slug: 'terminal/terminal/appearance', label: 'Overview' },
											'terminal/terminal/appearance/themes',
											'terminal/terminal/appearance/custom-themes',
											'terminal/terminal/appearance/prompt',
											'terminal/terminal/appearance/input-position',
											'terminal/terminal/appearance/text-fonts-cursor',
											'terminal/terminal/appearance/size-opacity-blurring',
											'terminal/terminal/appearance/pane-dimming',
											'terminal/terminal/appearance/blocks-behavior',
											'terminal/terminal/appearance/tabs-behavior',
											'terminal/terminal/appearance/app-icons',
										],
									},
									{
										label: 'Warpify',
										items: [
											{ slug: 'terminal/terminal/warpify', label: 'Overview' },
											'terminal/terminal/warpify/subshells',
											'terminal/terminal/warpify/ssh',
											'terminal/terminal/warpify/ssh-legacy',
										],
									},
									{
										label: 'More Features',
										items: [
											{ slug: 'terminal/terminal/more-features', label: 'Overview' },
											'terminal/terminal/more-features/accessibility',
											'terminal/terminal/more-features/files-and-links',
											'terminal/terminal/more-features/markdown-viewer',
											'terminal/terminal/more-features/working-directory',
											'terminal/terminal/more-features/text-selection',
											'terminal/terminal/more-features/full-screen-apps',
											'terminal/terminal/more-features/notifications',
											'terminal/terminal/more-features/audible-bell',
											'terminal/terminal/more-features/settings-sync',
											'terminal/terminal/more-features/quit-warning',
											'terminal/terminal/more-features/uri-scheme',
											'terminal/terminal/more-features/linux',
										],
									},
									'terminal/terminal/command-palette',
									{
										label: 'Comparisons',
										items: [
											{ slug: 'terminal/terminal/comparisons', label: 'Overview' },
											'terminal/terminal/comparisons/performance',
										],
									},
									'terminal/terminal/comparisons/terminal-features',
									'terminal/terminal/integrations-and-plugins',
								],
							},
							{
								label: 'Code',
								items: [
									'terminal/code/overview',
									{
										label: 'Code Editor',
										items: [
											{ slug: 'terminal/code/code-editor', label: 'Overview' },
											'terminal/code/code-editor/language-server-protocol',
											'terminal/code/code-editor/file-tree',
											'terminal/code/code-editor/find-and-replace',
											'terminal/code/code-editor/code-editor-vim-keybindings',
										],
									},
									'terminal/code/code-review',
									'terminal/code/git-worktrees',
									'terminal/code/ssh-feature-support',
								],
							},
							{
								label: 'Knowledge & Collaboration',
								items: [
									{
										label: 'Warp Drive',
										items: [
											{ slug: 'terminal/knowledge-and-collaboration/warp-drive', label: 'Overview' },
											'terminal/knowledge-and-collaboration/warp-drive/notebooks',
											'terminal/knowledge-and-collaboration/warp-drive/workflows',
											'terminal/knowledge-and-collaboration/warp-drive/prompts',
											'terminal/knowledge-and-collaboration/warp-drive/environment-variables',
											'terminal/knowledge-and-collaboration/warp-drive/ai-objects',
											'terminal/knowledge-and-collaboration/warp-drive/web',
											'terminal/knowledge-and-collaboration/warp-drive/agent-mode-context',
										],
									},
									'terminal/knowledge-and-collaboration/teams',
									'terminal/knowledge-and-collaboration/admin-panel',
									{ slug: 'terminal/knowledge-and-collaboration/session-sharing', label: 'Session Sharing' },
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
