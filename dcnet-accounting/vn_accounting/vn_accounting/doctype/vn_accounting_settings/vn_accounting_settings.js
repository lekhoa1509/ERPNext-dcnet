// Copyright (c) 2026, DCNet and Contributors
// License: MIT

frappe.ui.form.on("VN Accounting Settings", {
	refresh(frm) {
		// PM-11: Navigate to tab based on URL hash (e.g. #asset-permissions-tab)
		const hash = window.location.hash.replace("#", "");
		if (hash) {
			const tab_map = {
				"asset-permissions-tab": __("Phân quyền TSCĐ & CCDC"),
				"treasury-tab": __("Quỹ & Tiền gửi"),
				"bank-loan-tab": __("Khoản vay ngân hàng"),
			};
			const tab_label = tab_map[hash] || null;
			if (tab_label) {
				setTimeout(() => frm.set_active_tab && frm.set_active_tab(tab_label), 200);
			}
		}
		// FB-533: provide access to ERPNext Accounts Settings (sidebar entry removed
		// to avoid two "Cài đặt kế toán" items confusing users).
		frm.add_custom_button(__("Cài đặt kế toán ERPNext nâng cao"), function () {
			frappe.set_route("Form", "Accounts Settings");
		});

		frm.add_custom_button(__("Khôi phục mặc định"), function () {
			frappe.confirm(
				__("Đặt lại ma trận phân quyền về mặc định? Mọi thay đổi thủ công sẽ bị mất."),
				function () {
					frappe.call({
						method: "reset_permission_matrix",
						doc: frm.doc,
						callback(r) {
							if (!r.exc) {
								frappe.show_alert({
									message: r.message || __("Đã khôi phục mặc định"),
									indicator: "green",
								});
								frm.reload_doc();
							}
						},
					});
				}
			);
		}, __("Phân quyền TSCĐ & CCDC"));
	},
});
