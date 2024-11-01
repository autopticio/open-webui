<script lang="ts">
	import { DropdownMenu } from 'bits-ui';

	import { flyAndScale } from '$lib/utils/transitions';
	import { onMount, getContext, tick } from 'svelte';

	import CustomChevronDown from '$lib/components/icons/CustomChevronDown.svelte';
	import Check from '$lib/components/icons/Check.svelte';
	import Search from '$lib/components/icons/Search.svelte';


	import { getListPQL } from '$lib/apis/autoptic'; 

	import { mobile } from '$lib/stores';

	const i18n = getContext('i18n');

	export let value = '';
	export let placeholder = 'Select a your ID';
	export let searchEnabled = true;
	export let searchPlaceholder = $i18n.t('Search your PQL function');
	export let width = '100%';
	export let className = 'w-160';


	let show = false;

	let searchValue = '';

	let items = [];

	let selectedModel = '';

	onMount(async () => {
		items = await getListPQL();
	});

	$: filteredItems = items.length > 0
		? ['Any',...items.filter((item) =>
				(searchValue
					? item.toLowerCase().includes(searchValue.toLowerCase())
					: true) 
		  )]
		: [];

	$: selectedModel = items.find((item) => item === value) ?? '';

</script>

<DropdownMenu.Root bind:open={show} >
	<DropdownMenu.Trigger 
		class="w-full" 
		aria-label={placeholder}
		>		
			<div
				class="flex w-full justify-between px-0.5 outline-none bg-transparent text-lg font-semibold placeholder-gray-400 focus:outline-none"
			>
				{placeholder}
				
				<CustomChevronDown className=" self-center ml-2 size-3" strokeWidth="2.5" />
			</div>
	</DropdownMenu.Trigger>

	<DropdownMenu.Content
		class=" w-fixed overflow-x-hidden justify-center rounded-xl bg-white dark:bg-gray-850 dark:text-white shadow-lg border border-gray-300/30 dark:border-gray-850/50  outline-none "
	style="width: 350px"
	transition={flyAndScale}
	side={$mobile ? 'bottom' : 'bottom-start'}
	align="start"
	sideOffset={10}
	>
		<slot>
			<!-- element for the search -->
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

			<div class="hidden w-[42rem]" />
			<div class="hidden w-[32rem]" />
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
