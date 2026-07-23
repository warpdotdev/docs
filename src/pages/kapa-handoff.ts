import type { APIRoute } from 'astro';

export const prerender = false;

type HandoffPayload = {
	replyToEmail: string;
	note?: string;
	pageUrl?: string;
	threadId?: string | null;
	conversationCount?: number;
	conversationTranscript?: string;
	askedAt?: string;
};

function isValidEmail(value: string) {
	return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
}

function truncate(value: string, maxLength: number) {
	if (value.length <= maxLength) return value;
	return `${value.slice(0, maxLength)}…`;
}

export const POST: APIRoute = async ({ request }) => {
	let payload: HandoffPayload;
	try {
		payload = await request.json();
	} catch {
		return new Response(JSON.stringify({ error: 'Invalid JSON payload.' }), {
			status: 400,
			headers: { 'content-type': 'application/json' },
		});
	}

	const replyToEmail = payload.replyToEmail?.trim() ?? '';
	if (!replyToEmail || !isValidEmail(replyToEmail)) {
		return new Response(JSON.stringify({ error: 'A valid email address is required.' }), {
			status: 400,
			headers: { 'content-type': 'application/json' },
		});
	}

	const webhookUrl = process.env.KAPA_HANDOFF_WEBHOOK_URL?.trim();
	const transcript = payload.conversationTranscript?.trim() || 'No transcript provided.';
	const ticketBody = [
		`Reply-to email: ${replyToEmail}`,
		`Asked at: ${payload.askedAt || new Date().toISOString()}`,
		`Page URL: ${payload.pageUrl || 'Unknown page'}`,
		`Thread ID: ${payload.threadId || 'No thread ID yet'}`,
		`Conversation turns: ${payload.conversationCount ?? 0}`,
		'',
		'User note:',
		payload.note?.trim() || '(none)',
		'',
		'Conversation transcript:',
		transcript,
	].join('\n');

	if (webhookUrl) {
		const webhookResponse = await fetch(webhookUrl, {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({
				subject: '[Docs AI handoff] New support ticket request',
				replyToEmail,
				note: payload.note?.trim() || '',
				pageUrl: payload.pageUrl || '',
				threadId: payload.threadId || null,
				conversationCount: payload.conversationCount ?? 0,
				conversationTranscript: transcript,
				ticketBody,
			}),
		});

		if (!webhookResponse.ok) {
			return new Response(JSON.stringify({ error: 'Unable to deliver ticket to handoff webhook.' }), {
				status: 502,
				headers: { 'content-type': 'application/json' },
			});
		}

		return new Response(JSON.stringify({ ok: true, mode: 'webhook' }), {
			status: 200,
			headers: { 'content-type': 'application/json' },
		});
	}

	console.info(
		'[kapa-handoff-preview] Received handoff request:\n',
		truncate(ticketBody, 6000)
	);

	return new Response(
		JSON.stringify({
			ok: true,
			mode: 'preview',
			preview: {
				replyToEmail,
				threadId: payload.threadId || null,
				conversationCount: payload.conversationCount ?? 0,
			},
		}),
		{
			status: 200,
			headers: { 'content-type': 'application/json' },
		}
	);
};
