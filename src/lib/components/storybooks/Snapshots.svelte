<script lang="ts">
	import { toast } from 'svelte-sonner';
	import Sortable from 'sortablejs';

	import fileSaver from 'file-saver';
	const { saveAs } = fileSaver;

	import { onMount, getContext, setContext } from 'svelte';

	import { WEBUI_NAME, mobile, models, settings, user } from '$lib/stores';

	import { deleteModel } from '$lib/apis/ollama';
	import { goto } from '$app/navigation';

	import { getModels } from '$lib/apis';

	import EllipsisHorizontal from '../icons/EllipsisHorizontal.svelte';
	import ModelMenu from './Models/ModelMenu.svelte';

	const i18n = getContext('i18n');


	export let selectedPeriod = 'All' ;

	let sortable = null;
	let search = '';

	onMount(async () => {
		let selectedPeriod = 'All' ;
	});

	function selectPeriod(period) {
		selectedPeriod = period;
	}

	// $: filteredChatList = $chats.filter((chat) => {
	// 	if (search === '') {
	// 		return true;
	// 	} else {
	// 		let title = chat.title.toLowerCase();
	// 		const query = search.toLowerCase();

	// 		let contentMatches = false;
	// 		// Access the messages within chat.chat.messages
	// 		if (chat.chat && chat.chat.messages && Array.isArray(chat.chat.messages)) {
	// 			contentMatches = chat.chat.messages.some((message) => {
	// 				// Check if message.content exists and includes the search query
	// 				return message.content && message.content.toLowerCase().includes(query);
	// 			});
	// 		}

	// 		return title.includes(query) || contentMatches;
	// 	}
	// });

	// casos separados:

	// 	$: filteredChatList = $chats.filter((chat) => {
	// if (search === '') {
	// 	return true;
	// } else {
	// 	const searchTerms = search.toLowerCase().split(' '); // Split search string by spaces
	// 	let title = chat.title.toLowerCase();

	// 	let contentMatches = false;
	// 	if (chat.chat && chat.chat.messages && Array.isArray(chat.chat.messages)) {
	// 	contentMatches = chat.chat.messages.some((message) => {
	// 		if (message.content) {
	// 		// Check if any search term matches the message content
	// 		return searchTerms.some(term => message.content.toLowerCase().includes(term));
	// 		}
	// 	});
	// 	}

	// 	// Return true if any search term matches the title or content
	// 	return searchTerms.some(term => title.includes(term)) || contentMatches;
	// }
	// });

  // Helper function to determine if the chat is within the time range
//   const isWithinTimeRange = (chatDate) => {
//     const now = new Date();
//     const chatTime = new Date(chatDate); // Assuming chat has a date property

//     switch (selectedPeriod) {
//       case '1d':
//         return chatTime >= new Date(now.setDate(now.getDate() - 1));
//       case '1w':
//         return chatTime >= new Date(now.setDate(now.getDate() - 7));
//       case '1m':
//         return chatTime >= new Date(now.setMonth(now.getMonth() - 1));
//       case '1y':
//         return chatTime >= new Date(now.setFullYear(now.getFullYear() - 1));
//       default:
//         return true; // If selectedPeriod is 'all', return all chats
//     }
//   };

//   // Filtered chat list based on search and selectedPeriod
//   $: filteredChatList = $chats.filter((chat) => {
//     // Apply search filter
//     const searchTerms = search.toLowerCase().split(' ');
//     let title = chat.title.toLowerCase();

//     let contentMatches = false;
//     if (chat.chat && chat.chat.messages && Array.isArray(chat.chat.messages)) {
//       contentMatches = chat.chat.messages.some((message) => {
//         if (message.content) {
//           return searchTerms.some(term => message.content.toLowerCase().includes(term));
//         }
//       });
//     }

//     const searchMatches = searchTerms.some(term => title.includes(term)) || contentMatches;

//     // Apply time range filter
//     const timeRangeMatches = isWithinTimeRange(chat.date); // Assuming `chat.date` is the date of the chat

//     return searchMatches && timeRangeMatches;
//   });


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
			class=" w-full text-sm pr-4 py-1 rounded-r-xl outline-none bg-transparent"
			bind:value={search}
			placeholder={$i18n.t('Search your snapshots')

						}
		/>
	</div>

<!-- <input
	class="w-full rounded-r-xl py-1.5 pl-2.5 pr-4 text-sm bg-transparent dark:text-gray-300 outline-none"
	placeholder={$i18n.t('Search')}
	bind:value={search}
	on:focus={() => {
		enrichChatsWithContent($chats);
	}}
/> -->

	<div>
		<a
			class=" px-2 py-2 rounded-xl border border-gray-200 dark:border-gray-600 dark:border-0 hover:bg-gray-100 dark:bg-gray-800 dark:hover:bg-gray-700 transition font-medium text-sm flex items-center space-x-1"
		>
			<svg
				xmlns="http://www.w3.org/2000/svg"
				viewBox="0 0 16 16"
				fill="currentColor"
				class="w-4 h-4"
			>
				<path
					d="M8.75 3.75a.75.75 0 0 0-1.5 0v3.5h-3.5a.75.75 0 0 0 0 1.5h3.5v3.5a.75.75 0 0 0 1.5 0v-3.5h3.5a.75.75 0 0 0 0-1.5h-3.5v-3.5Z"
				/>
			</svg>
		</a>
	</div>
</div>

<hr class=" dark:border-gray-850 my-2.5" />

<div class=" flex w-full space-x-2">
	<div class="flex flex-1">
		<a class=" flex justify-end space-x-4 w-full mb-2 px-2 py-1" >

			<div class=" self-center w-10 ">
				<div 
					class="button-wrapper flex items-center justify-center dark:hover:bg-gray-900 hover:bg-black/5 bg-transparent dark:bg-gray-700 border border-gray-200 cursor-pointer"
					class:selected={selectedPeriod === '1h'}
					on:click={() => selectPeriod('1h')}
				>
					<span class="text-center">1h</span>
				</div>
			</div>
		
			<div class=" self-center w-10">
				<div 
					class="button-wrapper flex items-center justify-center dark:hover:bg-gray-900 hover:bg-black/5 bg-transparent dark:bg-gray-700 border border-gray-200 cursor-pointer"
					class:selected={selectedPeriod === '1d'}
					on:click={() => selectPeriod('1d')}
				>
					<span class="text-center">1d</span>
				</div>
			</div>
		
			<div class=" self-center w-10">
				<div 
					class="button-wrapper flex items-center justify-center dark:hover:bg-gray-900 hover:bg-black/5 bg-transparent dark:bg-gray-700 border border-gray-200 cursor-pointer"
					class:selected={selectedPeriod === '1w'}
					on:click={() => selectPeriod('1w')}
				>
					<span class="text-center">1w</span>
				</div>
			</div>
		
			<div class=" self-center w-10">
				<div 
					class="button-wrapper flex items-center justify-center dark:hover:bg-gray-900 hover:bg-black/5 bg-transparent dark:bg-gray-700 border border-gray-200 cursor-pointer"
					class:selected={selectedPeriod === '1m'}
					on:click={() => selectPeriod('1m')}
				>
					<span class="text-center">1m</span>
				</div>
			</div>
		
			<div class=" self-center w-10">
				<div 
					class="button-wrapper flex items-center justify-center dark:hover:bg-gray-900 hover:bg-black/5 bg-transparent dark:bg-gray-700 border border-gray-200 cursor-pointer"
					class:selected={selectedPeriod === '1y'}
					on:click={() => selectPeriod('1y')}
				>
					<span class="text-center">1y</span>
				</div>
			</div>
		
			<div class=" self-center w-10 ">
				<div 
					class="button-wrapper flex items-center justify-center dark:hover:bg-gray-900 hover:bg-black/5 bg-transparent dark:bg-gray-700 border border-gray-200 cursor-pointer"
					class:selected={selectedPeriod === 'All'}
					on:click={() => selectPeriod('All')}
				>
					<span class="text-center">All</span>
				</div>
			</div>
		
		</a>
	</div>

</div>
	
<div class=" flex w-full space-x-2">
	<span class=" flex space-x-4 w-full mb-2 px-2 py-1" >Testing</span>
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