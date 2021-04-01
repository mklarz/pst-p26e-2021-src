<script>
	import Blob from "./components/blob.svelte";
	import Form from "./components/form.svelte";
	import fetcher from "./fetcher";
	import { magicStore } from "./magic";
	import blocksToHtml from "@sanity/block-content-to-html";
	import { SvelteToast } from "@zerodevx/svelte-toast";
	import Slideshow from "./components/slideshow.svelte";
	import CloudOfFame from "./components/cloud-of-fame.svelte";

	let [challengesPromise, revalidate] = fetcher("/api/challenges");
	let selectedChallenge = undefined;

	function onSubmitSuccess() {
		if (selectedChallenge && selectedChallenge.slug?.current) {
			plausible(selectedChallenge.slug.current);
		}
		return revalidate();
	}
</script>

<SvelteToast />

<main>
	<h1>Mysteriet på <br /> Harefjell Vinterresort</h1>
	{#await $challengesPromise then challenges}
		<Slideshow {challenges} bind:selectedChallenge />
		{#if selectedChallenge}
			<Blob>
				<h2>{selectedChallenge.title}</h2>
				{#if selectedChallenge.description}
					{@html blocksToHtml({
						blocks: selectedChallenge.description,
					})}
				{/if}
				<ul>
					{#each selectedChallenge.attachments || [] as attachment}
						<li>
							<a
								href={attachment.url}
								target="_blank"
								rel="noopener noreferrer"
								download={attachment.filename}
							>
								{attachment.filename}
							</a>
						</li>
					{/each}
				</ul>
				{#if !selectedChallenge.informationOnly}
					<Form {onSubmitSuccess} {selectedChallenge} />
				{/if}
			</Blob>
			{#if !selectedChallenge.informationOnly}
				<section>
					<h2>Berømmelsesskyen</h2>
					<p>
						De 25 raskeste hver dag havner i <i>berømmelsesskyen</i>
					</p>
					<CloudOfFame {selectedChallenge} />
				</section>
			{/if}
		{/if}
	{:catch}
		<p>Heisann, her gikk vist noe i ball. Prøv å laste siden på nytt.</p>
	{/await}
</main>
<footer>
	<span>
		Vi har ledige stillinger: <a
			href="https://pst.no/jobb"
			target="_blank"
			rel="noopener noreferrer">https://pst.no/jobb</a
		>
	</span>
	<h3>Påskenøtter presentert av PST</h3>
</footer>

<style>
	h1 {
		display: inline-block;
		position: relative;
		left: 50%;
		color: #dbbf23;
		text-align: center;
		text-shadow: 2px 0 black, -2px 0 black, 0 2px black, 0 -2px black;
		transform: translateX(-50%) rotate(-6.5deg);
		font-size: clamp(2rem, -0.25rem + 10vw, 5rem);
		letter-spacing: 2px;
		margin-top: 3.5rem;
	}

	h2 {
		text-align: center;
		font-size: clamp(1.6rem, -0.2rem + 8vw, 4rem);
		text-shadow: 2px 0 0 black, -1px 0 black, 0 2px black, 0 -1px black;
		margin: 1.5rem 0;
		letter-spacing: 1px;
		line-height: 1.5em;
	}

	ul {
		list-style: none;
		padding: 0;
		max-width: 650px;
		display: flex;
		flex-wrap: wrap;
		align-items: flex-start;
		line-height: 1;
		justify-content: space-evenly;
		color: #cacaca;
		flex-direction: column;
		margin: 2rem 0 3rem;
	}

	a {
		color: inherit;
	}

	li::before {
		content: "📎 ";
	}

	li {
		padding: 0.1em;
	}

	section {
		padding: 1rem;
		max-width: 600px;
		margin: 0 auto;
	}

	section > p {
		text-align: center;
	}

	section > h2 {
		margin-top: 0;
	}

	footer {
		margin-top: 10rem;
	}

	footer h3 {
		font-family: "Bangers", cursive;
		color: #dbbf23;
		text-align: center;
		font-size: 1.5rem;
		text-shadow: 2px 0 0 black, -1px 0 black, 0 2px black, 0 -1px black;
		letter-spacing: 1px;
	}

	footer span {
		display: block;
		text-align: center;
	}

	:global(code) {
		background-color: rgba(0, 0, 0, 0.3);
		padding: 0.1em;
	}

	:global(a) {
		color: inherit;
	}
</style>
