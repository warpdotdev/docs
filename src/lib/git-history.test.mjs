import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { mkdtempSync, readFileSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import path from 'node:path';
import test from 'node:test';
import { getShallowBoundaryDates } from './git-history.js';

test('unavailable history is nonfatal and boundary dates are identifiable', () => {
	const root = process.cwd();
	const repo = mkdtempSync(path.join(tmpdir(), 'docs-history-test-'));
	const git = (...args) => {
		const result = spawnSync('git', args, { cwd: repo, encoding: 'utf8' });
		assert.equal(result.status, 0, result.stderr);
		return result.stdout.trim();
	};
	git('init');
	process.chdir(repo);
	try {
		assert.deepEqual(getShallowBoundaryDates(), new Set());
		git('commit', '--allow-empty', '-m', 'History fixture');
		const timestamp = Number(git('show', '--no-patch', '--format=%ct', 'HEAD')) * 1000;
		writeFileSync(path.join(repo, '.git/shallow'), `${git('rev-parse', 'HEAD')}\n`);
		assert.deepEqual(getShallowBoundaryDates(), new Set([timestamp]));
		const result = spawnSync('node', [path.join(root, 'scripts/ensure-git-history.mjs')], {
			cwd: repo,
			encoding: 'utf8',
			env: { ...process.env, VERCEL_GIT_REPO_OWNER: '', VERCEL_GIT_REPO_SLUG: '' },
		});
		assert.equal(result.status, 0, result.stderr);
		assert.match(result.stderr, /shallow-boundary page dates will be omitted/);
		assert.ok(readFileSync(path.join(repo, '.git/shallow'), 'utf8').trim());
	} finally {
		process.chdir(root);
	}
});
