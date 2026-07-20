// Copyright (c) 2026, VN Accounting and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["S03a-DN So Nhat Ky Chung"] = {
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
		{
			fieldname: "voucher_type",
			label: __("Loại chứng từ"),
			fieldtype: "Select",
			options: [
				"",
				"Journal Entry",
				"Payment Entry",
				"Sales Invoice",
				"Purchase Invoice",
				"Stock Entry",
				"Delivery Note",
				"Purchase Receipt",
				"Branch Cash Entry",
				"Expense Claim",
				"Asset",
			].join("\n"),
			description: __("Lọc theo loại chứng từ. Bỏ trống = tất cả."),
		},
	],
};
