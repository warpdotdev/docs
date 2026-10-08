import type { Plugin } from 'vite';
import { VARS } from '../data/vars.js';

/**
 * Replaces every `{{TOKEN}}` placeholder in `text` with its value from
 * `src/data/vars.ts`. Throws when a `{{...}}`-shaped token remains
 * unresolved afterward, naming the offending token(s) and `context`
 * (typically a file path) so a typo'd key fails the build loudly instead
 * of shipping literally.
 */
export function substituteVars(text: string, context: string): string {
	let result = text;
	for (const [key, value] of Object.entries(VARS)) {
		result = result.replaceAll(`{{${key}}}`, value as string);
	}

	const unresolved = result.match(/\{\{[A-Z_]+\}\}/g);
	if (unresolved) {
		throw new Error(`Unresolved variable token(s) in ${context}: ${unresolved.join(', ')}`);
	}

	return result;
}

/**
 * Vite transform plugin that replaces `{{TOKEN}}` placeholders in .mdx
 * frontmatter with values from src/data/vars.ts before any parser sees
 * the content.
 *
 * IMPORTANT: substitution is restricted to the frontmatter block only
 * (the content between the opening and closing `---` delimiters). Body
 * prose and code fences are left untouched, so authors can document or
 * example the `{{TOKEN}}` syntax without it being silently rewritten.
 *
 * Use `{{TOKEN}}` only in frontmatter YAML (title, description, sidebar.label).
 * For MDX body prose, import VARS directly instead:
 *   import { VARS } from '@data/vars';
 *   ...{VARS.WARP_AGENT_CLI}...
 *
 * NOTE: Starlight's `docs` collection loads frontmatter through Astro's
 * content-layer `glob()` loader, which parses each file directly and never
 * passes it through this Vite `transform` hook. That means this plugin
 * alone does NOT substitute `{{TOKEN}}` in `docs` collection frontmatter
 * (title/description/sidebar.label) — see the schema-level transform in
 * `src/content.config.ts`, which is what actually resolves those fields.
 * This plugin still covers any other `.mdx` frontmatter Vite transforms
 * directly (outside the content-layer loader).
 *
 * If any `{{...}}` tokens remain unresolved in the frontmatter after
 * substitution, the build fails with the file path and token name.
 */
export function varsTransformPlugin(): Plugin {
  return {
    name: 'warp-vars-transform',
    transform(code, id) {
      if (!id.endsWith('.mdx')) return null;

      // Isolate the frontmatter block (between the opening and closing ---).
      // Body prose and code fences are captured in `body` and passed through
      // unchanged so {{TOKEN}} examples in documentation are not rewritten.
      const frontmatterRegex = /^(---\n[\s\S]*?\n---)(\n?[\s\S]*)$/;
      const match = code.match(frontmatterRegex);
      if (!match) return null; // No frontmatter — nothing to substitute.

			const frontmatter = substituteVars(match[1], `frontmatter of ${id}`);
			const body = match[2];

			return frontmatter + body;
    },
  };
}
