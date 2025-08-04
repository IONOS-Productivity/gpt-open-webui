<script lang="ts">
	import CircleInfo from '$lib/IONOS/components/icons/CircleInfo.svelte';
</script>

<div class="flex flex-row gap-2.5 text-xs py-5 text-gray-400 border-b border-gray-200">
	<div class="flex-1 my-auto">
		<CircleInfo />
	</div>
	<slot />
</div>
