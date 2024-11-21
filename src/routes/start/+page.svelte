<script lang="ts">

/**
 * Landing page for IONOS GPT public demo.
 *
 * This page should be served as a resource from /start.
 *
 * The user should be redirected to this page if they do not have an
 * internal session yet.
 *
 * The user would then load a new resource as part of the Open WebUI SPA so
 * that a transparent sign-in mechanism can run.
 *
 * The router should avoid loading Open WebUI API resources like
 * authentication and Websockets.
 */

import { getContext } from 'svelte';
import { config } from '$lib/stores';

import Greeting from '$lib/components/chat/Greeting.svelte';
import Suggestions from '$lib/components/chat/Suggestions.svelte';
import PaperPlane from '$lib/components/icons/PaperPlane.svelte';
import Textarea from '$lib/components/common/Textarea.svelte';
import Trailer from '$lib/IONOS/components/Trailer.svelte';

const i18n = getContext('i18n');

// TODO hardcoded during early development, has to be provided by a
// suggested prompts + model config
const model = 'meta-llama/CodeLlama-13b-Instruct-hf';

let prompt = '';

function submit(promptToStart: string, modelNameForStart: string) {
	window.location = `/?q=${promptToStart}&models=${modelNameForStart}`
}
</script>

<div class="overflow-auto w-full h-full flex flex-col items-center">
	<Greeting />

	<form
		on:submit|preventDefault={(e) => submit(prompt, model)}
		class="flex items-center min-w-96 h-fit my-4 border rounded-xl"
		>

		<Textarea
			bind:value={prompt}
			placeholder={$i18n.t('Send a message to IONOS GPT', { ns: "ionos" })}
			className="w-full rounded-lg p-3 text-sm dark:text-gray-300 dark:bg-gray-850 outline-none resize-none h-full bg-transparent"
		/>

		<button type="submit" class="p-0 mx-2 flex w-8">
			<PaperPlane className="fill-gray-400 cursor-pointer hover:fill-ionos" />
		</button>
	</form>

	<div class="mx-5">
		<Suggestions
			suggestionPrompts={$config?.default_prompt_suggestions ?? []}
			on:select={(e) => submit(e.detail, model)}
		/>
	</div>

	<Trailer />
</div>
