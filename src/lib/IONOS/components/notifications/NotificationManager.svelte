<script lang="ts">
	import type { Readable } from 'svelte/store';
	import type { I18Next } from '$lib/IONOS/i18next.d.ts';
	import type { Chat } from '$lib/apis/chats/types.ts';
	import NotificationBanner from "$lib/IONOS/components/notifications/NotificationBanner.svelte";
	import PWAInstallDialog from "$lib/IONOS/components/notifications/PWAInstallDialog.svelte";
	import { chats, user } from '$lib/stores';
	import { updateSettings } from '$lib/IONOS/services/settings';
	import { buildSurveyUrl } from '$lib/IONOS/services/survey';
	import { notifications, addNotification, removeNotification, type Notification, NotificationType } from "$lib/IONOS/stores/notifications";
	import { getContext, onDestroy, onMount } from 'svelte';
	import { getUserSettings } from '$lib/apis/users';
	import {
		setupPWAEventListeners,
		shouldShowPWAPrompt,
		dismissPWAPrompt,
		trackUserEngagement,
		triggerPWAInstall,
		isIOSDevice,
		isSafari,
		type BeforeInstallPromptEvent
	} from '$lib/IONOS/services/pwa';

	const i18n = getContext<Readable<I18Next>>('i18n');

	const DAYS = 24 * 60 * 60 * 1000;

	// PWA Installation state
	let deferredPrompt: BeforeInstallPromptEvent | null = null;
	let showPWADialog = false;
	let cleanupPWAListeners: (() => void) | null = null;

	// Check if the user should be prompted for feedback
	const unsubscribeChats = chats.subscribe(async (chats: Chat[]|null) => {
		const userSettings = await getUserSettings(localStorage.token);
		const userCreatedAt = new Date($user!.created_at * 1000);
		if (chats?.length >= 2 || (new Date().getTime() - userCreatedAt.getTime()) > (14 * DAYS)) {
			if (!userSettings.ui?.ionosProvidedFeedback) {
				addSurveyNotification();
			}
		}
	});

	const addSurveyNotification = () => {
		const surveyUrl = buildSurveyUrl($user!);

		if (surveyUrl === null) {
			return;
		}

		const surveyNotification: Notification = {
			type: NotificationType.FEEDBACK,
			title: $i18n.t('Love our product?', { ns: 'ionos' }),
			message: $i18n.t('Help us improve', { ns: 'ionos' }),
			actions: [{
				label: $i18n.t('Take Our Quick Survey', { ns: 'ionos' }),
				handler: () => {
					window.open(surveyUrl, '_blank', "noopener=yes,noreferrer=yes");
					updateSettings({
						ionosProvidedFeedback: true
					});
				}
			}],
		}
		addNotification(surveyNotification);
	};

	const dismissHandler = (event: CustomEvent) => {
		const notification = event.detail.notification;

		// Handle PWA notification dismissal
		if (notification.type === NotificationType.PWA_INSTALL) {
			handlePWADismiss();
		}

		removeNotification(notification);
	};

	onDestroy(() => {
		unsubscribeChats();
		cleanupPWAListeners?.();
	});

	onMount(() => {
		trackUserEngagement();

		cleanupPWAListeners = setupPWAEventListeners(
			(event: BeforeInstallPromptEvent) => {
				deferredPrompt = event;

				if (shouldShowPWAPrompt(deferredPrompt)) {
					addPWANotification();
				}
			},
			() => {
				showPWADialog = false;
				deferredPrompt = null;
				notifications.update((currentNotifications: Notification[]) =>
					currentNotifications.filter(n => n.type !== NotificationType.PWA_INSTALL)
				);
			}
		);


		if (isIOSDevice() && isSafari() && shouldShowPWAPrompt()) {
			setTimeout(() => {
				if (shouldShowPWAPrompt()) {
					addPWANotification();
				}
			}, 3000); // Show after 3 seconds
		}
	});

	const addPWANotification = () => {
		const pwaNotification: Notification = {
			type: NotificationType.PWA_INSTALL,
			title: $i18n.t('Install IONOS GPT', { ns: 'ionos' }),
			message: $i18n.t('For quick and easy access, you can now install IONOS GPT like an app!', { ns: 'ionos' }),
			actions: [{
				label: $i18n.t('Install', { ns: 'ionos' }),
				handler: () => {
					if (isIOSDevice() && isSafari()) {
						handlePWAShowDialog();
					} else {
						handlePWAInstall();
					}
				}
			}],
			dismissible: true,
		};
		addNotification(pwaNotification);
	};

	const handlePWAInstall = async () => {
		if (deferredPrompt) {
			const accepted = await triggerPWAInstall(deferredPrompt);
			deferredPrompt = null;
		}
	};

	const handlePWADismiss = () => {
		dismissPWAPrompt();
	};

	const handlePWADialogDismiss = () => {
		showPWADialog = false;
		handlePWADismiss();
	};
</script>

<div class="sticky top-0 flex flex-col w-full z-50">
	<!-- All Notifications (including PWA) -->
	{#each $notifications as notification }
		<NotificationBanner
			{notification}
			{deferredPrompt}
			on:dismiss={dismissHandler}
			on:showDialog={showPWADialog = true }
		/>
	{/each}
</div>

<!-- PWA Installation Dialog -->
<PWAInstallDialog
	bind:show={showPWADialog}
	on:install={handlePWAInstall}
	on:dismiss={handlePWADialogDismiss}
/>
