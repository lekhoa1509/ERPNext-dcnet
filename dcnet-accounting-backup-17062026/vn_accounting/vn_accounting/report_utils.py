# Copyright (c) 2026, Long and Contributors
# License: GNU General Public License v3. See license.txt

"""Shared utilities for Vietnamese accounting reports.

Functions extracted from Cash Book (Sổ quỹ tiền mặt) and Bank Book
(Sổ tiền gửi ngân hàng) to eliminate duplication.
"""

import frappe

# Account prefix constants (TT99/2025)
# Used by reports and number card methods — single source of truth
CASH_PREFIX = "111%"
BANK_PREFIX = "112%"
REVENUE_PREFIX = "511%"
COGS_PREFIX = "632%"
AR_PREFIX = "131%"
AP_PREFIX = "331%"
# Expense account prefixes (TK 621-642)
EXPENSE_PREFIXES = ("621%", "622%", "623%", "627%", "632%", "635%", "641%", "642%")

# Voucher type display name — English DocType → Vietnamese display.
# Reports keep voucher_type field as English (for Dynamic Link resolution)
# but render this label in the user-facing column.
VOUCHER_TYPE_VN = {
	"Journal Entry": "Bút toán",
	"Payment Entry": "Phiếu thanh toán",
	"Sales Invoice": "Hóa đơn bán hàng",
	"Purchase Invoice": "Hóa đơn mua hàng",
	"Delivery Note": "Phiếu xuất kho",
	"Purchase Receipt": "Phiếu nhập kho",
	"Stock Entry": "Phiếu kho",
	"Sales Order": "Đơn bán hàng",
	"Purchase Order": "Đơn mua hàng",
}


def vn_voucher_type(en_name):
	"""Translate an ERPNext voucher type DocType name to its Vietnamese display label."""
	if not en_name:
		return ""
	return VOUCHER_TYPE_VN.get(en_name, en_name)


def extract_account_numbers(against_str):
	"""Extract account number prefixes from the against field.

	The 'against' field in GL Entry contains full account names like
	'6421 - Chi phi nhan vien - COMPANY'. Extract just the account number part.
	"""
	if not against_str:
		return ""

	parts = []
	for account in against_str.split(","):
		account = account.strip()
		if account:
			# Account format: "NUMBER - Name - Company" -> extract NUMBER
			account_number = account.split(" - ")[0].strip()
			if account_number and account_number not in parts:
				parts.append(account_number)

	return ", ".join(parts)


def get_accounts_by_prefix(company, prefix, specific_account=None):
	"""Get all leaf accounts matching a prefix for the company.

	Args:
		company: Company name.
		prefix: Account number prefix with SQL wildcard (e.g. "111%").
		specific_account: If provided, validate this specific account matches
			the prefix and return only it.

	Returns:
		List of account names (str).
	"""
	if specific_account:
		exists = frappe.db.sql(
			"""
			SELECT name
			FROM `tabAccount`
			WHERE company = %(company)s
				AND name = %(account)s
				AND (account_number LIKE %(account_prefix)s OR name LIKE %(account_prefix)s)
				AND is_group = 0
			""",
			{"company": company, "account": specific_account, "account_prefix": prefix},
			as_dict=True,
		)
		return [specific_account] if exists else []

	accounts = frappe.db.sql(
		"""
		SELECT name
		FROM `tabAccount`
		WHERE company = %(company)s
			AND (account_number LIKE %(account_prefix)s OR name LIKE %(account_prefix)s)
			AND is_group = 0
		""",
		{"company": company, "account_prefix": prefix},
		as_dict=True,
	)
	return [a.name for a in accounts]


def get_opening_balance(accounts, from_date, company):
	"""Calculate opening balance: SUM(debit) - SUM(credit) before from_date."""
	result = frappe.db.sql(
		"""
		SELECT
			COALESCE(SUM(debit), 0) - COALESCE(SUM(credit), 0) AS balance
		FROM `tabGL Entry`
		WHERE company = %(company)s
			AND account IN %(accounts)s
			AND posting_date < %(from_date)s
			AND is_cancelled = 0
		""",
		{"company": company, "accounts": accounts, "from_date": from_date},
		as_dict=True,
	)
	return result[0].balance if result else 0


def split_balance(net: float) -> tuple[float, float]:
	"""Split net (debit-credit) thành (debit, credit) — VAS convention:
	dương → debit cột, âm → credit cột."""
	if net >= 0:
		return float(net), 0.0
	return 0.0, float(-net)


def build_summary_rows(
	opening_debit: float, opening_credit: float,
	period_debit: float, period_credit: float,
	closing_debit: float, closing_credit: float,
	from_date=None, to_date=None,
	remarks_field: str = "remarks",
	debit_field: str = "debit",
	credit_field: str = "credit",
	date_field: str = "posting_date",
) -> list[dict]:
	"""Build 3 dòng tóm tắt VAS để pin ở ĐẦU data table:
	Số dư đầu kỳ → Cộng phát sinh kỳ → Số dư cuối kỳ.

	Mỗi dòng có ``bold=1`` để render đậm. Caller chỉ cần ``data = [*summary, *txns]``.
	"""
	from frappe import _
	def _row(label, dr, cr, dt):
		return {
			date_field: dt,
			"voucher_no": "",
			"voucher_date": None,
			remarks_field: label,
			"against": "",
			debit_field: dr,
			credit_field: cr,
			"bold": 1,
		}
	return [
		_row(_("Số dư đầu kỳ"), opening_debit, opening_credit, from_date),
		_row(_("Cộng phát sinh kỳ"), period_debit, period_credit, None),
		_row(_("Số dư cuối kỳ"), closing_debit, closing_credit, to_date),
	]


def build_summary_cards(
	opening_net: float, period_debit: float, period_credit: float, closing_net: float,
	currency: str = "VND",
) -> list[dict]:
	"""Build Frappe report_summary cards — 4 KPI cards lơ lửng trên data table.

	Format dùng cho execute() return tuple ``(cols, data, message, chart, report_summary)``.
	"""
	from frappe import _
	period_net = period_debit - period_credit
	return [
		{
			"value": opening_net,
			"label": _("Số dư đầu kỳ"),
			"datatype": "Currency", "currency": currency,
			"indicator": "Blue" if opening_net >= 0 else "Orange",
		},
		{
			"value": period_debit,
			"label": _("Phát sinh Nợ trong kỳ"),
			"datatype": "Currency", "currency": currency,
			"indicator": "Green",
		},
		{
			"value": period_credit,
			"label": _("Phát sinh Có trong kỳ"),
			"datatype": "Currency", "currency": currency,
			"indicator": "Red",
		},
		{
			"value": closing_net,
			"label": _("Số dư cuối kỳ"),
			"datatype": "Currency", "currency": currency,
			"indicator": "Blue" if closing_net >= 0 else "Orange",
		},
	]


def get_transactions(accounts, from_date, to_date, company):
	"""Get GL entries for accounts in date range, ordered by posting_date, creation."""
	return frappe.db.sql(
		"""
		SELECT
			posting_date,
			voucher_no,
			voucher_type,
			remarks,
			against,
			debit,
			credit,
			creation
		FROM `tabGL Entry`
		WHERE company = %(company)s
			AND account IN %(accounts)s
			AND posting_date >= %(from_date)s
			AND posting_date <= %(to_date)s
			AND is_cancelled = 0
		ORDER BY posting_date, creation
		""",
		{
			"company": company,
			"accounts": accounts,
			"from_date": from_date,
			"to_date": to_date,
		},
		as_dict=True,
	)


# Party account = TK công nợ cần gắn đối tác/hóa đơn. Receivable/Payable theo
# account_type (131/331) + mở rộng số hiệu 138/338/141 (phải thu/trả khác, tạm ứng).
_PARTY_ACCOUNT_NUMBER_RE = r"^(131|331|138|338|141)"


def get_party_link_info(voucher_nos, company):
	"""Soi các chân GL trên TK công nợ của từng chứng từ để phát hiện "mồ côi".

	Trả về dict: voucher_no -> {"party": str|None, "invoice": str|None, "is_auto": bool}
	CHỈ chứa các chứng từ có chạm TK công nợ (Receivable/Payable hoặc 138/338/141).
	Chứng từ không chạm TK công nợ (chi phí/doanh thu trực tiếp) sẽ KHÔNG có trong
	dict → caller hiển thị "—" (không phải mồ côi).

	- party / invoice: lấy từ chân công nợ (gle.party / gle.against_voucher). None =
	  chưa gắn → caller hiển thị "⚠ Chưa gắn".
	- is_auto: chứng từ do hệ thống tự sinh (DCNet Contract...) → không gắn cờ.
	"""
	voucher_nos = [v for v in set(voucher_nos or []) if v]
	if not voucher_nos:
		return {}

	rows = frappe.db.sql(
		"""
		SELECT gle.voucher_no, gle.party, gle.against_voucher
		FROM `tabGL Entry` gle
		JOIN `tabAccount` acc ON acc.name = gle.account
		WHERE gle.company = %(company)s
			AND gle.is_cancelled = 0
			AND gle.voucher_no IN %(vouchers)s
			AND (acc.account_type IN ('Receivable', 'Payable')
				OR acc.account_number REGEXP %(party_re)s)
		""",
		{"company": company, "vouchers": tuple(voucher_nos),
		 "party_re": _PARTY_ACCOUNT_NUMBER_RE},
		as_dict=True,
	)

	info = {}
	for r in rows:
		d = info.setdefault(r.voucher_no, {"party": None, "invoice": None, "is_auto": False})
		if r.party and not d["party"]:
			d["party"] = r.party
		if r.against_voucher and not d["invoice"]:
			d["invoice"] = r.against_voucher

	if info and frappe.db.exists("DocType", "Auto Generated Doc Registry"):
		auto = {x[0] for x in frappe.db.sql(
			"""SELECT target_name FROM `tabAuto Generated Doc Registry`
			   WHERE target_name IN %(vouchers)s""",
			{"vouchers": tuple(info.keys())},
		)}
		for vn in auto:
			if vn in info:
				info[vn]["is_auto"] = True

	return info


def party_link_cells(rec):
	"""(party_cell, invoice_cell) cho 1 chứng từ. rec = info.get(voucher_no) hoặc None."""
	if not rec:  # không chạm TK công nợ → không cần đối tác/hóa đơn
		return "—", "—"
	if rec.get("is_auto"):  # tự sinh → hiển thị giá trị, không gắn cờ
		return (rec.get("party") or "—"), (rec.get("invoice") or "—")
	return (rec.get("party") or "⚠ Chưa gắn"), (rec.get("invoice") or "⚠ Chưa gắn")
