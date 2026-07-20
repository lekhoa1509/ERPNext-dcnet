frappe.ui.form.on("PIT Annual Settlement", {
	refresh(frm) {
		if (frm.doc.fiscal_year && frm.doc.company) {
			frm.add_custom_button(__("Aggregate from Salary Slips"), () => {
				frm.call("aggregate_from_salary_slips").then(() => frm.reload_doc());
			});
		}
		if (!frm.is_new()) {
			frm.add_custom_button(__("Export 05/QTT-TNCN"), () => {
				frappe.call({
					method: "dcnet_hrm.export.qtt_tncn.export_qtt_tncn",
					args: { pit_annual_settlement: frm.doc.name },
					freeze: true,
					freeze_message: __("Đang tạo 05/QTT-TNCN..."),
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
