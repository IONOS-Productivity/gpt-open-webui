<script lang="ts">
	import { getContext } from 'svelte';
	import {
		showSidebar,
	} from '$lib/stores';
	const currentYear = new Date().getFullYear();
	const i18n = getContext('i18n');
</script>

<footer class="{$showSidebar
			? 'md:max-w-[calc(100%-260px)]'
			: ''}">

	<div class="footer-right">
		<span id="powered_by">{$i18n.t('powered by IONOS Model Hub', { ns: 'ionos' })}</span>
	</div>
	<div id="copyright">
		<p>© {currentYear} IONOS SE</p>
	</div>
	<div class="footer-left">
		<a href="{$i18n.t('https://www.ionos.de/impressum', { ns: 'ionos' })}" target="_blank" class="exos-link">
			{$i18n.t('Imprint', { ns: 'ionos' })}
		</a>
		<a href="{$i18n.t('https://www.ionos.de/terms-gtc/terms-privacy', { ns: 'ionos' })}" target="_blank" class="exos-link">
			{$i18n.t('Privacy Policy', { ns: 'ionos' })}
		</a>
		<a href="{$i18n.t('https://www.ionos.de/terms-gtc/terms', { ns: 'ionos' })}" target="_blank" class="exos-link">
			{$i18n.t('Terms and Conditions', { ns: 'ionos' })}
		</a>
	</div>
</footer>

<style>
	@import './ionos-variables.css';
	footer {
		z-index: 19;
		display: flex;
		justify-content: space-between;
		align-items: center;
		background-color: var(--ion-background-color);
		height: 32px;
		padding: 0 24px;
		position: fixed;
		bottom: 0;
		right: 0;
		width: 100%;
	}

	#powered_by {
		color: var(--powered-by-text-color);
	}

	.footer-left {
		display: flex;
		align-items: center;
		gap: 16px;
		margin-right: 16px;
	}

	#copyright {
		color: var(--ion-text-color);
		position: absolute;
		left: 50%;
		transform: translateX(-50%);
	}
</style>
