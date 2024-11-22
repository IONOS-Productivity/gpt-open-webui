<script lang="ts">
	import { Dialog } from 'bits-ui';
	import { getContext } from 'svelte';

	const i18n = getContext('i18n');

	let mailInput: string;

	$: isButtonDisabled = !mailInput;
</script>

<Dialog.Portal>
	<Dialog.Overlay class="fixed inset-0 z-50 bg-black/80" />
	<Dialog.Content
		class="bg-[var(--ion-background-color)] sheet fixed left-[50%] top-[50%] z-50 w-full max-w-[94%] translate-x-[-50%] translate-y-[-50%]  p-5 shadow-popover outline-none sm:max-w-[700px] md:w-full"
	>
		<Dialog.Close class="sheet__close"></Dialog.Close>

		<Dialog.Title>
			<h1 class="card__headline">{$i18n.t('Bleiben Sie informiert...', { ns: 'ionos' })}</h1>
		</Dialog.Title>
		<Dialog.Description class="paragraph">
			<p>
				{$i18n.t(
					'Wir arbeiten weiterhin daran und halten Sie auf dem Laufenden, wenn es Neuigkeiten gibt. Geben Sie uns einfach Ihre Email Adresse',
					{ ns: 'ionos' }
				)}
			</p>
		</Dialog.Description>
		<div class="card__content">
			<label class="label" for="email">Email</label>
			<span class="input-text-group">
				<span class="input-text-group__icon input-text-group__icon--mail"></span>
				<input
					type="email"
					class="input-text"
					id="email"
					bind:value={mailInput}
					placeholder={$i18n.t('Email Adresse', { ns: 'ionos' })}
				/>
			</span>
		</div>
		<div class="sheet__footer sheet__footer--align-right">
			<button
				class="button button--primary {isButtonDisabled ? 'button--disabled' : ''}"
				disabled={isButtonDisabled}
				on:click={() => {
					console.log('Send email:', mailInput);
				}}
			>
				{$i18n.t('Send')}
			</button>
		</div>
	</Dialog.Content>
</Dialog.Portal>
