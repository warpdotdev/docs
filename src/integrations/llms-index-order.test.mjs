import assert from 'node:assert/strict';
import test from 'node:test';
import { reorderLlmsIndex } from './llms-index-order.js';

test('small section sets come first and bundles move to Optional without losing links', () => {
	const full = '- [Complete documentation](https://docs.warp.dev/llms-full.txt)';
	const small = '- [Abridged documentation](https://docs.warp.dev/llms-small.txt)';
	const large = '- [Agents](https://docs.warp.dev/_llms-txt/agents.txt)';
	const compact = '- [Code](https://docs.warp.dev/_llms-txt/code.txt)';
	const input = ['# Warp', '## Documentation Sets', small, full, large, compact,
		'## Optional', '- [API](https://docs.warp.dev/openapi.json)', ''].join('\n');
	const output = reorderLlmsIndex(input, new Map([['agents.txt', 500000], ['code.txt', 50000]]));
	assert.ok(output.indexOf(compact) < output.indexOf(large));
	assert.ok(output.indexOf(full) > output.indexOf('## Optional'));
	assert.ok(output.indexOf(small) > output.indexOf('## Optional'));
	assert.deepEqual(output.match(/https:\/\/[^)]+/g).sort(), input.match(/https:\/\/[^)]+/g).sort());
});

test('an index without an Optional section gains one for the full bundles', () => {
	const output = reorderLlmsIndex('- [Complete documentation](https://docs.warp.dev/llms-full.txt)\n', new Map());
	assert.match(output, /## Optional\n\n- \[Complete documentation\]/);
});
