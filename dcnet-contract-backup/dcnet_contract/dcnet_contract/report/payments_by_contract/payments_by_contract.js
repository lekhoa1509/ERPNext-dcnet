frappe.query_reports["Payments by Contract"] = {
	filters: [
		{
			fieldname: "dcnet_contract",
			label: __("Hợp đồng"),
			fieldtype: "Link",
			options: "DCNet Contract",
		},
		{
			fieldname: "dcnet_pakd",
			label: __("PAKD"),
			fieldtype: "Link",
			options: "Phuong An Kinh Doanh",
		},
		{
			fieldname: "from_date",
			label: __("Từ ngày"),
			fieldtype: "Date",
		},
		{
			fieldname: "to_date",
			label: __("Đến ngày"),
			fieldtype: "Date",
		},
	],
};
