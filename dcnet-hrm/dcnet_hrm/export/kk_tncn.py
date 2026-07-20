"""Xuất mẫu 05/KK-TNCN (tờ khai khấu trừ thuế TNCN theo tháng/quý) từ dữ
liệu report `05-KK-TNCN` (dcnet_hrm/report/05_kk_tncn/).

⚠️ Cùng tình trạng với `d02lt.py`/`qtt_tncn.py`: CHƯA có file mẫu HTKK
chính thức để đối chiếu toạ độ cell.
"""

import os

import frappe
from frappe import _

TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "templates", "05-KK-TNCN.xlsx")


@frappe.whitelist()
def export_kk_tncn(company=None, from_date=None, to_date=None):
	if not os.path.exists(TEMPLATE_PATH):
		frappe.throw(
			_(
				"Missing the official 05/KK-TNCN Excel template (HTKK format). Please place the "
				"unmodified form at {0} before exporting."
			).format(TEMPLATE_PATH)
		)

	frappe.throw(
		_(
			"05/KK-TNCN cell mapping has not been confirmed against the official template yet. "
			"Please confirm cell coordinates in dcnet_hrm/export/kk_tncn.py before enabling this export."
		)
	)
