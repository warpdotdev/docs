// Keep the transform core in plain JavaScript so node:test can run it without transpilation.
import { VARS } from '../data/vars.js';
import { resolveHeadingVars } from './heading-vars-core.mjs';
import type { MdastNode } from './heading-vars-core.mjs';

/**
 * Resolve bare `{VARS.KEY}` expressions anywhere under a heading before
 * Starlight extracts table-of-contents labels and anchor slugs.
 */
export default function remarkHeadingVars() {
	return (tree: MdastNode, file: { path?: string }) => {
		resolveHeadingVars(tree, VARS, file.path ?? 'unknown file');
	};
}
