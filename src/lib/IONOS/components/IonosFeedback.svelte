<script lang="ts">
	import Star from '$lib/components/icons/Star.svelte';
	import { Dialog } from 'bits-ui';
	import { getContext } from 'svelte';
	import { postFeedback } from '$lib/IONOS/api/feedbackBackend';

	const i18n = getContext('i18n');

	export let dialogOpen = false;

	let rating = 0;
	export let noRating = false;

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
</script>

<Dialog.Portal>
	<Dialog.Overlay class="fixed inset-0 z-50 bg-black/80" />
	<Dialog.Content
		class="bg-[var(--ion-background-color)] exos-sheet fixed left-[50%] top-[50%] z-50 w-full max-w-[94%] translate-x-[-50%] translate-y-[-50%]  p-5 shadow-popover outline-none sm:max-w-[700px] md:w-full"
	>
		<Dialog.Close class="exos-sheet__close"></Dialog.Close>
		{#if !feedbackSent}
			<Dialog.Title>
				<h1 class="exos-card__headline">{$i18n.t('Feedback', { ns: 'ionos' })}</h1>
			</Dialog.Title>
			<Dialog.Description class="exos-paragraph">
				<p>{$i18n.t('Pass on your impressions, suggestions etc. to us...', { ns: 'ionos' })}</p>
			</Dialog.Description>
			<div class="exos-card__content">
				<textarea
					class="exos-input-textarea"
					placeholder={$i18n.t('Your feedback to us', { ns: 'ionos' })}
					bind:value={feedbackText}
					rows="8"
				></textarea>

				{#if noRating}
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
				{/if}
			</div>

			<div class="exos-sheet__footer exos-sheet__footer--align-right">
				<button
					type="button"
					class="exos-button exos-button--primary {feedbackProvided ? '' : 'exos-button--disabled'}"
					disabled={!feedbackProvided}
					on:click={() => {
						feedbackSent = true;
					}}
				>
					{$i18n.t('Send')}
				</button>
			</div>
		{/if}

		{#if feedbackSent}
			{#await postFeedback(feedbackText, rating)}
				<section class="exos-sheet__section">
					<ul class="exos-stripe exos-stripe--align-center">
						<li class="exos-stripe__item">
							<div
								class="exos-loading-spin exos-loading-spin--bright exos-loading-spin--small"
							></div>
						</li>
						<li class="exos-stripe__item">
							<p class="exos-paragraph exos-paragraph--cropped exos-paragraph--align-center">
								{$i18n.t('Feedback is being sent', { ns: 'ionos' })}
							</p>
						</li>
					</ul>
				</section>
			{:then}
				<Dialog.Title>
					<h1 class="exos-card__headline">{$i18n.t('Thanks!', { ns: 'ionos' })}</h1>
				</Dialog.Title>

				<div class="exos-message exos-message--success">
					<section class="exos-message__section">
						<h4 class="exos-headline exos-headline--sub exos-headline--success">
							{$i18n.t('We have received your feedback', { ns: 'ionos' })}
						</h4>
					</section>
				</div>
				<div class="exos-sheet__footer exos-sheet__footer--align-right">
					<Dialog.Close class="exos-sheet__footer exos-sheet__footer--align-right">
						<button type="button" class="exos-button exos-button--primary">
							{$i18n.t('Close')}
						</button>
					</Dialog.Close>
				</div>
			{:catch}
				<Dialog.Title>
					<h1 class="exos-card__headline">
						{$i18n.t('Something went wrong', { ns: 'ionos' })}
					</h1>
				</Dialog.Title>
				<div class="exos-message exos-message--critical">
					<section class="exos-message__section">
						<h4 class="exos-headline exos-headline--sub exos-headline--critical">
							{$i18n.t('Feedback could not be sent', { ns: 'ionos' })}
						</h4>
					</section>
				</div>
				<div class="exos-sheet__footer exos-sheet__footer--align-right">
					<Dialog.Close class="exos-sheet__footer exos-sheet__footer--align-right">
						<button
							type="button"
							class="exos-button exos-button--primary"
							on:click={resetFeedbackDialog}
						>
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
		color: var(--solid-corporate-background-color);
		cursor: pointer;
	}

	.star-rating button.filled {
		color: var(--warning-shape-color);
	}
</style>
