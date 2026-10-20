/**
 * Kapa Website Widget attributes for WebMCP.
 *
 * Docs human chat uses a custom React SDK surface (`KapaChatLauncher`) backed
 * by the CUSTOM_FRONTEND integration (`PUBLIC_KAPA_INTEGRATION_ID`). WebMCP
 * requires a separate Website Widget integration ID
 * (`PUBLIC_KAPA_WEBSITE_WIDGET_INTEGRATION_ID`) on the official widget script
 * with `data-webmcp-enabled="true"`:
 * https://docs.kapa.ai/integrations/website-widget/features/webmcp
 *
 * Do not pass the custom-frontend ID here — Kapa only enables WebMCP on
 * Website Widget integrations.
 *
 * `data-button-hide` keeps the default widget launcher off the page so the
 * existing custom Ask control remains the only human chat entry point.
 * Browsers without WebMCP ignore the enable flag; chat behavior is unchanged.
 */

export const KAPA_WIDGET_SCRIPT_SRC = 'https://widget.kapa.ai/kapa-widget.bundle.js';

/** Becomes `search_warp_knowledge_sources` via Kapa's snake_case tool naming. */
export const KAPA_WEBMCP_PROJECT_NAME = 'Warp';

/**
 * @param {string | undefined | null} websiteWidgetIntegrationId
 *   Website Widget integration ID (`PUBLIC_KAPA_WEBSITE_WIDGET_INTEGRATION_ID`).
 *   Not the custom React frontend integration ID.
 * @returns {null | {
 *   src: string,
 *   async: true,
 *   'data-website-id': string,
 *   'data-project-name': string,
 *   'data-webmcp-enabled': 'true',
 *   'data-button-hide': 'true',
 * }}
 */
export function getKapaWebMcpScriptAttributes(websiteWidgetIntegrationId) {
	const websiteId =
		typeof websiteWidgetIntegrationId === 'string' ? websiteWidgetIntegrationId.trim() : '';
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
