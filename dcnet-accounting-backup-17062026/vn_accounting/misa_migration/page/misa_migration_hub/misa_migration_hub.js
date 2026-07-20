// Misa Migration Hub — thin Page handler (ES5).
// Real UI lives in misa_migration_hub.bundle.js (Vue 3 SFC, mounted by
// frappe.misa_migration.Hub class). This file only sets up Frappe page chrome
// and delegates body rendering to the bundle.

frappe.pages["misa-migration-hub"].on_page_load = function (wrapper) {
	const page = frappe.ui.make_app_page({
		parent: wrapper,
		title: __("Misa Migration"),
		single_column: true,
	});

	page.set_secondary_action(__("Lịch sử"), function () {
		frappe.set_route("List", "Misa Migration Batch");
	});

	// Bundle exposes frappe.misa_migration.Hub via app_include_js (Phase A
	// commit 5). Fall back to a placeholder if the bundle hasn't loaded yet —
	// the smoke test for commit 4 ships before commit 5.
	if (frappe.misa_migration && frappe.misa_migration.Hub) {
		new frappe.misa_migration.Hub({ wrapper: wrapper, page: page });
	} else {
		$(page.body).html(
			'<div style="padding:24px;text-align:center;color:#888;">' +
				'<p>' + __("Bundle Vue chưa nạp. Chạy <code>bench build --app vn_accounting</code> và refresh.") + '</p>' +
				'</div>'
		);
	}
};
