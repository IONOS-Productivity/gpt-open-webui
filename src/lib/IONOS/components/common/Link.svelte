<script lang="ts">
	export let href: string = '';
</script>

<a
	{...$$restProps}
	{href}
	class="text-blue-700 hover:text-blue-500 active:text-blue-300 hover:underline"
	target="_blank"
	rel="noreferrer"
>
	<slot />
</a>
