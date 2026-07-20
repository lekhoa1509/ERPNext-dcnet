import frappe
from frappe import _

from vn_accounting.vn_accounting.report_utils import (
	BANK_PREFIX,
	CASH_PREFIX,
	get_accounts_by_prefix,
)


# Voucher DocType name → Vietnamese label for the "Loại chứng từ" column.
# Kept separate from the raw voucher_type field, which the Dynamic Link
# column (voucher_no) needs verbatim to resolve the document URL.
VOUCHER_TYPE_VN = {
	"Journal Entry": "Phiếu kế toán",
	"Payment Entry": "Phiếu thanh toán",
}


def execute(filters=None):
	if not filters:
		return [], []

	validate_filters(filters)
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def validate_filters(filters):
	if not filters.get("company"):
		frappe.throw(_("{0} is mandatory").format(_("Company")))
	if not filters.get("from_date") or not filters.get("to_date"):
		frappe.throw(_("From Date and To Date are mandatory"))
	if filters.get("from_date") > filters.get("to_date"):
		frappe.throw(_("From Date must be before To Date"))


def get_columns():
	return [
		{"label": _("Ngày"), "fieldname": "posting_date", "fieldtype": "Date", "width": 100},
		{"label": _("Số chứng từ"), "fieldname": "voucher_no", "fieldtype": "Dynamic Link", "options": "voucher_type", "width": 180},
		{"label": _("Loại chứng từ"), "fieldname": "voucher_type_label", "fieldtype": "Data", "width": 120},
		{"label": _("Diễn giải"), "fieldname": "remarks", "fieldtype": "Data", "width": 300},
		{"label": _("TK chuyển"), "fieldname": "from_account", "fieldtype": "Data", "width": 180},
		{"label": _("TK nhận"), "fieldname": "to_account", "fieldtype": "Data", "width": 180},
		{"label": _("Số tiền"), "fieldname": "amount", "fieldtype": "Currency", "width": 150},
	]


def get_data(filters):
	company = filters.get("company")
	from_date = filters.get("from_date")
	to_date = filters.get("to_date")

	# All cash + bank leaf accounts for this company
	cash_accounts = get_accounts_by_prefix(company, CASH_PREFIX)
	bank_accounts = get_accounts_by_prefix(company, BANK_PREFIX)
	all_accounts = cash_accounts + bank_accounts
	if not all_accounts:
		return []

	# Find GL entries where both debit and credit sides are cash/bank accounts
	# within the same voucher — that's an internal transfer
	entries = frappe.db.sql(
		"""
		SELECT
			posting_date, voucher_no, voucher_type, remarks,
			account, debit, credit, against
		FROM `tabGL Entry`
		WHERE company = %(company)s
			AND account IN %(accounts)s
			AND posting_date >= %(from_date)s
			AND posting_date <= %(to_date)s
			AND is_cancelled = 0
		ORDER BY posting_date, voucher_no, creation
		""",
		{
			"company": company,
			"accounts": all_accounts,
			"from_date": from_date,
			"to_date": to_date,
		},
		as_dict=True,
	)

	account_set = set(all_accounts)

	# Group by voucher — find vouchers with both debit and credit in cash/bank
	from collections import defaultdict

	voucher_entries = defaultdict(list)
	for e in entries:
		voucher_entries[e.voucher_no].append(e)

	data = []
	for voucher_no, rows in voucher_entries.items():
		debit_rows = [r for r in rows if (r.debit or 0) > 0]
		credit_rows = [r for r in rows if (r.credit or 0) > 0]

		# Both sides must be in cash/bank accounts
		if not debit_rows or not credit_rows:
			continue

		# Check that contra account is also a cash/bank account
		for cr in credit_rows:
			for dr in debit_rows:
				if cr.account != dr.account:
					data.append({
						"posting_date": cr.posting_date,
						"voucher_no": cr.voucher_no,
						"voucher_type": cr.voucher_type,
						"voucher_type_label": VOUCHER_TYPE_VN.get(cr.voucher_type, cr.voucher_type),
						"remarks": cr.remarks,
						"from_account": _short_name(cr.account),
						"to_account": _short_name(dr.account),
						"amount": cr.credit,
					})

	# Sort by date
	data.sort(key=lambda r: r.get("posting_date") or "")

	total = sum(r["amount"] for r in data)
	if data:
		data.append({"remarks": _("Tổng cộng"), "amount": total})

	return data


def _short_name(account_name):
	"""Extract account number from full name like '1121 - Tiền gửi BIDV - DC'."""
	parts = account_name.split(" - ")
	if len(parts) >= 2:
		return f"{parts[0]} - {parts[1]}"
	return account_name
