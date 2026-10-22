export const KAPA_CONVERSATION_HISTORY_STORAGE_KEY = 'warp_docs_kapa_conversation_history';
export const KAPA_CONVERSATION_TITLE_OVERRIDES_KEY = 'warp_docs_kapa_conversation_titles';

export const KAPA_CONVERSATION_HISTORY_OPTIONS = Object.freeze({
	enabled: true,
	maxThreads: 50,
	storageKey: KAPA_CONVERSATION_HISTORY_STORAGE_KEY,
});

export const KAPA_CONVERSATION_HISTORY_COPY = Object.freeze({
	title: 'Conversation history',
	empty: 'No saved conversations yet.',
	privacy:
		'Saved only in this browser. Renaming or deleting updates this device only. Clearing removes all saved conversations.',
	clear: 'Clear saved conversations',
	untitled: 'Untitled conversation',
	rename: 'Rename conversation',
	delete: 'Delete conversation',
	confirmDelete: 'Are you sure?',
	confirmDeleteAction: 'Delete',
	cancelDeleteAction: 'Cancel',
	renameSave: 'Save name',
	renameCancel: 'Cancel rename',
	current: 'Current conversation',
});

/** Lightened active-row tokens for static/contrast contracts. */
export const KAPA_HISTORY_ACTIVE_ROW_STYLE = Object.freeze({
	darkBackground: 'color-mix(in srgb, var(--sl-color-text-accent), var(--sl-color-black) 78%)',
	darkText: 'var(--sl-color-white)',
	lightBackground: 'color-mix(in srgb, var(--sl-color-text-accent), var(--sl-color-white) 92%)',
	lightText: 'var(--sl-color-black)',
});

function safeParseJson(raw) {
	if (!raw) return null;
	try {
		return JSON.parse(raw);
	} catch {
		return null;
	}
}

function readStorage(key) {
	try {
		return localStorage.getItem(key);
	} catch {
		return null;
	}
}

function writeStorage(key, value) {
	try {
		localStorage.setItem(key, value);
		return true;
	} catch {
		return false;
	}
}

function removeStorage(key) {
	try {
		localStorage.removeItem(key);
	} catch {
		// ignore quota / private mode failures
	}
}

export function readStoredHistoryThreads(storageKey = KAPA_CONVERSATION_HISTORY_STORAGE_KEY) {
	const parsed = safeParseJson(readStorage(storageKey));
	if (!parsed || !Array.isArray(parsed.threads)) return [];
	return parsed.threads
		.filter((thread) => thread && typeof thread.threadId === 'string')
		.sort((a, b) => (b.updatedAt ?? 0) - (a.updatedAt ?? 0));
}

export function writeStoredHistoryThreads(
	threads,
	storageKey = KAPA_CONVERSATION_HISTORY_STORAGE_KEY
) {
	const payload = JSON.stringify({
		version: 1,
		threads,
	});
	return writeStorage(storageKey, payload);
}

export function readTitleOverrides(key = KAPA_CONVERSATION_TITLE_OVERRIDES_KEY) {
	const parsed = safeParseJson(readStorage(key));
	if (!parsed || typeof parsed !== 'object' || Array.isArray(parsed)) return {};
	const overrides = {};
	for (const [threadId, title] of Object.entries(parsed)) {
		if (typeof title === 'string' && title.trim()) {
			overrides[threadId] = title.trim();
		}
	}
	return overrides;
}

export function writeTitleOverrides(overrides, key = KAPA_CONVERSATION_TITLE_OVERRIDES_KEY) {
	const cleaned = {};
	for (const [threadId, title] of Object.entries(overrides)) {
		if (typeof title === 'string' && title.trim()) {
			cleaned[threadId] = title.trim();
		}
	}
	if (Object.keys(cleaned).length === 0) {
		removeStorage(key);
		return true;
	}
	return writeStorage(key, JSON.stringify(cleaned));
}

export function validateRenameTitle(value) {
	const trimmed = typeof value === 'string' ? value.trim() : '';
	if (!trimmed) {
		return { ok: false, title: '', error: 'Name cannot be empty.' };
	}
	return { ok: true, title: trimmed, error: null };
}

/**
 * Rename is stored in an overlay key because the Chat SDK re-derives `title`
 * from the first question on every completed answer and would overwrite edits.
 */
export function renameStoredConversation(
	threadId,
	nextTitle,
	{
		storageKey = KAPA_CONVERSATION_HISTORY_STORAGE_KEY,
		overridesKey = KAPA_CONVERSATION_TITLE_OVERRIDES_KEY,
	} = {}
) {
	const validation = validateRenameTitle(nextTitle);
	if (!validation.ok) {
		return { ok: false, error: validation.error, threads: readStoredHistoryThreads(storageKey) };
	}
	const threads = readStoredHistoryThreads(storageKey);
	if (!threads.some((thread) => thread.threadId === threadId)) {
		return { ok: false, error: 'Conversation not found.', threads };
	}
	const overrides = readTitleOverrides(overridesKey);
	overrides[threadId] = validation.title;
	writeTitleOverrides(overrides, overridesKey);
	return { ok: true, error: null, title: validation.title, threads };
}

/** True local deletion from the browser history store (not a cosmetic hide). */
export function deleteStoredConversation(
	threadId,
	{
		storageKey = KAPA_CONVERSATION_HISTORY_STORAGE_KEY,
		overridesKey = KAPA_CONVERSATION_TITLE_OVERRIDES_KEY,
	} = {}
) {
	const existing = readStoredHistoryThreads(storageKey);
	const threads = existing.filter((thread) => thread.threadId !== threadId);
	const removed = threads.length !== existing.length;
	if (removed) {
		// Always write (including empty) so stale SDK in-memory threads cannot
		// reappear before the next provider remount/completed answer.
		writeStoredHistoryThreads(threads, storageKey);
	}
	const overrides = readTitleOverrides(overridesKey);
	if (overrides[threadId]) {
		delete overrides[threadId];
		writeTitleOverrides(overrides, overridesKey);
	}
	return { ok: removed, threads, deletedActiveCandidate: threadId };
}

export function clearStoredConversationHistory({
	storageKey = KAPA_CONVERSATION_HISTORY_STORAGE_KEY,
	overridesKey = KAPA_CONVERSATION_TITLE_OVERRIDES_KEY,
} = {}) {
	writeStoredHistoryThreads([], storageKey);
	removeStorage(overridesKey);
}

export function getConversationHistoryView(
	threads,
	activeThreadId,
	titleOverrides = {}
) {
	const items = threads.map((thread) => {
		const override = titleOverrides[thread.threadId];
		const generatedTitle = typeof thread.title === 'string' ? thread.title.trim() : '';
		return {
			threadId: thread.threadId,
			title: override || generatedTitle || KAPA_CONVERSATION_HISTORY_COPY.untitled,
			generatedTitle: generatedTitle || KAPA_CONVERSATION_HISTORY_COPY.untitled,
			isActive: thread.threadId === activeThreadId,
		};
	});

	return {
		...KAPA_CONVERSATION_HISTORY_COPY,
		canClear: items.length > 0,
		isEmpty: items.length === 0,
		items,
	};
}
