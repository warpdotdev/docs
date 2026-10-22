export const KAPA_CONVERSATION_HISTORY_OPTIONS = Object.freeze({
	enabled: true,
	maxThreads: 50,
});

export const KAPA_CONVERSATION_HISTORY_COPY = Object.freeze({
	title: 'Conversation history',
	empty: 'No saved conversations yet.',
	privacy: 'Saved only in this browser. Clearing removes all saved conversations from this device.',
	clear: 'Clear saved conversations',
	untitled: 'Untitled conversation',
});

export function getConversationHistoryView(threads, activeThreadId) {
	const items = threads.map((thread) => ({
		threadId: thread.threadId,
		title: thread.title.trim() || KAPA_CONVERSATION_HISTORY_COPY.untitled,
		isActive: thread.threadId === activeThreadId,
	}));

	return {
		...KAPA_CONVERSATION_HISTORY_COPY,
		canClear: items.length > 0,
		isEmpty: items.length === 0,
		items,
	};
}
