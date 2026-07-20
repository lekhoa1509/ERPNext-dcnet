frappe.query_reports["Batch Near Expiry Status"] = {
	filters: [
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			width: "80",
			default: erpnext.utils.get_fiscal_year(frappe.datetime.get_today(), true)[1],
			reqd: 1,
		},
		{
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Date",
			width: "80",
			default: frappe.datetime.get_today(),
			reqd: 1,
		},
		{
			fieldname: "item",
			label: __("Item"),
			fieldtype: "Link",
			options: "Item",
			width: "100",
			get_query: function () {
				return {
					filters: { has_batch_no: 1 },
				};
			},
		},
		{
			fieldname: "expired_filter",
			label: __("Expired Status"),
			fieldtype: "Select",
			options: "\nExclude Expired\nExpired Only",
			default: "",
			width: "120"
		},
		{
			fieldname: "near_expiry_days",
			label: __("Near Expired (Days)"),
			fieldtype: "Int",
			default: 7
		},
	],
};