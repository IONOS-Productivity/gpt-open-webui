<script lang="ts">
	import { getContext } from 'svelte';
	import AgentCard from '$lib/IONOS/components/ai-team/AgentCard.svelte';

	import { selectAgent } from '$lib/IONOS/services/agent';
	import type { I18Next } from '$lib/IONOS/i18next';
	import type { Readable } from 'svelte/motion';
	import { user } from '$lib/stores';
	import type { IAgentAiTeam } from '$lib/IONOS/components/ai-team/ai-team.type';

	const i18n = getContext<Readable<I18Next>>('i18n');

	let agents: IAgentAiTeam[] = [];

	$: agents = agentCardData($i18n);

	const agentList: string[] = [
		'rita',
		'greta',
		'derek',
		'dora',
		'chris',
		'simon',
		'fiona',
		'sofia',
        'cedric',
	];

	const agentCardData = (i18n: I18Next): IAgentAiTeam[] => {
		return agentList.map((agentId) => {
			const agentCapabilities = [1, 2, 3].map((num) =>
				i18n.t(`capabilities_${num}_${agentId}`, { ns: 'agents' })
			);
			return {
				id: agentId,
				name: i18n.t(`name_${agentId}`, { ns: 'agents' }),
				speciality: i18n.t(`speciality_${agentId}`, { ns: 'agents' }),
				description: i18n.t(`description_${agentId}`, { ns: 'agents' }),
				capabilities: agentCapabilities,
				...customAgentProps(agentId)
			};
		});
	};

	function selectAgentInternal(agentId: string) {
		// Check if agent has external link (like Rita)
		const agentData = agentCardData($i18n).find(a => a.id === agentId);
		if (agentData?.externalLink) {
			window.open(agentData.externalLink, '_blank');
			return;
		}

		selectAgent(agentId);
	}

	const customAgentProps = (agentId: string) => {
		switch (agentId) {
			case 'rita':
				return {
					externalLink: 'https://www.ionos.de/office-loesungen/ki-telefonassistent',
					showCrown: true,
					highlight: true
				};
		}
	};
</script>

<svelte:head>
	<title
		>{$i18n.t('Welcome to IONOS GPT,', { ns: 'ionos' })}
		{$i18n.t('Where AI becomes your ultimate team of experts!', { ns: 'ionos' })}</title
	>
</svelte:head>

<content class="flex flex-col items-center text-blue-800 w-full md:px-8">
	<div class="max-w-[1024px] w-full flex flex-col items-center">
		<div class="grid grid-cols-[repeat(auto-fit,320px)] justify-center gap-6 w-full mb-8 max-w-5xl">
			<h1
				class="col-span-full my-5 font-overpass font-normal text-3xl leading-tight text-left gradient-text"
			>
				{$i18n.t('ai.team.title.1', { ns: 'ionos' })} <span class="emoji">🚀</span> {$i18n.t('ai.team.title.2', { ns: 'ionos' })}
			</h1>

			<div class="col-span-full flex items-center gap-2 flex-wrap">
				<span class="font-sans font-normal text-lg">{$i18n.t('ai.team.nav', { ns: 'ionos' })}</span>
			</div>
			{#each agents as agent}
				<AgentCard {agent} on:select={(e) => selectAgentInternal(e.detail)} />
			{/each}
		</div>
	</div>
</content>

<style>
	:global(body) {
		background-color: #f9f9f9;
	}

	.gradient-text {
        background: linear-gradient(89.99deg, #095BB1 0.01%, #560E8A 79.99%);
		-webkit-background-clip: text;
		background-clip: text;
		-webkit-text-fill-color: transparent;
	}

	.gradient-text .emoji {
		-webkit-text-fill-color: initial;
		background: none;
		-webkit-background-clip: initial;
		background-clip: initial;
	}
</style>
