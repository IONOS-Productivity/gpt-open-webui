<script lang="ts">
	import { getContext, onMount } from 'svelte';
	import AnimatedBackground from '$lib/IONOS/components/explore/AnimatedBackground.svelte'
	import AgentSelector from '$lib/IONOS/components/explore/AgentSelector.svelte'
	import PromptSelector from '$lib/IONOS/components/explore/PromptSelector.svelte'
	import LoginRegisterOverlay from '$lib/IONOS/components/explore/LoginRegisterOverlay.svelte';
	import Robot from '$lib/components/icons/Robot.svelte'
	import ChevronDown from '$lib/components/icons/ChevronDown.svelte'
	import Sparkles from '$lib/IONOS/components/icons/Sparkles.svelte';
	import { user } from '$lib/stores';
	import { goto } from '$app/navigation';
	import { init as initAgentsStore } from '$lib/IONOS/stores/agents';
	import { init as initPromptsStore } from '$lib/IONOS/stores/prompts';
	import { selectAgent } from '$lib/IONOS/services/agent';
	import { selectPrompt } from '$lib/IONOS/services/prompt';
	import { signup } from '$lib/IONOS/services/signup';
	import Confirm from '$lib/IONOS/components/common/Confirm.svelte';

	const i18n = getContext('i18n');

	let selectedAgent: string|null = null;
	let selectedPrompt: number|null = null;

	$: showLoginDialog = selectedAgent !== null || selectedPrompt !== null;

	function selectAgentInternal(agentId: string) {
		if (!$user) {
			selectedAgent = agentId;
			return;
		}

		selectAgent(agentId);
	}

	function selectPromptInternal(promptId: number) {
		if (!$user) {
			selectedPrompt = promptId;
			return;
		}

		selectPrompt(promptId);
	}

	function login() {
		if (selectedAgent !== null) {
			console.log('Continue with selected agent', selectedAgent);
			selectAgent(selectedAgent);
		} else if (selectedPrompt !== null) {
			console.log('Continue with selected prompt', selectedPrompt);
			selectPrompt(selectedPrompt);
		}
	}

	onMount(async () => {
		await initAgentsStore();
		await initPromptsStore();
	});
</script>

<svelte:head>
	<title>{$i18n.t('Welcome to IONOS GPT,', { ns: 'ionos' })} {$i18n.t('Where AI becomes your ultimate team of experts!', { ns: 'ionos' })}</title>
</svelte:head>

<Confirm
	title={$i18n.t('Delete knowledge base?', { ns: 'ionos' })}
	show={showLoginDialog}
	confirmText={$i18n.t('Delete knowledge base', { ns: 'ionos' })}
	confirmHandler={() => { showLoginDialog = false; }}
	cancelHandler={() => { showLoginDialog = false; }}
>
	fooo bar 1
</Confirm>

<p>start</p>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<button on:click={() => { showLoginDialog = true; }} >open</button>
<p>end</p>



<style>
	:global(body) {
		background-color: #f9f9f9;
	}
</style>
