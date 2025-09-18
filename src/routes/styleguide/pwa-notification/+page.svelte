<script lang="ts">
	import type { Readable } from 'svelte/store';
	import { getContext, onMount, onDestroy } from 'svelte';
	import type { I18Next } from '$lib/IONOS/i18next.d.ts';
	import PWAInstallDialog from '$lib/IONOS/components/notifications/PWAInstallDialog.svelte';
	import NotificationManager from '$lib/IONOS/components/notifications/NotificationManager.svelte';
	import {
		notifications,
		addNotification,
		removeNotification,
		type Notification,
		NotificationType
	} from "$lib/IONOS/stores/notifications";
	import {
		setupPWAEventListeners,
		shouldShowPWAPrompt,
		dismissPWAPrompt,
		triggerPWAInstall,
		type BeforeInstallPromptEvent
	} from '$lib/IONOS/services/pwa';

	const i18n = getContext<Readable<I18Next>>('i18n');
	// PWA state
	let deferredPrompt: BeforeInstallPromptEvent | null = null;
	let showPWADialog = false;
	let cleanupListeners: (() => void) | null = null;
	onMount(() => {
		// Setup PWA event listeners
		cleanupListeners = setupPWAEventListeners(
			(event: BeforeInstallPromptEvent) => {
				deferredPrompt = event;
				// Show PWA notification if conditions are met
				if (shouldShowPWAPrompt(deferredPrompt)) {
					addPWANotification();
				}
			},
			() => {
				// App was installed - cleanup
				showPWADialog = false;
				deferredPrompt = null;
				// Remove PWA notification if it exists
				notifications.update(current =>
					current.filter(n => n.type !== NotificationType.PWA_INSTALL)
				);
			}
		);
	});
	onDestroy(() => {
		cleanupListeners?.();
	});
	// Add PWA notification to the notification store
	const addPWANotification = () => {
		const pwaNotification: Notification = {
			type: NotificationType.INFO,
			title: $i18n.t('Install IONOS GPT', { ns: 'ionos' }),
			message: $i18n.t('For quick and easy access, you can now install IONOS GPT like an app!', { ns: 'ionos' }),
			actions: [{
				label: $i18n.t('Install', { ns: 'ionos' }),
				handler: () => {
					if (deferredPrompt) {
						handlePWAInstall();
					} else {
						handleShowDialog();
					}
				}
			}],
			dismissible: true,
		};
		addNotification(pwaNotification);
	};
	// Handle notification dismissal
	const handleDismiss = (event: CustomEvent) => {
		const notification = event.detail.notification;
		// Handle PWA notification dismissal
		if (notification.type === NotificationType.PWA_INSTALL) {
			dismissPWAPrompt();
		}
		removeNotification(notification);
	};
	// Handle PWA dialog show (for iOS)
	const handleShowDialog = () => {
		showPWADialog = true;
	};
	// Handle PWA installation
	const handlePWAInstall = async () => {
		if (deferredPrompt) {
			const accepted = await triggerPWAInstall(deferredPrompt);
			if (accepted) {
				console.log('PWA installed successfully');
			}
			deferredPrompt = null;
		}
	};
	const handleDialogDismiss = () => {
		showPWADialog = false;
		dismissPWAPrompt();
	};
	// Demo functions
	const addFeedbackNotification = () => {
		const feedbackNotification: Notification = {
			type: NotificationType.FEEDBACK,
			title: $i18n.t('Love our product?', { ns: 'ionos' }),
			message: $i18n.t('Help us improve', { ns: 'ionos' }),
			actions: [{
				label: $i18n.t('Take Our Quick Survey', { ns: 'ionos' }),
				handler: () => {
					alert('Survey would open here');
				}
			}],
			dismissible: false,
		};
		addNotification(feedbackNotification);
	};
	const addErrorNotification = () => {
		const errorNotification: Notification = {
			type: NotificationType.ERROR,
			title: 'Error occurred',
			message: 'Something went wrong. Please try again.',
			actions: [],
			dismissible: true,
		};
		addNotification(errorNotification);
	};
	const clearAllNotifications = () => {
		notifications.set([]);
	};
</script>


<NotificationManager />

<div class="max-w-4xl mx-auto p-6">
	<h1 class="text-3xl font-bold mb-6 text-gray-900">
		Integrated PWA Notification System
	</h1>

	<!-- Demo Controls -->
	<div class="bg-gray-50 border border-gray-200 rounded-lg p-4 mb-6">
		<h2 class="text-lg font-semibold text-gray-900 mb-3">Demo Controls</h2>
		<div class="flex flex-wrap gap-2">
			<button
				on:click={addPWANotification}
				class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
			>
				Add PWA Notification
			</button>
			<button
				on:click={addFeedbackNotification}
				class="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
			>
				Add Feedback Notification
			</button>
			<button
				on:click={addErrorNotification}
				class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
			>
				Add Error Notification
			</button>
			<button
				on:click={clearAllNotifications}
				class="px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors"
			>
				Clear All
			</button>
		</div>
	</div>
</div>

<!-- PWA Installation Dialog -->
<PWAInstallDialog
	bind:show={showPWADialog}
	on:install={handlePWAInstall}
	on:dismiss={handleDialogDismiss}
/>

<style>
	pre {
		font-family: 'Fira Code', 'Monaco', 'Consolas', monospace;
	}
</style>
