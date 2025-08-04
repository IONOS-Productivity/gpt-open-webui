<script lang="ts">
	import type { Readable } from 'svelte/store';
	import type { I18Next } from '$lib/IONOS/i18next.d.ts';
	import { getContext } from 'svelte';
	import Dialog from '$lib/IONOS/components/common/Dialog.svelte';

	const i18n = getContext<Readable<I18Next>>('i18n');

	export let show: boolean = false;

	let animationDuration = 200;
</script>

<Dialog
	dialogId="subsetting-dialog"
	{animationDuration}
	class="p-0 md:min-h-[400px] h-screen w-screen md:max-h-fit md:min-w-[750px] md:max-w-[750px] overflow-y-scroll transition-transform duration-[{animationDuration}ms] ease-out {show ? '-translate-x-0' : '-translate-x-full'}"
	bind:show
>
	<div slot="header">
		<slot name="header" />
	</div>
	<div slot="content">
		<slot name="content" />
	</div>
</Dialog>
