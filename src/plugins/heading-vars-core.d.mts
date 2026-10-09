export interface MdastNode {
	type: string;
	value?: string;
	children?: MdastNode[];
	position?: {
		start?: {
			line?: number;
			column?: number;
		};
	};
}

export function resolveHeadingVars(
	node: MdastNode,
	vars: Readonly<Record<string, string>>,
	filePath: string,
	inHeading?: boolean,
): MdastNode;
