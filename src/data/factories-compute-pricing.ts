import type { PricingSource, VerificationStatus } from './model-pricing';

export interface ComputePrice {
	key: string;
	platform: 'Linux' | 'Windows' | 'macOS';
	architecture: string;
	shape?: { vcpus: number; memory: number; memoryUnit: 'GB' | 'GiB' };
	hourly?: number;
	formula?: { unitHourly: number; minimumUnits: number; memoryPerUnit: number };
	source: PricingSource;
	additionalSources?: PricingSource[];
	runtimeSource: string;
	status: VerificationStatus;
	blocker?: string;
}

export const computePricingCheckedAt = '2026-10-13';
const runtimeSource = 'warp-server/logic/ai/ambient_agents/billing/compute_rate.go@904a56f6c11d15bae2fe44d3497ff4144e8c1153';
export const computePricingSource: PricingSource = {
	label: 'Namespace pricing', url: 'https://namespace.so/pricing', accessed: computePricingCheckedAt,
};
const meteringBlocker = 'Remote Platform and Billing must confirm exact-duration billing, lifecycle boundaries, units, extras, and failover; resolve both macOS discrepancies before any compute rate publishes.';
const dockerSource: PricingSource = {
	label: 'Docker Sandboxes compute sizes', url: 'https://docs.docker.com/ai/sandboxes-api/limits/', accessed: computePricingCheckedAt,
};
const dockerBillingSource: PricingSource = {
	label: 'Docker Agentic Platform billing', url: 'https://docs.docker.com/agentic-platform/signup/', accessed: computePricingCheckedAt,
};

export const factoriesComputePricing: ComputePrice[] = [
	{ key: 'linux-configurable', platform: 'Linux', architecture: 'x86-64 or aarch64', formula: { unitHourly: 0.09, minimumUnits: 1, memoryPerUnit: 2 }, source: computePricingSource, runtimeSource, status: 'internal-verification', blocker: meteringBlocker },
	{ key: 'windows-configurable', platform: 'Windows', architecture: 'x86-64', formula: { unitHourly: 0.18, minimumUnits: 1, memoryPerUnit: 2 }, source: computePricingSource, runtimeSource, status: 'internal-verification', blocker: meteringBlocker },
	...([
		[4, 7, 4.5, 'code-mismatch'],
		[6, 14, 5.4, 'internal-verification'],
		[8, 14, 8.1, 'code-mismatch'],
		[12, 28, 10.8, 'internal-verification'],
		[12, 56, 16.2, 'internal-verification'],
	] as const).map(([vcpus, memory, hourly, status]): ComputePrice => ({
		key: `macos-${vcpus}-${memory}`, platform: 'macOS', architecture: 'Apple Silicon',
		shape: { vcpus, memory, memoryUnit: 'GB' }, hourly, source: computePricingSource, runtimeSource, status,
		blocker: status === 'code-mismatch' ? `Public hourly rate differs from the configured charge. ${meteringBlocker}` : meteringBlocker,
	})),
	...(['micro', 'small', 'medium', 'large', 'xl'] as const).map((size, index): ComputePrice => ({
		key: `docker-${size}`, platform: 'Linux', architecture: 'x86-64',
		shape: { vcpus: 2 ** index, memory: 2 ** (index + 1), memoryUnit: 'GiB' },
		source: dockerSource, additionalSources: [dockerBillingSource], runtimeSource,
		status: 'public-source-missing',
		blocker: 'No public numeric rate; confirm production availability and contractual billing evidence before adding a price.',
	})),
];

export const verifiedComputePricing = factoriesComputePricing.filter((row) => row.status === 'verified');
