// Frappe v16 auto-renders Percent fields as a progress bar in list view, which
// reads as "% complete". For Bank Loan:
//   * interest_rate is the annual rate, NOT a progress signal — render as
//     plain "X% / năm" text + tooltip clarifying.
//   * outstanding_amount IS a meaningful progress signal — render the currency
//     value plus a real progress bar of "% gốc đã trả" with tooltip.
frappe.listview_settings["Bank Loan"] = {
	add_fields: ["loan_amount", "outstanding_amount", "docstatus", "status"],
	formatters: {
		interest_rate(value) {
			if (value === null || value === undefined || value === "") return "";
			const pct = flt(value, 2);
			const tip = __("Lãi suất danh nghĩa hằng năm — không phải tiến độ trả nợ");
			return `<span title="${frappe.utils.escape_html(tip)}">${pct}% / ${__("năm")}</span>`;
		},
		outstanding_amount(value, df, doc) {
			const formatted = frappe.format(value, { fieldtype: "Currency" }, null, doc);
			const total = flt(doc.loan_amount);
			const remaining = flt(value);
			// Draft / cancelled / no loan amount → just show value, no bar.
			if (doc.docstatus !== 1 || total <= 0) return formatted;
			const paid = Math.max(0, total - remaining);
			const pct = Math.min(100, (paid / total) * 100);
			const tip = `${__("Đã trả gốc")}: ${pct.toFixed(1)}%`;
			return `
				<div title="${frappe.utils.escape_html(tip)}">
					<div>${formatted}</div>
					<div class="progress" style="height:6px; margin-top:3px; background:#e5e7eb;">
						<div class="progress-bar" style="width:${pct}%; background:#16a34a;"></div>
					</div>
				</div>`;
		},
	},
};
