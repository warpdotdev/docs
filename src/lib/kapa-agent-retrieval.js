/**
 * Public agent-discoverable retrieval proxy for Warp docs.
 *
 * Agents call GET /retrieve?q=<question> without auth. This module keeps the
 * Kapa API key server-side, attributes traffic to a dedicated HTTP API
 * integration, and returns ranked {content, source_url} chunks.
 *
 * Spec: https://docs.kapa.ai/retrieval/guides/agent-discoverable-retrieval
 */

export const KAPA_DOCS_PROJECT_ID = '7c2b9650-9197-4f55-b827-6856480fa1e1';
/** Dedicated HTTP API integration for this public /retrieve endpoint. */
export const KAPA_RETRIEVAL_INTEGRATION_ID = '70a539ee-ca63-440c-88c0-7cb839ca57c9';
export const KAPA_RETRIEVAL_UPSTREAM_URL = `https://api.kapa.ai/query/v1/projects/${KAPA_DOCS_PROJECT_ID}/retrieval/`;
export const RETRIEVE_PATH = '/retrieve';
/** Bound query length so agents cannot flood the upstream with huge payloads. */
export const MAX_RETRIEVE_QUERY_LENGTH = 2_000;

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
 * @returns {Response}
 */
function jsonResponse(body, status) {
	return new Response(JSON.stringify(body), {
		status,
		headers: { ...RETRIEVE_RESPONSE_HEADERS },
	});
}

/**
 * CORS preflight for cross-origin agent callers.
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
 * @param {string} query
 * @returns {{ query: string, integration_id: string }}
 */
export function buildKapaRetrievalBody(query) {
	return {
		query,
		integration_id: KAPA_RETRIEVAL_INTEGRATION_ID,
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
