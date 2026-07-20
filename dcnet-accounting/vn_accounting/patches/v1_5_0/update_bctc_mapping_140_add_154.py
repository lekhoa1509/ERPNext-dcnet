"""Update existing BCTC Mapping rows for mã 140 to include TK 154 (WIP).

Per TT99/2025, mã 140 "Hàng tồn kho" trong B01-DN gồm TK 151-158, trong
đó TK 154 "Chi phí sản xuất kinh doanh dở dang" (WIP) là cấu phần bắt buộc.

vn_small_trade template trước đây chỉ liệt kê `+152,+153,+156,+157` —
thiếu 151, 154, 155, 158. Hậu quả: nếu có TK 154 với số dư (vd dự án
xây dựng dở dang, đơn hàng sản xuất chưa hoàn thành), số dư 154 KHÔNG
được đếm vào mã 140 → B01 bị mất cân đối với chính số chênh = balance(154).

Patch này cập nhật mỗi tenant BCTC Mapping đã clone từ small template.
Bỏ qua nếu tenant đã sửa formula thành dạng khác (large template / custom).
"""

import frappe


OLD_FORMULA = "+152,+153,+156,+157"
NEW_FORMULA = "+151,+152,+153,+154,+155,+156,+157,+158"


def execute():
    rows = frappe.db.sql(
        """
        SELECT name, parent, account_formula FROM `tabBCTC Line`
        WHERE parenttype = 'BCTC Mapping' AND parentfield = 'b01_lines'
          AND code = '140'
        """,
        as_dict=True,
    )

    updated = 0
    skipped = 0
    for r in rows:
        cur = (r.account_formula or "").strip()
        if cur == OLD_FORMULA:
            frappe.db.set_value(
                "BCTC Line", r.name, "account_formula",
                NEW_FORMULA, update_modified=False,
            )
            updated += 1
        else:
            skipped += 1

    # Same fix for B03 mã 09 (Tăng/giảm hàng tồn kho) — same formula shape
    b03_rows = frappe.db.sql(
        """
        SELECT name, parent, account_formula FROM `tabBCTC Line`
        WHERE parenttype = 'BCTC Mapping' AND parentfield = 'b03_lines'
          AND code = '09'
        """,
        as_dict=True,
    )
    b03_updated = 0
    for r in b03_rows:
        cur = (r.account_formula or "").strip()
        if cur == OLD_FORMULA:
            frappe.db.set_value(
                "BCTC Line", r.name, "account_formula",
                NEW_FORMULA, update_modified=False,
            )
            b03_updated += 1

    frappe.db.commit()
    print(f"[update_bctc_mapping_140_add_154] B01 mã 140: updated {updated}, "
          f"skipped {skipped}. B03 mã 09: updated {b03_updated}.")
