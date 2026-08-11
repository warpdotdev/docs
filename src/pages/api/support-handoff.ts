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
};

const EMAIL_PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const KAPA_ID_PATTERN = /^[a-zA-Z0-9_-]{1,128}$/;
const MAX_QUESTION_LENGTH = 4_000;
const MAX_TRANSCRIPT_LENGTH = 50_000;
const MAX_PAGE_URL_LENGTH = 2_048;
const ALLOWED_PAGE_URL_HOSTS = new Set(['docs.warp.dev', 'localhost']);
const ALLOWED_PAGE_URL_SUFFIXES = ['.vercel.app'];

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
		const hostname = parsed.hostname.toLowerCase();
		if (ALLOWED_PAGE_URL_HOSTS.has(hostname)) return true;
		return ALLOWED_PAGE_URL_SUFFIXES.some((suffix) => hostname.endsWith(suffix));
	} catch {
		return false;
	}
}

export const POST: APIRoute = async ({ request }) => {
	const supportHandoffEndpointUrl = SUPPORT_HANDOFF_ENDPOINT_URL?.trim() || '';
	const supportHandoffSharedSecret = SUPPORT_HANDOFF_SHARED_SECRET?.trim() || '';
	if (!supportHandoffEndpointUrl || !supportHandoffSharedSecret) {
		return jsonError('Support handoff is not configured.', 503);
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

	const forwardHeaders: HeadersInit = {
		'content-type': 'application/json',
		authorization: `Bearer ${supportHandoffSharedSecret}`,
	};

	let upstreamResponse: Response;
	try {
		upstreamResponse = await fetch(supportHandoffEndpointUrl, {
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
