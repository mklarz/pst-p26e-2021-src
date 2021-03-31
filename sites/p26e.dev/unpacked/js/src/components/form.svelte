<script>
	import * as Sentry from "@sentry/browser";
	import { showMessage } from "../utils";
	import { magicStore } from "../magic";

	export let selectedChallenge;
	export let onSubmitSuccess = () => Promise.resolve();

	let isSubmitting = false;
	let flag = "";
	let nickname = "";

	async function handleSubmit() {
		isSubmitting = true;
		const challengeId = selectedChallenge._id;
		const token = await magicStore.getToken();
		const res = await fetch("/api/submit", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
				Authorization: `Bearer ${token}`,
			},
			body: JSON.stringify({ nickname, flag, challengeId }),
		});

		if (res.status === 201) {
			await onSubmitSuccess();
			flag = "";
			nickname = "";
		} else {
			const feedback = await res.text();
			showMessage("error", feedback);
			if (res.status === 500) {
				Sentry.captureException(new Error(`Submit Error ${res.status}`), {
					extra: { body: JSON.stringify({ nickname, flag, challengeId }) },
				});
			}
		}

		isSubmitting = false;
	}
</script>

{#await $magicStore}
	<p class="loading">Vent litt mens vi sjekker om du er logget inn...</p>
{:then user}
	{#if user}
		{#if !!selectedChallenge.solutions?.some((s) => s.id === user.id)}
			<p class="solved">Hurra, du har løst oppgaven!</p>
		{:else}
			<form on:submit|preventDefault={handleSubmit}>
				<label>
					<span
						>E-post <span class="description"
							>(vi deler ikke denne med noen)</span
						></span
					>
					<input value={user.email} type="text" disabled />
				</label>
				<label>
					<span
						>Kallenavn <span class="description"
							>(2-15 tegn, kun bokstaver, tall og "_")</span
						></span
					>
					<input
						bind:value={nickname}
						type="text"
						max="15"
						min="2"
						required
						pattern="[a-zA-z0-9æøåÆØÅ_]{'{'}2,15{'}'}"
						disabled={isSubmitting}
					/>
				</label>
				<label>
					<span>Løsningsord</span>
					<input
						placeholder="Eksempelvis: PST{'{'}j36_f4n7_5v4237{'}'}"
						bind:value={flag}
						type="text"
						required
						disabled={isSubmitting}
					/>
				</label>
				<button type="submit" disabled={isSubmitting}>
					{isSubmitting ? "Verifiserer..." : "Send inn"}
				</button>
			</form>
		{/if}

		<button type="button" id="logout" on:click={magicStore.logout}>
			Logg ut
		</button>
	{:else}
		<form
			on:submit|preventDefault={(event) =>
				magicStore.login(event.target.email.value)}
		>
			<label>
				<span
					>E-post <span class="description">(vi deler ikke denne med noen)</span
					></span
				>
				<input name="email" type="email" required />
			</label>
			<button type="submit">Logg inn med epost</button>
			<section>
				<span>Eller logg inn med:</span>
				<ul>
					{#each ["github"] as provider}
						<li>
							<button on:click={() => magicStore.loginOauth(provider)}
								>{provider}</button
							>
						</li>
					{/each}
				</ul>
			</section>
		</form>
	{/if}
{/await}

<style>
	.loading {
		text-align: center;
		opacity: 0.7;
		font-size: 0.85rem;
	}

	.solved {
		text-align: center;
		font-size: 1.25rem;
		color: #eeeeee;
	}

	form {
		display: flex;
		flex-direction: column;
		align-items: center;
	}

	label {
		width: 100%;
		display: flex;
		flex-direction: column;
		margin-top: 0.5rem;
	}

	label span {
		font-size: 0.75rem;
		text-transform: uppercase;
	}

	label span.description {
		text-transform: lowercase;
		opacity: 0.65;
	}

	input {
		line-height: 1.5;
		font-size: 1rem;
		border: 1px solid black;
		box-shadow: inset 0px 2px 4px rgb(0 0 0 / 25%);
		border-radius: 3px;
		padding: 0.5em;
	}

	input:disabled {
		opacity: 0.5;
		background: white;
	}

	button {
		border: none;
		background: none;
		color: white;
		opacity: 0.85;
		font-family: inherit;
		font-size: 0.8rem;
		cursor: pointer;
		padding: 0.5em 1em;
		text-transform: uppercase;
	}

	button[type="submit"] {
		margin-top: 1rem;
		opacity: 1;
		min-width: 200px;
		border: 1px solid black;
		font-size: 1rem;
		background-color: #5d0990;
		color: white;
		padding: 0.75em 1em;
		box-shadow: 2px 2px 2px 1px rgb(0 0 0 / 25%);
	}

	button:disabled {
		opacity: 0.5;
		cursor: not-allowed;
	}

	button:enabled:hover {
		text-decoration: underline;
	}

	button#logout {
		margin: 1em auto;
		display: block;
	}

	section {
		display: flex;
		flex-direction: column;
		align-items: center;
		margin-top: 0.5rem;
		font-size: 0.75rem;
	}

	ul {
		list-style: none;
		margin: 0.2em 0;
		padding: 0;
		display: flex;
		flex-direction: row;
		flex-wrap: wrap;
		align-items: center;
	}

	li:not(:last-of-type)::after {
		content: " • ";
	}
</style>
