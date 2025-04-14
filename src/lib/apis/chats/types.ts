// Derived from /api/v1/chats/?page=1

export type ChatId = string;
export type UnixTimestamp = number;

export type Chat = {
    id: string;
	title: string;
	updated_at: UnixTimestamp;
	created_at: UnixTimestamp;
};

export type ChatExport = {
    id: ChatId;
    chat: Chat;
	title: string;
	updated_at: UnixTimestamp;
	created_at: UnixTimestamp;
};
