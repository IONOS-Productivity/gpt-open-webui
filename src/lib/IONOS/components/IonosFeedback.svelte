<script lang="ts">
	import Star from '$lib/components/icons/Star.svelte';
	import { Dialog } from 'bits-ui';
	import { getContext } from 'svelte';
	import { postFeedback } from '$lib/IONOS/components/feedback';

	const i18n = getContext('i18n');

	export let dialogOpen = false;

	let rating = 0;
	let feedbackText = '';
	let feedbackSent = false;
	let hoveredRating: number | undefined;
	let feedbackProvided = false;

	$: feedbackProvided = feedbackText.trim().length > 0 || rating > 0;

	$: if (!dialogOpen) resetFeedbackDialog();

	function resetFeedbackDialog() {
		feedbackSent = false;
		feedbackProvided = false;
		feedbackText = '';
		rating = 0;
	}

	let response: Promise<any>;

	const sendFeedback = () => {
		response = postFeedback(feedbackText, rating);
	};
</script>

<Dialog.Portal>
	<Dialog.Overlay class="fixed inset-0 z-50 bg-black/80" />
	<Dialog.Content
		class="bg-[var(--ion-background-color)] sheet fixed left-[50%] top-[50%] z-50 w-full max-w-[94%] translate-x-[-50%] translate-y-[-50%]  p-5 shadow-popover outline-none sm:max-w-[700px] md:w-full"
	>
		<Dialog.Close class="sheet__close"></Dialog.Close>
		{#if !feedbackSent}
			<Dialog.Title>
				<h1 class="card__headline">{$i18n.t('Feedback', { ns: 'ionos' })}</h1>
			</Dialog.Title>
			<Dialog.Description class="paragraph">
				<p>{$i18n.t('Pass on your impressions, suggestions etc. to us...', { ns: 'ionos' })}</p>
			</Dialog.Description>
			<div class="card__content">
				<textarea
					class="input-textarea"
					placeholder={$i18n.t('Your feedback to us', { ns: 'ionos' })}
					bind:value={feedbackText}
					rows="8"
				></textarea>

				<div class="star-rating">
					<p>{$i18n.t('General evaluation', { ns: 'ionos' })}</p>
					{#each Array(5) as _, index}
						<button
							type="button"
							on:click={() => (rating = index + 1)}
							on:mouseover={() => (hoveredRating = index + 1)}
							on:mouseout={() => (hoveredRating = undefined)}
							on:focus={() => (hoveredRating = index + 1)}
							on:blur={() => (hoveredRating = undefined)}
							class:filled={index < (hoveredRating ?? rating ?? 0)}
						>
							<Star />
						</button>
					{/each}
				</div>
			</div>

			<div class="sheet__footer sheet__footer--align-right">
				<button
					type="button"
					class="button button--primary {feedbackProvided ? '' : 'button--disabled'}"
					disabled={!feedbackProvided}
					on:click={() => {
						feedbackSent = true;
						sendFeedback();
					}}
				>
					{$i18n.t('Send')}
				</button>
			</div>
		{/if}

		{#if feedbackSent}
			{#await postFeedback(feedbackText, rating)}
				<p>{$i18n.t('Feedback is being sent', { ns: 'ionos' })}</p>
			{:then}
				<Dialog.Title>
					<h1 class="card__headline">{$i18n.t('Thanks!', { ns: 'ionos' })}</h1>
				</Dialog.Title>

				<div class="message message--success">
					<section class="message__section">
						<h4 class="headline headline--sub headline--success">
							{$i18n.t('We have received your feedback', { ns: 'ionos' })}
						</h4>
					</section>
				</div>
				<div class="sheet__footer sheet__footer--align-right">
					<Dialog.Close class="sheet__footer sheet__footer--align-right">
						<button type="button" class="button button--primary">
							{$i18n.t('Close')}
						</button>
					</Dialog.Close>
				</div>
			{:catch}
				<Dialog.Title>
					<h1 class="card__headline">{$i18n.t('Das hat nicht funktioniert', { ns: 'ionos' })}</h1>
				</Dialog.Title>
				<div class="message message--critical">
					<section class="message__section">
						<h4 class="headline headline--sub headline--critical">
							{$i18n.t('Feedback could not be sent', { ns: 'ionos' })}
						</h4>
					</section>
				</div>
				<div class="sheet__footer sheet__footer--align-right">
					<Dialog.Close class="sheet__footer sheet__footer--align-right">
						<button type="button" class="button button--primary" on:click={resetFeedbackDialog}>
							{$i18n.t('Back')}
						</button>
					</Dialog.Close>
				</div>
			{/await}
		{/if}
	</Dialog.Content>
</Dialog.Portal>

<style>
	.star-rating {
		display: flex;
		gap: 0.5rem;
		margin-top: 1rem;
		align-items: center;
	}

	.star-rating button {
		color: var(--ion-text-color);
		cursor: pointer;
	}

	.star-rating button.filled {
		color: var(--warning-shape-color);
	}
</style>
