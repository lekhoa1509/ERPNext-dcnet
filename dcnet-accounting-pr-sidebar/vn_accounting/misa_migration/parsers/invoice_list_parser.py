"""Bảng kê hóa đơn parser — group rows by Số chứng từ into invoice docs.

Two file kinds:
  BR ("Bán ra" — sales)     → 29 columns, output feeds Sales Invoice builder
  MV ("Mua vào" — purchases) → 24 columns, output feeds Purchase Invoice builder

Each file contains:
  - Title rows (rows 0-1)
  - Header row (row 3 in 1-based Misa convention)
  - Occasional GROUP SUMMARY rows ("Nhóm HHDV: 2. Hàng hóa, dịch vụ ...") that
    cluster line items by Misa goods/service group — these have empty
    "Số chứng từ" cell and must be SKIPPED, not treated as line items.
  - Line item rows with full Số chứng từ + invoice metadata + qty/rate/tax.

Multiple line items per voucher are common:
  - Most invoices have 1 line.
  - ~40 sales invoices have multi-Item structure (different services).
  - Purchase MV often has multi-leg structure too (especially DECIX-style
    transit + peering bundle).

Output one dict per voucher_no, with line_items[] preserved in source order.

Voucher-level metadata is taken from the FIRST line of that voucher (Misa
guarantees consistent invoice_no/date/party across all rows of a voucher).
"""

from __future__ import annotations

import re
from collections import OrderedDict
from typing import Any, Iterable, Literal

# Vietnamese Misa headers — common to BR + MV
H_INVOICE_TEMPLATE = "Ký hiệu mẫu HĐ"
H_INVOICE_SERIES = "Ký hiệu HĐ"
H_INVOICE_NO = "Số hóa đơn"
H_INVOICE_DATE = "Ngày hóa đơn"
H_POSTING_DATE = "Ngày hạch toán"
H_VOUCHER_DATE = "Ngày chứng từ"
H_VOUCHER_NO = "Số chứng từ"
H_DESCRIPTION = "Diễn giải"
H_ITEM_NAME = "Mặt hàng"
H_UOM = "ĐVT"
H_QTY = "Số lượng"
H_RATE_NT = "Đơn giá NT"
H_RATE = "Đơn giá"
H_TAX_RATE = "Thuế suất"
H_TAX_AMOUNT_NT = "Thuế GTGT NT"
H_TAX_AMOUNT = "Thuế GTGT"
H_TAX_ACCOUNT = "Tài khoản thuế"
H_BRANCH = "Chi nhánh"

# BR-specific
H_BR_BUYER_NAME = "Tên người mua"
H_BR_BUYER_TAX = "Mã số thuế người mua"
H_BR_NET_NT = "Doanh số bán chưa có thuế GTGT"     # Both NT + VND share this label
H_BR_NET_ALT = "Doanh số bán chưa có thuế"          # Alt header without "GTGT" suffix (some Misa exports)
H_BR_DISCOUNT_NT = "Tiền thuế GTGT giảm trừ NT"
H_BR_DISCOUNT = "Tiền thuế GTGT giảm trừ"
H_BR_NQ406 = "Giảm 30% thuế GTGT theo NQ406"
H_BR_NOTE = "Ghi chú"

# MV-specific
H_MV_SELLER_NAME = "Tên người bán"
H_MV_SELLER_TAX = "Mã số thuế người bán"
H_MV_NET = "Giá trị HHDV mua vào chưa có thuế GTGT"  # Both NT + VND share label
H_MV_NET_ALT = "Giá trị HHDV mua vào chưa có thuế"   # Alt header without "GTGT" suffix
H_MV_DOC_TYPE = "Loại chứng từ"
H_MV_IS_IMPORT = "Là chứng từ nhập khẩu HHDV"


def _get_net(row: dict[str, Any], primary: str, alt: str) -> float:
    """Net-amount lookup with fallback. Different Misa export templates
    use 'Giá trị HHDV mua vào chưa có thuế GTGT' OR 'Giá trị HHDV mua vào
    chưa có thuế' (no GTGT). Same trap on BR side. Try primary first,
    fall back to alt."""
    v = row.get(primary)
    if v in (None, "", 0, "0"):
        v = row.get(alt)
    return _to_float(v)

# Group-summary detection: the first column ("Ký hiệu mẫu HĐ") in summary rows
# contains text like "Nhóm HHDV: ..." (BR) or "Nhóm HHDV mua vào: ..." (MV).
_GROUP_PREFIXES = ("Nhóm HHDV", "Nhóm HH ")


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
        s = val.isoformat()
    else:
        s = str(val).strip()
    if not s:
        return None
    return s[:10]


_TAX_RATE_RE = re.compile(r"(\d+(?:\.\d+)?)\s*%")


def parse_tax_rate(val: Any) -> float:
    """Parse Misa "Thuế suất" cell into a float percentage.

    Accepts: "0 %" / "10 %" / "8 %" / "5%" / "" / None / "KCT" / "KKT".
    Returns 0.0 for any non-numeric value (KCT = Không Chịu Thuế = 0%).
    """
    if val is None or val == "":
        return 0.0
    s = str(val).strip()
    if not s or s.upper() in ("KCT", "KKT", "KCT*", "KKT*", "K"):
        return 0.0
    m = _TAX_RATE_RE.search(s)
    if m:
        return float(m.group(1))
    # Fallback: try direct float
    try:
        return float(s)
    except ValueError:
        return 0.0


def _is_group_summary_row(row: dict[str, Any]) -> bool:
    """Detect Misa group-summary rows that must be skipped.

    Heuristic: first column contains "Nhóm HHDV..." marker, AND Số chứng từ is
    blank. Either signal alone is unreliable — combine both to avoid false
    positives.
    """
    voucher_no = _str_or_none(row.get(H_VOUCHER_NO))
    if voucher_no:
        return False  # has voucher_no = real line item
    first_col = _str_or_none(row.get(H_INVOICE_TEMPLATE))
    if not first_col:
        return False
    return any(first_col.startswith(p) for p in _GROUP_PREFIXES)


def _extract_line_item_br(row: dict[str, Any]) -> dict[str, Any]:
    """One BR line item dict from a row. BR-specific fields populated."""
    return {
        "description": _str_or_none(row.get(H_DESCRIPTION)),
        "item_name": _str_or_none(row.get(H_ITEM_NAME)),
        "uom": _str_or_none(row.get(H_UOM)),
        "qty": _to_float(row.get(H_QTY)),
        "rate_nt": _to_float(row.get(H_RATE_NT)),
        "rate": _to_float(row.get(H_RATE)),
        "net_amount": _get_net(row, H_BR_NET_NT, H_BR_NET_ALT),  # VND value, w/ alt header fallback
        "tax_rate_str": _str_or_none(row.get(H_TAX_RATE)),
        "tax_rate": parse_tax_rate(row.get(H_TAX_RATE)),
        "tax_amount": _to_float(row.get(H_TAX_AMOUNT)),
        "tax_amount_nt": _to_float(row.get(H_TAX_AMOUNT_NT)),
        "tax_account": _str_or_none(row.get(H_TAX_ACCOUNT)),
        "discount_amount": _to_float(row.get(H_BR_DISCOUNT)),
        "discount_amount_nt": _to_float(row.get(H_BR_DISCOUNT_NT)),
        "nq406_pct": _str_or_none(row.get(H_BR_NQ406)),
        "note": _str_or_none(row.get(H_BR_NOTE)),
    }


def _extract_line_item_mv(row: dict[str, Any]) -> dict[str, Any]:
    """One MV line item dict from a row. MV-specific fields populated."""
    return {
        "description": _str_or_none(row.get(H_DESCRIPTION)),
        "item_name": _str_or_none(row.get(H_ITEM_NAME)),
        "uom": _str_or_none(row.get(H_UOM)),
        "qty": _to_float(row.get(H_QTY)),
        "rate_nt": _to_float(row.get(H_RATE_NT)),
        "rate": _to_float(row.get(H_RATE)),
        "net_amount": _get_net(row, H_MV_NET, H_MV_NET_ALT),
        "tax_rate_str": _str_or_none(row.get(H_TAX_RATE)),
        "tax_rate": parse_tax_rate(row.get(H_TAX_RATE)),
        "tax_amount": _to_float(row.get(H_TAX_AMOUNT)),
        "tax_amount_nt": _to_float(row.get(H_TAX_AMOUNT_NT)),
        "tax_account": _str_or_none(row.get(H_TAX_ACCOUNT)),
    }


def _extract_voucher_header_br(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "voucher_no": _str_or_none(row.get(H_VOUCHER_NO)),
        "kind": "BR",
        "posting_date": _to_date_str(row.get(H_POSTING_DATE)),
        "voucher_date": _to_date_str(row.get(H_VOUCHER_DATE)),
        "invoice_date": _to_date_str(row.get(H_INVOICE_DATE)),
        "invoice_no": _str_or_none(row.get(H_INVOICE_NO)),
        "invoice_series": _str_or_none(row.get(H_INVOICE_SERIES)),
        "invoice_template": _str_or_none(row.get(H_INVOICE_TEMPLATE)),
        "party_name": _str_or_none(row.get(H_BR_BUYER_NAME)),
        "party_tax_id": _str_or_none(row.get(H_BR_BUYER_TAX)),
        "branch": _str_or_none(row.get(H_BRANCH)),
    }


def _extract_voucher_header_mv(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "voucher_no": _str_or_none(row.get(H_VOUCHER_NO)),
        "kind": "MV",
        "posting_date": _to_date_str(row.get(H_POSTING_DATE)),
        "voucher_date": _to_date_str(row.get(H_VOUCHER_DATE)),
        "invoice_date": _to_date_str(row.get(H_INVOICE_DATE)),
        "invoice_no": _str_or_none(row.get(H_INVOICE_NO)),
        "invoice_series": _str_or_none(row.get(H_INVOICE_SERIES)),
        "invoice_template": _str_or_none(row.get(H_INVOICE_TEMPLATE)),
        "party_name": _str_or_none(row.get(H_MV_SELLER_NAME)),
        "party_tax_id": _str_or_none(row.get(H_MV_SELLER_TAX)),
        "branch": _str_or_none(row.get(H_BRANCH)),
        "doc_type_note": _str_or_none(row.get(H_MV_DOC_TYPE)),
        "is_import": bool(_str_or_none(row.get(H_MV_IS_IMPORT))),
    }


def parse_invoice_list(
    rows: Iterable[dict[str, Any]],
    kind: Literal["BR", "MV"],
) -> list[dict[str, Any]]:
    """Group bảng kê rows by Số chứng từ. Returns one invoice dict per voucher.

    Args:
      rows: iterable of dicts with Vietnamese Misa keys.
      kind: 'BR' (bán ra / sales) or 'MV' (mua vào / purchases) — controls
            which party-name + amount columns to read.

    Behaviour:
      - Group-summary rows ("Nhóm HHDV: ...") are skipped.
      - Voucher header captured from first line of voucher.
      - line_items[] preserved in source order, one entry per non-summary row.
      - Totals (total_net / total_tax / total_gross) computed at end.
    """
    if kind not in ("BR", "MV"):
        raise ValueError(f"kind must be 'BR' or 'MV', got {kind!r}")

    header_extractor = _extract_voucher_header_br if kind == "BR" else _extract_voucher_header_mv
    line_extractor = _extract_line_item_br if kind == "BR" else _extract_line_item_mv

    buckets: OrderedDict[str, dict[str, Any]] = OrderedDict()

    for row in rows:
        if _is_group_summary_row(row):
            continue
        voucher_no = _str_or_none(row.get(H_VOUCHER_NO))
        if not voucher_no:
            continue

        if voucher_no not in buckets:
            v = header_extractor(row)
            v["line_items"] = []
            buckets[voucher_no] = v
        buckets[voucher_no]["line_items"].append(line_extractor(row))

    # Compute totals
    out: list[dict[str, Any]] = []
    for v in buckets.values():
        total_net = sum(li["net_amount"] for li in v["line_items"])
        total_tax = sum(li["tax_amount"] for li in v["line_items"])
        v["total_net"] = total_net
        v["total_tax"] = total_tax
        v["total_gross"] = total_net + total_tax
        out.append(v)
    return out


def iter_invoices_from_batch(
    batch_name: str,
    kind: Literal["BR", "MV"],
) -> list[dict[str, Any]]:
    """Load bảng kê rows from Misa Migration Row records and parse them.

    file_type stored by parse_job: 'Bang ke BR' or 'Bang ke MV'.
    entity_type for both: 'Voucher'.
    """
    import json

    import frappe

    file_type = "Bang ke BR" if kind == "BR" else "Bang ke MV"
    rows_raw = frappe.db.sql(
        """SELECT raw_payload FROM `tabMisa Migration Row`
           WHERE batch = %s AND file_type = %s AND entity_type = 'Voucher'
           ORDER BY row_index ASC""",
        (batch_name, file_type),
        as_dict=True,
    )

    def _decode():
        for r in rows_raw:
            try:
                yield json.loads(r["raw_payload"] or "{}")
            except (ValueError, TypeError):
                continue

    return parse_invoice_list(_decode(), kind=kind)
