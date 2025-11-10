	export interface IAgentAiTeam {
		id: string;
		name: string;
		speciality: string;
		description: string;
		capabilities?: string[];
		externalLink?: string;
		showCrown?: boolean;
        highlight?: boolean;
	}