import assert from 'node:assert/strict';
import test from 'node:test';
import {
	KAPA_DOCS_PROJECT_ID,
	KAPA_RETRIEVAL_INTEGRATION_ID,
	KAPA_RETRIEVAL_UPSTREAM_URL,
	MAX_RETRIEVE_QUERY_LENGTH,
	RETRIEVE_RESPONSE_HEADERS,
	buildKapaRetrievalBody,
	createFixedWindowRateLimiter,
	getRetrieveClientKey,
	handleRetrieveGet,
	handleRetrieveOptions,
} from './kapa-agent-retrieval.js';

const SECRET_KEY = 'kapa-test-secret-do-not-leak';
const SAMPLE_CHUNKS = [
	{ content: 'Warp indexes your codebase.', source_url: 'https://docs.warp.dev/agents/capabilities/codebase-context/' },
	{ content: 'Agents can run commands.', source_url: 'https://docs.warp.dev/agents/' },
];

/**
 * @param {string} pathWithQuery
 * @param {HeadersInit} [headers]
 */
function getRequest(pathWithQuery, headers) {
	return new Request(`https://docs.warp.dev${pathWithQuery}`, { method: 'GET', headers });
}

/**
 * @param {Response} response
 */
async function readJson(response) {
	return JSON.parse(await response.text());
}

function okFetch() {
	return async () =>
		new Response(JSON.stringify(SAMPLE_CHUNKS), {
			status: 200,
			headers: { 'content-type': 'application/json' },
		});
}

test('OPTIONS returns CORS preflight without a body and is not rate limited', async () => {
	const limiter = createFixedWindowRateLimiter({ windowMs: 60_000, max: 1 });
	// Exhaust the limiter; OPTIONS must still succeed and must not consume quota.
	limiter.check('preflight-key');
	assert.equal(limiter.check('preflight-key').allowed, false);

	const response = handleRetrieveOptions();
	assert.equal(response.status, 204);
	assert.equal(await response.text(), '');
	assert.equal(response.headers.get('Access-Control-Allow-Origin'), '*');
	assert.equal(response.headers.get('Access-Control-Allow-Methods'), 'GET, OPTIONS');
	assert.equal(response.headers.get('Cache-Control'), 'no-store');
	assert.equal(response.headers.get('Content-Type'), 'application/json');
});

test('success proxies ranked chunks and attributes project/integration', async () => {
	/** @type {RequestInit | undefined} */
	let upstreamInit;
	/** @type {string | undefined} */
	let upstreamUrl;
	const fetchImpl = async (url, init) => {
		upstreamUrl = String(url);
		upstreamInit = init;
		return new Response(JSON.stringify(SAMPLE_CHUNKS), {
			status: 200,
			headers: { 'content-type': 'application/json' },
		});
	};

	const response = await handleRetrieveGet(
		getRequest('/retrieve?q=How+do+I+use+codebase+context%3F', {
			Authorization: 'Bearer should-not-forward',
			'X-Custom': 'nope',
		}),
		{ apiKey: `  ${SECRET_KEY}  `, fetchImpl, rateLimiter: null },
	);

	assert.equal(response.status, 200);
	assert.deepEqual(await readJson(response), SAMPLE_CHUNKS);
	assert.equal(response.headers.get('Cache-Control'), 'no-store');
	assert.equal(response.headers.get('Access-Control-Allow-Origin'), '*');
	assert.equal(response.headers.get('Content-Type'), 'application/json');

	assert.equal(
		upstreamUrl,
		`https://api.kapa.ai/query/v1/projects/${KAPA_DOCS_PROJECT_ID}/retrieval/`,
	);
	assert.equal(upstreamUrl, KAPA_RETRIEVAL_UPSTREAM_URL);
	assert.equal(upstreamInit?.method, 'POST');
	const upstreamHeaders = new Headers(upstreamInit?.headers);
	assert.equal(upstreamHeaders.get('X-API-KEY'), SECRET_KEY);
	assert.equal(upstreamHeaders.get('Content-Type'), 'application/json');
	assert.equal(upstreamHeaders.get('Authorization'), null);
	assert.equal(upstreamHeaders.get('X-Custom'), null);

	const body = JSON.parse(String(upstreamInit?.body));
	assert.deepEqual(body, {
		query: 'How do I use codebase context?',
		integration_id: KAPA_RETRIEVAL_INTEGRATION_ID,
		redact_query: true,
	});
	assert.deepEqual(buildKapaRetrievalBody(body.query), body);
	assert.equal(body.redact_query, true);
	assert.equal(body.integration_id, KAPA_RETRIEVAL_INTEGRATION_ID);
});

test('buildKapaRetrievalBody always sets redact_query and integration attribution', () => {
	const body = buildKapaRetrievalBody('What is Warp Drive?');
	assert.deepEqual(body, {
		query: 'What is Warp Drive?',
		integration_id: KAPA_RETRIEVAL_INTEGRATION_ID,
		redact_query: true,
	});
});

test('missing, blank, and oversized queries return 400', async () => {
	const fetchImpl = async () => {
		throw new Error('fetch should not run for invalid queries');
	};

	for (const path of ['/retrieve', '/retrieve?q=', '/retrieve?q=%20%20']) {
		const response = await handleRetrieveGet(getRequest(path), {
			apiKey: SECRET_KEY,
			fetchImpl,
			rateLimiter: null,
		});
		assert.equal(response.status, 400, path);
		const payload = await readJson(response);
		assert.match(payload.error, /q query parameter/i);
		assert.doesNotMatch(JSON.stringify(payload), new RegExp(SECRET_KEY));
	}

	const oversized = 'x'.repeat(MAX_RETRIEVE_QUERY_LENGTH + 1);
	const oversizedResponse = await handleRetrieveGet(
		getRequest(`/retrieve?q=${encodeURIComponent(oversized)}`),
		{ apiKey: SECRET_KEY, fetchImpl, rateLimiter: null },
	);
	assert.equal(oversizedResponse.status, 400);
	const oversizedPayload = await readJson(oversizedResponse);
	assert.match(oversizedPayload.error, /maximum length/i);
	assert.doesNotMatch(JSON.stringify(oversizedPayload), new RegExp(SECRET_KEY));
});

test('missing API key returns 500 and never calls upstream', async () => {
	let called = false;
	const fetchImpl = async () => {
		called = true;
		return new Response('[]', { status: 200 });
	};

	for (const apiKey of [undefined, null, '', '   ']) {
		const response = await handleRetrieveGet(getRequest('/retrieve?q=hello'), {
			apiKey,
			fetchImpl,
			rateLimiter: null,
		});
		assert.equal(response.status, 500);
		const payload = await readJson(response);
		assert.match(payload.error, /not configured/i);
		assert.equal(called, false);
	}
});

test('upstream network failure returns 502 without leaking secrets', async () => {
	const fetchImpl = async () => {
		throw new TypeError('fetch failed');
	};
	const response = await handleRetrieveGet(getRequest('/retrieve?q=hello'), {
		apiKey: SECRET_KEY,
		fetchImpl,
		rateLimiter: null,
	});
	assert.equal(response.status, 502);
	const payload = await readJson(response);
	assert.match(payload.error, /Failed to reach retrieval service/i);
	const serialized = JSON.stringify(payload);
	assert.doesNotMatch(serialized, new RegExp(SECRET_KEY));
	assert.doesNotMatch(serialized, /X-API-KEY/i);
});

test('upstream error status and body pass through', async () => {
	const upstreamError = { detail: 'integration not found' };
	const fetchImpl = async () =>
		new Response(JSON.stringify(upstreamError), {
			status: 403,
			headers: { 'content-type': 'application/json; charset=utf-8' },
		});

	const response = await handleRetrieveGet(getRequest('/retrieve?q=hello'), {
		apiKey: SECRET_KEY,
		fetchImpl,
		rateLimiter: null,
	});
	assert.equal(response.status, 403);
	const text = await response.text();
	assert.deepEqual(JSON.parse(text), upstreamError);
	assert.equal(response.headers.get('Cache-Control'), 'no-store');
	assert.equal(response.headers.get('Access-Control-Allow-Origin'), '*');
	assert.doesNotMatch(text, new RegExp(SECRET_KEY));
});

test('response headers always advertise JSON CORS and no-store defaults', () => {
	assert.equal(RETRIEVE_RESPONSE_HEADERS['Content-Type'], 'application/json');
	assert.equal(RETRIEVE_RESPONSE_HEADERS['Cache-Control'], 'no-store');
	assert.equal(RETRIEVE_RESPONSE_HEADERS['Access-Control-Allow-Origin'], '*');
	assert.equal(RETRIEVE_RESPONSE_HEADERS['Access-Control-Allow-Methods'], 'GET, OPTIONS');
});

test('secret is never present in success response body', async () => {
	const response = await handleRetrieveGet(getRequest('/retrieve?q=hello'), {
		apiKey: SECRET_KEY,
		fetchImpl: okFetch(),
		rateLimiter: null,
	});
	const text = await response.text();
	assert.doesNotMatch(text, new RegExp(SECRET_KEY));
	assert.doesNotMatch(text, /X-API-KEY/i);
});

test('getRetrieveClientKey prefers first X-Forwarded-For hop', () => {
	assert.equal(
		getRetrieveClientKey(
			getRequest('/retrieve?q=hi', {
				'x-forwarded-for': ' 203.0.113.10, 198.51.100.7 ',
			}),
		),
		'203.0.113.10',
	);
	assert.equal(
		getRetrieveClientKey(getRequest('/retrieve?q=hi', { 'x-real-ip': '198.51.100.9' })),
		'198.51.100.9',
	);
	assert.equal(getRetrieveClientKey(getRequest('/retrieve?q=hi')), 'unknown');
});

test('rate limit returns 429 with CORS headers and does not call upstream', async () => {
	const limiter = createFixedWindowRateLimiter({ windowMs: 60_000, max: 2 });
	let calls = 0;
	const fetchImpl = async () => {
		calls += 1;
		return new Response(JSON.stringify(SAMPLE_CHUNKS), {
			status: 200,
			headers: { 'content-type': 'application/json' },
		});
	};

	const now = 1_700_000_000_000;
	const base = {
		apiKey: SECRET_KEY,
		fetchImpl,
		rateLimiter: limiter,
		rateLimitKey: 'client-a',
		now,
	};

	assert.equal((await handleRetrieveGet(getRequest('/retrieve?q=one'), base)).status, 200);
	assert.equal((await handleRetrieveGet(getRequest('/retrieve?q=two'), base)).status, 200);
	const limited = await handleRetrieveGet(getRequest('/retrieve?q=three'), base);
	assert.equal(limited.status, 429);
	assert.equal(calls, 2);

	const payload = await readJson(limited);
	assert.match(payload.error, /rate limit/i);
	assert.equal(limited.headers.get('Access-Control-Allow-Origin'), '*');
	assert.equal(limited.headers.get('Cache-Control'), 'no-store');
	assert.equal(limited.headers.get('Content-Type'), 'application/json');
	assert.equal(limited.headers.get('X-RateLimit-Limit'), '2');
	assert.equal(limited.headers.get('X-RateLimit-Remaining'), '0');
	assert.ok(Number(limited.headers.get('Retry-After')) >= 1);
	assert.doesNotMatch(JSON.stringify(payload), new RegExp(SECRET_KEY));

	// Invalid queries still short-circuit before the limiter consumes quota for a new key.
	const bad = await handleRetrieveGet(getRequest('/retrieve'), {
		...base,
		rateLimitKey: 'client-b',
	});
	assert.equal(bad.status, 400);
	assert.equal(
		(await handleRetrieveGet(getRequest('/retrieve?q=ok'), { ...base, rateLimitKey: 'client-b' }))
			.status,
		200,
	);
});
