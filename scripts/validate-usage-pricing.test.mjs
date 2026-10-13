import assert from 'node:assert/strict';
import test from 'node:test';
import { pricingInputs, validatePricing } from './validate-usage-pricing.mjs';

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
	['missing cache duration', (data) => delete data.models.find((row) => row.provider === 'Anthropic').rates.cacheWrite1h, /cache duration/],
	['expired promotion', (data) => data.models.find((row) => row.promotion).promotion.ends = '2026-10-12', /expired promotion/],
	['verified deprecation', (data) => data.models.find((row) => row.lifecycle === 'deprecated').status = 'verified', /deprecated model/],
	['incomplete compute formula', (data) => delete data.compute[0].formula.memoryPerUnit, /incomplete compute/],
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
