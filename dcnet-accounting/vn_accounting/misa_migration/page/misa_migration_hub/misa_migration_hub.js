// Misa Migration Hub — thin Page handler (ES5).
// Real UI lives in misa_migration_hub.bundle.js (Vue 3 SFC, mounted by
// frappe.misa_migration.Hub class). This file only sets up Frappe page chrome
// and lazy-loads the (heavy: ~194 KB Vue+Pinia) bundle ON THIS ROUTE ONLY via
// frappe.require — so the bundle is NOT shipped on every desk page. The
// background migration runs server-side (RQ jobs); this UI only triggers +
// polls, so route changes never affect a running migration.

frappe.pages["misa-migration-hub"].on_page_load = function (wrapper) {
	const page = frappe.ui.make_app_page({
		parent: wrapper,
		title: __("Misa Migration"),
		single_column: true,
	});

	page.set_secondary_action(__("Lịch sử"), function () {
		frappe.set_route("List", "Misa Migration Batch");
	});

	const BUNDLE = "misa_migration_hub.bundle.js";

	function has_asset() {
		return !!(frappe.boot.assets_json || {})[BUNDLE];
	}

	function mount() {
		$(page.body).empty();
		new frappe.misa_migration.Hub({ wrapper: wrapper, page: page });
	}

	function fail() {
		$(page.body).html(
			'<div style="padding:24px;text-align:center;color:#888;">' +
				'<p>' + __("Không nạp được giao diện. Chạy <code>bench build --app vn_accounting</code> và refresh.") + '</p>' +
				'</div>'
		);
	}

	function require_and_mount() {
		frappe.require(BUNDLE, function () {
			if (frappe.misa_migration && frappe.misa_migration.Hub) {
				mount();
			} else {
				fail();
			}
		});
	}

	if (frappe.misa_migration && frappe.misa_migration.Hub) {
		// Bundle already loaded earlier this session.
		mount();
		return;
	}

	$(page.body).html(
		'<div style="padding:24px;text-align:center;color:#888;">' +
			'<p>' + __("Đang tải giao diện…") + '</p>' +
			'</div>'
	);

	// frappe.boot.assets_json is captured once at login, so it can be stale when
	// `bench build` ran AFTER this session started — the new hashed path never
	// reaches the browser until re-login. If the key is missing we must NOT call
	// frappe.require with it: the resolver yields an undefined path → the browser
	// fetches /undefined → 404 → blank page + a cascade of console errors.
	// Instead, refresh assets_json from the server and retry once; a correctly
	// built site then self-heals without re-login. Only when the server genuinely
	// lacks the bundle do we show the "run bench build" message.
	if (has_asset()) {
		require_and_mount();
		return;
	}

	frappe.call("frappe.sessions.get_boot_assets_json").then(function (r) {
		if (r && r.message) {
			frappe.boot.assets_json = r.message;
		}
		if (has_asset()) {
			require_and_mount();
		} else {
			fail();
		}
	});
};
