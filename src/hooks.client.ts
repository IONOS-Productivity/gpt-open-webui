import { setupGlobalPWAListener } from '$lib/IONOS/stores/pwa-prompt';
import type { ClientInit } from '@sveltejs/kit';

export const init: ClientInit = () => {
	setupGlobalPWAListener();
};
