<script lang="ts">
	import type { Readable, Writable } from 'svelte/store';
	import type { I18Next } from '$lib/IONOS/i18next.d.ts';
	import { createEventDispatcher, getContext, onMount } from 'svelte';
	import { agents, type Agent } from '$lib/IONOS/stores/agents';
	import Button, { ButtonType } from '$lib/IONOS/components/common/Button.svelte';
	import Sparkles from '$lib/IONOS/components/icons/Sparkles.svelte';
	import ChevronUp from '$lib/components/icons/ChevronUp.svelte';
	import ChevronDown from '$lib/components/icons/ChevronDown.svelte';
	import { mobile } from '$lib/stores';

	const i18n = getContext<Readable<I18Next>>('i18n');
	const dispatch = createEventDispatcher();

	let shownAgents: Agent[] = [];
	let showAllAgents = false;
	let allAgents: Agent[] = [];

	onMount(() => {
		updateShownAgents();
	});

	$: {
		allAgents = $agents;
		updateShownAgents();
	}

	$: if ($mobile !== undefined) {
		updateShownAgents();
	}

	function updateShownAgents() {
		if (!$mobile || showAllAgents) {
			shownAgents = allAgents;
		} else {
			shownAgents = allAgents.slice(0, 4);
		}
	}

	function toggleShowMore() {
		showAllAgents = !showAllAgents;
		updateShownAgents();
	}

	function handleAgentSelect(id: string) {
		dispatch('select', id);
	}
</script>

<div class="grid lg:grid-cols-4 md:grid-cols-2 gap-6 sm:gap-6 overflow-show">
	{#each shownAgents as { id, name, subtitle, description } (id)}
		<div class="flex items-center relative z-10 p-5 pt-0 hover:z-50 focus-within:z-50 group mb-36 sm:mb-0">
			<div
				class="flex-0 w-56 bg-white text-blue-800 text-left rounded-2xl shadow-lg hover:shadow-xl focus-within:shadow-xl transition-all duration-500 relative"
				tabindex="0"
				role="button"
				aria-label="Expand {name} agent card"
				data-id={id}
				on:click={() => handleAgentSelect(id)}
				on:keydown={(e) => {
					if (e.key === 'Enter' || e.key === ' ') {
						handleAgentSelect(id);
					}
				}}
			>
				<div class="relative">
					<!-- Placeholder for fixed height -->
					<div class="h-[200px]" />
					<!-- Expandable Overlay (Absolute Positioned) -->
					<div class="absolute top-0 left-0 w-full bg-white rounded-2xl shadow-xl pointer-events-none transition-all duration-500 max-h-[200px] group-hover:max-h-fit group-hover:pointer-events-auto group-focus-within:max-h-fit group-focus-within:pointer-events-auto max-xs:max-h-fit max-xs:pointer-events-auto overflow-hidden">
						<div class="overflow-hidden h-36 rounded-t-2xl">
							<img
								class="h-full w-full object-cover"
								src={`/avatars/${id}.jpg`}
								alt="Model Avatar"
								loading="lazy"
							/>
						</div>
						<div class="px-4 pb-4">
							<h1 class="text-xs font-semibold mt-2">
								{name}
							</h1>
							<h2 class="text-xs mb-3">
								{subtitle}
							</h2>
							<div class="pt-3 transform -translate-y-4 opacity-0 transition-all duration-500 group-hover:translate-y-0 group-hover:opacity-100 group-focus-within:translate-y-0 group-focus-within:opacity-100 max-xs:translate-y-0 max-xs:opacity-100">
								<p class="text-xs text-gray-700 mb-4">
									{description}
								</p>
								<div class="text-center">
									<Button
										interactive={true}
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
					</div>
				</div>
			</div>
		</div>
	{/each}
</div>

{#if allAgents.length > 4 && $mobile}
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
