/**
 * Public agent-discoverable retrieval proxy for Warp docs.
 *
 * Agents call GET /retrieve?q=<question> without auth. This module keeps the
 * Kapa API key server-side, attributes traffic to a dedicated HTTP API
 * integration, and returns ranked {content, source_url} chunks.
 *
 * Spec: https://docs.kapa.ai/retrieval/guides/agent-discoverable-retrieval
 *
 * Abuse controls: an in-process fixed-window limit (per client IP) rejects
 * excess GET traffic with 429 while leaving OPTIONS preflight uncounted.
 * Pair this with a Vercel Firewall `rate_limit` rule on path `/retrieve` for
 * multi-region enforcement — `vercel.json` cannot express rate_limit actions.
 */

export const KAPA_DOCS_PROJECT_ID = '7c2b9650-9197-4f55-b827-6856480fa1e1';
/** Dedicated HTTP API integration for this public /retrieve endpoint. */
export const KAPA_RETRIEVAL_INTEGRATION_ID = '70a539ee-ca63-440c-88c0-7cb839ca57c9';
export const KAPA_RETRIEVAL_UPSTREAM_URL = `https://api.kapa.ai/query/v1/projects/${KAPA_DOCS_PROJECT_ID}/retrieval/`;
export const RETRIEVE_PATH = '/retrieve';
/** Bound query length so agents cannot flood the upstream with huge payloads. */
export const MAX_RETRIEVE_QUERY_LENGTH = 2_000;
/** Default fixed-window length for the in-process GET rate limit. */
export const RETRIEVE_RATE_LIMIT_WINDOW_MS = 60_000;
/** Default max GETs per client key inside each window. */
export const RETRIEVE_RATE_LIMIT_MAX = 60;

export const RETRIEVE_RESPONSE_HEADERS = Object.freeze({
	'Content-Type': 'application/json',
	'Cache-Control': 'no-store',
	'Access-Control-Allow-Origin': '*',
	'Access-Control-Allow-Methods': 'GET, OPTIONS',
	'Access-Control-Allow-Headers': 'Content-Type',
});

/**
 * @param {unknown} value
 * @returns {string}
 */
function asTrimmedString(value) {
	return typeof value === 'string' ? value.trim() : '';
}

/**
 * @param {unknown} body
 * @param {number} status
 * @param {Record<string, string>} [extraHeaders]
 * @returns {Response}
 */
function jsonResponse(body, status, extraHeaders = {}) {
	return new Response(JSON.stringify(body), {
		status,
		headers: { ...RETRIEVE_RESPONSE_HEADERS, ...extraHeaders },
	});
}

/**
 * Fixed-window rate limiter. Injectable for tests; default instance is
 * process-local (best-effort on multi-instance serverless).
 *
 * @param {{ windowMs?: number, max?: number }} [options]
 */
export function createFixedWindowRateLimiter(options = {}) {
	const windowMs = options.windowMs ?? RETRIEVE_RATE_LIMIT_WINDOW_MS;
	const max = options.max ?? RETRIEVE_RATE_LIMIT_MAX;
	/** @type {Map<string, { count: number, resetAt: number }>} */
	const buckets = new Map();

	return {
		windowMs,
		max,
		/**
		 * @param {string} key
		 * @param {number} [now]
		 * @returns {{ allowed: boolean, limit: number, remaining: number, resetAt: number }}
		 */
		check(key, now = Date.now()) {
			const existing = buckets.get(key);
			if (!existing || now >= existing.resetAt) {
				const resetAt = now + windowMs;
				buckets.set(key, { count: 1, resetAt });
				return { allowed: true, limit: max, remaining: max - 1, resetAt };
			}
			if (existing.count >= max) {
				return {
					allowed: false,
					limit: max,
					remaining: 0,
					resetAt: existing.resetAt,
				};
			}
			existing.count += 1;
			return {
				allowed: true,
				limit: max,
				remaining: Math.max(0, max - existing.count),
				resetAt: existing.resetAt,
			};
		},
		/** Test helper. */
		reset() {
			buckets.clear();
		},
	};
}

const defaultRateLimiter = createFixedWindowRateLimiter();

/**
 * Best-effort client key for rate limiting (first X-Forwarded-For hop).
 * @param {Request} request
 * @returns {string}
 */
export function getRetrieveClientKey(request) {
	const forwarded = asTrimmedString(request.headers.get('x-forwarded-for'));
	if (forwarded) {
		const first = asTrimmedString(forwarded.split(',')[0] ?? '');
		if (first) return first;
	}
	const realIp = asTrimmedString(request.headers.get('x-real-ip'));
	if (realIp) return realIp;
	return 'unknown';
}

/**
 * CORS preflight for cross-origin agent callers.
 * Not rate-limited — browsers must complete OPTIONS before GET.
 * @returns {Response}
 */
export function handleRetrieveOptions() {
	return new Response(null, {
		status: 204,
		headers: { ...RETRIEVE_RESPONSE_HEADERS },
	});
}

/**
 * @param {URL | string} requestUrl
 * @returns {string}
 */
export function getRetrieveQuery(requestUrl) {
	const url = typeof requestUrl === 'string' ? new URL(requestUrl, 'http://localhost') : requestUrl;
	return asTrimmedString(url.searchParams.get('q'));
}

/**
 * Validate the public `q` query parameter.
 * @param {string} query
 * @returns {{ ok: true, query: string } | { ok: false, response: Response }}
 */
export function validateRetrieveQuery(query) {
	if (!query) {
		return {
			ok: false,
			response: jsonResponse(
				{ error: 'Pass the question as the q query parameter.' },
				400,
			),
		};
	}
	if (query.length > MAX_RETRIEVE_QUERY_LENGTH) {
		return {
			ok: false,
			response: jsonResponse(
				{
					error: `Query exceeds the maximum length of ${MAX_RETRIEVE_QUERY_LENGTH} characters.`,
				},
				400,
			),
		};
	}
	return { ok: true, query };
}

/**
 * Build the upstream Kapa retrieval request body.
 *
 * `redact_query: true` is defense-in-depth so raw agent questions are not kept
 * in Kapa analytics text. Project-level user-message PII masking (dashboard)
 * still applies separately when enabled.
 *
 * @param {string} query
 * @returns {{ query: string, integration_id: string, redact_query: true }}
 */
export function buildKapaRetrievalBody(query) {
	return {
		query,
		integration_id: KAPA_RETRIEVAL_INTEGRATION_ID,
		redact_query: true,
	};
}

/**
 * GET /retrieve handler. Keeps the API key server-side; never forwards
 * arbitrary client headers or reflects secrets in responses.
 *
 * @param {Request} request
 * @param {{
 *   apiKey?: string | null | undefined,
 *   fetchImpl?: typeof fetch,
 *   rateLimiter?: { check: (key: string, now?: number) => { allowed: boolean, limit: number, remaining: number, resetAt: number } } | null,
 *   rateLimitKey?: string,
 *   now?: number,
 * }} [options]
 * @returns {Promise<Response>}
 */
export async function handleRetrieveGet(request, options = {}) {
	const apiKey = asTrimmedString(options.apiKey);
	if (!apiKey) {
		return jsonResponse({ error: 'Retrieval proxy is not configured.' }, 500);
	}

	const queryResult = validateRetrieveQuery(getRetrieveQuery(request.url));
	if (!queryResult.ok) return queryResult.response;

	const rateLimiter =
		options.rateLimiter === null
			? null
			: (options.rateLimiter ?? defaultRateLimiter);
	if (rateLimiter) {
		const key = options.rateLimitKey ?? getRetrieveClientKey(request);
		const verdict = rateLimiter.check(key, options.now);
		if (!verdict.allowed) {
			const retryAfterSec = Math.max(
				1,
				Math.ceil((verdict.resetAt - (options.now ?? Date.now())) / 1000),
			);
			return jsonResponse(
				{ error: 'Rate limit exceeded. Try again later.' },
				429,
				{
					'Retry-After': String(retryAfterSec),
					'X-RateLimit-Limit': String(verdict.limit),
					'X-RateLimit-Remaining': '0',
				},
			);
		}
	}

	const fetchImpl = options.fetchImpl ?? globalThis.fetch;
	let upstreamResponse;
	try {
		upstreamResponse = await fetchImpl(KAPA_RETRIEVAL_UPSTREAM_URL, {
			method: 'POST',
			headers: {
				'X-API-KEY': apiKey,
				'Content-Type': 'application/json',
			},
			body: JSON.stringify(buildKapaRetrievalBody(queryResult.query)),
		});
	} catch {
		// Do not log the request or key — secrets must never enter logs.
		return jsonResponse({ error: 'Failed to reach retrieval service.' }, 502);
	}

	const upstreamBody = await upstreamResponse.text();
	const contentType = upstreamResponse.headers.get('content-type') || 'application/json';

	return new Response(upstreamBody, {
		status: upstreamResponse.status,
		headers: {
			...RETRIEVE_RESPONSE_HEADERS,
			'Content-Type': contentType.includes('json') ? 'application/json' : contentType,
		},
	});
}
