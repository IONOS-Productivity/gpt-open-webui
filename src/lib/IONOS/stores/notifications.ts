import { get, writable, type Writable, type Readable } from 'svelte/store';

export enum NotificationType {
	INFO = 'bg-blue-100 text-blue-800',
	SUCCESS = 'success',
	ERROR = 'bg-red-100 text-blue-800',
	WARNING = 'warning',
	FEEDBACK = NotificationType.INFO,
	PWA_INSTALL = NotificationType.INFO,
}

export type NotificationActionBase = {
	label: string;
};

/**
 * Handle notification action clicks as click event handler
 */
export type NotificationActionClickHandler = {
	handler?: (e: Event) => void;
};

/**
 * Handle notification action clicks as href
 */
export type NotificationActionHref = {
	href?: string;
};

export type NotificationAction = NotificationActionBase & NotificationActionClickHandler & NotificationActionHref;

export type Notification = {
	id: string;
	type: NotificationType;
	title: string;
	message: string;
	actions: NotificationAction[];
	dismissible?: boolean;
};

export type SubscribableNotification = Readable<Notification>;

export const notifications: Writable<SubscribableNotification[]> = writable([]);

export const addNotification = (newNotificationStore: SubscribableNotification): void => {
	const newNotification: Notification = get(newNotificationStore);
	const currentNotifications = get(notifications);
	const alreadyPresent: boolean = currentNotifications.some(n => get(n).id === newNotification.id);

	if (!alreadyPresent) {
		notifications.update((current: SubscribableNotification[]) => [...current, newNotificationStore]);
	}
};

export const removeNotification = (id: string): void => {
	notifications.update((currentNotifications: Notification[]) =>
		currentNotifications.filter(n => n.id !== id)
	);
};
