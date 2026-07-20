"""B09-DN multi-sheet Excel generator — Thuyết minh BCTC theo TT99/2025."""
from __future__ import annotations

import io
import os
from datetime import date

import frappe
from frappe import _
from frappe.utils import getdate, now_datetime

# Gray background for auto-fill cells
_FILL_AUTOFILL = None
_FILL_WHITE = None
_FONT_HEADER = None
_FONT_BODY = None


def _init_styles():
    """Lazy-init openpyxl style objects (avoid import at module load)."""
    global _FILL_AUTOFILL, _FILL_WHITE, _FONT_HEADER, _FONT_BODY
    if _FILL_AUTOFILL is not None:
        return
    from openpyxl.styles import Font, PatternFill
    _FILL_AUTOFILL = PatternFill(fill_type="solid", fgColor="ECECEC")
    _FILL_WHITE = PatternFill(fill_type=None)
    _FONT_HEADER = Font(name="Times New Roman", size=11, bold=True)
    _FONT_BODY = Font(name="Times New Roman", size=11)


@frappe.whitelist()
def generate_b09(company: str, fiscal_year: str) -> dict:
    """Generate B09-DN multi-sheet Excel for the given company and fiscal year.

    Returns:
        dict with keys: file_url, file_name, sheets_generated
    """
    _init_styles()
    from openpyxl import Workbook
    from openpyxl.utils import get_column_letter

    fy = frappe.get_doc("Fiscal Year", fiscal_year)
    period_start = getdate(fy.year_start_date)
    period_end = getdate(fy.year_end_date)

    wb = Workbook()
    sheets_generated = []

    # Sheet 1: Văn xuôi (always generated)
    ws1 = wb.active
    ws1.title = "1_Van_xuoi"
    _build_van_xuoi_sheet(ws1, company, fiscal_year, period_start, period_end)
    sheets_generated.append("1_Van_xuoi — Thuyết minh văn xuôi (kế toán điền)")

    # Sheet 2: 5.1 Chi tiết phải thu (TK 131)
    data_131 = _get_ar_detail(company, period_end)
    if data_131:
        ws = wb.create_sheet("5.1_Chi_tiet_phai_thu")
        _build_ar_detail_sheet(ws, company, period_end, data_131)
        sheets_generated.append("5.1_Chi_tiet_phai_thu — Chi tiết TK 131")

    # Sheet 3: 5.2 Chi tiết phải trả (TK 331)
    data_331 = _get_ap_detail(company, period_end)
    if data_331:
        ws = wb.create_sheet("5.2_Chi_tiet_phai_tra")
        _build_ap_detail_sheet(ws, company, period_end, data_331)
        sheets_generated.append("5.2_Chi_tiet_phai_tra — Chi tiết TK 331")

    # Sheet 4: 5.3 Biến động TSCĐ
    data_assets = _get_asset_movement(company, period_start, period_end)
    if data_assets:
        ws = wb.create_sheet("5.3_Bien_dong_TSCD")
        _build_asset_movement_sheet(ws, company, period_start, period_end, data_assets)
        sheets_generated.append("5.3_Bien_dong_TSCD — Biến động tài sản cố định")

    # Sheet 5: 5.4 Biến động hàng tồn kho
    data_htk = _get_inventory_summary(company, period_start, period_end)
    if data_htk:
        ws = wb.create_sheet("5.4_Bien_dong_HTK")
        _build_inventory_sheet(ws, company, period_start, period_end, data_htk)
        sheets_generated.append("5.4_Bien_dong_HTK — Hàng tồn kho")

    # Sheet 6: 5.6 Biến động vốn chủ sở hữu
    data_vcsh = _get_equity_movement(company, period_start, period_end)
    if data_vcsh:
        ws = wb.create_sheet("5.6_Bien_dong_VCSH")
        _build_equity_sheet(ws, company, period_start, period_end, data_vcsh)
        sheets_generated.append("5.6_Bien_dong_VCSH — Vốn chủ sở hữu")

    # Save to Frappe file
    output = io.BytesIO()
    wb.save(output)
    output.seek(0)

    file_name = f"B09-DN_{company.replace(' ', '_')}_{fiscal_year}.xlsx"
    file_doc = frappe.new_doc("File")
    file_doc.file_name = file_name
    file_doc.content = output.read()
    file_doc.is_private = 0
    file_doc.insert(ignore_permissions=True)

    return {
        "file_url": file_doc.file_url,
        "file_name": file_name,
        "sheets_generated": sheets_generated,
    }


# ── Sheet builders ────────────────────────────────────────────────────────────

def _build_van_xuoi_sheet(ws, company, fiscal_year, period_start, period_end):
    """Sheet 1: Văn xuôi — TT99/2025 template with kế toán fill placeholders."""
    from openpyxl.styles import Alignment
    ws.column_dimensions["A"].width = 80

    rows = [
        ("THUYẾT MINH BÁO CÁO TÀI CHÍNH", True, False),
        (f"Năm tài chính: {fiscal_year}  |  Công ty: {company}", False, False),
        ("", False, False),
        ("PHẦN I. ĐẶC ĐIỂM HOẠT ĐỘNG CỦA DOANH NGHIỆP", True, False),
        ("1.1. Tên doanh nghiệp: [Kế toán điền: tên đầy đủ theo Giấy ĐKDN]", False, True),
        ("1.2. Địa chỉ trụ sở chính: [Kế toán điền]", False, True),
        ("1.3. Ngành nghề kinh doanh chính: [Kế toán điền: mã ngành + tên ngành]", False, True),
        ("1.4. Loại hình doanh nghiệp: [Kế toán điền: TNHH / Cổ phần / DNTN / HKD]", False, True),
        ("1.5. Số giấy phép ĐKDN + ngày cấp + cơ quan cấp: [Kế toán điền]", False, True),
        ("", False, False),
        ("PHẦN II. KỲ KẾ TOÁN, ĐƠN VỊ TIỀN TỆ SỬ DỤNG TRONG KẾ TOÁN", True, False),
        (f"2.1. Kỳ kế toán năm: từ {period_start.strftime('%d/%m/%Y')} đến {period_end.strftime('%d/%m/%Y')}", False, False),
        ("2.2. Đơn vị tiền tệ sử dụng trong kế toán: Đồng Việt Nam (VND)", False, False),
        ("2.3. Nguyên tắc chuyển đổi ngoại tệ: [Kế toán điền theo chính sách ngoại tệ DN đang áp dụng]", False, True),
        ("", False, False),
        ("PHẦN III. CHUẨN MỰC VÀ CHẾ ĐỘ KẾ TOÁN ÁP DỤNG", True, False),
        ("3.1. Chế độ kế toán: Thông tư 200/2014/TT-BTC + Thông tư 99/2025/TT-BTC", False, False),
        ("3.2. Chuẩn mực kế toán Việt Nam (VAS) áp dụng: theo quyết định của Bộ Tài chính", False, False),
        ("3.3. Hình thức kế toán: [Kế toán điền: Nhật ký chung / Chứng từ ghi sổ / Nhật ký - Sổ cái]", False, True),
        ("", False, False),
        ("PHẦN IV. CHÍNH SÁCH KẾ TOÁN CHI TIẾT", True, False),
        ("4.1. Nguyên tắc ghi nhận doanh thu:", True, False),
        ("[Kế toán điền: nguyên tắc ghi nhận doanh thu, hàng trả lại, chiết khấu thương mại]", False, True),
        ("4.2. Chi phí sản xuất kinh doanh:", True, False),
        ("[Kế toán điền: phương pháp tính giá thành, phân bổ chi phí chung]", False, True),
        ("4.3. Phương pháp khấu hao TSCĐ:", True, False),
        ("[Kế toán điền: đường thẳng / số dư giảm dần / theo sản lượng; thời gian sử dụng ước tính]", False, True),
        ("4.4. Phương pháp tính giá hàng tồn kho:", True, False),
        ("[Kế toán điền: FIFO / bình quân gia quyền / thực tế đích danh]", False, True),
        ("4.5. Dự phòng:", True, False),
        ("[Kế toán điền: chính sách dự phòng phải thu khó đòi, hàng tồn kho lỗi thời, đầu tư tài chính]", False, True),
        ("", False, False),
        ("PHẦN VI. SỰ KIỆN SAU NGÀY KẾT THÚC NIÊN ĐỘ KẾ TOÁN", True, False),
        ("[Kế toán điền: các sự kiện quan trọng sau ngày kết thúc niên độ đến ngày phát hành BCTC, nếu có]", False, True),
        ("", False, False),
        ("--- Hết thuyết minh văn xuôi. Phần V chi tiết khoản mục xem các sheet tiếp theo. ---", False, False),
    ]

    for row_idx, (text, bold, is_placeholder) in enumerate(rows, start=1):
        cell = ws.cell(row=row_idx, column=1, value=text)
        cell.font = _FONT_HEADER if bold else _FONT_BODY
        if is_placeholder:
            cell.fill = _FILL_WHITE
        else:
            cell.fill = _FILL_AUTOFILL
        cell.alignment = Alignment(wrap_text=True, vertical="top")

    ws.sheet_view.showGridLines = True


def _build_detail_header(ws, title: str, columns: list[str], data_rows):
    """Write a standard header + data rows. Returns last row index."""
    from openpyxl.styles import Alignment

    ws.cell(row=1, column=1, value=title).font = _FONT_HEADER
    ws.cell(row=1, column=1).fill = _FILL_AUTOFILL

    # Column headers
    for col_idx, col_name in enumerate(columns, start=1):
        cell = ws.cell(row=2, column=col_idx, value=col_name)
        cell.font = _FONT_HEADER
        cell.fill = _FILL_AUTOFILL
        cell.alignment = Alignment(horizontal="center")

    # Data rows
    for row_offset, row_data in enumerate(data_rows, start=3):
        for col_idx, val in enumerate(row_data, start=1):
            cell = ws.cell(row=row_offset, column=col_idx, value=val)
            cell.font = _FONT_BODY
            cell.fill = _FILL_AUTOFILL  # auto-fill — locked

    return 2 + len(data_rows)


def _build_ar_detail_sheet(ws, company, period_end, data):
    columns = ["Khách hàng", "TK", "Dư nợ cuối kỳ", "0–30 ngày", "31–60 ngày",
               "61–90 ngày", ">90 ngày", "Dự phòng (2293)", "Ghi chú"]
    ws.column_dimensions["A"].width = 35
    for i in "BCDEFGH":
        ws.column_dimensions[i].width = 16
    ws.column_dimensions["I"].width = 30
    last = _build_detail_header(ws, "V.1 — Chi tiết TK 131 (Phải thu khách hàng)", columns, data)
    # Last col (Ghi chú) is editable
    for row in range(3, last + 1):
        ws.cell(row=row, column=9).fill = _FILL_WHITE


def _build_ap_detail_sheet(ws, company, period_end, data):
    columns = ["Nhà cung cấp", "TK", "Dư có cuối kỳ", "0–30 ngày", "31–60 ngày",
               "61–90 ngày", ">90 ngày", "Ghi chú"]
    ws.column_dimensions["A"].width = 35
    for i in "BCDEFG":
        ws.column_dimensions[i].width = 16
    ws.column_dimensions["H"].width = 30
    last = _build_detail_header(ws, "V.2 — Chi tiết TK 331 (Phải trả người bán)", columns, data)
    for row in range(3, last + 1):
        ws.cell(row=row, column=8).fill = _FILL_WHITE


def _build_asset_movement_sheet(ws, company, period_start, period_end, data):
    columns = ["Nhóm TSCĐ", "Nguyên giá đầu kỳ", "Tăng trong kỳ", "Giảm trong kỳ",
               "Nguyên giá cuối kỳ", "KH lũy kế đầu kỳ", "KH kỳ này", "Giảm KH",
               "KH lũy kế cuối kỳ", "GTCL cuối kỳ"]
    _build_detail_header(ws, "V.3 — Biến động TSCĐ hữu hình", columns, data)
    ws.column_dimensions["A"].width = 30


def _build_inventory_sheet(ws, company, period_start, period_end, data):
    columns = ["Nhóm / SKU", "TK", "Tồn đầu kỳ", "Nhập trong kỳ", "Xuất trong kỳ",
               "Tồn cuối kỳ", "Dự phòng (2294)", "Ghi chú"]
    _build_detail_header(ws, "V.4 — Chi tiết hàng tồn kho", columns, data)
    ws.column_dimensions["A"].width = 40


def _build_equity_sheet(ws, company, period_start, period_end, data):
    columns = ["Khoản mục VCSH", "TK", "Đầu kỳ", "Tăng trong kỳ", "Giảm trong kỳ",
               "Cuối kỳ", "Ghi chú"]
    _build_detail_header(ws, "V.6 — Biến động vốn chủ sở hữu", columns, data)
    ws.column_dimensions["A"].width = 35


# ── Data fetchers ─────────────────────────────────────────────────────────────

def _get_ar_detail(company, period_end) -> list:
    """Fetch TK 131 balance per customer with aging buckets."""
    rows = frappe.db.sql("""
        SELECT
            party AS customer,
            SUM(debit) - SUM(credit) AS balance,
            SUM(CASE WHEN DATEDIFF(%(end_date)s, posting_date) <= 30 THEN debit - credit ELSE 0 END) AS bucket_30,
            SUM(CASE WHEN DATEDIFF(%(end_date)s, posting_date) BETWEEN 31 AND 60 THEN debit - credit ELSE 0 END) AS bucket_60,
            SUM(CASE WHEN DATEDIFF(%(end_date)s, posting_date) BETWEEN 61 AND 90 THEN debit - credit ELSE 0 END) AS bucket_90,
            SUM(CASE WHEN DATEDIFF(%(end_date)s, posting_date) > 90 THEN debit - credit ELSE 0 END) AS bucket_over
        FROM `tabGL Entry`
        WHERE company = %(company)s
          AND posting_date <= %(end_date)s
          AND is_cancelled = 0
          AND account LIKE '131%%'
          AND party IS NOT NULL AND party != ''
        GROUP BY party
        HAVING balance > 1
        ORDER BY balance DESC
    """, {"company": company, "end_date": period_end}, as_dict=True)

    result = []
    for r in rows:
        result.append([
            r.customer, "131", r.balance or 0,  # "131" = TK label column (display only)
            r.bucket_30 or 0, r.bucket_60 or 0, r.bucket_90 or 0, r.bucket_over or 0,
            0,  # dự phòng — để trống
            ""  # ghi chú — editable
        ])
    return result


def _get_ap_detail(company, period_end) -> list:
    rows = frappe.db.sql("""
        SELECT
            party AS supplier,
            SUM(credit) - SUM(debit) AS balance,
            SUM(CASE WHEN DATEDIFF(%(end_date)s, posting_date) <= 30 THEN credit - debit ELSE 0 END) AS bucket_30,
            SUM(CASE WHEN DATEDIFF(%(end_date)s, posting_date) BETWEEN 31 AND 60 THEN credit - debit ELSE 0 END) AS bucket_60,
            SUM(CASE WHEN DATEDIFF(%(end_date)s, posting_date) BETWEEN 61 AND 90 THEN credit - debit ELSE 0 END) AS bucket_90,
            SUM(CASE WHEN DATEDIFF(%(end_date)s, posting_date) > 90 THEN credit - debit ELSE 0 END) AS bucket_over
        FROM `tabGL Entry`
        WHERE company = %(company)s
          AND posting_date <= %(end_date)s
          AND is_cancelled = 0
          AND account LIKE '331%%'
          AND party IS NOT NULL AND party != ''
        GROUP BY party
        HAVING balance > 1
        ORDER BY balance DESC
    """, {"company": company, "end_date": period_end}, as_dict=True)

    return [
        [r.supplier, "331", r.balance or 0,  # "331" = TK label column (display only)
         r.bucket_30 or 0, r.bucket_60 or 0, r.bucket_90 or 0, r.bucket_over or 0, ""]
        for r in rows
    ]


def _get_asset_movement(company, period_start, period_end) -> list:
    """Fetch TSCĐ movement by asset category."""
    rows = frappe.db.sql("""
        SELECT
            ac.name AS category,
            SUM(a.purchase_amount) AS gross_current,
            SUM(CASE WHEN a.purchase_date BETWEEN %(from_date)s AND %(to_date)s
                     THEN a.purchase_amount ELSE 0 END) AS additions,
            SUM(a.value_after_depreciation) AS net_current
        FROM `tabAsset` a
        LEFT JOIN `tabAsset Category` ac ON a.asset_category = ac.name
        WHERE a.company = %(company)s
          AND a.docstatus = 1
        GROUP BY ac.name
        ORDER BY ac.name
    """, {"company": company, "from_date": period_start, "to_date": period_end}, as_dict=True)

    if not rows:
        return []

    result = []
    for r in rows:
        result.append([
            r.category or "Khác",
            r.gross_current or 0, r.additions or 0, 0,
            r.gross_current or 0,
            0, 0, 0, 0,
            r.net_current or 0
        ])
    return result


def _get_inventory_summary(company, period_start, period_end) -> list:
    """Fetch hàng tồn kho summary from Stock Ledger Entry, joining Item for item_group."""
    rows = frappe.db.sql("""
        SELECT
            i.item_group AS item_group,
            SUM(CASE WHEN sle.posting_date < %(from_date)s THEN sle.stock_value_difference ELSE 0 END) AS opening_value,
            SUM(CASE WHEN sle.posting_date BETWEEN %(from_date)s AND %(to_date)s
                          AND sle.stock_value_difference > 0 THEN sle.stock_value_difference ELSE 0 END) AS in_value,
            SUM(CASE WHEN sle.posting_date BETWEEN %(from_date)s AND %(to_date)s
                          AND sle.stock_value_difference < 0 THEN ABS(sle.stock_value_difference) ELSE 0 END) AS out_value,
            SUM(CASE WHEN sle.posting_date <= %(to_date)s THEN sle.stock_value_difference ELSE 0 END) AS closing_value
        FROM `tabStock Ledger Entry` sle
        LEFT JOIN `tabItem` i ON sle.item_code = i.name
        WHERE sle.company = %(company)s
          AND sle.docstatus = 1
        GROUP BY i.item_group
        HAVING closing_value > 1
        ORDER BY i.item_group
    """, {"company": company, "from_date": period_start, "to_date": period_end}, as_dict=True)

    if not rows:
        return []

    return [
        [r.item_group or "Khác", "151-156",
         r.opening_value or 0, r.in_value or 0, r.out_value or 0,
         r.closing_value or 0, 0, ""]
        for r in rows
    ]


def _get_equity_movement(company, period_start, period_end) -> list:
    """Fetch VCSH movement from GL Entry for TK 4xx accounts."""
    rows = frappe.db.sql("""
        SELECT
            account,
            SUM(CASE WHEN posting_date < %(from_date)s THEN credit - debit ELSE 0 END) AS opening_bal,
            SUM(CASE WHEN posting_date BETWEEN %(from_date)s AND %(to_date)s
                          AND credit > debit THEN credit - debit ELSE 0 END) AS increase_val,
            SUM(CASE WHEN posting_date BETWEEN %(from_date)s AND %(to_date)s
                          AND debit > credit THEN debit - credit ELSE 0 END) AS decrease_val,
            SUM(CASE WHEN posting_date <= %(to_date)s THEN credit - debit ELSE 0 END) AS closing_bal
        FROM `tabGL Entry`
        WHERE company = %(company)s
          AND posting_date <= %(to_date)s
          AND is_cancelled = 0
          AND account LIKE '4%%'
        GROUP BY account
        HAVING ABS(closing_bal) > 1
        ORDER BY account
    """, {"company": company, "from_date": period_start, "to_date": period_end}, as_dict=True)

    if not rows:
        return []

    return [
        [r.account, r.account[:3],
         r.opening_bal or 0, r.increase_val or 0, r.decrease_val or 0,
         r.closing_bal or 0, ""]
        for r in rows
    ]
