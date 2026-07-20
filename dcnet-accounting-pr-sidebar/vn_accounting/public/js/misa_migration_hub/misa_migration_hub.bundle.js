// Misa Migration Hub — Vue 3 SFC mount entry.
// Lazy-loaded via frappe.require() from the page handler (misa_migration_hub.js)
// ON THE misa-migration-hub ROUTE ONLY — not shipped on every desk page. The
// class frappe.misa_migration.Hub is instantiated by the page handler once the
// bundle resolves.

import { createApp } from "vue";
import { createPinia } from "pinia";
import App from "./App.vue";

class MisaMigrationHub {
	constructor({ wrapper, page }) {
		this.wrapper = wrapper;
		this.page = page;
		this.mount();
	}

	mount() {
		const $mount = $('<div class="misa-migration-app"></div>').appendTo(this.page.body);
		this.app = createApp(App, { page: this.page });
		// SetVueGlobals is provided by Frappe at runtime — wires i18n,
		// $format, $createElement, etc. Skip if not present (older Frappe).
		if (typeof SetVueGlobals === "function") {
			SetVueGlobals(this.app);
		}
		this.pinia = createPinia();
		this.app.use(this.pinia);
		this.instance = this.app.mount($mount.get(0));
	}

	destroy() {
		if (this.app) this.app.unmount();
	}
}

frappe.provide("frappe.misa_migration");
frappe.misa_migration.Hub = MisaMigrationHub;

export default MisaMigrationHub;
