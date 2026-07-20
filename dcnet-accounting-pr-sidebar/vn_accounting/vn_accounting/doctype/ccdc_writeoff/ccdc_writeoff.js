/* CCDC Writeoff — inline accounting section (TT99/2025)
 *
 * Handlers: ccdc_item, compensation_amount → fetch remaining amounts → rebuild entries
 * refresh: "Sổ Cái" button after submit
 */

function _vnd(v) {
	return Math.round(parseFloat(v) || 0);
}

async function _resolveAccount(company, code) {
	const r = await frappe.db.get_list("Account", {
		filters: { company, account_number: code, is_group: 0 },
		fields: ["name"],
		limit: 1,
	});
	return r && r.length ? r[0].name : code;
}

async function rebuild_writeoff_entries(frm, force) {
	const rem242 = _vnd(frm.doc.remaining_242_amount);
	const rem153 = _vnd(frm.doc.remaining_153_amount);
	const comp = _vnd(frm.doc.compensation_amount);

	if (!rem242 && !rem153 && !comp) return;

	const existing = frm.doc.accounting_entries || [];
	if (existing.length > 0 && !force) {
		frappe.confirm(
			__("Bút toán đã có dữ liệu. Tạo lại sẽ xóa các dòng hiện tại. Tiếp tục?"),
			() => rebuild_writeoff_entries(frm, true)
		);
		return;
	}

	const company = frm.doc.ccdc_item
		? await frappe.db.get_value("CCDC Item", frm.doc.ccdc_item, "company")
		: null;
	if (!company) return;

	const [tk6423, tk242, tk632, tk153, tk1388, tk711] = await Promise.all([
		_resolveAccount(company, "6423"),
		_resolveAccount(company, "242"),
		_resolveAccount(company, "632"),
		_resolveAccount(company, "153"),
		_resolveAccount(company, "1388"),
		_resolveAccount(company, "711"),
	]);

	frm.clear_table("accounting_entries");

	if (rem242 > 0) {
		frm.add_child("accounting_entries", {
			account_debit: tk6423,
			account_credit: tk242,
			amount: rem242,
			description: __("Ghi giảm CCDC — xóa số dư TK 242"),
			is_vat: 0,
		});
	}
	if (rem153 > 0) {
		frm.add_child("accounting_entries", {
			account_debit: tk632,
			account_credit: tk153,
			amount: rem153,
			description: __("Ghi giảm CCDC — xóa số dư TK 153"),
			is_vat: 0,
		});
	}
	if (comp > 0) {
		frm.add_child("accounting_entries", {
			account_debit: tk1388,
			account_credit: tk711,
			amount: comp,
			description: __("Bồi thường ghi giảm CCDC"),
			is_vat: 0,
		});
	}

	frm.refresh_field("accounting_entries");
}

frappe.ui.form.on("CCDC Writeoff", {
	refresh(frm) {
		if (frm.doc.docstatus === 1 && frm.doc.posted_je) {
			frm.add_custom_button(__("Sổ Cái"), () => {
				frappe.set_route("query-report", "General Ledger", {
					voucher_no: frm.doc.posted_je,
				});
			}, __("Mở"));
		}
	},

	ccdc_item(frm) {
		if (!frm.doc.ccdc_item) {
			frm.set_value("remaining_242_amount", 0);
			frm.set_value("remaining_153_amount", 0);
			return;
		}
		frappe.call({
			method: "vn_accounting.vn_accounting.doctype.ccdc_writeoff.ccdc_writeoff.get_writeoff_preview",
			args: { ccdc_item: frm.doc.ccdc_item },
			callback(r) {
				if (r.message) {
					frm.set_value("remaining_242_amount", r.message.remaining_242_amount || 0);
					frm.set_value("remaining_153_amount", r.message.remaining_153_amount || 0);
					rebuild_writeoff_entries(frm, false);
				}
			},
		});
	},

	compensation_amount(frm) {
		if (frm.doc.ccdc_item) {
			rebuild_writeoff_entries(frm, false);
		}
	},
});
