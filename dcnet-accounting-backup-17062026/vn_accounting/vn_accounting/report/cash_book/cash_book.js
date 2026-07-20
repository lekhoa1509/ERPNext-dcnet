// Copyright (c) 2026, Long and Contributors
// License: GNU General Public License v3. See license.txt

frappe.query_reports["Cash Book"] = {
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
			fieldname: "cash_account",
			label: __("Tài khoản tiền mặt"),
			fieldtype: "Link",
			options: "Account",
			get_query: function () {
				return {
					filters: {
						company: frappe.query_report.get_filter_value("company"),
						name: ["like", "111%"],
						is_group: 0,
					},
				};
			},
		},
		{
			fieldname: "transaction_type",
			label: __("Loại giao dịch"),
			fieldtype: "Select",
			options: "\nThu\nChi",
			default: "",
		},
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			default: frappe.datetime.add_months(frappe.datetime.get_today(), -1),
			reqd: 1,
			width: "80px",
		},
		{
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Date",
			default: frappe.datetime.get_today(),
			reqd: 1,
			width: "80px",
		},
	],

	onload: function (report) {
		report.page.add_inner_button(__("Nhận thanh toán"), function () {
			frappe.new_doc("Payment Entry", {
				payment_type: "Receive",
				mode_of_payment: "Cash",
			});
		});

		report.page.add_inner_button(__("Chi thanh toán"), function () {
			frappe.new_doc("Payment Entry", {
				payment_type: "Pay",
				mode_of_payment: "Cash",
			});
		});

		report.page.add_inner_button(__("Bút toán tiền mặt"), function () {
			frappe.new_doc("Journal Entry", {
				voucher_type: "Cash Entry",
			});
		});
	},
};
