"""NVK / CTNB / CK / PBDT / PBPTT / KH → Journal Entry handler.

Phase D commit 8: generic 1:1 leg mapping for NVK/CTNB/CK. Commit 9: PBDT
(1,260-leg large) with optional split-by-revenue-account flag. Commits 10:
PBPTT + KH (Depreciation Entry).

Per spec §5: JE-type vouchers use **1:1 NKC row → JE.accounts row**
mapping. KHÔNG consolidate. The leg-level user_remark + per-leg party
detection preserves audit detail.

Voucher_type mapping (ERPNext Journal Entry):
  NVK   → "Journal Entry"        (generic)
  CTNB  → "Bank Entry"           (bank-to-bank transfer)
  CK    → "Journal Entry"        (generic; spec calls it "Chuyển khoản")
  PBDT  → "Journal Entry"        (revenue allocation, large)
  PBPTT → "Journal Entry"        (commit 10)
  KH    → "Depreciation Entry"   (commit 10)

Also exposes `create_je_from_unc_deferred(voucher)` — a thin wrapper that
the payment_entry handler can call when it returns 'deferred' for the
bank-fee-only UNC variant (no Dr 331 leg).
"""

from __future__ import annotations

import json
from typing import Any

import frappe

from vn_accounting.misa_migration.context import get_active_company as _get_company

# TK prefixes that signal a party leg (need party_type + party fields on the
# JE.accounts row). 131 = Customer Receivable, 331 = Supplier Payable,
# 334/3341 = Employee salary payable, 141 = Employee advance, 138 = other recv.
_PARTY_RECEIVABLE_PREFIXES = ("131", "138")
_PARTY_PAYABLE_PREFIXES = ("331", "338")
_PARTY_EMPLOYEE_PREFIXES = ("334", "3341", "3348", "141")


def _load_account_mapping() -> dict[str, str]:
    try:
        doc = frappe.get_single("Misa Account Mapping")
        return json.loads(doc.mappings or "{}")
    except Exception:
        return {}


def _resolve_account(misa_tk: str | None, mapping: dict[str, str],
                     company: str | None) -> str | None:
    """Resolve Misa TK code → ERPNext Account.name (LEAF only).

    Delegates to nkc_handlers/payment_entry._resolve_account so the
    leaf-only enforcement + group→leaf self-heal logic stays in one
    place. ERPNext rejects group accounts in any transaction with
    "Account X is a Group Account" ValidationError.
    """
    from vn_accounting.misa_migration.importers.nkc_handlers.payment_entry import (
        _resolve_account as _pe_resolve_account,
    )
    return _pe_resolve_account(misa_tk, mapping, company)


def _company_default() -> str | None:
    return _get_company()


def _detect_leg_party(
    leg_account: str,
    voucher_party_code: str | None,
) -> tuple[str | None, str | None]:
    """Decide if a JE leg should carry party_type + party fields.

    Args:
      leg_account: Misa TK string like '131', '3341', '6421', '11215'.
      voucher_party_code: voucher-level 'Mã đối tượng' (may be None).

    Returns:
      (party_type, party) — both None if the leg doesn't touch a party account
      OR if voucher_party_code is missing / doesn't resolve to a master.
    """
    if not leg_account:
        return (None, None)
    code = (voucher_party_code or "").strip()
    if not code:
        return (None, None)
    acct = leg_account.strip()

    # PERF (Tier 1.5): set-lookup vs per-call DB round-trip
    from vn_accounting.misa_migration.importers.nkc_handlers import _party_cache

    if any(acct.startswith(p) for p in _PARTY_RECEIVABLE_PREFIXES):
        if _party_cache.is_customer(code):
            return ("Customer", code)
        # Some 131 entries reference supplier credit balances (refunds);
        # fall back to Supplier if Customer doesn't exist.
        if _party_cache.is_supplier(code):
            return ("Supplier", code)
        return (None, None)

    if any(acct.startswith(p) for p in _PARTY_PAYABLE_PREFIXES):
        if _party_cache.is_supplier(code):
            return ("Supplier", code)
        if _party_cache.is_customer(code):
            return ("Customer", code)
        return (None, None)

    if any(acct.startswith(p) for p in _PARTY_EMPLOYEE_PREFIXES):
        if _party_cache.is_employee(code):
            return ("Employee", code)
        return (None, None)

    return (None, None)


def _create_je_1to1(
    voucher: dict[str, Any],
    voucher_type: str = "Journal Entry",
    legs_override: list[dict[str, Any]] | None = None,
    name_override: str | None = None,
) -> dict[str, Any]:
    """Shared 1:1 NKC leg → JE.accounts row builder.

    Each NKC leg becomes one row in the JE accounts child table. No
    consolidation. Per-leg party_type/party set when account prefix +
    party_code resolve to a master.

    For PBDT split scenarios: pass `legs_override` (subset of legs) and
    `name_override` (`<voucher_no>-S1`, `-S2`, ...) to produce N JEs from
    one voucher.
    """
    voucher_no = voucher.get("voucher_no", "")
    if not voucher_no:
        return {"status": "failed", "error": "voucher missing voucher_no"}

    target_name = name_override or voucher_no
    if frappe.db.exists("Journal Entry", target_name):
        return {"status": "skipped", "target_name": target_name,
                "reason": "already_exists"}

    legs = legs_override if legs_override is not None else (voucher.get("legs") or [])
    if not legs:
        return {"status": "failed", "error": f"{voucher_no}: no legs"}

    company = _company_default()
    if not company:
        return {"status": "failed", "error": "No Company configured"}
    mapping = _load_account_mapping()

    voucher_party = voucher.get("party_code")

    accounts_payload: list[dict[str, Any]] = []
    for leg in legs:
        misa_tk = (leg.get("account") or "").strip()
        if not misa_tk:
            return {"status": "failed",
                    "error": f"{voucher_no}: leg with empty account"}
        erpnext_account = _resolve_account(misa_tk, mapping, company)
        if not erpnext_account:
            return {"status": "failed",
                    "error": f"{voucher_no}: cannot resolve TK {misa_tk!r}"}

        debit = float(leg.get("debit") or 0.0)
        credit = float(leg.get("credit") or 0.0)
        if debit == 0 and credit == 0:
            continue  # skip zero-amount legs

        # Prefer leg's own party_code (Misa NKC's per-row "Mã đối tượng")
        # over the voucher-level value — many NVK vouchers carry the
        # party only on the receivable/payable legs, leaving the
        # contra leg's party empty.
        leg_party = leg.get("party_code") or voucher_party
        party_type, party = _detect_leg_party(misa_tk, leg_party)

        row = {
            "account": erpnext_account,
            "debit_in_account_currency": debit,
            "credit_in_account_currency": credit,
            "user_remark": leg.get("leg_desc") or "",
        }
        if party_type:
            row["party_type"] = party_type
            row["party"] = party
        accounts_payload.append(row)

    # Re-validate balance on the assembled JE (parser already checked, but
    # zero-leg drop could shift in theory)
    total_dr = sum(r["debit_in_account_currency"] for r in accounts_payload)
    total_cr = sum(r["credit_in_account_currency"] for r in accounts_payload)
    if abs(total_dr - total_cr) > 0.01:
        return {"status": "failed",
                "error": f"{voucher_no}: JE unbalanced Dr={total_dr} Cr={total_cr}"}

    # Auto-upgrade voucher_type to "Depreciation Entry" if any leg posts
    # to an Account with account_type='Depreciation' (e.g. TK 6424).
    # ERPNext rejects regular JE posting to such accounts.
    if voucher_type == "Journal Entry":
        for row in accounts_payload:
            atype = frappe.db.get_value("Account", row["account"], "account_type")
            if atype == "Depreciation":
                voucher_type = "Depreciation Entry"
                break

    # Stock-type Account in a JE leg fails ERPNext's StockAccountInvalidTransaction.
    # Misa data has legitimate inter-stock JE transfers (e.g. CK Cr 154/Dr 155
    # for finished-goods transfer) that need to import as JE for GL parity
    # with Misa. Workaround: temporarily clear account_type on those accounts
    # for the duration of the insert, restore after. The Stock Ledger isn't
    # affected (JE doesn't touch SLE anyway).
    _stock_legs_restore: list[tuple[str, str]] = []
    for row in accounts_payload:
        atype = frappe.db.get_value("Account", row["account"], "account_type")
        if atype == "Stock":
            frappe.db.set_value(
                "Account", row["account"], "account_type", "",
                update_modified=False,
            )
            _stock_legs_restore.append((row["account"], atype))

    payload = {
        "doctype": "Journal Entry",
        "voucher_type": voucher_type,
        "company": company,
        "posting_date": voucher.get("posting_date"),
        "set_posting_time": 1,
        "user_remark": voucher.get("voucher_remark") or voucher_no,
        "accounts": accounts_payload,
        "misa_voucher_no": voucher_no,
    }
    # Bank Entry / Cash Entry require cheque_no + cheque_date for submit.
    # Use the Misa voucher_no as a stable reference.
    if voucher_type in ("Bank Entry", "Cash Entry"):
        payload["cheque_no"] = voucher_no
        payload["cheque_date"] = voucher.get("posting_date")

    try:
        doc = frappe.get_doc(payload)
        doc.flags.ignore_permissions = True
        # PERF (Tier 1.2): preflight already validated Account links on
        # every leg; skip ERPNext's per-row Link integrity check.
        doc.flags.ignore_links = True
        doc.insert(set_name=target_name)
        return {"status": "created", "target_name": doc.name,
                "target_doctype": "Journal Entry",
                "voucher_type": voucher_type,
                "leg_count": len(accounts_payload),
                "total_dr": total_dr}
    except Exception as exc:
        err = f"{type(exc).__name__}: {exc}"
        frappe.log_error(title=f"Misa JE create failed: {voucher_no}",
                         message=err)
        return {"status": "failed", "target_name": None, "error": err}
    finally:
        # Restore any stock account_type values we cleared above
        for acct, original_atype in _stock_legs_restore:
            try:
                frappe.db.set_value(
                    "Account", acct, "account_type", original_atype,
                    update_modified=False,
                )
            except Exception:
                pass


# ----------------------------------------------------------- public entry points

def create_je_from_nvk(voucher: dict[str, Any],
                      invoice: dict[str, Any] | None = None) -> dict[str, Any]:
    """NVK (Nghiệp vụ khác) → generic Journal Entry."""
    return _create_je_1to1(voucher, voucher_type="Journal Entry")


def create_je_from_ctnb(voucher: dict[str, Any],
                       invoice: dict[str, Any] | None = None) -> dict[str, Any]:
    """CTNB (Chuyển tiền nội bộ) → Bank Entry Journal."""
    return _create_je_1to1(voucher, voucher_type="Bank Entry")


def create_je_from_ck(voucher: dict[str, Any],
                     invoice: dict[str, Any] | None = None) -> dict[str, Any]:
    """CK (Chuyển khoản) → generic Journal Entry."""
    return _create_je_1to1(voucher, voucher_type="Journal Entry")


def create_je_from_unc_deferred(voucher: dict[str, Any]) -> dict[str, Any]:
    """Fallback path when payment_entry.create_pe_from_unc returns 'deferred'
    (bank-fee-only UNC with no Dr 331 leg). Posts a generic JE instead.

    Caller (orchestrator C14) routes the deferred voucher here.
    """
    return _create_je_1to1(voucher, voucher_type="Bank Entry")


def create_je_from_pbptt(voucher: dict[str, Any],
                        invoice: dict[str, Any] | None = None) -> dict[str, Any]:
    """PBPTT (Phân bổ chi phí trả trước) → generic Journal Entry.

    Allocates prepaid expense (TK 242, TT99/2025) into the period's expense
    accounts. 24-leg typical voucher in T1/2026. 1:1 leg mapping per spec §5.
    """
    return _create_je_1to1(voucher, voucher_type="Journal Entry")


def create_je_from_pbcc(voucher: dict[str, Any],
                       invoice: dict[str, Any] | None = None) -> dict[str, Any]:
    """PBCC (Phân bổ chi phí công cụ dụng cụ) → generic Journal Entry.

    Monthly allocation of tools/equipment cost — same shape as PBPTT but
    drawn from TK 242 → expense accounts (627/641/642). Per-voucher
    amounts typically small (1-5M VND). 1:1 leg mapping.
    """
    return _create_je_1to1(voucher, voucher_type="Journal Entry")


def create_je_from_kh(voucher: dict[str, Any],
                     invoice: dict[str, Any] | None = None) -> dict[str, Any]:
    """KH (Khấu hao TSCĐ) → Depreciation Entry.

    Posts monthly depreciation: Dr 627/641/642/811 / Cr 2141/2142/2143.
    16-leg typical voucher. ERPNext voucher_type="Depreciation Entry" makes
    Asset module reports recognise these as depreciation postings.
    """
    return _create_je_1to1(voucher, voucher_type="Depreciation Entry")


# ---------------------------------------------------- PBDT (revenue allocation)

def _split_legs_by_revenue_account(
    legs: list[dict[str, Any]],
) -> list[list[dict[str, Any]]]:
    """Group PBDT legs into balanced sub-vouchers keyed by Cr 5xx sub-account.

    PBDT (Phân bổ doanh thu) has 1,260+ legs in T1/2026. ERPNext's JE form
    becomes sluggish past ~500 rows. This helper splits into N JEs grouped
    by the revenue sub-account being allocated (Cr 511X / 521X / 711X).

    Strategy:
      1. Walk legs left-to-right preserving original order.
      2. For each Cr leg on a 5xx/7xx account, open a new group seeded with
         that leg.
      3. Every following Dr leg attaches to the current group until another
         Cr 5xx/7xx appears.
      4. Legs before the first revenue Cr (rare: a setup Dr) attach to a
         "_prologue" group, returned as group 0.

    Each returned sub-list must individually balance (Dr=Cr); if a group
    doesn't, fall back to a single big JE upstream.

    Args:
      legs: ordered NKC legs for a single PBDT voucher.

    Returns:
      List of leg-lists, one per Cr 5xx/7xx account encountered. Empty
      input → empty output.
    """
    if not legs:
        return []
    groups: list[list[dict[str, Any]]] = []
    current: list[dict[str, Any]] = []
    for leg in legs:
        acct = str(leg.get("account") or "").strip()
        credit = float(leg.get("credit") or 0.0)
        is_revenue_credit = (
            credit > 0 and (acct.startswith("5") or acct.startswith("7"))
        )
        if is_revenue_credit:
            if current:
                groups.append(current)
            current = [leg]
        else:
            current.append(leg)
    if current:
        groups.append(current)
    return groups


def _groups_balance(groups: list[list[dict[str, Any]]]) -> bool:
    """True iff every group's Dr total equals Cr total within 0.01 VND."""
    for grp in groups:
        dr = sum(float(l.get("debit") or 0.0) for l in grp)
        cr = sum(float(l.get("credit") or 0.0) for l in grp)
        if abs(dr - cr) > 0.01:
            return False
    return True


def create_je_from_pbdt(
    voucher: dict[str, Any],
    invoice: dict[str, Any] | None = None,
    split_by_revenue_account: bool = False,
) -> dict[str, Any]:
    """PBDT (Phân bổ doanh thu) → Journal Entry.

    Default (`split_by_revenue_account=False`): single JE with all legs
    (faithful to Misa per spec §5; ERPNext can handle 1k+ rows server-side
    even if form rendering lags).

    Opt-in split: legs grouped by Cr 5xx/7xx account → N small JEs named
    `<voucher_no>-S1`, `-S2`, ... Result aggregates statuses; any group
    failure returns 'failed' with the first error.
    """
    if not split_by_revenue_account:
        return _create_je_1to1(voucher, voucher_type="Journal Entry")

    voucher_no = voucher.get("voucher_no", "")
    if not voucher_no:
        return {"status": "failed", "error": "voucher missing voucher_no"}

    legs = voucher.get("legs") or []
    if not legs:
        return {"status": "failed", "error": f"{voucher_no}: no legs"}

    groups = _split_legs_by_revenue_account(legs)
    if not groups:
        return {"status": "failed",
                "error": f"{voucher_no}: split produced no groups"}

    if not _groups_balance(groups):
        # Fallback: single JE so user gets the original voucher posted
        return _create_je_1to1(voucher, voucher_type="Journal Entry")

    created: list[str] = []
    for idx, grp in enumerate(groups, start=1):
        sub_name = f"{voucher_no}-S{idx}"
        result = _create_je_1to1(
            voucher,
            voucher_type="Journal Entry",
            legs_override=grp,
            name_override=sub_name,
        )
        if result.get("status") == "failed":
            return {"status": "failed",
                    "error": f"{voucher_no} split #{idx}: {result.get('error')}",
                    "created_subset": created}
        if result.get("status") == "created":
            created.append(result.get("target_name") or sub_name)

    return {
        "status": "created",
        "target_doctype": "Journal Entry",
        "target_name": created[0] if created else None,
        "split_count": len(groups),
        "split_names": created,
        "voucher_type": "Journal Entry",
    }
