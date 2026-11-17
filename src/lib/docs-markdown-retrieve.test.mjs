import assert from 'node:assert/strict';
import test from 'node:test';
import { isEligibleDocHtmlPath } from './docs-markdown.js';

test('/retrieve and /api paths are not markdown-negotiated doc HTML', () => {
	assert.equal(isEligibleDocHtmlPath('/retrieve'), false);
	assert.equal(isEligibleDocHtmlPath('/retrieve/'), false);
	assert.equal(isEligibleDocHtmlPath('/api/support-handoff'), false);
	assert.equal(isEligibleDocHtmlPath('/agents/capabilities/skills'), true);
	assert.equal(isEligibleDocHtmlPath('/'), true);
});
