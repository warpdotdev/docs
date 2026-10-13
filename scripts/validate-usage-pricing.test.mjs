import assert from 'node:assert/strict';
import test from 'node:test';
import { readFile, writeFile } from 'node:fs/promises';
import ts from 'typescript';
import { parseHTML } from 'linkedom';
import { pricingInputs, validatePricing, validateBuiltPricing } from './validate-usage-pricing.mjs';

const baseline = await pricingInputs();
const today = '2026-10-13';

test('approved inventory and sourced, gated data pass', () => {
	assert.deepEqual(validatePricing(baseline, today), []);
});

for (const [name, mutate, message] of [
	['missing inventory model', (data) => data.models.shift(), /inventory model has no rate row/],
	['duplicate effort ID', (data) => data.models[1].modelIds.push(data.models[0].modelIds[0]), /belongs to multiple rows/],
	['moving alias', (data) => data.models[0].modelIds.push('auto'), /moving alias/],
	['missing provenance', (data) => delete data.models[0].source, /first-party source/],
	['invalid access date', (data) => data.models[0].source.accessed = '2026-02-30', /invalid source access date/],
	['incomplete threshold', (data) => delete data.models[0].threshold.rates.output, /invalid output rate/],
	['null billable threshold category', (data) => data.models[0].threshold.rates.cacheRead = null, /threshold omits billable cacheRead/],
	['missing regional evidence', (data) => delete data.models[0].regional.source, /first-party source/],
	['missing regional qualification', (data) => delete data.models[0].regional, /missing required regional/],
	['missing partner-cloud qualification', (data) => delete data.models.find((row) => row.provider === 'Anthropic').regionalVariants, /missing required regional/],
	['missing all regional qualifications', (data) => { for (const row of data.models) { delete row.regional; delete row.regionalVariants; } }, /missing required regional/],
	['missing publication status', (data) => delete data.models[0].status, /invalid key or status/],
	['missing cache duration', (data) => delete data.models.find((row) => row.provider === 'Anthropic').rates.cacheWrite1h, /cache duration/],
	['expired promotion', (data) => data.models.find((row) => row.promotion).promotion.ends = '2026-10-12', /expired promotion/],
	['verified deprecation', (data) => data.models.find((row) => row.lifecycle === 'deprecated').status = 'verified', /deprecated model/],
	['incomplete compute formula', (data) => delete data.compute[0].formula.memoryPerUnit, /incomplete compute/],
	['infinite minimum compute units', (data) => data.compute[0].formula.minimumUnits = Infinity, /incomplete compute/],
	['infinite memory per compute unit', (data) => data.compute[0].formula.memoryPerUnit = Infinity, /incomplete compute/],
	['infinite shape resources', (data) => data.compute.find((row) => row.shape).shape.memory = Infinity, /invalid compute shape/],
	['fractional shape CPUs', (data) => data.compute.find((row) => row.shape).shape.vcpus = 1.5, /invalid compute shape/],
	['missing hourly shape', (data) => delete data.compute.find((row) => row.hourly).shape, /invalid compute shape/],
	['verified macOS without shape', (data) => { const row = data.compute.find((row) => row.platform === 'macOS'); row.status = 'verified'; delete row.shape; }, /invalid compute shape/],
	['missing public compute rate', (data) => data.compute.find((row) => row.status === 'public-source-missing').status = 'verified', /verified compute price missing/],
	['cross-owned model data', (data) => data.compute[0].rates = data.models[0].rates, /model rates cannot live/],
	['duplicate rate surface', (data) => data.pages['factories/runners.mdx'] += '\n<ComputePricingTable />', /duplicate compute rate owner/],
	['handwritten rate', (data) => data.pages['factories/usage-and-billing.mdx'] += '\n$1 per hour', /handwritten numeric rate/],
	['copied named-model rate', (data) => data.pages['factories/runners.mdx'] += '\n| GPT-6 Astra | $10 |', /copied named-model numeric rate/],
	['ID table drift', (data) => data.pages['agents/inference/model-choice.mdx'] += '\n`gpt-new-low`', /undocumented inventory change/],
]) {
	test(`rejects ${name}`, () => {
		const data = structuredClone(baseline);
		mutate(data);
		assert.match(validatePricing(data, today).join('\n'), message);
	});
}

test('models without explicit approval stay blocked', async () => {
	const source = await readFile(new URL('../src/data/model-pricing.ts', import.meta.url), 'utf8');
	const unapproved = source + "\nexport const unapproved = model('future-model', 'Future model', 'OpenAI', ['future-model'], rates(1, null, null, 1));";
	const { outputText } = ts.transpileModule(unapproved, { compilerOptions: { module: ts.ModuleKind.ESNext } });
	const { unapproved: row } = await import(`data:text/javascript;base64,${Buffer.from(outputText).toString('base64')}`);
	assert.equal(row.status, 'internal-verification');
	assert.ok(row.blocker);
});

for (const [name, mutate] of [
	['note', (node) => node.querySelector('[data-regional-note]').remove()],
	['model scope', (node) => node.querySelector('[data-regional-scope]').remove()],
	['source', (node) => node.querySelector('a').remove()],
	['entire qualification', (node) => node.remove()],
]) {
	test(`built validation rejects missing regional ${name}`, { skip: !process.argv.includes('--built') }, async () => {
		const filename = new URL('../.vercel/output/static/agents/inference/model-choice/index.html', import.meta.url);
		const html = await readFile(filename, 'utf8');
		assert.deepEqual(await validateBuiltPricing(baseline), []);
		const { document } = parseHTML(html);
		const node = document.querySelector('[data-regional-pricing-key="openai-direct-us"]');
		assert.ok(node);
		try {
			mutate(node);
			await writeFile(filename, document.toString());
			assert.match((await validateBuiltPricing(baseline)).join('\n'), /regional qualification/);
		} finally {
			await writeFile(filename, html);
		}
	});
}
