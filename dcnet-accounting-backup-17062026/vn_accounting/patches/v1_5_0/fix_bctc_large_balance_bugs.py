"""Fix 6 BCTC Mapping bugs ở template large enterprise gây mất cân đối B01.

Phát hiện trên DCNET TEST (mã 270 = 12B, mã 440 = 130B — diff 118B).

Bug list:
1. Mã 136 — `+1385,+1388,+334,+338`: thiếu TK 141 (Tạm ứng) + nhầm 334/338
   (đó là liability, không vào mã 136). Sửa: `+1385,+1388,+141`.
2. Mã 151 — `+2421`: không match TK 242 (khi tenant không split sub-account).
   Sửa: `+242,+2421`.
3. Mã 319 — `+338` overlap với 318 (+3387) → double-count.
   Sửa: `+3381,+3382,+3383,+3384,+3385,+3386,+3388`.
4. Mã 320 — `+341,+3411,+3412`: prefix +341 match toàn bộ 341x family
   → double-count với +3411 explicit. Sửa: `+3411,+3412`.
5. Mã 321 — `+3521`: chỉ match 1 sub-TK của 352. Sửa: `+352%` (gồm tất cả
   sub-TK dự phòng phải trả).
6. Mã 336+337 — `+3387` và `+338` đã ở mã 318+319 ngắn hạn → để trống.
   Sửa: cả hai → "".
7. Mã 338 — `+3411,...,+3415`: overlap 3411+3412 với mã 320.
   Sửa: `+3413,+3414,+3415` (chỉ vay dài hạn).

Patch idempotent — chỉ update khi formula khớp pattern cũ (ko đụng custom).
"""

import frappe


FIXES = [
    # (code, old_formula_exact, new_formula, note)
    ('136', '+1385,+1388,+334,+338', '+1385,+1388,+141',
     '+TK 141 Tạm ứng; bỏ 334/338 (liability)'),
    ('151', '+2421', '+242,+2421',
     '+TK 242 cho tenant không split sub-account'),
    ('319', '+338', '+3381,+3382,+3383,+3384,+3385,+3386,+3388',
     'loại 3387 (đã ở mã 318) tránh double-count'),
    ('320', '+341,+3411,+3412', '+3411,+3412',
     'bỏ +341 prefix overlap 3411-3415'),
    ('321', '+3521', '+352%',
     'gồm toàn bộ 352* (3521 + 3522 + 3523 + 3524 …)'),
    ('336', '+3387', '',
     '3387 đã ở mã 318 ngắn hạn'),
    ('337', '+338', '',
     '338 đã ở mã 319 ngắn hạn'),
    ('338', '+3411,+3412,+3413,+3414,+3415', '+3413,+3414,+3415',
     '3411+3412 đã ở mã 320 ngắn hạn'),
]


def execute():
    rows = frappe.db.sql(
        """SELECT name, parent, code, account_formula
           FROM `tabBCTC Line`
           WHERE parenttype IN ('BCTC Mapping', 'BCTC Mapping Template')
             AND parentfield = 'b01_lines'
             AND code IN ('136','151','319','320','321','336','337','338')
        """,
        as_dict=True,
    )

    updated = 0
    skipped = 0
    for r in rows:
        match = next((f for f in FIXES if f[0] == r.code and (r.account_formula or '').strip() == f[1]), None)
        if not match:
            skipped += 1
            continue
        _, _, new_f, note = match
        frappe.db.set_value(
            "BCTC Line", r.name, "account_formula",
            new_f, update_modified=False,
        )
        updated += 1

    frappe.db.commit()
    print(f"[fix_bctc_large_balance_bugs] updated {updated} BCTC Line, "
          f"skipped {skipped} (custom or already fixed).")
