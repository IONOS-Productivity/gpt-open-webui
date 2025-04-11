<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import Button, { ButtonType } from '$lib/IONOS/components/common/Button.svelte'
	const dispatch = createEventDispatcher();

	export let type: ButtonType|null = null;
	export let accept: string = '*';
	export let multiple: boolean = true;

	let inputEl: HTMLInputElement|null = null;
	let files: FileList;
	let value = '';

	function change() {
		if (!files || files.length === 0) {
			console.warn('File change handler: no files in collection?');
			return;
		}

		dispatch('selected', [...files]);
	}
</script>

<label class="cursor-pointer">
	{#if type === null}
		<slot />
	{/if}
	<input
		type="file"
		bind:value={value}
		bind:files={files}
		bind:this={inputEl}
		{accept}
		{multiple}
		on:change={change}
		class="hidden"
	/>
</label>

{#if type !== null}
	<Button
		on:click={() => { inputEl?.click?.(); } }
		{type}
	>
		<slot />
	</Button>
{/if}
