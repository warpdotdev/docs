import type { FormEvent, MouseEvent } from 'react';
import * as Popover from '@radix-ui/react-popover';
import { useEffect, useMemo, useRef, useState } from 'react';
import { KapaProvider, useChat } from '@kapaai/react-sdk';
import { PUBLIC_KAPA_INTEGRATION_ID } from 'astro:env/client';
import { isMac, keymatch } from 'keymatch';
import ReactMarkdown from 'react-markdown';
import {
	LuExternalLink,
	LuLoaderCircle,
	LuMessageSquare,
	LuSend,
	LuSquarePen,
	LuTicket,
	LuThumbsDown,
	LuThumbsUp,
	LuX,
} from 'react-icons/lu';
import './KapaChatLauncher.css';

const integrationId = PUBLIC_KAPA_INTEGRATION_ID;
const title = 'Ask Warp';
const welcomeMessage = 'What do you want to know about Warp?';

type FeedbackReaction = 'upvote' | 'downvote';

function ChatSurface({ title, welcomeMessage, autoOpen = false, onNewConversation }: {
	title: string;
	welcomeMessage: string;
	autoOpen?: boolean;
	onNewConversation: () => void;
}) {
	const [isOpen, setIsOpen] = useState(autoOpen);
	const [query, setQuery] = useState('');
	const [hasStartedConversation, setHasStartedConversation] = useState(false);
	const [showHandoffForm, setShowHandoffForm] = useState(false);
	const [handoffEmail, setHandoffEmail] = useState('');
	const [handoffNote, setHandoffNote] = useState('');
	const [isSubmittingHandoff, setIsSubmittingHandoff] = useState(false);
	const [handoffStatus, setHandoffStatus] = useState<'idle' | 'success' | 'error'>('idle');
	const [handoffStatusMessage, setHandoffStatusMessage] = useState('');
	const [isAppleDevice, setIsAppleDevice] = useState(false);
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
		if (!isOpen || !messagesRef.current) return;
		messagesRef.current.scrollTop = messagesRef.current.scrollHeight;
	}, [conversation.length, isOpen]);

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

	const submitHandoff = async (event: FormEvent<HTMLFormElement>) => {
		event.preventDefault();
		if (isSubmittingHandoff) return;
		setIsSubmittingHandoff(true);
		setHandoffStatus('idle');
		setHandoffStatusMessage('');
		try {
			const response = await fetch('/kapa-handoff', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({
					replyToEmail: handoffEmail.trim(),
					note: handoffNote.trim(),
					pageUrl: window.location.href,
					threadId,
					conversationCount: conversation.length,
					conversationTranscript: buildConversationTranscript(),
					askedAt: new Date().toISOString(),
				}),
			});
			const data = await response.json();
			if (!response.ok) {
				throw new Error(data?.error || 'Unable to submit handoff request.');
			}
			setHandoffStatus('success');
			setHandoffStatusMessage(
				data?.mode === 'preview'
					? 'Ticket preview captured. Configure webhook env vars to send live emails.'
					: 'Ticket submitted. A team member can follow up via your email.'
			);
			setHandoffNote('');
			setShowHandoffForm(false);
		} catch (submitError) {
			setHandoffStatus('error');
			setHandoffStatusMessage(
				submitError instanceof Error ? submitError.message : 'Unable to submit handoff request.'
			);
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
		if (!pendingQuery && (window as any).__warpAskAiQuery) {
			pendingQuery = (window as any).__warpAskAiQuery;
			delete (window as any).__warpAskAiQuery;
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
						<div className="sl-kapa-handoff">
							<button
								type="button"
								className="sl-kapa-handoff__toggle"
								onClick={() => {
									setShowHandoffForm((current) => !current);
									setHandoffStatus('idle');
									setHandoffStatusMessage('');
								}}
								aria-expanded={showHandoffForm}
							>
								<LuTicket aria-hidden="true" />
								<span>Create ticket</span>
							</button>
							{showHandoffForm ? (
								<form className="sl-kapa-handoff__form" onSubmit={submitHandoff}>
									<label>
										<span>Your email</span>
										<input
											type="email"
											value={handoffEmail}
											onChange={(event) => setHandoffEmail(event.target.value)}
											placeholder="you@company.com"
											required
										/>
									</label>
									<label>
										<span>Optional note</span>
										<textarea
											value={handoffNote}
											onChange={(event) => setHandoffNote(event.target.value)}
											placeholder="Share any extra context for the team."
											rows={3}
										/>
									</label>
									<button
										type="submit"
										className="sl-kapa-handoff__submit"
										disabled={isSubmittingHandoff || !handoffEmail.trim()}
									>
										{isSubmittingHandoff ? 'Submitting…' : 'Send transcript'}
									</button>
								</form>
							) : null}
							{handoffStatus !== 'idle' ? (
								<p className={`sl-kapa-handoff__status sl-kapa-handoff__status--${handoffStatus}`}>
									{handoffStatusMessage}
								</p>
							) : null}
						</div>
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
			askAI: {},
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
