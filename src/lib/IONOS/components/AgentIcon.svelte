<script lang="ts">
	import Pencil from '$lib/components/icons/Pencil.svelte';
	import PhotoSolid from '$lib/components/icons/PhotoSolid.svelte';
	import Heart from '$lib/components/icons/Heart.svelte';
	import ChatBubbleOval from '$lib/components/icons/ChatBubbleOval.svelte';

	export let iconName = '';
</script>

{#if iconName == 'talk'}
	<ChatBubbleOval className="inline-block size-4" />
{:else if iconName == 'code'}
	<Heart className="inline-block size-4" />
{:else if iconName == 'image'}
	<PhotoSolid className="inline-block size-4" />
{:else if iconName == 'pencil'}
	<Pencil className="inline-block size-4" />
{:else}
	<Pencil className="inline-block size-4" />
{/if}
