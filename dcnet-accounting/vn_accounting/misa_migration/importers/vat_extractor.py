"""Shared VAT account + amount extraction for SI/PI handlers.

Misa NKC encodes VAT via two distinct VN VAS chart positions:

  Output VAT (Sales):    Cr 33311 / Cr 3331*  — owed to tax authority
  Input VAT (Purchases): Dr 1331            — recoverable from tax authority

Both are tied to a single Misa "Tài khoản thuế" cell on each bảng kê line
item (e.g. '33311' for sales, '1331' for purchases). The NKC contains the
matching GL leg (Cr or Dr) for that account at the voucher-level.

This module exposes the side-specific extraction so SI / PI handlers
don't duplicate logic.
"""

from __future__ import annotations

from typing import Any

OUTPUT_VAT_PREFIXES = ("3331", "33311", "33312", "33313")
INPUT_VAT_PREFIXES = ("1331", "13311", "13312")


def extract_vat_account(
    voucher_legs: list[dict[str, Any]],
    side: str = "output",
) -> str | None:
    """Find the VAT account string from NKC legs for either side.

    Args:
      voucher_legs: list of leg dicts with 'account', 'debit', 'credit' keys.
      side: 'output' (Cr 3331*) for sales, 'input' (Dr 1331*) for purchases.

    Returns:
      First matching Misa TK string (e.g. '33311', '1331') or None.
    """
    if side == "output":
        prefixes = OUTPUT_VAT_PREFIXES
        amount_field = "credit"
    elif side == "input":
        prefixes = INPUT_VAT_PREFIXES
        amount_field = "debit"
    else:
        raise ValueError(f"side must be 'input' or 'output', got {side!r}")

    for leg in voucher_legs:
        acct = (leg.get("account") or "").strip()
        amt = leg.get(amount_field) or 0.0
        if amt > 0 and any(acct.startswith(p) for p in prefixes):
            return acct
    return None


def compute_total_vat(
    line_items: list[dict[str, Any]],
) -> dict[float, float]:
    """Sum tax_amount per tax_rate across line items.

    Returns {tax_rate_pct: total_tax_amount_vnd}. Useful for building one
    'On Net Total' Taxes child row per rate group.
    """
    out: dict[float, float] = {}
    for li in line_items:
        rate = float(li.get("tax_rate") or 0.0)
        amt = float(li.get("tax_amount") or 0.0)
        out[rate] = out.get(rate, 0.0) + amt
    return out


def build_tax_rows(
    line_items: list[dict[str, Any]],
    vat_account: str | None,
    skip_zero: bool = True,
) -> list[dict[str, Any]]:
    """Build ERPNext SI/PI Taxes child rows grouped by tax_rate.

    Args:
      line_items: bảng kê line items, each with 'tax_rate' (pct) + 'tax_amount'.
      vat_account: pre-resolved ERPNext Account.name (e.g. 'Output VAT - DC').
      skip_zero: if True (default), drop 0% rate rows. ERPNext convention.

    Returns:
      list of dict ready to append to doc.taxes — empty if no vat_account or
      no positive-rate lines.
    """
    if not vat_account:
        return []
    totals = compute_total_vat(line_items)
    rows: list[dict[str, Any]] = []
    # Preserve first-seen rate order from line_items
    seen: list[float] = []
    for li in line_items:
        rate = float(li.get("tax_rate") or 0.0)
        if rate in seen:
            continue
        seen.append(rate)
        if skip_zero and rate == 0.0:
            continue
        tax_amount_total = totals.get(rate, 0.0)
        if tax_amount_total <= 0:
            continue
        rows.append({
            "charge_type": "On Net Total",
            "account_head": vat_account,
            "description": f"VAT {rate:g}%",
            "rate": rate,
            "included_in_print_rate": 0,
        })
    return rows
