// FB-510: add report filters (Loại DV, Khách hàng, Nhóm khách hàng, Hợp đồng,
// Thời gian, Công ty, Loại PAKD, Trạng thái)
frappe.query_reports["Profitability by Service"] = {
	filters: [
		{
			fieldname: "company",
			label: __("Công ty"),
			fieldtype: "Link",
			options: "Company",
			default: frappe.defaults.get_user_default("Company"),
		},
		{
			fieldname: "from_date",
			label: __("Từ ngày"),
			fieldtype: "Date",
			default: frappe.datetime.add_months(frappe.datetime.get_today(), -3),
		},
		{
			fieldname: "to_date",
			label: __("Đến ngày"),
			fieldtype: "Date",
			default: frappe.datetime.get_today(),
		},
		{
			fieldname: "pakd_type",
			label: __("Loại PAKD"),
			fieldtype: "Select",
			options: "\nRecurring Telecom\nOne-off Sale/Project",
		},
		{
			fieldname: "service_type",
			label: __("Loại DV"),
			fieldtype: "Select",
			options: "\nP2P\nMPLS\nILL\nFTTH DN\nIT Managed\nVTTB\nThi công",
		},
		{
			fieldname: "customer",
			label: __("Khách hàng"),
			fieldtype: "Link",
			options: "Customer",
		},
		{
			fieldname: "customer_group",
			label: __("Nhóm khách hàng"),
			fieldtype: "Link",
			options: "Customer Group",
		},
		{
			fieldname: "contract_ref",
			label: __("Hợp đồng"),
			fieldtype: "Link",
			options: "DCNet Contract",
		},
		{
			fieldname: "status",
			label: __("Trạng thái"),
			fieldtype: "Select",
			options: "\nDraft\nPending Sales Director\nPending General Dept\nPending Branch Director\nPending Board\nApproved\nRejected",
		},
	],
};
