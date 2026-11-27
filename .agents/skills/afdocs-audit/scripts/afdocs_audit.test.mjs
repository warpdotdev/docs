import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { mkdtempSync, readFileSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import test from 'node:test';
import { fileURLToPath } from 'node:url';

import {
	assessBotProtection,
	assessEmbeddedDataSerialization,
	assessMarkdownLinkPortability,
	assessSingleFetchCompleteness,
	buildReport,
	bulkElements,
	extractContinuation,
	probeNonHtmlSpecs,
	toMarkdownUrl,
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

function runCli(t, { compatibility = false, partial = false, blocked = false, specStatus = null } = {}) {
	const directory = mkdtempSync(join(tmpdir(), 'afdocs-cli-'));
	t.after(() => rmSync(directory, { recursive: true, force: true }));
	const output = join(directory, 'report.json');
	const raw = {
		url: 'https://docs.example.com',
		score: 91,
		results: [
			'bot-protection-interference',
			'page-size-transfer',
			'single-fetch-completeness',
			'markdown-link-portability',
			...(compatibility ? [] : ['embedded-data-serialization']),
		].map((id) => ({
			id, category: 'content-structure', status: 'pass', message: 'Passed',
			details: { fetchErrors: partial ? 1 : 0 },
		})),
	};
	if (specStatus !== null) raw.results.push(specMissingMarkdown());
	const preload = `
		import childProcess from 'node:child_process';
		import { syncBuiltinESMExports } from 'node:module';
		childProcess.execFileSync = () => {
			if (${blocked}) throw new Error('The CLI must not run after a firewall challenge');
			return ${JSON.stringify(JSON.stringify(raw))};
		};
		syncBuiltinESMExports();
		globalThis.fetch = async (url) => {
			const path = new URL(url).pathname;
			if (path === '/llms.txt') return new Response('Documentation index', {
				status: ${blocked ? 429 : 200},
				headers: ${JSON.stringify(blocked ? { 'x-vercel-mitigated': 'challenge' } : {})},
			});
			if (path === '/openapi.yaml') {
				if (${specStatus} === 0) throw new Error('fetch failed');
				return new Response('openapi: 3.1.0', {
					status: ${specStatus ?? 200},
					headers: { 'content-type': 'application/yaml' },
				});
			}
			const bodies = {
				'/sitemap-index.xml': '<urlset><url><loc>https://docs.example.com/page/</loc></url></urlset>',
				'/page/': '<main><p>Reference content</p></main>',
				'/page.md': '# Reference content',
			};
			if (!(path in bodies)) throw new Error('Unexpected fetch: ' + url);
			const response = new Response(bodies[path], {
				headers: { 'content-type': path.endsWith('.md') ? 'text/markdown' : 'text/html' },
			});
			Object.defineProperty(response, 'url', { value: String(url) });
			return response;
		};
	`;
	const result = spawnSync(process.execPath, [
		'--import', `data:text/javascript,${encodeURIComponent(preload)}`,
		fileURLToPath(new URL('./afdocs_audit.mjs', import.meta.url)),
		'--url', raw.url, '--output', output,
	], { encoding: 'utf8', timeout: 10_000 });
	assert.equal(result.error, undefined);
	assert.equal(result.status, blocked ? 2 : 0, result.stderr);
	return { ...result, report: JSON.parse(readFileSync(output, 'utf8')) };
}

test('CLI prints native score provenance and complete scan reliability', (t) => {
	const { stdout, report } = runCli(t);
	assert.match(stdout, /Spec: v0\.6\.0\n/);
	assert.ok(stdout.includes(`Score method: ${report.score_method}`));
	assert.match(stdout, /Score: 91\/100/);
	assert.match(stdout, /Reliability: complete/);
	assert.doesNotMatch(stdout, /compatibility audit|Legacy 23-check CLI score:/);
});

test('CLI identifies compatibility estimates separately from the legacy score', (t) => {
	const { stdout, report } = runCli(t, { compatibility: true });
	assert.match(report.score_method, /compatibility estimate/);
	assert.ok(stdout.includes(`Score method: ${report.score_method}`));
	assert.match(stdout, /Legacy 23-check CLI score: 91\/100/);
	assert.match(stdout, /Reliability: complete/);
});

test('CLI preserves partial-scan warnings and suppresses firewall-blocked scores', (t) => {
	const partial = runCli(t, { partial: true });
	assert.equal(partial.report.scan_reliability.status, 'partial');
	assert.match(partial.stdout, /Reliability: partial/);
	assert.doesNotMatch(partial.stdout, /All checks passed/);
	const blocked = runCli(t, { blocked: true });
	assert.equal(blocked.report.status, 'invalid');
	assert.equal(blocked.report.score, undefined);
	assert.doesNotMatch(blocked.stdout, /Score:/);
	assert.match(blocked.stderr, /audit INVALID/);
});

test('does not label an estimated score as native when the CLI omits its score', () => {
	const report = buildReport({
		results: [{ ...legacyResult, status: 'warn' }],
	});
	assert.equal(report.score, 50);
	assert.match(report.score_method, /compatibility estimate/);
	assert.equal(report.legacy_cli_score, null);
});

test('retains page-level diagnostics and excludes fetch-interrupted scans from complete baselines', () => {
	const result = {
		id: 'markdown-content-parity',
		category: 'observability',
		status: 'pass',
		message: 'Compared available pages; one failed to fetch',
		details: {
			fetchErrors: 1,
			rateLimited: 0,
			pageResults: [{ url: 'https://docs.example.com/page/', status: 'pass' }],
		},
	};
	const report = buildReport({ score: 90, results: [result] });

	assert.equal(report.score, 90);
	assert.equal(report.scan_reliability.status, 'partial');
	assert.deepEqual(report.scan_reliability.affected_checks, [result.id]);
	assert.deepEqual(report.all_results[0].details, result.details);

	const warning = buildReport({ score: 90, results: [{ ...result, status: 'warn' }] });
	assert.deepEqual(warning.issues[0].details, result.details);
});

test('treats rate limiting and discovery warnings as partial without interpreting intentional 404 tests as fetch errors', () => {
	for (const details of [{ rateLimited: 1 }, { discoveryWarnings: ['Sitemap fetch failed'] }]) {
		const report = buildReport({ score: 90, results: [{ ...legacyResult, details }] });
		assert.equal(report.scan_reliability.status, 'partial');
	}

	const report = buildReport({
		score: 90,
		results: [{
			...legacyResult,
			details: {
				fetchErrors: 0, rateLimited: 0, discoveryWarnings: [],
				pageResults: [{ url: 'https://docs.example.com/nonexistent/', status: 404 }],
			},
		}],
	});
	assert.equal(report.scan_reliability.status, 'complete');
});

test('does not mark a scan partial when missing markdown is independently verified as a non-HTML spec', async () => {
	const raw = {
		score: 90,
		results: [{
			id: 'llms-txt-directive-md',
			category: 'content-discoverability',
			status: 'pass',
			message: 'llms.txt directive found in markdown of all 49 sampled pages; 1 had no markdown version',
			details: {
				fetchErrors: 1,
				rateLimited: 0,
				pageResults: [
					{ url: 'https://docs.warp.dev/agents/capabilities/', found: true },
					{ url: 'https://docs.warp.dev/openapi.yaml', found: false, error: 'No markdown version available' },
				],
			},
		}],
	};
	const probes = await probeNonHtmlSpecs(raw.results, async () =>
		response({ headers: { 'content-type': 'application/yaml' }, body: 'openapi: 3.1.0' })
	);
	const nonHtmlOnly = buildReport(raw, [], probes);
	assert.equal(nonHtmlOnly.scan_reliability.status, 'complete');

	const htmlMissingMd = buildReport({
		score: 90,
		results: [{
			id: 'llms-txt-directive-md',
			category: 'content-discoverability',
			status: 'pass',
			message: '1 HTML doc page had no markdown version',
			details: {
				fetchErrors: 1,
				rateLimited: 0,
				pageResults: [
					{ url: 'https://docs.warp.dev/agents/capabilities/', found: false, error: 'No markdown version available' },
				],
			},
		}],
	});
	assert.equal(htmlMissingMd.scan_reliability.status, 'partial');

	const networkErrorOnSpec = buildReport({
		score: 90,
		results: [{
			id: 'llms-txt-directive-md',
			category: 'content-discoverability',
			status: 'pass',
			message: 'Network error fetching spec',
			details: {
				fetchErrors: 1,
				rateLimited: 0,
				pageResults: [
					{ url: 'https://docs.warp.dev/openapi.yaml', found: false, error: 'fetch failed' },
				],
			},
		}],
	});
	assert.equal(networkErrorOnSpec.scan_reliability.status, 'partial');
});

// afdocs 0.23.0 uses this error for both absent Markdown and failed requests,
// including when the other sampled HTML pages succeed.
function specMissingMarkdown(url = 'https://docs.example.com/openapi.yaml') {
	return {
		id: 'llms-txt-directive-md',
		category: 'content-discoverability',
		status: 'pass',
		message: 'llms.txt directive found in tested pages; 1 had no markdown version',
		details: {
			fetchErrors: 1,
			pageResults: [
				{ url: 'https://docs.example.com/page/', found: true },
				{ url, found: false, error: 'No markdown version available' },
			],
		},
	};
}

test('CLI probes canonical specs before discounting upstream-shaped errors', (t) => {
	const healthy = runCli(t, { specStatus: 200 });
	assert.equal(healthy.report.scan_reliability.status, 'complete');
	assert.equal(healthy.report.non_html_spec_probes[0].verified, true);
	for (const specStatus of [0, 404, 503]) {
		const failed = runCli(t, { specStatus });
		assert.equal(failed.report.scan_reliability.status, 'partial');
		assert.equal(failed.report.non_html_spec_probes[0].verified, false);
		assert.match(failed.stdout, /Reliability: partial/);
	}
});

test('upstream-shaped spec errors remain partial without positive evidence', () => {
	const result = specMissingMarkdown();
	const report = buildReport({ results: [result] });
	assert.equal(report.scan_reliability.status, 'partial');
	assert.deepEqual(report.all_results[0].details, result.details);
});

test('canonical probes verify supported non-HTML representations and retain evidence', async () => {
	for (const [extension, contentType, body] of [
		['yaml', 'application/yaml', 'openapi: 3.1.0'],
		['yml', 'text/plain; charset=utf-8', 'openapi: 3.1.0'],
		['json', 'application/json', '{"openapi":"3.1.0"}'],
		['xml', 'application/xml', '<spec/>'],
		['txt', 'text/plain', 'Documentation index'],
	]) {
		const url = `https://docs.example.com/spec.${extension}`;
		const raw = { results: [specMissingMarkdown(url)] };
		const requested = [];
		const probes = await probeNonHtmlSpecs(raw.results, async (target) => {
			requested.push(target);
			return response({ url, headers: { 'content-type': contentType }, body });
		});
		assert.deepEqual(requested, [url]);
		assert.equal(probes[0].verified, true);
		const report = buildReport(raw, [], probes);
		assert.equal(report.scan_reliability.status, 'complete');
		assert.deepEqual(report.non_html_spec_probes, probes);
		assert.equal(raw.results[0].details.fetchErrors, 1);
	}
});

test('ambiguous upstream errors stay partial on transport, HTTP, and representation failures', async () => {
	const raw = { results: [specMissingMarkdown()] };
	for (const overrides of [
		{ status: null, error: 'fetch failed', body: '' },
		{ status: null, timeout: true, body: '' },
		{ status: 404 },
		{ status: 429 },
		{ status: 503 },
		{ headers: { 'content-type': 'text/html' }, body: '<html>Error</html>' },
		{ headers: { 'content-type': 'text/plain' }, body: '<!doctype html><html>Error</html>' },
		{ headers: { 'content-type': 'text/plain' }, body: '404 Page not found' },
		{ headers: { 'content-type': 'application/yaml' }, body: '' },
		{ headers: { 'content-type': 'application/yaml', 'cf-mitigated': 'challenge' } },
	]) {
		const probes = await probeNonHtmlSpecs(raw.results, async () => response(overrides));
		assert.equal(probes[0].verified, false, JSON.stringify(overrides));
		assert.equal(buildReport(raw, [], probes).scan_reliability.status, 'partial');
	}
	const probes = await probeNonHtmlSpecs(raw.results, async () => { throw new Error('fetch failed'); });
	assert.equal(probes[0].error, 'fetch failed');
	assert.equal(buildReport(raw, [], probes).scan_reliability.status, 'partial');
});

test('verified specs do not hide HTML failures, unrelated checks, rate limits, or discovery warnings', async () => {
	const result = specMissingMarkdown();
	const probes = await probeNonHtmlSpecs([result], async () =>
		response({ headers: { 'content-type': 'application/yaml' }, body: 'openapi: 3.1.0' })
	);
	for (const overrides of [
		{ rateLimited: 1 },
		{ discoveryWarnings: ['Sitemap fetch failed'] },
		{ fetchErrors: 2, pageResults: [
			...result.details.pageResults,
			{ url: 'https://docs.example.com/other/', error: 'No markdown version available' },
		] },
	]) {
		const mixed = { ...result, details: { ...result.details, ...overrides } };
		assert.equal(buildReport({ results: [mixed] }, [], probes).scan_reliability.status, 'partial');
	}
	for (const other of [
		{ ...result, id: 'markdown-content-parity' },
		specMissingMarkdown('https://docs.example.com/other/'),
	]) {
		assert.deepEqual(await probeNonHtmlSpecs([other]), []);
		assert.equal(buildReport({ results: [other] }, [], probes).scan_reliability.status, 'partial');
	}
});

test('spec probes are deduplicated and bounded; unprobed failures remain partial', async () => {
	const results = Array.from({ length: 9 }, (_, i) => specMissingMarkdown(`https://docs.example.com/spec-${i}.yaml`));
	const requested = [];
	const probes = await probeNonHtmlSpecs([results[0], ...results], async (url) => {
		requested.push(url);
		return response({ headers: { 'content-type': 'application/yaml' }, body: 'openapi: 3.1.0' });
	});
	assert.equal(requested.length, 8);
	assert.equal(new Set(requested).size, 8);
	assert.equal(buildReport({ results }, [], probes).scan_reliability.status, 'partial');
});

test('compatibility sampler skips non-HTML spec assets and parameterized query endpoints', () => {
	assert.equal(toMarkdownUrl('https://docs.warp.dev/openapi.yaml'), null);
	assert.equal(toMarkdownUrl('https://docs.warp.dev/openapi.json'), null);
	assert.equal(toMarkdownUrl('https://docs.warp.dev/llms.txt'), null);
	assert.equal(toMarkdownUrl('https://docs.warp.dev/retrieve?q='), null);
	assert.equal(
		toMarkdownUrl('https://docs.warp.dev/agents/capabilities/'),
		'https://docs.warp.dev/agents/capabilities.md'
	);
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
