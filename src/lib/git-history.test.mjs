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

test('a shallow clone with a reachable origin gets its full history back', () => {
	const root = process.cwd();
	const dir = mkdtempSync(path.join(tmpdir(), 'docs-history-unshallow-'));
	const origin = path.join(dir, 'origin');
	const run = (cwd, ...args) => {
		const result = spawnSync('git', args, { cwd, encoding: 'utf8' });
		assert.equal(result.status, 0, result.stderr);
		return result.stdout.trim();
	};
	run(dir, 'init', '-q', origin);
	run(origin, 'config', 'uploadpack.allowFilter', 'true');
	for (const [i, date] of ['2026-01-01T00:00:00Z', '2026-02-01T00:00:00Z', '2026-03-01T00:00:00Z'].entries()) {
		writeFileSync(path.join(origin, `page-${i}.md`), `# Page ${i}\n`);
		run(origin, 'add', '.');
		const env = { ...process.env, GIT_AUTHOR_DATE: date, GIT_COMMITTER_DATE: date };
		const commit = spawnSync('git', ['-c', 'user.name=test', '-c', 'user.email=test@example.com', 'commit', '-q', '-m', `page ${i}`], { cwd: origin, encoding: 'utf8', env });
		assert.equal(commit.status, 0, commit.stderr);
	}
	const clone = path.join(dir, 'clone');
	run(dir, 'clone', '-q', '--depth', '1', `file://${origin}`, clone);
	assert.equal(run(clone, 'rev-parse', '--is-shallow-repository'), 'true');
	const result = spawnSync('node', [path.join(root, 'scripts/ensure-git-history.mjs')], { cwd: clone, encoding: 'utf8' });
	assert.equal(result.status, 0, result.stderr);
	assert.match(result.stdout, /Fetched (blob-less|full) git history/);
	assert.equal(run(clone, 'rev-parse', '--is-shallow-repository'), 'false');
	// The first page's real last-change date is visible again, not the boundary commit's.
	assert.equal(run(clone, 'log', '-1', '--format=%cI', '--', 'page-0.md'), '2026-01-01T00:00:00Z');
});
