/** Vercel edge middleware for LinkedIn URL canonicalization. */
export default function trackingRedirect(request) {
	const clean = new URL(request.url);
	if (!clean.searchParams.has('trk')) {
		return new Response(null, { headers: { 'x-middleware-next': '1' } });
	}
	clean.searchParams.delete('trk');
	return Response.redirect(clean, 301);
}
