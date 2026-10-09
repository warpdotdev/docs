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

test('rejects an unsupported nested expression with its source location', () => {
	const tree = {
		type: 'heading',
		children: [
			{
				type: 'emphasis',
				children: [
					{
						type: 'mdxTextExpression',
						value: 'VARS.AGENT_MODE.toUpperCase()',
						position: { start: { line: 7, column: 6 } },
					},
				],
			},
		],
	};

	assert.throws(
		() => resolveHeadingVars(tree, { AGENT_MODE: 'Agent Mode' }, 'unsupported.mdx'),
		/Unsupported MDX expression in heading at unsupported\.mdx:7:6/,
	);
});

test('rejects an MDX comment inside a heading', () => {
	const tree = {
		type: 'heading',
		children: [
			{
				type: 'mdxTextExpression',
				value: '/* a comment */',
				position: { start: { line: 12, column: 3 } },
			},
		],
	};

	assert.throws(
		() => resolveHeadingVars(tree, {}, 'comment.mdx'),
		/Use a bare \{VARS\.KEY\} expression, and move any MDX comment to its own line after the heading\./,
	);
});

test('rejects an unknown variable with its source location', () => {
	const tree = {
		type: 'heading',
		children: [
			{
				type: 'mdxTextExpression',
				value: 'VARS.MISSING',
				position: { start: { line: 4, column: 5 } },
			},
		],
	};

	assert.throws(
		() => resolveHeadingVars(tree, {}, 'unknown.mdx'),
		/Unknown content variable in heading at unknown\.mdx:4:5: VARS\.MISSING/,
	);
});

test('leaves expressions outside headings untouched', () => {
	const expression = { type: 'mdxTextExpression', value: 'VARS.AGENT_MODE' };
	const tree = {
		type: 'root',
		children: [{ type: 'paragraph', children: [expression] }],
	};

	resolveHeadingVars(tree, { AGENT_MODE: 'Agent Mode' }, 'body.mdx');

	assert.strictEqual(tree.children[0].children[0], expression);
});
