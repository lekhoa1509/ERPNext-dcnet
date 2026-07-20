"""SCT (Sổ chi tiết vật tư hàng hóa) parser.

Misa "Sổ chi tiết vật tư hàng hóa" exports use a SECTIONED row layout
that the generic flat-header parser in parse_job can't decode:

  Row 1:  "SỔ CHI TIẾT VẬT TƯ HÀNG HÓA"      (title)
  Row 2:  "Kho: <<Tất cả>>, Tháng N năm Y"   (subtitle)
  Row 3:  blank
  Row 4:  primary headers   (Tên kho, Mã hàng, ..., Nhập, Xuất, Tồn, ...)
  Row 5:  sub-headers       (Số lượng, Giá trị) — for Nhập/Xuất/Tồn triplets
  Row 6+: interleaved section markers + data rows

Section markers in col 1 (the "Tên kho" column):
  "Mã kho: <code>"          starts a new warehouse section
  "Số chứng từ: <voucher>"  starts a new voucher section (or empty for OB)

Data rows have a real warehouse name in col 1 (e.g. "KHO CÔNG TY"), an
item code in col 2, and quantity/value triplets in the Nhập/Xuất/Tồn
columns. Rows with col 9 ("Diễn giải") = "Số dư đầu kỳ" are opening
balance rows and MUST be skipped (Phase 0 OB Inventory handles those).

Two functions:

  parse_sct_xlsx(path)
      Opens an xlsx and yields one normalised item-line dict per
      transaction row. Section markers become per-line attributes
      (voucher_no, warehouse_code). Used by parse_job to emit one
      Misa Migration Row per item-line.

  group_by_voucher(item_lines)
      Groups a list of item-line dicts into a {voucher_no:
      voucher_dict} map. The voucher_dict carries voucher-level
      metadata + a "lines" list. Used by the SE handler to look
      up real items for a given NKC voucher.
"""

from __future__ import annotations

from collections import OrderedDict
from typing import Any, Iterable, Iterator


# Column index → field name (0-based). Built from row 4 + row 5 of the
# Misa SCT export. Column letters in xlsx terms: A..BO (67 cols).
# Only the columns we actually need downstream are mapped; the rest
# (extension fields, statistics, etc.) are ignored.
_COL_INDEX_FIELD = {
    0:  "warehouse_name",       # Tên kho                (or section marker)
    1:  "item_code",            # Mã hàng
    2:  "item_name",            # Tên hàng
    3:  "item_description",     # Mô tả
    4:  "posting_date",         # Ngày hạch toán
    5:  "voucher_date",         # Ngày chứng từ
    6:  "invoice_date",         # Ngày hóa đơn
    7:  "invoice_no",           # Số hóa đơn
    8:  "narration",            # Diễn giải
    9:  "uom",                  # ĐVT
    10: "uom_primary",          # ĐVT chính (ĐVC)
    11: "rate",                 # Đơn giá
    12: "rate_primary",         # Đơn giá theo ĐVC
    13: "sale_rate",            # Đơn giá bán
    # Nhập (receipt) triplet
    14: "qty_in",               # Nhập | Số lượng
    15: "qty_in_primary",       # Nhập | Số lượng theo ĐVC
    16: "value_in",             # Nhập | Giá trị
    # Xuất (issue) triplet
    17: "qty_out",              # Xuất | Số lượng
    18: "qty_out_primary",      # Xuất | Số lượng theo ĐVC
    19: "value_out",            # Xuất | Giá trị
    # Tồn (balance) triplet — included for OB cross-checks
    20: "qty_balance",          # Tồn | Số lượng
    21: "qty_balance_primary",  # Tồn | Số lượng theo ĐVC
    22: "value_balance",        # Tồn | Giá trị
    23: "no_update_issue_rate", # Không cập nhật giá xuất
    24: "voucher_type",         # Loại chứng từ
    25: "stock_account",        # TK Kho
    26: "offset_account",       # TK đối ứng
    27: "item_group_code",      # Mã nhóm VTHH
    28: "item_group_name",      # Tên nhóm VTHH
    29: "party_code",           # Mã đối tượng
    30: "party_name",           # Tên đối tượng
    31: "party_address",        # Địa chỉ
    34: "expense_item_code",    # Mã khoản mục CP
    35: "expense_item_name",    # Tên khoản mục CP
    40: "project_code",         # Mã công trình
    41: "project_name",         # Tên công trình
    66: "branch",               # Chi nhánh
}

# Marker prefixes in col 1
_MARKER_WAREHOUSE = "Mã kho:"
_MARKER_VOUCHER = "Số chứng từ:"
# Narration that means "this is an opening balance row, skip it"
_OPENING_BALANCE_NARRATION = "Số dư đầu kỳ"

# Header row signatures used to verify SCT layout. parse_job will check
# the title row contains "SỔ CHI TIẾT VẬT TƯ" before invoking us — we
# don't re-verify here, but bail gracefully if the layout doesn't match.
_HEADER_TITLE_SUBSTR = "SỔ CHI TIẾT VẬT TƯ"


def _str_or_none(val: Any) -> str | None:
    if val is None:
        return None
    s = str(val).strip()
    return s or None


def _to_float(val: Any) -> float:
    if val is None or val == "":
        return 0.0
    if isinstance(val, (int, float)):
        return float(val)
    s = str(val).strip().replace(",", "")
    if not s:
        return 0.0
    try:
        return float(s)
    except ValueError:
        return 0.0


def _to_date_str(val: Any) -> str | None:
    if val is None or val == "":
        return None
    if hasattr(val, "isoformat"):
        return val.isoformat()[:10]
    s = str(val).strip()
    return s[:10] if s else None


def _parse_marker(cell: str) -> tuple[str, str] | None:
    """Return (kind, value) for a section-marker cell, or None.

    kind ∈ {"warehouse", "voucher"}; value is the right-hand-side
    (possibly empty string for the OB-section voucher marker).
    """
    if not cell:
        return None
    s = str(cell).strip()
    if s.startswith(_MARKER_WAREHOUSE):
        return ("warehouse", s[len(_MARKER_WAREHOUSE):].strip())
    if s.startswith(_MARKER_VOUCHER):
        return ("voucher", s[len(_MARKER_VOUCHER):].strip())
    return None


def parse_sct_rows(
    raw_rows: Iterable[tuple],
    skip_first_n: int = 5,
) -> Iterator[dict[str, Any]]:
    """Walk a stream of raw xlsx rows; yield one item-line dict per data row.

    Tracks current warehouse_code + current voucher_no via section
    markers. Skips opening balance rows (narration = "Số dư đầu kỳ").

    Args:
        raw_rows: iterable of cell tuples (xlsx row.values).
        skip_first_n: rows to skip at start (title + subtitle + blank +
            primary header + sub-header). Default 5 = standard SCT layout.

    Yields:
        Dict per item-line. Keys are from _COL_INDEX_FIELD plus:
            - "voucher_no":     str from "Số chứng từ:" marker
            - "warehouse_code": str from "Mã kho:" marker
        Numerics (qty/value) are floats; dates are ISO strings or None.
    """
    current_warehouse_code: str | None = None
    current_voucher_no: str | None = None

    for i, row in enumerate(raw_rows):
        if i < skip_first_n:
            continue
        if not row:
            continue

        # Normalise to a tuple of fixed width for safe indexing
        cells = list(row)

        # Section marker?
        col1 = cells[0] if len(cells) > 0 else None
        marker = _parse_marker(col1) if col1 else None
        if marker:
            kind, val = marker
            if kind == "warehouse":
                current_warehouse_code = val or None
            elif kind == "voucher":
                # Empty value = OB section (no voucher_no). Subsequent
                # rows until next "Số chứng từ:" marker are OB rows.
                current_voucher_no = val or None
            continue

        # Skip opening-balance lines (col 9 = "Số dư đầu kỳ")
        narration = cells[8] if len(cells) > 8 else None
        if _str_or_none(narration) == _OPENING_BALANCE_NARRATION:
            continue

        # Skip if we haven't entered a voucher section yet
        if not current_voucher_no:
            continue

        # Skip rows without an item code (defensive — Misa sometimes
        # emits decorative blank lines between vouchers)
        item_code = _str_or_none(cells[1] if len(cells) > 1 else None)
        if not item_code:
            continue

        out: dict[str, Any] = {
            "voucher_no": current_voucher_no,
            "warehouse_code": current_warehouse_code,
        }
        for ci, fname in _COL_INDEX_FIELD.items():
            if ci >= len(cells):
                continue
            val = cells[ci]
            if val is None:
                continue
            if fname in {
                "posting_date", "voucher_date", "invoice_date",
            }:
                out[fname] = _to_date_str(val)
            elif fname in {
                "rate", "rate_primary", "sale_rate",
                "qty_in", "qty_in_primary", "value_in",
                "qty_out", "qty_out_primary", "value_out",
                "qty_balance", "qty_balance_primary", "value_balance",
            }:
                fv = _to_float(val)
                if fv != 0:
                    out[fname] = fv
            else:
                s = _str_or_none(val)
                if s is not None:
                    out[fname] = s

        yield out


def parse_sct_xlsx(file_path: str) -> Iterator[dict[str, Any]]:
    """Open a Misa SCT xlsx and stream item-line dicts. Used by parse_job.

    Loads the active worksheet in read_only mode for memory efficiency
    on large files (1k+ rows typical).
    """
    from openpyxl import load_workbook
    wb = load_workbook(file_path, read_only=True, data_only=True)
    ws = wb.active
    try:
        yield from parse_sct_rows(ws.iter_rows(values_only=True))
    finally:
        wb.close()


def group_by_voucher(
    item_lines: Iterable[dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    """Group a flat list of item-line dicts into {voucher_no: voucher_dict}.

    voucher_dict shape:
        {
          "voucher_no": str,
          "voucher_type": str | None,    # Misa Loại chứng từ
          "posting_date": str | None,
          "stock_account": str | None,
          "offset_account": str | None,
          "warehouse_codes": [str, ...],  # all warehouses touched
          "warehouse_names": [str, ...],
          "party_code": str | None,
          "party_name": str | None,
          "project_code": str | None,
          "lines": [
            {item_code, item_name, uom, qty_in, qty_out, value_in,
             value_out, warehouse_name, ...},
            ...
          ],
        }

    Voucher-level metadata (posting_date, voucher_type, etc.) is taken
    from the FIRST line of that voucher. Subsequent lines' metadata is
    expected to be consistent — we don't validate divergence here.
    """
    buckets: OrderedDict[str, dict[str, Any]] = OrderedDict()
    for line in item_lines:
        vno = line.get("voucher_no")
        if not vno:
            continue
        if vno not in buckets:
            buckets[vno] = {
                "voucher_no": vno,
                "voucher_type": line.get("voucher_type"),
                "posting_date": line.get("posting_date"),
                "voucher_date": line.get("voucher_date"),
                "invoice_no": line.get("invoice_no"),
                "invoice_date": line.get("invoice_date"),
                "stock_account": line.get("stock_account"),
                "offset_account": line.get("offset_account"),
                "narration": line.get("narration"),
                "party_code": line.get("party_code"),
                "party_name": line.get("party_name"),
                "project_code": line.get("project_code"),
                "project_name": line.get("project_name"),
                "branch": line.get("branch"),
                "warehouse_codes": [],
                "warehouse_names": [],
                "lines": [],
            }
        v = buckets[vno]
        v["lines"].append({
            "item_code": line.get("item_code"),
            "item_name": line.get("item_name"),
            "item_description": line.get("item_description"),
            "item_group_code": line.get("item_group_code"),
            "item_group_name": line.get("item_group_name"),
            "uom": line.get("uom") or "Nos",
            "uom_primary": line.get("uom_primary"),
            "warehouse_name": line.get("warehouse_name"),
            "warehouse_code": line.get("warehouse_code"),
            "qty_in": float(line.get("qty_in") or 0.0),
            "qty_out": float(line.get("qty_out") or 0.0),
            "value_in": float(line.get("value_in") or 0.0),
            "value_out": float(line.get("value_out") or 0.0),
            "rate": float(line.get("rate") or 0.0),
        })
        wc = line.get("warehouse_code")
        wn = line.get("warehouse_name")
        if wc and wc not in v["warehouse_codes"]:
            v["warehouse_codes"].append(wc)
        if wn and wn not in v["warehouse_names"]:
            v["warehouse_names"].append(wn)
    return dict(buckets)


def iter_vouchers_from_batch(batch_name: str) -> dict[str, dict[str, Any]]:
    """Load SCT rows from Misa Migration Row records for a batch and
    return them grouped by voucher_no. Production entry point — tests
    should call ``group_by_voucher(parse_sct_rows(...))`` directly.
    """
    import json
    import frappe

    rows_raw = frappe.db.sql(
        """SELECT raw_payload FROM `tabMisa Migration Row`
           WHERE batch = %s AND file_type = 'SCT' AND entity_type = 'Voucher Line'
           ORDER BY row_index ASC""",
        (batch_name,),
        as_dict=True,
    )
    lines: list[dict[str, Any]] = []
    for r in rows_raw:
        try:
            lines.append(json.loads(r["raw_payload"]))
        except (TypeError, ValueError):
            continue
    return group_by_voucher(lines)
