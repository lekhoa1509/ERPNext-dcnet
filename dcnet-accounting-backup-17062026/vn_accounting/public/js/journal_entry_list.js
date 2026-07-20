/**
 * VN Accounting — Journal Entry List Script
 *
 * FB-2026-00628: ERPNext core's journal_entry_list.js shows `voucher_type` in
 * the list indicator for submitted entries (and the default "Draft" for
 * drafts), so a single indicator column mixes "loại bút toán" with
 * "trạng thái". Override get_indicator to always show a docstatus-based
 * STATUS; voucher_type remains its own data column.
 */
frappe.listview_settings["Journal Entry"] = {
	add_fields: ["voucher_type", "posting_date", "total_debit", "company", "user_remark"],
	get_indicator: function (doc) {
		if (doc.docstatus === 2) {
			return [__("Cancelled"), "grey", "docstatus,=,2"];
		}
		if (doc.docstatus === 1) {
			return [__("Submitted"), "blue", "docstatus,=,1"];
		}
		return [__("Draft"), "red", "docstatus,=,0"];
	},
};
