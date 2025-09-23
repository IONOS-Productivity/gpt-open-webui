<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import { slideDuration } from '$lib/IONOS/components/constants';
	import { mobile } from '$lib/stores';
	import XMark from '$lib/IONOS/components/icons/XMark.svelte';

	const dispatch = createEventDispatcher();

	export let show = false;
	/**
	 * Cover whole viewport for mobile
	 */
	export let mobileCover = true;
	export let dialogId = 'dialog';
	let el: HTMLDialogElement|null = null;

	$: if (show) {
		el?.showModal();
	} else if (!show && !$mobile) {
		el?.close();
	}

	/**
	 * Mobile: show -> false changes the transition, which then
	 * triggers the transitionend event.
	 * Non-mobile: immediately closed
	 */
	function onTransitionEnd(e) {
		if (e.target == el && e.propertyName === 'translate' && !show) {
			el?.close();
		}
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

	function close() {
		show = false;
		dispatch('close');
	}
</script>

<dialog
	on:toggle={onToggle}
	on:close={close}
	on:transitionend={onTransitionEnd}
	bind:this={el}
	closedby="any"
	style:--slide-duration="{slideDuration}ms"
>

	<div class="fixed top-0 right-0 left-0 bottom-0 m-auto bg-white backdrop:bg-black/75 z-[99999999] overscroll-contain shadow-xl rounded-2xl {mobileCover ? 'max-md:h-full max-md:max-h-dvh max-md:w-dvw max-md:max-w-dvw max-md:m-0' : ''} max-md:transition-transform duration-(--slide-duration)  ease-out {$$props.class ?? 'p-[30px]'}">
		<div class="relative top-[-50px] flex justify-center max-md:hidden">
			<button on:click={() => close()}>
				<XMark />
			</button>
		</div>

		<div
			data-id={`dialog-${dialogId}`}
			class="min-h-full flex flex-col"
		>
			<slot name="header" />

			<div
				data-id={`dialog-content-${dialogId}`}
				class="flex flex-col flex-1"
			>
				<slot name="content"/>
			</div>
		</div>
	</div>
</dialog>
