// Frappe v16 auto-renders Percent fields as a progress bar in list view, which
// reads as "% complete". For Term Deposit:
//   * interest_rate / early_withdrawal_rate are rates, NOT progress — render
//     as plain "X% / năm" text + clarifying tooltip.
//   * maturity_date IS a meaningful progress signal — render the date plus a
//     real bar of "% kỳ hạn đã qua" (time elapsed from start_date to today
//     vs total term) with tooltip.
function _render_rate(value, tooltip) {
	if (value === null || value === undefined || value === "") return "";
	const pct = flt(value, 2);
	return `<span title="${frappe.utils.escape_html(tooltip)}">${pct}% / ${__("năm")}</span>`;
}

frappe.listview_settings["Term Deposit"] = {
	add_fields: ["start_date", "maturity_date", "docstatus", "status"],
	formatters: {
		interest_rate(value) {
			return _render_rate(
				value,
				__("Lãi suất danh nghĩa hằng năm — không phải tiến độ đáo hạn"),
			);
		},
		early_withdrawal_rate(value) {
			return _render_rate(
				value,
				__("Lãi suất áp dụng nếu tất toán trước hạn — không phải tiến độ"),
			);
		},
		maturity_date(value, df, doc) {
			const formatted = value
				? frappe.format(value, { fieldtype: "Date" }, null, doc)
				: "";
			if (doc.docstatus !== 1 || !doc.start_date || !value) return formatted;
			const start = frappe.datetime.str_to_obj(doc.start_date);
			const end = frappe.datetime.str_to_obj(value);
			const today = frappe.datetime.str_to_obj(frappe.datetime.now_date());
			const total = end - start;
			if (total <= 0) return formatted;
			const elapsed = today - start;
			const pct = Math.max(0, Math.min(100, (elapsed / total) * 100));
			const tip = `${__("Kỳ hạn đã qua")}: ${pct.toFixed(1)}%`;
			return `
				<div title="${frappe.utils.escape_html(tip)}">
					<div>${formatted}</div>
					<div class="progress" style="height:6px; margin-top:3px; background:#e5e7eb;">
						<div class="progress-bar" style="width:${pct}%; background:#0ea5e9;"></div>
					</div>
				</div>`;
		},
	},
};
