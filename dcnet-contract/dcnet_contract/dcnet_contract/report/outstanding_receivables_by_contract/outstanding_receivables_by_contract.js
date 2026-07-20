frappe.query_reports["Outstanding Receivables by Contract"] = {
	filters: [
		{
			fieldname: "customer",
			label: __("Customer"),
			fieldtype: "Link",
			options: "Customer",
		},
		{
			fieldname: "branch",
			label: __("Branch"),
			fieldtype: "Link",
			options: "Branch",
		},
		{
			fieldname: "service_type",
			label: __("Service Type"),
			fieldtype: "Select",
			options: "\nP2P\nMPLS\nILL\nFTTH DN\nIT Managed\nVTTB\nThi công",
		},
		{
			fieldname: "status",
			label: __("Billing State"),
			fieldtype: "Select",
			options: "\nProjected\nInvoiced\nOverdue\nPaid",
		},
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
		},
		{
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Date",
		},
	],
};
