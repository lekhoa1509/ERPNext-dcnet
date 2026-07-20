/* CCDC Item — inline accounting section (TT99/2025)
 *
 * Handlers: cost, has_vat, vat_rate → rebuild_entries()
 * refresh: "Sổ Cái" button after submit; "Lịch phân bổ" button
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

async function rebuild_entries(frm, force) {
	const cost = _vnd(frm.doc.cost);
	if (!cost) return;

	const existing = frm.doc.accounting_entries || [];
	if (existing.length > 0 && !force) {
		frappe.confirm(
			__("Bút toán đã có dữ liệu. Tạo lại sẽ xóa các dòng hiện tại. Tiếp tục?"),
			() => rebuild_entries(frm, true)
		);
		return;
	}

	const company =
		frm.doc.company ||
		frappe.defaults.get_user_default("Company") ||
		frappe.defaults.get_global_default("company");
	if (!company) return;

	const vatRate = parseFloat(frm.doc.vat_rate) || 10;
	const hasVat = frm.doc.has_vat;

	const [tk242, tk153, tk1331] = await Promise.all([
		_resolveAccount(company, "242"),
		_resolveAccount(company, "153"),
		_resolveAccount(company, "1331"),
	]);

	frm.clear_table("accounting_entries");

	frm.add_child("accounting_entries", {
		account_debit: tk242,
		account_credit: tk153,
		amount: cost,
		description: __("Ghi nhận CCDC trả trước"),
		is_vat: 0,
	});

	if (hasVat && cost > 0) {
		const vatAmt = _vnd(cost * vatRate / 100);
		frm.add_child("accounting_entries", {
			account_debit: tk1331,
			account_credit: tk153,
			amount: vatAmt,
			description: __("VAT đầu vào {0}%", [vatRate]),
			is_vat: 1,
		});
	}

	frm.refresh_field("accounting_entries");
}

frappe.ui.form.on("CCDC Item", {
	refresh(frm) {
		if (frm.doc.docstatus === 1) {
			if (frm.doc.posted_je) {
				frm.add_custom_button(__("Sổ Cái"), () => {
					frappe.set_route("query-report", "General Ledger", {
						voucher_no: frm.doc.posted_je,
					});
				}, __("Mở"));
			}
			frm.add_custom_button(__("Lịch phân bổ"), () => {
				frappe.set_route("List", "CCDC Allocation Schedule", {
					ccdc_item: frm.doc.name,
				});
			}, __("Mở"));
		}
	},

	cost(frm) {
		rebuild_entries(frm, false);
	},

	has_vat(frm) {
		rebuild_entries(frm, false);
	},

	vat_rate(frm) {
		if (frm.doc.has_vat) {
			rebuild_entries(frm, false);
		}
	},
});
