<script lang="ts">
	import type { Readable } from 'svelte/store';
	import type { I18Next } from '$lib/IONOS/i18next.d.ts';
	import { getContext } from 'svelte';
	import Dialog from '$lib/IONOS/components/common/Dialog.svelte';
	import Button, { ButtonType } from '$lib/IONOS/components/common/Button.svelte';
	import DialogHeader from '$lib/IONOS/components/common/DialogHeader.svelte';

	const i18n = getContext<Readable<I18Next>>('i18n');

	export let title = '';
	export let show = false;
	export let confirmText = $i18n.t('OK');
	export let confirmHandler = () => { };
	export let cancelText = $i18n.t('Cancel');
	export let cancelHandler = () => { };
</script>

<Dialog
	dialogId="confirmation-dialog"
	class="p-[30px] items-end md:items-center pb-[25px] px-[25px] max-md:mb-0 {show ? 'max-md:translate-y-[-5dvh]' : 'max-md:translate-y-[50dvh]'}"
	{show}
	mobileCover={false}
>
	<DialogHeader
			slot="header"
			{title}
			closable={false}
			dialogId="confirmation-dialog"
			class="mb-2.5 text-center md:text-left"
		/>
	<div slot="content" class="flex flex-col max-w-dvw md:min-w-[calc(400px-60px)] md:max-w-[calc(550px-60px)] text-blue-800">
		<div class="mb-2.5 text-sm text-center md:text-left" >
			<slot />
		</div>

		<div class="flex flex-col md:flex-row justify-end mt-2.5 gap-2.5">
			<div class="order-2 md:order-1 m-auto md:m-0">
				<Button
					on:click={cancelHandler}
					type={ButtonType.tertiary}
				>
					{cancelText}
				</Button>
			</div>
			<div class="order-1 md:order-2 m-auto md:m-0">
				<Button
					on:click={() => { confirmHandler() }}
					type={ButtonType.caution}
				>
					{confirmText}
				</Button>
			</div>
		</div>
	</div>
</Dialog>
