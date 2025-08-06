<script lang="ts">
	export let show = false;
	export let dialogId = 'dialog';
	export let positioning = 'items-center';
	let el: HTMLDialogElement|null = null;

	export let animationDuration = 400;
	export let showTranslate = '';

	$: if (show) {
		console.log("Dialog: show, flex immediately")
		// el?.showModal();
		el?.classList.remove('hidden');
		el?.classList.add('flex');
	} else {
		console.log("Dialog: hide, defer unflex+close deferred")
		setTimeout(() => {
			console.log("Dialog: hide, defer unflex+close NOW")
			// el?.close();
			el?.classList.remove('flex');
			el?.classList.add('hidden');
		}, animationDuration + 100);
	}
</script>

<div
	bind:this={el}
	class="fixed top-0 hidden right-0 left-0 bottom-0 m-0 bg-black/75 h-screen max-w-[100vw] w-[100vw] max-h-[100dvh] justify-center items-center z-[99999999] overflow-hidden overscroll-contain {positioning} center">
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
</div>
