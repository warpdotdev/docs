// Checks the generated llms files after `npm run build`.
//
// Every page that llms-full.txt, llms-small.txt, or a /_llms-txt/*.txt set
// includes carries a "Canonical page: [path](url)" line (see
// patches/starlight-llms-txt+0.8.1.patch). Each of those URLs must be a page
// listed in the sitemap, so the files never send agents to the 404 page or to a
// page that search engines are told does not exist.
//
// Usage: node scripts/validate-llms-txt.mjs [outputDir]
// outputDir defaults to .vercel/output/static.
import { readdir, readFile } from 'node:fs/promises';
import path from 'node:path';

const outputDir = path.resolve(process.argv[2] ?? '.vercel/output/static');

const sitemapFiles = (await readdir(outputDir)).filter((name) => /^sitemap-\d+\.xml$/.test(name));
if (sitemapFiles.length === 0) {
	console.error(`No sitemap-N.xml in ${outputDir}. Run npm run build first.`);
	process.exit(1);
}
const sitemapUrls = new Set();
for (const name of sitemapFiles) {
	const xml = await readFile(path.join(outputDir, name), 'utf8');
	for (const [, loc] of xml.matchAll(/<loc>([^<]+)<\/loc>/g)) sitemapUrls.add(loc.trim());
}

const llmsFiles = ['llms-full.txt', 'llms-small.txt'];
try {
	for (const name of await readdir(path.join(outputDir, '_llms-txt'))) {
		if (name.endsWith('.txt')) llmsFiles.push(path.join('_llms-txt', name));
	}
} catch {
	// No custom sets configured.
}

const problems = [];
let checked = 0;
for (const name of llmsFiles) {
	const text = await readFile(path.join(outputDir, name), 'utf8');
	for (const [, url] of text.matchAll(/Canonical page: \[[^\]]*\]\(([^)\s]+)\)/g)) {
		checked += 1;
		if (!sitemapUrls.has(url)) problems.push(`${name}: ${url} is not in the sitemap`);
	}
}

if (checked === 0) problems.push('No "Canonical page:" lines found; the llms-txt patch may not have applied.');

if (problems.length > 0) {
	console.error(`llms files list ${problems.length} page(s) that are not in the sitemap:`);
	for (const problem of [...new Set(problems)]) console.error(`  ${problem}`);
	process.exit(1);
}
console.log(`OK: ${checked} canonical page entries across ${llmsFiles.length} llms files are all in the sitemap.`);
