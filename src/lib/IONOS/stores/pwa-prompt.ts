import { writable, type Writable } from 'svelte/store';
import type { BeforeInstallPromptEvent } from '$lib/IONOS/services/pwa';

export const deferredPrompt: Writable<BeforeInstallPromptEvent | null> = writable(null);
export const isPWAInstallable = writable(false);

let isSetup = false;
let cleanupFunction: (() => void) | null = null;

export function setupGlobalPWAListener(): (() => void) | null {
	if (isSetup || typeof window === 'undefined') {
		console.log('PWA listener already set up or not in a browser environment.');
		return cleanupFunction;
	}

	const handleBeforeInstallPrompt = (event: Event) => {
		console.log('Received beforeinstallprompt event');
		event.preventDefault();
		const installPromptEvent = event as BeforeInstallPromptEvent;
		deferredPrompt.set(installPromptEvent);
		isPWAInstallable.set(true);
	};

	const handleAppInstalled = () => {
		console.log('PWA was installed');
		deferredPrompt.set(null);
		isPWAInstallable.set(false);
	};

	window.addEventListener('beforeinstallprompt', handleBeforeInstallPrompt);
	window.addEventListener('appinstalled', handleAppInstalled);
	console.log('PWA listeners set up');

	cleanupFunction = () => {
		window.removeEventListener('beforeinstallprompt', handleBeforeInstallPrompt);
		window.removeEventListener('appinstalled', handleAppInstalled);
		isSetup = false;
		cleanupFunction = null;
	};

	isSetup = true;
	return cleanupFunction;
}

export function clearDeferredPrompt() {
	deferredPrompt.set(null);
	isPWAInstallable.set(false);
}
