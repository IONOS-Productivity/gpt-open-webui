<script lang="ts">
	import { showSidebar } from '$lib/stores';
	import Bars from '$lib/IONOS/components/icons/Bars.svelte';

</script>
<button
	class=" cursor-pointer p-2.5 flex rounded-xl hover:bg-gray-100 dark:hover:bg-gray-900 transition"
	on:click={() => {
		showSidebar.set(!$showSidebar);
	}}
>
	<div class=" m-auto self-center text-blue-800">
		<Bars />
	</div>
</button>
