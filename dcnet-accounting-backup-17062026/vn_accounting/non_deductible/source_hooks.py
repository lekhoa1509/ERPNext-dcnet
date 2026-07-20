"""Phase 2 — Source-doc on_submit propagation hooks.

When source docs (PI / EC / Salary Slip / Asset Depreciation) submit, ERPNext
core creates GL Entry rows directly. These hooks run AFTER to mirror the
is_non_deductible flag from source items onto matching GL Entry rows.
"""
from __future__ import annotations

import frappe

from .helper import (
	REASON_NO_INVOICE,
	REASON_OVER_LIMIT,
	REASON_NOT_SXKD,
	REASON_PENALTY,
	REASON_OTHER,
)


def _set_gl_flag(gl_name: str, reason: str) -> None:
	"""Idempotent GL Entry flag setter."""
	frappe.db.set_value(
		"GL Entry", gl_name,
		{"is_non_deductible": 1, "non_deductible_reason": (reason or "")[:100]},
		update_modified=False,
	)


def _find_gl_for_voucher_detail(voucher_type: str, voucher_no: str, voucher_detail_no: str) -> list[str]:
	return frappe.db.sql_list(
		"""SELECT name FROM `tabGL Entry`
		   WHERE voucher_type = %s
		     AND voucher_no = %s
		     AND voucher_detail_no = %s
		     AND is_cancelled = 0
		     AND debit > 0""",
		(voucher_type, voucher_no, voucher_detail_no),
	)


def _find_gl_for_voucher_account(voucher_type: str, voucher_no: str, account: str) -> list[str]:
	return frappe.db.sql_list(
		"""SELECT name FROM `tabGL Entry`
		   WHERE voucher_type = %s
		     AND voucher_no = %s
		     AND account = %s
		     AND is_cancelled = 0
		     AND debit > 0""",
		(voucher_type, voucher_no, account),
	)


# ──────────────────────────────────────────────────────────────────────────────
# Purchase Invoice
# ──────────────────────────────────────────────────────────────────────────────

def on_purchase_invoice_validate(doc, method=None):
	"""Auto-flag PI Items when supplier disabled (NCC ngừng hoạt động).

	Note: bill_no missing is NOT auto-flagged here because procurement workflow
	often enters bill_no later. KTT can flag manually if known invoice-less.
	"""
	if not doc.supplier:
		return
	supplier_disabled = frappe.db.get_value("Supplier", doc.supplier, "disabled") or 0
	if not supplier_disabled:
		return
	for it in doc.get("items") or []:
		if not bool(getattr(it, "is_non_deductible", 0)):
			it.is_non_deductible = 1
			it.non_deductible_reason = REASON_NO_INVOICE


def on_purchase_invoice_submit(doc, method=None):
	"""Mirror PI Item flags → matching GL Entry rows."""
	flagged = [
		it for it in (doc.get("items") or [])
		if bool(getattr(it, "is_non_deductible", 0))
	]
	for it in flagged:
		reason = (getattr(it, "non_deductible_reason", "") or "")
		# PI Item GL: voucher_detail_no = PI Item.name
		gl_names = _find_gl_for_voucher_detail("Purchase Invoice", doc.name, it.name)
		# Fallback: match by account if voucher_detail_no not populated
		if not gl_names and getattr(it, "expense_account", None):
			gl_names = _find_gl_for_voucher_account("Purchase Invoice", doc.name, it.expense_account)
		for gl in gl_names:
			_set_gl_flag(gl, reason)


# ──────────────────────────────────────────────────────────────────────────────
# Expense Claim
# ──────────────────────────────────────────────────────────────────────────────

def on_expense_claim_submit(doc, method=None):
	"""Mirror Expense Claim Detail flags → matching GL Entry rows."""
	flagged = [
		d for d in (doc.get("expenses") or [])
		if bool(getattr(d, "is_non_deductible", 0))
	]
	for d in flagged:
		reason = (getattr(d, "non_deductible_reason", "") or "")
		gl_names = _find_gl_for_voucher_detail("Expense Claim", doc.name, d.name)
		if not gl_names and getattr(d, "default_account", None):
			gl_names = _find_gl_for_voucher_account("Expense Claim", doc.name, d.default_account)
		for gl in gl_names:
			_set_gl_flag(gl, reason)


# ──────────────────────────────────────────────────────────────────────────────
# Salary Slip
# ──────────────────────────────────────────────────────────────────────────────

def on_salary_slip_submit(doc, method=None):
	"""Mirror Salary Component config flag → matching GL Entry rows.

	Salary Component carries the persistent flag — when present in a slip's
	earnings or deductions, mirror onto the corresponding GL Entry rows.
	"""
	non_ded_components = {}  # account → reason
	for row in (doc.get("earnings") or []) + (doc.get("deductions") or []):
		comp = row.salary_component
		if not comp:
			continue
		comp_data = frappe.db.get_value(
			"Salary Component", comp,
			["is_non_deductible", "non_deductible_reason"],
			as_dict=True,
		) or {}
		if not comp_data.get("is_non_deductible"):
			continue
		account = getattr(row, "account", None) or comp_data.get("account") or ""
		reason = comp_data.get("non_deductible_reason") or REASON_OTHER
		if account:
			non_ded_components[account] = reason
	for account, reason in non_ded_components.items():
		gl_names = _find_gl_for_voucher_account("Salary Slip", doc.name, account)
		for gl in gl_names:
			_set_gl_flag(gl, reason)


# ──────────────────────────────────────────────────────────────────────────────
# Asset Depreciation (auto-JE created by cron / asset.depreciation_schedule)
# ──────────────────────────────────────────────────────────────────────────────

def on_depreciation_je_submit(doc, method=None):
	"""When a Depreciation JE is submitted, check linked Asset.is_welfare_asset.

	Frappe creates depreciation JE with voucher_type=Journal Entry and remarks
	referencing the asset. Better approach: check JE Account rows for asset ref.
	"""
	if doc.voucher_type != "Depreciation Entry":
		return
	asset_names = set()
	for row in doc.get("accounts") or []:
		if getattr(row, "reference_type", "") == "Asset" and getattr(row, "reference_name", None):
			asset_names.add(row.reference_name)
	if not asset_names:
		return
	welfare = frappe.db.get_all(
		"Asset",
		filters={"name": ["in", list(asset_names)], "is_welfare_asset": 1},
		pluck="name",
	)
	if not welfare:
		return
	# Mark every expense row tied to a welfare asset
	for row in doc.get("accounts") or []:
		if (
			getattr(row, "reference_type", "") == "Asset"
			and row.reference_name in welfare
			and (row.debit_in_account_currency or 0) > 0
		):
			row.is_non_deductible = 1
			row.non_deductible_reason = REASON_NOT_SXKD
	# Propagate via standard JE propagation (called from same on_submit chain)
	from .je_hooks import propagate_to_gl_entry
	propagate_to_gl_entry(doc)
