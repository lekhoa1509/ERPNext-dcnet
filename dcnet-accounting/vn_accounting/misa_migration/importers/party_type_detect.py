"""Party type auto-detection from Misa NKC accounts (spec §6.1).

Pure functions — no DB access. Used by Phase D (Voucher) processor to
classify a Misa party_code as Customer / Supplier / Employee / ambiguous
based on which TK accounts appear with that party code across voucher rows.

Rules (in priority order):
  1. Both 131* AND 331*       → ambiguous (most common — same party appears
                                 as both customer + supplier in same period)
  2. Only 131*                → Customer
  3. Only 331*                → Supplier
  4. 334*/141*                → Employee
  5. 138* (no 131)            → Customer (other receivables)
  6. 338* (no 331)            → Supplier (other payables)
  7. Neither                  → ambiguous (caller flags for review)
"""

from __future__ import annotations

from typing import Iterable


def classify_accounts(account_codes: Iterable[str]) -> str:
    """Classify a party as Customer / Supplier / Employee / ambiguous.

    Args:
        account_codes: iterable of Misa TK strings (e.g. ['131', '5111']).

    Returns: 'Customer' / 'Supplier' / 'Employee' / 'ambiguous'.
    """
    accs = [str(a or "").strip() for a in account_codes]
    accs = [a for a in accs if a]

    has_131 = any(a.startswith("131") for a in accs)
    has_331 = any(a.startswith("331") for a in accs)
    has_334 = any(a.startswith("334") or a.startswith("141") for a in accs)
    has_138 = any(a.startswith("138") for a in accs)
    has_338 = any(a.startswith("338") for a in accs)

    if has_131 and has_331:
        return "ambiguous"
    if has_131:
        return "Customer"
    if has_331:
        return "Supplier"
    if has_334:
        return "Employee"
    if has_138:
        return "Customer"
    if has_338:
        return "Supplier"
    return "ambiguous"


def detect_for_voucher(misa_party_code: str, voucher_rows: list[dict]) -> str:
    """Convenience: given a list of NKC row dicts (each {'account', 'party_code', ...}),
    return classification for a specific party_code.
    """
    if not misa_party_code:
        return "ambiguous"
    accs = [r.get("account") for r in voucher_rows if r.get("party_code") == misa_party_code]
    return classify_accounts(accs)
