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

	const openPanel = () => {
		setIsOpen(true);
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
				aria-label="Ask Kapa AI"
				aria-haspopup="dialog"
				aria-expanded={isOpen}
				aria-controls="sl-kapa-panel"
				aria-keyshortcuts={isAppleDevice ? 'Meta+I' : 'Control+I'}
				data-tooltip={isAppleDevice ? 'Ask Kapa AI ⌘I' : 'Ask Kapa AI Ctrl+I'}
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
