<script lang="ts">
	import { getContext, onMount } from 'svelte';
	import AgentSelector from '$lib/IONOS/components/AgentSelector.svelte'
	import PromptSelector from '$lib/IONOS/components/PromptSelector.svelte'
	import Robot from '$lib/components/icons/Robot.svelte'
	import ChevronDown from '$lib/components/icons/ChevronDown.svelte'
	import { init as initAgentsStore } from '$lib/IONOS/stores/agents';
	import { init as initPromptsStore } from '$lib/IONOS/stores/prompts';

	const i18n = getContext('i18n');

	onMount(async () => {
		await initAgentsStore();
		await initPromptsStore();
	});
</script>

<div class="animated-masked-background"></div>
<div class="animated-masked-background config-2"></div>

<content class="flex flex-col items-center pt-20 mx-3">
	<div class="animated-masked-text">
		<h1 class="my-5 text-3xl text-center text-pink-300 text-transparent">
			{$i18n.t('Welcome to IONOS GPT,', { ns: 'ionos' })}
			<br>
			{$i18n.t('Where AI becomes your ultimate team of experts!', { ns: 'ionos' })}
		</h1>
	</div>

	<p class="max-w-3xl mb-4 text-sm text-center">
		{$i18n.t('From ideas to execution, our virtual team is here to help — from writing and design to coding, they handle the details so you can focus on what matters. Get to know them and see how they can support your projects.', { ns: 'ionos' })}
	</p>

	<div class="flex flex-col items-center">
		<span>{$i18n.t('Select a specialist', { ns: 'ionos' })}</span>
		<span>
			<ChevronDown />
		</span>
	</div>

	<div class="block py-5 my-16">
		<AgentSelector />
	</div>

	<h1 class="my-4 text-xl text-center">
		{$i18n.t('Bringing your ideas to life is easy with our AI specialists', { ns: 'ionos' })}
	</h1>

	<p class="max-w-2xl text-sm text-center">
		{$i18n.t('Whether you need great content, eye-catching designs, or clean code, your virtual team is here to help every step of the way.', { ns: 'ionos' })}
	</p>

	<div class="block w-full py-5 my-8">
		<PromptSelector />
	</div>

	<div class="my-20">
		<Robot />
	</div>

	<p class="max-w-2xl my-5 text-sm text-center">
		{$i18n.t('By sending messages to IONOS GPT, you agree to our terms and conditions and confirm that you\'ve read our privacy policy.', { ns: 'ionos' })}
	</p>
</content>

<style>
	@property --pos-x {
		syntax: '<percentage>';
		inherits: false;
		initial-value: 0%;
	}

	@property --pos-y {
		syntax: '<percentage>';
		inherits: false;
		initial-value: 0%;
	}

	@property --rotation {
		syntax: "<angle>";
		inherits: false;
		initial-value: 90deg;
	}


	@property --color-1 {
		syntax: '<color>';
		inherits: false;
		initial-value: rgba(255, 255, 255, 0);
	}

	@property --color-2 {
		syntax: '<color>';
		inherits: false;
		initial-value: rgba(255, 255, 255, 0);
	}

	@property --color-3 {
		syntax: '<color>';
		inherits: false;
		initial-value: rgba(255, 255, 255, 0);
	}

	@property --color-4 {
		syntax: '<color>';
		inherits: false;
		initial-value: rgba(255, 255, 255, 0);
	}

	@property --color-5 {
		syntax: '<color>';
		inherits: false;
		initial-value: rgba(255, 255, 255, 0);
	}

	@property --background-size {
		syntax: '<percentage>';
		inherits: false;
		initial-value: 0;
	}

	.text-transparent {
		color: transparent;
	}

	.animated-masked-text {
		--pos-x: 50%;
		--pos-y: 10%;

		--color-1: hsl(238.71deg 46.67% 70.18%);
		--color-2: hsl(281.35deg 31.97% 52.78%);
		--color-3: hsl(311.26deg 100% 34.33%);
		--color-4: hsl(265.71deg 32.07% 61.05%);
		--color-5: hsl(222.68deg 59.99% 36.91%);

		--rotation: 90deg;

		width: fit-content;
		margin: 0 auto;

		color: transparent;

		background-image: linear-gradient(var(--rotation), var(--color-1), var(--color-2), var(--color-3), var(--color-4), var(--color-5));
		background-repeat: no-repeat;
		background-size: 100% 500%;

		mask-image: url(data:image/svg+xml;base64,PHN2ZwogICB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciCiAgIHhtbG5zOnhsaW5rPSAiaHR0cDovL3d3dy53My5vcmcvMTk5OS94bGluayIKICAgd2lkdGg9IjgwMCIKICAgaGVpZ2h0PSI3MCIKICAgdmlld0JveD0iMCAwIDgwMCA3MCI+CiAgPGcgc3R5bGU9ImZvbnQtZmFtaWx5OiBzYW5zOyBmb250LXNpemU6MzJweDsgbGluZS1oZWlnaHQ6MS4yNTsiPgogICAgPHRleHQgeD0iNDAwIiB5PSIzNSIgc3R5bGU9InRleHQtYWxpZ246Y2VudGVyO3RleHQtYW5jaG9yOm1pZGRsZSI+V2VsY29tZSB0byBJT05PUyBHUFQsPC90ZXh0PgogICAgPHRleHQgeD0iNDAwIiB5PSI2NSIgc3R5bGU9InRleHQtYWxpZ246Y2VudGVyO3RleHQtYW5jaG9yOm1pZGRsZSI+V2hlcmUgQUkgYmVjb21lcyB5b3VyIHVsdGltYXRlIHRlYW0gb2YgZXhwZXJ0cyE8L3RleHQ+CiAgPC9nPgo8L3N2Zz4K);

		mask-composite: add;
		mask-repeat: no-repeat;
		mask-size: 100% 100%;
		mask-mode: alpha;
		/*
		*/

		animation: change-shape 20s linear infinite, linear change-gradient 5s infinite;
		/*
		*/

		transition-property: --pos-x, --pos-y, --rotation;

		transition-duration: 2s;
		transition-timing-function: ease-in-out;
	}

	@keyframes change-shape {
		0% {
			background-size: 100% 100%;
			--rotation: 0deg;
		}
		10% {
			background-size: 110% 100%;
			--rotation: 90deg;
		}
		20% {
			background-size: 120% 100%;
			--rotation: 180deg;
		}
		30% {
			background-size: 130% 100%;
			--rotation: 270deg;
		}
		40% {
			background-size: 140% 100%;
			--rotation: 180deg;
		}
		50% {
			background-size: 150% 100%;
			--rotation: 90deg;
		}
		60% {
			background-size: 140% 100%;
			--rotation: 0deg;
		}
		70% {
			background-size: 130% 100%;
			--rotation: 90deg;
		}
		80% {
			background-size: 120% 100%;
			--rotation: 180deg;
		}
		90% {
			background-size: 110% 100%;
			--rotation: 90deg;
		}
		100% {
			background-size: 100% 100%;
			--rotation: 00deg;
		}
	}

	@keyframes change-gradient {
		0% {
			--color-1: hsl(238.71deg 46.67% 70.18%);
			--color-2: hsl(281.35deg 31.97% 52.78%);
			--color-3: hsl(311.26deg 100% 34.33%);
			--color-4: hsl(265.71deg 32.07% 61.05%);
			--color-5: hsl(222.68deg 59.99% 36.91%);
		}
		25% {
			--color-1: hsl(238.71deg 46.67% 70.18%);
			--color-2: hsl(281.35deg 31.97% 52.78%);
			--color-3: hsl(311.26deg 100% 34.33%);
			--color-4: hsl(265.71deg 32.07% 61.05%);
			--color-5: hsl(222.68deg 59.99% 36.91%);
		}
		50% {
			--color-1: hsl(238.71deg 46.67% 70.18%);
			--color-2: hsl(281.35deg 31.97% 52.78%);
			--color-3: hsl(311.26deg 100% 34.33%);
			--color-4: hsl(265.71deg 32.07% 61.05%);
			--color-5: hsl(222.68deg 59.99% 36.91%);
		}
		75% {
			--color-1: hsl(238.71deg 46.67% 70.18%);
			--color-2: hsl(281.35deg 31.97% 52.78%);
			--color-3: hsl(311.26deg 100% 34.33%);
			--color-4: hsl(265.71deg 32.07% 61.05%);
			--color-5: hsl(222.68deg 59.99% 36.91%);
		}
		100% {
			--color-1: hsl(238.71deg 46.67% 70.18%);
			--color-2: hsl(281.35deg 31.97% 52.78%);
			--color-3: hsl(311.26deg 100% 34.33%);
			--color-4: hsl(265.71deg 32.07% 61.05%);
			--color-5: hsl(222.68deg 59.99% 36.91%);
		}
	}


	@property --blob-color-1 {
		syntax: '<color>';
		inherits: false;
		initial-value: rgba(255, 255, 255, 0);
	}

	@property --blob-color-2 {
		syntax: '<color>';
		inherits: false;
		initial-value: rgba(255, 255, 255, 0);
	}

	@property --blob-color-3 {
		syntax: '<color>';
		inherits: false;
		initial-value: rgba(255, 255, 255, 0);
	}

	@property --blob-color-4 {
		syntax: '<color>';
		inherits: false;
		initial-value: rgba(255, 255, 255, 0);
	}

	/* Inspired by https://codepen.io/wilvander/pen/KKQrGgP */
	.animated-masked-background {
		--blob-offset-x: 5vw;
		--blob-offset-y: 5vh;
		--blob-rotation-offset: 90deg;
		--speed: 50s;

		--blob-color-1: hsla(311.26deg 100% 34.33% / 20%);
		--blob-color-2: hsla(222.68deg 59.99% 36.91% / 20%);
		--blob-color-3: hsla(186deg 60% 37% / 20%);
		--blob-color-4: hsla(0deg 100% 100% / 100%);

		--size: 500px;
		--easing: cubic-bezier(0.8, 0.2, 0.2, 0.8);

		user-select: none;
		position: fixed;
		top: var(--blob-offset-y);
		right: var(--blob-offset-x);
		width: 400px;
		height: 400px;
		z-index: -1;


		background-image: linear-gradient(var(--blob-color-4), var(--blob-color-1), var(--blob-color-2), var(--blob-color-3), var(--blob-color-4));

		animation: rotate var(--speed) var(--easing) alternate infinite;

		filter: blur(calc(var(--size) / 8));
		/*
		*/
		border-radius: 10% 60% 90% 10% / 10% 20% 90% 90%;

		transition: all 0.5s ease-out;
	}

	.config-2 {
		--blob-offset-x: -5vw;
		--blob-offset-y: 50vh;
		--blob-rotation-offset: 150deg;
		--speed: 65s;
	}

	@keyframes rotate {
		0% {
			transform: rotate(calc(0deg + var(--blob-rotation-offset)));
		}
		100% {
			transform: rotate(calc(360deg + var(--blob-rotation-offset)));
		}
	}
</style>
