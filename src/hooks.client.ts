import { setupGlobalPWAListener } from '$lib/IONOS/stores/pwa-prompt';
import type { ClientInit } from '@sveltejs/kit';

export const init: ClientInit = () => {
	console.log('hooks.client.ts:', 'Setting up pwa listener')
	setupGlobalPWAListener();
};
