<script lang="ts">
	import { getContext, createEventDispatcher } from 'svelte';
	import prompts from '$lib/IONOS/configs/ionosPromptSuggestions.json'
	import randomSelection from '$lib/IONOS/utils/randomSelection.ts'

	const dispatch = createEventDispatcher();

	const maxSuggestionsToDisplay = 3;

	// Filter for model
	export let model;
	export let className = '';

	$: suggestionsPerModel = prompts.filter(({ model: currentModel }) => model === currentModel);
	$: promptSelection = randomSelection(suggestionsPerModel, maxSuggestionsToDisplay)
</script>

<div class="flex flex-wrap md:flex-row md:flex-wrap justify-center {className}">
	{#each promptSelection as prompt, promptIdx}
	<div class="m-1 flex flex-col md:flex-wrap shrink-0 md:basis-52 h-50 w-full md:w-auto">
		<button
			type="radio"
			class="flex flex-col items-center h-full content px-3 py-2 rounded-xl bg-transparent border-2 border-gray-200 hover:bg-black/5 hover:text-ionos dark:hover:bg-white/5 transition"
			on:click={() => {
				dispatch('select', { prompt: prompt.content, model: prompt.model, modelName: prompt.modelName });
			}}
		>
			<div class="flex-1 text-center text-base">{prompt.description}</div>
			<div class="flex-1 text-center text-xs mt-2">{prompt.detail}</div>
		</button>
	</div>
	{/each}
</div>

<style>
input {
	display: none;
}
.masked {
	mask-repeat: no-repeat;
	mask-position: center;
}
input:hover .image {
	background-color: var(--ion-brand-color);
}
input:checked + label {
	border: 2px solid var(--ion-brand-color);
}
</style>
