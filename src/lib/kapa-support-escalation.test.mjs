import assert from 'node:assert/strict';
import test from 'node:test';
import {
	SUPPORT_ESCALATION_CONVERSATION_LENGTH_THRESHOLD,
	getSupportCtaRevealKey,
	getSupportCtaScrollBehavior,
	shouldAutoRevealSupportCta,
	shouldShowSupportEscalation,
} from './kapa-support-escalation.js';

test('hides the CTA when the answer is empty', () => {
	assert.equal(
		shouldShowSupportEscalation({
			answer: '',
			responseIndex: SUPPORT_ESCALATION_CONVERSATION_LENGTH_THRESHOLD - 1,
			conversationLength: SUPPORT_ESCALATION_CONVERSATION_LENGTH_THRESHOLD,
			isDownvoted: true,
		}),
		false
	);
	assert.equal(
		shouldShowSupportEscalation({
			answer: '   ',
			responseIndex: SUPPORT_ESCALATION_CONVERSATION_LENGTH_THRESHOLD - 1,
			conversationLength: SUPPORT_ESCALATION_CONVERSATION_LENGTH_THRESHOLD,
			isDownvoted: true,
		}),
		false
	);
	assert.equal(
		shouldShowSupportEscalation({
			answer: null,
			responseIndex: SUPPORT_ESCALATION_CONVERSATION_LENGTH_THRESHOLD - 1,
			conversationLength: SUPPORT_ESCALATION_CONVERSATION_LENGTH_THRESHOLD,
			isDownvoted: true,
		}),
		false
	);
});

test('pins the conversation-length CTA only to response #3', () => {
	const answer = 'Here is an answer.';
	const threshold = SUPPORT_ESCALATION_CONVERSATION_LENGTH_THRESHOLD;

	assert.equal(
		shouldShowSupportEscalation({
			answer,
			responseIndex: threshold - 2,
			conversationLength: threshold - 1,
			isDownvoted: false,
		}),
		false
	);

	// At exactly three turns, only the third response owns the threshold CTA.
	assert.equal(
		shouldShowSupportEscalation({
			answer,
			responseIndex: 0,
			conversationLength: threshold,
			isDownvoted: false,
		}),
		false
	);
	assert.equal(
		shouldShowSupportEscalation({
			answer,
			responseIndex: 1,
			conversationLength: threshold,
			isDownvoted: false,
		}),
		false
	);
	assert.equal(
		shouldShowSupportEscalation({
			answer,
			responseIndex: threshold - 1,
			conversationLength: threshold,
			isDownvoted: false,
		}),
		true
	);

	// Later responses must not inherit the threshold CTA.
	assert.equal(
		shouldShowSupportEscalation({
			answer,
			responseIndex: threshold,
			conversationLength: threshold + 2,
			isDownvoted: false,
		}),
		false
	);
	assert.equal(
		shouldShowSupportEscalation({
			answer,
			responseIndex: threshold + 1,
			conversationLength: threshold + 2,
			isDownvoted: false,
		}),
		false
	);
	// Response #3 still keeps its threshold CTA after the conversation continues.
	assert.equal(
		shouldShowSupportEscalation({
			answer,
			responseIndex: threshold - 1,
			conversationLength: threshold + 2,
			isDownvoted: false,
		}),
		true
	);
});

test('shows the CTA on each specifically thumbs-downed response', () => {
	assert.equal(
		shouldShowSupportEscalation({
			answer: 'Here is an answer.',
			responseIndex: 0,
			conversationLength: 1,
			isDownvoted: true,
		}),
		true
	);
	assert.equal(
		shouldShowSupportEscalation({
			answer: 'Here is an answer.',
			responseIndex: 1,
			conversationLength: 2,
			isDownvoted: false,
		}),
		false
	);
	assert.equal(
		shouldShowSupportEscalation({
			answer: 'Here is an answer.',
			responseIndex: 1,
			conversationLength: 2,
			isDownvoted: true,
		}),
		true
	);
});

test('dedupes threshold + downvote on response #3 into a single CTA owner', () => {
	const answer = 'Here is an answer.';
	const index = SUPPORT_ESCALATION_CONVERSATION_LENGTH_THRESHOLD - 1;
	assert.equal(
		shouldShowSupportEscalation({
			answer,
			responseIndex: index,
			conversationLength: SUPPORT_ESCALATION_CONVERSATION_LENGTH_THRESHOLD,
			isDownvoted: true,
		}),
		true
	);
	assert.equal(
		getSupportCtaRevealKey({
			answer,
			responseIndex: index,
			conversationLength: SUPPORT_ESCALATION_CONVERSATION_LENGTH_THRESHOLD,
			isDownvoted: true,
			responseId: 'qa-3',
		}),
		'down:qa-3'
	);
});

test('does not show the CTA for uncertain answers alone', () => {
	assert.equal(
		shouldShowSupportEscalation({
			answer: 'Here is an answer.',
			responseIndex: 0,
			conversationLength: 1,
			isDownvoted: false,
			// Uncertainty metadata must not influence escalation.
			metadata: { is_uncertain: true, uncertainty: 0.99 },
		}),
		false
	);
});

test('auto-reveal only fires for a new CTA on the last response', () => {
	assert.equal(
		shouldAutoRevealSupportCta({
			isLastResponse: true,
			revealKey: 'threshold:qa-3',
			lastRevealedKey: null,
		}),
		true
	);
	assert.equal(
		shouldAutoRevealSupportCta({
			isLastResponse: true,
			revealKey: 'threshold:qa-3',
			lastRevealedKey: 'threshold:qa-3',
		}),
		false
	);
	assert.equal(
		shouldAutoRevealSupportCta({
			isLastResponse: false,
			revealKey: 'down:qa-1',
			lastRevealedKey: null,
		}),
		false
	);
	assert.equal(
		shouldAutoRevealSupportCta({
			isLastResponse: true,
			revealKey: null,
			lastRevealedKey: null,
		}),
		false
	);
	// Downvote on the latest response is a new reveal even if threshold already scrolled.
	assert.equal(
		shouldAutoRevealSupportCta({
			isLastResponse: true,
			revealKey: 'down:qa-4',
			lastRevealedKey: 'threshold:qa-3',
		}),
		true
	);
});

test('scroll behavior respects prefers-reduced-motion when available', () => {
	assert.equal(getSupportCtaScrollBehavior(null), 'smooth');
	assert.equal(
		getSupportCtaScrollBehavior({
			matchMedia: () => ({ matches: true }),
		}),
		'auto'
	);
	assert.equal(
		getSupportCtaScrollBehavior({
			matchMedia: () => ({ matches: false }),
		}),
		'smooth'
	);
});
