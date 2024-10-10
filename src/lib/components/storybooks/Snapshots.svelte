<script lang="ts">

	import { onMount, getContext } from 'svelte';

	import { WEBUI_NAME } from '$lib/stores';

	import IDSelector from '$lib/components/chat/AutopticComponents/IDSelector.svelte';

	import ReadSnapModal from './Modals/ReadSnapModal.svelte';
	import DeleteSnapModal from '$lib/components/storybooks/Modals/DeleteSnapModal.svelte';
	import FormatSelector from '../chat/AutopticComponents/FormatSelector.svelte';

	const i18n = getContext('i18n');

	let selectedSnapshotId = '';
	let _snapshots = [
		{endpoint_id: 'pirate', id: "The man who would be the Pirate King" , format: 'JSON',  name: "Monkey D. Luffy" ,body:"Testing",creation_date: '2024-09-30T12:00:00Z'},
		{endpoint_id: 'pirate', id: "snapshot id" , format: 'HTML' , name:'example', tags: ['ec2'], creation_date: '2024-08-15T08:30:00Z', body:'My name is Monkey D. Luffy, and I am gonna be the next Pirate King'},
		{endpoint_id: 'monk', id: "snapshot id 2" , format: 'HTML' , name:'Aang', tags: ['ec2','ecs'], creation_date: '1997-09-30T12:00:00Z', body:'At least, Roger laugh.'},
		{endpoint_id: 'monk', id: "snapshot id 3" , format: 'JSON' , name:'Tenzin', tags: ['ec2','lambda'], creation_date: '2024-10-04T12:50:00Z', body:'At least, Roger laugh.',content:`<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title>Generic HTML Page</title>
    <link rel="stylesheet" href="styles.css"> <!-- Link to external stylesheet -->
    <style>
        /* Example internal CSS */
        body {
            font-family: Arial, sans-serif;
            background-color: #f0f0f0;
            margin: 0;
            padding: 20px;
        }
        h1 {
            color: #333;
        }
    </style>
</head>
<body>

    <header>
        <h1>Welcome to My Website</h1>
        <nav>
            <ul>
                <li><a href="#home">Home</a></li>
                <li><a href="#about">About</a></li>
                <li><a href="#contact">Contact</a></li>
            </ul>
        </nav>
    </header>

    <main>
        <section id="home">
            <h2>Home Section</h2>
            <p>This is a generic homepage section. You can add your own content here.</p>
        </section>

        <section id="about">
            <h2>About Section</h2>
            <p>This is where you can describe yourself or your website.</p>
        </section>

        <section id="contact">
            <h2>Contact Section</h2>
            <p>Feel free to reach out!</p>
        </section>
    </main>

    <footer>
        <p>&copy; 2024 Your Website. All rights reserved.</p>
    </footer>

</body>
</html>
`},
	];

	let filteredSnapshots = [];

	export let selectedPeriod = 'All' ;
	let sortOrder = 'desc';

	let search = '';

	function selectPeriod(period) {
		selectedPeriod = period;
	}

	function toggleSortOrder() {
		sortOrder = sortOrder === 'asc' ? 'desc' : 'asc';
	}

	let showReadModal = false;

	const openReadModal = () => {
		showReadModal = true;
	};

	let showDeleteModal = false;

	const openDeleteModal = () => {
		showDeleteModal = true;
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

		filteredSnapshots = _snapshots.slice().sort((a, b) => {
			return sortOrder === 'asc'
			? new Date(a.creation_date) - new Date(b.creation_date) // Ascending order
			: new Date(b.creation_date) - new Date(a.creation_date); // Descending order
		});

		filteredSnapshots = filteredSnapshots.filter((m) => {
			// Text search filter
			const matchesSearch = search === '' ||
				Object.keys(m).filter((key) => ['name', 'id', 'body', 'tags'].includes(key))
					.some((key) => m[key] && m[key].toString().toLowerCase().includes(search.toLowerCase()));
			
			// Date range filter
			const filterDate = getFilterDate();
			const matchesDate = filterDate ? new Date(m.creation_date) >= filterDate : true;
			const matchesEndpointID = m.endpoint_id == selectedSnapshotId;

			if (selectedFormat === 'Any') {
				return matchesSearch && matchesDate && matchesEndpointID;
			} else {
				const matchesFormat = m.format == selectedFormat;
				return matchesSearch && matchesDate && matchesEndpointID && matchesFormat;
			}
    		});
		};

	// Apply filters whenever search value changes using reactive statement
	$: applyFilters(search,selectedPeriod,selectedSnapshotId,sortOrder,selectedFormat); 


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
	
	<!-- botton cross class -->
	<!-- px-2 py-2 rounded-xl border border-gray-200 dark:border-gray-600 dark:border-0 hover:bg-gray-100 dark:bg-gray-800 dark:hover:bg-gray-700 transition font-medium text-sm flex items-center space-x-1 -->

	<!-- toggle for endpoint ID -->
	<div class="flex gap-2 ">
		<!-- <IDSelector
			placeholder={$i18n.t('Select your ID')}
			items={$models.map((model) => ({
				value: model.id,
				label: model.name,
				model: model
			}))}
			bind:value={selectedModelId}
		/> -->
		<IDSelector
			placeholder={$i18n.t('Select your ID')}
			bind:value={selectedSnapshotId}
		/>
	</div>

</div>

<hr class=" dark:border-gray-850 my-2.5" />

<div class=" flex w-full space-x-2">
	<div class="flex flex-1">

		<!-- svelte-ignore a11y-missing-attribute -->
		<a class=" flex justify-end space-x-4 w-full mb-2 px-2 py-1" >

			<div 
				class="w-50 flex justify-center items-center min-w-fit rounded-lg p-1.5 px-3 
				bg-gray-50 dark:bg-gray-850 transition cursor-pointer dark:hover:bg-gray-700 hover:bg-black/5"
			>
					<FormatSelector
					bind:value={selectedFormat}
					placeholder={`Selected format: ${selectedFormat}`}
				/>
			</div>

			<div 
				class="w-40 flex justify-center items-center min-w-fit rounded-lg p-1.5 px-3 
				bg-gray-50 dark:bg-gray-850 transition cursor-pointer dark:hover:bg-gray-700 hover:bg-black/5"
				on:click={() => {toggleSortOrder()}}
			>
				<span class="text-center">{sortOrder === 'asc' ? 'Sort by Newest' : 'Sort by Oldest'}</span>
			</div>

			<div 
				class="w-10 flex justify-center items-center min-w-fit rounded-lg p-1.5 px-3 
			bg-gray-50 dark:bg-gray-850 transition cursor-pointer dark:hover:bg-gray-700 hover:bg-black/5"
				class:selected={selectedPeriod === '1h'}
				on:click={() => {selectPeriod('1h')}
							}
			>
				<span class="text-center">1h</span>
			</div>
		
			<div 
				class="w-10 flex justify-center items-center min-w-fit rounded-lg p-1.5 px-3 
					bg-gray-50 dark:bg-gray-850 transition cursor-pointer dark:hover:bg-gray-700 hover:bg-black/5"
				class:selected={selectedPeriod === '1d'}
				on:click={() => {selectPeriod('1d')}}
			>
				<span class="text-center">1d</span>
			</div>
		
			<div 
				class="w-10 flex justify-center items-center min-w-fit rounded-lg p-1.5 px-3 
					bg-gray-50 dark:bg-gray-850 transition cursor-pointer dark:hover:bg-gray-700 hover:bg-black/5"
				class:selected={selectedPeriod === '1w'}
				on:click={() => {selectPeriod('1w')}}
			>
				<span class="text-center">1w</span>
			</div>

			<div 
				class="w-10 flex justify-center items-center min-w-fit rounded-lg p-1.5 px-3 
					bg-gray-50 dark:bg-gray-850 transition cursor-pointer dark:hover:bg-gray-700 hover:bg-black/5"
				class:selected={selectedPeriod === '1m'}
				on:click={() => {selectPeriod('1m')}}
			>
				<span class="text-center">1m</span>
			</div>
		
			<div 
				class="w-10 flex justify-center items-center min-w-fit rounded-lg p-1.5 px-3 
					bg-gray-50 dark:bg-gray-850 transition cursor-pointer dark:hover:bg-gray-700 hover:bg-black/5"
				class:selected={selectedPeriod === '1y'}
				on:click={() => {selectPeriod('1y')}}
			>
				<span class="text-center">1y</span>
			</div>

			<div 
				class="w-10 flex justify-center items-center min-w-fit rounded-lg p-1.5 px-3 
					bg-gray-50 dark:bg-gray-850 transition cursor-pointer dark:hover:bg-gray-700 hover:bg-black/5"
				class:selected={selectedPeriod === 'All'}
				on:click={() => {selectPeriod('All')}}
			>
				<span class="text-center">All</span>
			</div>
		
		</a>
	</div>

</div>

<!-- 		class="w-40 button-wrapper flex items-center justify-center dark:hover:bg-gray-900 hover:bg-black/5 
		bg-transparent dark:bg-gray-700 border border-gray-200 cursor-pointer" -->




<div class=" my-2 mb-5" id="snapshot-list">
	<!-- {#each _models.filter((m) => search === '' ||
		m.name && m.name.toLowerCase().includes(search.toLowerCase()) ||
		m.id && m.id.toString().toLowerCase().includes(search.toLowerCase()) ||
		m.body && m.body.toLowerCase().includes(search.toLowerCase())) as model} -->
	{#each filteredSnapshots as snapshot}
		<div
			class=" flex space-x-4 cursor-pointer w-full px-3 py-2 dark:hover:bg-white/5 hover:bg-black/5 rounded-xl"
			id="snapshot-item-{snapshot.id}"
		>

			<!-- First description -->
			<a
				class=" flex flex-1 space-x-3.5 cursor-pointer w-full"
				href={`/?snapshots=${encodeURIComponent(snapshot.id)}`}
			>
				<div class=" self-start w-8 pt-0.5">
					<div
						class=" rounded-full bg-stone-700 "
					>
						<img
							src={snapshot?.info?.meta?.profile_image_url ?? '/favicon.png'}
							alt="snapshotfile profile"
							class=" rounded-full w-full h-auto object-cover"
						/>
					</div>
				</div>

				<div
					class=" flex-1 self-center {snapshot?.info?.meta?.hidden ?? false ? 'text-gray-500' : ''}"
				>
					<div class="  font-bold line-clamp-1">{snapshot.name}</div>
					<div class=" text-xs overflow-hidden text-ellipsis line-clamp-1">
						{!!snapshot?.info?.meta?.description ? snapshot?.info?.meta?.description : snapshot.id}
					</div>
				</div>
			</a>
			<!-- Vertical Divider -->
			<div class="border-l border-gray-300 mx-4"></div>
			
			<!-- New section with creation date and tags -->
			<div class="flex-1 flex flex-col justify-center">
				<div class="text-sm text-gray-600">{snapshot.creation_date}</div>
				<!-- <div class="text-xs text-gray-500">
					{model.tags?.join(', ') ?? 'No tags available'}
				</div> -->
			</div>
			<!-- Vertical Divider -->
			<div class="border-l border-gray-300 mx-4"></div>

			<!-- Buttons -->
			<div class=" flex gap-2 self-center">

				<a
					class="self-center w-fit text-sm px-2 py-2 dark:text-gray-300 dark:hover:text-white hover:bg-black/5 dark:hover:bg-white/5 rounded-xl"
					type="button"
					on:click={ () => {openReadModal();
							  		  }}
					>
					<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-clipboard-data" viewBox="0 0 16 16">
						<path d="M4 11a1 1 0 1 1 2 0v1a1 1 0 1 1-2 0zm6-4a1 1 0 1 1 2 0v5a1 1 0 1 1-2 0zM7 9a1 1 0 0 1 2 0v3a1 1 0 1 1-2 0z"/>
						<path d="M4 1.5H3a2 2 0 0 0-2 2V14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V3.5a2 2 0 0 0-2-2h-1v1h1a1 1 0 0 1 1 1V14a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V3.5a1 1 0 0 1 1-1h1z"/>
						<path d="M9.5 1a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5h-3a.5.5 0 0 1-.5-.5v-1a.5.5 0 0 1 .5-.5zm-3-1A1.5 1.5 0 0 0 5 1.5v1A1.5 1.5 0 0 0 6.5 4h3A1.5 1.5 0 0 0 11 2.5v-1A1.5 1.5 0 0 0 9.5 0z"/>
					  </svg>
				</a>

				<a
					class="self-center w-fit text-sm px-2 py-2 dark:text-gray-300 dark:hover:text-white hover:bg-black/5 dark:hover:bg-white/5 rounded-xl"
					type="button"
					on:click={ () => {openDeleteModal();
							  		  }}
					>
					<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash3" viewBox="0 0 16 16">
						<path d="M6.5 1h3a.5.5 0 0 1 .5.5v1H6v-1a.5.5 0 0 1 .5-.5M11 2.5v-1A1.5 1.5 0 0 0 9.5 0h-3A1.5 1.5 0 0 0 5 1.5v1H1.5a.5.5 0 0 0 0 1h.538l.853 10.66A2 2 0 0 0 4.885 16h6.23a2 2 0 0 0 1.994-1.84l.853-10.66h.538a.5.5 0 0 0 0-1zm1.958 1-.846 10.58a1 1 0 0 1-.997.92h-6.23a1 1 0 0 1-.997-.92L3.042 3.5zm-7.487 1a.5.5 0 0 1 .528.47l.5 8.5a.5.5 0 0 1-.998.06L5 5.03a.5.5 0 0 1 .47-.53Zm5.058 0a.5.5 0 0 1 .47.53l-.5 8.5a.5.5 0 1 1-.998-.06l.5-8.5a.5.5 0 0 1 .528-.47M8 4.5a.5.5 0 0 1 .5.5v8.5a.5.5 0 0 1-1 0V5a.5.5 0 0 1 .5-.5"/>
					</svg>
				</a>
			</div>
		</div>
	{/each}
</div>

<hr class=" dark:border-gray-850" />

<div class=" my-10 ">
	<div class=" text-lg font-semibold mb-3 text-right">{$i18n.t('Made by Renaiss')}</div>
</div>

<DeleteSnapModal bind:showDelete={showDeleteModal} />
<ReadSnapModal bind:showRead={showReadModal} />

<style>
	/* Use the same hover colors for the selected state */
	.selected {
		background-color: rgba(164, 164, 164, 0.417)		; 
	}
	.dark .selected {
		background-color: rgba(31, 41, 55, 1); /* Same as dark:hover:bg-gray-700/5 */
	}
</style>