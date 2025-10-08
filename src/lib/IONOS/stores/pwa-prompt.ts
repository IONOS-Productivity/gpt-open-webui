import { writable, type Writable } from 'svelte/store';
import type { BeforeInstallPromptEvent } from '$lib/IONOS/services/pwa';

export const deferredPrompt: Writable<BeforeInstallPromptEvent | null> = writable(null);
export const isPWAInstallable = writable(false);

let isSetup = false;
let cleanupFunction: (() => void) | null = null;

export function setupGlobalPWAListener(): (() => void) | null {
	if (isSetup || typeof window === 'undefined') {
		return cleanupFunction;
	}

	const handleBeforeInstallPrompt = (event: Event) => {
		event.preventDefault();
		const installPromptEvent = event as BeforeInstallPromptEvent;
		deferredPrompt.set(installPromptEvent);
		isPWAInstallable.set(true);
	};

	const handleAppInstalled = () => {
		deferredPrompt.set(null);
		isPWAInstallable.set(false);
	};

	window.addEventListener('beforeinstallprompt', handleBeforeInstallPrompt);
	window.addEventListener('appinstalled', handleAppInstalled);

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
