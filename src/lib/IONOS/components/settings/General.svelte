<script lang="ts">
	import type { Readable } from 'svelte/store';
	import { toast } from 'svelte-sonner';
	import type { I18Next } from '$lib/IONOS/i18next.d.ts';
	import { getContext } from 'svelte';
	import Confirm from '$lib/IONOS/components/common/Confirm.svelte';
	import Button, { ButtonType } from '$lib/IONOS/components/common/Button.svelte'
	import {
		deleteAll,
		exportAll,
	} from '$lib/IONOS/services/chats';
	import GarbageBin from '$lib/IONOS/components/icons/GarbageBin.svelte';
	import DatabaseExport from '$lib/IONOS/components/icons/DatabaseExport.svelte';
	import SettingInfo from './SettingInfo.svelte';
	const i18n = getContext<Readable<I18Next>>('i18n');

	let confirmChatDeletion = false;

	async function onExportChats() {
		await exportAll();
	}

	function onDeleteAllChats() {
		confirmChatDeletion = true;
	}

	async function onDeleteChatsConfirmed() {
		try {
			await deleteAll();
			toast.success($i18n.t('All chats successfully deleted.', { ns: 'ionos' }));
			confirmChatDeletion = false;
		} catch (e) {
			console.error(`Error deleting all chats:`, e);
			toast.error($i18n.t('Error deleting all chats.', { ns: 'ionos' }));
		}
	}
</script>

<div class="flex flex-col md:gap-5 text-sm">
	<div class="hidden md:flex flex-row items-center h-10  border-none">
		<div class="flex-grow">
			{$i18n.t('Export all chats', { ns: 'ionos' })}
		</div>
		<div class="hidden md:block">
			<Button
				on:click={onExportChats}
				type={ButtonType.secondary}
			>
				{$i18n.t('Export chats', { ns: 'ionos' })}
			</Button>
		</div>
	</div>

	<button class="md:hidden text-left flex flex-row h-[60px] py-5 border-b border-gray-200"
		on:click={onExportChats}
	>
		<span class="grow">{$i18n.t('Export all chats', { ns: 'ionos' })}</span>
		<div class="md:hidden block">
			<DatabaseExport />
		</div>
	</button>
	<div class="block md:hidden">
		<SettingInfo>
			{$i18n.t('When you export your chats, they’re saved in a .json file. You can open this file with any app that supports JSON format.', { ns: 'ionos' })}
		</SettingInfo>
	</div>
	<div class="hidden md:flex flex-row items-center h-[60px] md:h-10 py-5 border-b border-gray-200 md:border-none">
		<div class="flex-grow">
			{$i18n.t('Delete all chats', { ns: 'ionos' })}
		</div>
		<div class="hidden md:block">
			<Button
				on:click={onDeleteAllChats}
				type={ButtonType.caution}
			>
				{$i18n.t('Delete chats', { ns: 'ionos' })}
			</Button>
		</div>
	</div>
	<button class="md:hidden text-left flex flex-row h-[60px] py-5 border-b border-gray-200"
		on:click={onDeleteAllChats}
	>
		<span class="grow">{$i18n.t('Delete all chats', { ns: 'ionos' })}</span>
		<div class="md:hidden block">
			<GarbageBin />
		</div>
	</button>
</div>

<Confirm
	title={$i18n.t('Do you want to delete all chats?', { ns: 'ionos' })}
	show={confirmChatDeletion}
	confirmText={$i18n.t('Delete all chats', { ns: 'ionos' })}
	confirmHandler={onDeleteChatsConfirmed}
	cancelHandler={() => { confirmChatDeletion = false; }}
>
	{$i18n.t('This action can not be undone', { ns: 'ionos' })}
</Confirm>
