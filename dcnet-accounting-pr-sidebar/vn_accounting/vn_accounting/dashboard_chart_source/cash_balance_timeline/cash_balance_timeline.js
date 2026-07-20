frappe.provide("frappe.dashboards.chart_sources");

frappe.dashboards.chart_sources["Cash Balance Timeline"] = {
	method: "vn_accounting.vn_accounting.dashboard_chart_source.cash_balance_timeline.cash_balance_timeline.get",
	filters: [
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			default: frappe.defaults.get_user_default("Company"),
		},
	],
};
