import assert from 'node:assert/strict';
import { existsSync, readFileSync, readdirSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { parseHTML } from 'linkedom';
import { DOCS_ORIGIN } from '../src/lib/site.js';

const repo = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const output = join(repo, '.vercel/output/static');
const fixture = JSON.parse(readFileSync(join(repo, 'scripts/fixtures/article-retirements.json'), 'utf8'));
const { redirects } = JSON.parse(readFileSync(join(repo, 'vercel.json'), 'utf8'));
const read = (file) => readFileSync(join(output, file), 'utf8');
const html = (route) => `${route.slice(1)}index.html`;
const md = (route) => `${route.slice(1).replace(/\/$/, '')}.md`;
const documents = new Map();
function article(route) {
	if (!documents.has(route)) documents.set(route, parseHTML(read(html(route))).document);
	const document = documents.get(route);
	const body = document.querySelector('main .sl-markdown-content');
	assert.ok(body, `missing article ${route}`);
	return { document, body };
}
function matches(rule, route) {
	if (rule.has?.length || rule.missing?.length || rule.source.includes(':')) return false;
	const optional = rule.source.endsWith('(/?)');
	const path = optional ? rule.source.slice(0, -4) : rule.source;
	return route === path || (optional && route === `${path}/`);
}
function redirect(from, to) {
	const rules = redirects.filter((rule) => matches(rule, from));
	assert.equal(rules.length, 1, `redirect count: ${from}`);
	assert.equal(rules[0].destination, to, from);
	assert.equal(rules[0].statusCode, 308, from);
	assert.ok(!to.includes('#'), 'do not override incoming fragments');
	assert.equal(redirects.filter((rule) => matches(rule, to)).length, 0, `chain: ${to}`);
}
function linkedTarget(href, from) {
	const url = new URL(href, `${DOCS_ORIGIN}${from}`);
	if (url.origin !== DOCS_ORIGIN || /^\/api\/?$/.test(url.pathname)) return;
	if (/\.[^/]+$/.test(url.pathname)) {
		assert.ok(existsSync(join(output, url.pathname.slice(1))), url.href);
		return;
	}
	const target = article(url.pathname.endsWith('/') ? url.pathname : `${url.pathname}/`);
	if (url.hash) assert.ok(target.document.getElementById(decodeURIComponent(url.hash.slice(1))), url.href);
}
const sitemap = readdirSync(output).filter((file) => /^sitemap.*\.xml$/.test(file)).map(read).join('\n');
const llms = [read('llms-full.txt'), read('llms-small.txt')];
assert.deepEqual(fixture.pages.map((page) => page.headings.length), [11, 40, 3]);
for (const page of fixture.pages) {
	const { oldPath, newPath, headings } = page;
	const { document, body } = article(newPath);
	const ids = [...body.querySelectorAll('[id]')].map((node) => node.id);
	assert.equal(new Set(ids).size, ids.length, `duplicate IDs: ${newPath}`);
	for (const { id } of headings) assert.ok(ids.includes(id), `lost fragment ${oldPath}#${id}`);
	assert.equal(document.querySelector('link[rel="canonical"]')?.getAttribute('href'), `${DOCS_ORIGIN}${newPath}`);
	assert.ok(!document.querySelector('meta[name="robots"]')?.getAttribute('content').includes('noindex'));
	assert.ok(document.querySelector('[data-pagefind-body]'), `missing search body: ${newPath}`);
	assert.ok(sitemap.includes(`<loc>${DOCS_ORIGIN}${newPath}</loc>`));
	for (const aggregate of llms) assert.ok(aggregate.includes(`Canonical page: [${newPath}]`));
	assert.ok(read(md(newPath)).includes('# '));
	for (const link of body.querySelectorAll('a[href]')) linkedTarget(link.getAttribute('href'), newPath);
	if (oldPath !== newPath) {
		assert.ok(!existsSync(join(repo, `src/content/docs${oldPath.slice(0, -1)}.mdx`)));
		assert.ok(!existsSync(join(output, html(oldPath))));
		assert.ok(!existsSync(join(output, md(oldPath))));
		redirect(oldPath.slice(0, -1), newPath);
		redirect(oldPath, newPath);
		redirect(`/${md(oldPath)}`, `/${md(newPath)}`);
		assert.ok(!sitemap.includes(`<loc>${DOCS_ORIGIN}${oldPath}</loc>`));
		for (const aggregate of llms) assert.ok(!aggregate.includes(`Canonical page: [${oldPath}]`));
	} else {
		assert.equal(redirects.filter((rule) => matches(rule, oldPath)).length, 0);
		assert.equal(Object.keys(page.destinations).length, 34);
		for (const [id, href] of Object.entries(page.destinations)) {
			const item = body.querySelector(`[id="${id}"]`)?.closest('li');
			assert.ok(item?.querySelector(`a[href="${href}"]`), `wrong FAQ successor: ${id}`);
			linkedTarget(href, newPath);
		}
		assert.ok(!body.textContent.includes('still being finalized'));
	}
}
for (const alias of [
	'/agent-platform/cloud-agents/skills-as-agents',
]) {
	for (const suffix of ['', '/']) redirect(`${alias}${suffix}`, '/agents/capabilities/skills/');
	redirect(`${alias}.md`, '/agents/capabilities/skills.md');
	const explicit = redirects.findIndex((rule) => matches(rule, alias));
	const fallback = redirects.findIndex((rule) => rule.source.startsWith('/agent-platform/cloud-agents/:'));
	assert.ok(fallback === -1 || explicit < fallback, 'legacy fallback shadows explicit redirect');
}
for (const alias of [
	'/university/developer-workflows/power-user/how-to-use-agent-profiles-efficiently',
	'/guides/developer-workflows/power-user/how-to-use-agent-profiles-efficiently',
]) {
	for (const suffix of ['', '/']) redirect(`${alias}${suffix}`, fixture.pages[2].newPath);
	redirect(`${alias}.md`, `/${md(fixture.pages[2].newPath)}`);
}
const retired = fixture.pages.filter((page) => page.oldPath !== page.newPath).map((page) => page.oldPath);
for (const rule of redirects) assert.ok(!retired.includes(rule.destination), `alias chain: ${rule.source}`);
const guides = article('/guides/').body;
assert.ok(!guides.querySelector(`a[href="${fixture.pages[2].oldPath}"]`));
assert.ok(guides.querySelector(`a[href="${fixture.pages[2].newPath}"]`));
assert.ok(read('agents/capabilities/skills.md').includes('WARP_SKILL_DIRS'));
assert.ok(read('factories/api-and-sdk.md').includes('"skill_spec"'));
assert.ok(read('platform/triggers/scheduled-agents.md').includes('--skill'));
console.log('Article retirements OK: 2 redirects, 1 topic bridge, 54 original fragments, 34 FAQ destinations.');
