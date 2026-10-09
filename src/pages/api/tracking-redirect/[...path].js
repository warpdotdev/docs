export const prerender = false;

/** @type {import('astro').APIRoute} */
export const GET = ({ url, params }) => {
	if (!url.searchParams.has('trk')) {
		return new Response(null, { status: 404 });
	}

	const clean = new URL(url);
	clean.pathname = `/${params.path ?? ''}`;
	clean.searchParams.delete('trk');
	return Response.redirect(clean, 301);
};

export const HEAD = GET;
