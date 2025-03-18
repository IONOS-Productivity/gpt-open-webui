<!-- Extracted from Open WebUI's MessageInput.svelte -->

<script lang="ts">
	import type { Readable } from 'svelte/store';
	import type { I18Next } from '$lib/IONOS/i18next.d.ts';
	import { tick, getContext, createEventDispatcher } from 'svelte';
	import { PASTED_TEXT_CHARACTER_LIMIT } from '$lib/constants';
	import { findWordIndices } from '$lib/utils';
	import {
		mobile,
		settings,
	} from '$lib/stores';

	const i18n = getContext<Readable<I18Next>>('i18n');
	const dispatch = createEventDispatcher();

	export let prompt = '';
	export let placeholder = '';
	export let stopResponse: () => void = () => { };
	export let uploadFileHandler: (file: File, fullContext: boolean) => void = () => { };
	export let createMessagePair: (prompt: string) => void = () => { };
	export let files: File[] = [];

	export function focus(): void {
		chatInputElement?.focus();
	}

	let chatInputElement: HTMLElement|null = null;
</script>

<textarea
	id="chat-input"
	bind:this={chatInputElement}
	class="scrollbar-hidden bg-transparent dark:text-gray-100 outline-none w-full py-3 px-1 rounded-xl resize-none h-[48px]"
	placeholder={placeholder ? placeholder : $i18n.t('Send a Message')}
	bind:value={prompt}
	on:keypress={(e) => {
		if (
			!$mobile ||
			!(
				'ontouchstart' in window ||
				navigator.maxTouchPoints > 0 ||
				navigator.msMaxTouchPoints > 0
			)
		) {
			// Prevent Enter key from creating a new line
			if (e.key === 'Enter' && !e.shiftKey) {
				e.preventDefault();
			}

			// Submit the prompt when Enter key is pressed
			if (prompt !== '' && e.key === 'Enter' && !e.shiftKey) {
				dispatch('submit', prompt);
			}
		}
	}}
	on:keydown={async (e) => {
		const isCtrlPressed = e.ctrlKey || e.metaKey; // metaKey is for Cmd key on Mac
		const commandsContainerElement =
			document.getElementById('commands-container');

		if (e.key === 'Escape') {
			stopResponse();
		}
		// Command/Ctrl + Shift + Enter to submit a message pair
		if (isCtrlPressed && e.key === 'Enter' && e.shiftKey) {
			e.preventDefault();
			createMessagePair(prompt);
		}

		// Check if Ctrl + R is pressed
		if (prompt === '' && isCtrlPressed && e.key.toLowerCase() === 'r') {
			e.preventDefault();
			console.log('regenerate');

			const regenerateButton = [
				...document.getElementsByClassName('regenerate-response-button')
			]?.at(-1);

			regenerateButton?.click();
		}

		if (prompt === '' && e.key == 'ArrowUp') {
			e.preventDefault();

			const userMessageElement = [
				...document.getElementsByClassName('user-message')
			]?.at(-1);

			const editButton = [
				...document.getElementsByClassName('edit-user-message-button')
			]?.at(-1);

			console.log(userMessageElement);

			userMessageElement.scrollIntoView({ block: 'center' });
			editButton?.click();
		}

		if (commandsContainerElement && e.key === 'ArrowUp') {
			e.preventDefault();
			commandsElement.selectUp();

			const commandOptionButton = [
				...document.getElementsByClassName('selected-command-option-button')
			]?.at(-1);
			commandOptionButton.scrollIntoView({ block: 'center' });
		}

		if (commandsContainerElement && e.key === 'ArrowDown') {
			e.preventDefault();
			commandsElement.selectDown();

			const commandOptionButton = [
				...document.getElementsByClassName('selected-command-option-button')
			]?.at(-1);
			commandOptionButton.scrollIntoView({ block: 'center' });
		}

		if (commandsContainerElement && e.key === 'Enter') {
			e.preventDefault();

			const commandOptionButton = [
				...document.getElementsByClassName('selected-command-option-button')
			]?.at(-1);

			if (e.shiftKey) {
				prompt = `${prompt}\n`;
			} else if (commandOptionButton) {
				commandOptionButton?.click();
			} else {
				document.getElementById('send-message-button')?.click();
			}
		}

		if (commandsContainerElement && e.key === 'Tab') {
			e.preventDefault();

			const commandOptionButton = [
				...document.getElementsByClassName('selected-command-option-button')
			]?.at(-1);

			commandOptionButton?.click();
		} else if (e.key === 'Tab') {
			const words = findWordIndices(prompt);

			if (words.length > 0) {
				const word = words.at(0);
				const fullPrompt = prompt;

				prompt = prompt.substring(0, word?.endIndex + 1);
				await tick();

				e.target.scrollTop = e.target.scrollHeight;
				prompt = fullPrompt;
				await tick();

				e.preventDefault();
				e.target.setSelectionRange(word?.startIndex, word.endIndex + 1);
			}

			e.target.style.height = '';
			e.target.style.height = Math.min(e.target.scrollHeight, 320) + 'px';
		}

		if (e.key === 'Escape') {
			console.log('Escape');
			atSelectedModel = undefined;
			webSearchEnabled = false;
			imageGenerationEnabled = false;
		}
	}}
	rows="1"
	on:input={async (e) => {
		e.target.style.height = '';
		e.target.style.height = Math.min(e.target.scrollHeight, 320) + 'px';
	}}
	on:focus={async (e) => {
		e.target.style.height = '';
		e.target.style.height = Math.min(e.target.scrollHeight, 320) + 'px';
	}}
	on:paste={async (e) => {
		const clipboardData = e.clipboardData || window.clipboardData;

		if (clipboardData && clipboardData.items) {
			for (const item of clipboardData.items) {
				if (item.type.indexOf('image') !== -1) {
					const blob = item.getAsFile();
					const reader = new FileReader();

					reader.onload = function (e) {
						files = [
							...files,
							{
								type: 'image',
								url: `${e.target.result}`
							}
						];
					};

					reader.readAsDataURL(blob);
				} else if (item.type === 'text/plain') {
					if ($settings?.largeTextAsFile ?? false) {
						const text = clipboardData.getData('text/plain');

						if (text.length > PASTED_TEXT_CHARACTER_LIMIT) {
							e.preventDefault();
							const blob = new Blob([text], { type: 'text/plain' });
							const file = new File([blob], `Pasted_Text_${Date.now()}.txt`, {
								type: 'text/plain'
							});

							await uploadFileHandler(file, true);
						}
					}
				}
			}
		}
	}}
/>
