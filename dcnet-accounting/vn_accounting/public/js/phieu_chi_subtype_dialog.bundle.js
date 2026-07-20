/**
 * Phieu Chi Sub-Type Dialog
 *
 * When user opens Journal Entry from sidebar "+ Phiếu chi" link
 * (URL has naming_series=PC-.YYYY.-), show a sub-type picker dialog
 * and pre-fill the accounts table with TK Có (credit account) based on
 * the selected sub-type. TK Nợ (debit account) defaults to company's
 * cash account (TK 1111).
 */
(function () {
	const NAMING_SERIES_PC = "PC-.YYYY.-";

	// Sub-type → credit account number prefix
	const SUBTYPE_TO_CREDIT_PREFIX = {
		"Trả NCC": "331",
		"Nộp thuế": "3331",
		"Đóng BHXH": "338",
		"Trả lương": "334",
		"Tạm ứng nhân viên": "141",
		"Khác": null,
	};

	const SUBTYPE_OPTIONS = [
		"Trả NCC",
		"Nộp thuế",
		"Đóng BHXH",
		"Trả lương",
		"Tạm ứng nhân viên",
		"Khác",
	];

	function isPhieuChiContext(frm) {
		// URL query has naming_series=PC-.YYYY.- ?
		const url = window.location.href;
		if (url.indexOf("naming_series=PC-.YYYY.-") !== -1) {
			return true;
		}
		// frappe.route_options.naming_series === PC-.YYYY.- ?
		if (frappe.route_options && frappe.route_options.naming_series === NAMING_SERIES_PC) {
			return true;
		}
		// frm.doc.naming_series already set to PC-.YYYY.-
		if (frm && frm.doc && frm.doc.naming_series === NAMING_SERIES_PC) {
			return true;
		}
		return false;
	}

	async function resolveCashAccount(company) {
		if (!company) return null;
		// 1. Company default
		try {
			const resp = await frappe.db.get_value("Company", company, "default_cash_account");
			if (resp && resp.message && resp.message.default_cash_account) {
				return resp.message.default_cash_account;
			}
		} catch (e) { /* fall through */ }
		// 2. Lookup by account_number prefix 1111
		try {
			const list = await frappe.db.get_list("Account", {
				filters: {
					company,
					account_number: ["like", "1111%"],
					is_group: 0,
				},
				fields: ["name"],
				limit: 1,
			});
			if (list && list.length) return list[0].name;
		} catch (e) { /* fall through */ }
		return null;
	}

	async function resolveAccountByPrefix(company, prefix) {
		if (!company || !prefix) return null;
		try {
			const list = await frappe.db.get_list("Account", {
				filters: {
					company,
					account_number: ["like", `${prefix}%`],
					is_group: 0,
				},
				fields: ["name"],
				limit: 1,
			});
			if (list && list.length) return list[0].name;
		} catch (e) { /* fall through */ }
		return null;
	}

	async function applySubtype(frm, subtype) {
		const company = frm.doc.company || frappe.defaults.get_default("company");
		if (!company) {
			frappe.msgprint(__("Vui lòng chọn Công ty trước khi chọn loại phiếu chi."));
			return;
		}
		if (!frm.doc.company) {
			frm.set_value("company", company);
		}
		frm.set_value("user_remark", `Phiếu chi: ${subtype}`);

		if (subtype === "Khác") {
			// User picks freely — no autofill
			return;
		}
		const creditPrefix = SUBTYPE_TO_CREDIT_PREFIX[subtype];
		if (!creditPrefix) return;

		const [cashAccount, creditAccount] = await Promise.all([
			resolveCashAccount(company),
			resolveAccountByPrefix(company, creditPrefix),
		]);

		if (!creditAccount) {
			frappe.msgprint(
				__(`Không tìm thấy tài khoản với prefix ${creditPrefix} trong công ty ${company}. Vui lòng nhập thủ công.`)
			);
		}
		if (!cashAccount) {
			frappe.msgprint(
				__("Không tìm thấy tài khoản tiền mặt mặc định (TK 1111). Vui lòng nhập thủ công.")
			);
		}

		// Clear existing accounts table
		frm.clear_table("accounts");

		// Row 1: TK Nợ (debit) — credit-side counterpart account
		const row1 = frm.add_child("accounts");
		if (creditAccount) row1.account = creditAccount;
		row1.debit_in_account_currency = 0;
		row1.credit_in_account_currency = 0;

		// Row 2: TK Có (credit) — cash account TK 1111
		const row2 = frm.add_child("accounts");
		if (cashAccount) row2.account = cashAccount;
		row2.debit_in_account_currency = 0;
		row2.credit_in_account_currency = 0;

		frm.refresh_field("accounts");
	}

	function showSubtypeDialog(frm) {
		frappe.prompt(
			[
				{
					fieldname: "subtype",
					fieldtype: "Select",
					label: __("Loại phiếu chi"),
					options: SUBTYPE_OPTIONS.join("\n"),
					default: "Trả NCC",
					reqd: 1,
				},
			],
			function (values) {
				applySubtype(frm, values.subtype);
			},
			__("Chọn loại phiếu chi"),
			__("Tiếp tục")
		);
	}

	function _maybeShowDialog(frm) {
		if (!frm.is_new()) return;
		if (!isPhieuChiContext(frm)) return;
		// Only when no account row has been filled (new JE always has 1 empty row)
		if (frm.doc.accounts && frm.doc.accounts.some(r => r.account)) return;
		// Only once per form session
		if (frm.__phieu_chi_dialog_shown) return;
		frm.__phieu_chi_dialog_shown = true;
		setTimeout(() => showSubtypeDialog(frm), 300);
	}

	frappe.ui.form.on("Journal Entry", {
		refresh(frm) {
			_maybeShowDialog(frm);
		},
		naming_series(frm) {
			// Also trigger when user manually selects PC-.YYYY.- naming series
			if (frm.doc.naming_series === NAMING_SERIES_PC) {
				frm.__phieu_chi_dialog_shown = false;
				_maybeShowDialog(frm);
			}
		},
	});
})();
