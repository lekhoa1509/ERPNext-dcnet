// Copyright (c) 2026, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on("HTKK Settings", {
	seed_mapping_btn(frm) {
		frappe.confirm(
			__(
				"Tạo mapping mặc định theo TT99/2025 cho tất cả công ty Việt Nam? Mapping hiện có sẽ bị ghi đè."
			),
			() => {
				frm.call("seed_default_mapping").then(() => {
					frm.reload_doc();
				});
			}
		);
	},
});
