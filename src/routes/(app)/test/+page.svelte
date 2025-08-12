<script>
	import { getContext } from 'svelte';

	const i18n = getContext('i18n');

	import Confirm from '$lib/IONOS/components/common/Confirm.svelte';
	let show = false;
</script>

<Confirm
	title={$i18n.t('Delete knowledge base?', { ns: 'ionos' })}
	show={show}
	confirmText="lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum"
	confirmHandler={() => { show = false; }}
	cancelHandler={() => { show = false; }}
>
	fooo bar 1
</Confirm>

<button on:click={() => { show = true; }}>show</button>

<p class="block">foo</p>
<p class="block">foo</p>
<p class="block">foo</p>
<p class="block">foo</p>
<p class="block">foo</p>
<p class="block">foo</p>
<p class="block">foo</p>
<p class="block">foo</p>
<p class="block">foo</p>
<p class="block">foo</p>
<p class="block">foo</p>
<p class="block">foo</p>
<p class="block">foo</p>
<p class="block">foo</p>
<p class="block">foo</p>
<p class="block">foo</p>
<p class="block">foo</p>
<p class="block">foo</p>
<p class="block">foo</p>
<p class="block">foo</p>
<p class="block">foo</p>
<p class="block">foo</p>
<p class="block">foo</p>
<p class="block">foo</p>
