"""Opening-balance (số dư đầu kỳ) parsers for the 9 Misa SDK exports.

Phase E commit 13a. Each Misa file ships a distinct xlsx schema; we
normalize them all into typed dicts that the Phase 0 handlers consume.

Categories (file → parser fn → emitted dict shape):

| Misa file                                              | Parser              | Emits per row                        |
|--------------------------------------------------------|---------------------|--------------------------------------|
| Danh_sach_so_du_tai_khoan.xlsx                         | parse_account_balance  | {account_number, account_name, dr, cr}  |
| Danh_sach_nhap_so_du_tai_khoan_ngan_hang.xlsx          | parse_bank_balance     | {bank_no, bank_name, account_number, dr, cr} |
| Danh_sach_cong_no_khach_hang.xlsx                      | parse_customer_ar      | {account_number, party_code, party_name, dr, cr} |
| Danh_sach_cong_no_nha_cung_cap.xlsx                    | parse_supplier_ap      | {account_number, party_code, party_name, dr, cr} |
| Danh_sach_cong_no_nhan_vien.xlsx                       | parse_employee_advance | {account_number, party_code, party_name, dr, cr} |
| Danh_sach_ton_kho_vthh.xlsx                            | parse_inventory        | {posting_date, voucher_no, item_code, item_name, item_group, uom, warehouse, qty, rate, amount, lot} |
| Danh_sach_tai_san_co_dinh_dau_ky.xlsx                  | parse_fixed_asset      | {asset_code, asset_name, asset_category, location, gross_amount, depreciable_amount, accumulated_depreciation, available_for_use_date, depreciation_start_date, useful_life_months, remaining_useful_life_months} |
| Danh_sach_cong_cu_dung_cu_dau_ky.xlsx                  | parse_ccdc             | {ccdc_code, ccdc_name, available_for_use_date, qty, gross_amount, remaining_amount, total_periods, remaining_periods, per_period_amount, holding_account, suspended} |
| Danh_sach_chi_phi_tra_truoc_dau_ky.xlsx                | parse_prepaid_expense  | {prepaid_code, prepaid_name, recognition_date, total_amount, remaining_amount, total_periods, remaining_periods, per_period_amount, holding_account} |

Row skip rules (all files):
- Header rows (rows 0..N where N is parser-specific) are skipped.
- "Tổng" summary footer rows are skipped (column 2/3 == "Tổng").
- Rows with empty `Số tài khoản` / `Mã *` first identifying column are
  skipped silently.

Date strings come back as ISO `YYYY-MM-DD`. Amounts come back as
`float`. Empty/None monetary cells → 0.0.
"""

from __future__ import annotations

from typing import Any, Iterable


def _to_float(val: Any) -> float:
    if val is None or val == "":
        return 0.0
    if isinstance(val, (int, float)):
        return float(val)
    s = str(val).replace(",", "").replace(" ", "").strip()
    if not s:
        return 0.0
    try:
        return float(s)
    except (TypeError, ValueError):
        return 0.0


def _to_str(val: Any) -> str | None:
    if val is None:
        return None
    s = str(val).strip()
    return s or None


def _to_date(val: Any) -> str | None:
    """ISO YYYY-MM-DD or None."""
    if val is None or val == "":
        return None
    if hasattr(val, "isoformat"):
        s = val.isoformat()
        return s.split("T")[0] if "T" in s else s.split(" ")[0]
    s = str(val).strip()
    if " " in s:
        s = s.split(" ", 1)[0]
    return s or None


def _to_int(val: Any) -> int | None:
    if val is None or val == "":
        return None
    if isinstance(val, int):
        return val
    if isinstance(val, float):
        return int(val)
    s = str(val).strip()
    if not s:
        return None
    try:
        return int(float(s))
    except (TypeError, ValueError):
        return None


def _is_summary_row(row: tuple) -> bool:
    """Misa adds a "Tổng" footer row that has 'Tổng' in one of the early
    columns and totals in the amount columns. Skip these.
    """
    for cell in row[:5]:
        if cell and str(cell).strip().lower() in ("tổng", "tong"):
            return True
    return False


# ---------------------------------------------------------------- per-file parsers

def parse_account_balance(rows: Iterable[tuple]) -> list[dict]:
    """Parse opening balance per Account.

    Auto-detects 2 layouts:

    Layout A — `Danh_sach_so_du_tai_khoan.xlsx` (≤5 cols, header idx 2):
      STT | Số TK | Tên TK | Dư Nợ | Dư Có

    Layout B — `Bang_can_doi_tai_khoan*.xlsx` (≥7 cols, header idx 7-8):
      Số TK | Tên TK | Đầu kỳ Nợ | Đầu kỳ Có | PS Nợ | PS Có | CB Nợ | CB Có
      For OB load, ONLY the Đầu kỳ columns matter — PS/CB ignored (those
      come from Phase 4 NKC activity, not from this file).

    Returns one dict per non-summary row with a non-empty account number,
    same shape `{account_number, account_name, dr, cr}` regardless of layout.
    """
    out: list[dict] = []
    rows = list(rows)
    if not rows:
        return out
    # Detect layout by max column count
    max_cols = max((len(r) for r in rows if r), default=0)
    is_bcdtk = max_cols >= 7

    # Find first data row: skip until we hit a row with a numeric-looking TK
    # in col 0 (BCDTK) or col 1 (Layout A). Avoid hard-coded header offsets
    # because Misa BCDTK templates vary in title-block row count.
    tk_col = 0 if is_bcdtk else 1
    name_col = 1 if is_bcdtk else 2
    if is_bcdtk:
        dr_col, cr_col = 2, 3  # Đầu kỳ Nợ, Đầu kỳ Có
    else:
        dr_col, cr_col = 3, 4  # Dư Nợ, Dư Có

    for row in rows:
        if not row or _is_summary_row(row):
            continue
        if len(row) <= tk_col:
            continue
        acct_no = _to_str(row[tk_col])
        if not acct_no:
            continue
        # Reject header-leak rows (acct_no is header text like "Số tài khoản")
        if acct_no.lower().startswith(("số tài khoản", "stt", "mã ")):
            continue
        out.append({
            "account_number": acct_no,
            "account_name": _to_str(row[name_col]) if len(row) > name_col else None,
            "dr": _to_float(row[dr_col]) if len(row) > dr_col else 0.0,
            "cr": _to_float(row[cr_col]) if len(row) > cr_col else 0.0,
        })
    return out


def parse_bank_balance(rows: Iterable[tuple]) -> list[dict]:
    """Parse `Danh_sach_nhap_so_du_tai_khoan_ngan_hang.xlsx`.

    Row layout (header at index 2):
      STT | Số TK ngân hàng | Tên ngân hàng | Số tài khoản | Dư Nợ | Dư Có
    """
    out: list[dict] = []
    rows = list(rows)
    for row in rows[3:]:
        if not row or _is_summary_row(row):
            continue
        bank_no = _to_str(row[1]) if len(row) > 1 else None
        acct_no = _to_str(row[3]) if len(row) > 3 else None
        if not bank_no and not acct_no:
            continue
        out.append({
            "bank_no": bank_no,
            "bank_name": _to_str(row[2]) if len(row) > 2 else None,
            "account_number": acct_no,
            "dr": _to_float(row[4]) if len(row) > 4 else 0.0,
            "cr": _to_float(row[5]) if len(row) > 5 else 0.0,
        })
    return out


def _parse_party_balance(rows: Iterable[tuple]) -> list[dict]:
    """Shared parser for Customer/Supplier/Employee AR/AP files.

    Row layout (header at index 2):
      STT | Số tài khoản | Mã (KH/NCC/NV) | Tên (KH/NCC/NV) | Dư Nợ | Dư Có
    """
    out: list[dict] = []
    rows = list(rows)
    for row in rows[3:]:
        if not row or _is_summary_row(row):
            continue
        party_code = _to_str(row[2]) if len(row) > 2 else None
        if not party_code:
            continue
        out.append({
            "account_number": _to_str(row[1]) if len(row) > 1 else None,
            "party_code": party_code,
            "party_name": _to_str(row[3]) if len(row) > 3 else None,
            "dr": _to_float(row[4]) if len(row) > 4 else 0.0,
            "cr": _to_float(row[5]) if len(row) > 5 else 0.0,
        })
    return out


def parse_customer_ar(rows):
    return _parse_party_balance(rows)


def parse_supplier_ap(rows):
    return _parse_party_balance(rows)


def parse_employee_advance(rows):
    return _parse_party_balance(rows)


def parse_inventory(rows: Iterable[tuple]) -> list[dict]:
    """Parse `Danh_sach_ton_kho_vthh.xlsx`.

    Row layout (header at index 3 — has extra title + "Kho: Tất cả" rows):
      STT | Ngày nhập kho | Số phiếu nhập | Mã hàng | Tên hàng |
      Nhóm VTHH | ĐVT | Mã kho | Số lượng tồn | Đơn giá | Giá trị tồn | Số lô
    """
    out: list[dict] = []
    rows = list(rows)
    for row in rows[4:]:  # skip 4-line header
        if not row or _is_summary_row(row):
            continue
        item_code = _to_str(row[3]) if len(row) > 3 else None
        if not item_code:
            continue
        out.append({
            "posting_date": _to_date(row[1]) if len(row) > 1 else None,
            "voucher_no": _to_str(row[2]) if len(row) > 2 else None,
            "item_code": item_code,
            "item_name": _to_str(row[4]) if len(row) > 4 else None,
            "item_group": _to_str(row[5]) if len(row) > 5 else None,
            "uom": _to_str(row[6]) if len(row) > 6 else None,
            "warehouse": _to_str(row[7]) if len(row) > 7 else None,
            "qty": _to_float(row[8]) if len(row) > 8 else 0.0,
            "rate": _to_float(row[9]) if len(row) > 9 else 0.0,
            "amount": _to_float(row[10]) if len(row) > 10 else 0.0,
            "lot": _to_str(row[11]) if len(row) > 11 else None,
        })
    return out


def parse_fixed_asset(rows: Iterable[tuple]) -> list[dict]:
    """Parse `Danh_sach_tai_san_co_dinh_dau_ky.xlsx`.

    Row layout (header at index 2):
      STT | Mã tài sản | Tên tài sản | Loại tài sản | Đơn vị sử dụng |
      Nguyên giá | Giá trị tính KH | Hao mòn lũy kế | Ngày ghi tăng |
      Ngày tính KH | Thời gian SD (tháng) | Thời gian SD còn lại (tháng)
    """
    out: list[dict] = []
    rows = list(rows)
    for row in rows[3:]:
        if not row or _is_summary_row(row):
            continue
        asset_code = _to_str(row[1]) if len(row) > 1 else None
        if not asset_code:
            continue
        out.append({
            "asset_code": asset_code,
            "asset_name": _to_str(row[2]) if len(row) > 2 else None,
            "asset_category": _to_str(row[3]) if len(row) > 3 else None,
            "location": _to_str(row[4]) if len(row) > 4 else None,
            "gross_amount": _to_float(row[5]) if len(row) > 5 else 0.0,
            "depreciable_amount": _to_float(row[6]) if len(row) > 6 else 0.0,
            "accumulated_depreciation": _to_float(row[7]) if len(row) > 7 else 0.0,
            "available_for_use_date": _to_date(row[8]) if len(row) > 8 else None,
            "depreciation_start_date": _to_date(row[9]) if len(row) > 9 else None,
            "useful_life_months": _to_int(row[10]) if len(row) > 10 else None,
            "remaining_useful_life_months": _to_int(row[11]) if len(row) > 11 else None,
        })
    return out


def parse_ccdc(rows: Iterable[tuple]) -> list[dict]:
    """Parse `Danh_sach_cong_cu_dung_cu_dau_ky.xlsx`.

    Row layout (header at index 2):
      STT | Mã CCDC | Tên CCDC | Ngày ghi tăng | Số lượng |
      Giá trị CCDC | Giá trị còn lại | Số kỳ phân bổ | Số kỳ PB còn lại |
      Số tiền PB hàng kỳ | TK chờ phân bổ | Ngừng phân bổ
    """
    out: list[dict] = []
    rows = list(rows)
    for row in rows[3:]:
        if not row or _is_summary_row(row):
            continue
        ccdc_code = _to_str(row[1]) if len(row) > 1 else None
        if not ccdc_code:
            continue
        out.append({
            "ccdc_code": ccdc_code,
            "ccdc_name": _to_str(row[2]) if len(row) > 2 else None,
            "available_for_use_date": _to_date(row[3]) if len(row) > 3 else None,
            "qty": _to_float(row[4]) if len(row) > 4 else 0.0,
            "gross_amount": _to_float(row[5]) if len(row) > 5 else 0.0,
            "remaining_amount": _to_float(row[6]) if len(row) > 6 else 0.0,
            "total_periods": _to_int(row[7]) if len(row) > 7 else None,
            "remaining_periods": _to_int(row[8]) if len(row) > 8 else None,
            "per_period_amount": _to_float(row[9]) if len(row) > 9 else 0.0,
            "holding_account": _to_str(row[10]) if len(row) > 10 else None,
            "suspended": bool(_to_str(row[11])) if len(row) > 11 else False,
        })
    return out


def parse_prepaid_expense(rows: Iterable[tuple]) -> list[dict]:
    """Parse `Danh_sach_chi_phi_tra_truoc_dau_ky.xlsx`.

    Row layout (header at index 2):
      STT | Mã CP trả trước | Tên CP trả trước | Ngày ghi nhận |
      Số tiền | Số tiền còn lại | Số kỳ phân bổ | Số kỳ phân bổ còn lại |
      Số tiền PB hàng kỳ | Tài khoản chờ phân bổ
    """
    out: list[dict] = []
    rows = list(rows)
    for row in rows[3:]:
        if not row or _is_summary_row(row):
            continue
        prepaid_code = _to_str(row[1]) if len(row) > 1 else None
        if not prepaid_code:
            continue
        out.append({
            "prepaid_code": prepaid_code,
            "prepaid_name": _to_str(row[2]) if len(row) > 2 else None,
            "recognition_date": _to_date(row[3]) if len(row) > 3 else None,
            "total_amount": _to_float(row[4]) if len(row) > 4 else 0.0,
            "remaining_amount": _to_float(row[5]) if len(row) > 5 else 0.0,
            "total_periods": _to_int(row[6]) if len(row) > 6 else None,
            "remaining_periods": _to_int(row[7]) if len(row) > 7 else None,
            "per_period_amount": _to_float(row[8]) if len(row) > 8 else 0.0,
            "holding_account": _to_str(row[9]) if len(row) > 9 else None,
        })
    return out


# Public router used by Phase 0 orchestrator (one file → one parser)
PARSER_BY_FILE_TYPE: dict[str, callable] = {
    "OB Account Balance": parse_account_balance,
    "OB Bank Balance": parse_bank_balance,
    "OB Customer AR": parse_customer_ar,
    "OB Supplier AP": parse_supplier_ap,
    "OB Employee Advance": parse_employee_advance,
    "OB Inventory": parse_inventory,
    "OB Fixed Asset": parse_fixed_asset,
    "OB CCDC": parse_ccdc,
    "OB Prepaid Expense": parse_prepaid_expense,
}


# Auto-detect file_type from xlsx title (row 0) — used by upload handler
TITLE_TO_FILE_TYPE: dict[str, str] = {
    "danh sách số dư tài khoản": "OB Account Balance",
    # BCDTK = Bảng cân đối tài khoản — Misa "mẫu quản trị" export.
    # Contains both OB + period activity + CB; parser extracts only Đầu kỳ
    # columns (other columns redundant with NKC Phase 4 + computed CB).
    "bảng cân đối tài khoản": "OB Account Balance",
    "danh sách nhập số dư tài khoản": "OB Bank Balance",
    "danh sách công nợ khách hàng": "OB Customer AR",
    "danh sách công nợ nhà cung cấp": "OB Supplier AP",
    "danh sách công nợ nhân viên": "OB Employee Advance",
    "danh sách tồn kho": "OB Inventory",
    "danh sách tài sản cố định": "OB Fixed Asset",
    "danh sách công cụ dụng cụ": "OB CCDC",
    "danh sách chi phí trả trước": "OB Prepaid Expense",
}


def detect_file_type(title_row: str | None) -> str | None:
    """Map the xlsx row-0 title to a Phase 0 file_type string.

    Args:
      title_row: row 0 cell A content (case-insensitive substring match).
    Returns:
      File type name from `PARSER_BY_FILE_TYPE` keys, or None on no match.
    """
    if not title_row:
        return None
    t = str(title_row).strip().lower()
    for prefix, ft in TITLE_TO_FILE_TYPE.items():
        if t.startswith(prefix):
            return ft
    return None
