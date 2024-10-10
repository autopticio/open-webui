<script lang="ts">

	import { getContext } from 'svelte';

	import Modal from '$lib/components/common/Modal.svelte';
    import { copyToClipboard } from '$lib/utils';

	const i18n = getContext('i18n');

	export let showRead = false;

	let readInput = 'https://autoptic.io/story/ep/{endpoint_id}/pql/{pql_id}/snap/{format}/{timestamp}/{snapshot_id}';

	$: if (!showRead) {
		readInput = '';
	}

</script>

<Modal size="m" bind:show={showRead}>
	<div>
		<div class=" flex justify-between dark:text-gray-300 px-5 pt-4 pb-1">
			<div class=" text-lg font-medium self-center">{$i18n.t('Share or read directly your snapshot!')}</div>
			<button
				class="self-center"
				on:click={() => {
					showRead = false;
				}}
			>
				<svg
					xmlns="http://www.w3.org/2000/svg"
					viewBox="0 0 20 20"
					fill="currentColor"
					class="w-5 h-5"
				>
					<path
						d="M6.28 5.22a.75.75 0 00-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 101.06 1.06L10 11.06l3.72 3.72a.75.75 0 101.06-1.06L11.06 10l3.72-3.72a.75.75 0 00-1.06-1.06L10 8.94 6.28 5.22z"
					/>
				</svg>
			</button>
		</div>

		<div class="flex flex-col w-full px-5 pb-4 dark:text-gray-200">
			<hr class=" dark:border-gray-850 my-2" />

			<div class=" flex flex-col w-full sm:flex-row sm:justify-center sm:space-x-6">
					<div class="text-left text-sm w-full mb-3">
						{$i18n.t('You can share this link with your corporation or just run it in a new tab')}
					</div>
			</div>

			<div class=" flex w-full space-x-2">
				<div class="flex flex-1 pl-1">
					<div
						class="dark:bg-gray-800 pl-2 italic-placeholder w-full text-sm pr-4 py-1 rounded outline-none bg-transparent"
                    >
                        {readInput}
                    </div>	
				</div>

				<button
					class="self-center w-fit text-sm px-2 py-2 dark:text-gray-300 dark:hover:text-white hover:bg-black/5 dark:hover:bg-white/5 rounded-xl"
					on:click={ () => {copyToClipboard(readInput)}}
					>
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-copy" viewBox="0 0 16 16">
                        <path fill-rule="evenodd" d="M4 2a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2zm2-1a1 1 0 0 0-1 1v8a1 1 0 0 0 1 1h8a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1zM2 5a1 1 0 0 0-1 1v8a1 1 0 0 0 1 1h8a1 1 0 0 0 1-1v-1h1v1a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h1v1z"/>
                    </svg>
                </button>

                <button
                class="self-center w-fit text-sm px-2 py-2 dark:text-gray-300 dark:hover:text-white hover:bg-black/5 dark:hover:bg-white/5 rounded-xl"
                on:click={ () => {console.log('hola');
                                    }}
                >
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-arrow-up-right-square" viewBox="0 0 16 16">
                    <path fill-rule="evenodd" d="M15 2a1 1 0 0 0-1-1H2a1 1 0 0 0-1 1v12a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1zM0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2zm5.854 8.803a.5.5 0 1 1-.708-.707L9.243 6H6.475a.5.5 0 1 1 0-1h3.975a.5.5 0 0 1 .5.5v3.975a.5.5 0 1 1-1 0V6.707z"/>
                </svg>
            </button>

			</div>

			<!-- <div class="flex justify-end pr-2 pt-3 text-sm font-medium">
				<button
					class=" disabled:opacity-50 disabled:hover:bg-red-700 disabled:cursor-not-allowed px-4 py-2 bg-red-700 hover:bg-red-800 text-gray-100 transition rounded-lg"
					disabled={readInput !== 'delete'}
					on:click={async () => {deletingSnapshot}}
				>
					{$i18n.t('Delete')}
				</button>
			</div> -->

		</div>
	</div>
</Modal>

<style>
	/* Style the placeholder of only the input with class 'italic-placeholder' */
	.italic-placeholder::placeholder {
	  font-style: italic;
	}
  </style>