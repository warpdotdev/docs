import { defineCollection } from 'astro:content';
import { docsLoader } from '@astrojs/starlight/loaders';
import { docsSchema } from '@astrojs/starlight/schema';
import { topicSchema } from 'starlight-sidebar-topics/schema';
import { z } from 'astro/zod';
import { substituteVars } from './plugins/vars-transform.js';

export const collections = {
	// `topicSchema` adds a `topic` frontmatter field used by
	// `starlight-sidebar-topics` to associate unlisted pages with a topic ID.
	// See guides/agent-workflows/warp-vs-claude-code.mdx for an example.
	//
	// Custom fields added for the Guides card-based discovery page:
	// - `tags`: topic/task tags for filtering (e.g. ["mcp", "agents", "docker"])
	// - `featured`: marks guides for the curated "Featured" section
	docs: defineCollection({
		loader: docsLoader(),
		schema: (context) =>
			docsSchema({
				extend: topicSchema.merge(
					z.object({
						tags: z.array(z.string()).optional(),
						featured: z.boolean().optional().default(false),
					}),
				),
			})(context).transform((data) => {
				// Starlight's docs collection reads frontmatter through Astro's
				// content-layer glob() loader, which never runs the `warp-vars-transform`
				// Vite plugin (see src/plugins/vars-transform.ts). Substituting
				// `{{TOKEN}}` here, on the parsed schema data, is what actually
				// resolves those placeholders in title/description/sidebar.label.
				return {
					...data,
					title: substituteVars(data.title, `frontmatter title of ${data.title}`),
					description:
						data.description !== undefined
							? substituteVars(data.description, `frontmatter description of ${data.title}`)
							: data.description,
					sidebar:
						data.sidebar?.label !== undefined
							? { ...data.sidebar, label: substituteVars(data.sidebar.label, `frontmatter sidebar.label of ${data.title}`) }
							: data.sidebar,
				};
			}),
	}),
};
