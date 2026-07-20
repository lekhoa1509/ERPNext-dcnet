frappe.provide("frappe.dashboards.chart_sources");

frappe.dashboards.chart_sources["Revenue Expense Monthly"] = {
	method: "vn_accounting.vn_accounting.dashboard_chart_source.revenue_expense_monthly.revenue_expense_monthly.get",
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
