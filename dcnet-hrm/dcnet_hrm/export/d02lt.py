"""Xuất mẫu D02-LT (báo tăng/giảm/điều chỉnh BHXH) từ Insurance Declaration.

⚠️ CHƯA có file mẫu D02-LT gốc của BHXH Việt Nam để đối chiếu toạ độ cell —
theo nguyên tắc mục 6 của spec ("dùng openpyxl fill vào file template gốc,
KHÔNG tự vẽ layout"), hàm này CHỦ ĐỘNG DỪNG lại ở bước chuẩn bị dữ liệu và
không tự đoán vị trí cell để tránh sinh sai hồ sơ nộp BHXH.

Việc cần làm trước khi dùng ở production:
1. Đặt file mẫu gốc (không sửa) tại `export/templates/D02-LT.xlsx`.
2. Xác nhận toạ độ cell của từng cột (STT, họ tên, mã số BHXH, mức đóng cũ/
   mới, ngày hiệu lực, lý do) trong `CELL_MAP` bên dưới rồi bỏ comment ở
   `_write_rows()`.
"""

import os

import frappe
from frappe import _

TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "templates", "D02-LT.xlsx")

# ⚠️ Placeholder — CẦN xác nhận với file mẫu gốc trước khi dùng.
CELL_MAP = {
	"first_data_row": 8,
	"columns": {
		"index": 1,
		"employee_name": 2,
		"si_number": 3,
		"old_amount": 4,
		"new_amount": 5,
		"effective_date": 6,
		"reason": 7,
	},
}


def get_export_rows(insurance_declaration):
	"""Chuẩn bị dữ liệu sẵn sàng để ghi vào template — phần này KHÔNG phụ
	thuộc file mẫu, dùng được ngay khi có template."""
	doc = frappe.get_doc("Insurance Declaration", insurance_declaration)
	rows = []
	for row in doc.employees:
		rows.append(
			{
				"employee": row.employee,
				"employee_name": frappe.db.get_value("Employee", row.employee, "employee_name"),
				"si_number": row.si_number,
				"old_amount": row.old_amount,
				"new_amount": row.new_amount,
				"effective_date": row.effective_date,
				"reason": row.reason,
			}
		)
	return doc, rows


@frappe.whitelist()
def export_d02lt(insurance_declaration):
	doc, rows = get_export_rows(insurance_declaration)
	frappe.has_permission("Insurance Declaration", doc=doc, throw=True)

	if not os.path.exists(TEMPLATE_PATH):
		frappe.throw(
			_(
				"Missing the official D02-LT Excel template. Please place the unmodified Vietnam "
				"Social Insurance D02-LT.xlsx form at {0} before exporting."
			).format(TEMPLATE_PATH)
		)

	frappe.throw(
		_(
			"D02-LT cell mapping has not been confirmed against the official template yet "
			"(see dcnet_hrm/export/d02lt.py CELL_MAP). Please confirm cell coordinates before "
			"enabling this export."
		)
	)


def _write_rows(workbook, rows):  # pragma: no cover — chờ xác nhận CELL_MAP
	ws = workbook.active
	cols = CELL_MAP["columns"]
	for idx, row in enumerate(rows):
		r = CELL_MAP["first_data_row"] + idx
		ws.cell(row=r, column=cols["index"], value=idx + 1)
		ws.cell(row=r, column=cols["employee_name"], value=row["employee_name"])
		ws.cell(row=r, column=cols["si_number"], value=row["si_number"])
		ws.cell(row=r, column=cols["old_amount"], value=row["old_amount"])
		ws.cell(row=r, column=cols["new_amount"], value=row["new_amount"])
		ws.cell(row=r, column=cols["effective_date"], value=row["effective_date"])
		ws.cell(row=r, column=cols["reason"], value=row["reason"])
