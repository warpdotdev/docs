import { defineCollection } from 'astro:content';
import { docsLoader } from '@astrojs/starlight/loaders';
import { docsSchema } from '@astrojs/starlight/schema';
import { topicSchema } from 'starlight-sidebar-topics/schema';

export const collections = {
	// `topicSchema` adds a `topic` frontmatter field used by
	// `starlight-sidebar-topics` to associate unlisted pages with a topic ID.
	// See guides/agent-workflows/warp-vs-claude-code.mdx for an example.
	docs: defineCollection({ loader: docsLoader(), schema: docsSchema({ extend: topicSchema }) }),
};
