import { VARS } from '../data/vars.js';

interface MdastNode {
	type: string;
	value?: string;
	children?: MdastNode[];
}

function resolveHeadingVars(node: MdastNode, filePath: string, inHeading = false): MdastNode {
	const isInHeading = inHeading || node.type === 'heading';
	if (isInHeading && node.type === 'mdxTextExpression') {
		const match = node.value?.match(/^\s*VARS\.([A-Z0-9_]+)\s*$/);
		if (!match) {
			throw new Error(
				`Unsupported MDX expression in heading in ${filePath}: {${node.value ?? ''}}. ` +
					'Use a bare {VARS.KEY} expression.',
			);
		}

		const key = match[1] as keyof typeof VARS;
		const value = VARS[key];
		if (value === undefined) {
			throw new Error(`Unknown content variable in heading: VARS.${key}`);
		}

		return { type: 'text', value };
	}

	if (node.children) {
		node.children = node.children.map((child) =>
			resolveHeadingVars(child, filePath, isInHeading),
		);
	}

	return node;
}

/**
 * Resolve bare `{VARS.KEY}` expressions anywhere under a heading before
 * Starlight extracts table-of-contents labels and anchor slugs.
 */
export default function remarkHeadingVars() {
	return (tree: MdastNode, file: { path?: string }) => {
		resolveHeadingVars(tree, file.path ?? 'unknown file');
	};
}
