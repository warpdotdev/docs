#!/usr/bin/env node
/**
 * SEO audit script.
 *
 * Verifies that every page we ship to docs.warp.dev has the same SEO tags
 * the legacy GitBook docs emit today (title, description, canonical, robots,
 * Open Graph, Twitter, alternate markdown link, apple-touch-icon, etc).
 *
 * Usage:
 *   # Audit a built site on disk (run after `npm run build`)
 *   node scripts/seo-audit.mjs --dist ./dist
 *
 *   # Audit live URLs (handy for spot-checking the legacy GitBook output)
 *   node scripts/seo-audit.mjs --base https://docs.warp.dev /agent-platform/cloud-agents/oz-web-app /changelog
 *
 *   # Diff between two sources, e.g. legacy vs. our preview deploy
 *   node scripts/seo-audit.mjs \\
 *     --base https://docs.warp.dev \\
 *     --compare https://docs-preview.warp.dev \\
 *     /agent-platform/cloud-agents/oz-web-app
 *
 * The script is intentionally dependency-free (uses regex over the raw HTML
 * head) so it runs in CI without installing extra packages.
 */
import { readFile } from 'node:fs/promises';
import path from 'node:path';

const DEFAULT_PATHS = [
	'/',
	'/quickstart/',
	'/agent-platform/',
	'/agent-platform/cloud-agents/oz-web-app/',
	'/agent-platform/capabilities/skills/',
	'/reference/cli/',
	'/reference/api-and-sdk/',
	'/changelog/',
	'/university/',
];

/** Tags GitBook produces that we want to keep at parity. */
const REQUIRED_TAGS = [
	{ key: 'title', label: '<title>' },
	{ key: 'meta:description', label: 'meta name="description"' },
	{ key: 'meta:robots', label: 'meta name="robots"' },
	{ key: 'link:canonical', label: 'link rel="canonical"' },
	{ key: 'meta:og:title', label: 'meta property="og:title"' },
	{ key: 'meta:og:description', label: 'meta property="og:description"' },
	{ key: 'meta:og:image', label: 'meta property="og:image"' },
	{ key: 'meta:og:url', label: 'meta property="og:url"' },
	{ key: 'meta:og:site_name', label: 'meta property="og:site_name"' },
	{ key: 'meta:twitter:card', label: 'meta name="twitter:card"' },
	{ key: 'meta:twitter:title', label: 'meta name="twitter:title"' },
	{ key: 'meta:twitter:description', label: 'meta name="twitter:description"' },
	{ key: 'meta:twitter:image', label: 'meta name="twitter:image"' },
	{ key: 'meta:apple-mobile-web-app-title', label: 'meta name="apple-mobile-web-app-title"' },
	{ key: 'link:apple-touch-icon', label: 'link rel="apple-touch-icon"' },
	{ key: 'link:alternate-markdown', label: 'link rel="alternate" type="text/markdown"' },
	{ key: 'link:sitemap-or-icon', label: 'link rel="sitemap" or "icon"/"shortcut icon"' },
];

function parseArgs(argv) {
	const args = { dist: null, base: null, compare: null, paths: [] };
	for (let i = 0; i < argv.length; i++) {
		const arg = argv[i];
		if (arg === '--dist') args.dist = argv[++i];
		else if (arg === '--base') args.base = argv[++i];
		else if (arg === '--compare') args.compare = argv[++i];
		else if (arg === '--help' || arg === '-h') args.help = true;
		else args.paths.push(arg);
	}
	return args;
}

function extractHead(html) {
	const headMatch = html.match(/<head[^>]*>([\s\S]*?)<\/head>/i);
	return headMatch ? headMatch[1] : html;
}

function getTitle(head) {
	const m = head.match(/<title[^>]*>([\s\S]*?)<\/title>/i);
	return m ? m[1].trim() : null;
}

function getMeta(head, attr, value) {
	// Match either name="x" or property="x" (and either order of attrs).
	const re = new RegExp(
		`<meta[^>]*(?:${attr}=["']${value}["'][^>]*content=["']([^"']*)["']|content=["']([^"']*)["'][^>]*${attr}=["']${value}["'])[^>]*>`,
		'i',
	);
	const m = head.match(re);
	return m ? (m[1] ?? m[2]) : null;
}

function getLink(head, rel, type) {
	const typePart = type ? `type=["']${type}["']` : null;
	// Try both attribute orders. Astro sometimes emits href before rel.
	const patterns = [
		new RegExp(
			`<link[^>]*rel=["']${rel}["']${typePart ? `[^>]*${typePart}` : ''}[^>]*href=["']([^"']*)["'][^>]*>`,
			'i',
		),
		new RegExp(
			`<link[^>]*href=["']([^"']*)["'][^>]*rel=["']${rel}["']${typePart ? `[^>]*${typePart}` : ''}[^>]*>`,
			'i',
		),
	];
	for (const re of patterns) {
		const m = head.match(re);
		if (m) return m[1];
	}
	return null;
}

function audit(html) {
	const head = extractHead(html);
	const result = {
		'title': getTitle(head),
		'meta:description': getMeta(head, 'name', 'description'),
		'meta:robots': getMeta(head, 'name', 'robots'),
		'link:canonical': getLink(head, 'canonical'),
		'meta:og:title': getMeta(head, 'property', 'og:title'),
		'meta:og:description': getMeta(head, 'property', 'og:description'),
		'meta:og:image': getMeta(head, 'property', 'og:image'),
		'meta:og:url': getMeta(head, 'property', 'og:url'),
		'meta:og:site_name': getMeta(head, 'property', 'og:site_name'),
		'meta:twitter:card': getMeta(head, 'name', 'twitter:card'),
		'meta:twitter:title': getMeta(head, 'name', 'twitter:title'),
		'meta:twitter:description': getMeta(head, 'name', 'twitter:description'),
		'meta:twitter:image': getMeta(head, 'name', 'twitter:image'),
		'meta:apple-mobile-web-app-title': getMeta(head, 'name', 'apple-mobile-web-app-title'),
		'link:apple-touch-icon': getLink(head, 'apple-touch-icon'),
		'link:alternate-markdown': getLink(head, 'alternate', 'text/markdown'),
		'link:sitemap-or-icon': getLink(head, 'sitemap') ?? getLink(head, 'icon') ?? getLink(head, 'shortcut icon'),
	};
	return result;
}

async function loadFromDist(distRoot, urlPath) {
	const trimmed = urlPath.replace(/^\/+|\/+$/g, '');
	const candidates = [
		path.join(distRoot, trimmed, 'index.html'),
		path.join(distRoot, trimmed + '.html'),
		// Root path
		...(trimmed === '' ? [path.join(distRoot, 'index.html')] : []),
	];
	for (const candidate of candidates) {
		try {
			return await readFile(candidate, 'utf8');
		} catch {
			// Try next candidate.
		}
	}
	throw new Error(`Could not find built HTML for ${urlPath} (looked in ${candidates.join(', ')})`);
}

async function loadFromUrl(base, urlPath) {
	const url = new URL(urlPath, base).href;
	const res = await fetch(url, {
		headers: {
			'User-Agent': 'Mozilla/5.0 (compatible; warp-seo-audit/1.0)',
			'Accept': 'text/html',
		},
		redirect: 'follow',
	});
	if (!res.ok) {
		throw new Error(`${url} → HTTP ${res.status}`);
	}
	return await res.text();
}

function format(value, width = 80) {
	if (value == null) return '— missing —';
	const single = value.replace(/\s+/g, ' ').trim();
	return single.length > width ? `${single.slice(0, width - 1)}…` : single;
}

async function fetchOne(args, urlPath) {
	if (args.dist) {
		return loadFromDist(path.resolve(args.dist), urlPath);
	}
	if (args.base) {
		return loadFromUrl(args.base, urlPath);
	}
	throw new Error('Must pass --dist <dir> or --base <url>');
}

async function main() {
	const args = parseArgs(process.argv.slice(2));
	if (args.help) {
		console.log(
			[
				'SEO audit — checks for the meta tags GitBook emitted on every page',
				'so we don\'t regress when migrating to Astro/Starlight.',
				'',
				'Usage:',
				'  node scripts/seo-audit.mjs --dist ./dist [paths...]',
				'  node scripts/seo-audit.mjs --base https://docs.warp.dev [paths...]',
				'  node scripts/seo-audit.mjs --base <url> --compare <url> [paths...]',
				'',
				'If no paths are passed, a default high-traffic set is audited.',
			].join('\n'),
		);
		return;
	}

	if (!args.dist && !args.base) {
		console.error('Error: provide --dist <dir> (built site) or --base <url> (live site).');
		process.exit(2);
	}

	const paths = args.paths.length ? args.paths : DEFAULT_PATHS;
	let totalMissing = 0;

	for (const p of paths) {
		console.log(`\n=== ${p} ===`);
		let primary;
		try {
			primary = audit(await fetchOne(args, p));
		} catch (err) {
			console.error(`  ERROR: ${err.message}`);
			totalMissing += REQUIRED_TAGS.length;
			continue;
		}

		let compare = null;
		if (args.compare) {
			try {
				compare = audit(await loadFromUrl(args.compare, p));
			} catch (err) {
				console.error(`  compare ERROR: ${err.message}`);
			}
		}

		for (const { key, label } of REQUIRED_TAGS) {
			const got = primary[key];
			const cmp = compare?.[key];
			const status = got == null ? '✗' : '✓';
			if (got == null) totalMissing += 1;
			let line = `  ${status} ${label.padEnd(48)} ${format(got)}`;
			if (compare) {
				line += `\n    compare: ${format(cmp)}`;
				if (got !== cmp && got != null && cmp != null) {
					line += '\n    (values differ — review for parity)';
				}
			}
			console.log(line);
		}
	}

	if (totalMissing > 0) {
		console.error(`\n${totalMissing} missing tag(s) across ${paths.length} page(s).`);
		process.exit(1);
	}
	console.log(`\nAll required tags present across ${paths.length} page(s).`);
}

main().catch((err) => {
	console.error(err);
	process.exit(1);
});
