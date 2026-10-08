export interface MdastNode {
	type: string;
	value?: string;
	children?: MdastNode[];
}

export function resolveHeadingVars(
	node: MdastNode,
	vars: Readonly<Record<string, string>>,
	filePath: string,
	inHeading?: boolean,
): MdastNode;
