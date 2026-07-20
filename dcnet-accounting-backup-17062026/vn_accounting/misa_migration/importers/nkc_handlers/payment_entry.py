"""BC / PT / PC / UNC → Payment Entry handler.

Phase D commit 6: simple 2-leg path covering BC + PT + PC.
Phase D commit 7: extends to UNC (multi-leg with deductions[]).

BC (Báo Có ngân hàng): Receive from Customer into Bank
   2-leg: Dr 11215 (bank) / Cr 131 (customer ledger)
   payment_type=Receive, mode_of_payment="Bank Draft"

PT (Phiếu thu tiền mặt): Receive from Customer in Cash
   2-leg: Dr 1111 (cash) / Cr 131 (or 11215 for bank→cash transfer)
   payment_type=Receive, mode_of_payment="Cash"

PC (Phiếu chi tiền mặt): Pay Supplier in Cash
   2-leg: Dr 331 (supplier ledger) / Cr 1111 (cash)
   payment_type=Pay, mode_of_payment="Cash"

UNC (Ủy nhiệm chi): Pay Supplier via Bank transfer
   2-leg: Dr 331 / Cr 11215   (simple)
   4-leg: + Dr 6427 + Dr 1331 / Cr 11215×2  (service-pay with VAT)
   6-leg: Dr 635×3 / Cr 11215×3            (bank fees / interest only)
   payment_type=Pay, mode_of_payment="Bank Draft", deductions[] for extra legs

When no resolvable party (UNC bank-fees-only case), fall back to a generic
Journal Entry instead of forcing a synthetic Customer/Supplier.
"""

from __future__ import annotations

import json
from typing import Any

import frappe

from vn_accounting.misa_migration.context import get_active_company as _get_company

# TK prefixes for routing legs
_BANK_PREFIXES = ("112", "1121", "11211", "11212", "11215", "11217", "11218")
_CASH_PREFIXES = ("111", "1111", "1112", "1113")
_RECEIVABLE_PREFIXES = ("131",)
_PAYABLE_PREFIXES = ("331",)
_EMPLOYEE_ADVANCE_PREFIXES = ("141", "334")


def _load_account_mapping() -> dict[str, str]:
    try:
        doc = frappe.get_single("Misa Account Mapping")
        return json.loads(doc.mappings or "{}")
    except Exception:
        return {}


_COST_CENTER_CACHE: dict[str, str | None] = {}


def _default_cost_center(company: str | None) -> str | None:
    """Resolve the Company's default Cost Center; cache per process.

    Some sites have accounting dimension enabled for cost_center on
    Payment Entry, which surfaces as `MandatoryError: cost_center` at
    PE.insert(). The Company default Cost Center is the safe fallback.
    """
    if not company:
        return None
    if company in _COST_CENTER_CACHE:
        return _COST_CENTER_CACHE[company]
    cc = frappe.db.get_value("Company", company, "cost_center")
    if not cc:
        cc = frappe.db.get_value(
            "Cost Center",
            {"company": company, "is_group": 0, "disabled": 0},
            "name",
        )
    _COST_CENTER_CACHE[company] = cc
    return cc


# PERF: module-level cache for Account.is_group + account_type — avoids
# a DB hit on every _resolve_account call. Pre-warmed by
# `_warm_account_cache_for_company()` at orchestrator start (or lazily
# on first miss). Eviction not needed — Account schema is read-mostly
# during migration. Cleared between batches via reset_perf_caches().
_ACCOUNT_META_CACHE: dict[str, tuple[int, str]] = {}  # name → (is_group, account_type)
_ACCOUNT_BY_NUMBER_CACHE: dict[tuple[str, str], str] = {}  # (account_number, company) → name (leaf only)


def _warm_account_cache_for_company(company: str) -> None:
    """Bulk-load Account.is_group + account_type for every account on
    company into _ACCOUNT_META_CACHE. Also pre-populate
    _ACCOUNT_BY_NUMBER_CACHE with leaf accounts so per-row lookups skip
    the DB entirely."""
    if not company:
        return
    rows = frappe.db.sql(
        """SELECT name, account_number, is_group, COALESCE(account_type, '') account_type
           FROM `tabAccount` WHERE company=%s""",
        (company,), as_dict=True,
    )
    for r in rows:
        _ACCOUNT_META_CACHE[r["name"]] = (int(r["is_group"] or 0), r["account_type"])
        if r["account_number"] and not r["is_group"]:
            _ACCOUNT_BY_NUMBER_CACHE[(r["account_number"], company)] = r["name"]


def _is_group_cached(account_name: str) -> int:
    """Returns is_group (0/1) for an Account, hitting cache first."""
    meta = _ACCOUNT_META_CACHE.get(account_name)
    if meta is not None:
        return meta[0]
    # Lazy load
    v = frappe.db.get_value("Account", account_name, "is_group")
    is_group = int(v or 0)
    _ACCOUNT_META_CACHE[account_name] = (is_group, "")
    return is_group


def reset_perf_caches() -> None:
    """Called by orchestrator between batches (or at startup) to clear
    stale per-request caches."""
    _ACCOUNT_META_CACHE.clear()
    _ACCOUNT_BY_NUMBER_CACHE.clear()
    # Tier 1.5: clear party sets too so the next warm rebuilds them
    # against the current Company.
    from vn_accounting.misa_migration.importers.nkc_handlers import _party_cache
    _party_cache.reset_party_cache()
    # Fix F: clear item-name map for fresh rebuild on next phase 4 run.
    from vn_accounting.misa_migration.importers.nkc_handlers import _item_cache
    _item_cache.reset_item_cache()


def _resolve_account(misa_tk: str | None, mapping: dict[str, str],
                     company: str | None) -> str | None:
    """Resolve Misa TK code → ERPNext Account.name (LEAF only).

    Filters is_group=0 at every layer because group accounts cannot be
    used in transactions (ERPNext rejects with `Tài khoản là Tài khoản
    nhóm` ValidationError on submit). Mapping table may carry stale
    entries from prior buggy runs that pointed leaf TK codes (11215,
    1121.81 etc.) at parent groups; verify is_group=0 on cached hits
    too, falling through to live lookup when stale.
    """
    if not misa_tk:
        return None
    misa_tk = str(misa_tk).strip()
    if not misa_tk:
        return None
    cached = mapping.get(misa_tk)
    if cached:
        # PERF: in-memory cache hit (no DB query); fall back to live
        # query only if Account not in cache.
        if _is_group_cached(cached) == 0:
            return cached
        # Stale group entry — fall through to live leaf lookup
    if company:
        # PERF: check per-(number, company) cache first
        key = (misa_tk, company)
        cached_leaf = _ACCOUNT_BY_NUMBER_CACHE.get(key)
        if cached_leaf:
            mapping[misa_tk] = cached_leaf
            return cached_leaf
        # Lazy fallback to DB
        live = frappe.db.get_value(
            "Account",
            {"account_number": misa_tk, "company": company, "is_group": 0},
            "name",
        )
        if live:
            mapping[misa_tk] = live
            _ACCOUNT_BY_NUMBER_CACHE[key] = live
            return live
        # Group-to-leaf self-heal: Misa references TK '8211' but our COA
        # has 8211 as a group (children 82111, 82112). Find the group and
        # descend to its first leaf descendant. Same shape as the company_
        # defaults self-heal in setup/company_defaults.py.
        group = frappe.db.get_value(
            "Account",
            {"account_number": misa_tk, "company": company, "is_group": 1},
            ["name", "lft", "rgt"], as_dict=True,
        )
        if group and group.get("lft") is not None and group.get("rgt") is not None:
            leaf = frappe.db.sql(
                """SELECT name FROM `tabAccount`
                   WHERE company=%s AND lft > %s AND rgt < %s AND is_group=0
                   ORDER BY account_number ASC LIMIT 1""",
                (company, group["lft"], group["rgt"]),
            )
            if leaf:
                leaf_name = leaf[0][0]
                mapping[misa_tk] = leaf_name
                _ACCOUNT_BY_NUMBER_CACHE[key] = leaf_name
                return leaf_name
    return None


def _find_leg_by_prefix(
    legs: list[dict[str, Any]],
    prefixes: tuple[str, ...],
    side: str,  # 'debit' or 'credit'
) -> dict[str, Any] | None:
    """Return first leg with positive amount on `side` and account matching any prefix."""
    for leg in legs:
        amt = leg.get(side) or 0.0
        acct = (leg.get("account") or "").strip()
        if amt > 0 and any(acct.startswith(p) for p in prefixes):
            return leg
    return None


def _detect_party_type(party_code: str) -> str | None:
    """Return 'Customer' if party_code exists as Customer, 'Supplier' if Supplier,
    'Employee' if Employee. None if absent in all three masters."""
    if not party_code:
        return None
    # PERF (Tier 1.5): set-lookup vs three per-call DB round-trips
    from vn_accounting.misa_migration.importers.nkc_handlers import _party_cache
    if _party_cache.is_customer(party_code):
        return "Customer"
    if _party_cache.is_supplier(party_code):
        return "Supplier"
    if _party_cache.is_employee(party_code):
        return "Employee"
    return None


def _company_default() -> str | None:
    return _get_company()


# ----------------------------------------------------------- PE → SI/PI linking

def _resolve_pe_references(
    party_type: str,
    party: str,
    amount: float,
    company: str,
    posting_date,
) -> list[dict]:
    """Return a list of `pe.references` rows linking this PE to open
    invoices on the same party (FIFO by posting_date asc).

    Returns empty list if party has no open invoice yet OR amount is 0.
    The handler creating the PE attaches this list to its payload so
    the PE submit reduces invoice outstanding_amount in the same call.

    Used by all PE-creating handlers (BC/PT/PC/UNC). For "PE before SI"
    cases (advance payment before invoice issued), the resolver returns
    empty and the orchestrator's post-pass backfill will re-link once
    the corresponding SI/PI is created later in the loop.
    """
    if not party_type or not party or amount <= 0 or not company:
        return []
    target_dt = "Sales Invoice" if party_type == "Customer" else (
        "Purchase Invoice" if party_type == "Supplier" else None
    )
    if not target_dt:
        return []
    party_field = "customer" if target_dt == "Sales Invoice" else "supplier"
    # Open invoices on this party, oldest first; only ones with positive
    # outstanding (already-fully-allocated ones can't take more).
    invoices = frappe.db.sql(
        f"""SELECT name, posting_date, grand_total, outstanding_amount
            FROM `tab{target_dt}`
            WHERE company=%s AND docstatus=1 AND {party_field}=%s
              AND outstanding_amount > 0
            ORDER BY posting_date ASC""",
        (company, party),
        as_dict=True,
    )
    references: list[dict] = []
    remaining = float(amount)
    for inv in invoices:
        if remaining <= 0:
            break
        avail = float(inv["outstanding_amount"] or 0)
        if avail <= 0:
            continue
        take = min(avail, remaining)
        references.append({
            "reference_doctype": target_dt,
            "reference_name": inv["name"],
            "allocated_amount": take,
        })
        remaining -= take
    return references


# ----------------------------------------------------------- simple 2-leg PE

def _create_simple_pe(
    voucher: dict[str, Any],
    voucher_no: str,
    payment_type: str,      # 'Receive' or 'Pay'
    mode_of_payment: str,   # 'Bank Draft' or 'Cash'
    paid_account_side: str, # 'debit' (for Receive: bank/cash side) or 'credit' (for Pay)
    paid_account_prefixes: tuple[str, ...],  # bank/cash prefixes
    party_account_side: str,  # opposite of paid_account_side
    party_account_prefixes: tuple[str, ...],
    expected_party_type: str | None,  # 'Customer' / 'Supplier'
) -> dict[str, Any]:
    if frappe.db.exists("Payment Entry", voucher_no):
        return {"status": "skipped", "target_name": voucher_no,
                "reason": "already_exists"}

    legs = voucher.get("legs") or []
    if not legs:
        return {"status": "failed",
                "error": f"voucher {voucher_no} has no legs"}

    company = _company_default()
    if not company:
        return {"status": "failed", "error": "No Company configured"}
    mapping = _load_account_mapping()

    paid_leg = _find_leg_by_prefix(legs, paid_account_prefixes, paid_account_side)
    if not paid_leg:
        # Non-standard PE shape (e.g. PC paying loan principal D341 Cr112,
        # BC receiving non-AR cash). Defer to JE handler.
        return {"status": "deferred",
                "error": f"{voucher_no}: cannot find {paid_account_side} leg with prefix {paid_account_prefixes}",
                "voucher_kind": "je_fallback"}

    party_leg = _find_leg_by_prefix(legs, party_account_prefixes, party_account_side)
    if not party_leg:
        return {"status": "deferred",
                "error": f"{voucher_no}: cannot find {party_account_side} leg with prefix {party_account_prefixes}",
                "voucher_kind": "je_fallback"}

    paid_account = _resolve_account(paid_leg["account"], mapping, company)
    party_account = _resolve_account(party_leg["account"], mapping, company)
    if not paid_account or not party_account:
        return {"status": "failed",
                "error": f"{voucher_no}: account mapping incomplete (paid={paid_account}, party={party_account})"}

    # Internal Transfer detection: if the "party leg" resolved to a Bank or
    # Cash account (no AR/AP involvement), this is a Bank↔Cash transfer, not
    # a customer/supplier payment. PT with `party_account_prefixes` widened
    # to BANK + RECEIVABLE picks this up; here we re-classify.
    party_leg_account_type = frappe.db.get_value(
        "Account", party_account, "account_type"
    )
    is_internal_transfer = party_leg_account_type in ("Bank", "Cash")

    party_code = voucher.get("party_code") or ""
    party_type = _detect_party_type(party_code) if party_code else None
    if is_internal_transfer:
        # No party for internal transfers
        party_type = None
        party_code = ""
    elif expected_party_type and party_type != expected_party_type:
        # Fallback: try expected_party_type anyway if record exists, else None
        if party_code and frappe.db.exists(expected_party_type, party_code):
            party_type = expected_party_type
        else:
            return {"status": "failed",
                    "error": f"{voucher_no}: party_code {party_code!r} not found as {expected_party_type}"}

    amount = float(paid_leg.get(paid_account_side) or 0.0)
    if amount <= 0:
        return {"status": "failed", "error": f"{voucher_no}: paid amount is 0"}

    if not frappe.db.exists("Mode of Payment", mode_of_payment):
        # Frappe ships these by default; if missing, skip and create later
        mode_of_payment = None

    effective_payment_type = "Internal Transfer" if is_internal_transfer else payment_type

    payload: dict[str, Any] = {
        "doctype": "Payment Entry",
        "company": company,
        "posting_date": voucher.get("posting_date"),
        "set_posting_time": 1,
        "payment_type": effective_payment_type,
        "mode_of_payment": mode_of_payment,
        "party_type": party_type,
        "party": party_code or None,
        "remarks": voucher.get("voucher_remark") or voucher_no,
        "misa_voucher_no": voucher_no,
        # Bank Payment Entries require reference_no / reference_date.
        # Use Misa voucher_no + posting_date as canonical reference.
        "reference_no": voucher_no,
        "reference_date": voucher.get("posting_date"),
        "cost_center": _default_cost_center(company),
    }

    if effective_payment_type == "Internal Transfer":
        # Bank/Cash → Bank/Cash. The "paid leg" side determines which is
        # source vs destination:
        #   paid_account_side='debit'  → paid_account = destination (Dr cash/bank)
        #   paid_account_side='credit' → paid_account = source (Cr cash/bank)
        if paid_account_side == "debit":
            payload.update({
                "paid_from": party_account,
                "paid_from_account_currency": "VND",
                "paid_amount": amount,
                "paid_to": paid_account,
                "paid_to_account_currency": "VND",
                "received_amount": amount,
            })
        else:
            payload.update({
                "paid_from": paid_account,
                "paid_from_account_currency": "VND",
                "paid_amount": amount,
                "paid_to": party_account,
                "paid_to_account_currency": "VND",
                "received_amount": amount,
            })
    elif payment_type == "Receive":
        payload.update({
            "paid_to": paid_account,
            "paid_to_account_currency": "VND",
            "received_amount": amount,
            "paid_from": party_account,
            "paid_from_account_currency": "VND",
            "paid_amount": amount,
        })
    else:  # Pay
        payload.update({
            "paid_from": paid_account,
            "paid_from_account_currency": "VND",
            "paid_amount": amount,
            "paid_to": party_account,
            "paid_to_account_currency": "VND",
            "received_amount": amount,
        })

    # Attach references → open SI/PI on same party (FIFO oldest-first).
    # Skipped for Internal Transfers (no party) and for vouchers whose
    # party has no open invoice yet (advance payment case — orchestrator
    # post-pass backfill catches those after all SIs/PIs created).
    # ALSO skipped when party_account is an employee-payable (334*) or
    # employee-advance (141*) account — salary payments don't reference PIs.
    party_acct_raw = (party_leg.get("account") or "").strip()
    is_employee_payable = (
        party_acct_raw.startswith("334") or party_acct_raw.startswith("141")
    )
    if not is_internal_transfer and party_type in ("Customer", "Supplier") \
            and not is_employee_payable:
        refs = _resolve_pe_references(
            party_type=party_type, party=party_code, amount=amount,
            company=company, posting_date=voucher.get("posting_date"),
        )
        if refs:
            payload["references"] = refs

    try:
        doc = frappe.get_doc(payload)
        doc.flags.ignore_permissions = True
        # PERF (Tier 1.2): preflight already validated Party / Account links;
        # skip ERPNext's per-row Link integrity check.
        doc.flags.ignore_links = True
        doc.insert(set_name=voucher_no)
        return {"status": "created", "target_name": doc.name,
                "target_doctype": "Payment Entry",
                "payment_type": payment_type,
                "amount": amount}
    except Exception as exc:
        err = f"{type(exc).__name__}: {exc}"
        frappe.log_error(title=f"Misa PE create failed: {voucher_no}",
                         message=err)
        return {"status": "failed", "target_name": None, "error": err}


# ----------------------------------------------------------- public entry points

def create_pe_from_bc(voucher: dict[str, Any],
                     invoice: dict[str, Any] | None = None) -> dict[str, Any]:
    """BC (Báo Có ngân hàng) → Receive payment to Bank."""
    voucher_no = voucher.get("voucher_no", "")
    if not voucher_no:
        return {"status": "failed", "error": "voucher missing voucher_no"}
    return _create_simple_pe(
        voucher, voucher_no,
        payment_type="Receive",
        mode_of_payment="Bank Draft",
        paid_account_side="debit",
        paid_account_prefixes=_BANK_PREFIXES,
        party_account_side="credit",
        party_account_prefixes=_RECEIVABLE_PREFIXES,
        expected_party_type="Customer",
    )


def create_pe_from_pt(voucher: dict[str, Any],
                     invoice: dict[str, Any] | None = None) -> dict[str, Any]:
    """PT (Phiếu thu tiền mặt) → Receive payment in Cash.

    Edge case: PT often represents internal cash withdrawal from bank
    (Dr 1111 / Cr 11215, party=own company). In that case there's no
    Customer/Supplier — handler returns 'failed' and caller can route
    to a JE instead. v1 best-effort: only create PE when party resolves
    as Customer.
    """
    voucher_no = voucher.get("voucher_no", "")
    if not voucher_no:
        return {"status": "failed", "error": "voucher missing voucher_no"}
    # PT Cr leg can be 131 (customer) or 11215 (bank, internal transfer)
    return _create_simple_pe(
        voucher, voucher_no,
        payment_type="Receive",
        mode_of_payment="Cash",
        paid_account_side="debit",
        paid_account_prefixes=_CASH_PREFIXES,
        party_account_side="credit",
        party_account_prefixes=_RECEIVABLE_PREFIXES + _BANK_PREFIXES,
        expected_party_type="Customer",
    )


def create_pe_from_pc(voucher: dict[str, Any],
                     invoice: dict[str, Any] | None = None) -> dict[str, Any]:
    """PC (Phiếu chi tiền mặt) → Pay Supplier in Cash."""
    voucher_no = voucher.get("voucher_no", "")
    if not voucher_no:
        return {"status": "failed", "error": "voucher missing voucher_no"}
    return _create_simple_pe(
        voucher, voucher_no,
        payment_type="Pay",
        mode_of_payment="Cash",
        paid_account_side="credit",
        paid_account_prefixes=_CASH_PREFIXES,
        party_account_side="debit",
        party_account_prefixes=_PAYABLE_PREFIXES + _EMPLOYEE_ADVANCE_PREFIXES,
        expected_party_type="Supplier",
    )


def _split_unc_legs(legs: list[dict[str, Any]]) -> dict[str, Any]:
    """Classify UNC legs into party_dr / vat_dr / fee_dr / paid_cr buckets.

    Returns:
      {
        "party_dr":   list of Dr legs with account starting 331 or 141
                      (payable / employee advance)
        "vat_dr":     list of Dr legs with account starting 1331 (input VAT)
        "fee_dr":     list of other Dr legs (expense — 635, 6427, etc.)
        "paid_cr":    list of Cr legs with account starting 1121/11215/etc. (bank)
        "other":      legs not matching any bucket (e.g. cash 1111 mid-voucher)
      }
    """
    out = {"party_dr": [], "vat_dr": [], "fee_dr": [], "paid_cr": [], "other": []}
    for leg in legs:
        acct = (leg.get("account") or "").strip()
        debit = leg.get("debit") or 0.0
        credit = leg.get("credit") or 0.0
        if debit > 0:
            if any(acct.startswith(p) for p in _PAYABLE_PREFIXES + _EMPLOYEE_ADVANCE_PREFIXES):
                out["party_dr"].append(leg)
            elif any(acct.startswith(p) for p in ("1331", "13311", "13312")):
                out["vat_dr"].append(leg)
            else:
                out["fee_dr"].append(leg)
        elif credit > 0:
            if any(acct.startswith(p) for p in _BANK_PREFIXES):
                out["paid_cr"].append(leg)
            else:
                out["other"].append(leg)
        else:
            out["other"].append(leg)
    return out


def create_pe_from_unc(voucher: dict[str, Any],
                      invoice: dict[str, Any] | None = None) -> dict[str, Any]:
    """UNC (Ủy nhiệm chi) → Pay via Bank.

    Handles 2/4/6-leg UNC variants:
      2-leg simple (175 vouchers): Dr 331 / Cr 11215 → PE Pay with single party
      4-leg with VAT (40 vouchers): Dr 331 + Dr 1331 / Cr 11215×2 OR
                                    Dr 6427 + Dr 1331 / Cr 11215×2 (bank fee)
      6-leg interest-only (5 vouchers): Dr 635×3 / Cr 11218×3 (no party)

    If party_dr legs absent (pure bank-fee case), returns 'deferred' so JE
    handler (C8) can post a Journal Entry instead. ERPNext PE requires a
    party — forcing a synthetic one corrupts AR/AP aging.
    """
    voucher_no = voucher.get("voucher_no", "")
    if not voucher_no:
        return {"status": "failed", "error": "voucher missing voucher_no"}

    if frappe.db.exists("Payment Entry", voucher_no):
        return {"status": "skipped", "target_name": voucher_no,
                "reason": "already_exists"}

    legs = voucher.get("legs") or []
    if not legs:
        return {"status": "failed", "error": f"{voucher_no}: no legs"}

    buckets = _split_unc_legs(legs)

    # Simple 2-leg path: delegate to _create_simple_pe
    if (len(legs) == 2 and len(buckets["party_dr"]) == 1
            and len(buckets["paid_cr"]) == 1):
        return _create_simple_pe(
            voucher, voucher_no,
            payment_type="Pay",
            mode_of_payment="Bank Draft",
            paid_account_side="credit",
            paid_account_prefixes=_BANK_PREFIXES,
            party_account_side="debit",
            party_account_prefixes=_PAYABLE_PREFIXES + _EMPLOYEE_ADVANCE_PREFIXES,
            expected_party_type="Supplier",
        )

    # No party leg → defer to JE handler (commit 8 will handle).
    if not buckets["party_dr"]:
        return {"status": "deferred",
                "target_name": None,
                "error": f"{voucher_no}: no Dr 331 / Dr 141 leg — route to JE handler",
                "voucher_kind": "je_fallback"}

    # Multi-leg with party: build PE Pay with deductions[]
    company = _company_default()
    if not company:
        return {"status": "failed", "error": "No Company configured"}
    mapping = _load_account_mapping()

    # Sum party Dr (main pay-to-party amount), fee/vat Dr (go to deductions)
    party_amount = sum(l.get("debit") or 0.0 for l in buckets["party_dr"])
    fee_amount = sum(l.get("debit") or 0.0 for l in buckets["fee_dr"])
    vat_amount = sum(l.get("debit") or 0.0 for l in buckets["vat_dr"])
    paid_amount = sum(l.get("credit") or 0.0 for l in buckets["paid_cr"])

    if abs((party_amount + fee_amount + vat_amount) - paid_amount) > 0.01:
        return {"status": "failed",
                "error": f"{voucher_no}: UNC unbalanced after split "
                         f"(party={party_amount}, fee={fee_amount}, "
                         f"vat={vat_amount}, paid={paid_amount})"}

    # Use FIRST party Dr leg's account as party_account (Cr 331 in ERPNext PE)
    party_account = _resolve_account(
        buckets["party_dr"][0]["account"], mapping, company
    )
    # Use FIRST paid Cr leg's account as paid_from (the bank)
    paid_from = _resolve_account(
        buckets["paid_cr"][0]["account"], mapping, company
    )
    if not party_account or not paid_from:
        return {"status": "failed",
                "error": f"{voucher_no}: cannot resolve party_account or paid_from"}

    party_code = voucher.get("party_code") or ""
    # PERF (Tier 1.5): set-lookup vs per-call DB round-trip
    from vn_accounting.misa_migration.importers.nkc_handlers import (
        _party_cache as _pc_unc,
    )
    if not party_code or not _pc_unc.is_supplier(party_code):
        return {"status": "failed",
                "error": f"{voucher_no}: Supplier {party_code!r} not found"}

    # Build deductions[] — one row per fee + vat leg
    deductions_payload: list[dict[str, Any]] = []
    cc_default = _default_cost_center(company)
    for leg in buckets["fee_dr"] + buckets["vat_dr"]:
        deduct_acct = _resolve_account(leg["account"], mapping, company)
        if not deduct_acct:
            return {"status": "failed",
                    "error": f"{voucher_no}: cannot resolve deduction account "
                             f"for TK {leg['account']!r}"}
        deductions_payload.append({
            "account": deduct_acct,
            "amount": float(leg.get("debit") or 0.0),
            "description": leg.get("leg_desc") or f"Misa TK {leg['account']}",
            "cost_center": cc_default,
        })

    payload = {
        "doctype": "Payment Entry",
        "company": company,
        "posting_date": voucher.get("posting_date"),
        "set_posting_time": 1,
        "payment_type": "Pay",
        "mode_of_payment": "Bank Draft"
            if frappe.db.exists("Mode of Payment", "Bank Draft") else None,
        "party_type": "Supplier",
        "party": party_code,
        "paid_from": paid_from,
        "paid_from_account_currency": "VND",
        "paid_amount": paid_amount,
        "paid_to": party_account,
        "paid_to_account_currency": "VND",
        # Bank Payment Entries require reference_no / reference_date.
        "reference_no": voucher_no,
        "reference_date": voucher.get("posting_date"),
        "received_amount": party_amount,  # only party-side reaches the payee
        "deductions": deductions_payload,
        "remarks": voucher.get("voucher_remark") or voucher_no,
        "misa_voucher_no": voucher_no,
        "cost_center": cc_default,
    }

    # Same FIFO-by-party reference linkage as 2-leg path. `party_amount`
    # is what actually reaches the Supplier (excluding fee/vat
    # deductions), so allocate references against that amount only.
    #
    # SKIP refs when the raw Misa party_dr leg account is an employee-payable
    # (334*) or employee-advance (141*) account. These are salary / advance
    # payments to the company-as-Supplier name (e.g. "DCNET" itself); they
    # don't represent payment of a Purchase Invoice. Adding refs to unrelated
    # PIs causes "associated with 331, but Party Account is 3341" validation
    # errors at PE.insert(). Leave refs empty and post as unallocated advance —
    # GL is still correct (Dr 3341 / Cr bank), only the per-invoice allocation
    # is intentionally absent.
    raw_party_tk = (buckets["party_dr"][0].get("account") or "").strip()
    is_employee_payable = raw_party_tk.startswith("334") or raw_party_tk.startswith("141")
    if is_employee_payable:
        refs = []
    else:
        refs = _resolve_pe_references(
            party_type="Supplier", party=party_code, amount=party_amount,
            company=company, posting_date=voucher.get("posting_date"),
        )
    if refs:
        payload["references"] = refs

    try:
        doc = frappe.get_doc(payload)
        doc.flags.ignore_permissions = True
        # PERF (Tier 1.2): preflight already validated Party / Account links;
        # skip ERPNext's per-row Link integrity check.
        doc.flags.ignore_links = True
        doc.insert(set_name=voucher_no)
        return {"status": "created", "target_name": doc.name,
                "target_doctype": "Payment Entry",
                "payment_type": "Pay",
                "party_amount": party_amount,
                "fee_amount": fee_amount,
                "vat_amount": vat_amount,
                "paid_amount": paid_amount,
                "deduction_count": len(deductions_payload)}
    except Exception as exc:
        err = f"{type(exc).__name__}: {exc}"
        frappe.log_error(title=f"Misa UNC multi-leg PE create failed: {voucher_no}",
                         message=err)
        return {"status": "failed", "target_name": None, "error": err}
