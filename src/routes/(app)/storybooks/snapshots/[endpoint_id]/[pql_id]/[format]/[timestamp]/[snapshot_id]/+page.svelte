<script>
	import ReadSnapshot from '$lib/components/storybooks/ReadSnapshot.svelte';
	import { page } from '$app/stores';

	let pql_id = $page.params.pql_id;
	let format = $page.params.format;
	let timestamp = $page.params.timestamp;
	let snapshot_id = $page.params.snapshot_id;
	let pageUrl = $page.url.href;
</script>

<ReadSnapshot {pql_id} {format} {timestamp} {snapshot_id} url={pageUrl}/>