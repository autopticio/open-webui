<script lang="ts">
	import { DropdownMenu } from 'bits-ui';

	import { flyAndScale } from '$lib/utils/transitions';
	import { getContext , createEventDispatcher } from 'svelte';

	import CustomChevronDown from '$lib/components/icons/CustomChevronDown.svelte';
	import Check from '$lib/components/icons/Check.svelte';

	import { mobile } from '$lib/stores';

	const i18n = getContext('i18n');
	const dispatch = createEventDispatcher();

	export let value = '';
	export let placeholder = '';

    let items = ['1','2','3','4','5','6','7','8','9','10']

	export let className = 'w-60';

	let showFormat = false;

	const selectItem = (item: string) => {
		dispatch('select', { value: item });
		showFormat = false;  // Close the dropdown
	};

</script>

<DropdownMenu.Root
	bind:open={showFormat}
>
	<DropdownMenu.Trigger 
		class="w-fixed" 
		aria-label={placeholder} 
		style="width: 220px;">
			<div
				class="flex w-full justify-between px-0.5 outline-none bg-transparent text-lg font-semibold placeholder-gray-400 focus:outline-none"
			>
				{placeholder}
				<CustomChevronDown className=" self-center ml-2 size-3" strokeWidth="2.5" />
			</div>
	</DropdownMenu.Trigger>

	<DropdownMenu.Content
		class=" w-fixed overflow-x-hidden justify-center rounded-xl bg-white dark:bg-gray-850 dark:text-white shadow-lg border border-gray-300/30 dark:border-gray-850/50  outline-none "
		style="width: 244px;"
		transition={flyAndScale}
		side={$mobile ? 'bottom' : 'bottom-center'}
		sideOffset={10}
	>
		<slot>

			<!-- toggle list -->
			<div class="px-3 my-2 max-h-64 overflow-y-auto scrollbar-hidden">
				{#each items as item}
					<button
						aria-label="model-item"
						class="flex w-full text-left font-medium line-clamp-1 select-none items-center rounded-button py-2 pl-3 pr-1.5 text-sm text-gray-700 dark:text-gray-100 outline-none transition-all duration-75 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg cursor-pointer data-[highlighted]:bg-muted"
						on:click={() => selectItem(item)}
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
