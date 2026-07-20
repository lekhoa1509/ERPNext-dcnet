"""Xuất mẫu 05/QTT-TNCN (quyết toán thuế TNCN năm) từ PIT Annual Settlement.

⚠️ Cùng tình trạng với `dcnet_hrm/export/d02lt.py`: CHƯA có file mẫu chính
thức (định dạng HTKK) để đối chiếu toạ độ cell — hàm chỉ chuẩn bị dữ liệu,
KHÔNG tự đoán layout. Xem hướng dẫn đầy đủ trong d02lt.py.
"""

import os

import frappe
from frappe import _

TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "templates", "05-QTT-TNCN.xlsx")


def get_export_rows(pit_annual_settlement):
	doc = frappe.get_doc("PIT Annual Settlement", pit_annual_settlement)
	rows = [
		{
			"employee": row.employee,
			"employee_name": row.employee_name,
			"total_taxable_income": row.total_taxable_income,
			"total_deductions": row.total_deductions,
			"tax_withheld": row.tax_withheld,
			"tax_payable_annual": row.tax_payable_annual,
			"difference": row.difference,
		}
		for row in doc.employees
	]
	return doc, rows


@frappe.whitelist()
def export_qtt_tncn(pit_annual_settlement):
	doc, _rows = get_export_rows(pit_annual_settlement)
	frappe.has_permission("PIT Annual Settlement", doc=doc, throw=True)

	if not os.path.exists(TEMPLATE_PATH):
		frappe.throw(
			_(
				"Missing the official 05/QTT-TNCN Excel template (HTKK format). Please place the "
				"unmodified form at {0} before exporting."
			).format(TEMPLATE_PATH)
		)

	frappe.throw(
		_(
			"05/QTT-TNCN cell mapping has not been confirmed against the official template yet. "
			"Please confirm cell coordinates in dcnet_hrm/export/qtt_tncn.py before enabling this export."
		)
	)
