// Copyright (c) 2026, DCNet and Contributors
// License: MIT

frappe.ui.form.on("Cash Count", {
	refresh(frm) {
		frm.set_query("cash_account", function () {
			return {
				filters: {
					account_number: ["like", "111%"],
					is_group: 0,
					company: frm.doc.company,
				},
			};
		});

		frm.set_query("difference_account", function () {
			return { filters: { is_group: 0, company: frm.doc.company } };
		});

		frm.set_query("resolution_target_account", function () {
			return { filters: { is_group: 0, company: frm.doc.company } };
		});

		// Status-based buttons
		if (frm.doc.status === "Draft" && !frm.is_new()) {
			frm.add_custom_button(__("Mark as Counted"), function () {
				frm.call("mark_counted").then(() => frm.reload_doc());
			});
		}

		if (frm.doc.status === "Counted") {
			frm.add_custom_button(__("Approve"), function () {
				frm.call("approve").then(() => frm.reload_doc());
			});
		}

		if (frm.doc.status === "Approved" && frm.doc.difference !== 0) {
			frm.add_custom_button(__("Record Difference"), function () {
				frm.call("record_difference").then(() => frm.reload_doc());
			});
		}

		if (frm.doc.status === "Pending Resolution") {
			frm.add_custom_button(__("Resolve Difference"), function () {
				frm.call("resolve_difference").then(() => frm.reload_doc());
			});
		}

		// FB-513: persistent JV panel so the user always sees the JV created by
		// "Xử lý chênh lệch" (and any related entries) instead of a fleeting toast.
		// Cash Count stores its 2 JEs as direct Link fields, so pass them in
		// explicitly rather than going through Journal Entry Account.reference_type.
		vn_accounting.render_linked_journal_entries(frm, {
			je_names: [frm.doc.pending_je, frm.doc.resolution_je],
		});
	},

	cash_account(frm) {
		_fetch_book_balance(frm);
	},

	count_date(frm) {
		_fetch_book_balance(frm);
	},

	show_denomination(frm) {
		if (frm.doc.show_denomination && (!frm.doc.denominations || frm.doc.denominations.length === 0)) {
			const denoms = [500000, 200000, 100000, 50000, 20000, 10000, 5000, 2000, 1000];
			denoms.forEach(function (d) {
				let row = frm.add_child("denominations");
				row.denomination = d;
				row.quantity = 0;
				row.amount = 0;
			});
			frm.refresh_field("denominations");
		}
	},

	resolution_type(frm) {
		if (!frm.doc.resolution_type) return;
		frappe.call({
			method: "frappe.client.get_value",
			args: {
				doctype: "VN Accounting Settings",
				filters: "VN Accounting Settings",
				fieldname: ["employee_receivable_account", "management_expense_account", "other_income_account"],
			},
			callback: function (r) {
				if (!r.message) return;
				const s = r.message;
				const map = {
					"Employee Compensation": s.employee_receivable_account,
					"Management Expense": s.management_expense_account,
					"Return to Owner": null, // cash_account is already set
					"Other Income": s.other_income_account,
				};
				const target = map[frm.doc.resolution_type];
				if (target) {
					frm.set_value("resolution_target_account", target);
				} else if (frm.doc.resolution_type === "Return to Owner") {
					frm.set_value("resolution_target_account", frm.doc.cash_account);
				}
			},
		});
	},
});

frappe.ui.form.on("Cash Count Denomination", {
	quantity(frm, cdt, cdn) {
		let row = locals[cdt][cdn];
		row.amount = (row.denomination || 0) * (row.quantity || 0);
		frm.refresh_field("denominations");
		_recalc_actual(frm);
	},
	denomination(frm, cdt, cdn) {
		let row = locals[cdt][cdn];
		row.amount = (row.denomination || 0) * (row.quantity || 0);
		frm.refresh_field("denominations");
		_recalc_actual(frm);
	},
});

function _fetch_book_balance(frm) {
	if (frm.doc.cash_account && frm.doc.count_date && frm.doc.company) {
		frappe.call({
			method: "vn_accounting.vn_accounting.doctype.cash_count.cash_count.get_book_balance",
			args: {
				cash_account: frm.doc.cash_account,
				count_date: frm.doc.count_date,
				company: frm.doc.company,
			},
			callback: function (r) {
				if (r.message !== undefined) {
					frm.set_value("book_balance", r.message);
				}
			},
		});
	}
}

function _recalc_actual(frm) {
	if (frm.doc.show_denomination && frm.doc.denominations) {
		let total = 0;
		frm.doc.denominations.forEach(function (row) {
			total += row.amount || 0;
		});
		frm.set_value("actual_amount", total);
	}
}
