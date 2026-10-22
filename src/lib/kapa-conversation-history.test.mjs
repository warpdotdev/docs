import assert from 'node:assert/strict';
import test from 'node:test';
import {
	KAPA_CONVERSATION_HISTORY_COPY,
	KAPA_CONVERSATION_HISTORY_OPTIONS,
	KAPA_CONVERSATION_HISTORY_STORAGE_KEY,
	KAPA_CONVERSATION_TITLE_OVERRIDES_KEY,
	KAPA_HISTORY_ACTIVE_ROW_STYLE,
	clearStoredConversationHistory,
	deleteStoredConversation,
	getConversationHistoryView,
	readStoredHistoryThreads,
	readTitleOverrides,
	renameStoredConversation,
	validateRenameTitle,
	writeStoredHistoryThreads,
	writeTitleOverrides,
} from './kapa-conversation-history.mjs';

const memory = new Map();

function installLocalStorageMock() {
	memory.clear();
	globalThis.localStorage = {
		getItem(key) {
			return memory.has(key) ? memory.get(key) : null;
		},
		setItem(key, value) {
			memory.set(key, String(value));
		},
		removeItem(key) {
			memory.delete(key);
		},
	};
}

function seedThreads(threads) {
	writeStoredHistoryThreads(threads);
}

test('uses native SDK threads in recency order and exposes their restore IDs', () => {
	const view = getConversationHistoryView(
		[
			{ threadId: 'most-recent', title: 'Latest question', updatedAt: 20 },
			{ threadId: 'older', title: 'Earlier question', updatedAt: 10 },
		],
		'older',
		{}
	);

	assert.equal(view.isEmpty, false);
	assert.equal(view.canClear, true);
	assert.deepEqual(view.items, [
		{
			threadId: 'most-recent',
			title: 'Latest question',
			generatedTitle: 'Latest question',
			isActive: false,
		},
		{
			threadId: 'older',
			title: 'Earlier question',
			generatedTitle: 'Earlier question',
			isActive: true,
		},
	]);
});

test('renders the empty state and local-storage disclosure without creating a duplicate store', () => {
	const view = getConversationHistoryView([], null, {});

	assert.equal(view.isEmpty, true);
	assert.equal(view.canClear, false);
	assert.deepEqual(view.items, []);
	assert.match(view.privacy, /this browser/i);
	assert.deepEqual(KAPA_CONVERSATION_HISTORY_OPTIONS, {
		enabled: true,
		maxThreads: 50,
		storageKey: KAPA_CONVERSATION_HISTORY_STORAGE_KEY,
	});
	assert.equal(KAPA_CONVERSATION_HISTORY_COPY.clear, 'Clear saved conversations');
	assert.equal(KAPA_CONVERSATION_HISTORY_COPY.rename, 'Rename conversation');
	assert.equal(KAPA_CONVERSATION_HISTORY_COPY.delete, 'Delete conversation');
	assert.equal(KAPA_CONVERSATION_HISTORY_COPY.confirmDelete, 'Are you sure?');
});

test('validateRenameTitle rejects empty names and trims valid ones', () => {
	assert.deepEqual(validateRenameTitle('   '), {
		ok: false,
		title: '',
		error: 'Name cannot be empty.',
	});
	assert.deepEqual(validateRenameTitle('  Agents  '), {
		ok: true,
		title: 'Agents',
		error: null,
	});
});

test('rename persists an overlay title without dropping the stored thread', () => {
	installLocalStorageMock();
	seedThreads([
		{
			threadId: 't1',
			title: 'Generated from first question',
			createdAt: 1,
			updatedAt: 2,
			qas: [{ id: 'qa1', question: 'Generated from first question', answer: 'A' }],
		},
	]);

	const result = renameStoredConversation('t1', '  My custom name  ');
	assert.equal(result.ok, true);
	assert.equal(result.title, 'My custom name');
	assert.equal(readTitleOverrides().t1, 'My custom name');
	assert.equal(readStoredHistoryThreads().length, 1);
	assert.equal(readStoredHistoryThreads()[0].title, 'Generated from first question');

	const view = getConversationHistoryView(readStoredHistoryThreads(), 't1', readTitleOverrides());
	assert.equal(view.items[0].title, 'My custom name');
	assert.equal(view.items[0].generatedTitle, 'Generated from first question');
});

test('rename validation failure leaves storage untouched', () => {
	installLocalStorageMock();
	seedThreads([
		{ threadId: 't1', title: 'Keep me', createdAt: 1, updatedAt: 1, qas: [] },
	]);
	writeTitleOverrides({ t1: 'Existing' });

	const result = renameStoredConversation('t1', '   ');
	assert.equal(result.ok, false);
	assert.equal(readTitleOverrides().t1, 'Existing');
});

test('delete removes the thread from browser storage and cleans title overrides', () => {
	installLocalStorageMock();
	seedThreads([
		{ threadId: 'keep', title: 'Keep', createdAt: 1, updatedAt: 3, qas: [] },
		{ threadId: 'drop', title: 'Drop', createdAt: 1, updatedAt: 2, qas: [] },
	]);
	writeTitleOverrides({ drop: 'Renamed drop', keep: 'Renamed keep' });

	const result = deleteStoredConversation('drop');
	assert.equal(result.ok, true);
	assert.deepEqual(
		readStoredHistoryThreads().map((thread) => thread.threadId),
		['keep']
	);
	assert.deepEqual(readTitleOverrides(), { keep: 'Renamed keep' });
	assert.equal(memory.has(KAPA_CONVERSATION_HISTORY_STORAGE_KEY), true);
});

test('deleting the last conversation clears the history storage key entirely', () => {
	installLocalStorageMock();
	seedThreads([{ threadId: 'only', title: 'Only', createdAt: 1, updatedAt: 1, qas: [] }]);
	writeTitleOverrides({ only: 'Solo' });

	const result = deleteStoredConversation('only');
	assert.equal(result.ok, true);
	assert.deepEqual(result.threads, []);
	assert.deepEqual(readStoredHistoryThreads(), []);
	assert.equal(memory.get(KAPA_CONVERSATION_TITLE_OVERRIDES_KEY), undefined);
});

test('clear removes history threads and rename metadata together', () => {
	installLocalStorageMock();
	seedThreads([{ threadId: 't1', title: 'T', createdAt: 1, updatedAt: 1, qas: [] }]);
	writeTitleOverrides({ t1: 'Custom' });

	clearStoredConversationHistory();
	assert.deepEqual(readStoredHistoryThreads(), []);
	assert.equal(memory.get(KAPA_CONVERSATION_TITLE_OVERRIDES_KEY), undefined);
});

test('active-row style contract stays lightened with readable text tokens', () => {
	assert.match(KAPA_HISTORY_ACTIVE_ROW_STYLE.darkBackground, /78%/);
	assert.equal(KAPA_HISTORY_ACTIVE_ROW_STYLE.darkText, 'var(--sl-color-white)');
	assert.match(KAPA_HISTORY_ACTIVE_ROW_STYLE.lightBackground, /92%/);
	assert.equal(KAPA_HISTORY_ACTIVE_ROW_STYLE.lightText, 'var(--sl-color-black)');
});

test('row control copy covers rename delete and confirmation states', () => {
	assert.equal(KAPA_CONVERSATION_HISTORY_COPY.confirmDeleteAction, 'Delete');
	assert.equal(KAPA_CONVERSATION_HISTORY_COPY.cancelDeleteAction, 'Cancel');
	assert.equal(KAPA_CONVERSATION_HISTORY_COPY.renameSave, 'Save name');
	assert.equal(KAPA_CONVERSATION_HISTORY_COPY.renameCancel, 'Cancel rename');
	assert.equal(KAPA_CONVERSATION_HISTORY_COPY.current, 'Current conversation');
});
