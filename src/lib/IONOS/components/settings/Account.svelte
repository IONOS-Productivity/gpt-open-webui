<script lang="ts">
	import { toast } from 'svelte-sonner';
	import type { Readable } from 'svelte/store';
	import type { I18Next } from '$lib/IONOS/i18next.d.ts';
	import { getContext } from 'svelte';
	import Button, { ButtonType } from '$lib/IONOS/components/common/Button.svelte'
	import Confirm from '$lib/IONOS/components/common/Confirm.svelte';
	import ChevronRight from '$lib/IONOS/components/icons/ChevronRight.svelte';
	import LoadingCover from '$lib/IONOS/components/common/LoadingCover.svelte';
	import { config, user } from '$lib/stores';
	import { resetPassword, deleteAccount } from '$lib/IONOS/services/account'
	import { buildSurveyUrl } from '$lib/IONOS/services/survey';
	import SubSettingPage from './SubSettingPage.svelte';
	import SettingInfo from './SettingInfo.svelte';
	import DialogHeader from '$lib/IONOS/components/common/DialogHeader.svelte';
	import GarbageBin from '$lib/IONOS/components/icons/GarbageBin.svelte';
	import ArrowsRotate from '$lib/IONOS/components/icons/ArrowsRotate.svelte';
	const i18n = getContext<Readable<I18Next>>('i18n');

	let confirmAccountDeletion = false;
	let showSecuritySubsettings = false;
	let loading = false;
	const surveyUrl = buildSurveyUrl($user!);

	async function onDeleteAccountConfirmed() {
		try {
			confirmAccountDeletion = false;
			loading = true;
			await deleteAccount();
		} catch(e) {
			toast.error($i18n.t('Deleting your account failed.', { ns: 'ionos' }));
		}
	}
</script>

<div class="flex flex-col md:gap-5 text-sm">
	<div class="flex flex-row items-center h-[60px] md:h-10 md:border-none border-b border-gray-200">
		<div class="flex-grow">
			{$i18n.t('Email', { ns: 'ionos' })}
		</div>
		<div>
			{$user?.email}
		</div>
	</div>
	<div class="hidden md:flex flex-row items-center h-[60px] md:h-10">
		<div class="flex-grow">
			{$i18n.t('Reset password', { ns: 'ionos' })}
		</div>
		<div>
			<Button
				on:click={() => resetPassword()}
				type={ButtonType.secondary}>
				{$i18n.t('Reset password', { ns: 'ionos' })}
			</Button>
		</div>
	</div>
	<div class="hidden md:flex flex-row items-center h-[60px] md:h-10">
		<div class="flex-grow">
			{$i18n.t('Delete account', { ns: 'ionos' })}
		</div>
		<div>
			<Button
				on:click={() => { confirmAccountDeletion = true; }}
				type={ButtonType.caution}>
				{$i18n.t('Delete account', { ns: 'ionos' })}
			</Button>
		</div>
	</div>
	<div class="md:hidden flex flex-row gap-2.5 h-[60px] items-center border-b border-gray-200"
		role="button"
		on:click={() => { showSecuritySubsettings = true; }}
	>
		<span class="text-sm grow">
			{$i18n.t('Security', { ns: 'ionos' })}
		</span>
		<ChevronRight />
	</div>
</div>

{#if loading}
	<LoadingCover />
{/if}

<Confirm
	title={$i18n.t('Do you want to delete your account?', { ns: 'ionos' })}
	show={confirmAccountDeletion}
	confirmText={$i18n.t('Delete my account', { ns: 'ionos' })}
	confirmHandler={onDeleteAccountConfirmed}
	cancelHandler={() => { confirmAccountDeletion = false; }}
>
	<p class="my-3">
		{$i18n.t('All your chats and uploaded documents will be lost.', { ns: 'ionos' })}
	</p>

	<p class="my-3">
		{$i18n.t('This action can not be undone.', { ns: 'ionos' })}
	</p>
</Confirm>

<SubSettingPage bind:show={showSecuritySubsettings}>
	<DialogHeader
		slot="header"
		title={$i18n.t("Security", { ns: 'ionos' })}
		on:close={() => {
			showSecuritySubsettings = false;
		}}
		submenu={true}
		dialogId="security"
		class="p-[30px] border-gray-200 border-b"
	/>

	<div slot="content" class="p-5  text-blue-800 text-sm">
		<div class="flex flex-row items-center h-[60px] border-b border-gray-200" on:click={() => resetPassword()} role="button">
			<div class="flex-grow">
				{$i18n.t('Reset password', { ns: 'ionos' })}
			</div>
			<ArrowsRotate />
		</div>
		<SettingInfo>
			{$i18n.t('When you reset your password, you will be redirected to an external site to complete the process.', { ns: 'ionos' })}
		</SettingInfo>
		<div class="flex flex-row items-center h-[60px] border-b border-gray-200" on:click={() => { confirmAccountDeletion = true;}} role="button">
			<div class="flex-grow">
				{$i18n.t('Delete account', { ns: 'ionos' })}
			</div>
			<GarbageBin />
		</div>
		{#if surveyUrl}
			<SettingInfo>
				<span>
					{$i18n.t('We’d really prefer you didn’t delete your account. Instead, help us get better →', { ns: 'ionos' })}
					<a class="font-semibold underline" href={surveyUrl} target="_blank" rel="noopener noreferrer">
						{$i18n.t('Share your feedback here', { ns: 'ionos' })}
					</a>
				</span>
			</SettingInfo>
		{/if}
	</div>
</SubSettingPage>
