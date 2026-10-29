import assert from 'node:assert/strict';
import test from 'node:test';
import {
	SUPPORT_ESCALATION_CONVERSATION_LENGTH_THRESHOLD,
	shouldShowSupportEscalation,
} from './kapa-support-escalation.js';

test('hides the CTA when the answer is empty', () => {
	assert.equal(
		shouldShowSupportEscalation({
			answer: '',
			conversationLength: SUPPORT_ESCALATION_CONVERSATION_LENGTH_THRESHOLD,
			isDownvoted: true,
		}),
		false
	);
	assert.equal(
		shouldShowSupportEscalation({
			answer: '   ',
			conversationLength: SUPPORT_ESCALATION_CONVERSATION_LENGTH_THRESHOLD,
			isDownvoted: true,
		}),
		false
	);
	assert.equal(
		shouldShowSupportEscalation({
			answer: null,
			conversationLength: SUPPORT_ESCALATION_CONVERSATION_LENGTH_THRESHOLD,
			isDownvoted: true,
		}),
		false
	);
});

test('shows the CTA after three conversation turns', () => {
	assert.equal(
		shouldShowSupportEscalation({
			answer: 'Here is an answer.',
			conversationLength: SUPPORT_ESCALATION_CONVERSATION_LENGTH_THRESHOLD - 1,
			isDownvoted: false,
		}),
		false
	);
	assert.equal(
		shouldShowSupportEscalation({
			answer: 'Here is an answer.',
			conversationLength: SUPPORT_ESCALATION_CONVERSATION_LENGTH_THRESHOLD,
			isDownvoted: false,
		}),
		true
	);
});

test('shows the CTA immediately after a thumbs-down', () => {
	assert.equal(
		shouldShowSupportEscalation({
			answer: 'Here is an answer.',
			conversationLength: 1,
			isDownvoted: true,
		}),
		true
	);
});

test('does not show the CTA for uncertain answers alone', () => {
	assert.equal(
		shouldShowSupportEscalation({
			answer: 'Here is an answer.',
			conversationLength: 1,
			isDownvoted: false,
			// Uncertainty metadata must not influence escalation.
			metadata: { is_uncertain: true, uncertainty: 0.99 },
		}),
		false
	);
});
