<script lang="ts">
	import type { Readable, Writable } from 'svelte/store';
	import type { I18Next } from '$lib/IONOS/i18next.d.ts';
	import { createEventDispatcher, getContext } from 'svelte';
	import { agents, type Agent } from '$lib/IONOS/stores/agents';
	import Button, { ButtonType } from '$lib/IONOS/components/common/Button.svelte';
	import Sparkles from '$lib/IONOS/components/icons/Sparkles.svelte';
	import ChevronUp from '$lib/components/icons/ChevronUp.svelte';
	import ChevronDown from '$lib/components/icons/ChevronDown.svelte';

	const i18n = getContext<Readable<I18Next>>('i18n');
	const dispatch = createEventDispatcher();

	let shownAgents: Agent[] = [];
	let showAllAgents = false;
	let allAgents: Agent[] = [];
	let isSmallScreen = false;

	// Check if screen is small
	function checkScreenSize() {
		isSmallScreen = window.innerWidth < 640; // sm breakpoint is 640px
		updateShownAgents();
	}

	// Initialize screen size check
	if (typeof window !== 'undefined') {
		checkScreenSize();
		window.addEventListener('resize', checkScreenSize);
	}

	agents.subscribe((agentsList: Agent[]) => {
		allAgents = [...agentsList];
		updateShownAgents();
	});

	function updateShownAgents() {
		if (!isSmallScreen || showAllAgents) {
			shownAgents = allAgents;
		} else {
			shownAgents = allAgents.slice(0, 4);
		}
	}

	function toggleShowMore() {
		showAllAgents = !showAllAgents;
		updateShownAgents();
	}
</script>

<div class="grid py-12 lg:grid-cols-4 md:grid-cols-2 gap-4 gap-y-[20px] max-xs:gap-y-[50px] max-xs:py-0">
	{#each shownAgents as { id, name, subtitle, description }}
		<div class="h-[280px] max-xs:h-[380px] flex items-center">
			<button
				class="group w-56 duration-[500ms] pb-4 mx-6 bg-white text-blue-800 text-left rounded-2xl shadow-xl group cursor-pointer"
				data-id={id}
				on:click={() => dispatch('select', id)}
			>
				<div class="overflow-hidden h-36 rounded-t-2xl">
					<img
						class="h-full w-full object-cover rounded-2xl rounded-b-none"
						src={`/avatars/${id}.jpg`}
						alt="Model Avatar"
					/>
				</div>
				<div class="px-4 overflow-hidden">
					<h1 class="text-xs/normal font-semibold mt-2">
						{name}
					</h1>
					<h2 class="text-xs/normal">
						{subtitle}
					</h2>
					<div class="flex flex-col justify-between mt-0 overflow-hidden duration-[500ms] transition-[height,margin-top] h-0 group-hover:h-[145px] group-hover:mt-4 group-focus:h-[145px] group-focus:mt-4 focus-within:h-[145px] focus-within:mt-4 max-xs:h-[145px] max-xs:mt-4 max-xs:h-[145px] max-xs:mt-4">
						<p class="text-xs">
							{description}
						</p>
						<div class="text-center">
							<Button
								interactive={false}
								name={id}
								className="px-4 py-1"
								type={ButtonType.special}
							>
								<span class="pr-1 text-sm font-semibold">
									{$i18n.t('Chat now', { ns: 'ionos' })}
								</span>
								<Sparkles className="w-4 h-4 inline text-purple-300" />
							</Button>
						</div>
					</div>
				</div>
			</button>
		</div>
	{/each}
</div>

{#if allAgents.length > 4 && isSmallScreen}
	<div class="flex justify-center mt-6">
		<button
			class="flex items-center gap-1 text-blue-600 hover:text-blue-800 font-medium text-sm transition-colors duration-200"
			on:click={toggleShowMore}
		>
			{showAllAgents
				? $i18n.t('Show less', { ns: 'ionos' })
				: $i18n.t('Show more', { ns: 'ionos' })
			}
			{#if showAllAgents}
				<ChevronUp className="size-4" />
			{:else}
				<ChevronDown className="size-4" />
			{/if}
		</button>
	</div>
{/if}
