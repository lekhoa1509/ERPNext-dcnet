# Copyright (c) 2026, VN Accounting and contributors
# For license information, please see license.txt

"""Quyết toán TNDN — Reconciliation (Phase 3).

Bridges Lợi nhuận kế toán (B02 KQKD) with Thu nhập chịu thuế và Thuế TNDN phải
nộp. Tích hợp B4 (chi phí không được trừ) tự động từ GL Entry.is_non_deductible.

Output structure mirrors Form 03/TNDN line-by-line:
- A: Lợi nhuận kế toán trước thuế (từ B02)
- B: Các khoản điều chỉnh
  - B4: Chi phí không được trừ (autofill)
  - B5/B6: placeholders (manual entry next session)
- C: Thu nhập chịu thuế
- D: Thuế TNDN phải nộp

Phase 3 spec: docs/specs/2026-05-25-non-deductible-expense-tracking.md
"""

import frappe
from frappe import _
from frappe.utils import flt, getdate, get_first_day, get_last_day, today

DEFAULT_CIT_RATE = 0.20


def execute(filters=None):
	filters = filters or {}
	validate_filters(filters)

	columns = get_columns()
	data = build_reconciliation(filters)
	summary = build_summary(data, filters)
	return columns, data, None, None, summary


def validate_filters(filters):
	if not filters.get("company"):
		frappe.throw(_("Công ty là bắt buộc"))
	if not filters.get("fiscal_year"):
		frappe.throw(_("Năm tài chính là bắt buộc"))
	fy = frappe.db.get_value(
		"Fiscal Year", filters["fiscal_year"],
		["year_start_date", "year_end_date"], as_dict=True,
	)
	if not fy:
		frappe.throw(_("Không tìm thấy năm tài chính {0}").format(filters["fiscal_year"]))
	filters["from_date"] = fy.year_start_date.isoformat()
	filters["to_date"] = fy.year_end_date.isoformat()
	if not filters.get("cit_rate"):
		filters["cit_rate"] = DEFAULT_CIT_RATE * 100  # display %


def get_columns():
	return [
		{"fieldname": "code", "label": _("Mã chỉ tiêu"), "fieldtype": "Data", "width": 110},
		{"fieldname": "label", "label": _("Diễn giải"), "fieldtype": "Data", "width": 380},
		{
			"fieldname": "amount",
			"label": _("Giá trị"),
			"fieldtype": "Currency",
			"options": "Company:company:default_currency",
			"width": 180,
		},
		{"fieldname": "note", "label": _("Ghi chú"), "fieldtype": "Small Text", "width": 320},
	]


def build_reconciliation(filters):
	company = filters["company"]
	from_date = filters["from_date"]
	to_date = filters["to_date"]
	cit_rate = flt(filters.get("cit_rate", DEFAULT_CIT_RATE * 100)) / 100.0

	# A. Lợi nhuận kế toán — Doanh thu (5xx, 711) - CP (6xx, 8xx) trừ Period-Closing
	revenue = _sum_root_type(company, from_date, to_date, "Income")
	expense = _sum_root_type(company, from_date, to_date, "Expense")
	accounting_profit = revenue - expense

	# B4: Chi phí không được trừ
	b4 = _sum_non_deductible(company, from_date, to_date)

	taxable_income = accounting_profit + b4
	cit_payable = taxable_income * cit_rate if taxable_income > 0 else 0
	cit_on_accounting = accounting_profit * cit_rate if accounting_profit > 0 else 0
	effective_rate = (cit_payable / accounting_profit * 100) if accounting_profit > 0 else 0

	rows = [
		{"code": "", "label": _("─── A. LỢI NHUẬN KẾ TOÁN ───"), "amount": None, "note": ""},
		{"code": "A1", "label": _("Doanh thu thuần (TK 511, 515, 711)"), "amount": revenue, "note": _("Tổng credit - debit của TK Income")},
		{"code": "A2", "label": _("Tổng chi phí (TK 6xx, 8xx)"), "amount": expense, "note": _("Tổng debit - credit của TK Expense")},
		{"code": "A",  "label": _("Lợi nhuận kế toán trước thuế"), "amount": accounting_profit, "note": _("A = A1 - A2")},
		{"code": "", "label": "", "amount": None, "note": ""},
		{"code": "", "label": _("─── B. ĐIỀU CHỈNH ───"), "amount": None, "note": ""},
		{"code": "B4", "label": _("Chi phí không được trừ"), "amount": b4, "note": _("Tự động từ GL Entry.is_non_deductible — chi tiết xem BC chi phí không được trừ")},
		{"code": "B5", "label": _("Lỗ từ năm trước chuyển sang"), "amount": 0, "note": _("(Nhập tay nếu có)")},
		{"code": "B6", "label": _("Thu nhập miễn thuế"), "amount": 0, "note": _("(Nhập tay nếu có)")},
		{"code": "", "label": "", "amount": None, "note": ""},
		{"code": "", "label": _("─── C. THU NHẬP CHỊU THUẾ ───"), "amount": None, "note": ""},
		{"code": "C",  "label": _("Thu nhập chịu thuế"), "amount": taxable_income, "note": _("C = A + B4 - B5 - B6")},
		{"code": "",   "label": _("Thuế suất TNDN áp dụng"), "amount": cit_rate * 100, "note": _("%")},
		{"code": "D",  "label": _("Thuế TNDN phải nộp"), "amount": cit_payable, "note": _("D = C × thuế suất, nếu C > 0")},
		{"code": "", "label": "", "amount": None, "note": ""},
		{"code": "", "label": _("─── PHÂN TÍCH HIỆU LỰC ───"), "amount": None, "note": ""},
		{"code": "X1", "label": _("Thuế TNDN theo LN kế toán (LN × 20%)"), "amount": cit_on_accounting, "note": _("Đối chiếu — KHÔNG phải số phải nộp")},
		{"code": "X2", "label": _("Chênh lệch (D - X1)"), "amount": cit_payable - cit_on_accounting, "note": _("Chênh lệch do điều chỉnh B4, B5, B6")},
		{"code": "X3", "label": _("Tỷ lệ thuế hiệu lực"), "amount": effective_rate, "note": _("% — thuế thực nộp / LN kế toán")},
	]
	return rows


def _sum_root_type(company: str, from_date: str, to_date: str, root_type: str) -> float:
	"""Sum GL Entry net movement for accounts of a given root_type within period.

	Income: credit - debit (positive = revenue)
	Expense: debit - credit (positive = expense)
	Filters out Period Closing Voucher to avoid double-counting closing entries.
	"""
	rows = frappe.db.sql(
		"""SELECT COALESCE(SUM(gle.credit - gle.debit), 0) AS cr_dr,
		          COALESCE(SUM(gle.debit - gle.credit), 0) AS dr_cr
		   FROM `tabGL Entry` gle
		   JOIN tabAccount acc ON acc.name = gle.account
		   WHERE gle.company = %s
		     AND gle.posting_date BETWEEN %s AND %s
		     AND gle.is_cancelled = 0
		     AND gle.voucher_type != 'Period Closing Voucher'
		     AND acc.root_type = %s""",
		(company, from_date, to_date, root_type),
		as_dict=True,
	)
	if not rows:
		return 0
	if root_type == "Income":
		return float(rows[0].cr_dr or 0)
	return float(rows[0].dr_cr or 0)


def _sum_non_deductible(company: str, from_date: str, to_date: str) -> float:
	"""Sum debit on GL Entry rows flagged is_non_deductible=1."""
	v = frappe.db.sql(
		"""SELECT COALESCE(SUM(gle.debit), 0)
		   FROM `tabGL Entry` gle
		   WHERE gle.company = %s
		     AND gle.posting_date BETWEEN %s AND %s
		     AND gle.is_cancelled = 0
		     AND gle.is_non_deductible = 1
		     AND gle.debit > 0""",
		(company, from_date, to_date),
	)
	return float(v[0][0] or 0) if v else 0


def build_summary(data, filters):
	rows_by_code = {r["code"]: r for r in data if r.get("code")}
	a = rows_by_code.get("A", {}).get("amount") or 0
	b4 = rows_by_code.get("B4", {}).get("amount") or 0
	c = rows_by_code.get("C", {}).get("amount") or 0
	d = rows_by_code.get("D", {}).get("amount") or 0
	x3 = rows_by_code.get("X3", {}).get("amount") or 0
	return [
		{"value": a, "label": _("LN kế toán"), "datatype": "Currency", "indicator": "Blue"},
		{"value": b4, "label": _("CP không trừ (B4)"), "datatype": "Currency", "indicator": "Red" if b4 > 0 else "Green"},
		{"value": c, "label": _("Thu nhập chịu thuế"), "datatype": "Currency"},
		{"value": d, "label": _("Thuế TNDN phải nộp"), "datatype": "Currency", "indicator": "Orange"},
		{"value": f"{x3:.2f}%", "label": _("Tỷ lệ hiệu lực"), "datatype": "Data"},
	]
