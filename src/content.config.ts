import { defineCollection } from 'astro:content';
import { docsLoader } from '@astrojs/starlight/loaders';
import { docsSchema } from '@astrojs/starlight/schema';
import { topicSchema } from 'starlight-sidebar-topics/schema';
import { z } from 'astro/zod';

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
		schema: docsSchema({
			extend: (context) => {
				const topic = typeof topicSchema === 'function' ? topicSchema(context) : topicSchema;
				return topic.merge(
					z.object({
						tags: z.array(z.string()).optional(),
						featured: z.boolean().optional().default(false),
					}),
				);
			},
		}),
	}),
};
