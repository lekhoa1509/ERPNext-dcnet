frappe.query_reports["Overdue Billing Periods"] = {
	filters: [
		{
			fieldname: "company",
			label: __("Công ty"),
			fieldtype: "Link",
			options: "Company",
		},
		{
			fieldname: "branch",
			label: __("Chi nhánh"),
			fieldtype: "Link",
			options: "Branch",
		},
	],
};
