frappe.ui.form.on("Insurance Declaration", {
	refresh(frm) {
		if (frm.doc.docstatus === 1) {
			frm.add_custom_button(__("Export D02-LT"), () => {
				frappe.call({
					method: "dcnet_hrm.export.d02lt.export_d02lt",
					args: { insurance_declaration: frm.doc.name },
					freeze: true,
					freeze_message: __("Đang tạo D02-LT..."),
					callback(r) {
						if (r.message) {
							window.open(r.message, "_blank");
						}
					},
				});
			});
		}
	},
});
