<script lang="ts">
	import { DropdownMenu } from 'bits-ui';
	import type { Readable } from 'svelte/store';
	import type { I18Next } from '$lib/IONOS/i18next.d.ts';
	import { getContext } from 'svelte';
	import { settings, mobile } from '$lib/stores';
	import { updateUserSettings } from '$lib/apis/users';
	import Button, { ButtonType } from '$lib/IONOS/components/common/Button.svelte'
	import { flyAndScale } from '$lib/utils/transitions';
	import { agents } from '$lib/IONOS/stores/agents';
	import Checkmark from '$lib/IONOS/components/icons/Checkmark.svelte';
	import Ellipsis from '$lib/IONOS/components/icons/Ellipsis.svelte';
	import Dialog from '$lib/IONOS/components/common/Dialog.svelte';
	import DialogHeader from '$lib/IONOS/components/common/DialogHeader.svelte';

	const i18n = getContext<Readable<I18Next>>('i18n');

	export let selectedModels = [''];
	export let anchorElement: HTMLElement | null = null;

	// Custom models obey have the convention of using only characters
	// This excludes stock models.
	// This can later be changed to testing for a marker tag in info.meta.tags
	const onlyCustomModels = ({ id }: { id: string }) => /^[a-z]+$/.test(id);

	const save = async () => {
		settings.set({ ...$settings, models: selectedModels });
		await updateUserSettings(localStorage.token, { ui: $settings });
	}

	const select = (id: string) => {
		selectedModels = [id];
		save();
		show = false;
	}
	export let show: boolean = false;

	$: console.log('show', show);
</script>

{#if !$mobile}
<DropdownMenu.Root
	bind:open={show}
>
	<DropdownMenu.Trigger>
		<Button
			className="flex flex-row items-center gap-1"
			type={ButtonType.secondary}
			pressable={true}
		>
			<span class="ml-1 text-nowrap">
				{$agents.length > 0 ? $agents.find((a) => a.id === selectedModels[0])?.name || $agents[0]?.name : $i18n.t('Select a specialist', { ns: 'ionos' })}
			</span>
			<Ellipsis />
		</Button>
	</DropdownMenu.Trigger>
	<DropdownMenu.Content
		class="rounded-2xl px-5 py-6 text-blue-800 text-xs font-semibold border-gray-300/30 dark:border-gray-700/50 z-50 bg-white dark:bg-gray-850 dark:text-white shadow-xl max-w-[750px]"
		side='bottom'
		sideOffset={15}
		align='start'
		alignOffset={-50}
		transition={flyAndScale}
	>
		<p class="font-semibold text-gray-500 pb-4 px-3">
			{$i18n.t('Select a specialist', { ns: 'ionos' })}
		</p>
		<div class="flex flex-col md:flex-row md:flex-wrap justify-between align-center items-stretch gap-2.5">
		{#each $agents as { id, name, subtitle }}
			<DropdownMenu.Item>
				<div
					on:click={() => select(id)}
					class="flex flex-row justify-between content-center w-[160px] h-[80px] py-2 px-3 rounded-sm cursor-pointer {id == selectedModels[0] ? 'text-purple-700' : 'text-blue-800'}  hover:bg-gray-50 dark:hover:bg-gray-800"
					aria-pressed={id === selectedModels[0]}
					role="button"
				>
					<div class="text-start text-xs" title="{name} - {subtitle}">
						<p>
							{name}
						</p>
						<p class="font-normal text-wrap truncate w-[120px]">
							{subtitle}
						</p>
					</div>
					{#if id === selectedModels[0]}
						<Checkmark className="self-center" />
					{/if}
				</div>
			</DropdownMenu.Item>
		{/each}
		</div>
	</DropdownMenu.Content>
</DropdownMenu.Root>
{:else}

<Button
	className="flex flex-row items-center gap-1"
	type={ButtonType.secondary}
	pressable={true}
	on:click
>
	<span class="ml-1 text-nowrap">
		{$agents.length > 0 ? $agents.find((a) => a.id === selectedModels[0])?.name || $agents[0]?.name : $i18n.t('Select a specialist', { ns: 'ionos' })}
	</span>
	<Ellipsis />
</Button>
<Dialog
	dialogId="small-agent-selector"
	{show}
	mobileCover={false}
	class="p-0 md:min-h-[400px] md:min-w-[750px] md:max-w-[750px] {show ? 'max-md:translate-y-[0]' : 'max-md:translate-y-[100dvh]'}"
	on:close
>
	<DialogHeader
		slot="header"
		title={$i18n.t('Select a specialist', { ns: 'ionos' })}
		dialogId="settings"
		class="p-[30px] text-left border-b border-gray-200"
		closable={false}
	/>

	<div class="relative" slot="content">
		<div class="flex flex-col md:flex-row md:flex-wrap justify-between align-center items-stretch max-h-[375px] max-md:w-[353px] overflow-y-scroll divide-y divide-gray-200">
			{#each $agents as { id, name, subtitle }}
					<div
						on:click={() => select(id)}
						class="flex flex-row justify-between content-center h-[80px] py-5 px-[30px] rounded-sm cursor-pointer {id == selectedModels[0] ? 'text-purple-700' : 'text-blue-800'}  hover:bg-gray-50 dark:hover:bg-gray-800"
						aria-pressed={id === selectedModels[0]}
						role="button"
					>
						<div class="font-semibold text-start text-xs grow" title="{name} - {subtitle}">
							<p>
								{name}
							</p>
							<p class="font-normal text-wrap truncate">
								{subtitle}
							</p>
						</div>
						{#if id === selectedModels[0]}
							<Checkmark className="self-center" />
						{/if}
					</div>
			{/each}
		</div>
		<div class="absolute bottom-0 left-0 right-0 h-[70px] bg-gradient-to-t from-white to-transparent pointer-events-none rounded-b-2xl" />
	</div>
</Dialog>
{/if}
