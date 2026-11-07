export const KAPA_CONVERSATION_HISTORY_STORAGE_KEY = 'warp_docs_kapa_conversation_history';
export const KAPA_CONVERSATION_TITLE_OVERRIDES_KEY = 'warp_docs_kapa_conversation_titles';
/** Last active thread id for reload continuity (separate from the history store). */
export const KAPA_ACTIVE_THREAD_STORAGE_KEY = 'warp_docs_kapa_thread_id';

export const KAPA_CONVERSATION_HISTORY_OPTIONS = Object.freeze({
	enabled: true,
	maxThreads: 50,
	storageKey: KAPA_CONVERSATION_HISTORY_STORAGE_KEY,
});

export const KAPA_CONVERSATION_HISTORY_COPY = Object.freeze({
	title: 'Conversation history',
	empty: 'No saved conversations yet.',
	privacy: 'Saved only in this browser. Renaming or deleting updates this device only.',
	untitled: 'Untitled conversation',
	rename: 'Rename conversation',
	delete: 'Delete conversation',
	confirmDelete: 'Are you sure?',
	confirmDeleteAction: 'Delete',
	cancelDeleteAction: 'Cancel',
	renameSave: 'Save name',
	renameCancel: 'Cancel rename',
	current: 'Current conversation',
	missingThread: 'That conversation is no longer saved on this device.',
});

/** Lightened active-row tokens for static/contrast contracts. */
export const KAPA_HISTORY_ACTIVE_ROW_STYLE = Object.freeze({
	darkBackground: 'color-mix(in srgb, var(--sl-color-text-accent), var(--sl-color-black) 78%)',
	darkText: 'var(--sl-color-white)',
	lightBackground: 'color-mix(in srgb, var(--sl-color-text-accent), var(--sl-color-black) 88%)',
	lightText: 'var(--sl-color-gray-1)',
	/** Element-specific light title paint; row `color` alone is not enough on buttons. */
	lightTitleSelector:
		":root[data-theme='light'] .sl-kapa-history__row[data-active='true'] .sl-kapa-history__open-title",
	lightTitleText: 'var(--sl-color-gray-1)',
	lightRenameSelector: ":root[data-theme='light'] .sl-kapa-history__rename input",
	lightRenameBackground: 'var(--sl-color-black)',
	lightRenameText: 'var(--sl-color-gray-1)',
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

function objectItems(value) {
	return Array.isArray(value)
		? value.filter((item) => item !== null && typeof item === 'object')
		: [];
}

/** Mirrors Chat SDK QA normalization so unrestorable rows are never listed. */
export function normalizeStoredQA(value) {
	if (!value || typeof value !== 'object') return null;
	const raw = value;
	if (typeof raw.id !== 'string' || raw.id.length === 0) return null;
	const rawThinking = raw.thinking;
	const thinking =
		rawThinking && typeof rawThinking.startedAt === 'number'
			? {
					startedAt: rawThinking.startedAt,
					completedAt:
						typeof rawThinking.completedAt === 'number'
							? rawThinking.completedAt
							: rawThinking.startedAt,
				}
			: undefined;
	return {
		id: raw.id,
		question: typeof raw.question === 'string' ? raw.question : '',
		answer: typeof raw.answer === 'string' ? raw.answer : '',
		sources: objectItems(raw.sources),
		files: objectItems(raw.files),
		toolCalls: objectItems(raw.toolCalls),
		reaction: raw.reaction === 'upvote' || raw.reaction === 'downvote' ? raw.reaction : null,
		isGenerationAborted: raw.isGenerationAborted === true,
		isFeedbackSubmissionEnabled: true,
		status: 'completed',
		metadata: {
			is_uncertain:
				typeof raw.metadata === 'object' &&
				raw.metadata !== null &&
				raw.metadata.is_uncertain === true,
		},
		thinking,
	};
}

/** Mirrors Chat SDK thread normalization requirements. */
export function normalizeStoredThread(value) {
	if (!value || typeof value !== 'object') return null;
	const thread = value;
	if (
		typeof thread.threadId !== 'string' ||
		thread.threadId.length === 0 ||
		typeof thread.title !== 'string' ||
		typeof thread.createdAt !== 'number' ||
		typeof thread.updatedAt !== 'number' ||
		!Array.isArray(thread.qas)
	) {
		return null;
	}
	const qas = thread.qas.map(normalizeStoredQA).filter((qa) => qa !== null);
	if (qas.length === 0) return null;
	return {
		threadId: thread.threadId,
		title: thread.title,
		createdAt: thread.createdAt,
		updatedAt: thread.updatedAt,
		qas,
	};
}

export function hasOwnedHistoryStore(storageKey = KAPA_CONVERSATION_HISTORY_STORAGE_KEY) {
	return readStorage(storageKey) !== null;
}

export function readStoredHistoryThreads(storageKey = KAPA_CONVERSATION_HISTORY_STORAGE_KEY) {
	const parsed = safeParseJson(readStorage(storageKey));
	if (!parsed || !Array.isArray(parsed.threads)) return [];
	return parsed.threads
		.map(normalizeStoredThread)
		.filter((thread) => thread !== null)
		.sort((a, b) => b.updatedAt - a.updatedAt);
}

export function writeStoredHistoryThreads(
	threads,
	storageKey = KAPA_CONVERSATION_HISTORY_STORAGE_KEY
) {
	const normalized = threads.map(normalizeStoredThread).filter((thread) => thread !== null);
	const payload = JSON.stringify({
		version: 1,
		threads: normalized,
	});
	return writeStorage(storageKey, payload);
}

export function getRestorableThread(
	threadId,
	storageKey = KAPA_CONVERSATION_HISTORY_STORAGE_KEY
) {
	if (typeof threadId !== 'string' || threadId.length === 0) return null;
	return readStoredHistoryThreads(storageKey).find((thread) => thread.threadId === threadId) || null;
}

export function canRestoreThread(threadId, storageKey = KAPA_CONVERSATION_HISTORY_STORAGE_KEY) {
	return getRestorableThread(threadId, storageKey) !== null;
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

export function pruneTitleOverrides(
	threads,
	overridesKey = KAPA_CONVERSATION_TITLE_OVERRIDES_KEY
) {
	const liveIds = new Set(
		(Array.isArray(threads) ? threads : []).map((thread) => thread.threadId).filter(Boolean)
	);
	const current = readTitleOverrides(overridesKey);
	const next = {};
	for (const [threadId, title] of Object.entries(current)) {
		if (liveIds.has(threadId)) next[threadId] = title;
	}
	writeTitleOverrides(next, overridesKey);
	return next;
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
		// reappear before the next provider remount or completed answer.
		writeStoredHistoryThreads(threads, storageKey);
	}
	pruneTitleOverrides(threads, overridesKey);
	return { ok: removed, threads, deletedActiveCandidate: threadId };
}

export function clearStoredConversationHistory({
	storageKey = KAPA_CONVERSATION_HISTORY_STORAGE_KEY,
	overridesKey = KAPA_CONVERSATION_TITLE_OVERRIDES_KEY,
} = {}) {
	writeStoredHistoryThreads([], storageKey);
	removeStorage(overridesKey);
}

/**
 * Snapshot used by the UI and by storage-event handlers.
 * Disk is authoritative whenever the owned history key exists.
 */
export function readHistoryUiSnapshot({
	storageKey = KAPA_CONVERSATION_HISTORY_STORAGE_KEY,
	overridesKey = KAPA_CONVERSATION_TITLE_OVERRIDES_KEY,
	sdkThreads = [],
	activeThreadId = null,
} = {}) {
	const owned = hasOwnedHistoryStore(storageKey);
	const threads = owned ? readStoredHistoryThreads(storageKey) : sdkThreads.map(normalizeStoredThread).filter(Boolean);
	const titleOverrides = pruneTitleOverrides(threads, overridesKey);
	const activeStillPresent =
		typeof activeThreadId === 'string' &&
		activeThreadId.length > 0 &&
		threads.some((thread) => thread.threadId === activeThreadId);
	return {
		owned,
		threads,
		titleOverrides,
		activeThreadMissing: Boolean(activeThreadId) && owned && !activeStillPresent,
		view: getConversationHistoryView(threads, activeThreadId, titleOverrides),
	};
}

export function isOwnedHistoryStorageEvent(event, {
	storageKey = KAPA_CONVERSATION_HISTORY_STORAGE_KEY,
	overridesKey = KAPA_CONVERSATION_TITLE_OVERRIDES_KEY,
} = {}) {
	if (!event) return false;
	// A null key means clear() wiped the whole origin storage.
	if (event.key === null) return true;
	return event.key === storageKey || event.key === overridesKey;
}

/**
 * Pure decision helper for restore attempts.
 * Never allow native restore unless a fully normalized disk thread exists.
 */
export function resolveRestoreAttempt(threadId, storageKey = KAPA_CONVERSATION_HISTORY_STORAGE_KEY) {
	const thread = getRestorableThread(threadId, storageKey);
	if (!thread) {
		return {
			ok: false,
			reason: 'missing-or-invalid',
			thread: null,
			message: KAPA_CONVERSATION_HISTORY_COPY.missingThread,
		};
	}
	return { ok: true, reason: null, thread, message: null };
}

/**
 * After local deletion, SDK memory may still hold the thread. Callers must not
 * re-persist deleted IDs; this helper models the guard used before any upsert path.
 */
export function shouldPersistThreadId(threadId, storageKey = KAPA_CONVERSATION_HISTORY_STORAGE_KEY) {
	if (!hasOwnedHistoryStore(storageKey)) return true;
	return canRestoreThread(threadId, storageKey);
}

export function readActiveThreadId(key = KAPA_ACTIVE_THREAD_STORAGE_KEY) {
	const value = readStorage(key);
	return typeof value === 'string' && value.length > 0 ? value : null;
}

/**
 * Persist the live thread id only when the owned history store still allows it.
 * Deleted IDs are cleared instead of rewritten so reload cannot resurrect them.
 */
export function writeActiveThreadId(
	threadId,
	{
		activeKey = KAPA_ACTIVE_THREAD_STORAGE_KEY,
		storageKey = KAPA_CONVERSATION_HISTORY_STORAGE_KEY,
	} = {}
) {
	if (typeof threadId !== 'string' || threadId.length === 0) {
		removeStorage(activeKey);
		return false;
	}
	if (!shouldPersistThreadId(threadId, storageKey)) {
		removeStorage(activeKey);
		return false;
	}
	return writeStorage(activeKey, threadId);
}

export function clearActiveThreadId(key = KAPA_ACTIVE_THREAD_STORAGE_KEY) {
	removeStorage(key);
}

/**
 * Pure mount-time restore decision.
 * Handles missing/stale keys, already-active sessions (StrictMode re-entry),
 * and the shouldPersistThreadId invariant before any SDK restore call.
 *
 * @param {string | null | undefined} savedThreadId
 * @param {{
 *   currentThreadId?: string | null,
 *   storageKey?: string
 * }} [options]
 * @returns {{
 *   action: 'none' | 'already-active' | 'clear-stale' | 'restore',
 *   threadId: string | null,
 *   message: string | null,
 *   reason: string | null
 * }}
 */
export function resolveMountRestore(
	savedThreadId,
	{
		currentThreadId = null,
		storageKey = KAPA_CONVERSATION_HISTORY_STORAGE_KEY,
	} = {}
) {
	if (typeof savedThreadId !== 'string' || savedThreadId.length === 0) {
		return { action: 'none', threadId: null, message: null, reason: 'no-saved-id' };
	}
	if (currentThreadId === savedThreadId) {
		return {
			action: 'already-active',
			threadId: savedThreadId,
			message: null,
			reason: 'already-restored',
		};
	}
	const attempt = resolveRestoreAttempt(savedThreadId, storageKey);
	if (!attempt.ok) {
		return {
			action: 'clear-stale',
			threadId: savedThreadId,
			message: attempt.message,
			reason: attempt.reason,
		};
	}
	if (!shouldPersistThreadId(savedThreadId, storageKey)) {
		return {
			action: 'clear-stale',
			threadId: savedThreadId,
			message: KAPA_CONVERSATION_HISTORY_COPY.missingThread,
			reason: 'deleted-owned-id',
		};
	}
	return {
		action: 'restore',
		threadId: savedThreadId,
		message: null,
		reason: null,
	};
}

/**
 * Decide whether deleting a thread requires a keyed ChatSurface remount and
 * whether that remount should land in history (remaining threads) or a fresh chat.
 *
 * @param {{ deletedThreadId?: string | null, activeThreadId?: string | null, remainingThreadCount?: number }} [input]
 * @returns {{ remount: boolean, openHistory: boolean, reason: string }}
 */
export function resolvePostDeleteNavigation({
	deletedThreadId,
	activeThreadId = null,
	remainingThreadCount = 0,
} = {}) {
	const deletedActive =
		typeof deletedThreadId === 'string' &&
		deletedThreadId.length > 0 &&
		deletedThreadId === activeThreadId;
	if (!deletedActive) {
		return {
			remount: false,
			openHistory: false,
			reason: 'inactive-delete',
		};
	}
	if (remainingThreadCount > 0) {
		return {
			remount: true,
			openHistory: true,
			reason: 'active-delete-with-remaining',
		};
	}
	return {
		remount: true,
		openHistory: false,
		reason: 'active-delete-empty',
	};
}

export function getConversationHistoryView(threads, activeThreadId, titleOverrides = {}) {
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
		isEmpty: items.length === 0,
		items,
	};
}
