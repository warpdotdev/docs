export type VerificationStatus =
	| 'verified'
	| 'catalog-mismatch'
	| 'code-mismatch'
	| 'public-source-missing'
	| 'internal-verification';

export interface PricingSource {
	label: string;
	url: string;
	accessed: string;
}

export interface TokenRates {
	input: number;
	cacheWrite: number | null;
	cacheWrite1h?: number;
	cacheRead: number | null;
	output: number;
}

export interface RegionalPrice {
	key: string;
	multiplier: number;
	note: string;
	source: PricingSource;
}

export interface ModelPrice {
	key: string;
	name: string;
	provider: string;
	modelIds: string[];
	rates: TokenRates;
	threshold?: { tokens: number; inclusive: boolean; rates: TokenRates };
	regional?: RegionalPrice;
	regionalVariants?: RegionalPrice[];
	lifecycle: 'active' | 'deprecated';
	deprecatedAt?: string;
	promotion?: { ends: string; afterwards: TokenRates };
	reverifyBy?: string;
	source: PricingSource;
	additionalSources?: PricingSource[];
	runtimeSource: string;
	status: VerificationStatus;
	blocker?: string;
	note?: string;
}

export const modelPricingCheckedAt = '2026-10-13';
export const runtimeRevision = '904a56f6c11d15bae2fe44d3497ff4144e8c1153';
export const modelPricingSources: Record<string, PricingSource> = {
	OpenAI: { label: 'OpenAI API pricing', url: 'https://developers.openai.com/api/docs/pricing', accessed: modelPricingCheckedAt },
	Anthropic: { label: 'Anthropic API pricing', url: 'https://platform.claude.com/docs/en/about-claude/pricing', accessed: modelPricingCheckedAt },
	Google: { label: 'Gemini Developer API pricing', url: 'https://ai.google.dev/gemini-api/docs/pricing', accessed: modelPricingCheckedAt },
	xAI: { label: 'xAI API pricing', url: 'https://docs.x.ai/developers/pricing', accessed: modelPricingCheckedAt },
	Fireworks: { label: 'Fireworks Serverless pricing', url: 'https://docs.fireworks.ai/serverless/pricing', accessed: modelPricingCheckedAt },
};
const fastSource: PricingSource = { label: 'Anthropic fast mode', url: 'https://platform.claude.com/docs/en/build-with-claude/fast-mode', accessed: modelPricingCheckedAt };
const lifecycleSource: PricingSource = { label: 'Anthropic model deprecations', url: 'https://platform.claude.com/docs/en/about-claude/model-deprecations', accessed: modelPricingCheckedAt };
const googleCloudSource: PricingSource = { label: 'Google Cloud model pricing', url: 'https://cloud.google.com/gemini-enterprise-agent-platform/generative-ai/pricing', accessed: modelPricingCheckedAt };
const googleMigrationSource: PricingSource = { label: 'Gemini 3.7 Flash migration', url: 'https://ai.google.dev/gemini-api/docs/whats-new-gemini-3.7', accessed: modelPricingCheckedAt };

function rates(input: number, cacheWrite: number | null, cacheRead: number | null, output: number, cacheWrite1h?: number): TokenRates {
	return { input, cacheWrite, cacheRead, output, ...(cacheWrite1h === undefined ? {} : { cacheWrite1h }) };
}

function efforts(family: string, levels = ['low', 'medium', 'high', 'xhigh', 'max']): string[] {
	return levels.map((level) => `${family}-${level}`);
}

function model(key: string, name: string, provider: string, modelIds: string[], price: TokenRates, options: Partial<ModelPrice> = {}): ModelPrice {
	return {
		key, name, provider, modelIds, rates: price, lifecycle: 'active',
		source: modelPricingSources[provider],
		runtimeSource: `warp-server/logic/ai/llm/llm.go@${runtimeRevision}`,
		status: 'internal-verification',
		blocker: options.status === 'verified' ? undefined : provider === 'Anthropic'
			? 'Confirm direct versus partner-cloud serving hosts and regional pricing applicability with AI Platform and Billing.'
			: 'Confirm rate and serving-route applicability before publication.',
		...(provider === 'Anthropic' ? { regionalVariants: [{ key: 'anthropic-partner-cloud', multiplier: 1.1, note: 'Partner-cloud regional and multi-region pricing is 1.1× global pricing for Claude 4.5 and later; Warp route applicability is unconfirmed.', source: modelPricingSources.Anthropic }] } : {}),
		...(provider === 'Google' ? { regional: { key: 'google-non-global', multiplier: 1.1, note: 'Google Cloud non-global inference is 1.1× global pricing; Warp endpoint and region applicability is unconfirmed.', source: googleCloudSource } } : {}),
		...(provider === 'xAI' && ['grok-4-6', 'grok-4-7'].includes(key) ? { regional: { key: 'xai-us', multiplier: 1.1, note: 'US-region inference is 1.1× global pricing for Grok 4.6 and 4.7; Warp route applicability is unconfirmed.', source: modelPricingSources.xAI } } : {}),
		...(provider === 'Fireworks' ? { regional: { key: 'fireworks-us', multiplier: 1.5, note: 'Fireworks publishes 1.5× pricing for US-region variants; Warp variant applicability is unconfirmed.', source: modelPricingSources.Fireworks } } : {}),
		...options,
	};
}

const openAIRegional = {
	key: 'openai-direct-us',
	multiplier: 1.1,
	note: 'Direct US-only inference costs 1.1× these global rates for all listed OpenAI models.',
	source: modelPricingSources.OpenAI,
};
const anthropicRegional = {
	key: 'anthropic-direct-us',
	multiplier: 1.1,
	note: 'Direct US-only inference costs 1.1× these global rates for Claude 4.6 and later, including fast mode.',
	source: { label: 'Anthropic data residency pricing', url: 'https://platform.claude.com/docs/en/build-with-claude/data-residency', accessed: modelPricingCheckedAt },
};
const googleBlocker = 'Confirm serving region and whether context-cache storage is passed through before publishing a customer rate.';
const xAIThresholdBlocker = 'Runtime applies the higher tier only above 200,000 input tokens; the public card applies it at 200,000.';
const fireworksBlocker = 'Billing must reconcile the configured customer charge with the public card before publication.';
const openAIThreshold = (price: TokenRates) => ({
	tokens: 272000, inclusive: false,
	rates: rates(price.input * 2, price.cacheWrite === null ? null : price.cacheWrite * 2, price.cacheRead === null ? null : price.cacheRead * 2, price.output * 1.5),
});

export const modelPricing: ModelPrice[] = [
	model('gpt-6-astra', 'GPT-6 Astra', 'OpenAI', efforts('gpt-6-astra'), rates(10, 12.5, 1, 50), { status: 'verified', threshold: openAIThreshold(rates(10, 12.5, 1, 50)), regional: openAIRegional }),
	model('gpt-6-1-sol', 'GPT-6.1 Sol', 'OpenAI', efforts('gpt-6-1-sol'), rates(2, 2.5, 0.1, 10), { status: 'verified', threshold: openAIThreshold(rates(2, 2.5, 0.1, 10)), regional: openAIRegional }),
	model('gpt-6-sol', 'GPT-6 Sol', 'OpenAI', efforts('gpt-6-sol'), rates(2, 2.5, 0.2, 10), { status: 'verified', threshold: openAIThreshold(rates(2, 2.5, 0.2, 10)), regional: openAIRegional }),
	model('gpt-6-luna', 'GPT-6 Luna', 'OpenAI', efforts('gpt-6-luna'), rates(0.1, 0.125, 0.01, 0.5), { status: 'verified', threshold: openAIThreshold(rates(0.1, 0.125, 0.01, 0.5)), regional: openAIRegional }),
	model('gpt-5-6-sol', 'GPT-5.6 Sol', 'OpenAI', efforts('gpt-5-6-sol', ['low', 'medium', 'high', 'xhigh']), rates(4, 5, 0.4, 20), { status: 'verified', threshold: openAIThreshold(rates(4, 5, 0.4, 20)), regional: openAIRegional, reverifyBy: '2026-11-21' }),
	model('gpt-5-6-terra', 'GPT-5.6 Terra', 'OpenAI', efforts('gpt-5-6-terra', ['low', 'medium', 'high', 'xhigh']), rates(2, 2.5, 0.2, 12), { status: 'verified', threshold: openAIThreshold(rates(2, 2.5, 0.2, 12)), regional: openAIRegional }),
	model('gpt-5-6-luna', 'GPT-5.6 Luna', 'OpenAI', efforts('gpt-5-6-luna', ['low', 'medium', 'high', 'xhigh']), rates(0.2, 0.25, 0.02, 1.2), { status: 'verified', threshold: openAIThreshold(rates(0.2, 0.25, 0.02, 1.2)), regional: openAIRegional }),
	model('gpt-5-5', 'GPT-5.5', 'OpenAI', efforts('gpt-5-5', ['low', 'medium', 'high', 'xhigh']), rates(5, null, 0.5, 30), { status: 'verified', threshold: openAIThreshold(rates(5, null, 0.5, 30)), regional: openAIRegional }),
	model('gpt-5-4', 'GPT-5.4', 'OpenAI', efforts('gpt-5-4', ['low', 'medium', 'high', 'xhigh']), rates(2.5, null, 0.25, 15), { status: 'verified', threshold: openAIThreshold(rates(2.5, null, 0.25, 15)), regional: openAIRegional }),
	model('claude-5-5-opus', 'Claude Opus 5.5', 'Anthropic', efforts('claude-5-5-opus'), rates(4, 5, 0.2, 20, 8), { regional: anthropicRegional }),
	model('claude-5-5-opus-fast', 'Claude Opus 5.5 Fast', 'Anthropic', ['claude-5-5-opus-xhigh-fast'], rates(8, 10, 0.4, 40, 16), { regional: anthropicRegional, additionalSources: [fastSource], note: 'Fast mode is a research preview.' }),
	model('claude-5-opus', 'Claude Opus 5', 'Anthropic', efforts('claude-5-opus'), rates(5, 6.25, 0.5, 25, 10), { regional: anthropicRegional }),
	model('claude-5-opus-fast', 'Claude Opus 5 Fast', 'Anthropic', ['claude-5-opus-xhigh-fast'], rates(10, 12.5, 1, 50, 20), { regional: anthropicRegional, additionalSources: [fastSource], note: 'Fast mode is a research preview.' }),
	model('claude-5-1-fable', 'Claude Fable 5.1', 'Anthropic', efforts('claude-5-1-fable'), rates(10, 12.5, 0.25, 50, 20), { regional: anthropicRegional }),
	model('claude-5-fable', 'Claude Fable 5', 'Anthropic', efforts('claude-5-fable'), rates(10, 12.5, 1, 50, 20), { regional: anthropicRegional }),
	model('claude-5-5-sonnet', 'Claude Sonnet 5.5', 'Anthropic', efforts('claude-5-5-sonnet'), rates(2, 2.5, 0.1, 10, 4), { regional: anthropicRegional }),
	model('claude-5-sonnet', 'Claude Sonnet 5', 'Anthropic', efforts('claude-5-sonnet'), rates(2, 2.5, 0.2, 10, 4), { regional: anthropicRegional }),
	model('claude-4-8-opus', 'Claude Opus 4.8', 'Anthropic', efforts('claude-4-8-opus'), rates(5, 6.25, 0.5, 25, 10), { regional: anthropicRegional }),
	model('claude-4-8-opus-fast', 'Claude Opus 4.8 Fast', 'Anthropic', ['claude-4-8-opus-xhigh-fast'], rates(10, 12.5, 1, 50, 20), { regional: anthropicRegional, additionalSources: [fastSource], note: 'Fast mode is a research preview.' }),
	model('claude-4-7-opus', 'Claude Opus 4.7', 'Anthropic', efforts('claude-4-7-opus', ['high', 'xhigh', 'max']), rates(5, 6.25, 0.5, 25, 10), { regional: anthropicRegional }),
	model('claude-4-6-opus', 'Claude Opus 4.6', 'Anthropic', efforts('claude-4-6-opus', ['high', 'max']), rates(5, 6.25, 0.5, 25, 10), { regional: anthropicRegional }),
	model('claude-4-6-sonnet', 'Claude Sonnet 4.6', 'Anthropic', efforts('claude-4-6-sonnet', ['high', 'max']), rates(3, 3.75, 0.3, 15, 6), { regional: anthropicRegional }),
	model('claude-4-5-opus', 'Claude Opus 4.5', 'Anthropic', ['claude-4-5-opus', 'claude-4-5-opus-thinking'], rates(5, 6.25, 0.5, 25, 10)),
	model('claude-4-5-sonnet', 'Claude Sonnet 4.5', 'Anthropic', ['claude-4-5-sonnet', 'claude-4-5-sonnet-thinking'], rates(3, 3.75, 0.3, 15, 6), { status: 'catalog-mismatch', lifecycle: 'deprecated', deprecatedAt: '2026-09-30', additionalSources: [lifecycleSource], blocker: 'Anthropic retires this model on 2026-11-30. Confirm retention, removal, or remapping with the catalog owner.' }),
	model('claude-5-5-haiku', 'Claude Haiku 5.5', 'Anthropic', efforts('claude-5-5-haiku'), rates(0.1, 0.125, 0.01, 0.5, 0.2), { regional: anthropicRegional, threshold: { tokens: 100000, inclusive: false, rates: rates(0.5, 0.625, 0.05, 2.5, 1) } }),
	model('claude-4-5-haiku', 'Claude Haiku 4.5', 'Anthropic', ['claude-4-5-haiku'], rates(1, 1.25, 0.1, 5, 2)),
	model('gemini-3.1-pro', 'Gemini 3.1 Pro', 'Google', ['gemini-3.1-pro'], rates(2, null, 0.2, 12), { status: 'internal-verification', blocker: googleBlocker, additionalSources: [googleCloudSource], threshold: { tokens: 200000, inclusive: false, rates: rates(4, null, 0.4, 18) } }),
	model('gemini-3.8-flash', 'Gemini 3.8 Flash', 'Google', ['gemini-3.8-flash'], rates(0.75, null, 0.075, 3.75), { status: 'internal-verification', blocker: googleBlocker, additionalSources: [googleCloudSource], promotion: { ends: '2026-12-31', afterwards: rates(1.5, null, 0.15, 7.5) } }),
	model('gemini-3.7-flash', 'Gemini 3.7 Flash', 'Google', ['gemini-3.7-flash'], rates(0.75, null, 0.075, 3.75), { status: 'catalog-mismatch', lifecycle: 'deprecated', blocker: 'Provider remaps this ID to Gemini 3.8 Flash; confirm the Warp catalog decision.', additionalSources: [googleCloudSource, googleMigrationSource], promotion: { ends: '2026-12-31', afterwards: rates(1.5, null, 0.15, 7.5) } }),
	model('gemini-3.6-flash', 'Gemini 3.6 Flash', 'Google', ['gemini-3.6-flash'], rates(0.75, null, 0.075, 3.75), { status: 'code-mismatch', blocker: 'Runtime uses the post-promotion tuple before the public promotion ends.', additionalSources: [googleCloudSource], promotion: { ends: '2026-12-31', afterwards: rates(1.5, null, 0.15, 7.5) } }),
	model('gemini-3.5-flash', 'Gemini 3.5 Flash', 'Google', ['gemini-3.5-flash'], rates(1.5, null, 0.15, 9), { status: 'internal-verification', blocker: googleBlocker, additionalSources: [googleCloudSource] }),
	model('grok-4-7', 'Grok 4.7', 'xAI', efforts('grok-4-7', ['low', 'medium', 'high', 'xhigh']), rates(2, null, 0.5, 6), { status: 'code-mismatch', blocker: xAIThresholdBlocker, threshold: { tokens: 200000, inclusive: true, rates: rates(4, null, 1, 12) } }),
	model('grok-4-6', 'Grok 4.6', 'xAI', efforts('grok-4-6', ['low', 'medium', 'high', 'xhigh']), rates(2, null, 0.5, 6), { status: 'code-mismatch', blocker: xAIThresholdBlocker, threshold: { tokens: 200000, inclusive: true, rates: rates(4, null, 1, 12) } }),
	model('grok-4-5', 'Grok 4.5', 'xAI', efforts('grok-4-5', ['low', 'medium', 'high']), rates(2, null, 0.3, 6), { status: 'code-mismatch', blocker: xAIThresholdBlocker, threshold: { tokens: 200000, inclusive: true, rates: rates(4, null, 0.6, 12) } }),
	model('grok-4-3', 'Grok 4.3', 'xAI', efforts('grok-4-3', ['low', 'medium', 'high']), rates(1.25, null, 0.2, 2.5), { status: 'code-mismatch', blocker: 'Runtime has no long-context tier.', threshold: { tokens: 200000, inclusive: true, rates: rates(2.5, null, 0.4, 5) } }),
	model('grok-build-0.1', 'Grok Build 0.1', 'xAI', ['grok-build-0.1'], rates(1, null, 0.2, 2), { status: 'code-mismatch', blocker: 'Runtime has no long-context tier.', threshold: { tokens: 200000, inclusive: true, rates: rates(2, null, 0.4, 4) } }),
	model('glm-5.3-fireworks', 'GLM 5.3', 'Fireworks', ['glm-5.3-fireworks'], rates(1.4, null, 0.26, 4.4), { status: 'code-mismatch', blocker: fireworksBlocker }),
	model('glm-5.3-flash-fireworks', 'GLM 5.3 Flash', 'Fireworks', ['glm-5.3-flash-fireworks'], rates(0.15, null, 0.03, 0.5), { status: 'code-mismatch', blocker: fireworksBlocker }),
	model('kimi-k3-fireworks', 'Kimi K3', 'Fireworks', ['kimi-k3-fireworks'], rates(3, null, 0.3, 15), { status: 'internal-verification', blocker: 'Confirm whether US-region Fireworks variants and their public multiplier apply to the Warp serving route.' }),
	model('minimax-3-fireworks', 'MiniMax M3', 'Fireworks', ['minimax-3-fireworks'], rates(0.3, null, 0.06, 1.2), { status: 'code-mismatch', blocker: fireworksBlocker }),
	model('qwen-3.8-max-fireworks', 'Qwen 3.8 Max', 'Fireworks', ['qwen-3.8-max-fireworks'], rates(2, null, 0.25, 6), { status: 'code-mismatch', blocker: fireworksBlocker }),
	model('deepseek-v4.1-flash-fireworks', 'DeepSeek V4.1 Flash', 'Fireworks', ['deepseek-v4.1-flash-fireworks'], rates(0.3, null, 0.006, 1.2), { status: 'code-mismatch', blocker: fireworksBlocker }),
];

export const verifiedModelPricing = modelPricing.filter((row) => row.status === 'verified');
