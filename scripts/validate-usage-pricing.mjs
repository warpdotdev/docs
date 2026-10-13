import { readFile, readdir } from 'node:fs/promises';
import { fileURLToPath, pathToFileURL } from 'node:url';
import path from 'node:path';
import ts from 'typescript';
import { parseHTML } from 'linkedom';

const root = fileURLToPath(new URL('../', import.meta.url));
const modelPage = 'agents/inference/model-choice.mdx';
const computePage = 'factories/usage-and-billing.mdx';
const statuses = new Set(['verified', 'catalog-mismatch', 'code-mismatch', 'public-source-missing', 'internal-verification']);
const firstPartyHosts = new Set(['developers.openai.com', 'platform.claude.com', 'ai.google.dev', 'cloud.google.com', 'docs.x.ai', 'docs.fireworks.ai', 'namespace.so', 'docs.docker.com']);

async function loadData(name) {
	const source = await readFile(path.join(root, 'src/data', name), 'utf8');
	const { outputText } = ts.transpileModule(source, { compilerOptions: { module: ts.ModuleKind.ESNext, target: ts.ScriptTarget.ES2022 } });
	return import(`data:text/javascript;base64,${Buffer.from(outputText).toString('base64')}`);
}

export async function pricingInputs() {
	const models = await loadData('model-pricing.ts');
	const compute = await loadData('factories-compute-pricing.ts');
	const inventory = JSON.parse(await readFile(path.join(root, 'src/data/pricing-inventory.json'), 'utf8'));
	const pages = {};
	async function walk(directory) {
		for (const entry of await readdir(directory, { withFileTypes: true })) {
			const filename = path.join(directory, entry.name);
			if (entry.isDirectory()) await walk(filename);
			else if (/\.mdx?$/.test(entry.name)) pages[path.relative(path.join(root, 'src/content/docs'), filename)] = await readFile(filename, 'utf8');
		}
	}
	await walk(path.join(root, 'src/content/docs'));
	return { models: models.modelPricing, compute: compute.factoriesComputePricing, inventory, pages };
}

export function validatePricing({ models, compute, inventory, pages }, today = new Date().toISOString().slice(0, 10)) {
	const errors = [];
	const check = (condition, message) => { if (!condition) errors.push(message); };
	const isoDate = (value) => typeof value === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(value) && !Number.isNaN(Date.parse(value)) && new Date(value).toISOString().slice(0, 10) === value;
	function source(value, key) {
		let url;
		try { url = new URL(value?.url); } catch {}
		check(url?.protocol === 'https:' && firstPartyHosts.has(url?.hostname) && !!value?.label, `${key}: missing first-party source`);
		check(isoDate(value?.accessed) && value.accessed <= today, `${key}: invalid source access date`);
	}
	function common(row) {
		check(!!row.key && statuses.has(row.status), `${row.key}: invalid key or status`);
		check(row.status === 'verified' || !!row.blocker, `${row.key}: blocked record needs a reason`);
		check(/warp-server\/.+@[a-f0-9]{40}$/.test(row.runtimeSource ?? ''), `${row.key}: missing runtime revision`);
		source(row.source, row.key);
		for (const value of row.additionalSources ?? []) source(value, row.key);
	}
	function tuple(value, key, anthropic) {
		for (const category of ['input', 'cacheWrite', 'cacheRead', 'output']) {
			check(Object.hasOwn(value ?? {}, category) && (value[category] === null && category.startsWith('cache') || Number.isFinite(value[category]) && value[category] >= 0), `${key}: incomplete or invalid ${category} rate`);
		}
		if (anthropic) check(Number.isFinite(value?.cacheWrite) && Number.isFinite(value?.cacheWrite1h) && value.cacheWrite1h >= 0, `${key}: missing Anthropic cache duration`);
	}
	const keys = new Set();
	const names = new Set();
	const ids = new Set();
	check(Array.isArray(inventory.regionalRequirements) && inventory.regionalRequirements.length > 0, 'missing approved regional requirements');
	const regionalRequirements = inventory.regionalRequirements ?? [];
	const regionalNotes = new Map();
	for (const row of models) {
		common(row);
		check(!keys.has(row.key), `${row.key}: duplicate row key`);
		check(!names.has(row.name), `${row.key}: duplicate named model`);
		keys.add(row.key); names.add(row.name);
		check(Array.isArray(row.modelIds) && row.modelIds.length > 0, `${row.key}: missing model IDs`);
		for (const id of row.modelIds ?? []) {
			check(!ids.has(id), `${id}: model ID belongs to multiple rows`);
			check(!/^(auto(?:-|$)|best$|opus$|sonnet$|haiku$|fable$|custom)/.test(id), `${id}: moving alias has a fixed rate`);
			ids.add(id);
		}
		check(row.lifecycle === 'active' || row.lifecycle === 'deprecated', `${row.key}: missing lifecycle status`);
		check(row.lifecycle !== 'deprecated' || row.status !== 'verified', `${row.key}: deprecated model cannot be verified`);
		tuple(row.rates, row.key, row.provider === 'Anthropic');
		if (row.threshold) {
			check(Number.isInteger(row.threshold.tokens) && row.threshold.tokens > 0 && typeof row.threshold.inclusive === 'boolean', `${row.key}: invalid threshold`);
			tuple(row.threshold.rates, `${row.key} threshold`, row.provider === 'Anthropic');
			for (const [category, price] of Object.entries(row.rates)) {
				check(price === null || Number.isFinite(row.threshold.rates?.[category]), `${row.key}: threshold omits billable ${category}`);
			}
		}
		const regionals = [...(row.regional ? [row.regional] : []), ...(row.regionalVariants ?? [])];
		for (const required of regionalRequirements.filter((item) => item.modelKeys.includes(row.key))) {
			check(regionals.some((regional) => regional.key === required.key), `${row.key}: missing required regional qualification ${required.key}`);
		}
		const regionalKeys = new Set();
		for (const regional of regionals) {
			check(!regionalKeys.has(regional.key), `${row.key}: duplicate regional qualification`);
			regionalKeys.add(regional.key);
			const required = regionalRequirements.find((item) => item.key === regional.key && item.modelKeys.includes(row.key));
			check(!!required && regional.multiplier === required.multiplier && regional.source?.url === required.sourceUrl, `${row.key}: regional qualification differs from approved inventory`);
			check(Number.isFinite(regional.multiplier) && regional.multiplier > 0 && !!regional.note, `${row.key}: regional rate needs a multiplier and customer note`);
			check(typeof regional.note === 'string' && regional.note.includes(`${regional.multiplier}×`), `${row.key}: regional note omits multiplier`);
			check(!regionalNotes.has(regional.key) || regionalNotes.get(regional.key) === regional.note, `${row.key}: inconsistent regional customer note`);
			regionalNotes.set(regional.key, regional.note);
			source(regional.source, `${row.key} regional`);
		}
		if (row.promotion) {
			check(isoDate(row.promotion.ends) && row.promotion.ends >= today, `${row.key}: missing or expired promotion end date`);
			tuple(row.promotion.afterwards, `${row.key} post-promotion`, row.provider === 'Anthropic');
		}
		if (row.reverifyBy) check(isoDate(row.reverifyBy) && row.reverifyBy >= today, `${row.key}: reverification overdue`);
	}
	const expectedIds = new Set(inventory.modelIds);
	for (const id of expectedIds) check(ids.has(id), `${id}: inventory model has no rate row`);
	for (const id of ids) check(expectedIds.has(id), `${id}: rate model not in approved inventory`);
	check(models.length === inventory.modelRows, 'named-model row count differs from approved inventory');
	for (const [provider, count] of Object.entries(inventory.providerRows)) check(models.filter((row) => row.provider === provider).length === count, `${provider}: inventory row count differs`);
	for (const required of regionalRequirements) {
		for (const key of required.modelKeys) check(keys.has(key), `${key}: required regional model missing`);
	}
	const pageIds = new Set([...pages[modelPage].matchAll(/`((?:gpt-|claude-|gemini-|grok-|glm-|kimi-|minimax-|qwen-|deepseek-)[^`]+)`/g)].map((match) => match[1]));
	for (const id of expectedIds) check(pageIds.has(id), `${id}: configuration table missing inventory ID`);
	for (const id of pageIds) check(expectedIds.has(id), `${id}: undocumented inventory change`);
	const computeKeys = new Set();
	check(Array.isArray(inventory.shapePricedComputeKeys) && inventory.shapePricedComputeKeys.length > 0, 'missing approved shaped-compute requirements');
	for (const row of compute) {
		common(row);
		check(!computeKeys.has(row.key), `${row.key}: duplicate compute row`);
		computeKeys.add(row.key);
		check(!Object.hasOwn(row, 'modelIds') && !Object.hasOwn(row, 'rates') && !Object.hasOwn(row, 'provider'), `${row.key}: model rates cannot live in compute data`);
		const hourly = Number.isFinite(row.hourly) && row.hourly >= 0;
		const formula = row.formula && Number.isFinite(row.formula.unitHourly) && row.formula.unitHourly >= 0 && Number.isInteger(row.formula.minimumUnits) && row.formula.minimumUnits > 0 && Number.isFinite(row.formula.memoryPerUnit) && row.formula.memoryPerUnit > 0;
		check(row.formula === undefined || formula, `${row.key}: incomplete compute formula`);
		check(row.hourly === undefined || hourly, `${row.key}: invalid compute hourly price`);
		if (row.shape || row.hourly !== undefined || inventory.shapePricedComputeKeys?.includes(row.key)) {
			check(Number.isInteger(row.shape?.vcpus) && row.shape.vcpus > 0 && Number.isFinite(row.shape?.memory) && row.shape.memory > 0 && ['GB', 'GiB'].includes(row.shape?.memoryUnit), `${row.key}: missing or invalid compute shape`);
		}
		check(hourly || formula || row.status === 'public-source-missing', `${row.key}: incomplete compute price or formula`);
		check(!(hourly && formula), `${row.key}: ambiguous compute price`);
		check(row.status !== 'verified' || hourly || formula, `${row.key}: verified compute price missing`);
		check(!!row.platform && !!row.architecture, `${row.key}: missing runner configuration`);
	}
	for (const key of inventory.computeKeys) check(computeKeys.has(key), `${key}: missing compute configuration`);
	for (const key of computeKeys) check(inventory.computeKeys.includes(key), `${key}: unapproved compute configuration`);
	for (const [filename, content] of Object.entries(pages)) {
		check(!content.includes('ModelPricingTable') || filename === modelPage, `${filename}: duplicate model rate owner`);
		check(!content.includes('ComputePricingTable') || filename === computePage, `${filename}: duplicate compute rate owner`);
		check(!content.includes('@data/model-pricing') || filename === modelPage, `${filename}: duplicate model data owner`);
		check(!content.includes('@data/factories-compute-pricing') || filename === computePage, `${filename}: duplicate compute data owner`);
		if (filename !== modelPage) {
			for (const line of content.split('\n')) {
				check(!(/\$\s*\d/.test(line) && models.some((row) => line.includes(row.name))), `${filename}: copied named-model numeric rate`);
			}
		}
		if (filename === modelPage || filename === computePage) check(!/\$\s*\d|USD\s+\d/i.test(content), `${filename}: handwritten numeric rate bypasses canonical data`);
		if (filename === computePage) check(!content.includes('model-pricing'), `${filename}: model data must not be imported`);
	}
	return errors;
}

export async function validateBuiltPricing({ models, compute, inventory }) {
	const errors = [];
	for (const [slug, records, attribute] of [
		['agents/inference/model-choice', models, 'data-pricing-key'],
		['factories/usage-and-billing', compute, 'data-compute-pricing-key'],
	]) {
		const html = await readFile(path.join(root, '.vercel/output/static', slug, 'index.html'), 'utf8');
		const { document } = parseHTML(html);
		const rendered = [...document.querySelectorAll(`[${attribute}]`)].map((node) => node.getAttribute(attribute));
		const expected = records.filter((row) => row.status === 'verified').map((row) => row.key);
		if (JSON.stringify(rendered.toSorted()) !== JSON.stringify(expected.toSorted())) errors.push(`${slug}: rendered records do not match verified data`);
		for (const table of document.querySelectorAll(`table:has([${attribute}])`)) {
			if (!table.querySelector('caption') || !table.querySelector('thead th[scope="col"]') || !table.querySelector('tbody th[scope="row"]')) errors.push(`${slug}: table lacks accessible headers or caption`);
		}
		if (slug === 'agents/inference/model-choice') {
			const qualifications = [...document.querySelectorAll('[data-regional-pricing-key]')];
			const verified = records.filter((row) => row.status === 'verified');
			for (const required of inventory.regionalRequirements) {
				const scoped = verified.filter((row) => required.modelKeys.includes(row.key));
				const notes = qualifications.filter((node) => node.getAttribute('data-regional-pricing-key') === required.key);
				if (scoped.length === 0) {
					if (notes.length) errors.push(`${required.key}: unverified regional qualification rendered`);
					continue;
				}
				const node = notes[0];
				const expectedScope = `Applies to: ${scoped.map((row) => row.name).join(', ')}.`;
				if (notes.length !== 1 || node?.querySelector('[data-regional-scope]')?.textContent !== expectedScope || !node?.querySelector(`a[href="${required.sourceUrl}"]`)?.textContent) {
					errors.push(`${required.key}: missing regional qualification scope or source`);
				}
				for (const row of scoped) {
					const regional = [row.regional, ...(row.regionalVariants ?? [])].find((value) => value?.key === required.key);
					if (!regional || node?.querySelector('[data-regional-note]')?.textContent !== regional.note || !regional.note.includes(`${required.multiplier}×`)) {
						errors.push(`${row.key}: missing built regional qualification`);
					}
				}
			}
			for (const node of qualifications) {
				if (!inventory.regionalRequirements.some((required) => required.key === node.getAttribute('data-regional-pricing-key'))) errors.push('unapproved regional qualification rendered');
			}
		}
	}
	return errors;
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
	const inputs = await pricingInputs();
	const errors = validatePricing(inputs);
	if (process.argv.includes('--built')) errors.push(...await validateBuiltPricing(inputs));
	if (process.argv.includes('--require-complete')) {
		for (const row of [...inputs.models, ...inputs.compute]) if (row.status !== 'verified') errors.push(`${row.key}: ${row.status}: ${row.blocker}`);
	}
	if (errors.length) {
		console.error(errors.join('\n'));
		process.exitCode = 1;
	} else {
		console.log(`Pricing validation passed: ${inputs.models.length} model rows, ${inputs.inventory.modelIds.length} IDs, ${inputs.compute.length} compute configurations.`);
		console.log(`${inputs.models.filter((row) => row.status !== 'verified').length} model rows and ${inputs.compute.filter((row) => row.status !== 'verified').length} compute configurations remain blocked.`);
	}
}
