import assert from 'node:assert/strict';
import test from 'node:test';
import {
	KAPA_CONVERSATION_HISTORY_COPY,
	KAPA_CONVERSATION_HISTORY_OPTIONS,
	getConversationHistoryView,
} from './kapa-conversation-history.mjs';

test('uses native SDK threads in recency order and exposes their restore IDs', () => {
	const view = getConversationHistoryView(
		[
			{ threadId: 'most-recent', title: 'Latest question', updatedAt: 20 },
			{ threadId: 'older', title: 'Earlier question', updatedAt: 10 },
		],
		'older'
	);

	assert.equal(view.isEmpty, false);
	assert.equal(view.canClear, true);
	assert.deepEqual(view.items, [
		{ threadId: 'most-recent', title: 'Latest question', isActive: false },
		{ threadId: 'older', title: 'Earlier question', isActive: true },
	]);
});

test('renders the empty state and local-storage disclosure without creating a duplicate store', () => {
	const view = getConversationHistoryView([], null);

	assert.equal(view.isEmpty, true);
	assert.equal(view.canClear, false);
	assert.deepEqual(view.items, []);
	assert.equal(
		view.privacy,
		'Saved only in this browser. Clearing removes all saved conversations from this device.'
	);
	assert.deepEqual(KAPA_CONVERSATION_HISTORY_OPTIONS, {
		enabled: true,
		maxThreads: 50,
	});
	assert.equal(KAPA_CONVERSATION_HISTORY_COPY.clear, 'Clear saved conversations');
});
