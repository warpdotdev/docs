import type { Plugin } from 'vite';
import { VARS } from '../data/vars.js';

/**
 * Vite transform plugin that replaces `{{TOKEN}}` placeholders in .mdx files
 * with values from src/data/vars.ts before any parser sees the content.
 *
 * Use `{{TOKEN}}` syntax only in frontmatter YAML (title, description,
 * sidebar.label, etc.). For MDX body prose, import VARS directly instead:
 *   import { VARS } from '@data/vars';
 *   ...{VARS.WARP_AGENT_CLI}...
 *
 * If any `{{...}}` tokens remain unresolved after substitution, the build
 * fails with the file path and unresolved token name to catch typos early.
 */
export function varsTransformPlugin(): Plugin {
  return {
    name: 'warp-vars-transform',
    transform(code, id) {
      if (!id.endsWith('.mdx')) return null;
      let result = code;
      for (const [key, value] of Object.entries(VARS)) {
        result = result.replaceAll(`{{${key}}}`, value as string);
      }
      // Validate only the frontmatter block for unresolved tokens.
      // Body prose may legitimately contain {{...}} patterns as code examples
      // (e.g., showing secret references), so we only enforce resolution in
      // the YAML frontmatter where {{TOKEN}} substitution is actually intended.
      const frontmatterMatch = result.match(/^---\n([\s\S]*?)\n---/);
      if (frontmatterMatch) {
        const frontmatter = frontmatterMatch[1];
        const unresolved = frontmatter.match(/\{\{[A-Z_]+\}\}/g);
        if (unresolved) {
          throw new Error(
            `[warp-vars-transform] Unresolved variable token(s) in frontmatter of ${id}: ${unresolved.join(', ')}`
          );
        }
      }
      return result;
    },
  };
}
