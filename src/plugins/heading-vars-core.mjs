function nodeLocation(filePath, node) {
	const { line, column } = node.position?.start ?? {};
	return line && column ? `${filePath}:${line}:${column}` : filePath;
}
export function resolveHeadingVars(node, vars, filePath, inHeading = false) {
	const isInHeading = inHeading || node.type === 'heading';
	if (isInHeading && node.type === 'mdxTextExpression') {
		const location = nodeLocation(filePath, node);
		const match = node.value?.match(/^\s*VARS\.([A-Z0-9_]+)\s*$/);
		if (!match) {
			throw new Error(
				`Unsupported MDX expression in heading at ${location}: {${node.value ?? ''}}. ` +
					'Use a bare {VARS.KEY} expression.',
			);
		}

		const key = match[1];
		const value = vars[key];
		if (value === undefined) {
			throw new Error(`Unknown content variable in heading at ${location}: VARS.${key}`);
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
