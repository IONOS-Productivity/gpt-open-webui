/**
 * PWA (Progressive Web App) utility functions
 * Handles PWA installation detection, prompts, and platform-specific logic
 */

export interface BeforeInstallPromptEvent extends Event {
	readonly platforms: string[];
	readonly userChoice: Promise<{
		outcome: 'accepted' | 'dismissed';
		platform: string;
	}>;
	prompt(): Promise<void>;
}

export enum PWADisplayMode {
	BROWSER = 'browser',
	STANDALONE = 'standalone',
	MINIMAL_UI = 'minimal-ui',
	FULLSCREEN = 'fullscreen',
	TWA = 'twa'
}

export enum PWAPlatform {
	IOS = 'ios',
	ANDROID = 'android',
	DESKTOP = 'desktop',
	UNKNOWN = 'unknown'
}

export function getPWADisplayMode(): PWADisplayMode {
	// Check if running as TWA (Trusted Web Activity)
	if (document.referrer.startsWith('android-app://')) {
		return PWADisplayMode.TWA;
	}

	if (window.matchMedia('(display-mode: standalone)').matches || (navigator as any).standalone) {
		return PWADisplayMode.STANDALONE;
	}

	if (window.matchMedia('(display-mode: minimal-ui)').matches) {
		return PWADisplayMode.MINIMAL_UI;
	}

	if (window.matchMedia('(display-mode: fullscreen)').matches) {
		return PWADisplayMode.FULLSCREEN;
	}

	return PWADisplayMode.BROWSER;
}

export function isPWAInstalled(): boolean {
	const displayMode = getPWADisplayMode();
	return displayMode === PWADisplayMode.STANDALONE || displayMode === PWADisplayMode.TWA || displayMode === PWADisplayMode.FULLSCREEN;
}

export function getPlatform(): PWAPlatform {
	const userAgent = navigator.userAgent.toLowerCase();

	if (/ipad|iphone|ipod/.test(userAgent) && !window.MSStream) {
		return PWAPlatform.IOS;
	}

	if (/android/.test(userAgent)) {
		return PWAPlatform.ANDROID;
	}

	if (/windows|macintosh|linux/.test(userAgent)) {
		return PWAPlatform.DESKTOP;
	}

	return PWAPlatform.UNKNOWN;
}

export function isSafari(): boolean {
	return /^((?!chrome|android).)*safari/i.test(navigator.userAgent);
}

export function isIOSDevice(): boolean {
	return getPlatform() === PWAPlatform.IOS;
}

export function isPWAInstallSupported(): boolean {
	if (isIOSDevice() && isSafari()) {
		return true;
	}

	return 'BeforeInstallPromptEvent' in window || 'onbeforeinstallprompt' in window;
}

/**
 * Checks if we should show the PWA install prompt
 */
export function shouldShowPWAPrompt(deferredPrompt: BeforeInstallPromptEvent | null = null): boolean {
	if (isPWAInstalled()) {
		return false;
	}

	if (localStorage.getItem('pwa-install-dismissed') === 'true') {
		return false;
	}

	if (!isPWAInstallSupported()) {
		return false;
	}

	if (isIOSDevice() && isSafari()) {
		return true;
	}

	return deferredPrompt !== null;
}

export function dismissPWAPrompt(): void {
	localStorage.setItem('pwa-install-dismissed', 'true');
}

/**
 * Triggers the native PWA install prompt if available
 */
export async function triggerPWAInstall(deferredPrompt: BeforeInstallPromptEvent): Promise<boolean> {

	if (!deferredPrompt) {
		return Promise.resolve(false);
	}
	try {
		await deferredPrompt.prompt();
		const choiceResult = await deferredPrompt.userChoice;
		return Promise.resolve(choiceResult.outcome === 'accepted');
	} catch (error) {
		return Promise.resolve(false);
	}
}

/**
 * Sets up PWA event listeners and returns cleanup function
 */
export function setupPWAEventListeners(
	onBeforeInstallPrompt?: (event: BeforeInstallPromptEvent) => void,
	onAppInstalled?: () => void
): () => void {
	const handleBeforeInstallPrompt = (event: Event) => {
		event.preventDefault();
		const installPromptEvent = event as BeforeInstallPromptEvent;
		onBeforeInstallPrompt?.(installPromptEvent);
	};

	const handleAppInstalled = () => {
		onAppInstalled?.();
	};

	window.addEventListener('beforeinstallprompt', handleBeforeInstallPrompt);
	window.addEventListener('appinstalled', handleAppInstalled);

	return () => {
		window.removeEventListener('beforeinstallprompt', handleBeforeInstallPrompt);
		window.removeEventListener('appinstalled', handleAppInstalled);
	};
}

/**
 * Tracks user engagement for PWA install prompt timing
 */
export function trackUserEngagement(): void {
	const currentPageViews = parseInt(localStorage.getItem('pwa-page-views') || '0');
	localStorage.setItem('pwa-page-views', (currentPageViews + 1).toString());

	if (!localStorage.getItem('pwa-first-visit')) {
		localStorage.setItem('pwa-first-visit', Date.now().toString());
	}
}

export function getPWADebugInfo(): Record<string, any> {
	return {
		displayMode: getPWADisplayMode(),
		platform: getPlatform(),
		isInstalled: isPWAInstalled(),
		isInstallSupported: isPWAInstallSupported(),
		isDismissed: localStorage.getItem('pwa-install-dismissed') === 'true',
		pageViews: localStorage.getItem('pwa-page-views'),
		firstVisit: localStorage.getItem('pwa-first-visit'),
		userAgent: navigator.userAgent,
		standalone: (navigator as any).standalone,
		referrer: document.referrer
	};
}
