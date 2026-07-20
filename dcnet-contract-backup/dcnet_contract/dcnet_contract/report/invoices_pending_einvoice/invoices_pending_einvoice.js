frappe.query_reports["Invoices Pending eInvoice"] = {
	filters: [
		{
			fieldname: "dcnet_contract",
			label: __("Hợp đồng"),
			fieldtype: "Link",
			options: "DCNet Contract",
		},
		{
			fieldname: "customer",
			label: __("Khách hàng"),
			fieldtype: "Link",
			options: "Customer",
		},
	],
};
