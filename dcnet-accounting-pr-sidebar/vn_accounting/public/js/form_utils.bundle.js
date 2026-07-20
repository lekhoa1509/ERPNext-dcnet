// vn_accounting form utilities — shared helpers for DocType controllers.
//
// Currently exposes:
//   vn_accounting.render_linked_journal_entries(frm)
//     Surfaces every Journal Entry that references frm.doc via
//     reference_type+reference_name. Used by Bank Loan, Term Deposit,
//     and Cash Count forms to give users one-click access to related
//     JV/PE entries without digging through Accounting reports.
//
// History: started inline in bank_loan.js (FB-525/527), copied into
// term_deposit.js, and extracted here when cash_count.js became the
// 3rd consumer (FB-513). See ~/.claude/rules/programming.md
// "rule of three" — third consumer triggers extraction.

(function () {
	window.vn_accounting = window.vn_accounting || {};

	const STATUS_MAP = { 0: "Nháp", 1: "Đã duyệt", 2: "Đã hủy" };
	const VOUCHER_TYPE_LABELS = {
		"Journal Entry": "Bút toán",
		"Bank Entry": "Bút toán ngân hàng",
		"Cash Entry": "Bút toán tiền mặt",
		"Contra Entry": "Bút toán đối ứng",
		"Depreciation Entry": "Bút toán khấu hao",
		"Opening Entry": "Bút toán khai mạc",
		"Write Off Entry": "Bút toán xóa nợ",
	};

	// render_linked_journal_entries(frm, options?)
	//   options.je_names: optional explicit list of JE names. When provided, we
	//     skip the JE Account reference_type lookup and use this list directly.
	//     Useful for DocTypes that store JE references as direct Link fields
	//     on themselves (e.g. Cash Count → pending_je / resolution_je) instead
	//     of via Journal Entry Account.reference_type/_name.
	//   options.title: optional panel heading (defaults to "Bút toán liên quan").
	window.vn_accounting.render_linked_journal_entries = async function (frm, options) {
		options = options || {};
		const mount_class = "vn-linked-jes-box";
		$(frm.wrapper).find("." + mount_class).remove();
		if (frm.is_new()) return;

		// Query parent Journal Entry directly with a child-table filter.
		// Querying `Journal Entry Account` (child) hits a 403 because Accounts roles
		// only carry DocPerm on the parent; Frappe parent-child filter syntax JOINs
		// the child table while running the permission check on the parent.
		let je_resp;
		if (options.je_names) {
			const names = [...new Set(options.je_names.filter(Boolean))];
			if (!names.length) return;
			je_resp = await frappe.call({
				method: "frappe.client.get_list",
				args: {
					doctype: "Journal Entry",
					filters: { name: ["in", names] },
					fields: ["name", "posting_date", "voucher_type", "total_debit", "docstatus", "user_remark"],
					limit_page_length: 200,
					order_by: "posting_date desc",
				},
			});
		} else {
			je_resp = await frappe.call({
				method: "frappe.client.get_list",
				args: {
					doctype: "Journal Entry",
					filters: [
						["Journal Entry Account", "reference_type", "=", frm.doc.doctype],
						["Journal Entry Account", "reference_name", "=", frm.doc.name],
					],
					fields: ["name", "posting_date", "voucher_type", "total_debit", "docstatus", "user_remark"],
					limit_page_length: 200,
					order_by: "posting_date desc",
				},
			});
		}
		const jes = je_resp.message || [];
		if (!jes.length) return;

		const rows = jes
			.map(
				(je) => `
				<tr>
					<td>${frappe.format(je.posting_date, { fieldtype: "Date" })}</td>
					<td><a href="/app/journal-entry/${encodeURIComponent(je.name)}">${frappe.utils.escape_html(je.name)}</a></td>
					<td>${frappe.utils.escape_html(__(VOUCHER_TYPE_LABELS[je.voucher_type] || je.voucher_type || ""))}</td>
					<td class="text-right">${format_currency(je.total_debit || 0)}</td>
					<td>${__(STATUS_MAP[je.docstatus] || "")}</td>
					<td>${frappe.utils.escape_html(je.user_remark || "")}</td>
				</tr>`
			)
			.join("");
		const title = options.title || __("Bút toán liên quan");
		const html = `
			<div class="${mount_class}" style="margin: 20px 15px 0;">
				<h6 style="margin-bottom: 8px;">${frappe.utils.escape_html(title)}</h6>
				<div class="table-responsive">
					<table class="table table-bordered table-sm" style="margin-bottom: 0;">
						<thead><tr>
							<th>${__("Ngày")}</th>
							<th>${__("Số chứng từ")}</th>
							<th>${__("Loại")}</th>
							<th class="text-right">${__("Số tiền")}</th>
							<th>${__("Trạng thái")}</th>
							<th>${__("Diễn giải")}</th>
						</tr></thead>
						<tbody>${rows}</tbody>
					</table>
				</div>
			</div>`;
		$(frm.wrapper).find(".layout-main-section").first().append(html);
	};
})();
