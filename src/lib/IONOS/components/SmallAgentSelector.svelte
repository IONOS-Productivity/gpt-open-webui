<script lang="ts">
	import { DropdownMenu } from 'bits-ui';
	import type { Readable } from 'svelte/store';
	import type { I18Next } from '$lib/IONOS/i18next.d.ts';
	import { getContext } from 'svelte';
	import { models, settings } from '$lib/stores';
	import { updateUserSettings } from '$lib/apis/users';
	import Button, { ButtonType } from '$lib/IONOS/components/common/Button.svelte'
	import { flyAndScale } from '$lib/utils/transitions';
	import { agents, type Agent } from '$lib/IONOS/stores/agents';
	import Checkmark from '$lib/IONOS/components/icons/Checkmark.svelte';
	import Ellipsis from '$lib/IONOS/components/icons/Ellipsis.svelte';

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
	}
	let show: boolean = false;
</script>

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
		alignOffset={-30}
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
					class="flex flex-row justify-between content-center w-[160px] h-full py-2 px-3 rounded cursor-pointer {id == selectedModels[0] ? 'text-purple-700' : 'text-blue-800'}  hover:bg-gray-50 dark:hover:bg-gray-800"
					aria-pressed={id === selectedModels[0]}
					role="button"
				>
					<div class="text-start text-xs" title="{name} - {subtitle}">
						<p>
							{name}
						</p>
						<p class="font-normal truncate w-[120px]">
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
