// Copyright (c) 2026, VN Accounting and contributors
// For license information, please see license.txt

// Helper — set as_on_date to end-of-month in fiscal year, or end-of-FY when
// month is empty ("Cả năm").
function _b01_apply_period() {
	const fy = frappe.query_report.get_filter_value("fiscal_year");
	const month = frappe.query_report.get_filter_value("month");
	if (!fy) return;
	frappe.db.get_value("Fiscal Year", fy, ["year_start_date", "year_end_date"]).then((r) => {
		if (!r.message) return;
		const start = r.message.year_start_date;
		const end = r.message.year_end_date;
		if (!month) {
			// Full year — snapshot at FY end
			frappe.query_report.set_filter_value("as_on_date", end);
			return;
		}
		// Month chosen — find that month's last day within the fiscal year
		const m = parseInt(month, 10);
		// Calendar year that contains month m within this fiscal year
		const startYear = parseInt(String(start).slice(0, 4), 10);
		const endYear = parseInt(String(end).slice(0, 4), 10);
		const startMonth = parseInt(String(start).slice(5, 7), 10);
		const targetYear = (m >= startMonth) ? startYear : endYear;
		const monthEnd = moment(`${targetYear}-${String(m).padStart(2, "0")}-01`).endOf("month").format("YYYY-MM-DD");
		frappe.query_report.set_filter_value("as_on_date", monthEnd);
	});
}

frappe.query_reports["B01-DN Bao Cao Tinh Hinh Tai Chinh"] = {
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
			on_change: _b01_apply_period,
		},
		{
			fieldname: "month",
			label: __("Tháng"),
			fieldtype: "Select",
			options: [
				{ value: "", label: __("Cả năm") },
				{ value: "1", label: __("Tháng 1") },
				{ value: "2", label: __("Tháng 2") },
				{ value: "3", label: __("Tháng 3") },
				{ value: "4", label: __("Tháng 4") },
				{ value: "5", label: __("Tháng 5") },
				{ value: "6", label: __("Tháng 6") },
				{ value: "7", label: __("Tháng 7") },
				{ value: "8", label: __("Tháng 8") },
				{ value: "9", label: __("Tháng 9") },
				{ value: "10", label: __("Tháng 10") },
				{ value: "11", label: __("Tháng 11") },
				{ value: "12", label: __("Tháng 12") },
			],
			default: "",
			on_change: _b01_apply_period,
		},
		{
			fieldname: "as_on_date",
			label: __("Tại ngày"),
			fieldtype: "Date",
			reqd: 1,
			default: frappe.datetime.year_end(),
			description: __("Số dư tại ngày này (snapshot)."),
		},
	],
};
