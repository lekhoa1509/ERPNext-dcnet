from frappe import _
from vn_accounting.vn_accounting.report_utils import (
	BANK_PREFIX,
	extract_account_numbers,
	get_accounts_by_prefix,
	get_transactions,
	get_party_link_info,
	party_link_cells,
)
from vn_accounting.vn_accounting.report.bank_account_book.bank_account_book import validate_filters


def execute(filters=None):
	if not filters:
		return [], []
	validate_filters(filters)
	company = filters.get("company")
	accounts = get_accounts_by_prefix(company, BANK_PREFIX, filters.get("bank_account"))
	if not accounts:
		return get_columns(), []
	txns = get_transactions(accounts, filters["from_date"], filters["to_date"], company)
	txns = [t for t in txns if (t.debit or 0) > 0]
	data = [
		{
			"posting_date": t.posting_date,
			"voucher_no": t.voucher_no,
			"voucher_type": t.voucher_type,
			"remarks": t.remarks,
			"against": extract_account_numbers(t.against),
			"amount": t.debit,
		}
		for t in txns
	]
	# Gắn cột Đối tác / Hóa đơn để rà giao dịch mồ côi (chạm TK công nợ mà
	# thiếu đối tác/hóa đơn). JE/chi phí trực tiếp → "—". Xem report_utils.
	link_info = get_party_link_info([r["voucher_no"] for r in data], company)
	for r in data:
		r["party"], r["invoice"] = party_link_cells(link_info.get(r["voucher_no"]))
	total = sum(r["amount"] for r in data)
	data.append({"remarks": _("Tổng cộng"), "amount": total})
	return get_columns(), data


def get_columns():
	return [
		{"label": _("Ngày"), "fieldname": "posting_date", "fieldtype": "Date", "width": 100},
		{"label": _("Số chứng từ"), "fieldname": "voucher_no", "fieldtype": "Dynamic Link", "options": "voucher_type", "width": 180},
		{"label": _("Loại chứng từ"), "fieldname": "voucher_type", "fieldtype": "Data", "width": 120},
		{"label": _("Diễn giải"), "fieldname": "remarks", "fieldtype": "Data", "width": 300},
		{"label": _("TK đối ứng"), "fieldname": "against", "fieldtype": "Data", "width": 150},
		{"label": _("Đối tác"), "fieldname": "party", "fieldtype": "Data", "width": 180},
		{"label": _("Hóa đơn"), "fieldname": "invoice", "fieldtype": "Data", "width": 150},
		{"label": _("Số tiền"), "fieldname": "amount", "fieldtype": "Currency", "width": 150},
	]
