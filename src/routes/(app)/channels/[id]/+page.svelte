<script lang="ts">
	import { page } from '$app/stores';

	import Channel from '$lib/components/channel/Channel.svelte';
	import Sidebar from '$lib/components/layout/Sidebar.svelte';

	let chat: Chat|null = null;
</script>

<Sidebar on:new-chat={chat.newChat()} />
<Channel bind:this={chat} id={$page.params.id} />
