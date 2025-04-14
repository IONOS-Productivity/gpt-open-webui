import { getImportOrigin } from '$lib/utils';
import type {
	ChatExport,
} from '$lib/apis/chats/types';

export const isIonosGptCompatible = (data: any): boolean => {
	if (!Array.isArray(data)) {
		return false;
	}

	if (data.length === 0) {
		return true;
	}

	// TODO check for model IDs too

	return getImportOrigin(data) === 'webui';
};

export const parseChatExportData = (contentsStr: string): ChatExport[] => {
	let imported: any|null = null;

	try {
		imported = JSON.parse(contentsStr);
	} catch(e) {
		throw new Error(`Format error while parsing the file: ${e.toString()}`);
	}

	if (!isIonosGptCompatible(imported)) {
		throw new Error(`The file is not IONOS GPT compatible`);
	}

	return imported as unknown as ChatExport[];
};
