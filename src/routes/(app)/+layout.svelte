<script lang="ts">
	import { toast } from 'svelte-sonner';
	import { onMount, tick, getContext } from 'svelte';
	import { openDB, deleteDB } from 'idb';
	import fileSaver from 'file-saver';
	const { saveAs } = fileSaver;
	import mermaid from 'mermaid';

	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import { fade } from 'svelte/transition';
	import { getChatList } from '$lib/apis/chats';
	import { getKnowledgeBases } from '$lib/apis/knowledge';
	import { getFunctions } from '$lib/apis/functions';
	import { getModels, getToolServersData, getVersionUpdates } from '$lib/apis';
	import { getAllTags } from '$lib/apis/chats';
	import { getPrompts } from '$lib/apis/prompts';
	import { getTools } from '$lib/apis/tools';
	import { getBanners } from '$lib/apis/configs';
	import { getUserSettings } from '$lib/apis/users';

	import { WEBUI_VERSION } from '$lib/constants';
	import { compareVersion } from '$lib/utils';
	import { hasStoredState } from '$lib/IONOS/services/startup';
	import { hasChats } from '$lib/IONOS/services/chats';
	import { init as initAgentsStore } from '$lib/IONOS/stores/agents';

	import {
		config,
		user,
		settings,
		models,
		prompts,
		knowledge,
		tools,
		functions,
		tags,
		banners,
		showSettings,
		showChangelog,
		temporaryChatEnabled,
		toolServers
	} from '$lib/stores';
	import { notifications } from '$lib/IONOS/stores/notifications';

	import NotificationManager from '$lib/IONOS/components/notifications/NotificationManager.svelte';
	import SettingsOverlay from '$lib/IONOS/components/settings/Settings.svelte';
	import ChangelogModal from '$lib/components/ChangelogModal.svelte';
	import AccountPending from '$lib/IONOS/components/AccountPending.svelte';
	import UpdateInfoToast from '$lib/components/layout/UpdateInfoToast.svelte';
	import { get } from 'svelte/store';
	import Spinner from '$lib/components/common/Spinner.svelte';
	import KnowledgeManager from '$lib/IONOS/components/knowledge/KnowledgeManager.svelte';

	const i18n = getContext('i18n');

	let loaded = false;
	let DB = null;
	let localDBChats = [];

	let version;

	onMount(async () => {

	});

	const checkForVersionUpdates = async () => {
		version = await getVersionUpdates(localStorage.token).catch((error) => {
			return {
				current: WEBUI_VERSION,
				latest: WEBUI_VERSION
			};
		});
	};
</script>

<KnowledgeManager />
<SettingsOverlay bind:show={$showSettings} />
<ChangelogModal bind:show={$showChangelog} />

<div class="app relative">
	<div
		class=" text-gray-700 dark:text-gray-100 bg-white dark:bg-gray-900 overflow-auto flex flex-row justify-end"
	>

		<div class="block">
				<slot />
		</div>
	</div>
</div>

<style>
	.loading {
		display: inline-block;
		clip-path: inset(0 1ch 0 0);
		animation: l 1s steps(3) infinite;
		letter-spacing: -0.5px;
	}

	@keyframes l {
		to {
			clip-path: inset(0 -1ch 0 0);
		}
	}

	pre[class*='language-'] {
		position: relative;
		overflow: auto;

		/* make space  */
		margin: 5px 0;
		padding: 1.75rem 0 1.75rem 1rem;
		border-radius: 10px;
	}

	pre[class*='language-'] button {
		position: absolute;
		top: 5px;
		right: 5px;

		font-size: 0.9rem;
		padding: 0.15rem;
		background-color: #828282;

		border: ridge 1px #7b7b7c;
		border-radius: 5px;
		text-shadow: #c4c4c4 0 0 2px;
	}

	pre[class*='language-'] button:hover {
		cursor: pointer;
		background-color: #bcbabb;
	}
</style>
