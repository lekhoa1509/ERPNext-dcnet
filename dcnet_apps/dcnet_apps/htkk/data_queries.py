"""
Query dữ liệu cho các tờ khai HTKK.

Module này HOÀN TOÀN ĐỘC LẬP — không import hay gọi bất kỳ hàm nào
từ localize_vn/report/ (b01_dn, b02_dn, b03_dn).

Tất cả hàm đều nhận param `finance_book` để lọc GL Entry theo sổ kế toán.
"""

import frappe
from frappe.utils import flt

from dcnet_apps.htkk.account_resolver import get_accounts_for_role, get_accounts_by_prefix


# ---------------------------------------------------------------------------
# Finance Book filter helper
# ---------------------------------------------------------------------------

def _finance_book_condition(finance_book):
	"""Trả về SQL condition string cho finance_book filter."""
	if finance_book:
		return (
			" AND (gl.finance_book = %(finance_book)s"
			" OR gl.finance_book IS NULL"
			" OR gl.finance_book = '')"
		)
	return ""


# ---------------------------------------------------------------------------
# GL Entry queries
# ---------------------------------------------------------------------------

def get_gl_balances(company, from_date, to_date, finance_book=None):
	"""
	Query GL Entry phát sinh trong kỳ, group by account_number.

	Returns:
		dict: {account_number: {"debit": x, "credit": y, "balance": debit - credit}}
	"""
	fb_condition = _finance_book_condition(finance_book)

	data = frappe.db.sql("""
		SELECT
			acc.account_number,
			SUM(gl.debit) AS debit,
			SUM(gl.credit) AS credit
		FROM `tabGL Entry` gl
		JOIN `tabAccount` acc ON acc.name = gl.account
		WHERE gl.company = %(company)s
			AND gl.posting_date >= %(from_date)s
			AND gl.posting_date <= %(to_date)s
			AND gl.is_cancelled = 0
			{fb_condition}
		GROUP BY acc.account_number
	""".format(fb_condition=fb_condition), {
		"company": company,
		"from_date": from_date,
		"to_date": to_date,
		"finance_book": finance_book,
	}, as_dict=True)

	result = {}
	for row in data:
		if row.account_number:
			result[row.account_number] = {
				"debit": flt(row.debit),
				"credit": flt(row.credit),
				"balance": flt(row.debit) - flt(row.credit),
			}
	return result


def get_account_balance_up_to(company, to_date, account_codes, finance_book=None):
	"""
	Số dư lũy kế đến to_date cho danh sách mã TK.
	Dùng cho Bảng CĐKT — cần số dư cuối kỳ, không phải phát sinh.

	Args:
		account_codes: list of account_number strings (VD: ["111", "112", "131"])

	Returns:
		dict: {account_number: balance (debit - credit)}
	"""
	if not account_codes:
		return {}

	fb_condition = _finance_book_condition(finance_book)

	# Build IN clause with named parameters
	code_placeholders = ", ".join(["%(code_{i})s".format(i=i) for i in range(len(account_codes))])
	params = {
		"company": company,
		"to_date": to_date,
		"finance_book": finance_book,
	}
	for i, code in enumerate(account_codes):
		params[f"code_{i}"] = code

	data = frappe.db.sql("""
		SELECT
			acc.account_number,
			SUM(gl.debit) - SUM(gl.credit) AS balance
		FROM `tabGL Entry` gl
		JOIN `tabAccount` acc ON acc.name = gl.account
		WHERE gl.company = %(company)s
			AND gl.posting_date <= %(to_date)s
			AND gl.is_cancelled = 0
			AND acc.account_number IN ({code_placeholders})
			{fb_condition}
		GROUP BY acc.account_number
	""".format(code_placeholders=code_placeholders, fb_condition=fb_condition),
		params, as_dict=True)

	return {row.account_number: flt(row.balance) for row in data if row.account_number}


# ---------------------------------------------------------------------------
# VAT Rate Resolution — 2-Layer Fallback Strategy
# ---------------------------------------------------------------------------
#
# Nguyên lý: phân tích từ cấp dòng Item, không từ cấp Invoice.
#
# Ưu tiên 1 — Item Tax Template (chính xác tuyệt đối):
#   Dòng Item có gắn Item Tax Template → lấy rate từ template detail
#   mà account_head trùng với TK thuế GTGT đầu ra/vào.
#
# Ưu tiên 2 — Sales/Purchase Taxes and Charges (mặc định thông minh):
#   Dòng Item không có Item Tax Template → nếu hóa đơn chỉ có 1 mức
#   thuế GTGT duy nhất trong bảng Taxes → gán rate đó cho dòng Item.
#
# Ưu tiên 3 — Không chịu thuế (phòng hờ rủi ro):
#   Nếu không xác định được → mặc định KCT (rate = None, label "KCT").
# ---------------------------------------------------------------------------

# Sentinel value for tax-exempt items
VAT_EXEMPT = "KCT"


def _resolve_item_vat_rate(item_row, invoice_taxes, output_vat_accounts):
	"""
	Xác định VAT rate cho 1 dòng Sales/Purchase Invoice Item.

	Args:
		item_row: dict — dòng item (cần có item_tax_template, item_tax_rate)
		invoice_taxes: list[dict] — bảng Taxes and Charges của hóa đơn
		output_vat_accounts: set — tên các TK thuế GTGT đầu ra/vào

	Returns:
		float or "KCT": VAT rate (VD: 10.0, 8.0, 5.0, 0.0) hoặc "KCT"
	"""
	# --- Ưu tiên 1: Item Tax Template ---
	rate = _rate_from_item_tax_template(item_row, output_vat_accounts)
	if rate is not None:
		return rate

	# --- Ưu tiên 2: Invoice-level Taxes (nếu chỉ 1 mức VAT duy nhất) ---
	rate = _rate_from_invoice_taxes(invoice_taxes, output_vat_accounts)
	if rate is not None:
		return rate

	# --- Ưu tiên 3: Không chịu thuế ---
	return VAT_EXEMPT


def _rate_from_item_tax_template(item_row, vat_accounts):
	"""
	Lấy VAT rate từ Item Tax Template của dòng item.

	item_tax_rate là JSON string: {"Account Head - Company": rate, ...}
	Tìm account head nào trùng với TK thuế GTGT → lấy rate.

	Returns:
		float or None
	"""
	item_tax_rate_json = item_row.get("item_tax_rate")
	if not item_tax_rate_json:
		return None

	import json
	try:
		tax_rates = json.loads(item_tax_rate_json)
	except (json.JSONDecodeError, TypeError):
		return None

	if not tax_rates or not isinstance(tax_rates, dict):
		return None

	# Tìm account head trùng với TK thuế GTGT
	for account_head, rate in tax_rates.items():
		if account_head in vat_accounts:
			return flt(rate)

	# Nếu không match account nào trong vat_accounts, vẫn trả None
	# để fallback sang ưu tiên 2
	return None


def _rate_from_invoice_taxes(invoice_taxes, vat_accounts):
	"""
	Fallback: lấy VAT rate từ bảng Taxes and Charges cấp invoice.

	Chỉ trả về rate nếu có đúng 1 mức thuế GTGT (khác 0 hoặc có giá trị)
	duy nhất trên hóa đơn để có thể gán cho tất cả các dòng Item.

	Returns:
		float or None
	"""
	if not invoice_taxes:
		return None

	resolved_rates = set()
	for tax in invoice_taxes:
		if tax.get("account_head") in vat_accounts:
			rate = flt(tax.get("rate", 0))
			amount = flt(tax.get("base_tax_amount", 0))
			
			# Nếu rate = 0 nhưng có tiền thuế -> thử suy luận rate (VD: HĐ nhập khẩu)
			# Ta chỉ suy luận nếu amount đáng kể (> 100đ)
			if rate == 0 and abs(amount) > 0.01:
				# Ta không có net_total ở đây, nhưng Tax Row thường lưu thông tin này
				# Tuy nhiên tinh thần là ưu tiên rate có sẵn.
				# Nếu rate = 0, ta chỉ gán 0 nếu nó thực sự là mức 0%.
				resolved_rates.add(0.0)
			elif rate != 0:
				resolved_rates.add(rate)

	# Nếu chỉ có 1 mức thuế suất VAT duy nhất được tìm thấy
	if len(resolved_rates) == 1:
		return resolved_rates.pop()

	# Nếu có nhiều mức (VD: vừa 5% vừa 10% trên cùng 1 bảng thuế doc-level)
	# ERPNext không khuyến khích điều này (nên dùng Item Tax Template), 
	# nhưng nếu có, ta không thể tự suy luận dòng nào ứng với rate nào.
	return None


def _get_vat_accounts_set(company, direction="output"):
	"""
	Lấy set tên TK thuế GTGT cho company.

	Args:
		direction: "output" (đầu ra, bán hàng) hoặc "input" (đầu vào, mua hàng)

	Returns:
		set of account names
	"""
	if direction == "output":
		return set(get_accounts_for_role(company, "OUTPUT_VAT"))
	else:
		return set(
			get_accounts_for_role(company, "INPUT_VAT")
			+ get_accounts_for_role(company, "INPUT_VAT_FIXED_ASSET")
		)


# ---------------------------------------------------------------------------
# VAT queries (Tờ khai 01/GTGT)
# ---------------------------------------------------------------------------

def get_vat_summary(company, from_date, to_date, finance_book=None):
	"""
	Tổng hợp thuế GTGT theo thuế suất — phân tích từ cấp dòng Item.

	- Output VAT: tổng hợp từ get_sales_invoices() (item-level, 2-layer fallback)
	- Input VAT: debit TK INPUT_VAT, INPUT_VAT_FIXED_ASSET từ GL Entry

	Returns:
		dict: {
			"output": {"KCT": amount, "0": amount, "5": amount, "8": amount, "10": amount, "total": amount},
			"input": {"goods_services": amount, "fixed_assets": amount, "total": amount},
		}
	"""
	# --- Output VAT: tổng hợp từ item-level analysis ---
	output_vat = {"KCT": 0, "0": 0, "5": 0, "8": 0, "10": 0, "total": 0}

	invoice_lines = get_sales_invoices(company, from_date, to_date)
	for line in invoice_lines:
		rate_key = _vat_rate_to_key(line["vat_rate"])
		if rate_key in output_vat:
			output_vat[rate_key] += flt(line["vat_amount"])
		output_vat["total"] += flt(line["vat_amount"])

	# --- Input VAT: từ GL Entry (vẫn dùng GL vì PI structure tương tự) ---
	fb_condition = _finance_book_condition(finance_book)
	input_goods = get_accounts_for_role(company, "INPUT_VAT")
	input_fa = get_accounts_for_role(company, "INPUT_VAT_FIXED_ASSET")
	input_vat = {"goods_services": 0, "fixed_assets": 0, "total": 0}

	all_input = input_goods + input_fa
	if all_input:
		params_in = {
			"company": company,
			"from_date": from_date,
			"to_date": to_date,
			"finance_book": finance_book,
		}
		for i, acc in enumerate(all_input):
			params_in[f"ia_{i}"] = acc

		placeholders_in = ", ".join(["%(ia_{i})s".format(i=i) for i in range(len(all_input))])

		gl_input = frappe.db.sql("""
			SELECT
				gl.account,
				SUM(gl.debit) - SUM(gl.credit) AS vat_amount
			FROM `tabGL Entry` gl
			WHERE gl.company = %(company)s
				AND gl.posting_date >= %(from_date)s
				AND gl.posting_date <= %(to_date)s
				AND gl.is_cancelled = 0
				AND gl.account IN ({placeholders_in})
				{fb_condition}
			GROUP BY gl.account
		""".format(placeholders_in=placeholders_in, fb_condition=fb_condition),
			params_in, as_dict=True)

		input_goods_set = set(input_goods)
		input_fa_set = set(input_fa)
		for row in gl_input:
			amt = flt(row.vat_amount)
			if row.account in input_goods_set:
				input_vat["goods_services"] += amt
			elif row.account in input_fa_set:
				input_vat["fixed_assets"] += amt

		input_vat["total"] = input_vat["goods_services"] + input_vat["fixed_assets"]

	return {"output": output_vat, "input": input_vat}


def _vat_rate_to_key(rate):
	"""Chuyển VAT rate thành key string cho dict tổng hợp."""
	if rate == VAT_EXEMPT:
		return "KCT"
	r = flt(rate)
	if r == int(r):
		return str(int(r))
	return str(r)


def get_sales_invoices(company, from_date, to_date):
	"""
	Phân tích Sales Invoice theo từng dòng Item, gom lại theo invoice + VAT rate.
	Dùng 2-Layer Fallback Strategy để xác định thuế suất cho mỗi dòng Item.

	Cho Phụ lục PL 01-1/GTGT (bảng kê bán ra).

	Một hóa đơn có nhiều mức thuế → xuất thành nhiều dòng trong kết quả,
	mỗi dòng ứng với 1 mức thuế suất (giá trị chưa thuế & tiền thuế riêng).

	Returns:
		list[dict]: mỗi dict = 1 dòng bảng kê, gồm:
			- invoice: tên SI
			- posting_date, customer, customer_name, customer_tax_id
			- einvoice_number, einvoice_issued
			- vat_rate: float hoặc "KCT"
			- base_net_amount: giá trị chưa thuế (theo rate này)
			- vat_amount: tiền thuế (theo rate này)
	"""
	# 1. Query invoice headers
	invoices = frappe.db.sql("""
		SELECT
			si.name,
			si.posting_date,
			si.customer,
			si.customer_name,
			si.einvoice_number,
			si.einvoice_issued,
			cust.tax_id AS customer_tax_id
		FROM `tabSales Invoice` si
		LEFT JOIN `tabCustomer` cust ON cust.name = si.customer
		WHERE si.company = %(company)s
			AND si.posting_date >= %(from_date)s
			AND si.posting_date <= %(to_date)s
			AND si.docstatus = 1
		ORDER BY si.posting_date, si.name
	""", {"company": company, "from_date": from_date, "to_date": to_date}, as_dict=True)

	if not invoices:
		return []

	vat_accounts = _get_vat_accounts_set(company, "output")

	# 2. Query all items + taxes in bulk for performance
	invoice_names = [inv.name for inv in invoices]
	inv_map = {inv.name: inv for inv in invoices}

	all_items = _bulk_get_invoice_items("Sales Invoice Item", invoice_names)
	all_taxes = _bulk_get_invoice_taxes("Sales Taxes and Charges", invoice_names)

	# 3. Per-invoice analysis
	result = []
	for inv in invoices:
		items = all_items.get(inv.name, [])
		taxes = all_taxes.get(inv.name, [])

		# Bước 1: Group items by resolved VAT rate, chỉ tích lũy net
		rate_groups = {}  # {rate: {"net": 0, "vat": 0}}

		for item in items:
			rate = _resolve_item_vat_rate(item, taxes, vat_accounts)
			if rate not in rate_groups:
				rate_groups[rate] = {"net": 0, "vat": 0}
			rate_groups[rate]["net"] += flt(item.get("base_net_amount", 0))

		# Bước 2: Điền VAT — ưu tiên base_tax_amount thực tế từ bảng thuế
		_fill_vat_amounts(rate_groups, taxes, vat_accounts)

		# Emit 1 dòng per rate (hoặc 1 dòng duy nhất nếu HĐ thuần)
		if not rate_groups:
			# HĐ không có item nào (edge case)
			rate_groups[VAT_EXEMPT] = {"net": 0, "vat": 0}

		for rate, amounts in sorted(rate_groups.items(), key=_rate_sort_key):
			result.append({
				"invoice": inv.name,
				"posting_date": inv.posting_date,
				"customer": inv.customer,
				"customer_name": inv.customer_name,
				"customer_tax_id": inv.customer_tax_id,
				"einvoice_number": inv.get("einvoice_number"),
				"einvoice_issued": inv.get("einvoice_issued"),
				"vat_rate": rate,
				"base_net_amount": amounts["net"],
				"vat_amount": amounts["vat"],
			})

	return result


def get_purchase_invoices(company, from_date, to_date):
	"""
	Phân tích Purchase Invoice theo từng dòng Item, gom lại theo invoice + VAT rate.
	Dùng 2-Layer Fallback Strategy tương tự Sales Invoice.

	Cho Phụ lục PL 01-2/GTGT (bảng kê mua vào).

	Returns:
		list[dict]: mỗi dict = 1 dòng bảng kê, gồm:
			- invoice: tên PI
			- posting_date, supplier, supplier_name, supplier_tax_id
			- bill_no, bill_date
			- inward_*: thông tin từ Inward Invoice (nếu có)
			- vat_rate: float hoặc "KCT"
			- base_net_amount: giá trị chưa thuế (theo rate này)
			- vat_amount: tiền thuế (theo rate này)
	"""
	invoices = frappe.db.sql("""
		SELECT
			pi.name,
			pi.posting_date,
			pi.supplier,
			pi.supplier_name,
			pi.bill_no,
			pi.bill_date,
			pi.einvoice_inward,
			pi.einvoice_lookup_code,
			sup.tax_id AS supplier_tax_id
		FROM `tabPurchase Invoice` pi
		LEFT JOIN `tabSupplier` sup ON sup.name = pi.supplier
		WHERE pi.company = %(company)s
			AND pi.posting_date >= %(from_date)s
			AND pi.posting_date <= %(to_date)s
			AND pi.docstatus = 1
		ORDER BY pi.posting_date, pi.name
	""", {"company": company, "from_date": from_date, "to_date": to_date}, as_dict=True)

	if not invoices:
		return []

	vat_accounts = _get_vat_accounts_set(company, "input")

	invoice_names = [inv.name for inv in invoices]
	all_items = _bulk_get_invoice_items("Purchase Invoice Item", invoice_names)
	all_taxes = _bulk_get_invoice_taxes("Purchase Taxes and Charges", invoice_names)

	# Bulk fetch Inward Invoice data
	iw_links = {inv.name: inv.einvoice_inward for inv in invoices if inv.get("einvoice_inward")}
	iw_data = _bulk_get_inward_invoices(list(set(iw_links.values()))) if iw_links else {}

	result = []
	for inv in invoices:
		items = all_items.get(inv.name, [])
		taxes = all_taxes.get(inv.name, [])

		# Resolve Inward Invoice info
		iw_info = {}
		if inv.get("einvoice_inward"):
			iw_info = iw_data.get(inv.einvoice_inward, {})

		# Bước 1: Group items by resolved VAT rate, tích lũy net và fa_net riêng
		rate_groups = {}

		for item in items:
			rate = _resolve_item_vat_rate(item, taxes, vat_accounts)
			if rate not in rate_groups:
				rate_groups[rate] = {"net": 0, "vat": 0, "fa_net": 0}
			net = flt(item.get("base_net_amount", 0))
			rate_groups[rate]["net"] += net
			if item.get("is_fixed_asset"):
				rate_groups[rate]["fa_net"] += net

		# Bước 2: Điền VAT — ưu tiên base_tax_amount thực tế từ bảng thuế
		_fill_vat_amounts(rate_groups, taxes, vat_accounts)

		# Bước 3: Tính fa_vat proportionally từ tỉ lệ fa_net/net
		for amounts in rate_groups.values():
			total = amounts["net"]
			fa_ratio = amounts["fa_net"] / total if total else 0
			amounts["fa_vat"] = amounts["vat"] * fa_ratio
			amounts["goods_vat"] = amounts["vat"] - amounts["fa_vat"]

		if not rate_groups:
			rate_groups[VAT_EXEMPT] = {"net": 0, "vat": 0, "fa_net": 0, "fa_vat": 0, "goods_vat": 0}

		for rate, amounts in sorted(rate_groups.items(), key=_rate_sort_key):
			row = {
				"invoice": inv.name,
				"posting_date": inv.posting_date,
				"supplier": inv.supplier,
				"supplier_name": inv.supplier_name,
				"supplier_tax_id": inv.supplier_tax_id,
				"bill_no": inv.bill_no,
				"bill_date": inv.bill_date,
				"einvoice_inward": inv.get("einvoice_inward"),
				"einvoice_lookup_code": inv.get("einvoice_lookup_code"),
				"vat_rate": rate,
				"base_net_amount": amounts["net"],
				"vat_amount": amounts["vat"],
				"goods_vat": amounts["goods_vat"],
				"fa_vat": amounts["fa_vat"],
			}

			# Merge Inward Invoice fields
			if iw_info:
				row["inward_invoice_number"] = iw_info.get("invoice_number")
				row["inward_invoice_date"] = iw_info.get("invoice_date")
				row["inward_supplier_tax_code"] = iw_info.get("supplier_tax_code")
				row["inward_invoice_pattern"] = iw_info.get("invoice_pattern", "")
				row["inward_invoice_serial"] = iw_info.get("invoice_serial", "")

			result.append(row)

	return result


# ---------------------------------------------------------------------------
# Bulk query helpers (avoid N+1 queries)
# ---------------------------------------------------------------------------

def _bulk_get_invoice_items(doctype, invoice_names):
	"""
	Bulk fetch invoice items cho danh sách invoices.

	Returns:
		dict: {parent_name: [item_rows]}
	"""
	if not invoice_names:
		return {}

	params = {}
	for i, name in enumerate(invoice_names):
		params[f"inv_{i}"] = name
	placeholders = ", ".join(["%(inv_{i})s".format(i=i) for i in range(len(invoice_names))])

	items = frappe.db.sql("""
		SELECT
			parent,
			item_code,
			item_name,
			qty,
			base_net_amount,
			item_tax_template,
			item_tax_rate,
			IFNULL(is_fixed_asset, 0) AS is_fixed_asset
		FROM `tab{doctype}`
		WHERE parent IN ({placeholders})
		ORDER BY parent, idx
	""".format(doctype=doctype, placeholders=placeholders), params, as_dict=True)

	result = {}
	for item in items:
		result.setdefault(item.parent, []).append(item)

	return result


def _bulk_get_invoice_taxes(doctype, invoice_names):
	"""
	Bulk fetch taxes and charges cho danh sách invoices.

	Returns:
		dict: {parent_name: [tax_rows]}
	"""
	if not invoice_names:
		return {}

	params = {}
	for i, name in enumerate(invoice_names):
		params[f"inv_{i}"] = name
	placeholders = ", ".join(["%(inv_{i})s".format(i=i) for i in range(len(invoice_names))])

	taxes = frappe.db.sql("""
		SELECT
			parent,
			charge_type,
			account_head,
			rate,
			base_tax_amount
		FROM `tab{doctype}`
		WHERE parent IN ({placeholders})
		ORDER BY parent, idx
	""".format(doctype=doctype, placeholders=placeholders), params, as_dict=True)

	result = {}
	for tax in taxes:
		result.setdefault(tax.parent, []).append(tax)

	return result


def _bulk_get_inward_invoices(iw_names):
	"""
	Bulk fetch Inward Invoice data.

	Returns:
		dict: {iw_name: {invoice_number, invoice_date, ...}}
	"""
	if not iw_names:
		return {}

	params = {}
	for i, name in enumerate(iw_names):
		params[f"iw_{i}"] = name
	placeholders = ", ".join(["%(iw_{i})s".format(i=i) for i in range(len(iw_names))])

	data = frappe.db.sql("""
		SELECT
			name,
			invoice_number,
			invoice_date,
			supplier_tax_code,
			invoice_pattern,
			invoice_serial
		FROM `tabEInvoice Inward`
		WHERE name IN ({placeholders})
	""".format(placeholders=placeholders), params, as_dict=True)

	return {row.name: row for row in data}


def _rate_sort_key(item):
	"""Sort key cho rate_groups.items(): KCT đầu, rồi 0, 5, 8, 10."""
	rate = item[0]
	if rate == VAT_EXEMPT:
		return (-1, 0)
	return (0, flt(rate))


def get_import_vat_from_account(company, from_date, to_date, account, finance_book=None):
	"""
	Đọc số dư Nợ phát sinh trong kỳ của TK chỉ định từ Journal Entry.

	Thuế GTGT hàng nhập khẩu thường được hạch toán qua JE từ tờ khai hải quan,
	không qua Purchase Invoice. Chỉ đọc JE để tránh trùng với PI đã tính vào ct23.

	Args:
		account: tên TK đầy đủ (VD: "1331 - Thuế GTGT được khấu trừ - MST")

	Returns:
		float: tổng Nợ phát sinh từ JE
	"""
	fb_condition = _finance_book_condition(finance_book)
	rows = frappe.db.sql("""
		SELECT COALESCE(SUM(gl.debit), 0) AS total_debit
		FROM `tabGL Entry` gl
		WHERE gl.company = %(company)s
			AND gl.posting_date >= %(from_date)s
			AND gl.posting_date <= %(to_date)s
			AND gl.is_cancelled = 0
			AND gl.account = %(account)s
			AND gl.voucher_type = 'Journal Entry'
			{fb_condition}
	""".format(fb_condition=fb_condition), {
		"company": company,
		"from_date": from_date,
		"to_date": to_date,
		"account": account,
		"finance_book": finance_book,
	}, as_dict=True)
	return flt(rows[0].total_debit) if rows else 0


def _fill_vat_amounts(rate_groups, taxes, vat_accounts):
	"""
	Điền vat_amount cho mỗi rate_group từ base_tax_amount thực tế.

	Ưu tiên đọc từ bảng Taxes and Charges (base_tax_amount đã tính bởi ERPNext).
	Fallback về net * rate / 100 nếu không tìm thấy tax row khớp.

	Với hóa đơn hoàn trả (is_return=1), base_tax_amount sẽ âm — để nguyên.
	"""
	for rate, amounts in rate_groups.items():
		if rate == VAT_EXEMPT or flt(rate) == 0:
			amounts["vat"] = 0
			continue

		# Tìm tax row khớp account + rate
		actual_vat = None
		for tax in taxes:
			if tax.get("account_head") in vat_accounts:
				tax_rate = flt(tax.get("rate", 0))
				if abs(tax_rate - flt(rate)) < 0.01:
					actual_vat = flt(tax.get("base_tax_amount", 0))
					break

		if actual_vat is not None:
			amounts["vat"] = actual_vat
		else:
			# Fallback: tính từ net amount
			amounts["vat"] = amounts["net"] * flt(rate) / 100


# ---------------------------------------------------------------------------
# Income / Expense queries (Tờ khai 03/TNDN)
# ---------------------------------------------------------------------------

def get_income_expense_by_account(company, from_date, to_date, finance_book=None):
	"""
	Phát sinh theo mã TK cho B02-DN / 03-TNDN.

	Revenue (5xx, 7xx): credit - debit (dương = doanh thu).
	Expense (6xx, 8xx): debit - credit (dương = chi phí).
	Group by account_number.

	Returns:
		dict: {account_number: amount}
	"""
	fb_condition = _finance_book_condition(finance_book)

	data = frappe.db.sql("""
		SELECT
			acc.account_number,
			acc.root_type,
			SUM(gl.debit) AS total_debit,
			SUM(gl.credit) AS total_credit
		FROM `tabGL Entry` gl
		JOIN `tabAccount` acc ON acc.name = gl.account
		WHERE gl.company = %(company)s
			AND gl.posting_date >= %(from_date)s
			AND gl.posting_date <= %(to_date)s
			AND gl.is_cancelled = 0
			AND acc.root_type IN ('Income', 'Expense')
			{fb_condition}
		GROUP BY acc.account_number, acc.root_type
	""".format(fb_condition=fb_condition), {
		"company": company,
		"from_date": from_date,
		"to_date": to_date,
		"finance_book": finance_book,
	}, as_dict=True)

	result = {}
	for row in data:
		if not row.account_number:
			continue
		if row.root_type == "Income":
			# Revenue: credit - debit
			result[row.account_number] = flt(row.total_credit) - flt(row.total_debit)
		else:
			# Expense: debit - credit
			result[row.account_number] = flt(row.total_debit) - flt(row.total_credit)

	return result


# ---------------------------------------------------------------------------
# Financial Statements queries (BCTC)
# ---------------------------------------------------------------------------

def get_cash_flows(company, from_date, to_date, finance_book=None):
	"""
	Phân tích dòng tiền cho B03-DN (phương pháp trực tiếp).

	Query GL Entry có TK tiền (CASH, BANK, CASH_IN_TRANSIT) matched
	với TK đối ứng. Phân loại theo hoạt động.

	Returns:
		dict: {
			"operating": {"receipts": amount, "payments": amount, "net": amount},
			"investing": {"receipts": amount, "payments": amount, "net": amount},
			"financing": {"receipts": amount, "payments": amount, "net": amount},
		}
	"""
	fb_condition = _finance_book_condition(finance_book)

	# Get cash/bank accounts
	cash_accounts = (
		get_accounts_for_role(company, "CASH")
		+ get_accounts_for_role(company, "BANK")
		+ get_accounts_for_role(company, "CASH_IN_TRANSIT")
	)

	if not cash_accounts:
		# Fallback: get all accounts starting with 111, 112, 113
		cash_accounts = (
			get_accounts_by_prefix(company, "111")
			+ get_accounts_by_prefix(company, "112")
			+ get_accounts_by_prefix(company, "113")
		)

	if not cash_accounts:
		return {
			"operating": {"receipts": 0, "payments": 0, "net": 0},
			"investing": {"receipts": 0, "payments": 0, "net": 0},
			"financing": {"receipts": 0, "payments": 0, "net": 0},
		}

	params = {
		"company": company,
		"from_date": from_date,
		"to_date": to_date,
		"finance_book": finance_book,
	}
	for i, acc in enumerate(cash_accounts):
		params[f"ca_{i}"] = acc

	cash_placeholders = ", ".join(["%(ca_{i})s".format(i=i) for i in range(len(cash_accounts))])

	# Get GL entries for cash accounts with their counter-party accounts
	data = frappe.db.sql("""
		SELECT
			gl.account,
			gl.against,
			gl.debit,
			gl.credit,
			against_acc.account_number AS against_account_number,
			against_acc.root_type AS against_root_type
		FROM `tabGL Entry` gl
		LEFT JOIN `tabAccount` against_acc ON against_acc.name = gl.against
		WHERE gl.company = %(company)s
			AND gl.posting_date >= %(from_date)s
			AND gl.posting_date <= %(to_date)s
			AND gl.is_cancelled = 0
			AND gl.account IN ({cash_placeholders})
			{fb_condition}
	""".format(cash_placeholders=cash_placeholders, fb_condition=fb_condition),
		params, as_dict=True)

	result = {
		"operating": {"receipts": 0, "payments": 0, "net": 0},
		"investing": {"receipts": 0, "payments": 0, "net": 0},
		"financing": {"receipts": 0, "payments": 0, "net": 0},
	}

	for row in data:
		category = _classify_cash_flow(row.against_account_number, row.against_root_type)
		debit = flt(row.debit)
		credit = flt(row.credit)

		if debit > 0:
			result[category]["receipts"] += debit
		if credit > 0:
			result[category]["payments"] += credit

	# Calculate net for each category
	for cat in result:
		result[cat]["net"] = result[cat]["receipts"] - result[cat]["payments"]

	return result


def _classify_cash_flow(against_account_number, against_root_type):
	"""
	Phân loại dòng tiền dựa trên TK đối ứng.

	- Đầu tư: TK TSCĐ (2xx), đầu tư (12x, 228)
	- Tài chính: TK vay (34x), vốn CSH (41x), cổ tức
	- Kinh doanh: còn lại
	"""
	if not against_account_number:
		return "operating"

	prefix = against_account_number[:2] if len(against_account_number) >= 2 else against_account_number

	# Investing: fixed assets (21x), construction in progress (24x),
	# long-term investments (22x), short-term investments (12x)
	if prefix in ("21", "22", "24", "12"):
		return "investing"

	# Financing: borrowings (34x), equity (41x), reserves (41x)
	if prefix in ("34", "41", "42"):
		return "financing"

	return "operating"


def get_trial_balance(company, from_date, to_date, finance_book=None):
	"""
	Bảng cân đối phát sinh tài khoản.

	Mỗi TK: số dư đầu kỳ, phát sinh nợ, phát sinh có, số dư cuối kỳ.

	Returns:
		list[dict]: sorted by account_number, each dict has:
			account_number, account_name, opening_debit, opening_credit,
			debit, credit, closing_debit, closing_credit
	"""
	fb_condition = _finance_book_condition(finance_book)

	# Opening balances (before from_date)
	opening_data = frappe.db.sql("""
		SELECT
			acc.account_number,
			acc.account_name,
			SUM(gl.debit) AS debit,
			SUM(gl.credit) AS credit
		FROM `tabGL Entry` gl
		JOIN `tabAccount` acc ON acc.name = gl.account
		WHERE gl.company = %(company)s
			AND gl.posting_date < %(from_date)s
			AND gl.is_cancelled = 0
			{fb_condition}
		GROUP BY acc.account_number, acc.account_name
	""".format(fb_condition=fb_condition), {
		"company": company,
		"from_date": from_date,
		"finance_book": finance_book,
	}, as_dict=True)

	# Period transactions
	period_data = frappe.db.sql("""
		SELECT
			acc.account_number,
			acc.account_name,
			SUM(gl.debit) AS debit,
			SUM(gl.credit) AS credit
		FROM `tabGL Entry` gl
		JOIN `tabAccount` acc ON acc.name = gl.account
		WHERE gl.company = %(company)s
			AND gl.posting_date >= %(from_date)s
			AND gl.posting_date <= %(to_date)s
			AND gl.is_cancelled = 0
			{fb_condition}
		GROUP BY acc.account_number, acc.account_name
	""".format(fb_condition=fb_condition), {
		"company": company,
		"from_date": from_date,
		"to_date": to_date,
		"finance_book": finance_book,
	}, as_dict=True)

	# Merge
	accounts = {}

	for row in opening_data:
		if not row.account_number:
			continue
		opening_balance = flt(row.debit) - flt(row.credit)
		accounts[row.account_number] = {
			"account_number": row.account_number,
			"account_name": row.account_name,
			"opening_debit": flt(row.debit) if opening_balance >= 0 else 0,
			"opening_credit": flt(row.credit) if opening_balance < 0 else 0,
			"debit": 0,
			"credit": 0,
			"closing_debit": 0,
			"closing_credit": 0,
		}

	for row in period_data:
		if not row.account_number:
			continue
		if row.account_number not in accounts:
			accounts[row.account_number] = {
				"account_number": row.account_number,
				"account_name": row.account_name,
				"opening_debit": 0,
				"opening_credit": 0,
				"debit": 0,
				"credit": 0,
				"closing_debit": 0,
				"closing_credit": 0,
			}
		accounts[row.account_number]["debit"] = flt(row.debit)
		accounts[row.account_number]["credit"] = flt(row.credit)

	# Calculate closing balances
	for acc_num, acc in accounts.items():
		opening_net = acc["opening_debit"] - acc["opening_credit"]
		closing_net = opening_net + acc["debit"] - acc["credit"]
		acc["closing_debit"] = closing_net if closing_net >= 0 else 0
		acc["closing_credit"] = abs(closing_net) if closing_net < 0 else 0

	# Sort by account_number
	return sorted(accounts.values(), key=lambda x: x["account_number"])


# ---------------------------------------------------------------------------
# Mapping Wrapper Functions for HTKK Engine
# ---------------------------------------------------------------------------

def get_purchase_net_total(company, from_date, to_date):
    """Tổng giá trị hàng mua vào (chưa thuế)."""
    lines = get_purchase_invoices(company, from_date, to_date)
    return sum(flt(l["base_net_amount"]) for l in lines)

def get_purchase_vat_total(company, from_date, to_date):
    """Tổng thuế GTGT hàng mua vào."""
    lines = get_purchase_invoices(company, from_date, to_date)
    return sum(flt(l["vat_amount"]) for l in lines)

def get_sales_exempt_net(company, from_date, to_date):
    """Doanh thu không chịu thuế (KCT)."""
    lines = get_sales_invoices(company, from_date, to_date)
    return sum(flt(l["base_net_amount"]) for l in lines if l["vat_rate"] == VAT_EXEMPT)

def get_sales_0_net(company, from_date, to_date):
    """Doanh thu thuế suất 0%."""
    lines = get_sales_invoices(company, from_date, to_date)
    return sum(flt(l["base_net_amount"]) for l in lines if flt(l["vat_rate"]) == 0)

def get_sales_5_net(company, from_date, to_date):
    """Doanh thu thuế suất 5%."""
    lines = get_sales_invoices(company, from_date, to_date)
    return sum(flt(l["base_net_amount"]) for l in lines if flt(l["vat_rate"]) == 5)

def get_sales_5_vat(company, from_date, to_date):
    """Thuế GTGT 5%."""
    lines = get_sales_invoices(company, from_date, to_date)
    return sum(flt(l["vat_amount"]) for l in lines if flt(l["vat_rate"]) == 5)

def get_sales_10_net(company, from_date, to_date):
    """Doanh thu thuế suất 10%."""
    lines = get_sales_invoices(company, from_date, to_date)
    return sum(flt(l["base_net_amount"]) for l in lines if flt(l["vat_rate"]) == 10)

def get_sales_10_vat(company, from_date, to_date):
    """Thuế GTGT 10%."""
    lines = get_sales_invoices(company, from_date, to_date)
    return sum(flt(l["vat_amount"]) for l in lines if flt(l["vat_rate"]) == 10)

def get_sales_8_net(company, from_date, to_date):
    """Doanh thu thuế suất 8% (NĐ44)."""
    lines = get_sales_invoices(company, from_date, to_date)
    return sum(flt(l["base_net_amount"]) for l in lines if flt(l["vat_rate"]) == 8)
