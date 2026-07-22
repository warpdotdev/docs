import type { Plugin } from 'vite';
import { VARS } from '../data/vars.js';

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

      let frontmatter = match[1];
      const body = match[2];

      for (const [key, value] of Object.entries(VARS)) {
        frontmatter = frontmatter.replaceAll(`{{${key}}}`, value as string);
      }

      // Fail the build if any {{TOKEN}} patterns remain unresolved in frontmatter.
      const unresolved = frontmatter.match(/\{\{[A-Z_]+\}\}/g);
      if (unresolved) {
        throw new Error(
          `[warp-vars-transform] Unresolved variable token(s) in frontmatter of ${id}: ${unresolved.join(', ')}`
        );
      }

      return frontmatter + body;
    },
  };
}
