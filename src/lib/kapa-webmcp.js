/**
 * Kapa Website Widget attributes for WebMCP.
 *
 * Docs use a custom React SDK chat surface (`KapaChatLauncher`), not Kapa's
 * default floating Ask AI button. WebMCP still requires the website widget
 * script with `data-webmcp-enabled="true"`:
 * https://docs.kapa.ai/integrations/website-widget/features/webmcp
 *
 * `data-button-hide` keeps the default widget launcher off the page so the
 * existing custom Ask control remains the only human chat entry point.
 * Browsers without WebMCP ignore the enable flag; chat behavior is unchanged.
 */

export const KAPA_WIDGET_SCRIPT_SRC = 'https://widget.kapa.ai/kapa-widget.bundle.js';

/** Becomes `search_warp_knowledge_sources` via Kapa's snake_case tool naming. */
export const KAPA_WEBMCP_PROJECT_NAME = 'Warp';

/**
 * @param {string | undefined | null} integrationId
 * @returns {null | {
 *   src: string,
 *   async: true,
 *   'data-website-id': string,
 *   'data-project-name': string,
 *   'data-webmcp-enabled': 'true',
 *   'data-button-hide': 'true',
 * }}
 */
export function getKapaWebMcpScriptAttributes(integrationId) {
	const websiteId = typeof integrationId === 'string' ? integrationId.trim() : '';
	if (!websiteId) return null;

	return {
		src: KAPA_WIDGET_SCRIPT_SRC,
		async: true,
		'data-website-id': websiteId,
		'data-project-name': KAPA_WEBMCP_PROJECT_NAME,
		'data-webmcp-enabled': 'true',
		// Hide Kapa's default floating button only. The custom sidebar Ask
		// launcher (and search-footer Ask AI CTA) stay visible.
		'data-button-hide': 'true',
	};
}
