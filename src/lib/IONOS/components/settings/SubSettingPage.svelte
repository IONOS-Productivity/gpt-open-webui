<script lang="ts">
	import Dialog from '$lib/IONOS/components/common/Dialog.svelte';

	export let show: boolean = false;
</script>

<Dialog
	dialogId="subsetting-dialog"
	class="p-0 md:min-h-[400px] h-screen w-screen md:max-h-fit md:min-w-[750px] md:max-w-[750px] overflow-y-scroll {show ? 'max-md:translate-x-0' : 'max-md:translate-x-[100dvw]'}"
	bind:show
>
	<div slot="header">
		<slot name="header" />
	</div>
	<div slot="content">
		<slot name="content" />
	</div>
</Dialog>
