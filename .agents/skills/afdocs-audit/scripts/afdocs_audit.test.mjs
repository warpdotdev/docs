import assert from 'node:assert/strict';
import test from 'node:test';

import { buildReport } from './afdocs_audit.mjs';

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
