import type { APIRoute } from 'astro';
import { SUPPORT_HANDOFF_ENDPOINT_URL, SUPPORT_HANDOFF_SHARED_SECRET } from 'astro:env/server';

export const prerender = false;

type HandoffPayload = {
	user_email?: unknown;
	question?: unknown;
	page_url?: unknown;
	conversation_transcript?: unknown;
	kapa_project_id?: unknown;
	kapa_thread_id?: unknown;
	kapa_conversation_url?: unknown;
	captcha_token?: unknown;
	captcha_header?: unknown;
};

const EMAIL_PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const KAPA_ID_PATTERN = /^[a-zA-Z0-9_-]{1,128}$/;
const MAX_QUESTION_LENGTH = 4_000;
const MAX_TRANSCRIPT_LENGTH = 50_000;
const MAX_PAGE_URL_LENGTH = 2_048;
const MAX_CAPTCHA_TOKEN_LENGTH = 4_096;
const ALLOWED_PAGE_URL_HOSTS = new Set(['docs.warp.dev', 'localhost']);
const DOCS_PREVIEW_HOSTNAME_PATTERN = /^docs-[a-z0-9]+(?:-[a-z0-9]+)*-warpdotdev\.vercel\.app$/;
const ALLOWED_CAPTCHA_HEADERS = new Set(['X-RECAPTCHA-ENTERPRISE-TOKEN', 'X-HCAPTCHA-TOKEN']);
const RATE_LIMIT_WINDOW_MS = 10 * 60 * 1000;
const RATE_LIMIT_MAX_REQUESTS = 5;
const rateLimitStore = new Map<string, { count: number; resetAt: number }>();

function asTrimmedString(value: unknown) {
	return typeof value === 'string' ? value.trim() : '';
}

function jsonError(message: string, status = 400) {
	return new Response(JSON.stringify({ message }), {
		status,
		headers: { 'content-type': 'application/json' },
	});
}

function buildKapaConversationUrl(kapaProjectId: string, kapaThreadId: string) {
	return `https://app.kapa.ai/${kapaProjectId}/conversations/${kapaThreadId}`;
}

function isAllowedPageUrl(url: string) {
	if (url.length > MAX_PAGE_URL_LENGTH) return false;
	try {
		const parsed = new URL(url);
		if (!['http:', 'https:'].includes(parsed.protocol)) return false;
		return isAllowedHostname(parsed.hostname);
	} catch {
		return false;
	}
}

function isAllowedHostname(hostname: string) {
	const lowercasedHostname = hostname.toLowerCase();
	if (ALLOWED_PAGE_URL_HOSTS.has(lowercasedHostname)) return true;
	return DOCS_PREVIEW_HOSTNAME_PATTERN.test(lowercasedHostname);
}

function isAllowedRequestOrigin(request: Request) {
	const originHeader = request.headers.get('origin');
	if (!originHeader) return false;
	try {
		const parsedOrigin = new URL(originHeader);
		if (!['http:', 'https:'].includes(parsedOrigin.protocol)) return false;
		return isAllowedHostname(parsedOrigin.hostname);
	} catch {
		return false;
	}
}

function getClientIp(request: Request) {
	// Vercel overwrites `x-forwarded-for` and strips external values to prevent
	// spoofing: https://vercel.com/docs/headers/request-headers#x-forwarded-for
	const forwardedFor = request.headers.get('x-forwarded-for');
	if (forwardedFor) {
		const firstIp = forwardedFor.split(',')[0]?.trim();
		if (firstIp) return firstIp;
	}
	const connectingIp = request.headers.get('cf-connecting-ip')?.trim();
	if (connectingIp) return connectingIp;
	const realIp = request.headers.get('x-real-ip')?.trim();
	if (realIp) return realIp;
	return 'unknown';
}

function isRateLimited(clientIp: string) {
	const now = Date.now();
	const existing = rateLimitStore.get(clientIp);
	if (!existing || existing.resetAt <= now) {
		rateLimitStore.set(clientIp, { count: 1, resetAt: now + RATE_LIMIT_WINDOW_MS });
		return false;
	}
	existing.count += 1;
	if (existing.count > RATE_LIMIT_MAX_REQUESTS) {
		return true;
	}
	rateLimitStore.set(clientIp, existing);
	return false;
}

export const POST: APIRoute = async ({ request }) => {
	const supportHandoffEndpointUrl = SUPPORT_HANDOFF_ENDPOINT_URL?.trim() || '';
	const supportHandoffSharedSecret = SUPPORT_HANDOFF_SHARED_SECRET?.trim() || '';
	if (!supportHandoffEndpointUrl || !supportHandoffSharedSecret) {
		return jsonError('Support handoff is not configured.', 503);
	}
	if (!isAllowedRequestOrigin(request)) {
		return jsonError('Request origin is not allowed.', 403);
	}
	const clientIp = getClientIp(request);
	if (isRateLimited(clientIp)) {
		return jsonError('Too many support handoff attempts. Please try again later.', 429);
	}

	let payload: HandoffPayload;
	try {
		payload = (await request.json()) as HandoffPayload;
	} catch {
		return jsonError('Invalid JSON payload.');
	}

	const userEmail = asTrimmedString(payload.user_email).toLowerCase();
	if (!EMAIL_PATTERN.test(userEmail)) {
		return jsonError('Please enter a valid email address.');
	}

	const question = asTrimmedString(payload.question);
	const pageUrl = asTrimmedString(payload.page_url);
	const conversationTranscript = asTrimmedString(payload.conversation_transcript);
	const kapaProjectId = asTrimmedString(payload.kapa_project_id);
	const kapaThreadId = asTrimmedString(payload.kapa_thread_id);
	const suppliedKapaConversationUrl = asTrimmedString(payload.kapa_conversation_url);
	const captchaToken = asTrimmedString(payload.captcha_token);
	const captchaHeader = asTrimmedString(payload.captcha_header);

	if (!question) return jsonError('A question is required.');
	if (question.length > MAX_QUESTION_LENGTH) return jsonError('Question is too long.');
	if (!pageUrl) return jsonError('The current page URL is required.');
	if (!isAllowedPageUrl(pageUrl)) return jsonError('Page URL is invalid or not allowed.');
	if (!conversationTranscript) return jsonError('Conversation transcript is required.');
	if (conversationTranscript.length > MAX_TRANSCRIPT_LENGTH) {
		return jsonError('Conversation transcript is too long.');
	}
	if (!kapaThreadId) return jsonError('Kapa thread ID is required.');
	if (!KAPA_ID_PATTERN.test(kapaThreadId)) return jsonError('Kapa thread ID is invalid.');
	if (!captchaToken) return jsonError('Captcha verification is required.');
	if (captchaToken.length > MAX_CAPTCHA_TOKEN_LENGTH) return jsonError('Captcha token is invalid.');
	if (!ALLOWED_CAPTCHA_HEADERS.has(captchaHeader)) return jsonError('Captcha token header is invalid.');
	if (kapaProjectId && !KAPA_ID_PATTERN.test(kapaProjectId)) {
		return jsonError('Kapa project ID is invalid.');
	}
	const derivedKapaConversationUrl =
		kapaProjectId && kapaThreadId
			? buildKapaConversationUrl(kapaProjectId, kapaThreadId)
			: '';
	if (kapaProjectId) {
		if (
			suppliedKapaConversationUrl &&
			suppliedKapaConversationUrl !== derivedKapaConversationUrl
		) {
			return jsonError('Kapa conversation URL does not match project/thread values.');
		}
	} else if (suppliedKapaConversationUrl) {
		return jsonError('Kapa project ID is required when a Kapa conversation URL is supplied.');
	}

	const forwardPayload = {
		user_email: userEmail,
		question,
		page_url: pageUrl,
		conversation_transcript: conversationTranscript,
		kapa_project_id: kapaProjectId || null,
		kapa_thread_id: kapaThreadId,
		kapa_conversation_url: derivedKapaConversationUrl || null,
		source: 'docs-kapa-custom-chat',
	};

	// DevX `gcp_front_docs_handoff` validates the shared secret the same way
	// Front webhooks do: as a `?secret=` query param (see
	// helper_flask.validate_front_webhook_secret). Bearer alone is ignored.
	const upstreamUrl = new URL(supportHandoffEndpointUrl);
	upstreamUrl.searchParams.set('secret', supportHandoffSharedSecret);

	const forwardHeaders: HeadersInit = {
		'content-type': 'application/json',
		[captchaHeader]: captchaToken,
	};

	let upstreamResponse: Response;
	try {
		upstreamResponse = await fetch(upstreamUrl.toString(), {
			method: 'POST',
			headers: forwardHeaders,
			body: JSON.stringify(forwardPayload),
		});
	} catch {
		return jsonError('Failed to reach support handoff service.', 502);
	}

	let upstreamData: unknown = null;
	try {
		upstreamData = await upstreamResponse.json();
	} catch {
		upstreamData = null;
	}

	if (!upstreamResponse.ok) {
		const upstreamMessage =
			upstreamData &&
			typeof upstreamData === 'object' &&
			'message' in upstreamData &&
			typeof upstreamData.message === 'string'
				? upstreamData.message
				: 'Support handoff failed.';
		return jsonError(upstreamMessage, upstreamResponse.status);
	}

	return new Response(
		JSON.stringify({
			message: 'Message sent to Warp Support.',
		}),
		{
			status: 200,
			headers: { 'content-type': 'application/json' },
		}
	);
};
