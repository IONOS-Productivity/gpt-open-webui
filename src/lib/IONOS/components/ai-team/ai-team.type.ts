	export interface IAgentAiTeam {
		id: string;
		name: string;
		specialty: string;
		description: string;
		capabilities?: string[];
		externalLink?: string;
		showCrown?: boolean;
        highlight?: boolean;
	}