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
	const userAgent = navigator.userAgent;
	// Check for Safari but exclude Chrome on iOS (CriOS) and Android Chrome
	return /safari/i.test(userAgent) && !/crios|chrome|android/i.test(userAgent);
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

export function shouldShowPWAPrompt(deferredPrompt?: BeforeInstallPromptEvent | null): boolean {
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

	return deferredPrompt !== null && deferredPrompt !== undefined;
}

export function dismissPWAPrompt(): void {
	localStorage.setItem('pwa-install-dismissed', 'true');
}

export async function triggerPWAInstall(deferredPrompt: BeforeInstallPromptEvent | null): Promise<boolean> {
	if (!deferredPrompt) {
		return false;
	}

	try {
		await deferredPrompt.prompt();
		const choiceResult = await deferredPrompt.userChoice;
		return choiceResult.outcome === 'accepted';
	} catch (error) {
		console.error('Error triggering PWA install prompt:', error);
		return false;
	}
}

export function getPWADebugInfo(): Record<string, any> {
	const isSecureContext = location.protocol === 'https:' || location.hostname === 'localhost' || location.hostname === '127.0.0.1';

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
		referrer: document.referrer,
		protocol: location.protocol,
		hostname: location.hostname,
		isSecureContext: isSecureContext,
		hasBeforeInstallPrompt: 'BeforeInstallPromptEvent' in window || 'onbeforeinstallprompt' in window,
		serviceWorkerSupport: 'serviceWorker' in navigator
	};
}
