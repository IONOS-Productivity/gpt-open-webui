	export interface IAgentAiTeam {
		id: string;
		name: string;
		specialty: string;
		bgColor?: string;
		fontColor?: string;
		description: string;
		capabilities?: string[];
		externalLink?: string;
		showCrown?: boolean;
	}