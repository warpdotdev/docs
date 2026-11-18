// Every docs page has one URL: the trailing-slash form. vercel.json sets
// `trailingSlash: true`, so Vercel 308s `/page` to `/page/` before any
// redirect runs. These tests compile vercel.json with @vercel/routing-utils
// (the library Vercel uses to build the routing table) and replay requests
// against the result, so a redirect that only matches one slash form, a
// shadowed page, or a long redirect chain fails CI instead of production.
import assert from 'node:assert/strict';
import { readdir, readFile } from 'node:fs/promises';
import { test } from 'node:test';
import routingUtils from '@vercel/routing-utils';

const { getTransformedRoutes } = routingUtils;
const repoFile = (path) => new URL(`../${path}`, import.meta.url);
const config = JSON.parse(await readFile(repoFile('vercel.json'), 'utf8'));
const redirects = config.redirects;

const { routes, error } = getTransformedRoutes({
	trailingSlash: config.trailingSlash,
	redirects,
});
assert.equal(error, null, error?.message);
const table = routes
	.filter((route) => !route.handle)
	.map((route) => ({
		re: new RegExp(route.src),
		status: route.status,
		location: route.headers?.Location,
	}));

const EXTENSION = /\.[A-Za-z0-9]+$/;
const lastSegment = (path) => path.replace(/\/$/, '').split('/').pop();
const isFragmentSource = (source) => source.includes('#');
const hasParams = (value) => /:[A-Za-z_]|\(\.\*\)|\$/.test(value.replace('(/?)', ''));

/** One routing pass: the redirect Location for `path`, or null. */
function step(path) {
	for (const route of table) {
		const match = route.re.exec(path);
		if (!match) continue;
		if (!route.status) return null; // e.g. /.well-known passthrough
		return substitute(route.location, match);
	}
	return null;
}

/** Fill `$1` / `$name` placeholders from a regex match, as Vercel does. */
function substitute(template, match) {
	return template.replace(/\$(\d+|[A-Za-z_]\w*)/g, (_, key) =>
		(/^\d+$/.test(key) ? match[Number(key)] : match.groups?.[key]) ?? '',
	);
}

/** Follow redirects; returns the final path (or URL) and the hop count. */
function follow(path) {
	let current = path;
	let hops = 0;
	while (hops < 6) {
		const next = step(current.split(/[?#]/)[0]);
		if (next === null) break;
		hops += 1;
		current = next;
		if (/^https?:\/\//.test(current)) return { final: current, hops, external: true };
	}
	return { final: current, hops, external: false };
}

async function contentFiles(dir) {
	const entries = await readdir(dir, { withFileTypes: true });
	const files = await Promise.all(entries.map((entry) => {
		const url = new URL(entry.name + (entry.isDirectory() ? '/' : ''), dir);
		return entry.isDirectory() ? contentFiles(url) : [url];
	}));
	return files.flat();
}

const docsRoot = repoFile('src/content/docs/');
const pages = new Set(['/api/']);
const contentSources = [];
for (const file of await contentFiles(docsRoot)) {
	const rel = file.href.slice(docsRoot.href.length);
	if (!/\.mdx?$/.test(rel)) continue;
	contentSources.push([rel, await readFile(file, 'utf8')]);
	const slug = rel.replace(/\.mdx?$/, '').replace(/(^|\/)index$/, '').toLowerCase();
	pages.add(slug ? `/${slug}/` : '/');
}

function isServed(target) {
	const path = target.split(/[?#]/)[0];
	if (pages.has(path)) return true;
	if (path.endsWith('.md')) return pages.has(`${path.slice(0, -3)}/`) || path === '/index.md';
	return EXTENSION.test(lastSegment(path)); // generated asset (feed, sitemap, spec)
}

/** A concrete request path that `source` matches. */
function sampleFor(source) {
	return source
		.replace(/\(\/\?\)$/, '')
		.replace(/:[A-Za-z_]\w*(\([^)]*\))?[*+?]?/g, 'sample-segment')
		.replace(/\(\.\*\)/g, 'sample-segment')
		.replace(/\\/g, '');
}

/** Collect every failure in a loop so one CI run lists them all. */
function expectNone(failures, label) {
	assert.deepEqual(failures, [], `${failures.length} ${label}:\n${failures.join('\n')}`);
}

const slashForms = (path) => {
	if (EXTENSION.test(lastSegment(path)) && !path.endsWith('/')) return [path];
	const base = path.replace(/\/$/, '');
	return [base, `${base}/`];
};

test('vercel.json enables trailing slashes', () => {
	assert.equal(config.trailingSlash, true);
});

test('no-slash page URLs 308 once to the slash form and slash forms are served', () => {
	assert.ok(pages.size > 100, `only ${pages.size} pages found`);
	const failures = [];
	for (const page of pages) {
		if (page === '/') continue;
		if (step(page) !== null) failures.push(`${page} is shadowed by a redirect to ${step(page)}`);
		const { final, hops } = follow(page.slice(0, -1));
		if (final !== page || hops !== 1) failures.push(`${page.slice(0, -1)} -> ${final} in ${hops} hops`);
	}
	expectNone(failures, 'page URL problems');
});

test('files, well-known paths, and Markdown twins are never slash-redirected', () => {
	for (const path of [
		'/llms.txt', '/llms-full.txt', '/sitemap-index.xml', '/robots.txt', '/openapi.json',
		'/.well-known/ard.json', '/.well-known/mcp.json', '/.well-known/anything',
		'/factories.md', '/agents/capabilities/skills.md', '/index.md',
	]) {
		assert.equal(step(path), null, path);
	}
});

test('every redirect source matches both slash forms and ends on a served page in at most 2 hops', () => {
	const failures = [];
	for (const { source, destination } of redirects) {
		if (isFragmentSource(source)) continue;
		const results = slashForms(sampleFor(source)).map((form) => ({ form, ...follow(form) }));
		for (const result of results) {
			if (result.hops < 1) failures.push(`${source}: ${result.form} is not redirected`);
		}
		if (new Set(results.map((result) => result.final)).size !== 1) {
			failures.push(`${source}: slash forms diverge ${JSON.stringify(results)}`);
		}
		if (hasParams(source) || hasParams(destination)) continue;
		for (const { form, final, hops, external } of results) {
			if (hops > 2) failures.push(`${source}: ${form} takes ${hops} hops`);
			if (!external && !isServed(final)) failures.push(`${source}: ${form} ends at missing ${final}`);
		}
	}
	expectNone(failures, 'redirect problems');
});

test('fragment-only sources have a fragment-free redirect or page for their path', () => {
	// Browsers never send #fragments, so these sources cannot match on their own.
	const failures = [];
	for (const { source } of redirects.filter((redirect) => isFragmentSource(redirect.source))) {
		const path = slashForms(source.split('#')[0]).at(-1);
		const { final } = follow(path);
		if (!isServed(final)) failures.push(`${source}: ${path} ends at missing ${final}`);
	}
	expectNone(failures, 'uncovered fragment sources');
});

test('no duplicate or conflicting redirect sources', () => {
	const failures = [];
	const sources = new Set();
	const byNormalized = new Map();
	for (const { source, destination } of redirects) {
		if (sources.has(source)) failures.push(`duplicate source ${source}`);
		sources.add(source);
		const key = source.replace(/\(\/\?\)$/, '').replace(/\/$/, '');
		const previous = byNormalized.get(key);
		if (previous !== undefined && previous !== destination) {
			failures.push(`${source} conflicts: ${previous} vs ${destination}`);
		}
		byNormalized.set(key, destination);
	}
	expectNone(failures, 'duplicate or conflicting sources');
});

test('internal page destinations use the canonical slash form', () => {
	const failures = redirects
		.filter(({ destination }) => destination.startsWith('/') && !hasParams(destination))
		.filter(({ destination }) => {
			const path = destination.split(/[?#]/)[0];
			return !path.endsWith('/') && !EXTENSION.test(lastSegment(path));
		})
		.map(({ source, destination }) => `${source} -> ${destination}`);
	expectNone(failures, 'destinations without a trailing slash');
});

test('no redirect or rewrite turns a page URL into a /.md path', () => {
	// Rewrites are replayed as if their `has` conditions (such as an Accept
	// header) match. This guards the path shape only; it does not check what
	// any rewrite serves.
	const rewrites = getTransformedRoutes({ rewrites: config.rewrites ?? [] }).routes
		.filter((route) => route.dest)
		.map((route) => ({ re: new RegExp(route.src), dest: route.dest }));
	const failures = [];
	for (const page of pages) {
		for (const form of new Set([page, page.replace(/\/$/, '') || '/'])) {
			const seen = [form];
			let current = form;
			for (let hop = 0; hop < 6; hop += 1) {
				const next = step(current);
				if (next === null) break;
				seen.push(next);
				current = next.split(/[?#]/)[0];
			}
			const rewritten = [];
			for (const path of seen) {
				for (const { re, dest } of rewrites) {
					const match = re.exec(path.split(/[?#]/)[0]);
					if (match) rewritten.push(substitute(dest, match));
				}
			}
			const bad = [...seen, ...rewritten].filter((path) => path.split(/[?#]/)[0].endsWith('/.md'));
			if (bad.length) failures.push(`${form} -> ${bad.join(', ')}`);
		}
	}
	expectNone(failures, 'page URLs that reach a /.md path');
});

test('internal links in docs content use the canonical slash URL', () => {
	// A link to /page instead of /page/ costs every reader and crawler a 308.
	// Fenced code blocks and inline code are skipped.
	const link = /(\]\(|href=["'])(\/[^)\s"'#?]*[^)\s"'#?/])(?=[)\s"'#?])/g;
	const failures = [];
	for (const [file, text] of contentSources) {
		const prose = text
			.replace(/^\s*(```|~~~)[\s\S]*?^\s*\1.*$/gm, '')
			.replace(/`[^`\n]*`/g, '');
		for (const match of prose.matchAll(link)) {
			const path = match[2];
			if (!EXTENSION.test(lastSegment(path)) && pages.has(`${path}/`)) {
				failures.push(`${file}: ${path} -> ${path}/`);
			}
		}
	}
	expectNone(failures, 'no-slash internal links');
});
