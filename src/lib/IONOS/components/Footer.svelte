<script lang="ts">
	import type { Readable } from 'svelte/store';
	import type { I18Next } from '$lib/IONOS/i18next.d.ts';
	import { getContext } from 'svelte';
	import TermsMenu from './TermsMenu.svelte';

	const i18n = getContext<Readable<I18Next>>('i18n');
	let showTerms: boolean = false;
</script>

<div class="flex md:flex-row flex-col justify-center mx-auto mb-7 max-w-2xl text-gray-400 text-xs gap-[3px] text-center">
	<p>
		{$i18n.t('IONOS GPT can make mistakes.', { ns: 'ionos' })}
	</p>
	<TermsMenu
		show={showTerms}
		className="text-blue-700"
	>
		<div class="font-semibold underline">
			{$i18n.t('Check important info.', { ns: 'ionos' })}
		</div>
	</TermsMenu>
</div>
