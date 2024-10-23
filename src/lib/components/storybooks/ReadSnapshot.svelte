<script lang="ts">

	import { onMount, getContext } from 'svelte';
	import { WEBUI_NAME } from '$lib/stores';
	import { toast } from 'svelte-sonner';
	import { copyToClipboard, formatDateTime } from '$lib/utils';
    import { snapshotStore } from '$lib/stores';
    import { readSnapshot } from '$lib/apis/autoptic';

	const i18n = getContext('i18n');
    const autoptic_prefix = 'http://localhost:9999/'

    export let snapshot_id; 

    let snapshot;
    let snapshotDate;
    let html_to_render;


    // Subscribe to the store to get the snapshot
    snapshotStore.subscribe(value => {
        snapshot = value;
    });
    
    snapshotDate = formatDateTime(snapshot.timestamp)


    onMount( async () => {

        html_to_render = await readSnapshot(snapshot.endpoint_id, snapshot.pql_id, snapshot.format, snapshot.timestamp, snapshot.snapshot_id)

        const iframe = document.getElementById('iframe');
        if (iframe) {
            // Inject the HTML content using srcdoc
            iframe.srcdoc = html_to_render;

            // Add an event listener to adjust height after the content is loaded
            iframe.onload = () => {
                // Get the content height of the iframe (from its body)
                const iframeDocument = iframe.contentDocument || iframe.contentWindow.document;
                const iframeBody = iframeDocument.body;
                const contentHeight = iframeBody.scrollHeight;

                // Add extra height (e.g., 50px more)
                const extraHeight = 20

                // Set the iframe height dynamically
                iframe.style.height = contentHeight + extraHeight + 'px';

                // Adjust parent container if needed
                const container = document.getElementById('iframe-container');
                if (container) {
                    container.style.height = contentHeight + 'px';
                }
            };
        }

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
id="snapshot-item-{snapshot.snapshot_id}"
>

    <!-- First description -->
    <div
        class=" flex flex-1 space-x-3.5 w-full"
    >
        <div class=" self-start w-8 pt-0.5">
            <div
                class=" rounded-full bg-stone-700 "
            >
                <img
                    src={'/autoptic.png'}
                    alt="snapshotfile profile"
                    class=" rounded-full w-full h-auto object-cover bg-white dark:bg-white"
                />
            </div>
        </div>

        <div
            class=" flex-1 self-center "
        >
            <div class="  font-bold line-clamp-1">{'hello'}</div>
            <div class=" text-xs overflow-hidden text-ellipsis line-clamp-1">
                {snapshot.snapshot_id}
            </div>
        </div>
    </div>
    <!-- Vertical Divider -->
    <div class="border-l border-gray-300 mx-4"></div>

    <!-- New section with creation date and tags -->
    <div class="flex-1 flex flex-col justify-center">
        <div class="text-sm text-gray-600">{snapshot.pql_id}</div>
    </div>

    <!-- Vertical Divider -->
    <div class="border-l border-gray-300 mx-4"></div>

    <!-- New section with creation date and tags -->
    <div class="flex-1 flex flex-col justify-center">
        <div class="text-sm text-gray-600">{snapshotDate}</div>
    </div>

    <!-- Vertical Divider -->
    <div class="border-l border-gray-300 "></div>

    <!-- Buttons -->
    <div class=" flex self-center">

        <button
            class="self-center text-sm px-2 py-2 dark:text-gray-300 dark:hover:text-white hover:bg-black/5 dark:hover:bg-white/5 rounded-xl"
            on:click={ () => {copyToClipboard(autoptic_prefix+snapshot.url);
            toast.success($i18n.t('Snapshot URL copied.'));}
                }
            >
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-copy" viewBox="0 0 16 16">
                <path fill-rule="evenodd" d="M4 2a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2zm2-1a1 1 0 0 0-1 1v8a1 1 0 0 0 1 1h8a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1zM2 5a1 1 0 0 0-1 1v8a1 1 0 0 0 1 1h8a1 1 0 0 0 1-1v-1h1v1a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h1v1z"/>
            </svg>
        </button>

    </div>
</div>

<div id="iframe-container" class="w-full h-full">
    <iframe
        id="iframe"
        title="snapshot"
        frameborder="0"
        class="w-full h-full"
        allowfullscreen
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