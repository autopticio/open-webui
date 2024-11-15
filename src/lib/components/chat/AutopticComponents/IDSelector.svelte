<script lang="ts">
	import { DropdownMenu } from 'bits-ui';

	import { flyAndScale } from '$lib/utils/transitions';
	import { onMount, getContext, tick } from 'svelte';

	import CustomChevronDown from '$lib/components/icons/CustomChevronDown.svelte';
	import Check from '$lib/components/icons/Check.svelte';
	import Search from '$lib/components/icons/Search.svelte';


	import { getListPQL } from '$lib/apis/autoptic'; 

	import { mobile , refreshTrigger } from '$lib/stores';

	const i18n = getContext('i18n');

	export let value = '';
	export let placeholder = 'Select a your ID';
	export let searchEnabled = true;
	export let searchPlaceholder = $i18n.t('Search your PQL function');
	export let width = '100%';
	export let className = 'w-160';
	
	let show = false;
	let isLoading = false;

	let searchValue = '';

	let items = [];

	let selectedModel = '';
	let dropdownContentWidth = 'auto';

	async function resizeMenu() {

		tick().then(() => {
		
			const triggerElement = document.getElementById('selector') as HTMLElement;
			if (triggerElement) {
				const rect = triggerElement.getBoundingClientRect();
				dropdownContentWidth = `${rect.width}px`;
			}
		});
	}
	
	async function loadingPQLs() {
		items = []
		isLoading = true;
		if (localStorage.serverURL !== '' && localStorage.endpointID !== '') {
				items = await getListPQL();
		}
		isLoading = false;
	}

	async function initializeComponent() {
		await resizeMenu();
		await loadingPQLs()
	}

	onMount(() => {

		initializeComponent();

		window.addEventListener('resize', resizeMenu);

		return () => {
			window.removeEventListener('resize', resizeMenu);
		};
	
	});

	$: filteredItems = items.length > 0
		? ['Any',...items.filter((item) =>
				(searchValue
					? item.toLowerCase().includes(searchValue.toLowerCase())
					: true) 
		  )]
		: [];

	$: selectedModel = items.find((item) => item === value) ?? '';
	$: refreshTrigger.subscribe(async (shouldRefresh) => {
		if (shouldRefresh) {
			await loadingPQLs()
			refreshTrigger.set(false); 
		}
	});
	
</script>

<DropdownMenu.Root bind:open={show} >
	<DropdownMenu.Trigger 
		class="w-full" 
		aria-label={placeholder}
		id='selector'
		>		
		<div class="flex justify-center items-center min-w-fit rounded-lg p-1.5 px-3 
			bg-gray-50 dark:bg-gray-850 transition cursor-pointer dark:hover:bg-gray-700 hover:bg-black/5 "
			>
			<div
				class="flex-grow flex w-full justify-between px-0.5 outline-none bg-transparent text-lg font-semibold placeholder-gray-400 focus:outline-none"
			>
				{placeholder}
				
				<CustomChevronDown className=" self-center ml-2 size-3" strokeWidth="2.5" />
			</div>
		</div>

	</DropdownMenu.Trigger>

	<DropdownMenu.Content
		class=" w-fixed overflow-x-hidden justify-center rounded-xl bg-white dark:bg-gray-850 dark:text-white shadow-lg border border-gray-300/30 dark:border-gray-850/50  outline-none "
		style={`width: ${dropdownContentWidth}; min-width: 244px`}
		transition={flyAndScale}
		side={$mobile ? 'bottom' : 'bottom-start'}
		align="start"
		sideOffset={10}
	>
		<slot>
			<!-- element for the search -->
			{#if isLoading} 
				<div class="flex text-left items-left justify-center">
					<div class="flex items-center justify-left space-x-1">
						<svg xmlns="http://www.w3.org/2000/svg" class="animate-spin h-5 w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354v4.352M12 15.294v4.352M6.343 6.343l3.07 3.071M14.587 14.587l3.071 3.07M4.354 12H8.706M15.294 12h4.352"/>
						</svg>
						<div class="block py-2 text-sm text-gray-700 dark:text-gray-100">Loading PQLs, please wait...</div>
					</div>
				</div>
			{:else}
				{#if searchEnabled && filteredItems.length >0}
					<div class="flex items-center gap-2.5 px-5 mt-3.5 mb-3">	
						<Search className="size-4" strokeWidth="2.5" />

						<input
							id="model-search-input"
							bind:value={searchValue}
							class="w-full text-sm bg-transparent outline-none"
							placeholder={searchPlaceholder}
							autocomplete="off"
						/>
					</div>

					<hr class="border-gray-100 dark:border-gray-800" />
				{/if}

				<!-- toggle list -->
				<div class="px-3 my-2 max-h-64 overflow-y-auto scrollbar-hidden">
					{#each filteredItems as item}
						<button
							aria-label="model-item"
							class="flex w-full text-left font-medium line-clamp-1 select-none items-center rounded-button py-2 pl-3 pr-1.5 text-sm text-gray-700 dark:text-gray-100 outline-none transition-all duration-75 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg cursor-pointer data-[highlighted]:bg-muted"
							on:click={() => {
								value = item;
								resizeMenu()
								show = false;
							}}
						>
							<div class="flex flex-col">
								<div class="flex items-center gap-2">
									<div class="flex items-center min-w-fit">
										<div class="line-clamp-1">
											{item}
										</div>
									</div>

								</div>
							</div>

							{#if value === item}
								<div class="ml-auto pl-2">
									<Check />
								</div>
							{/if}
						</button>
					{:else}
						<div>
							<div class="block px-3 py-2 text-sm text-gray-700 dark:text-gray-100">
								{$i18n.t('There is no PQL found')}
							</div>
						</div>
					{/each}

				</div>
			{/if}
		</slot>
	</DropdownMenu.Content>
</DropdownMenu.Root>

<style>
	.scrollbar-hidden:active::-webkit-scrollbar-thumb,
	.scrollbar-hidden:focus::-webkit-scrollbar-thumb,
	.scrollbar-hidden:hover::-webkit-scrollbar-thumb {
		visibility: visible;
	}
	.scrollbar-hidden::-webkit-scrollbar-thumb {
		visibility: hidden;
	}
</style>
