frappe.query_reports["Beneficiary Payable"] = {
	filters: [
		{
			fieldname: "pakd",
			label: __("PAKD"),
			fieldtype: "Link",
			options: "Phuong An Kinh Doanh",
		},
		{
			fieldname: "kind",
			label: __("Loại"),
			fieldtype: "Select",
			options: "\nManager Services\nAdd Costs\nReferral",
		},
		{
			fieldname: "with_recipient_only",
			label: __("Chỉ có người nhận đích danh (3-leg TNCN)"),
			fieldtype: "Check",
		},
	],
};
