<script lang="ts">
	import type { Readable } from 'svelte/store';
	import type { I18Next } from '$lib/IONOS/i18next.d.ts';
	import { getContext } from 'svelte';
	import { signout } from '$lib/services/auths';
	import Button, { ButtonType } from '$lib/IONOS/components/common/Button.svelte';
	import Dialog from '$lib/IONOS/components/common/Dialog.svelte';
 	import FilledUserAvatar from '$lib/IONOS/components/icons/FilledUserAvatar.svelte';
	import DialogHeader from '$lib/IONOS/components/common/DialogHeader.svelte';
 	import Gear from '$lib/IONOS/components/icons/Gear.svelte';
	import General from './General.svelte';
	import Account from './Account.svelte';
	import NavItem from './NavItem.svelte';
	import { showSettings, mobile, user } from '$lib/stores';
	import Stacks from '$lib/IONOS/components/icons/Stacks.svelte';
	import ChevronRight from '$lib/IONOS/components/icons/ChevronRight.svelte';
	import LifeRing from '$lib/IONOS/components/icons/LifeRing.svelte';
	import ArrowUpRightFromSquare from '$lib/IONOS/components/icons/ArrowUpRightFromSquare.svelte';
	import LightbulbShining from '$lib/IONOS/components/icons/LightbulbShining.svelte';
	import Logout from '$lib/IONOS/components/icons/Logout.svelte';
	const i18n = getContext<Readable<I18Next>>('i18n');
	import { showKnowlegeManager } from '$lib/IONOS/stores/dialogs';
	import { buildSurveyUrl } from '$lib/IONOS/services/survey';

	export let show = false;

	let section = 'general';
	const surveyUrl = buildSurveyUrl($user!);
</script>

<Dialog
	dialogId="settings"
	show={show}
	on:close={() => { showSettings.set(false); } }
	class="p-0 md:min-h-[400px] md:min-w-[750px] md:max-w-[750px] md:max-h-fit overflow-y-scroll {show ? 'max-md:translate-y-0' : 'max-md:translate-y-[100dvh]'}"
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
			<div class="flex flex-col gap-5">
				<div>
					<div class="flex flex-row gap-2.5 mb-5">
						<Gear />
						<span class=" font-semibold text-sm">
							{$i18n.t('General', { ns: 'ionos' })}
						</span>
					</div>
					<General />
				</div>
				<div>
					<div class="flex flex-row gap-2.5 py-2.5">
						<Stacks />
						<span class=" font-semibold text-sm">
							{$i18n.t('Knowledge Management', { ns: 'ionos' })}
						</span>
					</div>
					<button class="w-full text-left flex flex-row gap-2.5 py-5 border-b border-gray-200"
						on:click={() => {
							showKnowlegeManager(true);
					}}>
						<span class="grow text-sm">
							{$i18n.t('Manage knowledge bases', { ns: 'ionos' })}
						</span>
						<ChevronRight />
					</button>
				</div>
				<div>
					<div class="flex flex-row gap-2.5 mb-5 mt-2.5">
						<FilledUserAvatar />
						<span class=" font-semibold text-sm">
							{$i18n.t('Account', { ns: 'ionos' })}
						</span>
					</div>
					<Account />
				</div>
				<div>
					<div class="flex flex-row gap-2.5 py-2.5">
						<LifeRing />
						<span class="font-semibold text-sm">
							{$i18n.t('Support', { ns: 'ionos' })}
						</span>
					</div>
					<a class="flex flex-row gap-2.5 py-5 border-b border-gray-200"
						href="https://www.ionos.de/hilfe/index.php?id=25241" target="_blank">
						<span class="grow text-sm">
							{$i18n.t('Help & FAQ', { ns: 'ionos' })}
						</span>
						<ArrowUpRightFromSquare />
					</a>
					{#if surveyUrl}
						<a class="flex flex-row gap-2.5 py-5 border-b border-gray-200"
						href={surveyUrl} target="_blank" rel="noopener noreferrer">
							<span class="grow text-sm">
								{$i18n.t('Feedback', { ns: 'ionos' })}
							</span>
							<LightbulbShining />
						</a>
					{/if}
				</div>
				<Button
					type={ButtonType.secondary}
					className="flex justify-center transition"
					on:click={() => { signout(); show = false; }}
				>
					<div class="flex row gap-1">
						<Logout />
						<div class=" self-center truncate">{$i18n.t('Sign Out')}</div>
					</div>
				</Button>
			</div>
		{/if}
	</div>
</Dialog>
