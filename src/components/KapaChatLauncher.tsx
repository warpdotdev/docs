import type { FormEvent, MouseEvent } from 'react';
import * as Popover from '@radix-ui/react-popover';
import { useEffect, useMemo, useRef, useState } from 'react';
import { KapaProvider, useChat } from '@kapaai/react-sdk';
import { PUBLIC_KAPA_INTEGRATION_ID, PUBLIC_KAPA_PROJECT_ID } from 'astro:env/client';
import { isMac, keymatch } from 'keymatch';
import ReactMarkdown from 'react-markdown';
import {
	LuExternalLink,
	LuLoaderCircle,
	LuMessageSquare,
	LuSend,
	LuSquarePen,
	LuThumbsDown,
	LuThumbsUp,
	LuX,
} from 'react-icons/lu';
import './KapaChatLauncher.css';

const integrationId = PUBLIC_KAPA_INTEGRATION_ID;
const projectId = PUBLIC_KAPA_PROJECT_ID?.trim() || '';
const title = 'Ask Warp';
const welcomeMessage = 'What do you want to know about Warp?';
const uncertaintyThreshold = 0.15;
const conversationLengthThreshold = 3;
const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

type FeedbackReaction = 'upvote' | 'downvote';
type GenericRecord = Record<string, unknown>;
type HandoffApiSuccess = {
	message?: string;
};

function isObject(value: unknown): value is GenericRecord {
	return typeof value === 'object' && value !== null;
}

function readNumberField(record: GenericRecord, key: string) {
	const value = record[key];
	if (typeof value === 'number' && Number.isFinite(value)) return value;
	if (typeof value === 'string') {
		const parsed = Number(value);
		if (Number.isFinite(parsed)) return parsed;
	}
	return null;
}

function readBooleanField(record: GenericRecord, key: string) {
	const value = record[key];
	if (typeof value === 'boolean') return value;
	if (typeof value === 'string') {
		const normalized = value.trim().toLowerCase();
		if (normalized === 'true') return true;
		if (normalized === 'false') return false;
	}
	return null;
}

function getUncertaintyScore(metadata: unknown) {
	if (!isObject(metadata)) return null;
	return (
		readNumberField(metadata, 'uncertainty') ??
		readNumberField(metadata, 'uncertainty_score') ??
		readNumberField(metadata, 'uncertaintyScore')
	);
}

function isAnswerUncertain(metadata: unknown) {
	if (!isObject(metadata)) return false;
	const flag =
		readBooleanField(metadata, 'is_uncertain') ??
		readBooleanField(metadata, 'isUncertain');
	if (flag === true) return true;
	const score = getUncertaintyScore(metadata);
	return score !== null ? score >= uncertaintyThreshold : false;
}

function isValidEmailAddress(value: string) {
	return emailPattern.test(value.trim());
}

function ChatSurface({ title, welcomeMessage, autoOpen = false, onNewConversation }: {
	title: string;
	welcomeMessage: string;
	autoOpen?: boolean;
	onNewConversation: () => void;
}) {
	const [isOpen, setIsOpen] = useState(autoOpen);
	const [query, setQuery] = useState('');
	const [hasStartedConversation, setHasStartedConversation] = useState(false);
	const [isAppleDevice, setIsAppleDevice] = useState(false);
	const [storedThreadId, setStoredThreadId] = useState<string | null>(null);
	const [downvotedAnswerIds, setDownvotedAnswerIds] = useState<Record<string, true>>({});
	const [handoffEmailInput, setHandoffEmailInput] = useState('');
	const [handoffQaId, setHandoffQaId] = useState<string | null>(null);
	const [handoffErrorMessage, setHandoffErrorMessage] = useState<string | null>(null);
	const [handoffSuccessMessage, setHandoffSuccessMessage] = useState<string | null>(null);
	const [isSubmittingHandoff, setIsSubmittingHandoff] = useState(false);
	const messagesRef = useRef<HTMLDivElement | null>(null);
	const dialogRef = useRef<HTMLDialogElement | null>(null);
	const triggerRef = useRef<HTMLButtonElement | null>(null);
	const closeButtonRef = useRef<HTMLButtonElement | null>(null);
	const inputRef = useRef<HTMLInputElement | null>(null);
	const {
		addFeedback,
		conversation,
		error,
		isGeneratingAnswer,
		isPreparingAnswer,
		submitQuery,
		threadId,
	} = useChat();

	useEffect(() => {
		setIsAppleDevice(isMac());
	}, []);

	useEffect(() => {
		const savedThreadId = localStorage.getItem('warp_docs_kapa_thread_id');
		if (savedThreadId) {
			setStoredThreadId(savedThreadId);
		}
	}, []);

	useEffect(() => {
		if (!threadId) return;
		setStoredThreadId(threadId);
		localStorage.setItem('warp_docs_kapa_thread_id', threadId);
	}, [threadId]);

	useEffect(() => {
		if (!isOpen || !messagesRef.current) return;
		messagesRef.current.scrollTop = messagesRef.current.scrollHeight;
	}, [conversation.length, isOpen]);

	useEffect(() => {
		if (!isOpen || !messagesRef.current) return;
		if (!isGeneratingAnswer && !isPreparingAnswer) return;
		messagesRef.current.scrollTop = messagesRef.current.scrollHeight;
	}, [conversation, isGeneratingAnswer, isOpen, isPreparingAnswer]);

	useEffect(() => {
		if (!handoffQaId || !isOpen) return;
		const frame = window.requestAnimationFrame(() => {
			const inlineForm = document.getElementById(`sl-kapa-handoff-inline-${handoffQaId}`);
			if (!inlineForm) return;
			inlineForm.scrollIntoView({
				behavior: 'smooth',
				block: 'nearest',
			});
			const emailInput = inlineForm.querySelector<HTMLInputElement>('input[type="email"]');
			emailInput?.focus();
		});
		return () => {
			window.cancelAnimationFrame(frame);
		};
	}, [handoffQaId, isOpen, conversation.length]);

	useEffect(() => {
		const dialog = dialogRef.current;
		if (!dialog) return;

		if (isOpen) {
			if (!dialog.open) {
				dialog.showModal();
			}

			const frame = window.requestAnimationFrame(() => {
				if (inputRef.current && !inputRef.current.disabled) {
					inputRef.current.focus();
					return;
				}

				closeButtonRef.current?.focus();
			});

			return () => {
				window.cancelAnimationFrame(frame);
			};
		}

		if (dialog.open) {
			dialog.close();
		}
	}, [isOpen]);

	useEffect(() => {
		const onKeyDown = (event: KeyboardEvent) => {
			if (keymatch(event, 'CmdOrCtrl+I')) {
				if (dialogRef.current?.open) {
					closePanel();
				} else {
					openPanel();
				}
				event.preventDefault();
			}
		};

		window.addEventListener('keydown', onKeyDown);
		return () => {
			window.removeEventListener('keydown', onKeyDown);
		};
	}, []);

	const hasConversation = conversation.length > 0;
	const isBusy = isGeneratingAnswer || isPreparingAnswer;

	const submit = () => {
		const value = query.trim();
		if (!value || isBusy) return;
		closeHandoffForm();
		submitQuery(value);
		setHasStartedConversation(true);
		setQuery('');
	};

	const onSubmit = (event: FormEvent<HTMLFormElement>) => {
		event.preventDefault();
		submit();
	};

	const feedback = (questionAnswerId: string, reaction: FeedbackReaction) => {
		addFeedback(questionAnswerId, reaction);
		if (reaction === 'downvote') {
			setDownvotedAnswerIds((current) => ({ ...current, [questionAnswerId]: true }));
		}
	};

	const isDownvoted = (qaId: string | null | undefined, reaction: string | null | undefined) => {
		if (!qaId) return false;
		return reaction === 'downvote' || downvotedAnswerIds[qaId] === true;
	};

	const shouldShowHandoffForAnswer = (qa: {
		id?: string | null;
		answer?: string | null;
		metadata?: unknown;
		reaction?: string | null;
	}) => {
		if (!qa.answer?.trim()) return false;
		const conversationLengthTriggered = conversation.length >= conversationLengthThreshold;
		const downvoteTriggered = isDownvoted(qa.id ?? null, qa.reaction ?? null);
		const uncertaintyTriggered = isAnswerUncertain(qa.metadata);
		return conversationLengthTriggered || downvoteTriggered || uncertaintyTriggered;
	};

	const buildConversationTranscript = () => {
		if (!conversation.length) return 'No conversation history yet.';
		return conversation
			.map((qa, index) => {
				const sources = qa.sources?.length
					? `\nSources:\n${qa.sources.map((source) => `- ${source.title}: ${source.source_url}`).join('\n')}`
					: '';
				return `Q${index + 1}: ${qa.question}\nA${index + 1}: ${qa.answer || '(no answer generated yet)'}${sources}`;
			})
			.join('\n\n');
	};

	const buildConversationLink = (currentThreadId: string | null) => {
		if (!projectId || !currentThreadId) return null;
		return `https://app.kapa.ai/${projectId}/conversations/${currentThreadId}`;
	};
	const openHandoffForm = (qaId: string) => {
		setHandoffQaId(qaId);
		setHandoffErrorMessage(null);
		setHandoffSuccessMessage(null);
	};

	const closeHandoffForm = () => {
		setHandoffQaId(null);
		setHandoffErrorMessage(null);
		setHandoffSuccessMessage(null);
	};

	const submitSupportHandoff = async (qa: { id?: string | null; question?: string }) => {
		const userEmail = handoffEmailInput.trim().toLowerCase();
		if (!isValidEmailAddress(userEmail)) {
			setHandoffErrorMessage('Enter a valid email address to continue.');
			return;
		}
		const localStorageThreadId = localStorage.getItem('warp_docs_kapa_thread_id');
		const activeThreadId = threadId || storedThreadId || localStorageThreadId;
		if (!activeThreadId) {
			setHandoffErrorMessage('Missing Kapa thread context; please send another message and try again.');
			return;
		}

		const question = qa.question?.trim();
		if (!question) {
			setHandoffErrorMessage('Missing question context for handoff.');
			return;
		}

		const conversationLink = buildConversationLink(activeThreadId);

		setIsSubmittingHandoff(true);
		setHandoffErrorMessage(null);
		setHandoffSuccessMessage(null);
		try {
			const response = await fetch('/api/support-handoff', {
				method: 'POST',
				headers: {
					'content-type': 'application/json',
				},
				body: JSON.stringify({
					user_email: userEmail,
					question,
					page_url: window.location.href,
					conversation_transcript: buildConversationTranscript(),
					kapa_project_id: projectId || null,
					kapa_thread_id: activeThreadId,
					kapa_conversation_url: conversationLink || null,
				}),
			});
			const payload: HandoffApiSuccess & { message?: string } = await response.json().catch(() => ({}));
			if (!response.ok) {
				setHandoffErrorMessage(payload.message || 'Could not create support ticket. Please try again.');
				return;
			}
			setHandoffSuccessMessage(payload.message || 'Support ticket created successfully.');
		} catch {
			setHandoffErrorMessage('Could not reach support handoff service. Please try again.');
		} finally {
			setIsSubmittingHandoff(false);
		}
	};

	const openPanel = () => {
		// If the Pagefind search dialog is open with a query typed in, hand
		// that query off to Kapa's input. Both entry points (the ⌘+I / Ctrl+I
		// global shortcut and the "Ask AI" footer CTA) route through here, so
		// this is the single place that owns the search → Kapa handoff. Read
		// the value BEFORE closing the dialog — closing tears down the input.
		const searchDialog = document.querySelector<HTMLDialogElement>('site-search dialog');
		let pendingQuery: string | undefined;
		if (searchDialog?.open) {
			const searchInput = searchDialog.querySelector<HTMLInputElement>('.pagefind-ui__search-input');
			pendingQuery = searchInput?.value.trim() || undefined;
			searchDialog.close();
		}
		// Legacy fallback: earlier callers stashed the query on window before
		// triggering us. Kept as a belt-and-braces guard in case any path
		// still uses it.
		const windowWithAskQuery = window as Window & { __warpAskAiQuery?: string };
		if (!pendingQuery && windowWithAskQuery.__warpAskAiQuery) {
			pendingQuery = windowWithAskQuery.__warpAskAiQuery;
			delete windowWithAskQuery.__warpAskAiQuery;
		}

		setIsOpen(true);
		// Pre-fill (don't auto-submit) so the user can refine before sending.
		// The input is controlled by `query` state, and the open-dialog effect
		// focuses inputRef once the dialog mounts — cursor lands at the end
		// of the pre-filled text, ready for Enter or edits.
		if (pendingQuery) {
			setQuery(pendingQuery);
		}
	};

	const closePanel = () => {
		dialogRef.current?.close();
	};

	const restoreFocus = () => {
		window.requestAnimationFrame(() => {
			triggerRef.current?.focus();
		});
	};

	const onDialogClose = () => {
		setIsOpen(false);
		restoreFocus();
	};

	const onDialogClick = (event: MouseEvent<HTMLDialogElement>) => {
		if (event.target === dialogRef.current) {
			closePanel();
		}
	};

	return (
		<div className="warp-kapa-shell">
			<button
				type="button"
				ref={triggerRef}
				className="warp-kapa-button"
				onClick={openPanel}
				aria-label="Ask AI"
				aria-haspopup="dialog"
				aria-expanded={isOpen}
				aria-controls="sl-kapa-panel"
				aria-keyshortcuts={isAppleDevice ? 'Meta+I' : 'Control+I'}
				data-tooltip={isAppleDevice ? 'Ask AI ⌘I' : 'Ask AI Ctrl+I'}
			>
				<LuMessageSquare aria-hidden="true" />
				<span className="warp-kapa-button__label">Ask</span>
			</button>
			<dialog
				ref={dialogRef}
				id="sl-kapa-panel"
				className="sl-kapa-dialog"
				aria-label={title}
				onClose={onDialogClose}
				onClick={onDialogClick}
			>
				<div className="sl-kapa-panel">
					<header className="sl-kapa-panel__header">
						<button
							type="button"
							className="sl-kapa-icon-button sl-kapa-icon-button--ghost"
							onClick={onNewConversation}
							disabled={!hasStartedConversation}
							aria-label="New conversation"
							data-tooltip="New conversation"
						>
							<LuSquarePen aria-hidden="true" />
						</button>
						<div className="sl-kapa-panel__header-actions">
							<button
								type="button"
								ref={closeButtonRef}
								className="sl-kapa-icon-button sl-kapa-icon-button--close sl-kapa-icon-button--ghost"
								onClick={closePanel}
								aria-label="Close AI chat"
							>
								<LuX aria-hidden="true" />
							</button>
						</div>
					</header>

					<div className="sl-kapa-panel__body" ref={messagesRef}>
						{!hasConversation && (
							<div className="sl-kapa-empty-state">
								<p className="sl-kapa-empty-state__title">Ask a question</p>
								<p>{welcomeMessage}</p>
							</div>
						)}

						{conversation.map((qa) => (
							<div className="sl-kapa-message-group" key={qa.id ?? `temp-${qa.question}`}>
								<div className="sl-kapa-message sl-kapa-message--user">{qa.question}</div>
								<div className="sl-kapa-message sl-kapa-message--assistant">
									{qa.answer ? (
										<ReactMarkdown>{qa.answer}</ReactMarkdown>
									) : (
										<div className="sl-kapa-thinking">
											<LuLoaderCircle className="sl-kapa-spinner" aria-hidden="true" />
											<span>{isPreparingAnswer ? 'Preparing answer…' : 'Generating answer…'}</span>
										</div>
									)}

									{qa.sources?.length ? (
										<div className="sl-kapa-sources">
											<p>Sources</p>
											<ul>
												{qa.sources.map((source, index) => (
													<li key={`${source.source_url}-${index}`}>
														<a href={source.source_url} target="_blank" rel="noreferrer">
															<span>{source.title}</span>
															<LuExternalLink aria-hidden="true" />
														</a>
													</li>
												))}
											</ul>
										</div>
									) : null}

									{qa.id ? (
										<div className="sl-kapa-feedback">
											<button
												type="button"
												className="sl-kapa-feedback__button"
												onClick={() => feedback(qa.id as string, 'upvote')}
												aria-label="Mark answer as helpful"
											>
												<LuThumbsUp aria-hidden="true" />
											</button>
											<button
												type="button"
												className="sl-kapa-feedback__button"
												onClick={() => feedback(qa.id as string, 'downvote')}
												aria-label="Mark answer as not helpful"
											>
												<LuThumbsDown aria-hidden="true" />
											</button>
											{shouldShowHandoffForAnswer(qa) ? (
												<button
													type="button"
													className="sl-kapa-feedback__handoff"
													onClick={() => openHandoffForm(qa.id as string)}
												>
													Create ticket
												</button>
											) : null}
										</div>
									) : null}
									{handoffQaId === qa.id && !isBusy && shouldShowHandoffForAnswer(qa) ? (
										<div
											className="sl-kapa-handoff-inline"
											id={`sl-kapa-handoff-inline-${qa.id}`}
										>
											<label htmlFor={`sl-kapa-handoff-email-${qa.id}`}>
												Your Warp account email
											</label>
											<form
												className="sl-kapa-handoff-inline__row"
												onSubmit={(event) => {
													event.preventDefault();
													void submitSupportHandoff(qa);
												}}
											>
												<input
													id={`sl-kapa-handoff-email-${qa.id}`}
													type="email"
													placeholder="you@company.com"
													value={handoffEmailInput}
													onChange={(event) => setHandoffEmailInput(event.target.value)}
													required
												/>
												<button
													type="submit"
													className="sl-kapa-feedback__handoff sl-kapa-feedback__handoff--submit"
													disabled={isSubmittingHandoff}
												>
													{isSubmittingHandoff ? 'Submitting…' : 'Submit'}
												</button>
												<button
													type="button"
													className="sl-kapa-feedback__handoff sl-kapa-feedback__handoff--ghost"
													onClick={closeHandoffForm}
													disabled={isSubmittingHandoff}
												>
													Cancel
												</button>
											</form>
											{handoffErrorMessage ? (
												<p className="sl-kapa-handoff-inline__status sl-kapa-handoff-inline__status--error">
													{handoffErrorMessage}
												</p>
											) : null}
											{handoffSuccessMessage ? (
												<p className="sl-kapa-handoff-inline__status sl-kapa-handoff-inline__status--success">
													{handoffSuccessMessage}
												</p>
											) : null}
										</div>
									) : null}
								</div>
							</div>
						))}

						{error ? <div className="sl-kapa-error">{error}</div> : null}
					</div>
					<footer className="sl-kapa-panel__footer">
						<form className="sl-kapa-form" onSubmit={onSubmit}>
							<input
								ref={inputRef}
								type="text"
								value={query}
								onChange={(event) => setQuery(event.target.value)}
								placeholder="Ask a question about Warp…"
							/>
							<button
								type="submit"
								className="sl-kapa-submit"
								disabled={isBusy || !query.trim()}
								aria-label="Send message"
							>
								<LuSend aria-hidden="true" />
							</button>
						</form>
						<div className="sl-kapa-meta">
							<p className="sl-kapa-attribution">
								Powered by{' '}
								<a href="https://kapa.ai" target="_blank" rel="noreferrer">
									kapa.ai
								</a>
							</p>
							<Popover.Root>
								<p className="sl-kapa-disclosure">
									Protected by{' '}
									<Popover.Trigger asChild>
										<button type="button" className="sl-kapa-disclosure-trigger">
											reCAPTCHA
										</button>
									</Popover.Trigger>
								</p>
								<Popover.Content
									className="sl-kapa-popover"
									side="top"
									align="end"
									sideOffset={8}
								>
									<p>
										This site is protected by reCAPTCHA and the Google{' '}
										<a href="https://policies.google.com/privacy" target="_blank" rel="noreferrer">
											Privacy Policy
										</a>{' '}
										and{' '}
										<a href="https://policies.google.com/terms" target="_blank" rel="noreferrer">
											Terms of Service
										</a>{' '}
										apply.
									</p>
									<Popover.Arrow className="sl-kapa-popover__arrow" />
								</Popover.Content>
							</Popover.Root>
						</div>
					</footer>
				</div>
			</dialog>
		</div>
	);
}

export default function KapaChatLauncher({ autoOpen = false }: { autoOpen?: boolean } = {}) {
	const [chatSessionKey, setChatSessionKey] = useState(0);
	const [sessionAutoOpen, setSessionAutoOpen] = useState(autoOpen);
	const callbacks = useMemo(
		() => ({
			askAI: {
				onAnswerGenerationCompleted: (data: { threadId?: string | null }) => {
					if (data.threadId) {
						localStorage.setItem('warp_docs_kapa_thread_id', data.threadId);
					}
				},
			},
		}),
		[]
	);
	if (!integrationId) {
		return null;
	}
	const startNewConversation = () => {
		// `autoOpen` is read once by each keyed `ChatSurface` remount so the
		// fresh conversation opens immediately without controlling later renders.
		setSessionAutoOpen(true);
		setChatSessionKey((key) => key + 1);
	};

	return (
		<KapaProvider
			key={chatSessionKey}
			integrationId={integrationId}
			callbacks={callbacks}
			userTrackingMode="none"
		>
			<ChatSurface
				title={title}
				welcomeMessage={welcomeMessage}
				autoOpen={sessionAutoOpen}
				onNewConversation={startNewConversation}
			/>
		</KapaProvider>
	);
}
