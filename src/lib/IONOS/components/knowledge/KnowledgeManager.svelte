<script lang="ts">
	import type { Readable } from 'svelte/store';
	import type { I18Next } from '$lib/IONOS/i18next.d.ts';
	import type {
		Knowledge,
		KnowledgeId,
	} from '$lib/apis/knowledge/types';
	import { getContext, onMount } from 'svelte';
	import Fuse from 'fuse.js';
	import { knowledge, mobile } from '$lib/stores';
	import { getKnowledgeBaseList } from '$lib/apis/knowledge';
	import { WEBUI_NAME } from '$lib/stores';
	import { knowledgeManager, showKnowlegeManager } from '$lib/IONOS/stores/dialogs';
	import LoadingCover from '$lib/IONOS/components/common/LoadingCover.svelte';
	import MagnifyingGlass from '$lib/IONOS/components/icons/MagnifyingGlass.svelte';
	import Dialog from '$lib/IONOS/components/common/Dialog.svelte';
	import Button, { ButtonType } from '$lib/IONOS/components/common/Button.svelte';
	import KnowledgeList from './KnowledgeList.svelte';
	import EditKnowledge from './EditKnowledge.svelte';
	import CreateKnowledge from './CreateKnowledge.svelte';
	import DialogHeader from '$lib/IONOS/components/common/DialogHeader.svelte';

	const i18n = getContext<Readable<I18Next>>('i18n');

	let loaded = false;

	let query = '';
	let fuse: Fuse<Knowledge>|null = null;

	let knowledgeBases: Knowledge[] = [];
	let filteredItems: Knowledge[] = [];
	let knowledgeBeingEdited:Knowledge|null = null;
	let create = false;

	$: if (knowledgeBases) {
		fuse = new Fuse(knowledgeBases, {
			keys: ['name', 'description']
		});
	}

	$: if (fuse) {
		filteredItems = query
			? fuse.search(query).map((e) => {
					return e.item;
				})
			: knowledgeBases;
	}

	function select({ detail: knowledgeId }: { detail: KnowledgeId }): void {
		knowledgeBeingEdited = knowledgeBases.find(({ id }) => id == knowledgeId) ?? null;
	}

	async function load() {
		loaded = false;
		knowledgeBases = await getKnowledgeBaseList(localStorage.token);
		loaded = true;
	}

	async function onKnowledgeDeleted(): Promise<void> {
		await load();
		knowledgeBeingEdited = null;
		console.log('knowledgeBeingEdited = null');
	}

	async function onEditClose(): Promise<void> {
		await load();
		console.log('edit close');
		console.log('knowledgeBeingEdited = null');
		knowledgeBeingEdited = null;
	}

	async function onKnowledgeCreated(): Promise<void> {
		await load();
		create = false;
	}

	function onCloseManager() {
		// @ts-expect-error Argument of type 'Knowledge[]' is not assignable to parameter of type 'Document[]'.
		knowledge.set(knowledgeBases);
		create = false;
	}

	onMount(async () => {
		load();
	});
</script>

<svelte:head>
	<title>
		{$i18n.t('Knowledge', { ns: 'ionos' })} | {$WEBUI_NAME}
	</title>
</svelte:head>

<Dialog
	dialogId="knowledge-manager"
	show={$knowledgeManager}
	on:close={() => { showKnowlegeManager(false); } }
	class="p-0 md:min-h-[300px] h-screen w-screen md:max-h-[436px] md:min-w-[750px] md:max-w-[800px] {$knowledgeManager ? 'max-md:translate-x-0' : 'max-md:translate-x-[100dvw]'}"
>
	<DialogHeader
		slot="header"
		title={$i18n.t("Knowledge Management", { ns: 'ionos' })}
		on:close={() => { showKnowlegeManager(false); }}
		dialogId="knowledge-manager"
		class="p-[30px] shrink-0 basis-auto border-b border-gray-200 overflow-x-scroll"
		submenu={$mobile ? true : false}
	/>

	<div slot="content" class="p-5 h-full flex flex-col flex-1 basis-0 min-h-0">
		{#if loaded}
			<div class="flex pb-5 gap-2.5 border-gray-200 border-b md:min-w-[500px]">
				<div class="flex grow rounded-lg p-3 text-sm bg-gray-100 outline-hidden text-blue-800 placeholder:text-gray-400">
					<div class="self-center ml-1 mr-3">
						<MagnifyingGlass />
					</div>
					<input
						class="w-full"
						bind:value={query}
						placeholder={$i18n.t('Search Knowledge', { ns: 'ionos' })}
					/>
				</div>
				<div class="hidden md:block self-center">
					<Button
						on:click={() => create = true}
						type={ButtonType.secondary}
					>
						{$i18n.t('Create knowledge base', { ns: 'ionos' })}
					</Button>
				</div>
			</div>
			<div class="md:max-h-[190px] flex-1 min-h-[0] overflow-y-scroll" >
				<KnowledgeList
					items={filteredItems}
					on:select={select}
				/>
			</div>
			<div class="hidden md:block text-gray-400 text-xs py-5 border-t border-gray-200">
				ⓘ {$i18n.t("Use '#' in the prompt input to load and include your knowledge.", { ns: 'ionos' })}
			</div>
			<div class="md:hidden block mt-5">
				<Button
					on:click={() => create = true}
					type={ButtonType.secondary}
					className="w-full"
				>
					{$i18n.t('Create knowledge base', { ns: 'ionos' })}
				</Button>
			</div>
		{:else}
			<LoadingCover />
		{/if}
	</div>
</Dialog>

<EditKnowledge
	show={!!knowledgeBeingEdited}
	knowledge={knowledgeBeingEdited ?? {}}
	on:deleted={onKnowledgeDeleted}
	on:close={onEditClose}
	submenu={$mobile ? true : false}
/>

<CreateKnowledge
	show={!!create}
	on:created={onKnowledgeCreated}
	on:close={onCloseManager}
	submenu={$mobile ? true : false}
/>
