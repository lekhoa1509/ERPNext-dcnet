// Copyright (c) 2026, VN Accounting and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["S03b-DN So Cai"] = {
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
			fieldname: "account",
			label: __("Tài khoản"),
			fieldtype: "Link",
			options: "Account",
			reqd: 1,
			get_query: () => ({
				filters: {
					company: frappe.query_report.get_filter_value("company"),
					is_group: 0,
				},
			}),
			description: __("Chọn 1 tài khoản leaf (is_group=0) để xem Sổ Cái của tài khoản đó."),
		},
		{
			fieldname: "from_date",
			label: __("Từ ngày"),
			fieldtype: "Date",
			reqd: 1,
			default: frappe.datetime.year_start(),
		},
		{
			fieldname: "to_date",
			label: __("Đến ngày"),
			fieldtype: "Date",
			reqd: 1,
			default: frappe.datetime.year_end(),
		},
	],
};
