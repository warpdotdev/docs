import assert from 'node:assert/strict';
import test from 'node:test';
import { readFile, writeFile } from 'node:fs/promises';
import ts from 'typescript';
import { parseHTML } from 'linkedom';
import { pricingInputs, validatePricing, validateBuiltPricing } from './validate-usage-pricing.mjs';

const baseline = await pricingInputs();
const today = '2026-10-13';

const modelModule = await import(`data:text/javascript;base64,${Buffer.from(ts.transpileModule(
	(await readFile(new URL('../src/data/model-pricing.ts', import.meta.url), 'utf8')).replace("import pricingInventory from './pricing-inventory.json';", `const pricingInventory = ${JSON.stringify(baseline.inventory)};`),
	{ compilerOptions: { module: ts.ModuleKind.ESNext } },
).outputText).toString('base64')}`);
const approved = structuredClone(baseline.models[0]);

test('explicitly qualified model is publishable', () => {
	assert.equal(modelModule.isPublishableModelPrice(approved, today), true);
});

test('the public export contains only explicitly qualified models', () => {
	assert.ok(modelModule.verifiedModelPricing.length > 0);
	assert.ok(modelModule.verifiedModelPricing.every((row) => row.publication?.ga.status === 'ga'
		&& row.publication?.access.status === 'all-customers'
		&& row.publication?.deployment.environment === 'production'
		&& row.publication?.billedPath.status === 'confirmed'
		&& row.publication?.regional.status === 'qualified'));
});

for (const [name, mutate] of [
	['GA evidence', (row) => delete row.publication.ga],
	['preview status', (row) => row.publication.ga.status = 'preview'],
	['access evidence', (row) => delete row.publication.access],
	['tier restriction', (row) => row.publication.access.status = 'restricted'],
	['deployment evidence', (row) => delete row.publication.deployment],
	['undeployed effort', (row) => row.publication.deployment.modelIds = row.publication.deployment.modelIds.filter((id) => id !== row.modelIds[0])],
	['billed-path evidence', (row) => delete row.publication.billedPath],
	['unconfirmed host', (row) => row.publication.billedPath.host = ''],
	['regional evidence', (row) => delete row.publication.regional],
	['unqualified region', (row) => row.publication.regional.keys = []],
	['regional source', (row) => delete row.regional.source],
	['source evidence', (row) => delete row.source],
	['evidence reference', (row) => delete row.publication.ga.reference],
	['future confirmation', (row) => row.publication.ga.checkedAt = '2026-10-14'],
	['deprecated lifecycle', (row) => row.lifecycle = 'deprecated'],
	['overdue reverification', (row) => row.reverifyBy = '2026-10-12'],
	['expired promotional rate', (row) => row.promotion = { ends: '2026-10-12', afterwards: row.rates }],
]) {
	test(`publication rejects missing or ineligible ${name}`, () => {
		const row = structuredClone(approved);
		mutate(row);
		assert.equal(modelModule.isPublishableModelPrice(row, today), false);
		const inputs = structuredClone(baseline);
		inputs.models[0] = row;
		assert.match(validatePricing(inputs, today).join('\n'), /verified row lacks/);
	});
}

test('built validation rejects an unqualified numeric row', { skip: !process.argv.includes('--built') }, async () => {
	const inputs = structuredClone(baseline);
	delete inputs.models[0].publication;
	assert.match((await validateBuiltPricing(inputs)).join('\n'), /verified row lacks|rendered records do not match/);
});

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
	['duplicate rate surface', (data) => data.pages['factories/runners.mdx'] += '\n<ModelPricingTable />', /duplicate model rate owner/],
	['handwritten rate', (data) => data.pages['agents/inference/model-choice.mdx'] += '\n$1 per million tokens', /handwritten numeric rate/],
	['excluded compute surface', (data) => data.pages['factories/runners.mdx'] += '\n<ComputePricingTable />', /excluded compute deliverable/],
	['unqualified verified row', (data) => delete data.models[0].publication, /verified row lacks/],
	['unapproved published set', (data) => data.inventory.publishedModelKeys.pop(), /published model set/],
	['ambiguous approval', (data) => data.inventory.publicationEvidence.push(structuredClone(data.inventory.publicationEvidence[0])), /ambiguous/],
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
	const source = (await readFile(new URL('../src/data/model-pricing.ts', import.meta.url), 'utf8')).replace("import pricingInventory from './pricing-inventory.json';", `const pricingInventory = ${JSON.stringify(baseline.inventory)};`);
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
