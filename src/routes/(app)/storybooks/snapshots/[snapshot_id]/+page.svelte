<script>
	import ReadSnapshot from '$lib/components/storybooks/ReadSnapshot.svelte';
	import { page } from '$app/stores';

	let snapshot_id = $page.params.snapshot_id;

</script>

<ReadSnapshot {snapshot_id}/>