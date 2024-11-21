<svelte:head>
	<title>
		IONOS GPT
	</title>
</svelte:head>

<content class="flex flex-col">
	<slot />
</content>

<style>
content {
	display: block;
	display: flex;
	flex-direction: column;
	margin-top: 68px;
	height: calc(100vh - 2 * 68px);
}
</style>
