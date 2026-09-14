#!/usr/bin/env node
/**
 * AFDocs audit wrapper script.
 *
 * Runs `npx afdocs check` against docs.warp.dev, parses the JSON output,
 * and produces a structured report with scores, issues, and fix guidance.
 *
 * Usage:
 *   node .agents/skills/afdocs-audit/scripts/afdocs_audit.mjs
 *   node .agents/skills/afdocs-audit/scripts/afdocs_audit.mjs --output /tmp/report.json
 *   node .agents/skills/afdocs-audit/scripts/afdocs_audit.mjs --url https://preview.docs.warp.dev
 */

import { execFileSync } from 'node:child_process';
import { writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { pathToFileURL } from 'node:url';

const SPEC_VERSION = '0.6.0';
const COMPATIBILITY_SAMPLE_LIMIT = 8;
const REQUEST_TIMEOUT_MS = 10_000;
const V06_CHECK_IDS = new Set([
	'bot-protection-interference',
	'page-size-transfer',
	'single-fetch-completeness',
	'markdown-link-portability',
	'embedded-data-serialization',
]);

const GRADE_THRESHOLDS = [
	[97, 'A+'],
	[93, 'A'],
	[90, 'A-'],
	[87, 'B+'],
	[83, 'B'],
	[80, 'B-'],
	[77, 'C+'],
	[73, 'C'],
	[70, 'C-'],
	[67, 'D+'],
	[63, 'D'],
	[60, 'D-'],
	[0, 'F'],
];

function scoreToGrade(score) {
	for (const [threshold, grade] of GRADE_THRESHOLDS) {
		if (score >= threshold) return grade;
	}
	return 'F';
}

function parseArgs(argv) {
	const args = { output: null, url: 'https://docs.warp.dev' };
	for (let i = 0; i < argv.length; i++) {
		if (argv[i] === '--output') args.output = argv[++i];
		else if (argv[i] === '--url') args.url = argv[++i];
		else if (argv[i] === '--help' || argv[i] === '-h') {
			console.log('Usage: node afdocs_audit.mjs [--output FILE] [--url URL]');
			process.exit(0);
		}
	}
	return args;
}

/**
 * Detect whether the target site is behind a Vercel Firewall bot challenge
 * (Attack Challenge Mode or the Bot Protection managed ruleset in challenge
 * mode). When active, Vercel returns HTTP 429 with an `x-vercel-mitigated:
 * challenge` header and a `x-vercel-challenge-token` to every non-browser
 * client — including the `afdocs` crawler. The crawler cannot solve the
 * JavaScript challenge, so every page "fails" to fetch and the resulting
 * scorecard is meaningless (all checks become false positives).
 *
 * Detecting this up front lets us abort with a clear "audit invalid" status
 * instead of publishing a misleading score. The remediation is on the Vercel
 * side (see references/vercel-firewall-challenge.md), since the `afdocs` CLI
 * cannot send a bypass header.
 *
 * Returns `null` when no challenge is detected, or an object describing the
 * block when one is found. Network errors are treated as "not a challenge"
 * so an unrelated transient failure doesn't mask a real audit.
 */
async function detectVercelChallenge(url) {
	const probeUrl = new URL('/llms.txt', url).toString();
	let res;
	try {
		res = await fetch(probeUrl, {
			redirect: 'manual',
			headers: {
				// Mimic a browser UA; the Vercel challenge still fires for
				// non-browser clients even with a spoofed UA, so this only
				// avoids unrelated UA-based blocks.
				'user-agent':
					'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36',
			},
		});
	} catch {
		return null; // Network error — let the real audit surface the problem.
	}

	const mitigated = res.headers.get('x-vercel-mitigated');
	const challengeToken = res.headers.get('x-vercel-challenge-token');
	const isChallenge = mitigated === 'challenge' || challengeToken != null;

	if (!isChallenge) return null;

	return {
		probeUrl,
		status: res.status,
		mitigated: mitigated || null,
		server: res.headers.get('server') || null,
	};
}

function runAfdocsCheck(url) {
	// Validate URL to prevent shell injection
	try {
		const parsed = new URL(url);
		if (!['http:', 'https:'].includes(parsed.protocol)) {
			throw new Error(`Invalid protocol: ${parsed.protocol}`);
		}
	} catch (e) {
		throw new Error(`Invalid URL "${url}": ${e.message}`);
	}

	try {
		const stdout = execFileSync('npx', ['--yes', 'afdocs', 'check', url, '--format', 'json'], {
			encoding: 'utf8',
			maxBuffer: 10 * 1024 * 1024, // 10 MB — the JSON output can be large
			timeout: 300_000, // 5 minutes
			stdio: ['pipe', 'pipe', 'pipe'],
		});
		return JSON.parse(stdout);
	} catch (error) {
		// npx afdocs exits with code 1 when there are failures, but still
		// prints valid JSON to stdout. Try to parse it.
		if (error.stdout) {
			try {
				return JSON.parse(error.stdout);
			} catch {
				// Fall through to error
			}
		}
		throw new Error(`Failed to run afdocs check: ${error.message}`);
	}
}

function createResult(id, category, status, message, fix = null, details = null) {
	return { id, category, status, message, fix, details };
}

function statusSummary(results) {
	return results.reduce(
		(summary, result) => {
			summary[result.status] = (summary[result.status] || 0) + 1;
			return summary;
		},
		{ pass: 0, fail: 0, warn: 0, skip: 0 }
	);
}

function decodeHtmlEntities(value) {
	return value
		.replaceAll('&amp;', '&')
		.replaceAll('&lt;', '<')
		.replaceAll('&gt;', '>')
		.replaceAll('&quot;', '"')
		.replaceAll('&#39;', "'");
}

function htmlToText(html) {
	return decodeHtmlEntities(
		html
			.replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi, ' ')
			.replace(/<style\b[^>]*>[\s\S]*?<\/style>/gi, ' ')
			.replace(/<[^>]+>/g, ' ')
			.replace(/\s+/g, ' ')
			.trim()
	);
}

function isSoft404(response) {
	if (!response || response.status !== 200) return false;
	const text = htmlToText(response.body || '').slice(0, 4_000);
	return /\b(404|page not found|not found|does not exist)\b/i.test(text);
}

function isChallenge(response) {
	if (!response) return false;
	const mitigated = response.headers['x-vercel-mitigated'];
	const hasChallengeHeader =
		mitigated === 'challenge' ||
		response.headers['x-vercel-challenge-token'] != null ||
		response.headers['cf-mitigated'] === 'challenge';
	const hasChallengeBody =
		/(verifying (you are )?(human|browser)|just a moment|security checkpoint|captcha|attention required)/i.test(
			response.body || ''
		);
	return hasChallengeHeader || hasChallengeBody;
}

async function fetchResource(url, headers = {}) {
	const controller = new AbortController();
	const timeout = setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS);
	const startedAt = Date.now();

	try {
		const response = await fetch(url, {
			redirect: 'follow',
			headers: {
				'user-agent': 'afdocs-v06-compatibility-audit/1.0',
				...headers,
			},
			signal: controller.signal,
		});
		const bytes = new Uint8Array(await response.arrayBuffer());
		return {
			url: response.url,
			status: response.status,
			headers: Object.fromEntries(response.headers.entries()),
			body: new TextDecoder().decode(bytes),
			bytes: bytes.byteLength,
			duration_ms: Date.now() - startedAt,
			timeout: false,
		};
	} catch (error) {
		return {
			url,
			status: null,
			headers: {},
			body: '',
			bytes: 0,
			duration_ms: Date.now() - startedAt,
			timeout: error.name === 'AbortError',
			error: error.message,
		};
	} finally {
		clearTimeout(timeout);
	}
}

function extractMarkdownLinks(markdown) {
	const links = [];
	const pattern = /!?\[[^\]]*]\(\s*(?:<([^>]+)>|([^\s)]+))/g;
	let match;
	while ((match = pattern.exec(markdown)) !== null) {
		const href = (match[1] || match[2]).trim();
		if (href && !href.startsWith('#')) links.push(href);
	}
	return links;
}

function toMarkdownUrl(rawUrl) {
	const url = new URL(rawUrl);
	if (url.pathname.endsWith('.md') || url.pathname === '/') return null;
	url.pathname = `${url.pathname.replace(/\/$/, '')}.md`;
	return url.toString();
}

function toHtmlUrl(markdownUrl) {
	const url = new URL(markdownUrl);
	url.pathname = url.pathname.replace(/\.md$/, '/');
	return url.toString();
}

function markdownTargets(baseUrl, llmsResponse) {
	const origin = new URL(baseUrl).origin;
	const candidates = extractMarkdownLinks(llmsResponse?.body || '')
		.map((href) => {
			try {
				return new URL(href, llmsResponse.url).toString();
			} catch {
				return null;
			}
		})
		.filter((url) => url && new URL(url).origin === origin)
		.map(toMarkdownUrl)
		.filter(Boolean);

	return [...new Set(candidates)].slice(0, COMPATIBILITY_SAMPLE_LIMIT);
}

function urlsFromSitemap(xml) {
	return [...xml.matchAll(/<loc>([^<]+)<\/loc>/gi)].map((match) => decodeHtmlEntities(match[1].trim()));
}

async function sitemapMarkdownTargets(baseUrl) {
	const origin = new URL(baseUrl).origin;
	const index = await fetchResource(new URL('/sitemap-index.xml', baseUrl).toString(), {
		accept: 'application/xml, text/xml;q=0.9, */*;q=0.1',
	});
	if (index.status !== 200) return [];

	const sitemapUrls = urlsFromSitemap(index.body);
	const leafSitemaps = sitemapUrls.filter((url) => url.endsWith('.xml'));
	const pageUrls =
		leafSitemaps.length === 0
			? sitemapUrls
			: (
					await Promise.all(
						leafSitemaps.slice(0, 4).map((url) =>
							fetchResource(url, { accept: 'application/xml, text/xml;q=0.9, */*;q=0.1' })
						)
					)
				).flatMap((response) => (response.status === 200 ? urlsFromSitemap(response.body) : []));

	return [...new Set(pageUrls)]
		.filter((url) => {
			try {
				return new URL(url).origin === origin;
			} catch {
				return false;
			}
		})
		.map(toMarkdownUrl)
		.filter(Boolean)
		.slice(0, COMPATIBILITY_SAMPLE_LIMIT);
}

async function collectSamples(baseUrl) {
	const llmsResponse = await fetchResource(new URL('/llms.txt', baseUrl).toString(), {
		accept: 'text/plain, text/markdown;q=0.9, */*;q=0.1',
	});
	const sitemapTargets = await sitemapMarkdownTargets(baseUrl);
	const fallbackTargets = markdownTargets(baseUrl, llmsResponse);
	const targets = [...new Set([...sitemapTargets, ...fallbackTargets])].slice(
		0,
		COMPATIBILITY_SAMPLE_LIMIT
	);
	const samples = [];

	for (const markdownUrl of targets) {
		const htmlUrl = toHtmlUrl(markdownUrl);
		const html = await fetchResource(htmlUrl, { accept: 'text/html, */*;q=0.1' });
		const markdown = await fetchResource(markdownUrl, {
			accept: 'text/markdown, text/plain;q=0.9, */*;q=0.1',
		});
		samples.push({ html, markdown });
	}

	return { llmsResponse, samples };
}

function assessBotProtection(samples) {
	const observations = samples.flatMap((sample) => [sample.html, sample.markdown]);
	if (observations.length === 0) {
		return createResult(
			'bot-protection-interference',
			'authentication',
			'skip',
			'No first-party documentation samples were available to test sustained automated fetching'
		);
	}

	const blocked = observations.filter(
		(response) =>
			response.timeout ||
			isChallenge(response) ||
			[403, 429, 503].includes(response.status)
	);
	if (blocked.length === 0) {
		return createResult(
			'bot-protection-interference',
			'authentication',
			'pass',
			`No bot-protection interference observed across ${observations.length} sustained automated fetches`
		);
	}

	const status = blocked.length * 2 >= observations.length ? 'fail' : 'warn';
	const modes = [...new Set(blocked.map((response) => (response.timeout ? 'tarpit timeout' : isChallenge(response) ? 'challenge page' : `HTTP ${response.status}`)))];
	return createResult(
		'bot-protection-interference',
		'authentication',
		status,
		`${blocked.length}/${observations.length} sustained automated fetches showed bot-protection interference (${modes.join(', ')})`,
		'Exempt public documentation routes from behavioral bot enforcement. When limits are necessary, return an explicit 429 with Retry-After instead of challenge pages or stalled responses.',
		{ blocked_fetches: blocked.length, total_fetches: observations.length, modes }
	);
}

function assessTransferSize(samples) {
	const htmlSamples = samples.map((sample) => sample.html).filter((response) => response.status === 200);
	if (htmlSamples.length === 0) {
		return createResult(
			'page-size-transfer',
			'page-size',
			'skip',
			'No successful HTML responses were available to measure transfer size'
		);
	}

	const maxBytes = Math.max(...htmlSamples.map((response) => response.bytes));
	const status = maxBytes > 10 * 1024 * 1024 ? 'fail' : maxBytes >= 1024 * 1024 ? 'warn' : 'pass';
	return createResult(
		'page-size-transfer',
		'page-size',
		status,
		`Largest decoded HTML response was ${Math.round(maxBytes / 1024)} KB across ${htmlSamples.length} sampled pages`,
		status === 'pass'
			? null
			: 'Reduce inline framework serialization, embedded data, and duplicate content. HTML-path agents pay this transfer cost before conversion.'
	);
}

function extractContinuation(markdown, headers) {
	const signals = [];
	const linkHeader = headers.link || '';
	const headerMatch = linkHeader.match(/<([^>]+)>;\s*rel="?next"?/i);
	if (headerMatch) signals.push({ href: headerMatch[1], position: markdown.length, source: 'Link header' });

	const links = extractMarkdownLinks(markdown);
	for (const href of links) {
		if (/(?:[?&](?:page|offset|cursor)=|next)/i.test(href)) {
			signals.push({ href, position: markdown.indexOf(href), source: 'markdown link' });
		}
	}
	if (/\b\d+\s+of\s+\d+\b/i.test(markdown) && signals.length === 0) {
		signals.push({ href: null, position: markdown.search(/\b\d+\s+of\s+\d+\b/i), source: 'count marker' });
	}
	return signals;
}

async function assessSingleFetchCompleteness(samples) {
	const markdownSamples = samples
		.map((sample) => sample.markdown)
		.filter((response) => response.status === 200 && response.body.length > 0);
	if (markdownSamples.length === 0) {
		return createResult(
			'single-fetch-completeness',
			'page-size',
			'skip',
			'No successful markdown responses were available to inspect for pagination'
		);
	}

	const findings = [];
	for (const response of markdownSamples) {
		for (const continuation of extractContinuation(response.body, response.headers)) {
			if (!continuation.href) {
				findings.push({ status: 'fail', response, continuation, reason: 'pagination is declared without a continuation URL' });
				continue;
			}
			let target;
			try {
				target = new URL(continuation.href, response.url);
			} catch {
				findings.push({ status: 'fail', response, continuation, reason: 'continuation URL cannot be resolved' });
				continue;
			}
			const next = await fetchResource(target.toString(), {
				accept: 'text/markdown, text/plain;q=0.9, */*;q=0.1',
			});
			const absolute = /^https?:\/\//i.test(continuation.href);
			const nearTop = continuation.position >= 0 && continuation.position / response.body.length <= 0.1;
			const working =
				next.status >= 200 &&
				next.status < 300 &&
				next.body.trim().length > 0 &&
				!isChallenge(next) &&
				!isSoft404(next);
			findings.push({
				status: !working ? 'fail' : absolute && nearTop ? 'pass' : 'warn',
				response,
				continuation,
				reason: !working ? 'continuation does not return substantive content' : !absolute ? 'continuation URL is relative' : 'continuation is declared after the first 10% of content',
			});
		}
	}

	if (findings.length === 0) {
		return createResult(
			'single-fetch-completeness',
			'page-size',
			'pass',
			`No pagination signals detected across ${markdownSamples.length} sampled markdown responses`
		);
	}
	const status = findings.some((finding) => finding.status === 'fail')
		? 'fail'
		: findings.some((finding) => finding.status === 'warn')
			? 'warn'
			: 'pass';
	return createResult(
		'single-fetch-completeness',
		'page-size',
		status,
		`${findings.length} pagination signal(s) found; ${findings.filter((finding) => finding.status === 'fail').length} broken and ${findings.filter((finding) => finding.status === 'warn').length} fragile`,
		status === 'pass'
			? null
			: 'Serve complete markdown in one response where possible. Otherwise put an absolute, working continuation link near the top of the response.',
		{ findings: findings.map(({ status: findingStatus, reason, response }) => ({ status: findingStatus, reason, url: response.url })) }
	);
}

async function assessMarkdownLinkPortability(samples) {
	const markdownSamples = samples
		.map((sample) => sample.markdown)
		.filter((response) => response.status === 200 && response.body.length > 0);
	if (markdownSamples.length === 0) {
		return createResult(
			'markdown-link-portability',
			'content-structure',
			'skip',
			'No successful markdown responses were available to inspect links'
		);
	}

	const links = markdownSamples.flatMap((response) =>
		extractMarkdownLinks(response.body)
			.filter((href) => !/^(mailto:|tel:|data:)/i.test(href))
			.map((href) => ({ href, response }))
	);
	const pathRelative = links.filter(({ href }) => !/^(https?:\/\/|\/)/i.test(href));
	const rootRelative = links.filter(({ href }) => href.startsWith('/'));
	const markdownLinks = links.filter(({ href }) => /\.md(?:[?#]|$)/i.test(href)).slice(0, COMPATIBILITY_SAMPLE_LIMIT);
	const broken = [];

	for (const { href, response } of markdownLinks) {
		const target = new URL(href, response.url).toString();
		const resolved = await fetchResource(target, {
			accept: 'text/markdown, text/plain;q=0.9, */*;q=0.1',
		});
		const contentType = resolved.headers['content-type'] || '';
		if (
			resolved.status < 200 ||
			resolved.status >= 300 ||
			isSoft404(resolved) ||
			isChallenge(resolved) ||
			!/(text\/markdown|text\/plain)/i.test(contentType)
		) {
			broken.push({ href, url: target, status: resolved.status, content_type: contentType || null });
		}
	}

	const status = pathRelative.length > 0 || broken.length > 0 ? 'fail' : rootRelative.length > 0 ? 'warn' : 'pass';
	return createResult(
		'markdown-link-portability',
		'content-structure',
		status,
		`${links.length} markdown link(s): ${links.length - pathRelative.length - rootRelative.length} absolute, ${rootRelative.length} root-relative, ${pathRelative.length} path-relative; ${broken.length}/${markdownLinks.length} sampled .md link(s) failed representation verification`,
		status === 'pass'
			? null
			: 'Generate absolute URLs in served markdown. Fetch a representative sample in CI and verify both successful status and the promised markdown representation.',
		{ absolute: links.length - pathRelative.length - rootRelative.length, root_relative: rootRelative.length, path_relative: pathRelative.length, broken_markdown_links: broken }
	);
}

function bulkElements(html) {
	const content = htmlToText(html);
	const elements = [];
	for (const table of html.match(/<table\b[^>]*>[\s\S]*?<\/table>/gi) || []) {
		const rows = (table.match(/<tr\b/gi) || []).length;
		const text = htmlToText(table);
		if (rows >= 25) elements.push({ type: 'table', rows, characters: text.length });
	}
	for (const block of content.match(/```(?:json|ya?ml|csv)?[\s\S]{1024,}?```/gi) || []) {
		elements.push({ type: 'data block', characters: block.length });
	}
	for (const base64 of content.match(/[A-Za-z0-9+/]{1024,}={0,2}/g) || []) {
		elements.push({ type: 'base64 payload', characters: base64.length });
	}
	return { contentCharacters: content.length, elements };
}

function assessEmbeddedDataSerialization(samples) {
	const analyses = samples
		.map((sample) => ({ url: sample.html.url, ...bulkElements(sample.html.body) }))
		.filter((analysis) => analysis.contentCharacters > 0);
	if (analyses.length === 0) {
		return createResult(
			'embedded-data-serialization',
			'content-structure',
			'skip',
			'No successful HTML responses were available to inspect for embedded bulk data'
		);
	}

	const dominant = analyses
		.map((analysis) => ({
			...analysis,
			bulkCharacters: analysis.elements.reduce((total, element) => total + element.characters, 0),
		}))
		.filter((analysis) => analysis.bulkCharacters / analysis.contentCharacters > 0.5);
	const failing = dominant.filter((analysis) => analysis.contentCharacters > 100_000);
	const warning = dominant.filter((analysis) => analysis.contentCharacters >= 50_000 && analysis.contentCharacters <= 100_000);
	const status = failing.length > 0 ? 'fail' : warning.length > 0 ? 'warn' : 'pass';
	const maxBulkShare = Math.max(
		...analyses.map((analysis) => analysis.elements.reduce((total, element) => total + element.characters, 0) / analysis.contentCharacters)
	);
	return createResult(
		'embedded-data-serialization',
		'content-structure',
		status,
		`${dominant.length}/${analyses.length} sampled pages have bulk data as the dominant converted-content contributor (largest share ${Math.round(maxBulkShare * 100)}%)`,
		status === 'pass'
			? null
			: 'Split large generated tables into self-contained pages, load bulk payloads on demand, and place prose before bulk data. Do not replace complete pages with pagination windows.',
		{ dominant_pages: dominant.map(({ url, contentCharacters, bulkCharacters, elements }) => ({ url, content_characters: contentCharacters, bulk_characters: bulkCharacters, elements })) }
	);
}

function interactionEffects(results) {
	const resultFor = (id) => results.find((result) => result.id === id);
	const interactions = [];
	const botProtection = resultFor('bot-protection-interference');
	if (botProtection && ['warn', 'fail'].includes(botProtection.status)) {
		interactions.push({
			id: 'bot-protection-degrading-scan-reliability',
			status: 'observed',
			affected_checks: results
				.filter((result) => result.category !== 'authentication' && result.status !== 'skip')
				.map((result) => result.id),
			message: 'Bot protection interfered with sustained fetching, so multi-page findings may reflect a partial sample rather than the complete site.',
		});
	}

	const dynamicCheckIds = [
		'page-size-transfer',
		'single-fetch-completeness',
		'embedded-data-serialization',
		'markdown-content-parity',
		'page-size-markdown',
		'page-size-html',
	];
	const dynamicSignals = dynamicCheckIds.filter((id) => {
		const result = resultFor(id);
		return result && ['warn', 'fail'].includes(result.status);
	});
	if (dynamicSignals.length >= 2) {
		interactions.push({
			id: 'dynamic-content-rendered-statically',
			status: 'observed',
			affected_checks: dynamicSignals,
			message: 'Multiple dynamic-content failure signals co-occur. Review HTML and markdown rendering paths together: serialization payloads, static bulk-data output, parity, and pagination can fail independently.',
		});
	}
	return interactions;
}

function scanReliability(results) {
	const botProtection = results.find((result) => result.id === 'bot-protection-interference');
	if (botProtection && ['warn', 'fail'].includes(botProtection.status)) {
		return {
			status: 'partial',
			reason: 'bot-protection-interference',
			message: 'Sustained automated fetching was interrupted, so multi-page findings may not represent the complete site.',
		};
	}
	return {
		status: 'complete',
		reason: null,
		message: 'No bot-protection interference was observed during this scan.',
	};
}

export async function runV06CompatibilityChecks(baseUrl, existingResults = []) {
	const existingIds = new Set(existingResults.map((result) => result.id));
	const missingCheckIds = new Set(
		[...V06_CHECK_IDS].filter((checkId) => !existingIds.has(checkId))
	);
	if (missingCheckIds.size === 0) return { results: [], samples: [] };
	const { samples } = await collectSamples(baseUrl);
	const candidates = [
		assessBotProtection(samples),
		assessTransferSize(samples),
		await assessSingleFetchCompleteness(samples),
		await assessMarkdownLinkPortability(samples),
		assessEmbeddedDataSerialization(samples),
	];
	return {
		results: candidates.filter((result) => missingCheckIds.has(result.id)),
		samples,
	};
}

export function buildReport(raw, supplementalResults = []) {
	const results = [...raw.results, ...supplementalResults];
	const summary = statusSummary(results);
	const nativeCliScore = raw.summary?.score ?? raw.score ?? estimateScore(raw.results);
	const score = supplementalResults.length > 0 ? estimateScore(results) : nativeCliScore ?? estimateScore(results);
	const grade = scoreToGrade(score);

	// Group results by category
	const categories = {};
	for (const r of results) {
		if (!categories[r.category]) {
			categories[r.category] = { checks: [], pass: 0, fail: 0, warn: 0, skip: 0 };
		}
		categories[r.category].checks.push(r);
		categories[r.category][r.status] = (categories[r.category][r.status] || 0) + 1;
	}

	// Extract issues (fail + warn)
	const issues = results
		.filter((r) => r.status === 'fail' || r.status === 'warn')
		.map((r) => ({
			id: r.id,
			category: r.category,
			status: r.status,
			message: r.message,
			fix: r.details?.fix || r.fix || null,
		}));

	return {
		url: raw.url,
		timestamp: raw.timestamp || new Date().toISOString(),
		spec_version: SPEC_VERSION,
		score,
		grade,
		score_method:
			supplementalResults.length > 0
				? 'unweighted compatibility estimate; warnings count as half-passes'
				: 'native afdocs CLI score',
		legacy_cli_score: supplementalResults.length > 0 ? nativeCliScore : null,
		total_checks: results.length,
		summary,
		categories: Object.fromEntries(
			Object.entries(categories).map(([name, cat]) => [
				name,
				{ pass: cat.pass, fail: cat.fail, warn: cat.warn, skip: cat.skip },
			])
		),
		issues,
		all_results: results.map((r) => ({ id: r.id, category: r.category, status: r.status, message: r.message })),
		scan_reliability: scanReliability(results),
		interaction_effects: interactionEffects(results),
	};
}

/**
 * Estimate score from results when the raw JSON doesn't include a score field.
 * Uses a simple formula: (pass / (total - skip)) * 100.
 */
function estimateScore(results) {
	const scored = results.filter((r) => r.status !== 'skip');
	if (scored.length === 0) return 100;
	const passing = scored.filter((r) => r.status === 'pass').length;
	// Warnings count as half-pass
	const warnings = scored.filter((r) => r.status === 'warn').length;
	return Math.round(((passing + warnings * 0.5) / scored.length) * 100);
}

function printSummary(report) {
	console.log(`\nAFDocs Audit — ${report.url}`);
	console.log(`Spec: v${report.spec_version} compatibility audit`);
	console.log(`Score: ${report.score}/100 (${report.grade})`);
	if (report.legacy_cli_score != null) {
		console.log(`Legacy 23-check CLI score: ${report.legacy_cli_score}/100 (not comparable to the v0.6 score)`);
	}
	console.log(
		`Checks: ${report.total_checks} total | ${report.summary.pass} pass, ${report.summary.fail} fail, ${report.summary.warn} warn, ${report.summary.skip} skip`
	);
	if (report.scan_reliability.status !== 'complete') {
		console.log(`Reliability: ${report.scan_reliability.status} — ${report.scan_reliability.message}`);
	}

	if (report.issues.length === 0) {
		console.log('\n✅ All checks passed!');
		return;
	}

	const failures = report.issues.filter((i) => i.status === 'fail');
	const warnings = report.issues.filter((i) => i.status === 'warn');

	if (failures.length > 0) {
		console.log(`\nFailures (${failures.length}):`);
		for (const f of failures) {
			console.log(`  ✗ ${f.id}: ${f.message}`);
			if (f.fix) console.log(`    Fix: ${f.fix}`);
		}
	}

	if (warnings.length > 0) {
		console.log(`\nWarnings (${warnings.length}):`);
		for (const w of warnings) {
			console.log(`  ⚠ ${w.id}: ${w.message}`);
		}
	}

	if (report.interaction_effects.length > 0) {
		console.log('\nInteraction effects:');
		for (const effect of report.interaction_effects) {
			console.log(`  ⚠ ${effect.id}: ${effect.message}`);
		}
	}
}

async function main() {
	const args = parseArgs(process.argv.slice(2));

	// Preflight: if the site is behind a Vercel Firewall bot challenge, the
	// afdocs crawler can't reach any real content and every check becomes a false
	// positive. Bail out with a clear "invalid" status so we never publish a
	// misleading score.
	const challenge = await detectVercelChallenge(args.url);
	if (challenge) {
		const invalidReport = {
			url: args.url,
			timestamp: new Date().toISOString(),
			spec_version: SPEC_VERSION,
			status: 'invalid',
			reason: 'vercel-firewall-challenge',
			detail: challenge,
		};

		console.error(
			`\n⛔ AFDocs audit INVALID — ${args.url} is behind a Vercel Firewall bot challenge.`
		);
		console.error(
			`   Probe ${challenge.probeUrl} returned HTTP ${challenge.status}` +
				(challenge.mitigated ? ` (x-vercel-mitigated: ${challenge.mitigated})` : '') +
				'.'
		);
		console.error(
			'   The afdocs crawler cannot solve the JavaScript challenge, so a score cannot be computed.'
		);
		console.error(
			'   Fix: see .agents/skills/afdocs-audit/references/vercel-firewall-challenge.md'
		);

		if (args.output) {
			const outputPath = resolve(args.output);
			writeFileSync(outputPath, JSON.stringify(invalidReport, null, 2));
			console.error(`\nInvalid-audit report written to ${outputPath}`);
		}

		process.exitCode = 2;
		return;
	}

	console.log(`Running AFDocs check on ${args.url}...`);

	const raw = runAfdocsCheck(args.url);
	console.log(`Running ${SPEC_VERSION} compatibility checks on a bounded markdown sample...`);
	const { results: supplementalResults } = await runV06CompatibilityChecks(args.url, raw.results);
	const report = buildReport(raw, supplementalResults);

	printSummary(report);

	if (args.output) {
		const outputPath = resolve(args.output);
		writeFileSync(outputPath, JSON.stringify(report, null, 2));
		console.log(`\nReport written to ${outputPath}`);
	}
}

if (process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href) {
	await main();
}
