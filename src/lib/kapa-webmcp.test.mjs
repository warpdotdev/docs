import assert from 'node:assert/strict';
import test from 'node:test';
import {
	KAPA_WEBMCP_PROJECT_NAME,
	KAPA_WIDGET_SCRIPT_SRC,
	getKapaWebMcpScriptAttributes,
} from './kapa-webmcp.js';

test('returns null when the Website Widget integration id is missing', () => {
	assert.equal(getKapaWebMcpScriptAttributes(undefined), null);
	assert.equal(getKapaWebMcpScriptAttributes(null), null);
	assert.equal(getKapaWebMcpScriptAttributes(''), null);
	assert.equal(getKapaWebMcpScriptAttributes('   '), null);
});

test('enables WebMCP on the official widget script without duplicating chat UI', () => {
	// Fixture only — production uses PUBLIC_KAPA_WEBSITE_WIDGET_INTEGRATION_ID.
	const websiteWidgetIntegrationId = '00000000-0000-4000-8000-000000000001';
	const attrs = getKapaWebMcpScriptAttributes(`  ${websiteWidgetIntegrationId}  `);

	assert.deepEqual(attrs, {
		src: KAPA_WIDGET_SCRIPT_SRC,
		async: true,
		'data-website-id': websiteWidgetIntegrationId,
		'data-project-name': KAPA_WEBMCP_PROJECT_NAME,
		'data-webmcp-enabled': 'true',
		// Default floating Ask button stays hidden; custom sidebar Ask remains.
		'data-button-hide': 'true',
	});
	assert.equal(attrs.src, 'https://widget.kapa.ai/kapa-widget.bundle.js');
	assert.equal(attrs['data-project-name'], 'Warp');
	assert.equal(attrs['data-consent-required'], undefined);
	// Must not accidentally lean on the custom-frontend env var name/value.
	assert.notEqual(websiteWidgetIntegrationId, process.env.PUBLIC_KAPA_INTEGRATION_ID);
});
