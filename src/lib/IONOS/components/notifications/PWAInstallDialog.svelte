<script lang="ts">
	import type { Readable } from 'svelte/store';
	import type { I18Next } from '$lib/IONOS/i18next.d.ts';
	import Dialog from '$lib/IONOS/components/common/Dialog.svelte';
	import Touch from '$lib/IONOS/components/icons/Touch.svelte';
	import Share from '$lib/IONOS/components/icons/Share.svelte';
	import Button from '$lib/IONOS/components/common/Button.svelte';
	import { ButtonType } from '$lib/IONOS/components/common/buttons.ts';
	import { getContext } from 'svelte';
	import { createEventDispatcher } from 'svelte';
	import { isIOSDevice, isSafari } from '$lib/IONOS/services/pwa';
	import DialogHeader from '$lib/IONOS/components/common/DialogHeader.svelte';

	const i18n = getContext<Readable<I18Next>>('i18n');
	const dispatch = createEventDispatcher();

	export let show = false;

	const showIOSInstructions = isIOSDevice() && isSafari();

	const handleInstall = () => {
		dispatch('install');
		show = false;
	};

	const handleLater = () => {
		dispatch('dismiss');
		show = false;
	};
</script>

<Dialog bind:show on:close={handleLater}
	dialogId="pwa-install"
	class="p-[30px] items-end md:items-center pb-[25px] px-[25px] max-md:mb-0 {show ? 'max-md:translate-y-[-5dvh]' : 'max-md:translate-y-[50dvh]'}"
	animationDuration={150}
	mobileCover={false}
>
	<DialogHeader closable={false} slot="header" />
	<div slot="content" class="w-full ">
		{#if showIOSInstructions}
			<!-- iOS Installation Instructions -->
			<div class="text-center mb-6">
				<div class="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
					<Touch className="w-8 h-8 text-blue-600" />
				</div>
				<h3 class="text-xl font-semibold text-gray-900 mb-2">
					{$i18n.t('Install IONOS GPT', { ns: 'ionos' })}
				</h3>
				<p class="text-gray-600 mb-6">
					{$i18n.t('For quick and easy access, you can now install IONOS GPT like an app!', { ns: 'ionos' })}
				</p>
			</div>

			<div class="space-y-4 mb-6">
				<div class="flex items-start space-x-3">
					<div class="flex-shrink-0 w-6 h-6 bg-blue-600 rounded-full flex items-center justify-center">
						<span class="text-white text-sm font-medium">1</span>
					</div>
					<div class="flex-1">
						<p class="text-gray-900">
							{$i18n.t('Tap the Share button', { ns: 'ionos' })}
							<Share className="inline w-4 h-4 mx-1" />
						</p>
					</div>
				</div>

				<div class="flex items-start space-x-3">
					<div class="flex-shrink-0 w-6 h-6 bg-blue-600 rounded-full flex items-center justify-center">
						<span class="text-white text-sm font-medium">2</span>
					</div>
					<div class="flex-1 flex flex-row gap-1">
						<p class="text-gray-900">
							{$i18n.t('Select', { ns: 'ionos' })}
						</p>
						<p class="font-semibold">{$i18n.t('Add to Home Screen', { ns: 'ionos' })}</p>
					</div>
				</div>
			</div>
		{:else}
			<!-- Standard PWA Installation -->
			<div class="text-center mb-6">
				<div class="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
					<Touch className="w-8 h-8 text-blue-600" />
				</div>
				<h3 class="text-xl font-semibold text-gray-900 mb-2">
					{$i18n.t('Install IONOS GPT', { ns: 'ionos' })}
				</h3>
				<p class="text-gray-600 mb-6">
					{$i18n.t('For quick and easy access, you can now install IONOS GPT like an app!', { ns: 'ionos' })}
				</p>
			</div>

			<div class="flex justify-center space-x-3">
				<Button
					on:click={handleInstall}
					type={ButtonType.primary}
					className="transition-colors"
				>
					{$i18n.t('Install IONOS GPT', { ns: 'ionos' })}
				</Button>
			</div>
		{/if}
	</div>
</Dialog>
