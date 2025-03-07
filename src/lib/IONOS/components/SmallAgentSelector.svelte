<script lang="ts">
	import { getContext, onMount } from 'svelte';
	import { models, settings } from '$lib/stores';
	import { updateUserSettings } from '$lib/apis/users';

	export let selectedModels = [''];

	$: modelsUi = $models
		.filter(({ id }) => !id.includes('/') && id !== 'arena-model')
		.map((model) => ({
			id: model.id,
			modelDisplayName: model.name,
		}));

	const save = async () => {
		const hasEmptyModel = selectedModels.filter((it) => it === '');
		if (hasEmptyModel.length) {
			throw new Error('selectedModels contains empty entry');
		}
		settings.set({ ...$settings, models: selectedModels });
		await updateUserSettings(localStorage.token, { ui: $settings });
	};

	const select = (id) => {
		selectedModels = [id];
		save();
	}
</script>

<div class="">
	{#each modelsUi as { id, modelDisplayName }}
		<button
			data-model-id={id}
			on:click={() => select(id)}
			class="m-auto px-4 py-2 mx-4 border-2 border-blue-500 bg-white-500 hover:bg-blue-700 text-black hover:text-white transition rounded-3xl"
		>
			{modelDisplayName}
		</button>
	{/each}
</div>
