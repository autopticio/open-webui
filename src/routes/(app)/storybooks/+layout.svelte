<script lang="ts">
	import { onMount, getContext } from 'svelte';

	import { WEBUI_NAME, showSidebar } from '$lib/stores';
	import MenuLines from '$lib/components/icons/MenuLines.svelte';
	import { page } from '$app/stores';

	const i18n = getContext('i18n');
</script>

<svelte:head>
	<title>
		{$i18n.t('Storybooks')} | {$WEBUI_NAME}
	</title>
</svelte:head>

<div
	class=" flex flex-col w-full min-h-screen max-h-screen {$showSidebar
		? 'md:max-w-[calc(100%-260px)]'
		: ''}"
>
	<div class=" px-4 pt-3 mt-0.5 mb-1">
		<div class=" flex items-center gap-1">
			<div class="{$showSidebar ? 'md:hidden' : ''} mr-1 self-start flex flex-none items-center">
				<button
					id="sidebar-toggle-button"
					class="cursor-pointer p-1 flex rounded-xl hover:bg-gray-100 dark:hover:bg-gray-850 transition"
					on:click={() => {
						showSidebar.set(!$showSidebar);
					}}
				>
					<div class=" m-auto self-center">
						<MenuLines />
					</div>
				</button>
			</div>
			<div class="flex items-center text-xl font-semibold">{$i18n.t('Storybooks')}</div>
		</div>
	</div>

	<div class="px-4 my-1">
		<div
			class="flex scrollbar-none overflow-x-auto w-fit text-center text-sm font-medium rounded-xl bg-transparent/10 p-1"
		>
			<a
				class="min-w-fit rounded-lg p-1.5 px-3 {$page.url.pathname.includes('/storybooks/snapshots')
					? 'bg-gray-50 dark:bg-gray-850'
					: ''} transition"
				href="/storybooks/snapshots">{$i18n.t('Snapshots')}
			</a>

			<a
				class="min-w-fit rounded-lg p-1.5 px-3 {$page.url.pathname.includes('/storybooks/pqls')
					? 'bg-gray-50 dark:bg-gray-850'
					: ''} transition"
				href="/storybooks/pqls">{$i18n.t('PQLs')}
			</a>

			<a
				class="min-w-fit rounded-lg p-1.5 px-3 {$page.url.pathname.includes('/storybooks/environments')
					? 'bg-gray-50 dark:bg-gray-850'
					: ''} transition"
				href="/storybooks/environments">{$i18n.t('Environments')}
			</a>

			<a
				class="min-w-fit rounded-lg p-1.5 px-3 {$page.url.pathname.includes('/storybooks/tokens')
					? 'bg-gray-50 dark:bg-gray-850'
					: ''} transition"
				href="/storybooks/tokens">{$i18n.t('Tokens')}
			</a>

			<a
				class="disabled min-w-fit rounded-lg p-1.5 px-3 {$page.url.pathname.includes('/workspace')
					? 'bg-gray-50 dark:bg-gray-850'
					: ''} transition"
				href="/storybooks/">{$i18n.t('Future catalog')}
			</a>

		</div>
	</div>

	<hr class=" my-2 dark:border-gray-850" />

	<div class=" py-1 px-5 flex-1 max-h-full overflow-y-auto">
		<slot />
	</div>
</div>

<style>
	.disabled {
		pointer-events: none;
		cursor: not-allowed; /* 'Not allowed' cursor */
	}
</style>

