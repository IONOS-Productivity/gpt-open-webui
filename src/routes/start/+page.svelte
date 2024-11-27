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
import Suggestions from '$lib/IONOS/components/Suggestions.svelte';
import PaperPlane from '$lib/components/icons/PaperPlane.svelte';
import Textarea from '$lib/components/common/Textarea.svelte';
import Trailer from '$lib/IONOS/components/Trailer.svelte';

const i18n = getContext('i18n');

// If the user did not pick a default model
const defaultModel = 'meta-llama/Meta-Llama-3.1-8B-Instruct';

let prompt = '';
let model = defaultModel;

let promptTextarea;

function submit(promptToStart: string, modelNameForStart: string) {
	// Pass prompt and model securely via sessionStorage and start chat by
	// *hard* page load, deliberately circumventing the push state API
	sessionStorage.selectedModels = JSON.stringify([modelNameForStart]);
	sessionStorage.ionosGptDemoPrompt = promptToStart;

	window.location = `/auth`;
}

function selectSuggestion({ detail: { prompt: selectedPrompt, model: selectedModel } }) {
	prompt = selectedPrompt;
	model = selectedModel;
	promptTextarea.focus();
}
</script>

<div class="overflow-auto w-full h-full flex flex-col items-center">
	<Greeting />

	<div class="w-3/5 py-5">
		<Suggestions
			on:select={selectSuggestion}
		/>
	</div>

	<p>{$i18n.t('Using {{model}}', { ns: "ionos", model })}</p>

	<form
		on:submit|preventDefault={(e) => submit(prompt, model)}
		class="flex items-center min-w-96 h-fit my-4 border rounded-xl"
		>

		<Textarea
			bind:this={promptTextarea}
			bind:value={prompt}
			placeholder={$i18n.t('Send a message to IONOS GPT', { ns: "ionos" })}
			className="w-full rounded-lg p-3 text-sm dark:text-gray-300 dark:bg-gray-850 outline-none resize-none h-full bg-transparent"
		/>


		<button type="submit" class="p-0 mx-2 flex w-8">
			<PaperPlane className="fill-gray-400 cursor-pointer hover:fill-ionos" />
		</button>
	</form>


	<Trailer />
</div>
