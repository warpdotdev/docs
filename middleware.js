/**
 * Vercel Routing Middleware runs before static files are served. Astro's
 * src/middleware.ts only runs at build time for prerendered documentation.
 */
export default function middleware(request) {
	const url = new URL(request.url);
	if (!url.searchParams.has('trk')) {
		return new Response(null, { headers: { 'x-middleware-next': '1' } });
	}

	url.searchParams.delete('trk');
	return Response.redirect(url, 301);
}
