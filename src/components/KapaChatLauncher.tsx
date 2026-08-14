import type { FormEvent, MouseEvent, ReactElement, ReactNode } from 'react';
import * as Popover from '@radix-ui/react-popover';
import {
	Children,
	isValidElement,
	useEffect,
	useMemo,
	useRef,
	useState,
} from 'react';
import { CaptchaAction, KapaProvider, useCaptcha, useChat } from '@kapaai/react-sdk';
import { PUBLIC_KAPA_INTEGRATION_ID, PUBLIC_KAPA_PROJECT_ID } from 'astro:env/client';
import { isMac, keymatch } from 'keymatch';
import ReactMarkdown from 'react-markdown';
import {
	LuExternalLink,
	LuCheck,
	LuCopy,
	LuLoaderCircle,
	LuMessageSquare,
	LuPlug,
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
const warpDocsMcpUrl = 'https://warp.mcp.kapa.ai';
const warpDocsMcpConfig = JSON.stringify(
	{
		'Warp Docs': {
			url: warpDocsMcpUrl,
		},
	},
	null,
	2
);

type FeedbackReaction = 'upvote' | 'downvote';
type McpCopyTarget = 'config' | 'url';
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
function getChatErrorMessage(error: unknown) {
	const message = typeof error === 'string' ? error : String(error ?? '');
	const normalized = message.toLowerCase();
	const looksLikeBlockedNetworkError =
		normalized.includes('network error while fetching answer') ||
		normalized.includes('failed to fetch') ||
		normalized.includes('err_blocked_by_client');
	if (looksLikeBlockedNetworkError) {
		return "Couldn't reach the chat service. If you use an ad blocker or privacy extension, allow kapa.ai and proxy.kapa.ai, then try again.";
	}
	return message;
}

const CHAT_LANGUAGE_ALIASES: Record<string, string> = {
	shell: 'bash',
	zsh: 'bash',
	pwsh: 'powershell',
	plaintext: 'text',
};

function normalizeChatLanguage(language: string): string {
	return CHAT_LANGUAGE_ALIASES[language.toLowerCase()] ?? language.toLowerCase();
}

function inferLanguageFromCode(codeText: string, fallbackLanguage: string): string {
	if (fallbackLanguage !== 'text') return fallbackLanguage;
	const sample = codeText.trim();
	if (!sample) return fallbackLanguage;
	const commandLikePattern =
		/^(sudo|apt|apt-get|dnf|yum|zypper|pacman|curl|wget|git|npm|pnpm|yarn|cargo|python|node|brew|sh|bash)\b/m;
	if (commandLikePattern.test(sample)) return 'bash';
	return fallbackLanguage;
}

function escapeHtml(value: string): string {
	return value.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

async function copyTextToClipboard(text: string): Promise<boolean> {
	try {
		if (navigator.clipboard?.writeText) {
			await navigator.clipboard.writeText(text);
			return true;
		}
	} catch {
		// Fall through to execCommand fallback.
	}
	try {
		const pre = document.createElement('pre');
		Object.assign(pre.style, {
			opacity: '0',
			pointerEvents: 'none',
			position: 'absolute',
			overflow: 'hidden',
			left: '0',
			top: '0',
			width: '20px',
			height: '20px',
			webkitUserSelect: 'auto',
			userSelect: 'all',
		});
		pre.setAttribute('aria-hidden', 'true');
		pre.textContent = text;
		document.body.appendChild(pre);
		const range = document.createRange();
		range.selectNode(pre);
		const selection = window.getSelection();
		if (!selection) {
			document.body.removeChild(pre);
			return false;
		}
		selection.removeAllRanges();
		selection.addRange(range);
		const ok = document.execCommand('copy');
		selection.removeAllRanges();
		document.body.removeChild(pre);
		return ok;
	} catch {
		return false;
	}
}

type MarkdownCodeProps = { className?: string; children?: ReactNode };

// react-markdown v9+ no longer passes an `inline` flag to the `code`
// component. The reliable way to tell fenced blocks apart from inline
// code is nesting: fenced blocks are always rendered as <pre><code>, so
// we intercept `pre` (block) and leave bare `code` (inline) untouched.
function extractCodeElement(children: ReactNode): ReactElement<MarkdownCodeProps> | null {
	const items = Array.isArray(children) ? children : [children];
	for (const item of items) {
		if (isValidElement<MarkdownCodeProps>(item)) return item;
	}
	return null;
}

function markdownChildrenToText(children: ReactNode): string {
	return (Array.isArray(children) ? children.join('') : String(children ?? '')).replace(/\n$/, '');
}
type ChatMarkdownImageProps = {
	alt?: string;
	src?: string;
	title?: string;
};

function isImageOnlyMarkdownLink(children: ReactNode) {
	const items = Children.toArray(children).filter(
		(child) => typeof child !== 'string' || child.trim().length > 0
	);
	return (
		items.length === 1 &&
		isValidElement(items[0]) &&
		items[0].type === ChatMarkdownImage
	);
}

function ChatMarkdownLink({
	children,
	href,
	title,
}: {
	children?: ReactNode;
	href?: string;
	title?: string;
}) {
	// Kapa sometimes wraps an image in its source link. Keep ordinary links,
	// but remove the image-only wrapper so the thumbnail can be a real button.
	if (isImageOnlyMarkdownLink(children)) {
		return <>{children}</>;
	}

	return (
		<a href={href} title={title}>
			{children}
		</a>
	);
}

function ChatMarkdownImage({ alt, src, title }: ChatMarkdownImageProps) {
	const [hasFailed, setHasFailed] = useState(false);
	const imageAlt = alt?.trim() || 'Image from Kapa answer';

	useEffect(() => {
		setHasFailed(false);
	}, [src]);

	if (!src || hasFailed) {
		return (
			<span
				className="sl-kapa-answer-image-fallback"
				role="img"
				aria-label={`${imageAlt} unavailable`}
			>
				Image unavailable
			</span>
		);
	}

	// `src` has already passed react-markdown's default safe URL transformation.
	// Image-only Markdown links are unwrapped above to avoid nesting this button
	// inside an anchor. Ordinary text links retain their original behavior.
	const image = (
		<img
			className="sl-kapa-answer-image"
			src={src}
			alt={imageAlt}
			title={title}
			loading="lazy"
			decoding="async"
			referrerPolicy="no-referrer"
			style={{ maxWidth: '100%', height: 'auto' }}
			onError={() => setHasFailed(true)}
		/>
	);

	return (
		<button
			type="button"
			className="sl-kapa-answer-image-button"
			data-warp-image-lightbox-trigger="true"
			aria-label={`Expand image: ${imageAlt}`}
			aria-haspopup="dialog"
		>
			{image}
			<span className="sl-kapa-answer-image-button__overlay" aria-hidden="true">
				Expand image
			</span>
		</button>
	);
}
const highlightCache = new Map<string, string | null>();
const highlightInFlight = new Map<string, Promise<string | null>>();
let highlightRequestQueue: Promise<void> = Promise.resolve();
type ShikiModule = typeof import('shiki');
type ShikiHighlighter = Awaited<ReturnType<ShikiModule['createHighlighter']>>;
let shikiHighlighterPromise: Promise<ShikiHighlighter> | null = null;
const SHIKI_LANGUAGES = new Set([
	'bash',
	'powershell',
	'json',
	'javascript',
	'typescript',
	'tsx',
	'jsx',
	'python',
	'go',
	'rust',
	'yaml',
	'markdown',
	'html',
	'css',
	'text',
]);

async function getShikiHighlighter(): Promise<ShikiHighlighter> {
	if (!shikiHighlighterPromise) {
		shikiHighlighterPromise = import('shiki/bundle/full').then(({ createHighlighter }) =>
			createHighlighter({
				themes: ['github-light', 'github-dark'],
				langs: [...SHIKI_LANGUAGES],
			})
		);
	}
	return shikiHighlighterPromise;
}

async function requestHighlightedPre({
	code,
	language,
	theme,
}: {
	code: string;
	language: string;
	theme: 'dark' | 'light';
}): Promise<string | null> {
	const cacheKey = `${theme}:${language}:${code}`;
	if (highlightCache.has(cacheKey)) {
		return highlightCache.get(cacheKey) ?? null;
	}
	const existing = highlightInFlight.get(cacheKey);
	if (existing) return existing;

	const requestPromise = new Promise<string | null>((resolve, reject) => {
		const run = async () => {
			try {
				const highlighter = await getShikiHighlighter();
				const shikiLanguage = SHIKI_LANGUAGES.has(language) ? language : 'text';
				const html = highlighter.codeToHtml(code, {
					lang: shikiLanguage,
					theme: theme === 'light' ? 'github-light' : 'github-dark',
				});
				const preMatch = html.match(/<pre[^>]*>[\s\S]*?<\/pre>/i);
				const preHtml = preMatch?.[0] ?? null;
				highlightCache.set(cacheKey, preHtml);
				resolve(preHtml);
			} catch (error) {
				reject(error);
			}
		};

		highlightRequestQueue = highlightRequestQueue
			.then(run)
			.catch(() => run())
			.then(() => undefined, () => undefined);
	});

	highlightInFlight.set(cacheKey, requestPromise);
	requestPromise.then(
		() => {
			highlightInFlight.delete(cacheKey);
		},
		() => {
			highlightInFlight.delete(cacheKey);
		}
	);
	return requestPromise;
}

function ChatCodeBlock({
	className,
	codeText,
	deferHighlight,
}: {
	className?: string;
	codeText: string;
	deferHighlight?: boolean;
}) {
	const language = className?.replace('language-', '') ?? 'text';
	const normalizedLanguage = inferLanguageFromCode(
		codeText,
		normalizeChatLanguage(language)
	);
	const isTerminalLanguage = ['bash', 'sh', 'shell', 'zsh', 'powershell'].includes(normalizedLanguage);
	const [highlighted, setHighlighted] = useState<{ key: string; preHtml: string } | null>(null);
	const [isDarkTheme, setIsDarkTheme] = useState(true);
	const [isCopied, setIsCopied] = useState(false);
	const copiedResetRef = useRef<number | null>(null);

	useEffect(() => {
		const root = document.documentElement;
		const updateTheme = () => {
			const explicitTheme = root.dataset.theme;
			if (explicitTheme === 'light') {
				setIsDarkTheme(false);
				return;
			}
			if (explicitTheme === 'dark') {
				setIsDarkTheme(true);
				return;
			}
			setIsDarkTheme(window.matchMedia('(prefers-color-scheme: dark)').matches);
		};

		updateTheme();
		const observer = new MutationObserver(updateTheme);
		observer.observe(root, { attributes: true, attributeFilter: ['data-theme'] });
		return () => observer.disconnect();
	}, []);

	useEffect(() => {
		return () => {
			if (copiedResetRef.current !== null) {
				window.clearTimeout(copiedResetRef.current);
			}
		};
	}, []);

	const theme = isDarkTheme ? 'dark' : 'light';
	const highlightKey = `${theme}:${normalizedLanguage}:${codeText}`;

	useEffect(() => {
		// While the answer is still streaming, the code text changes on every
		// token. Requesting a highlight per token causes the block to churn
		// between plaintext and highlighted DOM (visible flicker), so wait
		// until streaming settles and highlight the final text once.
		if (deferHighlight) return;
		const controller = new AbortController();
		(async (): Promise<void> => {
			try {
				const preHtml = await requestHighlightedPre({
					code: codeText,
					language: normalizedLanguage,
					theme,
				});
				if (!controller.signal.aborted && preHtml) {
					setHighlighted({ key: `${theme}:${normalizedLanguage}:${codeText}`, preHtml });
				}
			} catch (error) {
				if (!controller.signal.aborted) {
					console.warn('[kapa-chat] code highlighting failed; using plaintext fallback', error);
				}
			}
		})();

		return () => {
			controller.abort();
		};
	}, [codeText, deferHighlight, theme, normalizedLanguage]);

	// Only use highlighted HTML that matches the *current* code text and
	// theme; otherwise render the plaintext fallback. This prevents stale
	// highlighted content from flashing while new text is streaming in.
	const highlightedPreHtml = highlighted?.key === highlightKey ? highlighted.preHtml : null;

	const onCopy = async () => {
		const ok = await copyTextToClipboard(codeText);
		if (!ok) return;
		setIsCopied(true);
		if (copiedResetRef.current !== null) {
			window.clearTimeout(copiedResetRef.current);
		}
		copiedResetRef.current = window.setTimeout(() => {
			setIsCopied(false);
			copiedResetRef.current = null;
		}, 1500);
	};

	return (
		<div className="expressive-code sl-kapa-codeblock">
			<figure className={`frame not-content${isTerminalLanguage ? ' is-terminal' : ''}`}>
				<figcaption className="header">
					<span className="title" />
					{isTerminalLanguage ? <span className="sr-only">Terminal window</span> : null}
				</figcaption>
				{highlightedPreHtml ? (
					<div
						className="sl-kapa-codeblock__shiki"
						dangerouslySetInnerHTML={{ __html: highlightedPreHtml }}
					/>
				) : (
					<pre data-language={language}>
						<code className={className} dangerouslySetInnerHTML={{ __html: escapeHtml(codeText) }} />
					</pre>
				)}
				{/* Dedicated chat copy control — intentionally NOT EC's `.copy`
				    class. Reusing EC markup stacked EC's CSS mask icon on top of
				    any residual SVG and produced a double clipboard. One button,
				    one icon (CSS mask), one click handler. */}
				<div className="sl-kapa-codeblock__copy-wrap">
					<span className="sr-only" aria-live="polite">
						{isCopied ? 'Copied!' : ''}
					</span>
					{isCopied ? <span className="sl-kapa-codeblock__copy-feedback">Copied!</span> : null}
					<button
						type="button"
						className="sl-kapa-codeblock__copy"
						onClick={() => {
							void onCopy();
						}}
						title={isCopied ? 'Copied!' : 'Copy to clipboard'}
						aria-label={isCopied ? 'Code copied' : 'Copy code block'}
					>
						<span className="sl-kapa-codeblock__copy-icon" aria-hidden="true" />
					</button>
				</div>
			</figure>
		</div>
	);
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
	const [copiedMcpValue, setCopiedMcpValue] = useState<McpCopyTarget | null>(null);
	const messagesRef = useRef<HTMLDivElement | null>(null);
	const dialogRef = useRef<HTMLDialogElement | null>(null);
	const triggerRef = useRef<HTMLButtonElement | null>(null);
	const closeButtonRef = useRef<HTMLButtonElement | null>(null);
	const inputRef = useRef<HTMLInputElement | null>(null);
	const mcpCopyResetRef = useRef<number | null>(null);
	const {
		addFeedback,
		conversation,
		error,
		isGeneratingAnswer,
		isPreparingAnswer,
		submitQuery,
		threadId,
	} = useChat();
	const { executeCaptcha } = useCaptcha();

	useEffect(() => {
		setIsAppleDevice(isMac());
	}, []);
	useEffect(() => {
		return () => {
			if (mcpCopyResetRef.current !== null) {
				window.clearTimeout(mcpCopyResetRef.current);
			}
		};
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
		if (isSubmittingHandoff) return;
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
			let captcha;
			try {
				captcha = await executeCaptcha(CaptchaAction.FeedbackSubmit);
			} catch {
				setHandoffErrorMessage('Captcha verification could not be completed. Please try again.');
				return;
			}
			if (!captcha?.token || !captcha?.key) {
				setHandoffErrorMessage('Captcha verification did not return a token. Please try again.');
				return;
			}
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
					captcha_token: captcha.token,
					captcha_header: captcha.key,
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
	const copyMcpValue = async (target: McpCopyTarget) => {
		const value = target === 'config' ? warpDocsMcpConfig : warpDocsMcpUrl;
		const copied = await copyTextToClipboard(value);
		if (!copied) return;
		setCopiedMcpValue(target);
		if (mcpCopyResetRef.current !== null) {
			window.clearTimeout(mcpCopyResetRef.current);
		}
		mcpCopyResetRef.current = window.setTimeout(() => {
			setCopiedMcpValue(null);
			mcpCopyResetRef.current = null;
		}, 1500);
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
							<Popover.Root>
								<Popover.Trigger asChild>
									<button
										type="button"
										className="sl-kapa-mcp-connect__trigger"
										aria-label="Connect to Warp Docs with MCP"
									>
										<LuPlug aria-hidden="true" />
										<span>Connect with MCP</span>
									</button>
								</Popover.Trigger>
								<Popover.Content
									className="sl-kapa-mcp-connect"
									side="bottom"
									align="end"
									sideOffset={8}
									collisionPadding={12}
								>
									<div className="sl-kapa-mcp-connect__header">
										<LuPlug aria-hidden="true" />
										<div>
											<p className="sl-kapa-mcp-connect__title">Connect to Warp Docs</p>
											<p className="sl-kapa-mcp-connect__description">
												Give agents direct access to Warp&apos;s official documentation through MCP.
											</p>
										</div>
									</div>
									<div className="sl-kapa-mcp-connect__section">
										<p className="sl-kapa-mcp-connect__eyebrow">Use in Warp</p>
										<p className="sl-kapa-mcp-connect__instructions">
											In Warp, go to <strong>Settings</strong> &gt; <strong>Agents</strong> &gt;{' '}
											<strong>MCP servers</strong>, click <strong>+ Add</strong>, and paste the
											configuration.
										</p>
										<code className="sl-kapa-mcp-connect__config">{warpDocsMcpConfig}</code>
										<button
											type="button"
											className="sl-kapa-mcp-connect__action sl-kapa-mcp-connect__action--primary"
											onClick={() => {
												void copyMcpValue('config');
											}}
											aria-label={
												copiedMcpValue === 'config'
													? 'Warp Docs MCP configuration copied'
													: 'Copy Warp Docs MCP configuration'
											}
										>
											{copiedMcpValue === 'config' ? (
												<LuCheck aria-hidden="true" />
											) : (
												<LuCopy aria-hidden="true" />
											)}
											<span>{copiedMcpValue === 'config' ? 'Copied' : 'Copy Warp config'}</span>
										</button>
									</div>
									<div className="sl-kapa-mcp-connect__section">
										<p className="sl-kapa-mcp-connect__eyebrow">Use in another MCP client</p>
										<p className="sl-kapa-mcp-connect__instructions">
											Copy the official MCP URL for Claude, ChatGPT, and other compatible clients.
										</p>
										<button
											type="button"
											className="sl-kapa-mcp-connect__action"
											onClick={() => {
												void copyMcpValue('url');
											}}
											aria-label={
												copiedMcpValue === 'url'
													? 'Warp Docs MCP URL copied'
													: 'Copy Warp Docs MCP URL'
											}
										>
											{copiedMcpValue === 'url' ? (
												<LuCheck aria-hidden="true" />
											) : (
												<LuCopy aria-hidden="true" />
											)}
											<span>{copiedMcpValue === 'url' ? 'Copied' : 'Copy MCP URL'}</span>
										</button>
									</div>
									<span className="sr-only" aria-live="polite">
										{copiedMcpValue === 'config'
											? 'Warp Docs MCP configuration copied to clipboard.'
											: copiedMcpValue === 'url'
												? 'Warp Docs MCP URL copied to clipboard.'
												: ''}
									</span>
									<Popover.Arrow className="sl-kapa-mcp-connect__arrow" />
								</Popover.Content>
							</Popover.Root>
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
										<ReactMarkdown
											components={{
												a: ChatMarkdownLink,
												img: ChatMarkdownImage,
												// Fenced code blocks arrive as <pre><code>; inline code
												// arrives as a bare <code>. react-markdown v9+ removed the
												// `inline` prop, so nesting is the only reliable signal.
												pre({ children }) {
													const codeElement = extractCodeElement(children);
													if (!codeElement) {
														return <pre>{children}</pre>;
													}
													const codeClassName =
														typeof codeElement.props.className === 'string'
															? codeElement.props.className
															: undefined;
													const codeText = markdownChildrenToText(codeElement.props.children);
													const isStreamingAnswer =
														isBusy && conversation[conversation.length - 1]?.id === qa.id;
													return (
														<ChatCodeBlock
															className={codeClassName}
															codeText={codeText}
															deferHighlight={isStreamingAnswer}
														/>
													);
												},
												code({ className, children }) {
													return <code className={className}>{children}</code>;
												},
											}}
										>
											{qa.answer}
										</ReactMarkdown>
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

						{error ? <div className="sl-kapa-error">{getChatErrorMessage(error)}</div> : null}
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
			// Anonymous first-party cookie (`kapa_web_id`). Default in the Kapa
			// React SDK; set explicitly so we do not accidentally ship `none` again.
			// https://docs.kapa.ai/dev/sdk/components/KapaProvider#user-tracking-mode
			userTrackingMode="cookie"
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
