<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import XMark from '$lib/IONOS/components/icons/XMark.svelte';
	import ChevronLeft from '$lib/IONOS/components/icons/ChevronLeft.svelte';

	const dispatch = createEventDispatcher();

	export let closable = true;
	export let title = '';
	export let dialogId = title;
	export let submenu = false;
</script>

<div class="flex items-center justify-between gap-2.5 {$$props.class} " >
	{#if closable && submenu}
		<button class="justify-self-start" data-id="dialog-close-{dialogId}" on:click={() => dispatch('close') }>
			<ChevronLeft />
		</button>
	{/if}
	<h1 class="grow font-semibold text-sm text-blue-800">
		{title}
	</h1>
	{#if closable && !submenu}
		<button class="justify-self-end" data-id="dialog-close-{dialogId}" on:click={() => dispatch('close') }>
			<XMark />
		</button>
	{/if}
</div>
