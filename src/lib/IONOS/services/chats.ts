import { goto } from '$app/navigation';
import { default as saveAs } from 'file-saver';
import dayjs from 'dayjs';
import { readFile } from '$lib/IONOS/utils/files';
import { parseChatExportData } from '$lib/IONOS/utils/import';
import type { Chat } from '$lib/apis/chats/types';
import {
	deleteAllChats,
	getAllChats,
	getChatList,
	createNewChat,
} from '$lib/apis/chats';
import {
	chats,
} from '$lib/stores';

export const EXPORT_FILENAME_PREFIX = 'ionos-gpt-export';

export const deleteAll = async (): Promise<void> => {
	const chatPaginationCurrentChatPage = 1;
	const token = localStorage.token;
	await goto('/');
	await deleteAllChats(token);
	chats.set(await getChatList(token, chatPaginationCurrentChatPage));
};

export const exportAll = async (): Promise<void> => {
	const blob = new Blob([JSON.stringify(await getAllChats(localStorage.token))], {
		type: 'application/json'
	});

	const timestamp = dayjs(Date.now()).format('YYYY-MM-DD--HH-mm');

	saveAs(blob, `${EXPORT_FILENAME_PREFIX}-${timestamp}.json`);
};

export const importChats = async (file: File): Promise<void> => {
	const token = localStorage.token;
	console.log(file);
	const contentsStr: string = await readFile(file);
	let imported: Chat[] = parseChatExportData(contentsStr);

	for (const chat of imported) {
		console.log(chat);

		if (chat.chat) {
			console.warn('IMPORT: what is this?');
			await createNewChat(localStorage.token, chat.chat);
		} else {
			await createNewChat(localStorage.token, chat);
		}
	}

	await chats.set(await getChatList(localStorage.token, 1));
};
