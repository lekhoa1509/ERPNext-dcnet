// Copyright (c) 2026 DCNET
// Tờ khai thuế GTGT — Mẫu 01/GTGT (TT80/2021) frontend

frappe.query_reports["vat_return_01_gtgt"] = {
	filters: [
		{
			fieldname: "company",
			label: __("Công ty"),
			fieldtype: "Link",
			options: "Company",
			default: frappe.defaults.get_user_default("Company"),
		},
		{
			fieldname: "from_date",
			label: __("Từ ngày"),
			fieldtype: "Date",
			default: frappe.datetime.month_start(),
		},
		{
			fieldname: "to_date",
			label: __("Đến ngày"),
			fieldtype: "Date",
			default: frappe.datetime.month_end(),
		},
		{
			fieldname: "tax_period",
			label: __("Kỳ tính thuế"),
			fieldtype: "Select",
			options: ["Tháng", "Quý"],
			default: "Tháng",
			on_change: function () {
				const val = frappe.query_report.get_filter_value("tax_period");
				const from = frappe.query_report.get_filter("from_date");
				const to = frappe.query_report.get_filter("to_date");
				if (val === "Tháng") {
					from.set_value(frappe.datetime.month_start());
					to.set_value(frappe.datetime.month_end());
				} else {
					from.set_value(frappe.datetime.quarter_start());
					to.set_value(frappe.datetime.quarter_end());
				}
			},
		},
		{
			fieldname: "thue_ky_truoc_chuyen_sang",
			label: __("Thuế GTGT đầu vào được KT kỳ trước chuyển sang [30]"),
			fieldtype: "Currency",
			default: 0,
		},
	],

	formatter: function (value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		if (!data) return value;
		if (column.fieldname === "chi_tieu" && data.bold) {
			value = "<b>" + value + "</b>";
		}
		return value;
	},
};
