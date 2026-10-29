/**
 * Vercel edge middleware that 301s parameter copies of a page to its clean URL:
 * LinkedIn's `trk`, plus `fallback` and `slug`, which nothing on the site reads.
 * Every other query parameter, such as `utm_*`, is kept.
 */
export const STRIPPED_PARAMS = ['trk', 'fallback', 'slug'];

export default function trackingRedirect(request) {
	const clean = new URL(request.url);
	const present = STRIPPED_PARAMS.filter((key) => clean.searchParams.has(key));
	if (present.length === 0) {
		return new Response(null, { headers: { 'x-middleware-next': '1' } });
	}
	for (const key of present) clean.searchParams.delete(key);
	return Response.redirect(clean, 301);
}
