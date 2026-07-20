"""Opening Prepaid Expense (TK 242) row-builder.

Phase E commit 13e. Per spec: TK 242 "Chi phí trả trước" / "Chi phí chờ
phân bổ" balance is brought forward by emitting Dr 242 lines in the
Opening Entry JE. The remaining amortization schedule (remaining_periods
× per_period_amount) is handled by ERPNext's Process Deferred Expense
feature OR vn_accounting's deferred-expense scheduler — that's runtime
behavior after opening, not Phase 0 scope.

This handler does NOT create its own doc; it produces a list of
JE.accounts row dicts that get appended to the Opening Entry JE by the
Phase 0 orchestrator (E13f).

Row builder output per prepaid line:
  {
    account: <resolved holding_account, default TK 242>,
    debit_in_account_currency: <remaining_amount>,
    credit_in_account_currency: 0,
    user_remark: "OB Prepaid <prepaid_code> — <name>",
  }

The matching credit lands in the Opening JE's natural Dr=Cr balance
(other rows include Cr Retained Earnings / Cr Supplier 331 etc.).
If residual remains, opening_journal._temporary_opening_account picks
it up.

Skipped silently:
  - remaining_amount <= 0 (already fully amortized)
  - holding_account TK not mappable
"""

from __future__ import annotations

from typing import Any

import frappe


_DEFAULT_PREPAID_ACCOUNT = "242"  # TT99/2025 unifies prepaid into TK 242


def _resolve_account(misa_tk: str, mapping: dict[str, str],
                     company: str) -> str | None:
    """Misa TK → leaf Account.name, COMPANY-VERIFIED (see _account_lookup)."""
    from vn_accounting.misa_migration.importers.nkc_handlers._account_lookup import (
        resolve_account,
    )
    return resolve_account(misa_tk, mapping, company)


def build_prepaid_rows(
    parsed_rows: list[dict],
    company: str,
    mapping: dict[str, str] | None = None,
) -> dict[str, Any]:
    """Build JE.accounts dicts for prepaid-expense opening balance.

    Args:
      parsed_rows: output of parse_prepaid_expense().
      company: ERPNext Company.
      mapping: Misa Account Mapping dict (optional; auto-loaded if absent).

    Returns:
      {
        rows: list[JE.accounts dict],     # Dr TK 242 per prepaid line
        skipped: list[{code, reason}],
        total_dr: float,
        prepaid_count: int,
        schedule_pending: int,             # rows with remaining_periods > 0
      }
    """
    if mapping is None:
        import json
        try:
            doc = frappe.get_single("Misa Account Mapping")
            mapping = json.loads(doc.mappings or "{}")
        except Exception:
            mapping = {}

    out_rows: list[dict] = []
    skipped: list[dict] = []
    total_dr = 0.0
    schedule_pending = 0

    for r in parsed_rows:
        code = r.get("prepaid_code")
        if not code:
            skipped.append({"code": None, "reason": "missing prepaid_code"})
            continue

        remaining = float(r.get("remaining_amount") or 0.0)
        if remaining <= 0:
            # Already fully amortized; no opening balance to bring forward
            continue

        # Resolve holding account (default TK 242)
        holding_tk = (r.get("holding_account") or _DEFAULT_PREPAID_ACCOUNT).strip()
        acct_name = _resolve_account(holding_tk, mapping, company)
        if not acct_name:
            skipped.append({
                "code": code,
                "reason": f"TK {holding_tk!r} không map được sang Account",
            })
            continue

        out_rows.append({
            "account": acct_name,
            "debit_in_account_currency": remaining,
            "credit_in_account_currency": 0.0,
            "user_remark": (
                f"OB Prepaid {code} — {r.get('prepaid_name') or ''} "
                f"(còn {r.get('remaining_periods') or '?'}/"
                f"{r.get('total_periods') or '?'} kỳ)"
            )[:140],
        })
        total_dr += remaining
        if (r.get("remaining_periods") or 0) > 0:
            schedule_pending += 1

    return {
        "rows": out_rows,
        "skipped": skipped,
        "total_dr": total_dr,
        "prepaid_count": len(out_rows),
        "schedule_pending": schedule_pending,
    }
