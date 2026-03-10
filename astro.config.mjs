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
                                  'agent-platform/capabilities/mcp',
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