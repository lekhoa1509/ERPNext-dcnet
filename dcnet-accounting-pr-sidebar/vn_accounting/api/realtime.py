"""Realtime cho Query Reports (FB-2026-00625).

Endpoint dirty-check rẻ: trả "vân tay" (fingerprint) của dữ liệu nguồn để client
quyết định có cần re-query report nặng hay không. Xem
docs/specs/2026-05-29-realtime-query-reports-analysis.md.
"""

import frappe
from frappe.query_builder.functions import Count, Max


@frappe.whitelist()
def report_data_fingerprint(doctypes: str = "", company: str | None = None) -> str:
	"""Trả fingerprint gọn của các doctype nguồn.

	Fingerprint = "<doctype>:<max_modified>:<count>|..." gộp mọi doctype.
	Client so fingerprint cũ/mới; chỉ refresh report khi đổi.

	Rẻ: mỗi doctype 1 query MAX(modified)+COUNT, dùng index sẵn có.
	An toàn: validate doctype tồn tại trước khi truy vấn (tên bảng do client gửi);
	dùng query builder nên tên bảng được escape, không nối chuỗi SQL thô.
	"""
	if not doctypes:
		return ""
	dts = frappe.parse_json(doctypes) if isinstance(doctypes, str) else doctypes
	if not isinstance(dts, (list, tuple)):
		return ""

	parts = []
	for dt in dts:
		if not isinstance(dt, str) or not frappe.db.exists("DocType", dt):
			continue

		table = frappe.qb.DocType(dt)
		query = (
			frappe.qb.from_(table)
			.select(Max(table.modified), Count(table.name))
			.where(table.docstatus.isin([1, 2]))  # bắt cả submit lẫn cancel
		)
		# chỉ lọc company nếu doctype có trường company
		if company and frappe.get_meta(dt).has_field("company"):
			query = query.where(table.company == company)

		row = query.run()
		max_modified, count = (row[0][0], row[0][1]) if row else (None, 0)
		parts.append(f"{dt}:{max_modified}:{count}")

	return "|".join(parts)
