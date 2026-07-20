frappe.query_reports["05-KK-TNCN"] = {
	filters: [
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			default: frappe.defaults.get_user_default("Company"),
		},
		{ fieldname: "from_date", label: __("From Date"), fieldtype: "Date", reqd: 1 },
		{ fieldname: "to_date", label: __("To Date"), fieldtype: "Date", reqd: 1 },
	],
	onload(report) {
		report.page.add_inner_button(__("Export 05/KK-TNCN"), () => {
			frappe.call({
				method: "dcnet_hrm.export.kk_tncn.export_kk_tncn",
				args: report.get_values(),
				freeze: true,
				freeze_message: __("Đang tạo 05/KK-TNCN..."),
				callback(r) {
					if (r.message) {
						window.open(r.message, "_blank");
					}
				},
			});
		});
	},
};
