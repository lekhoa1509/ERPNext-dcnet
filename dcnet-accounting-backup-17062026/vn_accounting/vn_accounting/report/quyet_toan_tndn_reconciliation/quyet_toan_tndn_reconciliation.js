// Copyright (c) 2026, VN Accounting and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Quyet Toan TNDN Reconciliation"] = {
	filters: [
		{
			fieldname: "company",
			label: __("Công ty"),
			fieldtype: "Link",
			options: "Company",
			reqd: 1,
			default: frappe.defaults.get_user_default("Company"),
		},
		{
			fieldname: "fiscal_year",
			label: __("Năm tài chính"),
			fieldtype: "Link",
			options: "Fiscal Year",
			reqd: 1,
			default: frappe.defaults.get_user_default("fiscal_year"),
		},
		{
			fieldname: "cit_rate",
			label: __("Thuế suất TNDN (%)"),
			fieldtype: "Float",
			default: 20,
			description: __("Mặc định 20%. Doanh nghiệp ưu đãi có thể nhập 10/15/17."),
		},
	],

	formatter(value, row, column, data, default_formatter) {
		const label = data && data.label;
		if (label && (String(label).startsWith("───") || data.code === "A" || data.code === "C" || data.code === "D")) {
			return `<strong>${default_formatter(value, row, column, data)}</strong>`;
		}
		return default_formatter(value, row, column, data);
	},
};
