"""Bảng cân đối số phát sinh (BCDPS) — VAS-labeled wrapper around ERPNext
Trial Balance.

ERPNext's Trial Balance report exposes period movement columns labeled
"Debit"/"Credit". Vietnamese translation renders them as "Ghi nợ"/"Ghi có"
which sounds like account-side labels (balance direction). Users then ask
"why do many accounts have BOTH Ghi nợ and Ghi có populated?" — confused
because PERIOD MOVEMENTS naturally have both directions for any active
account (cash in + cash out, AR invoice + payment).

This wrapper invokes the same underlying logic but re-labels columns to
match VAS / Misa convention:

  Đầu kỳ (Nợ)    → Dư đầu kỳ Nợ
  Mở đầu (Cr)    → Dư đầu kỳ Có
  Ghi nợ         → Phát sinh Nợ
  Ghi có         → Phát sinh Có
  Kết thúc (Dr)  → Dư cuối kỳ Nợ
  Kết thúc (Cr)  → Dư cuối kỳ Có

Identical column structure + same filter set; no logic divergence.
"""
from erpnext.accounts.report.trial_balance.trial_balance import (
    execute as _trial_balance_execute,
)


_VAS_LABEL_MAP = {
    "opening_debit":  "Dư đầu kỳ Nợ",
    "opening_credit": "Dư đầu kỳ Có",
    "debit":          "Phát sinh Nợ",
    "credit":         "Phát sinh Có",
    "closing_debit":  "Dư cuối kỳ Nợ",
    "closing_credit": "Dư cuối kỳ Có",
}


def execute(filters=None):
    result = _trial_balance_execute(filters)
    # ERPNext execute returns (columns, data) or (columns, data, message, chart)
    columns = result[0] if isinstance(result, tuple) else result
    rest = result[1:] if isinstance(result, tuple) else ()

    for col in columns:
        if isinstance(col, dict) and col.get("fieldname") in _VAS_LABEL_MAP:
            col["label"] = _VAS_LABEL_MAP[col["fieldname"]]

    return (columns,) + rest if rest else (columns, [])
