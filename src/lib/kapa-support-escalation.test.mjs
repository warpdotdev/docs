import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import test from 'node:test';
import { fileURLToPath } from 'node:url';
import {
	SUPPORT_ESCALATION_CONVERSATION_LENGTH_THRESHOLD,
	getConversationScrollBehavior,
	getLatestResponseCompletionKey,
	getSupportCtaRevealKey,
	getSupportCtaScrollBehavior,
	scrollMessageContainerToBottom,
	shouldAutoRevealSupportCta,
	shouldScrollLatestResponseToBottom,
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
	assert.equal(getConversationScrollBehavior(null), 'smooth');
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

test('completion key tracks latest finished response layout including CTA/downvote', () => {
	assert.equal(
		getLatestResponseCompletionKey({
			conversationLength: 2,
			responseIndex: 1,
			responseId: 'qa-2',
			answer: '',
			isDownvoted: false,
		}),
		null
	);
	assert.equal(
		getLatestResponseCompletionKey({
			conversationLength: 3,
			responseIndex: 1,
			responseId: 'qa-2',
			answer: 'Done',
			isDownvoted: false,
		}),
		null,
		'non-last response must not own the completion key'
	);
	assert.equal(
		getLatestResponseCompletionKey({
			conversationLength: 2,
			responseIndex: 1,
			responseId: 'qa-2',
			answer: 'Done',
			isDownvoted: false,
		}),
		'len:2|id:qa-2|nocta|nodown'
	);
	assert.equal(
		getLatestResponseCompletionKey({
			conversationLength: 3,
			responseIndex: 2,
			responseId: 'qa-3',
			answer: 'Done',
			isDownvoted: false,
		}),
		'len:3|id:qa-3|cta|nodown'
	);
	assert.equal(
		getLatestResponseCompletionKey({
			conversationLength: 2,
			responseIndex: 1,
			responseId: 'qa-2',
			answer: 'Done',
			isDownvoted: true,
		}),
		'len:2|id:qa-2|cta|down'
	);
});

test('completion bottom-scroll fires once per finished latest layout', () => {
	assert.equal(
		shouldScrollLatestResponseToBottom({
			isOpen: true,
			isHistoryOpen: false,
			isBusy: false,
			completionKey: 'len:3|id:qa-3|cta|nodown',
			lastScrolledKey: null,
		}),
		true
	);
	assert.equal(
		shouldScrollLatestResponseToBottom({
			isOpen: true,
			isHistoryOpen: false,
			isBusy: false,
			completionKey: 'len:3|id:qa-3|cta|nodown',
			lastScrolledKey: 'len:3|id:qa-3|cta|nodown',
		}),
		false
	);
	assert.equal(
		shouldScrollLatestResponseToBottom({
			isOpen: true,
			isHistoryOpen: false,
			isBusy: true,
			completionKey: 'len:3|id:qa-3|cta|nodown',
			lastScrolledKey: null,
		}),
		false
	);
	assert.equal(
		shouldScrollLatestResponseToBottom({
			isOpen: false,
			isHistoryOpen: false,
			isBusy: false,
			completionKey: 'len:3|id:qa-3|cta|nodown',
			lastScrolledKey: null,
		}),
		false
	);
	assert.equal(
		shouldScrollLatestResponseToBottom({
			isOpen: true,
			isHistoryOpen: true,
			isBusy: false,
			completionKey: 'len:3|id:qa-3|cta|nodown',
			lastScrolledKey: null,
		}),
		false
	);
});

test('scrollMessageContainerToBottom writes true bottom scrollTop', () => {
	const calls = [];
	const container = {
		scrollHeight: 1200,
		clientHeight: 400,
		scrollTop: 0,
		scrollTo(opts) {
			calls.push(opts);
			this.scrollTop = opts.top;
		},
	};
	assert.equal(scrollMessageContainerToBottom(null), false);
	assert.equal(scrollMessageContainerToBottom(container, { behavior: 'auto' }), true);
	assert.equal(container.scrollTop, 1200);
	assert.equal(scrollMessageContainerToBottom(container, { behavior: 'smooth' }), true);
	assert.deepEqual(calls.at(-1), { top: 800, behavior: 'smooth' });
});

test('component wires completion bottom-scroll instead of CTA-only nearest reveal', () => {
	const componentPath = join(
		dirname(fileURLToPath(import.meta.url)),
		'../components/KapaChatLauncher.tsx'
	);
	const cssPath = join(
		dirname(fileURLToPath(import.meta.url)),
		'../components/KapaChatLauncher.css'
	);
	const source = readFileSync(componentPath, 'utf8');
	const css = readFileSync(cssPath, 'utf8');
	assert.match(source, /getLatestResponseCompletionKey/);
	assert.match(source, /shouldScrollLatestResponseToBottom/);
	assert.match(source, /scrollMessageContainerToBottom/);
	assert.match(source, /scrolledCompletionKeyRef/);
	assert.doesNotMatch(source, /scrollIntoView\(\{\s*behavior,\s*block:\s*'nearest'/);
	assert.doesNotMatch(source, /revealedSupportCtaKeyRef/);
	assert.match(css, /\.sl-kapa-panel__body\s*\{[^}]*scroll-padding-bottom:\s*1\.5rem/s);
	assert.match(css, /\.sl-kapa-panel__body\s*\{[^}]*padding-bottom:\s*1\.5rem/s);
});
