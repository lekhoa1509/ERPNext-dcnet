"""Journal Entry hooks for non-deductible flag.

- validate: ensure reason set when flag=1; auto-tick when reason chosen
- on_submit: propagate flag from JE Account row → GL Entry rows (since ERPNext
  creates GL Entry rows AFTER doc submit, this runs after make_gl_entries())
"""
from __future__ import annotations

import frappe
from frappe import _


def validate_non_deductible(doc, method=None):
	"""Ensure reason chosen when is_non_deductible=1.

	If user picked a reason but forgot to tick → auto-tick (helpful UX).
	"""
	for row in doc.get("accounts") or []:
		flag = bool(getattr(row, "is_non_deductible", 0))
		reason = (getattr(row, "non_deductible_reason", "") or "").strip()
		if flag and not reason:
			frappe.throw(
				_("Dòng {0}: Phải chọn lý do khi đánh dấu Không được trừ (TNDN).").format(row.idx),
				title=_("Thiếu lý do non-deductible"),
			)
		if reason and not flag:
			row.is_non_deductible = 1


def propagate_to_gl_entry(doc, method=None):
	"""After JE submit, mirror is_non_deductible flag from JE Account → GL Entry.

	Runs on_submit AFTER ERPNext's core on_submit (which creates the GL entries).
	Match by (voucher_no, account, debit, credit) — JE doesn't populate
	GL Entry.voucher_detail_no with the JE Account row name (it uses
	reference_detail_no instead, which is for advance/reference linking).
	"""
	flagged_rows = [
		row for row in (doc.get("accounts") or [])
		if bool(getattr(row, "is_non_deductible", 0))
	]
	if not flagged_rows:
		return

	for row in flagged_rows:
		reason = (getattr(row, "non_deductible_reason", "") or "")[:100]
		debit = float(row.debit_in_account_currency or 0)
		credit = float(row.credit_in_account_currency or 0)
		# Match GL Entry by (voucher_no, account, debit, credit) — unique within a JE
		# unless the same account appears twice with identical amounts (rare).
		gl_names = frappe.db.sql_list(
			"""SELECT name FROM `tabGL Entry`
			   WHERE voucher_type = 'Journal Entry'
			     AND voucher_no = %s
			     AND account = %s
			     AND ABS(debit - %s) < 0.01
			     AND ABS(credit - %s) < 0.01
			     AND is_cancelled = 0""",
			(doc.name, row.account, debit, credit),
		)
		for gl_name in gl_names:
			frappe.db.set_value(
				"GL Entry", gl_name,
				{"is_non_deductible": 1, "non_deductible_reason": reason},
				update_modified=False,
			)


def clear_on_je_cancel(doc, method=None):
	"""On JE cancel, ERPNext sets GL Entry.is_cancelled=1 — flag stays for audit.

	No action needed: the report query filters is_cancelled=0.
	Placeholder for symmetry / future hook chaining.
	"""
	return
