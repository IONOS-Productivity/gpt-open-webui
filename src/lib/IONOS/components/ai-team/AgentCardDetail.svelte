<script lang="ts">
	import XMark from '$lib/components/icons/XMark.svelte';
	import { createEventDispatcher } from 'svelte';
	import type { IAgentAiTeam } from './ai-team.type';
	import Checkmark from '../icons/Checkmark.svelte';
	import Button from '$lib/IONOS/components/common/Button.svelte';
	import Sparkles from '$lib/components/icons/Sparkles.svelte';

	const dispatch = createEventDispatcher();

	export let agent: IAgentAiTeam;

	function close() {
		dispatch('close');
	}

	function startChat() {
		dispatch('select', agent.id);
		close();
	}
</script>

<div
	class="w-full max-w-md flex flex-col gap-4 opacity-100 rounded-2xl p-4 sm:p-8 bg-white shadow-l"
>
	<div class="flex justify-end relative z-10">
		<button
			type="button"
			class="cursor-pointer bg-transparent border-none p-0"
			on:click={close}
			aria-label="Close dialog"
		>
			<XMark className="w-5 h-5" />
		</button>
	</div>
	<div class="flex items-center gap-4">
		{#if agent.id}
			<img
				src={`/avatars/${agent.id}.jpg`}
				alt={agent.name}
				class="w-20 h-20 sm:w-30 sm:h-30 rounded-full flex-shrink-0"
			/>
		{:else}
			<div
				class="w-20 h-20 sm:w-30 sm:h-30 rounded-full bg-gradient-to-r from-blue-500 to-purple-700 flex items-center justify-center text-white font-bold text-xl sm:text-2xl flex-shrink-0"
			>
				{agent.name.charAt(0)}
			</div>
		{/if}

		<div class="flex-1">
			<h2
				class="font-overpass font-normal text-2xl leading-8 sm:leading-10 text-gray-900 mb-1"
			>
				{agent.name}
			</h2>
			{#if agent.speciality}
				<h3 class="font-sans font-normal text-lg mb-2">
					{agent.speciality}
				</h3>
			{/if}
		</div>
	</div>

	<div>
		<p class="font-sans font-normal text-sm leading-[150%] text-gray-700">
			{agent.description}
		</p>
	</div>

	<!-- Capabilities Section -->
	{#if agent.capabilities && agent.capabilities.length > 0}
		<div>
			<h4 class="font-sans font-semibold text-sm leading-tight mb-3">
				Capabilities
			</h4>
			<div class="flex flex-col">
				{#each agent.capabilities as capability}
					<div class="flex items-center py-1 gap-2">
						<span
							class="w-6 h-6 rounded-full flex justify-center items-center text-blue-600 bg-blue-200"
							><Checkmark className="w-3 h-3" /></span
						>
						<span class="font-sans font-normal text-sm leading-normal"
							>{capability}</span
						>
					</div>
				{/each}
			</div>
		</div>
	{/if}

	<div class="flex gap-3 pt-4">
		<Button
			className="w-full !bg-purple-700 !border-purple-700 hover:!bg-purple-700/90 hover:!border-purple-700/90"
			on:click={startChat}
		>
			<span class="font-sans font-semibold text-sm leading-normal text-center flex justify-center items-center gap-2">
                Chat now <span class="text-purple-300"><Sparkles className="w-4 h-4 fill-purple-300" /></span>
            </span>
		</Button>
	</div>
</div>