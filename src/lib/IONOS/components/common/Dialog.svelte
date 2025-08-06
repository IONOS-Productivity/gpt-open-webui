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

	/**
	 * Handle close via Escape key.
	 * See https://html.spec.whatwg.org/multipage/interactive-elements.html#close-the-dialog
	 */
	function onToggle(e) {
		if (!e.target.open) {
			dispatch('close');
		}
	}
</script>

<dialog
	on:toggle={onToggle}
	bind:this={el}
	closedby="any"
	class="fixed top-0 right-0 left-0 bottom-0 m-auto bg-white backdrop:bg-black/25 z-[99999999] overflow-hidden overscroll-contain shadow-xl rounded-2xl {$$props.class ?? 'p-[30px]'}"
>
	<div
		data-id={`dialog-${dialogId}`}
		class="flex flex-col relative"
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
