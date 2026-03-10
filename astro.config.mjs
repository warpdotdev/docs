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
				]),
			],
		}),
	],
	adapter: vercel(),
});
