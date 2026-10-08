import { VARS } from '../data/vars.js';

interface MdastNode {
	type: string;
	value?: string;
	children?: MdastNode[];
}

function resolveHeadingVars(node: MdastNode): void {
	if (node.type === 'heading' && node.children) {
		node.children = node.children.map((child) => {
			if (child.type !== 'mdxTextExpression' || child.value === undefined) {
				return child;
			}

			const match = child.value.match(/^\s*VARS\.([A-Z_]+)\s*$/);
			if (!match) {
				return child;
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
		resolveHeadingVars(child);
	}
}

export default function remarkHeadingVars() {
	return (tree: MdastNode) => resolveHeadingVars(tree);
}
