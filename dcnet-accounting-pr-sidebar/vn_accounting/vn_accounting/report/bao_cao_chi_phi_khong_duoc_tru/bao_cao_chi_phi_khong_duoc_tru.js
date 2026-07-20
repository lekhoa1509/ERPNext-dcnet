// Copyright (c) 2026, VN Accounting and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Bao Cao Chi Phi Khong Duoc Tru"] = {
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
			fieldname: "account",
			label: __("Tài khoản"),
			fieldtype: "Link",
			options: "Account",
			get_query: () => ({
				filters: {
					company: frappe.query_report.get_filter_value("company"),
					is_group: 0,
				},
			}),
		},
		{
			fieldname: "voucher_type",
			label: __("Loại CT"),
			fieldtype: "Select",
			options: [
				"",
				"Journal Entry",
				"Purchase Invoice",
				"Expense Claim",
				"Salary Slip",
			].join("\n"),
		},
		{
			fieldname: "non_deductible_reason",
			label: __("Lý do"),
			fieldtype: "Select",
			options: [
				"",
				"Không HĐ hợp lệ",
				"Vượt định mức quy định",
				"Không liên quan SXKD",
				"Tiền phạt (thuế / BHXH / hợp đồng)",
				"Related-party không TP doc",
				"Khác",
			].join("\n"),
		},
	],

	formatter(value, row, column, data, default_formatter) {
		if (data && data.account && String(data.account).startsWith("TỔNG CỘNG")) {
			value = `<strong>${default_formatter(value, row, column, data)}</strong>`;
			return value;
		}
		return default_formatter(value, row, column, data);
	},
};
