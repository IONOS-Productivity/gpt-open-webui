<script lang="ts">
	import { type Readable, get } from 'svelte/store';
	import type { I18Next } from '$lib/IONOS/i18next.d.ts';
	import type { Chat } from '$lib/apis/chats/types.ts';
	import NotificationBanner from "$lib/IONOS/components/notifications/NotificationBanner.svelte";
	import PWAInstallDialog from "$lib/IONOS/components/notifications/PWAInstallDialog.svelte";
	import { chats, user } from '$lib/stores';
	import { updateSettings } from '$lib/IONOS/services/settings';
	import { buildSurveyUrl } from '$lib/IONOS/services/survey';
	import { notifications, addNotification, removeNotification, type Notification, type SubscribableNotification, NotificationType } from "$lib/IONOS/stores/notifications";
	import { getContext, onDestroy, onMount } from 'svelte';
	import { getUserSettings } from '$lib/apis/users';
	import {
		shouldShowPWAPrompt,
		dismissPWAPrompt,
		triggerPWAInstall,
		isIOSDevice,
		isSafari
	} from '$lib/IONOS/services/pwa';
	import { deferredPrompt, isPWAInstallable, setupGlobalPWAListener, clearDeferredPrompt } from '$lib/IONOS/stores/pwa-prompt';

	const i18n = getContext<Readable<I18Next>>('i18n');
	const DAYS = 24 * 60 * 60 * 1000;

	let showPWADialog = false;
	let cleanupPWAListeners: (() => void) | null = null;

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

		const surveyNotification = {
			subscribe: (fn: (notification: Notification) => void) => {
				return i18n.subscribe(() => {
					fn({
						id: "survey",
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
					});
				});
			}
		};
		addNotification(surveyNotification);
	};

	const dismissHandler = (event: CustomEvent) => {
		const notification = event.detail.notification;

		if (get(notification).type === NotificationType.PWA_INSTALL) {
			dismissPWAPrompt();
		}

		removeNotification(notification);
	};

	onDestroy(() => {
		unsubscribeChats();
	});

	onMount(() => {
		if ("serviceWorker" in navigator) {
			navigator.serviceWorker.ready.then(() => {
				console.log('NotificationManager:', 'Service Worker is ready');
				if (shouldShowPWAPrompt($deferredPrompt)) {
					console.log('NotificationManager:', 'PWA is installable, showing prompt');
					addPWANotification();
				}
			});
		}
	});

	$: if (!$isPWAInstallable && !$deferredPrompt) {
		showPWADialog = false;
		notifications.update((currentNotifications: Notification[]) =>
			currentNotifications.filter(n => n.type !== NotificationType.PWA_INSTALL)
		);
	}

	const addPWANotification = () => {
		const pwaNotification = {
			subscribe: (fn: (notification: Notification) => void) => {
				return i18n.subscribe(() => {
					fn({
						id: "pwa",
						type: NotificationType.PWA_INSTALL,
						title: $i18n.t('Install IONOS GPT', { ns: 'ionos' }),
						message: $i18n.t('For quick and easy access, you can now install IONOS GPT like an app!', { ns: 'ionos' }),
						actions: [{
							label: $i18n.t('Install', { ns: 'ionos' }),
							handler: () => {
								handlePWAInstall();
							}
						}],
						dismissible: true,
					});
				});
			}
		};

		addNotification(pwaNotification);
	};

	const handlePWAInstall = async () => {
		const showIOSInstructions = isIOSDevice() && isSafari();

		if (showIOSInstructions) {
			showPWADialog = true;
		} else if ($deferredPrompt) {
			const accepted = await triggerPWAInstall($deferredPrompt);
			if (accepted) {
				clearDeferredPrompt();
				removeNotification("pwa");
			}
		}
	};

	const handlePWADialogDismiss = () => {
		showPWADialog = false;
	};

	const handlePWADialogInstall = async () => {
		if ($deferredPrompt) {
			const accepted = await triggerPWAInstall($deferredPrompt);
			if (accepted) {
				clearDeferredPrompt();
			}
		}
		showPWADialog = false;
		removeNotification("pwa");
	};
</script>

<div class="sticky top-0 flex flex-col w-full z-50">
	{#each $notifications as notification }
		<NotificationBanner
			{notification}
			on:dismiss={dismissHandler}
		/>
	{/each}
</div>

<PWAInstallDialog
	bind:show={showPWADialog}
	on:install={handlePWADialogInstall}
	on:close={handlePWADialogDismiss}
/>
