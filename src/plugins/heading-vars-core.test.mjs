import assert from 'node:assert/strict';
import test from 'node:test';
import { resolveHeadingVars } from './heading-vars-core.mjs';

test('resolves a variable nested in formatted heading content', () => {
	const tree = {
		type: 'root',
		children: [
			{
				type: 'heading',
				children: [
					{
						type: 'strong',
						children: [{ type: 'mdxTextExpression', value: 'VARS.AGENT_MODE' }],
					},
				],
			},
		],
	};

	resolveHeadingVars(tree, { AGENT_MODE: 'Agent Mode' }, 'nested.mdx');

	assert.deepEqual(tree.children[0].children[0].children, [
		{ type: 'text', value: 'Agent Mode' },
	]);
});

test('rejects an unsupported nested expression with its file path', () => {
	const tree = {
		type: 'heading',
		children: [
			{
				type: 'emphasis',
				children: [
					{ type: 'mdxTextExpression', value: 'VARS.AGENT_MODE.toUpperCase()' },
				],
			},
		],
	};

	assert.throws(
		() => resolveHeadingVars(tree, { AGENT_MODE: 'Agent Mode' }, 'unsupported.mdx'),
		/Unsupported MDX expression in heading in unsupported\.mdx/,
	);
});

test('rejects an MDX comment inside a heading', () => {
	const tree = {
		type: 'heading',
		children: [{ type: 'mdxTextExpression', value: '/* a comment */' }],
	};

	assert.throws(
		() => resolveHeadingVars(tree, {}, 'comment.mdx'),
		/Unsupported MDX expression in heading in comment\.mdx/,
	);
});

test('rejects an unknown variable with its file path', () => {
	const tree = {
		type: 'heading',
		children: [{ type: 'mdxTextExpression', value: 'VARS.MISSING' }],
	};

	assert.throws(
		() => resolveHeadingVars(tree, {}, 'unknown.mdx'),
		/Unknown content variable in heading in unknown\.mdx: VARS\.MISSING/,
	);
});
