"""NKC (Sổ Nhật ký chung) parser — group rows by Số chứng từ, balance check.

Per spec §5: each Misa NKC row represents ONE leg of a voucher. N-row voucher
= N legs. We do NOT dedupe legs and we do NOT pair-match. The "TK đối ứng"
column is Misa display-only and is completely ignored.

Input shape per row (keys = Vietnamese Misa headers from parse_job):

    {
      "Ngày hạch toán":   "2026-01-01" | datetime,
      "Ngày chứng từ":    "2026-01-01" | datetime,
      "Số chứng từ":      "BC20260001",
      "Ngày hóa đơn":     "" | "2026-01-01" | datetime,
      "Số hóa đơn":       "" | "3777-HK",
      "Mã đối tượng":     "PTE.A.1206.1121",
      "Tên đối tượng":    "LÊ THỊ BÍCH TRÂN",
      "Diễn giải chung":  "...",
      "Diễn giải":        "...",
      "Tài khoản":        "11215",
      "TK đối ứng":       "131",          # ignored
      "Phát sinh Nợ":     "209000" | 209000,
      "Phát sinh Có":     "0" | 0,
      "Chi nhánh":        "..."           # optional, may not exist
    }

Output per voucher:

    {
      "voucher_no":     "BC20260001",
      "prefix":         "BC",
      "posting_date":   "2026-01-01",
      "voucher_date":   "2026-01-01",
      "invoice_date":   None | "2026-01-01",
      "invoice_no":     None | "3777-HK",
      "party_code":     "PTE.A.1206.1121",
      "party_name":     "LÊ THỊ BÍCH TRÂN",
      "voucher_remark": "...",
      "branch":         None | "...",
      "legs": [
        {"account": "11215", "debit": 209000.0, "credit": 0.0, "leg_desc": "..."},
        {"account": "131",   "debit": 0.0,      "credit": 209000.0, "leg_desc": "..."},
      ],
      "total_dr":       209000.0,
      "total_cr":       209000.0,
      "row_indices":    [4, 5],  # 1-based positions in source rows list
    }
"""

from __future__ import annotations

import re
from collections import OrderedDict
from typing import Any, Iterable

# Vietnamese Misa headers — exact strings as emitted by parse_job._row_to_dict
H_POSTING_DATE = "Ngày hạch toán"
H_VOUCHER_DATE = "Ngày chứng từ"
H_VOUCHER_NO = "Số chứng từ"
H_INVOICE_DATE = "Ngày hóa đơn"
H_INVOICE_NO = "Số hóa đơn"
H_PARTY_CODE = "Mã đối tượng"
H_PARTY_NAME = "Tên đối tượng"
H_VOUCHER_REMARK = "Diễn giải chung"
H_LEG_DESC = "Diễn giải"
H_ACCOUNT = "Tài khoản"
H_DEBIT = "Phát sinh Nợ"
H_CREDIT = "Phát sinh Có"
H_BRANCH = "Chi nhánh"

# Known Misa voucher prefixes (per spec §2.2). Longest-first so "PXHN" beats "PX",
# "PNHN" beats "PN", "PBDT"/"PBPTT" beat "PB"/"PT", "CTNB" beats "CT".
KNOWN_PREFIXES = (
    "PXHN", "PNHN", "PBPTT", "PBDT", "CTNB",
    "MDV", "UNC", "NVK",
    "BC", "BH", "CK", "KH", "MH", "PC", "PN", "PT", "PX",
)

# Balance tolerance: 0.01 VND. Misa exports are integer VND, but openpyxl
# sometimes promotes int → float during cell value resolution.
BALANCE_TOLERANCE = 0.01


class BalanceError(ValueError):
    """Raised when a voucher's Dr total != Cr total within tolerance."""

    def __init__(self, voucher_no: str, total_dr: float, total_cr: float):
        self.voucher_no = voucher_no
        self.total_dr = total_dr
        self.total_cr = total_cr
        diff = total_dr - total_cr
        super().__init__(
            f"Voucher {voucher_no} unbalanced: Dr={total_dr} Cr={total_cr} diff={diff}"
        )


def extract_prefix(voucher_no: str) -> str:
    """Return the longest matching known prefix for a Misa Số chứng từ.

    Examples:
      BC20260001    -> "BC"
      PXHN20260005  -> "PXHN"
      PBPTT2026001  -> "PBPTT"
      UNC20260012   -> "UNC"

    Fallback: leading uppercase letter run (greedy). Empty string for blank/numeric.
    """
    if not voucher_no:
        return ""
    s = str(voucher_no).strip()
    if not s:
        return ""
    # Try known prefixes longest-first
    for p in KNOWN_PREFIXES:
        if s.startswith(p):
            return p
    # Fallback: leading uppercase letters
    m = re.match(r"^([A-Z]+)", s)
    return m.group(1) if m else ""


def _to_float(val: Any) -> float:
    """Coerce a Misa numeric cell to float. Empty/None → 0.0."""
    if val is None or val == "":
        return 0.0
    if isinstance(val, (int, float)):
        return float(val)
    s = str(val).strip()
    if not s:
        return 0.0
    # Some Misa exports use "1,234,567" — strip thousand separators
    s = s.replace(",", "")
    try:
        return float(s)
    except ValueError:
        return 0.0


def _to_date_str(val: Any) -> str | None:
    """Normalize a Misa date cell to ISO YYYY-MM-DD string. Empty → None."""
    if val is None or val == "":
        return None
    if hasattr(val, "isoformat"):
        s = val.isoformat()
    else:
        s = str(val).strip()
    if not s:
        return None
    # Strip time portion if any
    return s[:10]


def _str_or_none(val: Any) -> str | None:
    if val is None:
        return None
    s = str(val).strip()
    return s or None


def parse_nkc_rows(
    rows: Iterable[dict[str, Any]],
    raise_on_unbalanced: bool = False,
) -> list[dict[str, Any]]:
    """Group an iterable of NKC row dicts by Số chứng từ; one voucher dict per group.

    Args:
      rows: iterable of dicts with Vietnamese Misa keys (see module docstring).
      raise_on_unbalanced: if True, raise BalanceError on first unbalanced voucher.
            If False (default), tag voucher dict with "balance_error" string and continue.

    Returns:
      list of voucher dicts in first-seen order. Rows missing Số chứng từ are
      silently dropped (callers should already have filtered blank rows).
    """
    buckets: OrderedDict[str, dict[str, Any]] = OrderedDict()

    for idx, row in enumerate(rows, start=1):
        voucher_no = _str_or_none(row.get(H_VOUCHER_NO))
        if not voucher_no:
            continue

        leg = {
            "account": _str_or_none(row.get(H_ACCOUNT)) or "",
            "debit": _to_float(row.get(H_DEBIT)),
            "credit": _to_float(row.get(H_CREDIT)),
            "leg_desc": _str_or_none(row.get(H_LEG_DESC)),
            "party_code": _str_or_none(row.get(H_PARTY_CODE)),
        }

        if voucher_no not in buckets:
            buckets[voucher_no] = {
                "voucher_no": voucher_no,
                "prefix": extract_prefix(voucher_no),
                "posting_date": _to_date_str(row.get(H_POSTING_DATE)),
                "voucher_date": _to_date_str(row.get(H_VOUCHER_DATE)),
                "invoice_date": _to_date_str(row.get(H_INVOICE_DATE)),
                "invoice_no": _str_or_none(row.get(H_INVOICE_NO)),
                "party_code": _str_or_none(row.get(H_PARTY_CODE)),
                "party_name": _str_or_none(row.get(H_PARTY_NAME)),
                "voucher_remark": _str_or_none(row.get(H_VOUCHER_REMARK)),
                "branch": _str_or_none(row.get(H_BRANCH)),
                "legs": [],
                "row_indices": [],
            }

        buckets[voucher_no]["legs"].append(leg)
        buckets[voucher_no]["row_indices"].append(idx)

    # Dedup identical legs per voucher — only safe when GCD scaling applies.
    # Misa NKC export emits one row per reporting axis × leg. For SIMPLE
    # vouchers (e.g. 2-leg UNC salary), every leg is duplicated identically
    # by the same factor N (typically 3). For COMPLEX vouchers (multi-line
    # invoices with VAT splits + deferred revenue), the per-leg duplication
    # factor varies (5× for VAT, 3× for revenue) — collapsing identical
    # tuples then loses balance.
    #
    # Safe dedup: only when ALL distinct (account, debit, credit, leg_desc)
    # tuples appear the SAME number of times (uniform scaling). Compute the
    # scaling factor N and keep one copy of each.
    from collections import Counter
    for v in buckets.values():
        if not v["legs"]:
            continue
        # Count occurrences of each canonical tuple
        keyfn = lambda l: (
            l["account"], round(l["debit"], 2),
            round(l["credit"], 2), l["leg_desc"] or "",
        )
        counts = Counter(keyfn(l) for l in v["legs"])
        # All counts equal AND >1 → uniform scaling, safe to collapse
        count_values = set(counts.values())
        if len(count_values) == 1 and count_values.pop() > 1:
            seen: set[tuple] = set()
            deduped: list[dict[str, Any]] = []
            for leg in v["legs"]:
                k = keyfn(leg)
                if k in seen:
                    continue
                seen.add(k)
                deduped.append(leg)
            v["legs"] = deduped
        # else: mixed counts → leave alone (uniform per-axis dedup unsafe)

    # Compute balance + finalize per voucher
    out: list[dict[str, Any]] = []
    for v in buckets.values():
        total_dr = sum(l["debit"] for l in v["legs"])
        total_cr = sum(l["credit"] for l in v["legs"])
        v["total_dr"] = total_dr
        v["total_cr"] = total_cr
        if abs(total_dr - total_cr) > BALANCE_TOLERANCE:
            v["balance_error"] = (
                f"Dr={total_dr} ≠ Cr={total_cr} diff={total_dr - total_cr}"
            )
            if raise_on_unbalanced:
                raise BalanceError(v["voucher_no"], total_dr, total_cr)
        out.append(v)
    return out


def iter_vouchers_from_batch(
    batch_name: str,
    raise_on_unbalanced: bool = False,
) -> list[dict[str, Any]]:
    """Load NKC rows from Misa Migration Row records for a batch and parse them.

    Reads docs where file_type='NKC' and entity_type='Voucher', ordered by
    row_index. Each row's raw_payload (JSON) is decoded back into a dict and
    fed to parse_nkc_rows().

    This is the production entry point. Tests should call parse_nkc_rows
    directly with inline fixtures.
    """
    import json

    import frappe

    rows_raw = frappe.db.sql(
        """SELECT raw_payload FROM `tabMisa Migration Row`
           WHERE batch = %s AND file_type = 'NKC' AND entity_type = 'Voucher'
           ORDER BY row_index ASC""",
        (batch_name,),
        as_dict=True,
    )

    def _decode():
        for r in rows_raw:
            try:
                yield json.loads(r["raw_payload"] or "{}")
            except (ValueError, TypeError):
                continue

    return parse_nkc_rows(_decode(), raise_on_unbalanced=raise_on_unbalanced)
