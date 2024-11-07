<script lang="ts">

	import { onMount, getContext } from 'svelte';

	import { WEBUI_NAME } from '$lib/stores';

	import { refreshTrigger } from '$lib/stores';

	import { toast } from 'svelte-sonner';
	import { copyToClipboard , formatDateTime } from '$lib/utils';

	import { getDefaultListSnapshots } from '$lib/apis/autoptic'; 

	import IDSelector from '$lib/components/chat/AutopticComponents/IDSelector.svelte';

	import DeleteSnapModal from '$lib/components/storybooks/Modals/DeleteSnapModal.svelte';
	import FormatSelector from '../chat/AutopticComponents/FormatSelector.svelte';
	import TimeSelector from '../chat/AutopticComponents/TimeSelector.svelte';
	import TimeUnitSelector from '../chat/AutopticComponents/TimeUnitSelector.svelte';

	import { goto } from '$app/navigation';

	const i18n = getContext('i18n');

	let selectedPQLId = 'Any'; // DON'T make this a real empty string.

	let _snapshots = [];
	let isLoading = false;

	let defaultSnapshots = async () => {
		isLoading = true;
		let window = selectedTime+selectedTimeUnit.toLowerCase()
		try {
			_snapshots = await getDefaultListSnapshots(window); 
		} catch (error) {
			_snapshots = []
		}
		isLoading = false;
	};

	let filteredSnapshots = [];

	let sortOrder = 'desc';

	let search = '';

	function toggleSortOrder() {
		sortOrder = sortOrder === 'asc' ? 'desc' : 'asc';
	}

	const openReadSnapshot = (snapshot) => {
		goto(`/storybooks/snapshots/${snapshot.endpoint_id}/${snapshot.pql_id}/${snapshot.format}/${snapshot.timestamp}/${snapshot.snapshot_id}`);
	};

	let showDeleteModal = false;

	let snapshotData = null

	let openDeleteModal = (snapshot) => {
		showDeleteModal = true;
		snapshotData = snapshot;
	};

	export let refreshSnapshots = async () => {
		await defaultSnapshots();
		applyFilters();
	};

	let selectedFormat = 'Any'

	let selectedTime = '1'
	let selectedTimeUnit = 'Days'

	const applyFilters = () => {

		filteredSnapshots = _snapshots.filter((m) => {

			let matchesFormat = true;
			let matchesPqlID = true;

			if (selectedFormat !== 'Any') {
				matchesFormat = m.format.toLowerCase() == selectedFormat.toLowerCase();
			}

			if (selectedPQLId !== 'Any') {
				matchesPqlID = m.pql_id == selectedPQLId;
			}

			return matchesPqlID && matchesFormat;
			
    		});

		filteredSnapshots = filteredSnapshots.sort((a, b) => {
			return sortOrder === 'asc' ?
			 a.timestamp.localeCompare(b.timestamp) :
			 b.timestamp.localeCompare(a.timestamp);
		});
	};

	onMount( async () => {
		await defaultSnapshots();
		applyFilters();
	})

	$: defaultSnapshots(selectedTime,selectedTimeUnit,localStorage.serverURL);
	$: applyFilters(sortOrder,_snapshots, selectedPQLId, selectedFormat);
	$: refreshTrigger.subscribe((shouldRefresh) => {
		if (shouldRefresh) {
			refreshSnapshots();
			refreshTrigger.set(false); 
		}
	});

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

<div class=" flex w-full space-x-2 overflow-x-auto whitespace-nowrap">
	
	<div class=" flex justify space-x-4 w-full mb-2 px-2 py-1" >

		<!-- toggle for endpoint ID -->
		<div class="flex-grow flex justify-center items-center min-w-fit rounded-lg p-1.5 px-3 
			bg-gray-50 dark:bg-gray-850 transition cursor-pointer dark:hover:bg-gray-700 hover:bg-black/5 "
			>
				<IDSelector
					placeholder={`Selected PQL: ${selectedPQLId}`}
					on:select={(event) => selectedPQLId = event.detail.value}
					bind:value={selectedPQLId}	
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
		
		<div 
			class="w-fixed flex justify-center items-center min-w-fit rounded-lg p-1.5 px-3 
			bg-gray-50 dark:bg-gray-850 transition cursor-pointer dark:hover:bg-gray-700 hover:bg-black/5"
			style="width: 220px;"
		>
		<TimeSelector
			bind:value={selectedTime}
			placeholder={selectedTime}
			on:select={(event) => selectedTime = event.detail.value}
		/>
		</div>

		<div 
			class="w-fixed flex justify-center items-center min-w-fit rounded-lg p-1.5 px-3 
			bg-gray-50 dark:bg-gray-850 transition cursor-pointer dark:hover:bg-gray-700 hover:bg-black/5"
			style="width: 220px;"
		>
		<TimeUnitSelector
			bind:value={selectedTimeUnit}
			placeholder={selectedTimeUnit}
			on:select={(event) => selectedTimeUnit = event.detail.value}
		/>
		</div>
		
		<div 
			class="w-fixed flex justify-center items-center min-w-fit rounded-lg p-1.5 px-3 
			bg-gray-50 font-semibold dark:bg-gray-850 transition cursor-pointer dark:hover:bg-gray-700 hover:bg-black/5"
			style="width: 220px;"
			on:click={() => {toggleSortOrder()}}
		>
			<span class="text-center">{sortOrder === 'asc' ? 'Sort by Newest' : 'Sort by Oldest'}</span>
		</div>

	</div>

</div>

<div class=" my-2 mb-5" id="snapshot-list">
	{#if isLoading}
		<div class="flex text-center items-center justify-center h-[48px]">
			<div class="flex items-center justify-center space-x-2">
				<svg xmlns="http://www.w3.org/2000/svg" class="animate-spin h-10 w-10" viewBox="0 0 24 24" fill="none" stroke="currentColor">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354v4.352M12 15.294v4.352M6.343 6.343l3.07 3.071M14.587 14.587l3.071 3.07M4.354 12H8.706M15.294 12h4.352"/>
				</svg>
				<div class=" flex items-center justify-center text-lg font-semibold ">Loading snapshots, please wait...</div>
			</div>
		</div>
	{:else}
		{#if filteredSnapshots.length === 0}
			<div class="flex text-center items-center justify-center h-[48px]">
				<div class=" flex items-center justify-center text-lg font-semibold ">No snapshots found.</div>
			</div>
		{:else}
			{#each filteredSnapshots as snapshot}
				<div
					class=" flex space-x-4 cursor-pointer w-full px-3 py-2 dark:hover:bg-white/5 hover:bg-black/5 rounded-xl"
					id="snapshot-item-{snapshot.snapshot_id}"
				>

					<!-- First description -->
					<div class="flex flex-1 space-x-3.5 w-full cursor-pointer">
					
						<!-- svelte-ignore a11y-click-events-have-key-events -->
						<!-- svelte-ignore a11y-no-static-element-interactions -->
						<div
							class="flex-1 self-center {snapshot?.info?.meta?.hidden ?? false ? 'text-gray-500' : 'text-blue-500 underline'}"
						>
							<div class="font-bold line-clamp-1"
								on:click={() => openReadSnapshot(snapshot)}
								>
								{formatDateTime(snapshot.timestamp)}
							</div>
						</div>
					</div>
					<!-- Vertical Divider -->
					<div class="border-l border-gray-300 mx-4"></div>
					
					<!-- New section with creation date and tags -->
					<div class="flex-1 flex flex-col justify-center">
						<div class="text-m">{snapshot.pql_id}</div>
					</div>

					<!-- Vertical Divider -->
					<div class="border-l border-gray-300 mx-4"></div>

					<!-- New section with creation date and tags -->
					<div class="flex-1 flex flex-col justify-center">
						<div class="text-sm text-gray-600">{snapshot.snapshot_id}</div>
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
							on:click={ () => {copyToClipboard(`${window.location.origin}/storybooks/snapshots/${snapshot.endpoint_id}/${snapshot.pql_id}/${snapshot.format}/${snapshot.timestamp}/${snapshot.snapshot_id}`);
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
		{/if}
	{/if}
</div>

<hr class=" dark:border-gray-850" />

<div class=" my-10 ">
	<div class=" text-lg font-semibold mb-3 text-right flex items-center justify-end">{$i18n.t('Made by Renaiss')}
		<img src={"/renaiss.png"} alt="renaiss_logo" class="ml-2 h-6 w-6" />
	</div>
</div>

<DeleteSnapModal 
	bind:showDelete={showDeleteModal}
	snapshot={snapshotData} 
	onRefresh={refreshSnapshots} />

<style>
	/* Use the same hover colors for the selected state */
	.selected {
		background-color: rgba(164, 164, 164, 0.417)		; 
	}
	.dark .selected {
		background-color: rgba(31, 41, 55, 1); /* Same as dark:hover:bg-gray-700/5 */
	}
</style>