<script lang="ts">
	import { createEventDispatcher } from 'svelte';

	const dispatch = createEventDispatcher();

	export let show = false;
	export let dialogId = 'dialog';

	let el: HTMLDialogElement|null = null;

	$: if (show) {
		el?.showModal();
	} else {
		el?.close();
	}

	function onToggle(e) {
		if (!e.target.open) {
			dispatch('close');
		}
	}
</script>

<dialog
	on:toggle={onToggle}
	bind:this={el}
	class="fixed top-0 right-0 left-0 bottom-0 m-auto bg-white z-[99999999] overflow-hidden overscroll-contain shadow-xl rounded-2xl {$$props.class ?? 'p-[30px]'}"
>
	<div
		data-id={`dialog-${dialogId}`}
		class="flex flex-col bg-white relative"
	>
		<slot name="header" />

		<div
			data-id={`dialog-content-${dialogId}`}
			class=""
		>
			<slot name="content"/>
		</div>
	</div>
</dialog>

<style>
	dialog::backdrop {
		background-color: rgba(0, 0, 0, 0.75);
	}
</style>
