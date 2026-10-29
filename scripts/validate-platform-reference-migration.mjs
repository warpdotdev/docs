import assert from 'node:assert/strict';
import { existsSync, readFileSync, readdirSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { parseHTML } from 'linkedom';
import { DOCS_ORIGIN } from '../src/lib/site.js';

const repo = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const output = resolve(repo, process.argv[2] ?? '.vercel/output/static');
const fixture = JSON.parse(readFileSync(join(repo, 'scripts/fixtures/platform-reference-migration.json'), 'utf8'));
const { redirects } = JSON.parse(readFileSync(join(repo, 'vercel.json'), 'utf8'));
const moved = fixture.pages.filter(({ oldPath, newPath }) => oldPath !== newPath);
const bridges = fixture.pages.filter(({ oldPath, newPath }) => oldPath === newPath);
const failures = [];
const documents = new Map();

function check(label, fn) {
	try {
		fn();
	} catch (error) {
		failures.push(`${label}: ${error.message}`);
	}
}

function read(relativePath) {
	return readFileSync(join(output, relativePath), 'utf8');
}

function htmlFile(route) {
	return join(route.slice(1), 'index.html');
}

function markdownFile(route) {
	return `${route.slice(1).replace(/\/$/, '')}.md`;
}

function content(route) {
	if (!documents.has(route)) documents.set(route, parseHTML(read(htmlFile(route))).document);
	const document = documents.get(route);
	const body = document.querySelector('main .sl-markdown-content');
	assert.ok(body, `missing article content for ${route}`);
	return { document, body };
}

function sourceExists(route) {
	const id = route.slice(1).replace(/\/$/, '');
	return [join(repo, 'src/content/docs', `${id}.mdx`), join(repo, 'src/content/docs', id, 'index.mdx')]
		.some((file) => existsSync(file));
}

// Scope this check to unconditional literal/optional-slash rules. Broad legacy
// aliases are checked for final destinations separately; query middleware has
// its own tracking-route regression suite.
function staticMatches(rule, route) {
	if (rule.has?.length || rule.missing?.length || rule.source.includes(':')) return false;
	const optionalSlash = rule.source.endsWith('(/?)');
	const literal = optionalSlash ? rule.source.slice(0, -4) : rule.source;
	return route === literal || (optionalSlash && route === `${literal}/`);
}

function expectRedirect(from, to) {
	const matches = redirects.filter((rule) => staticMatches(rule, from));
	assert.equal(matches.length, 1, `expected one static redirect for ${from}`);
	assert.equal(matches[0].statusCode, 308, from);
	assert.equal(matches[0].destination, to, from);
	assert.equal(redirects.filter((rule) => staticMatches(rule, to)).length, 0, `redirect chain at ${to}`);
	assert.ok(!to.includes('#'), `redirect destination must preserve the incoming fragment: ${to}`);
}

assert.equal(moved.length, 10);
assert.equal(bridges.length, 2);
assert.equal(new Set(fixture.pages.map(({ oldPath }) => oldPath)).size, 12);

const sitemap = readdirSync(output)
	.filter((file) => /^sitemap.*\.xml$/.test(file))
	.map(read)
	.join('\n');
const llmsFull = read('llms-full.txt');
const llmsSmall = read('llms-small.txt');
const llmsFactories = read('_llms-txt/factories.txt');
const llmsPlatform = read('_llms-txt/automation-platform.txt');

for (const page of fixture.pages) {
	const { oldPath, newPath, anchors } = page;
	check(newPath, () => {
		assert.ok(sourceExists(newPath), `missing new MDX source ${newPath}`);
		const { document, body } = content(newPath);
		for (const id of anchors) assert.ok([...body.querySelectorAll('[id]')].some((node) => node.id === id), `lost #${id}`);
		const ids = [...body.querySelectorAll('[id]')].map((node) => node.id);
		assert.equal(new Set(ids).size, ids.length, 'duplicate article IDs');
		const canonical = [...document.querySelectorAll('link[rel="canonical"]')];
		assert.equal(canonical.length, 1, 'canonical count');
		assert.equal(canonical[0].getAttribute('href'), `${DOCS_ORIGIN}${newPath}`);
		const robots = [...document.querySelectorAll('meta[name="robots"]')];
		assert.equal(robots.length, 1, 'robots count');
		assert.ok(!robots[0].getAttribute('content').includes('noindex'), 'page must remain indexable');
		assert.ok(document.querySelector('[data-pagefind-body]'), 'missing Pagefind content');
		assert.ok(sitemap.includes(`<loc>${DOCS_ORIGIN}${newPath}</loc>`), 'missing sitemap entry');
		for (const aggregate of [llmsFull, llmsSmall]) {
			assert.ok(aggregate.includes(`Canonical page: [${newPath}]`), 'missing LLM canonical entry');
		}
		assert.ok(read(markdownFile(newPath)).includes('# '), 'missing Markdown content');
		assert.equal(document.querySelector('link[rel="alternate"][type="text/markdown"]')?.getAttribute('href'),
			`/${markdownFile(newPath)}`);
		for (const image of body.querySelectorAll('img[src]')) {
			const src = image.getAttribute('src');
			if (src.startsWith('/')) assert.ok(existsSync(join(output, src.slice(1).split('?')[0])), `missing image ${src}`);
		}
		for (const anchor of body.querySelectorAll('a[href]')) {
			const url = new URL(anchor.getAttribute('href'), `${DOCS_ORIGIN}${newPath}`);
			if (url.origin !== DOCS_ORIGIN || /^\/api\/?$/.test(url.pathname)) continue;
			if (/\.[^/]+$/.test(url.pathname)) {
				assert.ok(existsSync(join(output, url.pathname.slice(1))), `missing linked file ${url.pathname}`);
				continue;
			}
			const target = content(url.pathname.endsWith('/') ? url.pathname : `${url.pathname}/`);
			if (url.hash) assert.ok(target.document.getElementById(decodeURIComponent(url.hash.slice(1))),
				`missing rendered link target ${url.pathname}${url.hash}`);
		}
		if (oldPath !== newPath) {
			assert.ok(!sourceExists(oldPath), `old source remains at ${oldPath}`);
			assert.ok(!existsSync(join(output, htmlFile(oldPath))), `old HTML remains at ${oldPath}`);
			assert.ok(!existsSync(join(output, markdownFile(oldPath))), `old Markdown remains at ${oldPath}`);
			expectRedirect(oldPath.slice(0, -1), newPath);
			expectRedirect(oldPath, newPath);
			expectRedirect(`/${markdownFile(oldPath)}`, `/${markdownFile(newPath)}`);
			const legacyPaths = [
				oldPath.replace(/^\/platform\//, '/agent-platform/cloud-agents/'),
				...(page.legacyPaths ?? []),
			];
			for (const legacy of legacyPaths) {
				expectRedirect(legacy.slice(0, -1), newPath);
				expectRedirect(legacy, newPath);
				expectRedirect(`/${markdownFile(legacy)}`, `/${markdownFile(newPath)}`);
				if (legacy.startsWith('/agent-platform/cloud-agents/')) {
					const explicit = redirects.findIndex((rule) => staticMatches(rule, legacy));
					const fallback = redirects.findIndex((rule) => rule.source.startsWith('/agent-platform/cloud-agents/:'));
					assert.ok(fallback === -1 || explicit < fallback, 'legacy alias runs after broad fallback');
				}
			}
			assert.ok(llmsFactories.includes(`Canonical page: [${newPath}]`), 'missing Factories LLM owner');
			for (const aggregate of [llmsFull, llmsSmall, llmsPlatform]) {
				assert.ok(!aggregate.includes(`Canonical page: [${oldPath}]`), 'old LLM owner remains');
			}
			assert.ok(!sitemap.includes(`<loc>${DOCS_ORIGIN}${oldPath}</loc>`), 'old sitemap owner remains');
			assert.equal(document.querySelector('.warp-topic-nav a[aria-current="page"]')?.getAttribute('href'),
				'/factories/', 'wrong documentation topic');
		} else {
			assert.ok(body.querySelector('a[href="/factories/quickstart/"]'), 'missing primary factory setup link');
			assert.ok(body.querySelector('a[href="/platform/transitioning-from-oz/"], a[href="/platform/"]'),
				'missing standalone/transition entry point');
		}
	});
}

check('incoming aliases', () => {
	const oldTargets = new Set(moved.flatMap(({ oldPath }) => [
		oldPath, oldPath.slice(0, -1), `/${markdownFile(oldPath)}`,
	]));
	assert.ok(!redirects.some(({ destination }) => oldTargets.has(destination)), 'incoming alias still chains through a moved page');
});
check('bare Platform entry', () => expectRedirect('/platform', '/platform/'));
check('self-hosting security discovery', () => {
	const route = '/factories/self-hosting/security-and-networking/';
	const { document, body } = content(route);
	assert.ok(document.querySelector(`.sidebar-pane a[href="${route}"]`), 'missing self-hosting sidebar entry');
	for (const parent of ['/factories/self-hosting/', '/factories/infrastructure-and-security/']) {
		assert.ok(content(parent).body.querySelector(`a[href="${route}#network-requirements"]`),
			`missing direct network requirements link from ${parent}`);
	}
	assert.ok(body.querySelector('a[href="/platform/unmanaged-execution/"]'), 'lost standalone unmanaged guidance');
	for (const host of ['app.warp.dev', 'rtc.app.warp.dev', 'sessions.app.warp.dev', 'oz.warp.dev', 'storage.googleapis.com']) {
		assert.ok(body.textContent.includes(host), `lost network destination ${host}`);
	}
});
check('original guide retirement', () => {
	const old = '/guides/agent-workflows/run-a-software-factory-in-the-cloud';
	expectRedirect(old, '/factories/quickstart/');
	expectRedirect(`${old}/`, '/factories/quickstart/');
	expectRedirect(`${old}.md`, '/factories/quickstart.md');
	assert.ok(!sourceExists(`${old}/`));
	assert.ok(!existsSync(join(output, htmlFile(`${old}/`))));
});
for (const [route, other] of [
	['/factories/mcp/', '/factories/factory-mcp/'],
	['/factories/factory-mcp/', '/factories/mcp/'],
]) {
	check(`MCP direction: ${route}`, () => {
		const { body } = content(route);
		const intro = parseHTML(`<div>${body.innerHTML.split(/<h2\b/i)[0]}</div>`).document;
		assert.ok(intro.querySelector(`a[href="${other}"]`), 'missing opposite-task link before setup');
		assert.match(intro.textContent ?? intro.documentElement?.textContent ?? '', /external tools|coding agent/i);
	});
}

if (failures.length) {
	console.error(`Platform reference migration failed:\n${failures.map((failure) => `- ${failure}`).join('\n')}`);
	process.exitCode = 1;
} else {
	console.log(`Platform reference migration OK: ${moved.length} moves, ${bridges.length} entry bridges, preserved anchors and discovery.`);
}
