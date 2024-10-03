<script lang="ts">

	import { onMount, getContext } from 'svelte';

	import { WEBUI_NAME, models } from '$lib/stores';

	import IDSelector from '$lib/components/chat/AutopticComponents/IDSelector.svelte';

	const i18n = getContext('i18n');

	let selectedModelId = '';
	let _models = [
		{endpoint_id: 'pirate', id: "The man who would be the Pirate King" , name: "Monkey D. Luffy" ,body:"Testing",creation_date: '2024-09-30T12:00:00Z'},
		{endpoint_id: 'pirate', id: "snapshot id" , name:'example', tags: ['ec2'], creation_date: '2024-08-15T08:30:00Z', body:'My name is Monkey D. Luffy, and I am gonna be the next Pirate King'},
		{endpoint_id: 'monk', id: "snapshot id 2" , name:'example 2', tags: ['ec2','ecs'], creation_date: '1997-09-30T12:00:00Z', body:'At least, Roger laugh.'},
	];

	let filteredModels = [];

	export let selectedPeriod = 'All' ;

	let sortable = null;
	let search = '';

	onMount(async () => {
		let selectedPeriod = '1h' ;
	});

	function selectPeriod(period) {
		selectedPeriod = period;
	}


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

	const applyFilters = () => {
		filteredModels = _models.filter((m) => {
			// Text search filter
			const matchesSearch = search === '' ||
				Object.keys(m).filter((key) => ['name', 'id', 'body', 'tags'].includes(key))
					.some((key) => m[key] && m[key].toString().toLowerCase().includes(search.toLowerCase()));
			
			// Date range filter
			const filterDate = getFilterDate();
			const matchesDate = filterDate ? new Date(m.creation_date) >= filterDate : true;
			// const matchesEndpointID =

			// Return true if both conditions are met
			return matchesSearch && matchesDate;
    		});
		};

	// Apply filters whenever search value changes using reactive statement
	$: applyFilters(search,selectedPeriod,selectedModelId); 

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
		<IDSelector
			placeholder={$i18n.t('Select your ID')}
			items={$models.map((model) => ({
				value: model.id,
				label: model.name,
				model: model
			}))}
			bind:value={selectedModelId}
		/>
	</div>

</div>

<hr class=" dark:border-gray-850 my-2.5" />

<div class=" flex w-full space-x-2">
	<div class="flex flex-1">
		<!-- svelte-ignore a11y-missing-attribute -->
		<a class=" flex justify-end space-x-4 w-full mb-2 px-2 py-1" >
<!-- 
			{#each ['1h', '1d', '1m', '1y', 'All'] as period}
				<div class="self-center w-10">
					<div
						class={`button-wrapper flex items-center justify-center cursor-pointer bg-transparent dark:bg-gray-700 border border-gray-200 
							${selectedPeriod === period ? 'bg-gray-200 dark:bg-gray-900 text-white' : 'hover:bg-black/5 dark:hover:bg-gray-900 text-black'}`}
						on:click={() => selectPeriod(period)}
					>
						<span class="text-center">{period}</span>
					</div>
				</div>
			{/each} -->

			<div class=" self-center w-10 ">
				<div 
					class="button-wrapper flex items-center justify-center dark:hover:bg-gray-900 hover:bg-black/5 bg-transparent dark:bg-gray-700 border border-gray-200 cursor-pointer"
					class:selected={selectedPeriod === '1h'}
					on:click={() => {selectPeriod('1h')}
								}
				>
					<span class="text-center">1h</span>
				</div>
			</div>
		
			<div class=" self-center w-10">
				<div 
					class="button-wrapper flex items-center justify-center dark:hover:bg-gray-900 hover:bg-black/5 bg-transparent dark:bg-gray-700 border border-gray-200 cursor-pointer"
					class:selected={selectedPeriod === '1d'}
					on:click={() => {selectPeriod('1d')}}
				>
					<span class="text-center">1d</span>
				</div>
			</div>
		
			<div class=" self-center w-10">
				<div 
					class="button-wrapper flex items-center justify-center dark:hover:bg-gray-900 hover:bg-black/5 bg-transparent dark:bg-gray-700 border border-gray-200 cursor-pointer"
					class:selected={selectedPeriod === '1w'}
					on:click={() => {selectPeriod('1w')}}
				>
					<span class="text-center">1w</span>
				</div>
			</div>
		
			<div class=" self-center w-10">
				<div 
					class="button-wrapper flex items-center justify-center dark:hover:bg-gray-900 hover:bg-black/5 bg-transparent dark:bg-gray-700 border border-gray-200 cursor-pointer"
					class:selected={selectedPeriod === '1m'}
					on:click={() => {selectPeriod('1m')}}
				>
					<span class="text-center">1m</span>
				</div>
			</div>
		
			<div class=" self-center w-10">
				<div 
					class="button-wrapper flex items-center justify-center dark:hover:bg-gray-900 hover:bg-black/5 bg-transparent dark:bg-gray-700 border border-gray-200 cursor-pointer"
					class:selected={selectedPeriod === '1y'}
					on:click={() => {selectPeriod('1y')}}
				>
					<span class="text-center">1y</span>
				</div>
			</div>
			<div class=" self-center w-10 ">
				<div 
					class="button-wrapper flex items-center justify-center dark:hover:bg-gray-900 hover:bg-black/5 bg-transparent dark:bg-gray-700 border border-gray-200 cursor-pointer"
					class:selected={selectedPeriod === 'All'}
					on:click={() => {selectPeriod('All')}}
				>
					<span class="text-center">All</span>
				</div>
			</div>
		
		</a>
	</div>

</div>
	
<div class=" my-2 mb-5" id="model-list">
	<!-- {#each _models.filter((m) => search === '' ||
		m.name && m.name.toLowerCase().includes(search.toLowerCase()) ||
		m.id && m.id.toString().toLowerCase().includes(search.toLowerCase()) ||
		m.body && m.body.toLowerCase().includes(search.toLowerCase())) as model} -->
	{#each filteredModels as model}
		<div
			class=" flex space-x-4 cursor-pointer w-full px-3 py-2 dark:hover:bg-white/5 hover:bg-black/5 rounded-xl"
			id="model-item-{model.id}"
		>

			<!-- First description -->
			<a
				class=" flex flex-1 space-x-3.5 cursor-pointer w-full"
				href={`/?models=${encodeURIComponent(model.id)}`}
			>
				<div class=" self-start w-8 pt-0.5">
					<div
						class=" rounded-full bg-stone-700 "
					>
						<img
							src={model?.info?.meta?.profile_image_url ?? '/favicon.png'}
							alt="modelfile profile"
							class=" rounded-full w-full h-auto object-cover"
						/>
					</div>
				</div>

				<div
					class=" flex-1 self-center {model?.info?.meta?.hidden ?? false ? 'text-gray-500' : ''}"
				>
					<div class="  font-bold line-clamp-1">{model.name}</div>
					<div class=" text-xs overflow-hidden text-ellipsis line-clamp-1">
						{!!model?.info?.meta?.description ? model?.info?.meta?.description : model.id}
					</div>
				</div>
			</a>
			<!-- Vertical Divider -->
			<div class="border-l border-gray-300 mx-4"></div>
			
			<!-- New section with creation date and tags -->
			<div class="flex-1 flex flex-col justify-center">
				<div class="text-sm text-gray-600">{model.creation_date}</div>
				<!-- <div class="text-xs text-gray-500">
					{model.tags?.join(', ') ?? 'No tags available'}
				</div> -->
			</div>
			<!-- Vertical Divider -->
			<div class="border-l border-gray-300 mx-4"></div>

			<!-- Buttons -->
			<div class=" flex flex-row gap-0.5 self-center">
				<a
					class="self-center w-fit text-sm px-2 py-2 dark:text-gray-300 dark:hover:text-white hover:bg-black/5 dark:hover:bg-white/5 rounded-xl"
					type="button"
					on:click={null}
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

<style>
	/* Use the same hover colors for the selected state */
	.selected {
		background-color: rgba(0, 0, 0, 0.05); /* Same as hover:bg-black/5 */
	}
	.dark .selected {
		background-color: rgba(55, 65, 81, 0.05); /* Same as dark:hover:bg-gray-700/5 */
	}
</style>