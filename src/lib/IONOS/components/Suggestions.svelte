<script lang="ts">
	import { getContext, createEventDispatcher } from 'svelte';
	import prompts from '$lib/IONOS/configs/ionosPromptSuggestions.json'

	const dispatch = createEventDispatcher();

	export let className = '';
</script>

<div class="flex flex-wrap justify-center {className}">
	{#each prompts as prompt, promptIdx}
		<button
			class="flex flex-col shrink-0 basis-64 w-52 justify-between items-center px-3 py-2 rounded-xl bg-transparent hover:bg-black/5 hover:text-ionos dark:hover:bg-white/5 transition group"
			on:click={() => {
				dispatch('select', { prompt: prompt.content, model: prompt.model });
			}}
		>
		<div class="text-xl h-10">{prompt.description}</div>
		<img class="w-32 h-14 m-4" src={prompt.iconUrl} />
		<div class="h-10">{prompt.detail}</div>
		</button>
	{/each}
</div>
