# Copyright (c) 2026 DCNET
# Tờ khai thuế GTGT — Mẫu 01/GTGT (TT80/2021)
from __future__ import annotations

import frappe
from frappe import _
from frappe.utils import flt, getdate


def execute(filters=None):
	"""Script Report entry point. Returns (columns, data)."""
	filters = frappe._dict(filters or {})
	_validate_filters(filters)

	columns = get_columns()
	data = _build_vat_return(filters)

	return columns, data


def get_columns():
	return [
		{"fieldname": "stt", "label": _("STT"), "fieldtype": "Int", "width": 50},
		{"fieldname": "chi_tieu", "label": _("Chỉ tiêu"), "fieldtype": "Data", "width": 340},
		{"fieldname": "ma_so", "label": _("Mã số"), "fieldtype": "Data", "width": 70},
		{"fieldname": "doanh_thu", "label": _("Giá trị HHDV (chưa thuế)"), "fieldtype": "Currency", "options": "currency", "width": 170},
		{"fieldname": "thue_gtgt", "label": _("Thuế GTGT"), "fieldtype": "Currency", "options": "currency", "width": 150},
	]


def _validate_filters(filters):
	if not filters.company:
		filters.company = frappe.defaults.get_user_default("Company")
	if not filters.company:
		filters.company = frappe.db.get_single_value("Global Defaults", "default_company") or ""
	if not filters.company:
		companies = frappe.get_all("Company", limit=1, pluck="name")
		filters.company = companies[0] if companies else ""
	if not filters.from_date:
		filters.from_date = frappe.utils.get_first_day(frappe.utils.today()).strftime("%Y-%m-%d")
	if not filters.to_date:
		filters.to_date = frappe.utils.get_last_day(frappe.utils.today()).strftime("%Y-%m-%d")
	if getdate(filters.from_date) > getdate(filters.to_date):
		frappe.throw(_("Từ ngày phải trước Đến ngày"))


def _build_vat_return(filters):
	company = filters.company
	from_date = filters.from_date
	to_date = filters.to_date

	si = _get_sales_invoice_vat(company, from_date, to_date)
	adj = _get_vat_adjustments(company, from_date, to_date)
	pi = _get_purchase_invoice_vat(company, from_date, to_date)
	paid = _get_vat_paid(company, from_date, to_date)

	# --- User input ---
	thue_ky_truoc_cs = flt(filters.get("thue_ky_truoc_chuyen_sang", 0))

	# --- Computed values ---
	# B. VAT Output
	revenue_0pct_not_declare = flt(si["revenue_not_declare"])    # [22]
	revenue_0pct = flt(si["revenue_0pct"])                       # [23]
	revenue_5pct = flt(si["revenue_5pct"]);   vat_5pct = flt(si["vat_5pct"])     # [24]
	revenue_10pct = flt(si["revenue_10pct"]); vat_10pct = flt(si["vat_10pct"])   # [25]

	adj_increase = flt(adj["increase"])   # [26a]
	adj_decrease = flt(adj["decrease"])   # [26b]

	total_taxable_revenue = revenue_5pct + revenue_10pct                          # [27]
	total_output_vat_goods = vat_5pct + vat_10pct                                 # [28]
	total_output_vat = total_output_vat_goods + adj_increase - adj_decrease       # [29]

	# C. VAT Input
	vat_input_domestic = flt(pi["vat_domestic"])   # [31]
	vat_input_import = flt(pi["vat_import"])        # [32]
	total_input_vat = thue_ky_truoc_cs + vat_input_domestic + vat_input_import    # [33]

	# D. VAT Payable
	vat_payable = total_output_vat - total_input_vat                               # [34]
	vat_paid_in_period = flt(paid)                                                 # [35]
	vat_remaining = vat_payable - vat_paid_in_period                                # [36]
	vat_carry_forward = max(0, -vat_payable)                                        # [37]

	def R(chi_tieu, ma_so, doanh_thu=0, thue_gtgt=0, bold=False, indent=0):
		prefix = "  " * indent
		return {
			"chi_tieu": prefix + chi_tieu,
			"ma_so": ma_so,
			"doanh_thu": doanh_thu,
			"thue_gtgt": thue_gtgt,
			"indent": indent,
			"bold": bold,
		}

	data = []

	# ── A ──
	data.append(R(_("A. KHÔNG PHÁT SINH HOẠT ĐỘNG MUA BÁN TRONG KỲ"), "", bold=True))
	data.append(R(_("Đánh dấu nếu kỳ này không có hóa đơn đầu vào/ra"), "[21]", indent=1))

	# ── B: Thuế GTGT đầu ra ──
	data.append(R("", ""))
	data.append(R(_("B. THUẾ GTGT ĐẦU RA"), "", bold=True))
	data.append(R(_("HHDV bán ra không phải kê khai, tính nộp thuế"), "[22]", doanh_thu=revenue_0pct_not_declare, indent=1))
	data.append(R(_("HHDV bán ra chịu thuế suất 0%"), "[23]", doanh_thu=revenue_0pct, indent=1))
	data.append(R(_("HHDV bán ra chịu thuế suất 5%"), "[24]", doanh_thu=revenue_5pct, thue_gtgt=vat_5pct, indent=1))
	data.append(R(_("HHDV bán ra chịu thuế suất 10%"), "[25]", doanh_thu=revenue_10pct, thue_gtgt=vat_10pct, indent=1))
	data.append(R(_("Điều chỉnh thuế GTGT của HHDV bán ra các kỳ trước"), "[26]", indent=1))
	data.append(R(_("  Điều chỉnh tăng"), "[26a]", thue_gtgt=adj_increase, indent=2))
	data.append(R(_("  Điều chỉnh giảm"), "[26b]", thue_gtgt=adj_decrease, indent=2))
	data.append(R(_("Tổng doanh thu HHDV bán ra chịu thuế GTGT ([24]+[25])"), "[27]", doanh_thu=total_taxable_revenue, indent=1))
	data.append(R(_("Thuế GTGT của HHDV bán ra ([24]+[25])"), "[28]", thue_gtgt=total_output_vat_goods, indent=1))
	data.append(R(_("Tổng thuế GTGT đầu ra ([28]+[26a]-[26b])"), "[29]", thue_gtgt=total_output_vat, indent=1))

	# ── C: Thuế GTGT đầu vào ──
	data.append(R("", ""))
	data.append(R(_("C. THUẾ GTGT ĐẦU VÀO ĐƯỢC KHẤU TRỪ"), "", bold=True))
	data.append(R(_("Thuế GTGT đầu vào được KT kỳ trước chuyển sang"), "[30]", thue_gtgt=thue_ky_truoc_cs, indent=1))
	data.append(R(_("Thuế GTGT mua vào trong nước"), "[31]", thue_gtgt=vat_input_domestic, indent=1))
	data.append(R(_("Thuế GTGT nhập khẩu"), "[32]", thue_gtgt=vat_input_import, indent=1))
	data.append(R(_("Tổng thuế GTGT đầu vào được khấu trừ ([30]+[31]+[32])"), "[33]", thue_gtgt=total_input_vat, indent=1))

	# ── D: Thuế GTGT phải nộp ──
	data.append(R("", ""))
	data.append(R(_("D. THUẾ GTGT PHẢI NỘP"), "", bold=True))
	data.append(R(_("Thuế GTGT phải nộp ([29]-[33])"), "[34]", thue_gtgt=vat_payable, indent=1))
	data.append(R(_("Thuế GTGT đã nộp trong kỳ"), "[35]", thue_gtgt=vat_paid_in_period, indent=1))
	data.append(R(_("Thuế GTGT còn phải nộp ([34]-[35])"), "[36]", thue_gtgt=vat_remaining, indent=1))
	data.append(R(_("Thuế GTGT đầu vào được KT chuyển kỳ sau"), "[37]", thue_gtgt=vat_carry_forward, indent=1))

	# Add STT numbering
	for i, row in enumerate(data, 1):
		row["stt"] = i if row["chi_tieu"].strip() else 0

	return data


# ═══════════════════════════════════════════════════════════════════════════════
# Data query helpers
# ═══════════════════════════════════════════════════════════════════════════════

def _get_sales_invoice_vat(company, from_date, to_date):
	"""Sales Invoices grouped by tax rate for VAT output [22]-[25]."""
	result = frappe.db.sql("""
		SELECT
			stc.rate AS tax_rate,
			SUM(stc.tax_amount) AS vat_amount,
			SUM(si.net_total) AS net_revenue
		FROM `tabSales Invoice` si
		INNER JOIN `tabSales Taxes and Charges` stc ON stc.parent = si.name
		WHERE si.docstatus = 1
			AND si.company = %(company)s
			AND si.posting_date BETWEEN %(from_date)s AND %(to_date)s
			AND si.is_return = 0
			AND stc.account_head LIKE %(vat_out)s
		GROUP BY stc.rate
	""", {
		"company": company, "from_date": from_date, "to_date": to_date,
		"vat_out": "%33311%",
	}, as_dict=True)

	data = {
		"revenue_not_declare": 0,
		"revenue_0pct": 0,
		"revenue_5pct": 0, "vat_5pct": 0,
		"revenue_10pct": 0, "vat_10pct": 0,
	}

	for row in result:
		rate = flt(row.tax_rate)
		net = flt(row.net_revenue)
		vat = flt(row.vat_amount)
		if rate == 0:
			data["revenue_0pct"] += net
		elif rate == 5:
			data["revenue_5pct"] += net; data["vat_5pct"] += vat
		elif rate == 10:
			data["revenue_10pct"] += net; data["vat_10pct"] += vat

	return data


def _get_vat_adjustments(company, from_date, to_date):
	"""VAT adjustments from Sales Return (Credit Notes) and Debit Notes [26]."""
	result = frappe.db.sql("""
		SELECT
			si.is_return,
			SUM(stc.tax_amount) AS vat_amount
		FROM `tabSales Invoice` si
		INNER JOIN `tabSales Taxes and Charges` stc ON stc.parent = si.name
		WHERE si.docstatus = 1
			AND si.company = %(company)s
			AND si.posting_date BETWEEN %(from_date)s AND %(to_date)s
			AND (si.is_return = 1 OR si.is_debit_note = 1)
			AND stc.account_head LIKE %(vat_out)s
		GROUP BY si.is_return
	""", {
		"company": company, "from_date": from_date, "to_date": to_date,
		"vat_out": "%33311%",
	}, as_dict=True)

	increase = 0.0
	decrease = 0.0
	for row in result:
		vat = flt(row.vat_amount)
		if row.is_return == 1:
			decrease += abs(vat)
		else:
			increase += vat

	return {"increase": increase, "decrease": decrease}


def _get_purchase_invoice_vat(company, from_date, to_date):
	"""Purchase Invoices for deductible VAT input [31]-[32]."""
	result = frappe.db.sql("""
		SELECT
			ptc.rate AS tax_rate,
			SUM(ptc.tax_amount) AS vat_amount
		FROM `tabPurchase Invoice` pi
		INNER JOIN `tabPurchase Taxes and Charges` ptc ON ptc.parent = pi.name
		WHERE pi.docstatus = 1
			AND pi.company = %(company)s
			AND pi.posting_date BETWEEN %(from_date)s AND %(to_date)s
			AND pi.is_return = 0
			AND ptc.account_head LIKE %(vat_in)s
		GROUP BY ptc.rate
	""", {
		"company": company, "from_date": from_date, "to_date": to_date,
		"vat_in": "%133%",
	}, as_dict=True)

	data = {"vat_domestic": 0.0, "vat_import": 0.0}

	for row in result:
		vat = flt(row.vat_amount)
		rate = flt(row.tax_rate)
		if rate in (5, 10):
			data["vat_domestic"] += vat
		else:
			data["vat_import"] += vat

	# Import VAT via Journal Entry (Nợ 133 / Có 33312)
	je_vat = frappe.db.sql("""
		SELECT SUM(jea.debit) AS vat_amount
		FROM `tabJournal Entry Account` jea
		INNER JOIN `tabJournal Entry` je ON je.name = jea.parent
		WHERE je.docstatus = 1
			AND je.company = %(company)s
			AND je.posting_date BETWEEN %(from_date)s AND %(to_date)s
			AND jea.account LIKE %(vat_133)s
			AND EXISTS (
				SELECT 1 FROM `tabJournal Entry Account` jea2
				WHERE jea2.parent = je.name AND jea2.account LIKE %(tk_33312)s
			)
	""", {
		"company": company, "from_date": from_date, "to_date": to_date,
		"vat_133": "%133%", "tk_33312": "%33312%",
	})[0][0] or 0

	data["vat_import"] += flt(je_vat)
	return data


def _get_vat_paid(company, from_date, to_date):
	"""VAT already paid — credit side of TK 33311 in Journal Entries [35]."""
	result = frappe.db.sql("""
		SELECT SUM(jea.credit) AS paid
		FROM `tabJournal Entry Account` jea
		INNER JOIN `tabJournal Entry` je ON je.name = jea.parent
		WHERE je.docstatus = 1
			AND je.company = %(company)s
			AND je.posting_date BETWEEN %(from_date)s AND %(to_date)s
			AND jea.account LIKE %(tk_33311)s
			AND jea.credit > 0
	""", {
		"company": company, "from_date": from_date, "to_date": to_date,
		"tk_33311": "%33311%",
	})[0][0] or 0

	return flt(result)
