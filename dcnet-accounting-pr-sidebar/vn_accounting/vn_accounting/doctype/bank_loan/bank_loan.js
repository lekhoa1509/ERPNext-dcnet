// Copyright (c) 2026, DCNet and Contributors
// License: MIT

frappe.ui.form.on("Bank Loan", {
	async onload(frm) {
		if (!frm.is_new() || !frm.doc.company) return;
		const pairs = [
			["default_loan_account", "loan_account"],
			["default_interest_expense_account", "interest_expense_account"],
			["default_loan_interest_payable", "interest_payable_account"],
		];
		const to_resolve = pairs.filter(([, dest]) => !frm.doc[dest]).map(([src]) => src);
		if (!to_resolve.length) return;
		const r = await frappe.call({
			method: "vn_accounting.utils.account_resolver.resolve_accounts_api",
			args: { fields: JSON.stringify(to_resolve), company: frm.doc.company },
		});
		if (r && r.message) {
			for (const [src, dest] of pairs) {
				if (!frm.doc[dest] && r.message[src]) frm.set_value(dest, r.message[src]);
			}
		}
	},
	refresh(frm) {
		if (frm.doc.status === "Active" && frm.doc.docstatus === 1) {
			frm.add_custom_button(__("Create Accrual Entry"), function () {
				frappe.prompt(
					{ fieldname: "accrual_date", fieldtype: "Date", label: __("Accrual Date"), reqd: 1 },
					function (values) {
						frm.call("create_accrual", { accrual_date: values.accrual_date }).then(() => {
							frm.reload_doc();
						});
					},
					__("Create Accrual Entry"),
					__("Create")
				);
			}, __("Actions"));
		}
		vn_accounting.render_linked_journal_entries(frm);
	}
});
