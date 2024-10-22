<script lang="ts">

	import { onMount, getContext } from 'svelte';

	import { WEBUI_NAME } from '$lib/stores';
	import { toast } from 'svelte-sonner';
	import { copyToClipboard , formatDateTime } from '$lib/utils';

	import { snapshotStore } from '$lib/stores'

	import { getListSnapshots } from '$lib/apis/autoptic'; 

	import IDSelector from '$lib/components/chat/AutopticComponents/IDSelector.svelte';

	import DeleteSnapModal from '$lib/components/storybooks/Modals/DeleteSnapModal.svelte';
	import FormatSelector from '../chat/AutopticComponents/FormatSelector.svelte';
	import { goto } from '$app/navigation';

	const i18n = getContext('i18n');

	let selectedPQLId = 'Any'; // DON'T make this a real empty string.
	const autoptic_prefix = 'http://localhost:9999/'

	let _snapshots = [];

	let defaultSnapshots = async () => {
		await getListSnapshots('jere-test', 'aws-api-usage', 'html', '2024');
	};

	let filteredSnapshots = [];

	export let selectedPeriod = '1m' ;
	let sortOrder = 'desc';

	let search = '';

	function selectPeriod(period) {
		selectedPeriod = period;
	}

	function toggleSortOrder() {
		sortOrder = sortOrder === 'asc' ? 'desc' : 'asc';
	}

	const openReadSnapshot = (snapshot) => {
		snapshotStore.set(snapshot);
		goto('/storybooks/snapshots/read');
	};

	let showDeleteModal = false;

	let snapshotData = null

	let openDeleteModal = (snapshot) => {
		showDeleteModal = true;
		snapshotData = snapshot;
	};

	export let refreshSnapshots = async () => {
		await defaultSnapshots();
	};

	const getFilterDate = () => {
		const now = new Date();
        let filterDate;
        switch (selectedPeriod) {
            case '1h':
                filterDate = new Date(now.getTime() - 1 * 60 * 60 * 1000); // 1 hour ago
                break;
            case '1d':
                filterDate = new Date(now.getTime() - 24 * 60 * 60 * 1000); // 1 day ago
                break;
			case '1w':
				filterDate = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000); // 1 week ago
				break;
            case '1m':
                filterDate = new Date(now.setMonth(now.getMonth() - 1)); // 1 month ago
                break;
            case '1y':
                filterDate = new Date(now.setFullYear(now.getFullYear() - 1)); // 1 year ago
                break;
            case 'All':
            default:
                filterDate = null;
                break;
        }
        return filterDate;
    };

	let selectedFormat = 'Any'

	const applyFilters = () => {
		filteredSnapshots = _snapshots.filter((m) => {

			const matchesEndpointID = m.pql_id == selectedPQLId;
			const matchesFormat = m.format == selectedFormat.toLowerCase();
			return matchesEndpointID && matchesFormat;
			
    		});

		};

	// const applyFilters = () => {

	// 	filteredSnapshots = _snapshots.slice().sort((a, b) => {
	// 		return sortOrder === 'asc'
	// 		? new Date(a.timestamp) - new Date(b.timestamp) // Ascending order
	// 		: new Date(b.timestamp) - new Date(a.timestamp); // Descending order
	// 	});

	// 	filteredSnapshots = filteredSnapshots.filter((m) => {
	// 		// Text search filter
	// 		const matchesSearch = search === '' ||
	// 			Object.keys(m).filter((key) => ['name', 'snapshot_id', 'body', 'tags'].includes(key))
	// 				.some((key) => m[key] && m[key].toString().toLowerCase().includes(search.toLowerCase()));
			
	// 		// Date range filter
	// 		const filterDate = getFilterDate();
	// 		const matchesDate = filterDate ? new Date(m.timestamp) >= filterDate : true;
	// 		const matchesEndpointID = m.endpoint_id == selectedPQLId;

	// 		if (selectedFormat === 'Any') {
	// 			return matchesSearch && matchesDate && matchesEndpointID;
	// 		} else {
	// 			const matchesFormat = m.format == selectedFormat;
	// 			return matchesSearch && matchesDate && matchesEndpointID && matchesFormat;
	// 		}
    // 		});
	// 	};


	// Apply filters whenever search value changes using reactive statement
	
	let endpoint_id = 'jere-test';
	let timestamp = '2024';

	onMount( async () => {
		await getListSnapshots('jere-test', 'aws-api-usage', 'html', '2024');
	})

	$: applyFilters(endpoint_id, selectedPQLId, selectedFormat.toLowerCase(), timestamp); 

</script>

<svelte:head>
	<title>
		{$i18n.t('Snapshots')} | {$WEBUI_NAME}
	</title>
</svelte:head>

<div class=" text-lg font-semibold mb-3">{$i18n.t('Snapshots')}</div>

<div class=" flex w-full space-x-2">
	<div class="flex flex-1">
		<div class=" self-center ml-1 mr-3">
			<svg
				xmlns="http://www.w3.org/2000/svg"
				viewBox="0 0 20 20"
				fill="currentColor"
				class="w-4 h-4"
			>
				<path
					fill-rule="evenodd"
					d="M9 3.5a5.5 5.5 0 100 11 5.5 5.5 0 000-11zM2 9a7 7 0 1112.452 4.391l3.328 3.329a.75.75 0 11-1.06 1.06l-3.329-3.328A7 7 0 012 9z"
					clip-rule="evenodd"
				/>
			</svg>
		</div>

		<input
			class=" w-full  text-sm pr-4 py-1 rounded-r-xl outline-none bg-transparent"
			bind:value={search}
			placeholder={$i18n.t('Search your snapshots')
						}
		/>
	</div>

</div>

<hr class=" dark:border-gray-850 my-2.5" />

<div class=" flex w-full space-x-2">
	
	<div class=" flex justify space-x-4 w-full mb-2 px-2 py-1" >

		<!-- toggle for endpoint ID -->
		<div class="w-fixed flex justify-center items-center min-w-fit rounded-lg p-1.5 px-3 
			bg-gray-50 dark:bg-gray-850 transition cursor-pointer dark:hover:bg-gray-700 hover:bg-black/5 "
			style="width: 765px;">
			<IDSelector
				bind:value={selectedPQLId}
				placeholder={`Selected PQL: ${selectedPQLId}`}
				on:select={(event) => selectedPQLId = event.detail.value}
			/>
		</div>

		<div 
			class="w-fixed flex justify-center items-center min-w-fit rounded-lg p-1.5 px-3 
			bg-gray-50 dark:bg-gray-850 transition cursor-pointer dark:hover:bg-gray-700 hover:bg-black/5"
			style="width: 220px;"
		>
			<FormatSelector
				bind:value={selectedFormat}
				placeholder={`Selected format: ${selectedFormat}`}
				on:select={(event) => selectedFormat = event.detail.value}
			/>
		</div>
		
	</div>

	<div class="border-l dark:border-gray-850 mx-4"></div>

	<div class="flex flex-1">

		<!-- svelte-ignore a11y-missing-attribute -->
		<a class=" flex justify-end space-x-4 w-full mb-2 px-2 py-1" >

			<div 
				class="w-40 flex justify-center items-center min-w-fit rounded-lg p-1.5 px-3 
				bg-gray-50 dark:bg-gray-850 transition cursor-pointer dark:hover:bg-gray-700 hover:bg-black/5"
				on:click={() => {toggleSortOrder()}}
			>
				<span class="text-center">{sortOrder === 'asc' ? 'Sort by Newest' : 'Sort by Oldest'}</span>
			</div>

			<div 
				class="w-12 flex justify-center items-center min-w-fit rounded-lg p-1.5 px-3 
					bg-gray-50 dark:bg-gray-850 transition cursor-pointer dark:hover:bg-gray-700 hover:bg-black/5"
				class:selected={selectedPeriod === '1y'}
				on:click={() => {selectPeriod('1y')}}
			>
				<span class="text-center">1y</span>
			</div>



			<div 
				class="w-12 flex justify-center items-center min-w-fit rounded-lg p-1.5 px-3 
					bg-gray-50 dark:bg-gray-850 transition cursor-pointer dark:hover:bg-gray-700 hover:bg-black/5"
				class:selected={selectedPeriod === '1m'}
				on:click={() => {selectPeriod('1m')}}
			>
				<span class="text-center">1m</span>
			</div>

			<div 
				class="w-12 flex justify-center items-center min-w-fit rounded-lg p-1.5 px-3 
					bg-gray-50 dark:bg-gray-850 transition cursor-pointer dark:hover:bg-gray-700 hover:bg-black/5"
				class:selected={selectedPeriod === '1w'}
				on:click={() => {selectPeriod('1w')}}
			>
				<span class="text-center">1w</span>
			</div>

			<div 
				class="w-12 flex justify-center items-center min-w-fit rounded-lg p-1.5 px-3 
					bg-gray-50 dark:bg-gray-850 transition cursor-pointer dark:hover:bg-gray-700 hover:bg-black/5"
				class:selected={selectedPeriod === '1d'}
				on:click={() => {selectPeriod('1d')}}
			>
				<span class="text-center">1d</span>
			</div>

			<div 
				class="w-12 flex justify-center items-center min-w-fit rounded-lg p-1.5 px-3 
			bg-gray-50 dark:bg-gray-850 transition cursor-pointer dark:hover:bg-gray-700 hover:bg-black/5"
				class:selected={selectedPeriod === '1h'}
				on:click={() => {selectPeriod('1h')}
							}
			>
				<span class="text-center">1h</span>
			</div>

			<!-- <div 
				class="w-10 flex justify-center items-center min-w-fit rounded-lg p-1.5 px-3 
					bg-gray-50 dark:bg-gray-850 transition cursor-pointer dark:hover:bg-gray-700 hover:bg-black/5"
				class:selected={selectedPeriod === 'All'}
				on:click={() => {selectPeriod('All')}}
			>
				<span class="text-center">All</span>
			</div>
		-->
		
		</a>
	</div>

</div>

<div class=" my-2 mb-5" id="snapshot-list">
	<!-- {#each _models.filter((m) => search === '' ||
		m.name && m.name.toLowerCase().includes(search.toLowerCase()) ||
		m.id && m.id.toString().toLowerCase().includes(search.toLowerCase()) ||
		m.body && m.body.toLowerCase().includes(search.toLowerCase())) as model} -->
	{#each filteredSnapshots as snapshot}
		<div
			class=" flex space-x-4 cursor-pointer w-full px-3 py-2 dark:hover:bg-white/5 hover:bg-black/5 rounded-xl"
			id="snapshot-item-{snapshot.snapshot_id}"
		>

			<!-- First description -->
			<a
				class=" flex flex-1 space-x-3.5 cursor-pointer w-full"
				href={`/?snapshots=${encodeURIComponent(snapshot.snapshot_id)}`}
			>
				<div class=" self-start w-8 pt-0.5">
					<div
						class=" rounded-full bg-stone-700 "
					>
						<img
							src={snapshot?.info?.meta?.profile_image_url ?? '/autoptic.png'}
							alt="snapshotfile profile"
							class=" rounded-full w-full h-auto object-cover bg-white dark:bg-white"
						/>
					</div>
				</div>

				<div
					class=" flex-1 self-center {snapshot?.info?.meta?.hidden ?? false ? 'text-gray-500' : ''}"
				>
					<div class="  font-bold line-clamp-1">{'hello'}</div>
					<div class=" text-xs overflow-hidden text-ellipsis line-clamp-1">
						{!!snapshot?.info?.meta?.description ? snapshot?.info?.meta?.description : snapshot.snapshot_id}
					</div>
				</div>
			</a>
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
				<div class="text-sm text-gray-600">{formatDateTime(snapshot.timestamp)}</div>
			</div>

			<!-- Vertical Divider -->
			<div class="border-l border-gray-300 mx-4"></div>

			<!-- Buttons -->
			<div class=" flex gap-2 self-center">

				<button	
				class="self-center w-fit text-sm px-2 py-2 dark:text-gray-300 dark:hover:text-white hover:bg-black/5 dark:hover:bg-white/5 rounded-xl"
					on:click={ () => {openReadSnapshot(snapshot);
							  		  }}
					>
					<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-clipboard-data" viewBox="0 0 16 16">
						<path d="M4 11a1 1 0 1 1 2 0v1a1 1 0 1 1-2 0zm6-4a1 1 0 1 1 2 0v5a1 1 0 1 1-2 0zM7 9a1 1 0 0 1 2 0v3a1 1 0 1 1-2 0z"/>
						<path d="M4 1.5H3a2 2 0 0 0-2 2V14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V3.5a2 2 0 0 0-2-2h-1v1h1a1 1 0 0 1 1 1V14a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V3.5a1 1 0 0 1 1-1h1z"/>
						<path d="M9.5 1a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5h-3a.5.5 0 0 1-.5-.5v-1a.5.5 0 0 1 .5-.5zm-3-1A1.5 1.5 0 0 0 5 1.5v1A1.5 1.5 0 0 0 6.5 4h3A1.5 1.5 0 0 0 11 2.5v-1A1.5 1.5 0 0 0 9.5 0z"/>
					  </svg>
				</button>

				<button
					class="self-center w-fit text-sm px-2 py-2 dark:text-gray-300 dark:hover:text-white hover:bg-black/5 dark:hover:bg-white/5 rounded-xl"
					on:click={ () => {copyToClipboard(autoptic_prefix+snapshot.url);
					toast.success($i18n.t('Snapshot URL copied.'));}
						}
					>
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-copy" viewBox="0 0 16 16">
                        <path fill-rule="evenodd" d="M4 2a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2zm2-1a1 1 0 0 0-1 1v8a1 1 0 0 0 1 1h8a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1zM2 5a1 1 0 0 0-1 1v8a1 1 0 0 0 1 1h8a1 1 0 0 0 1-1v-1h1v1a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h1v1z"/>
                    </svg>
                </button>

				<button
					class="self-center w-fit text-sm px-2 py-2 dark:text-gray-300 dark:hover:text-white hover:bg-black/5 dark:hover:bg-white/5 rounded-xl"
					on:click={ () => {openDeleteModal(snapshot);
							  		  }}
					>
					<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash3" viewBox="0 0 16 16">
						<path d="M6.5 1h3a.5.5 0 0 1 .5.5v1H6v-1a.5.5 0 0 1 .5-.5M11 2.5v-1A1.5 1.5 0 0 0 9.5 0h-3A1.5 1.5 0 0 0 5 1.5v1H1.5a.5.5 0 0 0 0 1h.538l.853 10.66A2 2 0 0 0 4.885 16h6.23a2 2 0 0 0 1.994-1.84l.853-10.66h.538a.5.5 0 0 0 0-1zm1.958 1-.846 10.58a1 1 0 0 1-.997.92h-6.23a1 1 0 0 1-.997-.92L3.042 3.5zm-7.487 1a.5.5 0 0 1 .528.47l.5 8.5a.5.5 0 0 1-.998.06L5 5.03a.5.5 0 0 1 .47-.53Zm5.058 0a.5.5 0 0 1 .47.53l-.5 8.5a.5.5 0 1 1-.998-.06l.5-8.5a.5.5 0 0 1 .528-.47M8 4.5a.5.5 0 0 1 .5.5v8.5a.5.5 0 0 1-1 0V5a.5.5 0 0 1 .5-.5"/>
					</svg>
				</button>

			</div>
		</div>
	{/each}
</div>

<hr class=" dark:border-gray-850" />

<div class=" my-10 ">
	<div class=" text-lg font-semibold mb-3 text-right">{$i18n.t('Made by Renaiss')}</div>
</div>

<DeleteSnapModal bind:showDelete={showDeleteModal} snapshot={snapshotData} onRefresh={refreshSnapshots} />

<style>
	/* Use the same hover colors for the selected state */
	.selected {
		background-color: rgba(164, 164, 164, 0.417)		; 
	}
	.dark .selected {
		background-color: rgba(31, 41, 55, 1); /* Same as dark:hover:bg-gray-700/5 */
	}
</style>