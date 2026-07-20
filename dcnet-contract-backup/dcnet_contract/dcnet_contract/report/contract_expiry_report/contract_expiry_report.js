frappe.query_reports["Contract Expiry Report"] = {
	filters: [
		{
			fieldname: "expiry_days",
			label: __("Expiring Within (Days)"),
			fieldtype: "Int",
			default: 30,
			description: __("Show contracts expiring within N days from today"),
		},
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
	],
};
