/** Show the support CTA after this many Q&A turns. */
export const SUPPORT_ESCALATION_CONVERSATION_LENGTH_THRESHOLD = 3;

/**
 * Whether the Kapa chat support CTA should appear for an answer.
 * Escalation is limited to long conversations or an explicit thumbs-down.
 *
 * @param {{
 *   answer?: string | null;
 *   conversationLength: number;
 *   isDownvoted: boolean;
 * }} options
 * @returns {boolean}
 */
export function shouldShowSupportEscalation({ answer, conversationLength, isDownvoted }) {
	if (typeof answer !== 'string' || !answer.trim()) return false;
	return (
		conversationLength >= SUPPORT_ESCALATION_CONVERSATION_LENGTH_THRESHOLD || isDownvoted === true
	);
}
