import { useState } from 'react';
import { LuThumbsUp, LuThumbsDown, LuCheck } from 'react-icons/lu';
import './DocsFeedback.css';

interface Props {
	pageSlug: string;
	pageTitle: string;
}

type Step = 'idle' | 'expanded' | 'submitted';
type Rating = 'positive' | 'negative';

interface Category {
	label: string;
	description: string;
}

const POSITIVE_CATEGORIES: Category[] = [
	{ label: 'Accurate', description: 'Accurately describes the feature.' },
	{ label: 'Solved my problem', description: 'Helped me resolve an issue.' },
	{ label: 'Easy to understand', description: 'Clear and well-written.' },
	{ label: 'Another reason', description: '' },
];

const NEGATIVE_CATEGORIES: Category[] = [
	{ label: 'Inaccurate', description: 'Contains incorrect information.' },
	{ label: 'Missing information', description: "Couldn't find what I needed." },
	{ label: 'Hard to understand', description: 'Too complicated or confusing.' },
	{ label: 'Outdated', description: 'Information is no longer current.' },
	{ label: 'Another reason', description: '' },
];

export default function DocsFeedback({ pageSlug, pageTitle }: Props) {
	const [step, setStep] = useState<Step>('idle');
	const [rating, setRating] = useState<Rating | null>(null);
	const [category, setCategory] = useState<string>('');
	const [comment, setComment] = useState<string>('');

	const handleRating = (r: Rating) => {
		setRating(r);
		setCategory('');
		setComment('');
		setStep('expanded');
	};

	const handleSend = () => {
		const payload: Record<string, string> = {
			page_url: window.location.origin + window.location.pathname,
			page_slug: pageSlug,
			page_title: pageTitle.replace(/ \| Warp$/, ''),
			rating: rating === 'positive' ? 'positive' : 'negative',
		};
		if (category && category !== 'Another reason') {
			payload.category = category;
		}
		const trimmedComment = comment.trim();
		if (trimmedComment) {
			payload.comment = trimmedComment;
		}

		// rudderanalytics is stubbed as a queue array by RudderStackAnalytics.astro
		// before the full SDK loads, so calling .track() here is always safe.
		const ra = (window as any).rudderanalytics;
		if (ra) {
			ra.track('docs_feedback_submitted', payload);
		}

		setStep('submitted');
	};

	const categories = rating === 'positive' ? POSITIVE_CATEGORIES : NEGATIVE_CATEGORIES;
	const formHeader = rating === 'positive' ? 'What did you like?' : 'What could we improve?';

	return (
		<div className="docs-feedback">
			<hr className="docs-feedback__divider" aria-hidden="true" />

			{step === 'idle' && (
				<div className="docs-feedback__prompt">
					<span className="docs-feedback__question">Was this page useful?</span>
					<div className="docs-feedback__buttons">
						<button
							type="button"
							className="docs-feedback__vote-btn"
							onClick={() => handleRating('positive')}
							aria-label="Yes, this page was useful"
						>
							<LuThumbsUp className="docs-feedback__vote-icon" aria-hidden="true" />
							Yes
						</button>
						<button
							type="button"
							className="docs-feedback__vote-btn"
							onClick={() => handleRating('negative')}
							aria-label="No, this page was not useful"
						>
							<LuThumbsDown className="docs-feedback__vote-icon" aria-hidden="true" />
							No
						</button>
					</div>
				</div>
			)}

			{step === 'expanded' && (
				<div className="docs-feedback__form">
					<h3 className="docs-feedback__form-header">{formHeader}</h3>
					<div
						className="docs-feedback__categories"
						role="radiogroup"
						aria-label={formHeader}
					>
						{categories.map(({ label, description }) => (
							<label key={label} className="docs-feedback__category">
								<input
									type="radio"
									name="docs-feedback-category"
									value={label}
									checked={category === label}
									onChange={() => setCategory(label)}
									className="docs-feedback__radio"
								/>
								<span className="docs-feedback__category-label">{label}</span>
								{description && (
									<span className="docs-feedback__category-desc">{description}</span>
								)}
							</label>
						))}
					</div>
					<textarea
						className="docs-feedback__textarea"
						placeholder="Any additional details (optional)"
						value={comment}
						onChange={(e) => setComment(e.target.value)}
						rows={4}
						aria-label="Additional details (optional)"
					/>
					<button
						type="button"
						className="docs-feedback__send-btn"
						onClick={handleSend}
					>
						SEND
					</button>
				</div>
			)}

			{step === 'submitted' && (
				<div className="docs-feedback__success" aria-live="polite" role="status">
					<LuCheck className="docs-feedback__success-check" aria-hidden="true" />
					<span>Thanks for your feedback!</span>
				</div>
			)}
		</div>
	);
}
