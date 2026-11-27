// Cases shared by the build-output model and the deployed HTTP verifier.
export const routingJourneys = [
	{ path: '/factories', final: '/factories/', hops: 1 },
	{ path: '/factories/', final: '/factories/', hops: 0 },
	{ path: '/factories?utm_source=routing-check', final: '/factories/?utm_source=routing-check', hops: 1 },
	{ path: '/factories/?trk=routing-check', final: '/factories/', hops: 1 },
	{ path: '/agent-platform', final: '/agents/', hops: 2 },
	{ path: '/agent-platform/', final: '/agents/', hops: 1 },
	{ path: '/errors/authentication_required', final: '/factories/api-and-sdk/troubleshooting/errors/authentication-required/', hops: 2 },
	{ path: '/errors/authentication_required/', final: '/factories/api-and-sdk/troubleshooting/errors/authentication-required/', hops: 1 },
	{ path: '/cli/oz-cli/api-keys', final: '/agents/cli/oz-cli/api-keys/', hops: 2 },
	{ path: '/api', final: '/api/', hops: 1 },
	{ path: '/api/', final: '/api/', hops: 0 },
	{ path: '/factories.md', final: '/factories.md', hops: 0, type: 'text/markdown' },
	{ path: '/llms.txt', final: '/llms.txt', hops: 0, type: 'text/plain' },
	{ path: '/.well-known/ard.json', final: '/.well-known/ard.json', hops: 0, type: 'application/json' },
	{ path: '/factories/index.html', final: '/factories/index.html', hops: 0 },
	{ path: '/not-a-real-page-routing-check', final: '/not-a-real-page-routing-check/', hops: 1, status: 404 },
];
