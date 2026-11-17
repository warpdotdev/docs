import type { APIRoute } from 'astro';
import { KAPA_API_KEY } from 'astro:env/server';
import { handleRetrieveGet, handleRetrieveOptions } from '../lib/kapa-agent-retrieval.js';

// On-demand Vercel Function — must not be prerendered as static HTML.
export const prerender = false;

export const OPTIONS: APIRoute = () => handleRetrieveOptions();

export const GET: APIRoute = async ({ request }) =>
	handleRetrieveGet(request, { apiKey: KAPA_API_KEY });
