import { writable } from "svelte/store";

const cache = new Map();

export default function fetcher(url) {
	const store = writable(new Promise(() => {}));

	// Get cached result
	if (cache.has(url)) {
		store.set(Promise.resolve(cache.get(url)));
	}

	// Revalidate
	async function revalidate(url) {
		try {
			const result = await fetch(url + window.location.search);
			const data = await result.json();
			cache.set(url, data);
			store.set(Promise.resolve(data));
		} catch (err) {
			store.set(Promise.reject(err));
		}
	}

	revalidate(url);

	return [store, () => revalidate(url)];
}
