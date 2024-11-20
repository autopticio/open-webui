<script lang="ts">

	import { onMount, getContext } from 'svelte';
	import { WEBUI_NAME } from '$lib/stores';
	import { toast } from 'svelte-sonner';
	import { copyToClipboard, formatDateTime } from '$lib/utils';
    import { readSnapshot } from '$lib/apis/autoptic';

	const i18n = getContext('i18n');

    export let pql_id: string; 
    export let format: string;
    export let timestamp: string;
    export let snapshot_id: string;
    export let url;

    let isLoading = false
    let snapshotDate;
    let html_to_render;
    
    snapshotDate = formatDateTime(timestamp)

    async function loadSnapshot() {
        isLoading = true;        

        html_to_render = await readSnapshot(pql_id, format, timestamp, snapshot_id)

        const iframe = document.getElementById('iframe');
        if (iframe) {
            iframe.srcdoc = html_to_render;
            iframe.style.backgroundColor = 'white';
            iframe.style.borderRadius = '20px';     
            iframe.style.overflow = 'hidden';

            iframe.onload = () => {

                const iframeDocument = iframe.contentDocument || iframe.contentWindow.document;
                const iframeBody = iframeDocument.body;

                const contentHeight = iframeBody.scrollHeight;

                const extraHeight = 20

                iframe.style.height = contentHeight + extraHeight + 'px';

                const container = document.getElementById('iframe-container');
                if (container) {
                    container.style.height = contentHeight + 'px';
                }
            };
        }

        isLoading = false;
    }

    onMount( async () => {
        await loadSnapshot()
    });

</script>

<svelte:head>
	<title>
		{$i18n.t('Snapshots')} | {$WEBUI_NAME}
	</title>
</svelte:head>

<div class=" text-lg  font-semibold mb-3">{$i18n.t(`Snapshot ${snapshot_id}`)}</div>

<div
class=" flex space-x-4 w-full px-3 py-2 dark:bg-white/5 rounded-xl"
id="snapshot-item-{snapshot_id}"
>

    <!-- First description -->
    <div
        class=" flex flex-1 space-x-3.5 w-full"
    >

        <div
            class=" flex-1 self-center "
        >
            <div class=" font-bold line-clamp-1">{snapshotDate}</div>
        </div>
    </div>
    <!-- Vertical Divider -->
    <div class="border-l border-gray-300 mx-4"></div>

    <!-- New section with creation date and tags -->
    <div class="flex-1 flex flex-col justify-center">
        <div class="text-m ">{pql_id}</div>
    </div>

    <!-- Vertical Divider -->
    <div class="border-l border-gray-300 mx-4"></div>

    <!-- New section with creation date and tags -->
    <div class="flex-1 flex flex-col justify-center">
        <div class="text-sm text-gray-600">{snapshot_id}</div>
    </div>

    <!-- Vertical Divider -->
    <div class="border-l border-gray-300 "></div>

    <!-- Buttons -->
    <div class=" flex self-center">

        <button
            class="self-center text-sm px-2 py-2 dark:text-gray-300 dark:hover:text-white hover:bg-black/5 dark:hover:bg-white/5 rounded-xl"
            on:click={ () => {copyToClipboard(url);
            toast.success($i18n.t('Snapshot URL copied.'));}
                }
            >
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-copy" viewBox="0 0 16 16">
                <path fill-rule="evenodd" d="M4 2a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2zm2-1a1 1 0 0 0-1 1v8a1 1 0 0 0 1 1h8a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1zM2 5a1 1 0 0 0-1 1v8a1 1 0 0 0 1 1h8a1 1 0 0 0 1-1v-1h1v1a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h1v1z"/>
            </svg>
        </button>

    </div>
</div>

<div class=" my-2 mb-5">
    {#if isLoading}
        <div class="flex text-center items-center justify-center h-[48px]">
            <div class="flex items-center justify-center space-x-2">
                <svg xmlns="http://www.w3.org/2000/svg" class="animate-spin h-10 w-10" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354v4.352M12 15.294v4.352M6.343 6.343l3.07 3.071M14.587 14.587l3.071 3.07M4.354 12H8.706M15.294 12h4.352"/>
                </svg>
                <div class=" flex items-center justify-center text-lg font-semibold ">Loading snapshot, please wait...</div>
            </div>
        </div>
    {/if}    
</div>

<div id="iframe-container" class="w-full h-full">
    <iframe
        id="iframe"
        title="snapshot"
        frameborder="0"
        class="w-full h-full"
        allowfullscreen
        scrolling="no"
    />
</div>

<style>
	/* Use the same hover colors for the selected state */
	.selected {
		background-color: rgba(164, 164, 164, 0.417)		; 
	}
	.dark .selected {
		background-color: rgba(31, 41, 55, 1); /* Same as dark:hover:bg-gray-700/5 */
	}
</style>