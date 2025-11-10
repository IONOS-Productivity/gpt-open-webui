<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import CircleInfo from '../icons/CircleInfo.svelte';
	import Crown from '../icons/Crown.svelte';
	import Dialog from '$lib/IONOS/components/common/Dialog.svelte';
	import AgentCardDetail from './AgentCardDetail.svelte';
	import type { IAgentAiTeam } from '../../../../routes/ai-team/ai-team.type';

	export let agent: IAgentAiTeam;

	const dispatch = createEventDispatcher();

	let showDetail = false;

	function openDetail() {
		showDetail = true;
	}

	function closeDetail() {
		showDetail = false;
	}

	function handleCardClick() {
		dispatch('select', agent.id);
	}
</script>

<div
	class="w-[320px] gap-4 opacity-100 rounded-2xl p-6 shadow-l cursor-pointer"
	class:bg-white={!agent.bgColor}
	style="{agent.bgColor ? `background-color: ${agent.bgColor};` : ''}"
	on:click={handleCardClick}
	on:keydown={(e) => e.key === 'Enter' && handleCardClick()}
	role="button"
	tabindex="0"
>
	<div class="flex items-center gap-4 mb-4 relative">
		{#if agent.id}
			<img src={`/avatars/${agent.id}.jpg`} alt="Model Avatar" class="w-8 h-8 rounded-full" />
		{:else}
			<div
				class="w-8 h-8 rounded-full bg-gradient-to-r from-blue-500 to-purple-700 flex items-center justify-center text-white font-semibold"
			>
				{agent.name.charAt(0)}
			</div>
		{/if}
		<div>
			<h3
				class="text-xs font-semibold leading-tight font-sans"
				class:text-gray-900={!agent.fontColor}
				style={agent.fontColor ? `color: ${agent.fontColor};` : ''}
			>
				{agent.name}
			</h3>
			{#if agent.specialty}
				<p
					class="text-xs font-normal leading-[150%] font-sans"
					style={agent.fontColor ? `color: ${agent.fontColor};` : ''}
				>
					{agent.specialty}
				</p>
			{/if}
		</div>
		<button
			type="button"
			class="absolute top-0 right-0 cursor-pointer bg-transparent border-none p-0"
			style={agent.fontColor ? `color: ${agent.fontColor};` : ''}
			on:click={(e) => {
				e.stopPropagation();
				openDetail();
			}}
			aria-label="View agent details"
		>
			{#if agent.showCrown}
				<Crown className="w-5 h-5" />
			{:else}
				<CircleInfo className="w-5 h-5" />
			{/if}
		</button>
	</div>

	<p
		class="text-xs font-normal leading-[150%] font-sans"
		class:text-gray-700={!agent.fontColor}
		style={agent.fontColor ? `color: ${agent.fontColor};` : ''}
	>
		{agent.description}
	</p>
</div>


<Dialog
	bind:show={showDetail}
	on:close={closeDetail}
	mobileCover={false}
	class="!p-0 !w-fit !h-fit !max-h-[90vh] overflow-y-auto {showDetail ? 'max-md:translate-y-[0]' : 'max-md:translate-y-[100dvh]'}"
>
	<div slot="content">
		<AgentCardDetail {agent} on:close={closeDetail} on:select />
	</div>
</Dialog>