<script lang="ts">

	import { onMount, getContext } from 'svelte';

	import { WEBUI_NAME } from '$lib/stores';

	import IDSelector from '$lib/components/chat/AutopticComponents/IDSelector.svelte';

	const i18n = getContext('i18n');

	let selectedModelId = '';
	let _models = [
		{endpoint_id: 'pirate', id: "The man who would be the Pirate King" , name: "Monkey D. Luffy" ,body:"Testing",creation_date: '2024-09-30T12:00:00Z'},
		{endpoint_id: 'pirate', id: "snapshot id" , name:'example', tags: ['ec2'], creation_date: '2024-08-15T08:30:00Z', body:'My name is Monkey D. Luffy, and I am gonna be the next Pirate King'},
		{endpoint_id: 'monk', id: "snapshot id 2" , name:'Aang', tags: ['ec2','ecs'], creation_date: '1997-09-30T12:00:00Z', body:'At least, Roger laugh.'},
		{endpoint_id: 'monk', id: "snapshot id 3" , name:'Tenzin', tags: ['ec2','lambda'], creation_date: '2024-10-04T12:50:00Z', body:'At least, Roger laugh.'},
	];

	let filteredModels = [];

	export let selectedPeriod = 'All' ;

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

	let sortOrder = 'desc';

	const applyFilters = () => {

		filteredModels = _models.slice().sort((a, b) => {
			return sortOrder === 'asc'
			? new Date(a.creation_date) - new Date(b.creation_date) // Ascending order
			: new Date(b.creation_date) - new Date(a.creation_date); // Descending order
		});

		filteredModels = filteredModels.filter((m) => {
			// Text search filter
			const matchesSearch = search === '' ||
				Object.keys(m).filter((key) => ['name', 'id', 'body', 'tags'].includes(key))
					.some((key) => m[key] && m[key].toString().toLowerCase().includes(search.toLowerCase()));
			
			// Date range filter
			const filterDate = getFilterDate();
			const matchesDate = filterDate ? new Date(m.creation_date) >= filterDate : true;
			const matchesEndpointID = m.endpoint_id == selectedModelId;

			// Return true if both conditions are met
			return matchesSearch && matchesDate && matchesEndpointID;
			
    		});
		};

	// Apply filters whenever search value changes using reactive statement
	$: applyFilters(search,selectedPeriod,selectedModelId,sortOrder); 

</script>

<svelte:head>
	<title>
		{$i18n.t('PQLs')} | {$WEBUI_NAME}
	</title>
</svelte:head>

<div class=" text-lg font-semibold mb-3">{$i18n.t('PQLs')}</div>


<div class=" text-lg font-semibold mb-3">{$i18n.t('Coming soon!')}</div>

<hr class=" dark:border-gray-850" />

<div class=" my-10 ">
	<div class=" text-lg font-semibold mb-3 text-right flex items-center justify-end">{$i18n.t('Made by Renaiss')}
		<img src={"/renaiss.png"} alt="renaiss_logo" class="ml-2 h-6 w-6" />
	</div>
</div>

<style>
	/* Use the same hover colors for the selected state */
	.selected {
		background-color: rgba(164, 164, 164, 0.417)		; 
	}
	.dark .selected {
		background-color: rgba(55, 65, 81, 0.05); /* Same as dark:hover:bg-gray-700/5 */
	}
</style>