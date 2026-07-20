// eslint-disable-next-line no-unused-vars
frappe.query_reports["S21-DN"] = {
	filters: [
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			default: frappe.defaults.get_user_default("Company"),
			reqd: 1,
		},
		{
			fieldname: "asset_category",
			label: __("Asset Category"),
			fieldtype: "Link",
			options: "Asset Category",
		},
		{
			fieldname: "location",
			label: __("Location"),
			fieldtype: "Link",
			options: "Location",
		},
		{
			fieldname: "status",
			label: __("Status"),
			fieldtype: "Select",
			options:
				"\nIn Location\nIssued\nPartially Depreciated\nFully Depreciated",
		},
	],
};
