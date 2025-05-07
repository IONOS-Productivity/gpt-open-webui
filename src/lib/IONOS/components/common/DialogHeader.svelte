<script lang="ts">
	import type { Readable } from 'svelte/store';
	import type { I18Next } from '$lib/IONOS/i18next.d.ts';
	import { getContext } from 'svelte';
	import { createEventDispatcher } from 'svelte';
	import XMark from '$lib/IONOS/components/icons/XMark.svelte';

	const dispatch = createEventDispatcher();

	const i18n = getContext<Readable<I18Next>>('i18n');

	export let closable = true;
	export let title = '';
	export let dialogId = title;
</script>

<div class="flex items-center justify-between {$$props.class}" class:border-b={closable}>
	<h1 class="font-semibold text-sm text-blue-800">
		{title}
	</h1>
	{#if closable}
		<button class="justify-self-end" data-id="dialog-close-{dialogId}" on:click={() => dispatch('close') }>
			<XMark />
		</button>
	{/if}
</div>
