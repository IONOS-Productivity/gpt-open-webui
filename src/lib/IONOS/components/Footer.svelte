<script lang="ts">
	import type { Readable } from 'svelte/store';
	import type { I18Next } from '$lib/IONOS/i18next.d.ts';
	import { getContext } from 'svelte';
	import Link from '$lib/IONOS/components/common/Link.svelte';
	import { URLS } from '$lib/IONOS/urls';

	const i18n = getContext<Readable<I18Next>>('i18n');
</script>

<div class="flex flex-row justify-between px-4 py-1 gap-4 text-sm max-lg:flex-col bg-gray-50">
	<div class="flex-1">
	</div>
	<div class="flex-1 flex flex-row justify-center">
		{$i18n.t('© 2025 IONOS SE', { ns: 'ionos' })}
	</div>
	<div class="flex-1 flex flex-row justify-end gap-3 max-lg:justify-center">
		<Link href={URLS.imprint}>
			{$i18n.t('Imprint', { ns: 'ionos' })}
		</Link>
		<Link href={URLS.privacy}>
			{$i18n.t('Privacy', { ns: 'ionos' })}
		</Link>
		<Link href={URLS.terms}>
			{$i18n.t('Terms and conditions', { ns: 'ionos' })}
		</Link>
	</div>
</div>
