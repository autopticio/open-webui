<script>
	import ReadSnapshot from '$lib/components/storybooks/ReadSnapshot.svelte';
	import { page } from '$app/stores';

	let endpoint_id = $page.params.endpoint_id;
	let pql_id = $page.params.pql_id;
	let format = $page.params.format;
	let timestamp = $page.params.timestamp;
	let snapshot_id = $page.params.snapshot_id;
	let pageUrl = $page.url.href;
</script>

<ReadSnapshot {endpoint_id} {pql_id} {format} {timestamp} {snapshot_id} url={pageUrl}/>