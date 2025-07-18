<script lang="ts">
	import type { Readable, Writable } from 'svelte/store';
	import type { I18Next } from '$lib/IONOS/i18next.d.ts';
	import { createEventDispatcher, getContext } from 'svelte';
	import { agents, type Agent } from '$lib/IONOS/stores/agents';
	import Button, { ButtonType } from '$lib/IONOS/components/common/Button.svelte';
	import Sparkles from '$lib/IONOS/components/icons/Sparkles.svelte';

	const i18n = getContext<Readable<I18Next>>('i18n');
	const dispatch = createEventDispatcher();

	let shownAgents: Agent[]

	agents.subscribe((allAgents: Writable<Agent[]>) => {
		const shuffled = allAgents.sort(() => 0.5 - Math.random());
		shownAgents = shuffled.slice(0, 4);
	});
</script>

<div class="flex flex-row gap-4 items-center justify-center flex-wrap">
	{#each shownAgents as { id, name, subtitle, description }}
		<div class="min-h-96 flex items-center">
			<button
				class="flex-0 group w-56 hover:pb-0 duration-[500ms] transition-[padding] pb-4 mx-6 bg-white text-blue-800 text-left rounded-2xl shadow-xl transition group cursor-pointer"
				data-id={id}
				on:click={() => dispatch('select', id)}
			>
				<div class="overflow-hidden transition-[width,height] duration-[500ms] h-36 rounded-t-2xl">
					<img
						class="h-full w-full object-cover rounded-2xl rounded-b-none"
						src={`/avatars/${id}.jpg`}
						alt="Model Avatar"
					/>
				</div>
				<div class="px-4 overflow-hidden">
					<h1 class="text-xs font-semibold mt-2">
						{name}
					</h1>
					<h2 class="text-xs">
						{subtitle}
					</h2>
					<div class="flex flex-col justify-between mt-0 overflow-hidden duration-[500ms] transition-[height,margin-top] h-0 group-hover:h-40 group-hover:mt-4 group-focus:h-40 group-focus:mt-4 focus-within:h-40 focus-within:mt-4 max-xs:h-40 max-xs:mt-4 max-xs:h-40 max-xs:mt-4">
						<p class="text-xs">
							{description}
						</p>
						<div class="mb-4 text-center">
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
