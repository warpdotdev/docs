import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import test from 'node:test';
import { fileURLToPath } from 'node:url';
import {
	KAPA_CONVERSATION_HISTORY_COPY,
	KAPA_CONVERSATION_HISTORY_OPTIONS,
	KAPA_CONVERSATION_HISTORY_STORAGE_KEY,
	KAPA_CONVERSATION_TITLE_OVERRIDES_KEY,
	KAPA_HISTORY_ACTIVE_ROW_STYLE,
	canRestoreThread,
	clearStoredConversationHistory,
	deleteStoredConversation,
	getConversationHistoryView,
	getRestorableThread,
	hasOwnedHistoryStore,
	isOwnedHistoryStorageEvent,
	normalizeStoredThread,
	pruneTitleOverrides,
	readHistoryUiSnapshot,
	readStoredHistoryThreads,
	readTitleOverrides,
	renameStoredConversation,
	resolveRestoreAttempt,
	shouldPersistThreadId,
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

function validThread(threadId, title, updatedAt = 1) {
	return {
		threadId,
		title,
		createdAt: 1,
		updatedAt,
		qas: [
			{
				id: `${threadId}-qa`,
				question: title,
				answer: 'Answer',
				sources: [],
				files: [],
				toolCalls: [],
				reaction: null,
				isGenerationAborted: false,
			},
		],
	};
}

function seedThreads(threads) {
	writeStoredHistoryThreads(threads);
}

test('uses native SDK threads in recency order and exposes their restore IDs', () => {
	const view = getConversationHistoryView(
		[
			validThread('most-recent', 'Latest question', 20),
			validThread('older', 'Earlier question', 10),
		],
		'older',
		{}
	);

	assert.equal(view.isEmpty, false);
	assert.equal(view.canClear, true);
	assert.deepEqual(
		view.items.map((item) => item.threadId),
		['most-recent', 'older']
	);
	assert.equal(view.items[1].isActive, true);
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
	seedThreads([validThread('t1', 'Generated from first question', 2)]);

	const result = renameStoredConversation('t1', '  My custom name  ');
	assert.equal(result.ok, true);
	assert.equal(result.title, 'My custom name');
	assert.equal(readTitleOverrides().t1, 'My custom name');
	assert.equal(readStoredHistoryThreads()[0].title, 'Generated from first question');

	const view = getConversationHistoryView(readStoredHistoryThreads(), 't1', readTitleOverrides());
	assert.equal(view.items[0].title, 'My custom name');
	assert.equal(view.items[0].generatedTitle, 'Generated from first question');
});

test('rename validation failure leaves storage untouched', () => {
	installLocalStorageMock();
	seedThreads([validThread('t1', 'Keep me')]);
	writeTitleOverrides({ t1: 'Existing' });

	const result = renameStoredConversation('t1', '   ');
	assert.equal(result.ok, false);
	assert.equal(readTitleOverrides().t1, 'Existing');
});

test('delete removes the thread from browser storage and cleans title overrides', () => {
	installLocalStorageMock();
	seedThreads([validThread('keep', 'Keep', 3), validThread('drop', 'Drop', 2)]);
	writeTitleOverrides({ drop: 'Renamed drop', keep: 'Renamed keep' });

	const result = deleteStoredConversation('drop');
	assert.equal(result.ok, true);
	assert.deepEqual(
		readStoredHistoryThreads().map((thread) => thread.threadId),
		['keep']
	);
	assert.deepEqual(readTitleOverrides(), { keep: 'Renamed keep' });
});

test('deleting the last conversation writes an empty owned history store', () => {
	installLocalStorageMock();
	seedThreads([validThread('only', 'Only')]);
	writeTitleOverrides({ only: 'Solo' });

	const result = deleteStoredConversation('only');
	assert.equal(result.ok, true);
	assert.deepEqual(result.threads, []);
	assert.deepEqual(readStoredHistoryThreads(), []);
	assert.equal(hasOwnedHistoryStore(), true);
	assert.equal(memory.get(KAPA_CONVERSATION_TITLE_OVERRIDES_KEY), undefined);
});

test('clear removes history threads and rename metadata together', () => {
	installLocalStorageMock();
	seedThreads([validThread('t1', 'T')]);
	writeTitleOverrides({ t1: 'Custom' });

	clearStoredConversationHistory();
	assert.deepEqual(readStoredHistoryThreads(), []);
	assert.equal(memory.get(KAPA_CONVERSATION_TITLE_OVERRIDES_KEY), undefined);
});

test('stale row restore is blocked unless a fully normalized disk thread exists', () => {
	installLocalStorageMock();
	seedThreads([validThread('live', 'Live')]);

	assert.equal(canRestoreThread('missing'), false);
	assert.equal(resolveRestoreAttempt('missing').ok, false);
	assert.equal(resolveRestoreAttempt('live').ok, true);
	assert.equal(getRestorableThread('live')?.threadId, 'live');
});

test('cross-tab delete of inactive thread keeps active thread and prunes UI snapshot', () => {
	installLocalStorageMock();
	seedThreads([validThread('active', 'Active', 5), validThread('other', 'Other', 4)]);
	writeTitleOverrides({ active: 'A', other: 'O' });

	deleteStoredConversation('other');
	const snapshot = readHistoryUiSnapshot({ activeThreadId: 'active' });
	assert.equal(snapshot.activeThreadMissing, false);
	assert.deepEqual(
		snapshot.threads.map((thread) => thread.threadId),
		['active']
	);
	assert.deepEqual(snapshot.titleOverrides, { active: 'A' });
});

test('cross-tab delete of active thread marks active missing so UI can remount fresh', () => {
	installLocalStorageMock();
	seedThreads([validThread('active', 'Active', 5), validThread('other', 'Other', 4)]);

	deleteStoredConversation('active');
	const snapshot = readHistoryUiSnapshot({ activeThreadId: 'active' });
	assert.equal(snapshot.activeThreadMissing, true);
	assert.deepEqual(
		snapshot.threads.map((thread) => thread.threadId),
		['other']
	);
});

test('deleted thread cannot be re-persisted once owned store exists', () => {
	installLocalStorageMock();
	seedThreads([validThread('keep', 'Keep'), validThread('drop', 'Drop')]);
	deleteStoredConversation('drop');

	assert.equal(shouldPersistThreadId('drop'), false);
	assert.equal(shouldPersistThreadId('keep'), true);
	assert.equal(resolveRestoreAttempt('drop').ok, false);
});

test('storage-event helper recognizes history and title-overlay keys', () => {
	assert.equal(
		isOwnedHistoryStorageEvent({ key: KAPA_CONVERSATION_HISTORY_STORAGE_KEY }),
		true
	);
	assert.equal(
		isOwnedHistoryStorageEvent({ key: KAPA_CONVERSATION_TITLE_OVERRIDES_KEY }),
		true
	);
	assert.equal(isOwnedHistoryStorageEvent({ key: null }), true);
	assert.equal(isOwnedHistoryStorageEvent({ key: 'unrelated' }), false);
});

test('malformed threads and empty QA payloads are rejected by normalization', () => {
	assert.equal(normalizeStoredThread({ threadId: 'x' }), null);
	assert.equal(
		normalizeStoredThread({
			threadId: 'x',
			title: 't',
			createdAt: 1,
			updatedAt: 1,
			qas: [{ question: 'no id' }],
		}),
		null
	);
	installLocalStorageMock();
	writeStoredHistoryThreads([
		{
			threadId: 'bad',
			title: 'Bad',
			createdAt: 1,
			updatedAt: 1,
			qas: [{ question: 'missing id' }],
		},
		validThread('good', 'Good'),
	]);
	assert.deepEqual(
		readStoredHistoryThreads().map((thread) => thread.threadId),
		['good']
	);
});

test('confirmation copy contracts cover Escape cancel and announce labels', () => {
	assert.equal(KAPA_CONVERSATION_HISTORY_COPY.confirmDelete, 'Are you sure?');
	assert.equal(KAPA_CONVERSATION_HISTORY_COPY.cancelDeleteAction, 'Cancel');
	assert.equal(KAPA_CONVERSATION_HISTORY_COPY.confirmDeleteAction, 'Delete');
	assert.equal(KAPA_CONVERSATION_HISTORY_COPY.missingThread, 'That conversation is no longer saved on this device.');
});

test('overlay pruning drops titles for threads removed by delete eviction or clear', () => {
	installLocalStorageMock();
	seedThreads([validThread('keep', 'Keep'), validThread('drop', 'Drop')]);
	writeTitleOverrides({ keep: 'K', drop: 'D', orphan: 'O' });

	const afterDelete = pruneTitleOverrides(readStoredHistoryThreads());
	assert.deepEqual(afterDelete, { keep: 'K', drop: 'D' });

	deleteStoredConversation('drop');
	assert.deepEqual(readTitleOverrides(), { keep: 'K' });

	clearStoredConversationHistory();
	assert.deepEqual(readTitleOverrides(), {});
});

test('active-row style contract stays lightened with readable text tokens', () => {
	assert.match(KAPA_HISTORY_ACTIVE_ROW_STYLE.darkBackground, /78%/);
	assert.equal(KAPA_HISTORY_ACTIVE_ROW_STYLE.darkText, 'var(--sl-color-white)');
	assert.match(KAPA_HISTORY_ACTIVE_ROW_STYLE.lightBackground, /88%/);
	assert.equal(KAPA_HISTORY_ACTIVE_ROW_STYLE.lightText, 'var(--sl-color-gray-1)');
	assert.equal(
		KAPA_HISTORY_ACTIVE_ROW_STYLE.lightTitleSelector,
		":root[data-theme='light'] .sl-kapa-history__row[data-active='true'] .sl-kapa-history__open-title"
	);
	assert.equal(KAPA_HISTORY_ACTIVE_ROW_STYLE.lightTitleText, 'var(--sl-color-gray-1)');
	assert.equal(
		KAPA_HISTORY_ACTIVE_ROW_STYLE.lightRenameSelector,
		":root[data-theme='light'] .sl-kapa-history__rename input"
	);
	assert.equal(KAPA_HISTORY_ACTIVE_ROW_STYLE.lightRenameBackground, 'var(--sl-color-black)');
	assert.equal(KAPA_HISTORY_ACTIVE_ROW_STYLE.lightRenameText, 'var(--sl-color-gray-1)');

	const cssPath = join(dirname(fileURLToPath(import.meta.url)), '../components/KapaChatLauncher.css');
	const css = readFileSync(cssPath, 'utf8');
	assert.match(
		css,
		/:root\[data-theme='light'\]\s*\.sl-kapa-history__row\[data-active='true'\]\s*\.sl-kapa-history__open-title\s*\{[^}]*color:\s*var\(--sl-color-gray-1\)/s
	);
	assert.match(
		css,
		/:root\[data-theme='light'\]\s*\.sl-kapa-history__row\[data-active='true'\]\s*\.sl-kapa-history__open-title\s*\{[^}]*-webkit-text-fill-color:\s*var\(--sl-color-gray-1\)/s
	);
	assert.match(
		css,
		/:root\[data-theme='light'\]\s*\.sl-kapa-history__rename input\s*\{[^}]*background:\s*var\(--sl-color-black\)/s
	);
	assert.match(
		css,
		/:root\[data-theme='light'\]\s*\.sl-kapa-history__rename input\s*\{[^}]*color:\s*var\(--sl-color-gray-1\)/s
	);
	assert.match(
		css,
		/:root\[data-theme='light'\]\s*\.sl-kapa-history__rename input\s*\{[^}]*-webkit-text-fill-color:\s*var\(--sl-color-gray-1\)/s
	);
});
