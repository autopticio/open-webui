<script lang="ts">

	import { onMount, getContext } from 'svelte';

	import { WEBUI_NAME } from '$lib/stores';

	const i18n = getContext('i18n');

	onMount(async () => {});

</script>

<svelte:head>
	<title>
		{$i18n.t('Environments')} | {$WEBUI_NAME}
	</title>
</svelte:head>

<div class=" text-lg font-semibold mb-3">{$i18n.t('Environments')}</div>


<div class=" text-lg font-semibold mb-3">{$i18n.t('Coming soon!')}</div>

<hr class=" dark:border-gray-850" />

<style>
	/* Use the same hover colors for the selected state */
	.selected {
		background-color: rgba(0, 0, 0, 0.05); /* Same as hover:bg-black/5 */
	}
	.dark .selected {
		background-color: rgba(55, 65, 81, 0.05); /* Same as dark:hover:bg-gray-700/5 */
	}
</style>