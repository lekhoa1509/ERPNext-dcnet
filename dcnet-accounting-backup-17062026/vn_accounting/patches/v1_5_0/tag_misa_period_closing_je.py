"""Tag Misa-imported period-closing JEs với flag `vn_is_period_closing=1`.

Misa NKC export includes 1 monthly "Kết chuyển lãi lỗ" voucher per kỳ
(thường mã NVK%, user_remark bắt đầu bằng "Kết chuyển..."). Sau khi
import vào DB, các JE này KHÔNG được phân biệt với JE thường, khiến
B02-DN resolver (`_signed_period_movement` / `_period_movement`) đếm
luôn các bút toán Nợ/Có 5xx/6xx-→911 → triệt tiêu doanh thu/chi phí
gốc trong kỳ → BCKQHĐKD ra số gần 0.

Patch này set `vn_is_period_closing=1` cho các JE có user_remark khớp
3 pattern phổ biến nhất từ Misa export. Idempotent — chạy lại OK.

Phải chạy SAU khi Custom Field `vn_is_period_closing` được sync vào DB
(fixture custom_field.json đã ship trong cùng release).
"""

import frappe


PATTERNS = (
    "Kết chuyển lãi lỗ%",
    "Kết chuyển doanh thu%",
    "Kết chuyển chi phí%",
)


def execute():
    if not frappe.db.has_column("Journal Entry", "vn_is_period_closing"):
        # Custom Field chưa sync — Frappe sẽ sync trước khi rerun patch
        # ở migrate kế tiếp; bỏ qua an toàn.
        print("[tag_misa_period_closing_je] CF vn_is_period_closing chưa có, skip.")
        return

    total = 0
    for pat in PATTERNS:
        rows = frappe.db.sql(
            """SELECT name FROM `tabJournal Entry`
               WHERE docstatus = 1
                 AND COALESCE(vn_is_period_closing, 0) = 0
                 AND user_remark LIKE %s""",
            (pat,), as_dict=True,
        )
        for r in rows:
            frappe.db.set_value(
                "Journal Entry", r["name"],
                "vn_is_period_closing", 1, update_modified=False,
            )
            total += 1
    frappe.db.commit()
    print(f"[tag_misa_period_closing_je] tagged {total} JE")
