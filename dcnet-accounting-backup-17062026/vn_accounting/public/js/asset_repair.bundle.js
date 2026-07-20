/* Asset Repair — inline accounting section (TT99/2025)
 *
 * Handlers: repair_classification, repair_cost, has_vat, vat_rate → rebuild_entries()
 * refresh: override "Accounting Ledger" button to GL filtered by posted_je
 */

/* Default D/C pairs per TT99/2025 §5.1 */
const AR_DEFAULTS = {
	"Chi phí": { debit: "6427", credit: "111" },
	"Sửa chữa lớn vốn hóa": { debit: "2413", credit: "331" },
	"Nâng cấp cải tạo": { debit: "2412", credit: "331" },
};

function _vnd(v) {
	return Math.round(parseFloat(v) || 0);
}

/**
 * Fetch full account names for account_number codes via frappe.call.
 * Returns Promise<{code: accountName}>.
 */
async function _resolveAccounts(company, codes) {
	const result = {};
	await Promise.all(
		codes.map(async (code) => {
			const r = await frappe.db.get_list("Account", {
				filters: { company, account_number: code, is_group: 0 },
				fields: ["name"],
				limit: 1,
			});
			result[code] = r && r.length ? r[0].name : code;
		})
	);
	return result;
}

async function rebuild_entries(frm, force) {
	const cls = frm.doc.repair_classification;
	const cost = _vnd(frm.doc.repair_cost);
	if (!cls || !cost) return;

	const existing = frm.doc.accounting_entries || [];
	if (existing.length > 0 && !force) {
		frappe.confirm(
			__("Bút toán đã có dữ liệu. Tạo lại sẽ xóa các dòng hiện tại. Tiếp tục?"),
			() => rebuild_entries(frm, true)
		);
		return;
	}

	const pair = AR_DEFAULTS[cls];
	if (!pair) return;

	const company =
		frm.doc.company ||
		frappe.defaults.get_user_default("Company") ||
		frappe.defaults.get_global_default("company");

	const vatRate = parseFloat(frm.doc.vat_rate) || 10;
	const hasVat = frm.doc.has_vat;
	const codesToResolve = [pair.debit, pair.credit];
	if (hasVat) codesToResolve.push("1331");

	const accs = await _resolveAccounts(company, [...new Set(codesToResolve)]);

	frm.clear_table("accounting_entries");

	frm.add_child("accounting_entries", {
		account_debit: accs[pair.debit] || pair.debit,
		account_credit: accs[pair.credit] || pair.credit,
		amount: cost,
		description: __("Sửa chữa TSCĐ {0} ({1})", [frm.doc.asset || frm.doc.name, cls]),
		is_vat: 0,
	});

	if (hasVat && cost > 0) {
		const vatAmt = _vnd((cost * vatRate) / 100);
		frm.add_child("accounting_entries", {
			account_debit: accs["1331"] || "1331",
			account_credit: accs[pair.credit] || pair.credit,
			amount: vatAmt,
			description: __("VAT đầu vào {0}%", [vatRate]),
			is_vat: 1,
		});
	}

	frm.refresh_field("accounting_entries");
}

frappe.ui.form.on("Asset Repair", {
	repair_classification(frm) {
		// Classification change is fundamental → confirm before overwriting
		rebuild_entries(frm, false);
	},
	repair_cost(frm) {
		// Amount sync — always re-sync without confirm (VAT row depends on cost)
		rebuild_entries(frm, true);
	},
	has_vat(frm) {
		// VAT toggle must always add/remove the 1331 row, no confirm
		rebuild_entries(frm, true);
	},
	vat_rate(frm) {
		// Rate change must always recompute VAT row, no confirm
		rebuild_entries(frm, true);
	},

	refresh(frm) {
		if (frm.doc.docstatus === 1 && frm.doc.posted_je) {
			/* Lock accounting entries once JE is posted — entries no longer editable.
			 * Force-display the section even when the table has 0 rows (Frappe hides
			 * empty child tables on submitted forms). */
			frm.toggle_display("vn_accounting_section", true);
			frm.toggle_display("accounting_entries", true);
			frm.set_df_property("accounting_entries", "read_only", 1);
			frm.set_df_property("has_vat", "read_only", 1);
			frm.set_df_property("vat_rate", "read_only", 1);

			/* Override "Accounting Ledger" sidebar button to route to GL by JE.
			 * Use a wide from_date so historic JEs (e.g. 2024) are not filtered out
			 * by the GL report's default 30-day window. */
			frm.add_custom_button(
				__("Sổ Cái"),
				() => {
					frappe.route_options = {
						voucher_no: frm.doc.posted_je,
						from_date: "2000-01-01",
						to_date: frappe.datetime.now_date(),
					};
					frappe.set_route("query-report", "General Ledger");
				},
				__("Xem")
			);
		}
	},
});
