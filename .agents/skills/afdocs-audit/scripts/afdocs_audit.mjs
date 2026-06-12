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

import { execSync } from 'node:child_process';
import { writeFileSync } from 'node:fs';
import { resolve } from 'node:path';

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
	const isChallenge =
		mitigated === 'challenge' || challengeToken != null || res.status === 429;

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
		const stdout = execSync(`npx afdocs check ${url} --format json`, {
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

function buildReport(raw) {
	const { summary, results } = raw;
	const score = raw.summary?.score ?? estimateScore(results);
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
		score,
		grade,
		total_checks: summary.total,
		summary: {
			pass: summary.pass,
			fail: summary.fail,
			warn: summary.warn,
			skip: summary.skip,
		},
		categories: Object.fromEntries(
			Object.entries(categories).map(([name, cat]) => [
				name,
				{ pass: cat.pass, fail: cat.fail, warn: cat.warn, skip: cat.skip },
			])
		),
		issues,
		all_results: results.map((r) => ({ id: r.id, category: r.category, status: r.status, message: r.message })),
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
	console.log(`Score: ${report.score}/100 (${report.grade})`);
	console.log(
		`Checks: ${report.total_checks} total | ${report.summary.pass} pass, ${report.summary.fail} fail, ${report.summary.warn} warn, ${report.summary.skip} skip`
	);

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
}

// Main
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

	process.exit(2);
}

console.log(`Running AFDocs check on ${args.url}...`);

const raw = runAfdocsCheck(args.url);
const report = buildReport(raw);

printSummary(report);

if (args.output) {
	const outputPath = resolve(args.output);
	writeFileSync(outputPath, JSON.stringify(report, null, 2));
	console.log(`\nReport written to ${outputPath}`);
}
