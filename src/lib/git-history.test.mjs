import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { mkdtempSync, readFileSync, unlinkSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import path from 'node:path';
import test from 'node:test';
import { getShallowBoundaryDates } from './git-history.js';

test('unavailable history is nonfatal and boundary dates are identifiable', () => {
	const root = process.cwd();
	const repo = path.join(mkdtempSync(path.join(tmpdir(), 'docs-history-test-')), 'repo');
	const init = spawnSync('git', ['init', repo], { encoding: 'utf8' });
	assert.equal(init.status, 0, init.stderr);
	const objects = spawnSync('git', ['rev-parse', '--git-path', 'objects'], { encoding: 'utf8' });
	const head = spawnSync('git', ['rev-parse', 'HEAD'], { encoding: 'utf8' }).stdout.trim();
	writeFileSync(path.join(repo, '.git/objects/info/alternates'), `${path.resolve(root, objects.stdout.trim())}\n`);
	const git = (...args) => {
		const result = spawnSync('git', args, { cwd: repo, encoding: 'utf8' });
		assert.equal(result.status, 0, result.stderr);
		return result.stdout.trim();
	};
	process.chdir(repo);
	try {
		git('update-ref', 'HEAD', head);
		writeFileSync(path.join(repo, '.git/shallow'), `${head}\n`);
		const timestamp = Number(git('show', '--no-patch', '--format=%ct', 'HEAD')) * 1000;
		assert.deepEqual(getShallowBoundaryDates(), new Set([timestamp]));
		const result = spawnSync('node', [path.join(root, 'scripts/ensure-git-history.mjs')], {
			cwd: repo,
			encoding: 'utf8',
			env: { ...process.env, VERCEL_GIT_REPO_OWNER: '', VERCEL_GIT_REPO_SLUG: '' },
		});
		assert.equal(result.status, 0, result.stderr);
		assert.match(result.stderr, /shallow-boundary page dates will be omitted/);
		assert.ok(readFileSync(path.join(repo, '.git/shallow'), 'utf8').trim());
		unlinkSync(path.join(repo, '.git/shallow'));
		assert.deepEqual(getShallowBoundaryDates(), new Set());
	} finally {
		process.chdir(root);
	}
});
