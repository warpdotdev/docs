export function resolveHeadingVars(node, vars, filePath, inHeading = false) {
	const isInHeading = inHeading || node.type === 'heading';
	if (isInHeading && node.type === 'mdxTextExpression') {
		const match = node.value?.match(/^\s*VARS\.([A-Z0-9_]+)\s*$/);
		if (!match) {
			throw new Error(
				`Unsupported MDX expression in heading in ${filePath}: {${node.value ?? ''}}. ` +
					'Use a bare {VARS.KEY} expression.',
			);
		}

		const key = match[1];
		const value = vars[key];
		if (value === undefined) {
			throw new Error(`Unknown content variable in heading in ${filePath}: VARS.${key}`);
		}

		return { type: 'text', value };
	}

	if (node.children) {
		node.children = node.children.map((child) =>
			resolveHeadingVars(child, vars, filePath, isInHeading),
		);
	}

	return node;
}
