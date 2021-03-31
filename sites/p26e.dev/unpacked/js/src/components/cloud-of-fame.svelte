<script>
	import { flip } from "svelte/animate";

	export let selectedChallenge;
	export let largest = 3;
	export let lowest = 0.5;

	function cloudify(participants = []) {
		const cloudWorthy = participants
			.map((p) => ({
				...p,
				timestamp: new Date(p.timestamp),
			}))
			.sort((p1, p2) => p1.timestamp.getTime() - p2.timestamp.getTime())
			.slice(0, 25);
		const cloudSize = cloudWorthy.length;
		return cloudWorthy
			.map((p, i) => ({
				id: p.id,
				nickname: p.nickname,
				place: i + 1,
				size: lowest + ((largest - lowest) * (cloudSize - i)) / cloudSize,
			}))
			.sort(() => 0.5 - Math.random());
	}

	$: cloudList = selectedChallenge?.solutions
		? cloudify(selectedChallenge.solutions)
		: [];
</script>

<ul>
	{#each cloudList as cloudItem (cloudItem.id)}
		<li
			style="font-size: {cloudItem.size}rem"
			class:rainbowText={cloudItem.place === 1}
			animate:flip
		>
			{cloudItem.nickname}
		</li>
	{:else}
		<p>Skyfritt i dag ser det ut til</p>
	{/each}
</ul>

<style>
	ul {
		list-style: none;
		padding: 0;
		margin: 5rem auto;
		width: 100%;
		display: flex;
		flex-wrap: wrap;
		align-items: flex-start;
		line-height: 1;
		justify-content: space-evenly;
		color: #cacaca;
	}

	li {
		padding: 0.1em;
	}

	.rainbowText {
		background: linear-gradient(
			to right,
			#6666ff,
			#0099ff,
			#00ff00,
			#ff3399,
			#6666ff,
			#0099ff
		);
		-webkit-background-clip: text;
		background-clip: text;
		color: transparent;
		animation: rainbow_animation 2.5s linear infinite;
		background-size: 400% 100%;
	}

	@keyframes rainbow_animation {
		from {
			background-position: 0 0;
		}

		to {
			background-position: 100% 0;
		}
	}
</style>
