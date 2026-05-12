import type { APIRoute } from 'astro';
import fs from 'node:fs';

export const prerender = true;

/**
 * Serves the raw Oz Agent API OpenAPI spec at /openapi.yaml so LLMs, crawlers,
 * and developer tooling can consume the machine-readable definition directly.
 *
 * The spec source of truth is `developers/agent-api-openapi.yaml` (same file
 * that `src/pages/api.astro` reads at build time for the Scalar reference).
 */
export const GET: APIRoute = async () => {
	const yaml = fs.readFileSync('developers/agent-api-openapi.yaml', 'utf-8');
	return new Response(yaml, {
		headers: { 'Content-Type': 'text/yaml; charset=utf-8' },
	});
};
