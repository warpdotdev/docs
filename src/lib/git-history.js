import { spawnSync } from 'node:child_process';
import { readFileSync } from 'node:fs';

// Boundary commits in a shallow checkout synthesize modifications for all
// files at the clone horizon. Their timestamps are not content-change dates.
export function getShallowBoundaryDates() {
	const result = spawnSync('git', ['rev-parse', '--git-path', 'shallow'], { encoding: 'utf8' });
	if (result.status !== 0) return new Set();
	let commits;
	try {
		commits = readFileSync(result.stdout.trim(), 'utf8').trim().split('\n');
	} catch {
		return new Set();
	}
	if (!commits.every((commit) => /^[a-f0-9]{40,64}$/.test(commit))) return new Set();
	const dates = spawnSync('git', ['show', '--no-patch', '--format=%ct', ...commits], { encoding: 'utf8' });
	return new Set(dates.stdout.trim().split('\n').map((timestamp) => Number(timestamp) * 1000));
}
