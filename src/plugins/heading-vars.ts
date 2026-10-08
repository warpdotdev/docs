import { VARS } from '../data/vars.js';

interface MdastNode {
	type: string;
	value?: string;
	children?: MdastNode[];
}

function resolveHeadingVars(node: MdastNode, filePath: string): void {
	if (node.type === 'heading' && node.children) {
		node.children = node.children.map((child) => {
			if (child.type !== 'mdxTextExpression' || child.value === undefined) {
				return child;
			}
			const match = child.value.match(/^\s*VARS\.([A-Z0-9_]+)\s*$/);
			if (!match) {
				throw new Error(
					`Unsupported MDX expression in heading in ${filePath}: {${child.value}}. ` +
						'Use a bare {VARS.KEY} expression.',
				);
			}

			const key = match[1] as keyof typeof VARS;
			const value = VARS[key];
			if (value === undefined) {
				throw new Error(`Unknown content variable in heading: VARS.${key}`);
			}

			return { type: 'text', value };
		});
	}

	for (const child of node.children ?? []) {
		resolveHeadingVars(child, filePath);
	}
}

/**
 * Resolve bare `{VARS.KEY}` heading expressions before Starlight extracts
 * table-of-contents labels and anchor slugs.
 */
export default function remarkHeadingVars() {
	return (tree: MdastNode, file: { path?: string }) =>
		resolveHeadingVars(tree, file.path ?? 'unknown file');
}
