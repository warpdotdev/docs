import { useEffect, useMemo, useRef, useState } from 'react';
import { KapaProvider, useChat } from '@kapaai/react-sdk';
import { PUBLIC_KAPA_INTEGRATION_ID } from 'astro:env/client';
import { isMac, keymatch } from 'keymatch';
import ReactMarkdown from 'react-markdown';
import {
	LuBot,
	LuExternalLink,
	LuLoaderCircle,
	LuMessageSquare,
	LuPlus,
	LuSend,
	LuThumbsDown,
	LuThumbsUp,
	LuX,
} from 'react-icons/lu';
import './KapaChatLauncher.css';

const integrationId = PUBLIC_KAPA_INTEGRATION_ID;
const title = 'Ask Warp';
const welcomeMessage = 'What do you want to know about Warp?';

type FeedbackReaction = 'upvote' | 'downvote';

function ChatSurface({ title, welcomeMessage }: { title: string; welcomeMessage: string }) {
	const [isOpen, setIsOpen] = useState(false);
	const [query, setQuery] = useState('');
	const isAppleDevice = isMac();
	const messagesRef = useRef<HTMLDivElement | null>(null);
	const dialogRef = useRef<HTMLDialogElement | null>(null);
	const triggerRef = useRef<HTMLButtonElement | null>(null);
	const closeButtonRef = useRef<HTMLButtonElement | null>(null);
	const inputRef = useRef<HTMLInputElement | null>(null);
	const previouslyFocusedElementRef = useRef<HTMLElement | null>(null);
	const {
		addFeedback,
		conversation,
		error,
		isGeneratingAnswer,
		isPreparingAnswer,
		resetConversation,
		stopGeneration,
		submitQuery,
	} = useChat();

	useEffect(() => {
		if (!isOpen || !messagesRef.current) return;
		messagesRef.current.scrollTop = messagesRef.current.scrollHeight;
	}, [conversation, isGeneratingAnswer, isPreparingAnswer, isOpen]);

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
		setQuery('');
	};

	const onSubmit = (event: React.FormEvent<HTMLFormElement>) => {
		event.preventDefault();
		submit();
	};

	const feedback = (questionAnswerId: string, reaction: FeedbackReaction) => {
		addFeedback(questionAnswerId, reaction);
	};

	const openPanel = () => {
		const activeElement = document.activeElement;
		previouslyFocusedElementRef.current =
			activeElement instanceof HTMLElement ? activeElement : triggerRef.current;
		setIsOpen(true);
	};

	const closePanel = () => {
		dialogRef.current?.close();
	};

	const restoreFocus = () => {
		const focusTarget = previouslyFocusedElementRef.current ?? triggerRef.current;
		window.requestAnimationFrame(() => {
			focusTarget?.focus();
		});
	};

	const onDialogClose = () => {
		setIsOpen(false);
		restoreFocus();
	};

	const onDialogClick = (event: React.MouseEvent<HTMLDialogElement>) => {
		if (event.target === dialogRef.current) {
			closePanel();
		}
	};

	return (
		<div className="sl-kapa-shell">
			<button
				type="button"
				ref={triggerRef}
				className="sl-kapa-button sl-kapa-button--primary"
				onClick={openPanel}
				aria-haspopup="dialog"
				aria-expanded={isOpen}
				aria-controls="sl-kapa-panel"
				aria-keyshortcuts={isAppleDevice ? 'Meta+I' : 'Control+I'}
			>
				<LuMessageSquare aria-hidden="true" />
				<span className="sl-kapa-button__label">Ask AI</span>
				<kbd className="sl-kapa-button__shortcut sl-hidden md:sl-flex" aria-hidden="true">
					<kbd>{isAppleDevice ? '⌘' : 'Ctrl'}</kbd>
					<kbd>I</kbd>
				</kbd>
			</button>
			<dialog
				ref={dialogRef}
				id="sl-kapa-panel"
				className="sl-kapa-dialog"
				aria-labelledby="sl-kapa-panel-title"
				onClose={onDialogClose}
				onClick={onDialogClick}
			>
				<div className="sl-kapa-panel">
					<header className="sl-kapa-panel__header">
						<div className="sl-kapa-panel__heading">
							<span className="sl-kapa-panel__icon">
								<LuBot aria-hidden="true" />
							</span>
							<div>
								<p className="sl-kapa-panel__eyebrow">Docs AI</p>
								<h2 id="sl-kapa-panel-title">{title}</h2>
							</div>
						</div>
						<div className="sl-kapa-panel__header-actions">
							<button
								type="button"
								className="sl-kapa-icon-button"
								onClick={() => resetConversation()}
								disabled={!hasConversation || isBusy}
								aria-label="Start a new conversation"
							>
								<LuPlus aria-hidden="true" />
							</button>
							<button
								type="button"
								ref={closeButtonRef}
								className="sl-kapa-icon-button"
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
								disabled={isBusy}
							/>
							{isBusy ? (
								<button
									type="button"
									className="sl-kapa-submit"
									onClick={() => stopGeneration()}
								>
									Stop
								</button>
							) : (
								<button type="submit" className="sl-kapa-submit" disabled={!query.trim()}>
									<LuSend aria-hidden="true" />
									<span>Send</span>
								</button>
							)}
						</form>
						<p className="sl-kapa-attribution">
							Powered by{' '}
							<a href="https://kapa.ai" target="_blank" rel="noreferrer">
								kapa.ai
							</a>
						</p>
					</footer>
				</div>
			</dialog>
		</div>
	);
}

export default function KapaChatLauncher() {
	const callbacks = useMemo(
		() => ({
			askAI: {},
		}),
		[]
	);

	return (
		<KapaProvider integrationId={integrationId} callbacks={callbacks} userTrackingMode="none">
			<ChatSurface title={title} welcomeMessage={welcomeMessage} />
		</KapaProvider>
	);
}
