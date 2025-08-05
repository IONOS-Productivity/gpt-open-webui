<script lang="ts">
	import type { Readable } from 'svelte/store';
	import type { I18Next } from '$lib/IONOS/i18next.d.ts';
	import { getContext } from 'svelte';
	import Dialog from '$lib/IONOS/components/common/Dialog.svelte';
 	import FilledUserAvatar from '$lib/IONOS/components/icons/FilledUserAvatar.svelte';
	import DialogHeader from '$lib/IONOS/components/common/DialogHeader.svelte';
 	import Gear from '$lib/IONOS/components/icons/Gear.svelte';
	import General from './General.svelte';
	import Account from './Account.svelte';
	import NavItem from './NavItem.svelte';
	import { showSettings, mobile } from '$lib/stores';
	const i18n = getContext<Readable<I18Next>>('i18n');

	export let show = false;

	let section = 'general';
	let animationDuration = 200;
</script>

<Dialog
	dialogId="settings"
	{show}
	{animationDuration}
	class="p-0 md:min-h-[400px] h-screen w-screen md:max-h-fit md:min-w-[750px] md:max-w-[750px] transition-transform duration-[{animationDuration}ms] ease-out {show ? 'translate-y-0' : 'translate-y-[90dvh]'}"
>
	<DialogHeader
		slot="header"
		title={$i18n.t("Settings", { ns: 'ionos' })}
		on:close={() => {
			showSettings.set(false);
		}}
		dialogId="settings"
		class="p-[30px] border-gray-200 border-b"
	/>

	<div slot="content" class="flex flex-col md:flex-row sm:gap-[30px] p-5 text-blue-800">
		{#if !$mobile}
			<nav class="w-48 shrink-0">
				<ul class="flex flex-col">
					<li class="mb-3">
						<NavItem bind:group={section} value="general">
							<Gear slot="icon" className="inline s-4"/>
							<span class="ml-2 text-sm">
								{$i18n.t('General', { ns: 'ionos' })}
							</span>
						</NavItem>
					</li>
					<li class="mb-3">
						<NavItem bind:group={section} value="account">
							<FilledUserAvatar slot="icon" className="inline s-4"/>
							<span class="ml-2 text-sm">
								{$i18n.t('Account', { ns: 'ionos' })}
							</span>
						</NavItem>
					</li>
				</ul>
			</nav>

			<div class="flex-grow pr-2.5">
				{#if section === 'general'}
					<General />
				{:else if section === 'account'}
					<Account />
				{/if}
			</div>
		{:else}
			<General />
			<hr />
			<Account />
		{/if}
	</div>
</Dialog>
