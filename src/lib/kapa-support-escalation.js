/** Show the support CTA on this 1-based response ordinal (the third assistant reply). */
export const SUPPORT_ESCALATION_CONVERSATION_LENGTH_THRESHOLD = 3;

/**
 * Whether the Kapa chat support CTA should appear for a specific answer card.
 *
 * Rules:
 * - Empty answers never show a CTA.
 * - A thumbs-down shows the CTA only on that downvoted response.
 * - The conversation-length threshold pins a CTA only on response #3
 *   (0-based index threshold - 1), not on later responses.
 *
 * @param {{
 *   answer?: string | null;
 *   responseIndex: number;
 *   conversationLength: number;
 *   isDownvoted: boolean;
 * }} options
 * @returns {boolean}
 */
export function shouldShowSupportEscalation({
	answer,
	responseIndex,
	conversationLength,
	isDownvoted,
}) {
	if (typeof answer !== 'string' || !answer.trim()) return false;
	if (isDownvoted === true) return true;
	if (typeof responseIndex !== 'number' || responseIndex < 0) return false;
	if (conversationLength < SUPPORT_ESCALATION_CONVERSATION_LENGTH_THRESHOLD) return false;
	// Threshold CTA stays on response #3 only — never propagates to #4+.
	return responseIndex === SUPPORT_ESCALATION_CONVERSATION_LENGTH_THRESHOLD - 1;
}

/**
 * Stable key for a newly revealed support CTA on a response.
 *
 * @param {{
 *   answer?: string | null;
 *   responseIndex: number;
 *   conversationLength: number;
 *   isDownvoted: boolean;
 *   responseId?: string | null;
 * }} options
 * @returns {string | null}
 */
export function getSupportCtaRevealKey({
	answer,
	responseIndex,
	conversationLength,
	isDownvoted,
	responseId = null,
}) {
	if (
		!shouldShowSupportEscalation({
			answer,
			responseIndex,
			conversationLength,
			isDownvoted,
		})
	) {
		return null;
	}
	const idPart =
		typeof responseId === 'string' && responseId.length > 0
			? responseId
			: `idx:${responseIndex}`;
	if (isDownvoted === true) return `down:${idPart}`;
	return `threshold:${idPart}`;
}

/**
 * Whether to auto-scroll so a newly appeared CTA on the last response is visible.
 * Older responses and already-revealed keys must not steal scroll.
 *
 * @param {{
 *   isLastResponse: boolean;
 *   revealKey: string | null;
 *   lastRevealedKey?: string | null;
 * }} options
 * @returns {boolean}
 */
export function shouldAutoRevealSupportCta({
	isLastResponse,
	revealKey,
	lastRevealedKey = null,
}) {
	if (!isLastResponse) return false;
	if (typeof revealKey !== 'string' || revealKey.length === 0) return false;
	if (revealKey === lastRevealedKey) return false;
	return true;
}

/**
 * Stable key for the completed latest-response layout (answer + controls + optional CTA).
 * Changes when the last card finishes, gains a CTA, or is thumbs-downed.
 *
 * @param {{
 *   conversationLength: number;
 *   responseIndex: number;
 *   responseId?: string | null;
 *   answer?: string | null;
 *   isDownvoted?: boolean;
 * }} options
 * @returns {string | null}
 */
export function getLatestResponseCompletionKey({
	conversationLength,
	responseIndex,
	responseId = null,
	answer = null,
	isDownvoted = false,
}) {
	if (typeof conversationLength !== 'number' || conversationLength <= 0) return null;
	if (typeof responseIndex !== 'number' || responseIndex !== conversationLength - 1) return null;
	if (typeof answer !== 'string' || !answer.trim()) return null;
	const idPart =
		typeof responseId === 'string' && responseId.length > 0
			? responseId
			: `idx:${responseIndex}`;
	const showCta = shouldShowSupportEscalation({
		answer,
		responseIndex,
		conversationLength,
		isDownvoted: isDownvoted === true,
	});
	return [
		`len:${conversationLength}`,
		`id:${idPart}`,
		showCta ? 'cta' : 'nocta',
		isDownvoted === true ? 'down' : 'nodown',
	].join('|');
}

/**
 * Whether to scroll the message list to the true bottom after the latest response completes.
 * Skips closed chat, history view, in-flight generation, incomplete answers, and repeats.
 *
 * @param {{
 *   isOpen: boolean;
 *   isHistoryOpen: boolean;
 *   isBusy: boolean;
 *   completionKey: string | null;
 *   lastScrolledKey?: string | null;
 * }} options
 * @returns {boolean}
 */
export function shouldScrollLatestResponseToBottom({
	isOpen,
	isHistoryOpen,
	isBusy,
	completionKey,
	lastScrolledKey = null,
}) {
	if (!isOpen || isHistoryOpen || isBusy) return false;
	if (typeof completionKey !== 'string' || completionKey.length === 0) return false;
	if (completionKey === lastScrolledKey) return false;
	return true;
}

/**
 * Scroll a message container to its true bottom so the full latest card
 * (frame, feedback controls, optional support CTA) clears the composer.
 * Prefer this over scrollIntoView({ block: 'nearest' }), which can stop early.
 *
 * @param {Pick<HTMLElement, 'scrollHeight' | 'clientHeight' | 'scrollTop' | 'scrollTo'> | null | undefined} container
 * @param {{ behavior?: 'auto' | 'smooth' }} [options]
 * @returns {boolean}
 */
export function scrollMessageContainerToBottom(container, { behavior = 'auto' } = {}) {
	if (!container) return false;
	const top = Math.max(0, container.scrollHeight - container.clientHeight);
	if (behavior === 'smooth' && typeof container.scrollTo === 'function') {
		container.scrollTo({ top, behavior: 'smooth' });
	} else {
		container.scrollTop = container.scrollHeight;
	}
	return true;
}

/**
 * Scroll behavior for conversation auto-scroll. Honors prefers-reduced-motion when available.
 * @param {Pick<Window, 'matchMedia'> | null | undefined} [media]
 * @returns {'auto' | 'smooth'}
 */
export function getSupportCtaScrollBehavior(media = typeof window !== 'undefined' ? window : null) {
	try {
		if (media?.matchMedia?.('(prefers-reduced-motion: reduce)')?.matches) {
			return 'auto';
		}
	} catch {
		// ignore
	}
	return 'smooth';
}

/** Alias kept for call sites that talk about completion scroll rather than CTA-only reveal. */
export const getConversationScrollBehavior = getSupportCtaScrollBehavior;
