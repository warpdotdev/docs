import type { APIRoute } from 'astro';
import { SUPPORT_HANDOFF_ENDPOINT_URL, SUPPORT_HANDOFF_SHARED_SECRET } from 'astro:env/server';

export const prerender = false;
const DEFAULT_SUPPORT_HANDOFF_ENDPOINT_URL =
	'https://gcp-front-docs-handoff-66982094909.us-east4.run.app';

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

export const POST: APIRoute = async ({ request }) => {
	const supportHandoffEndpointUrl =
		SUPPORT_HANDOFF_ENDPOINT_URL || DEFAULT_SUPPORT_HANDOFF_ENDPOINT_URL;
	if (!supportHandoffEndpointUrl) {
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
	if (!pageUrl) return jsonError('The current page URL is required.');
	if (!conversationTranscript) return jsonError('Conversation transcript is required.');
	if (!kapaThreadId) return jsonError('Kapa thread ID is required.');
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
	};
	if (SUPPORT_HANDOFF_SHARED_SECRET) {
		forwardHeaders.authorization = `Bearer ${SUPPORT_HANDOFF_SHARED_SECRET}`;
	}

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
			message: 'Support ticket created.',
			...(upstreamData && typeof upstreamData === 'object' ? upstreamData : {}),
		}),
		{
			status: 200,
			headers: { 'content-type': 'application/json' },
		}
	);
};
