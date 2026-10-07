import assert from 'node:assert/strict';
import test from 'node:test';

import {
	assessBotProtection,
	assessEmbeddedDataSerialization,
	assessMarkdownLinkPortability,
	assessSingleFetchCompleteness,
	buildReport,
	bulkElements,
	extractContinuation,
} from './afdocs_audit.mjs';

const legacyResult = {
	id: 'page-size-html',
	category: 'page-size',
	status: 'fail',
	message: 'Converted content is too large',
};

test('creates a transparent v0.6 compatibility report when the CLI has 23 checks', () => {
	const report = buildReport(
		{
			url: 'https://docs.example.com',
			score: 80,
			summary: {},
			results: [
				legacyResult,
				{
					id: 'page-size-markdown',
					category: 'page-size',
					status: 'fail',
					message: 'Markdown is too large',
				},
				{
					id: 'markdown-content-parity',
					category: 'observability',
					status: 'fail',
					message: 'Markdown differs from HTML',
				},
			],
		},
		[
			{
				id: 'page-size-transfer',
				category: 'page-size',
				status: 'warn',
				message: 'Large transfer',
			},
			{
				id: 'embedded-data-serialization',
				category: 'content-structure',
				status: 'fail',
				message: 'Bulk table dominates page content',
			},
			{
				id: 'bot-protection-interference',
				category: 'authentication',
				status: 'warn',
				message: 'Sustained fetches are throttled',
			},
		]
	);

	assert.equal(report.spec_version, '0.6.0');
	assert.equal(report.total_checks, 6);
	assert.equal(report.legacy_cli_score, 80);
	assert.match(report.score_method, /compatibility estimate/);
	assert.equal(report.summary.fail, 4);
	assert.equal(report.summary.warn, 2);
	assert.equal(report.scan_reliability.status, 'partial');
	assert.deepEqual(
		report.interaction_effects.map((effect) => effect.id),
		['bot-protection-degrading-scan-reliability', 'dynamic-content-rendered-statically']
	);
});


function response(overrides = {}) {
	return {
		url: 'https://docs.example.com/page.md',
		status: 200,
		headers: { 'content-type': 'text/markdown' },
		body: 'Documentation content',
		bytes: 128,
		timeout: false,
		...overrides,
	};
}
test('uses the native CLI score after afdocs supplies every v0.6 check', () => {
	const report = buildReport({
		url: 'https://docs.example.com',
		score: 91,
		summary: {},
		results: [legacyResult],
	});

	assert.equal(report.score, 91);
	assert.equal(report.legacy_cli_score, null);
	assert.equal(report.score_method, 'native afdocs CLI score');
});

test('treats a valid Link-header continuation as visible at the start of the response', async () => {
	const headers = { link: '<https://docs.example.com/page.md?cursor=next>; rel="next"' };
	assert.deepEqual(extractContinuation('First page', headers), [
		{
			href: 'https://docs.example.com/page.md?cursor=next',
			position: 0,
			source: 'Link header',
		},
	]);

	const result = await assessSingleFetchCompleteness(
		[{ markdown: response({ headers, body: 'First page' }) }],
		async () => response({ body: 'Second page' })
	);
	assert.equal(result.status, 'pass');
});

test('detects a bot challenge during a sustained scan', () => {
	const result = assessBotProtection([
		{
			html: response({
				headers: { 'cf-mitigated': 'challenge' },
				body: 'Verifying your browser',
			}),
			markdown: response(),
		},
		{
			html: response(),
			markdown: response(),
		},
	]);

	assert.equal(result.status, 'warn');
	assert.match(result.message, /challenge page/);
});

test('fails markdown links that return HTML instead of the promised markdown representation', async () => {
	const result = await assessMarkdownLinkPortability(
		[
			{
				markdown: response({
					body: '[Reference](https://docs.example.com/reference.md)',
				}),
			},
		],
		async () => response({ headers: { 'content-type': 'text/html' }, body: '<h1>Not Found</h1>' })
	);

	assert.equal(result.status, 'fail');
	assert.equal(result.details.broken_markdown_links.length, 1);
});

test('attributes rendered data code blocks and ignores challenge pages', () => {
	const largeJson = JSON.stringify({ records: 'x'.repeat(101_000) });
	const validHtml = `<p>Reference data</p><pre><code class="language-json">${largeJson}</code></pre>`;
	const challengeHtml = `<table>${'<tr><td>challenge</td></tr>'.repeat(100)}</table>`;

	assert.deepEqual(bulkElements(validHtml).elements[0].type, 'data code block');

	const result = assessEmbeddedDataSerialization([
		{
			html: response({ url: 'https://docs.example.com/reference/', body: validHtml }),
		},
		{
			html: response({
				url: 'https://docs.example.com/blocked/',
				headers: { 'cf-mitigated': 'challenge' },
				body: challengeHtml,
			}),
		},
	]);

	assert.equal(result.status, 'fail');
	assert.deepEqual(
		result.details.dominant_pages.map((page) => page.url),
		['https://docs.example.com/reference/']
	);
});
