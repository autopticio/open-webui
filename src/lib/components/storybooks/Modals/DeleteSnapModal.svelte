<script lang="ts">

	import { getContext } from 'svelte';


	import Modal from '$lib/components/common/Modal.svelte';
	import { deleteSnapshot } from '$lib/apis/autoptic';

	const i18n = getContext('i18n');

	export let showDelete = false;

	let deleteInput = '';

	export let snapshot = null;

	$: if (!showDelete) {
		deleteInput = '';
	}

</script>

<Modal size="sm" bind:show={showDelete}>
	<div>
		<div class=" flex justify-between dark:text-gray-300 px-5 pt-4 pb-1">
			<div class=" text-lg font-medium self-center">{$i18n.t('You are about to delete a Snapshot')}</div>
			<button
				class="self-center"
				on:click={() => {
					showDelete = false;
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
						{$i18n.t('If you want to delete this snapshot, please type "delete".')}
					</div>
			</div>

			<div class=" flex w-full space-x-2">
				<div class="flex flex-1 pl-1">
					<input
						class="dark:bg-gray-800 pl-2 italic-placeholder w-full text-sm pr-4 py-1 rounded outline-none bg-transparent"
						bind:value={deleteInput}
						placeholder={$i18n.t('delete')}
					/>
				</div>
			</div>

			<div class="flex justify-end pr-2 pt-3 text-sm font-medium">
				<button
					class=" disabled:opacity-50 disabled:hover:bg-red-700 disabled:cursor-not-allowed px-4 py-2 bg-red-700 hover:bg-red-800 text-gray-100 transition rounded-lg"
					disabled={deleteInput !== 'delete'}
					on:click={async () => {
						deleteSnapshot(snapshot.endpoint_id, snapshot.pql_id, snapshot.format, snapshot.timestamp, snapshot.snapshot_id);
						showDelete = false;
					}}
				>
					{$i18n.t('Delete')}
				</button>
			</div>

		</div>
	</div>
</Modal>

<style>
	/* Style the placeholder of only the input with class 'italic-placeholder' */
	.italic-placeholder::placeholder {
	  font-style: italic;
	}
  </style>