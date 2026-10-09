import { readFile, stat, writeFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

export default function llmsIndexOrder() {
	return {
		name: 'warp-llms-index-order',
		hooks: {
			'astro:build:generated': async ({ dir }) => {
				const root = fileURLToPath(dir);
				const indexPath = path.join(root, 'llms.txt');
				const text = await readFile(indexPath, 'utf8');
				const sizes = new Map();
				for (const filename of text.matchAll(/\/_llms-txt\/([\w-]+\.txt)/g)) {
					sizes.set(filename[1], (await stat(path.join(root, '_llms-txt', filename[1]))).size);
				}
				await writeFile(indexPath, reorderLlmsIndex(text, sizes));
			},
		},
	};
}

export function reorderLlmsIndex(text, sizes) {
	const lines = text.split('\n');
	const bundles = lines.filter((line) => /^- \[(Abridged|Complete) documentation\]/.test(line));
	const filename = (line) => line.match(/\/_llms-txt\/([\w-]+\.txt)/)?.[1];
	const sets = lines.filter((line) => filename(line));
	sets.sort((a, b) => sizes.get(filename(a)) - sizes.get(filename(b)));
	const output = lines.filter((line) => !bundles.includes(line)).map((line) =>
		filename(line) ? sets.shift() : line,
	);
	const optional = output.indexOf('## Optional');
	if (optional === -1) output.push('## Optional', '', ...bundles);
	else output.splice(optional + 1, 0, '', ...bundles);
	return output.join('\n');
}
