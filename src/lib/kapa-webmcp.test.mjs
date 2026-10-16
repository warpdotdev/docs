import assert from 'node:assert/strict';
import test from 'node:test';
import {
	KAPA_WEBMCP_PROJECT_NAME,
	KAPA_WIDGET_SCRIPT_SRC,
	getKapaWebMcpScriptAttributes,
} from './kapa-webmcp.js';

test('returns null when the integration id is missing', () => {
	assert.equal(getKapaWebMcpScriptAttributes(undefined), null);
	assert.equal(getKapaWebMcpScriptAttributes(null), null);
	assert.equal(getKapaWebMcpScriptAttributes(''), null);
	assert.equal(getKapaWebMcpScriptAttributes('   '), null);
});

test('enables WebMCP on the official widget script without duplicating chat UI', () => {
	const integrationId = 'f31c5644-dd65-4f49-9762-bf580062afa8';
	const attrs = getKapaWebMcpScriptAttributes(`  ${integrationId}  `);

	assert.deepEqual(attrs, {
		src: KAPA_WIDGET_SCRIPT_SRC,
		async: true,
		'data-website-id': integrationId,
		'data-project-name': KAPA_WEBMCP_PROJECT_NAME,
		'data-webmcp-enabled': 'true',
		// Default floating Ask button stays hidden; custom sidebar Ask remains.
		'data-button-hide': 'true',
	});
	assert.equal(attrs.src, 'https://widget.kapa.ai/kapa-widget.bundle.js');
	assert.equal(attrs['data-project-name'], 'Warp');
	assert.equal(attrs['data-consent-required'], undefined);
});
