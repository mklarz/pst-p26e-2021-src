import * as Sentry from "@sentry/browser";
import { Integrations } from "@sentry/tracing";
import App from "./app.svelte";

Sentry.init({
	dsn:
		"https://b806f29937d04769a280b3455945e764@o483471.ingest.sentry.io/5699423",
	integrations: [new Integrations.BrowserTracing()],
	tracesSampleRate: 1.0,
});

const app = new App({
	target: document.body,
});

export default app;
