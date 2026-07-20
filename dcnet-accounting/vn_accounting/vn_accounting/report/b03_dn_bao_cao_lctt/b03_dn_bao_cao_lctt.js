// Copyright (c) 2026, VN Accounting and contributors
// For license information, please see license.txt

function _b03_apply_period() {
	const fy = frappe.query_report.get_filter_value("fiscal_year");
	const month = frappe.query_report.get_filter_value("month");
	if (!fy) return;
	frappe.db.get_value("Fiscal Year", fy, ["year_start_date", "year_end_date"]).then((r) => {
		if (!r.message) return;
		const start = r.message.year_start_date;
		const end = r.message.year_end_date;
		if (!month) {
			frappe.query_report.set_filter_value("from_date", start);
			frappe.query_report.set_filter_value("to_date", end);
			return;
		}
		const m = parseInt(month, 10);
		const startYear = parseInt(String(start).slice(0, 4), 10);
		const endYear = parseInt(String(end).slice(0, 4), 10);
		const startMonth = parseInt(String(start).slice(5, 7), 10);
		const targetYear = (m >= startMonth) ? startYear : endYear;
		const mFrom = moment(`${targetYear}-${String(m).padStart(2, "0")}-01`).startOf("month").format("YYYY-MM-DD");
		const mTo = moment(`${targetYear}-${String(m).padStart(2, "0")}-01`).endOf("month").format("YYYY-MM-DD");
		frappe.query_report.set_filter_value("from_date", mFrom);
		frappe.query_report.set_filter_value("to_date", mTo);
	});
}

const _MONTH_OPTIONS_B03 = [
	{ value: "", label: __("Cả năm") },
	...Array.from({ length: 12 }, (_, i) => ({
		value: String(i + 1),
		label: __(`Tháng ${i + 1}`),
	})),
];

frappe.query_reports["B03-DN Bao Cao LCTT"] = {
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
			default: frappe.defaults.get_user_default("fiscal_year"),
			on_change: _b03_apply_period,
		},
		{
			fieldname: "month",
			label: __("Tháng"),
			fieldtype: "Select",
			options: _MONTH_OPTIONS_B03,
			default: "",
			on_change: _b03_apply_period,
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
