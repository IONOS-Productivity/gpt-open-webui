<script lang="ts">
	export let show = false;
	export let dialogId = 'dialog';
	export let positioning = 'items-center';
	let el: HTMLDialogElement|null = null;

	export let animationDuration = 200;

	$: if (show) {
		el?.classList.add('flex');
		el?.showModal();
	} else {
		setTimeout(() => {
			el?.close();
			el?.classList.remove('flex');
		}, animationDuration);
	}
</script>

<dialog
	bind:this={el}
	class="fixed top-0 right-0 left-0 bottom-0 m-0 bg-black/75 h-screen max-w-[100vw] w-[100vw] max-h-[100dvh] justify-center items-center z-[99999999] overflow-hidden overscroll-contain {positioning}"
>
	<div
		data-id={`dialog-${dialogId}`}
		class="{$$props.class ?? 'p-[30px]'} flex flex-col bg-white relative shadow-xl rounded-2xl md:translate-none"
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
