import { writable } from "svelte/store";
import { Magic } from "magic-sdk";
import { OAuthExtension } from "@magic-ext/oauth";

function createMagicStore() {
	const magic = new Magic("pk_live_6D109FD8E8026A65", {
		locale: "no",
		extensions: [new OAuthExtension()],
	});

	const { subscribe, set } = writable(
		new Promise(async (resolve) => {
			if (/[?&]magic_oauth_request_id=/.test(location.search)) {
				const {
					magic: {
						userMetadata: { email, publicAddress: id },
					},
				} = await magic.oauth.getRedirectResult();
				resolve({ email, id });
			} else if (await magic.user.isLoggedIn()) {
				const { email, publicAddress: id } = await magic.user.getMetadata();
				resolve({ email, id });
			} else {
				resolve(null);
			}
		})
	);

	return {
		subscribe,
		login: async (loginEmail) => {
			set(
				new Promise(async (resolve) => {
					try {
						await magic.auth.loginWithMagicLink({ email: loginEmail });
						const { email, publicAddress: id } = await magic.user.getMetadata();
						resolve({ email, id });
					} catch {
						resolve(null);
					}
				})
			);
		},
		loginOauth: async (provider) => {
			set(
				new Promise(async () => {
					await magic.oauth.loginWithRedirect({
						provider,
						scope: ["user:email"],
						redirectURI: location.href,
					});
				})
			);
		},
		logout: async () => {
			set(Promise.resolve(null));
			await magic.user.logout();
		},
		getToken: async () => magic.user.getIdToken(),
	};
}

export const magicStore = createMagicStore();
