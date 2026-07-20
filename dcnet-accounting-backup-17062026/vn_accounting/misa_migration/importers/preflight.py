"""Pre-flight validation for Phase 4 Post.

Phase D commit 13. Runs 10 checks per spec §9 before any voucher hits
ERPNext. Block-level issues prevent Post (UI shows the dialog +
disables submit); warn-level issues show a confirmation modal but
allow continue; info-level issues just appear in the summary.

Each check is an isolated function `check_*(...)` returning a
CheckResult dict. The orchestrator `run_preflight()` calls each, builds
the aggregate {status, checks, issue_count, block_count} envelope, and
collapses status to:

  - "block" if ANY check has level=block AND passed=False
  - "warn"  if no block fails AND any check has level=warn AND passed=False
  - "ok"    otherwise

The vouchers + invoice dicts must follow the shapes emitted by
parsers/nkc_parser.parse_nkc_rows and
parsers/invoice_list_parser.parse_br_rows / parse_mv_rows.
"""

from __future__ import annotations

import json
from typing import Any

import frappe

from vn_accounting.misa_migration.context import (
    get_active_company as _get_company,
)


# Each check returns a result with this shape
CheckResult = dict[str, Any]
#   {
#     "name": str,        # short id, e.g. "nkc_balance"
#     "label": str,       # human-readable VN label for the UI
#     "level": "block" | "warn" | "info",
#     "passed": bool,
#     "issues": list[str],   # detail strings shown in the dialog
#   }

# Voucher prefix groupings for invoice-join checks
_BH_PREFIXES = ("BH",)
_MV_NEEDED_PREFIXES = ("MDV", "MH", "PN")


# ----------------------------------------------------------------- individual checks

def check_nkc_balance(vouchers: list[dict[str, Any]]) -> CheckResult:
    """1. Every NKC voucher must have Dr=Cr (parser already flags this)."""
    issues: list[str] = []
    for v in vouchers:
        if v.get("balance_error"):
            issues.append(
                f"{v.get('voucher_no', '?')}: {v['balance_error']}"
            )
    return {
        "name": "nkc_balance",
        "label": "Bút toán cân Dr=Cr",
        "level": "block",
        "passed": not issues,
        "issues": issues,
    }


def _has_register_match(invoices: Any, voucher_no: str, invoice_no: str | None) -> bool:
    """True iff the register has line items keyed by voucher_no OR invoice_no.

    Accepts either the new InvoiceLookup or a legacy dict for backward compat
    with tests that pre-date the dual-index refactor.
    """
    if hasattr(invoices, "has"):
        return invoices.has(voucher_no, invoice_no)
    # legacy dict
    return bool(voucher_no) and voucher_no in invoices


def check_bh_has_br_match(
    vouchers: list[dict[str, Any]],
    br_invoices: dict[str, dict[str, Any]],
) -> CheckResult:
    """2. Every BH voucher must have a matching bảng kê BR entry.

    Matches via voucher_no first, then falls back to invoice_no (Số hóa
    đơn) — one invoice in Misa can spawn multiple voucher numbers
    (warehouse + VAT + adjustment), and BR is keyed by the VAT-bearing
    voucher, not the NKC voucher.
    """
    issues: list[str] = []
    for v in vouchers:
        if (v.get("prefix") or "") in _BH_PREFIXES:
            vn = v.get("voucher_no", "")
            inv_no = v.get("invoice_no")
            if vn and not _has_register_match(br_invoices, vn, inv_no):
                issues.append(f"{vn}: thiếu line items trong bảng kê BR")
    return {
        "name": "bh_has_br_match",
        "label": "BH có line items bảng kê",
        "level": "warn",  # spec: warn, allow placeholder Item fallback
        "passed": not issues,
        "issues": issues,
    }


def check_mdv_mh_pn_has_mv_match(
    vouchers: list[dict[str, Any]],
    mv_invoices: dict[str, dict[str, Any]],
) -> CheckResult:
    """3. Every MDV/MH voucher should have matching bảng kê MV entry.

    PN (Phiếu nhập kho) is warehouse-only by Misa convention — it NEVER
    has VAT line items in MV register because the matching VAT voucher
    lives under a sibling MDV20...XXX with the same Số hóa đơn. The
    handler resolves PN's line items via the invoice_no fallback in
    phase_4_orchestrator, so warning here is noise; PN is excluded.

    For MDV/MH: match via voucher_no first, fall back to invoice_no.
    """
    issues: list[str] = []
    for v in vouchers:
        prefix = v.get("prefix") or ""
        if prefix not in _MV_NEEDED_PREFIXES or prefix == "PN":
            continue
        vn = v.get("voucher_no", "")
        inv_no = v.get("invoice_no")
        if vn and not _has_register_match(mv_invoices, vn, inv_no):
            issues.append(f"{vn}: thiếu line items trong bảng kê MV")
    return {
        "name": "mdv_mh_pn_has_mv_match",
        "label": "MDV/MH có line items bảng kê",
        "level": "warn",
        "passed": not issues,
        "issues": issues,
    }


def check_party_code_uniqueness(
    vouchers: list[dict[str, Any]],
) -> CheckResult:
    """4. Informational: party code seen with both 131 (Customer) and 331 (Supplier) legs.

    ERPNext natively supports the same party being both Customer and Supplier
    (banks, telcos, suppliers who also buy from us). Surfaced as info only.
    """
    party_accts: dict[str, set[str]] = {}
    for v in vouchers:
        code = (v.get("party_code") or "").strip()
        if not code:
            continue
        for leg in v.get("legs") or []:
            acct = (leg.get("account") or "").strip()
            if acct.startswith("131") or acct.startswith("331"):
                party_accts.setdefault(code, set()).add(acct[:3])

    issues: list[str] = []
    for code, prefixes in sorted(party_accts.items()):
        if {"131", "331"} <= prefixes:
            issues.append(f"{code}: vừa Customer (131) vừa Supplier (331) — ERPNext hỗ trợ")
    return {
        "name": "party_code_uniqueness",
        "label": "Mã đối tượng đa vai trò (thông tin)",
        "level": "info",
        "passed": not issues,
        "issues": issues,
    }


def check_tk_mapping(
    vouchers: list[dict[str, Any]],
    company: str,
    mapping: dict[str, str] | None = None,
) -> CheckResult:
    """5. Every Misa TK referenced in NKC legs must map to ERPNext Account."""
    if mapping is None:
        try:
            doc = frappe.get_single("Misa Account Mapping")
            mapping = json.loads(doc.mappings or "{}")
        except Exception:
            mapping = {}

    unmapped: set[str] = set()
    for v in vouchers:
        for leg in v.get("legs") or []:
            tk = (leg.get("account") or "").strip()
            if not tk:
                continue
            if tk in mapping:
                continue
            # Live lookup
            live = frappe.db.get_value(
                "Account", {"account_number": tk, "company": company}, "name"
            )
            if live:
                mapping[tk] = live
            else:
                unmapped.add(tk)

    issues = sorted([f"TK {tk}: không tìm thấy Account" for tk in unmapped])
    return {
        "name": "tk_mapping",
        "label": "Tài khoản kế toán đã map",
        "level": "block",
        "passed": not issues,
        "issues": issues,
    }


def check_item_lookup(
    br_invoices: dict[str, dict[str, Any]],
    mv_invoices: dict[str, dict[str, Any]],
) -> CheckResult:
    """6. Item lookup OK or auto-create OK.

    v1 uses placeholder Item for everything; this check is informational.
    """
    line_count = 0
    for inv_dict in (br_invoices, mv_invoices):
        for inv in inv_dict.values():
            line_count += len(inv.get("line_items") or [])
    return {
        "name": "item_lookup",
        "label": "Item lookup / auto-create",
        "level": "info",
        "passed": True,
        "issues": [
            f"v1 dùng placeholder Item cho {line_count} line items "
            "(Phase E sẽ fuzzy-match item_name).",
        ] if line_count else [],
    }


def check_posting_period_not_locked(
    vouchers: list[dict[str, Any]],
    company: str,
) -> CheckResult:
    """7. No Period Closing Voucher (PCV) blocks the posting_date range."""
    dates = sorted({
        v["posting_date"]
        for v in vouchers
        if v.get("posting_date")
    })
    if not dates:
        return {
            "name": "posting_period_not_locked",
            "label": "Kỳ kế toán chưa khóa",
            "level": "block",
            "passed": True,
            "issues": [],
        }
    min_date, max_date = dates[0], dates[-1]
    # Check for PCV with transaction_date covering our window
    blocking_pcvs = frappe.db.sql(
        """
        SELECT name, transaction_date, fiscal_year
        FROM `tabPeriod Closing Voucher`
        WHERE company=%s AND docstatus=1
          AND transaction_date >= %s
        """,
        (company, min_date),
        as_dict=True,
    )
    issues = [
        f"PCV {pcv['name']} (ngày {pcv['transaction_date']}, FY "
        f"{pcv.get('fiscal_year', '?')}) khoá kỳ chứa voucher Misa"
        for pcv in blocking_pcvs
    ]
    return {
        "name": "posting_period_not_locked",
        "label": "Kỳ kế toán chưa khóa",
        "level": "block",
        "passed": not issues,
        "issues": issues,
    }


def check_company_vnd_default(company: str) -> CheckResult:
    """8. Company default currency must be VND (v1 single-currency only)."""
    currency = frappe.db.get_value("Company", company, "default_currency")
    issues: list[str] = []
    if currency != "VND":
        issues.append(
            f"Company {company!r} default_currency = {currency!r}; v1 chỉ "
            "hỗ trợ VND. Đa tệ defer v2."
        )
    return {
        "name": "company_vnd_default",
        "label": "Company default currency = VND",
        "level": "block",
        "passed": not issues,
        "issues": issues,
    }


def check_no_existing_posted(
    vouchers: list[dict[str, Any]],
) -> CheckResult:
    """9. No existing SUBMITTED ERPNext doc with the same Misa voucher_no.

    Checks all 5 target DocTypes (SI, PI, PE, JE, SE — PR covered by PI).

    Only flags ``docstatus=1`` (submitted) docs as a true duplicate-import
    risk. Draft docs (``docstatus=0``) from a previously-interrupted run
    are handled transparently by each handler's ``lookup_existing`` skip
    branch — blocking on them would prevent legitimate resume after a
    worker crash mid-Phase 4a.
    """
    target_doctypes = (
        "Sales Invoice", "Purchase Invoice", "Payment Entry",
        "Journal Entry", "Stock Entry",
    )
    voucher_nos = sorted({
        v.get("voucher_no") for v in vouchers if v.get("voucher_no")
    })
    if not voucher_nos:
        return {
            "name": "no_existing_posted",
            "label": "Voucher chưa được import lần trước",
            "level": "block",
            "passed": True,
            "issues": [],
        }
    existing: list[str] = []
    for dt in target_doctypes:
        rows = frappe.db.sql(
            f"""
            SELECT name, docstatus FROM `tab{dt}`
            WHERE name IN ({','.join(['%s'] * len(voucher_nos))})
              AND docstatus = 1
            """,
            tuple(voucher_nos),
            as_dict=True,
        )
        for r in rows:
            existing.append(f"{dt} {r['name']} đã tồn tại (docstatus=1, đã submit)")
    return {
        "name": "no_existing_posted",
        "label": "Voucher chưa được import lần trước",
        "level": "block",
        "passed": not existing,
        "issues": existing,
    }


def check_supplier_master_present(
    vouchers: list[dict[str, Any]],
) -> CheckResult:
    """10. Every party_code on a PI/PE/PN voucher resolves to a Supplier
    (or Customer for SI-side). Mainly a Phase-3-already-imported check."""
    issues: list[str] = []
    missing_supplier: set[str] = set()
    missing_customer: set[str] = set()
    for v in vouchers:
        code = (v.get("party_code") or "").strip()
        if not code:
            continue
        prefix = v.get("prefix") or ""
        if prefix in ("MDV", "MH", "PN", "UNC", "PC"):
            if not frappe.db.exists("Supplier", code):
                missing_supplier.add(code)
        elif prefix in ("BH", "BC", "PT"):
            if not frappe.db.exists("Customer", code):
                missing_customer.add(code)
    for code in sorted(missing_supplier):
        issues.append(f"Supplier {code!r} thiếu — chạy Phase 3 trước")
    for code in sorted(missing_customer):
        issues.append(f"Customer {code!r} thiếu — chạy Phase 3 trước")
    return {
        "name": "party_masters_present",
        "label": "Master Customer/Supplier đã import",
        "level": "block",
        "passed": not issues,
        "issues": issues,
    }


# ------------------------------------------------------------------- orchestrator

def run_preflight(
    vouchers: list[dict[str, Any]],
    br_invoices: dict[str, dict[str, Any]] | None = None,
    mv_invoices: dict[str, dict[str, Any]] | None = None,
    company: str | None = None,
) -> dict[str, Any]:
    """Run all 10 pre-flight checks and return the aggregate envelope.

    Args:
      vouchers: parsed NKC vouchers (nkc_parser.parse_nkc_rows output).
      br_invoices: dict[voucher_no → invoice] from invoice_list_parser.parse_br_rows.
      mv_invoices: same from parse_mv_rows.
      company: ERPNext Company name. Falls back to global default.

    Returns:
      {
        "status": "ok" | "warn" | "block",
        "checks": list[CheckResult],
        "issue_count": int,    # total issues across all checks
        "block_count": int,    # block-level fail count
        "warn_count": int,
      }
    """
    br_invoices = br_invoices or {}
    mv_invoices = mv_invoices or {}
    if not company:
        company = _get_company()

    checks: list[CheckResult] = []
    # Order matters for UI presentation: balance → joins → party →
    # accounts → items → period → currency → existing → masters
    checks.append(check_nkc_balance(vouchers))
    checks.append(check_bh_has_br_match(vouchers, br_invoices))
    checks.append(check_mdv_mh_pn_has_mv_match(vouchers, mv_invoices))
    checks.append(check_party_code_uniqueness(vouchers))
    if company:
        checks.append(check_tk_mapping(vouchers, company))
    checks.append(check_item_lookup(br_invoices, mv_invoices))
    if company:
        checks.append(check_posting_period_not_locked(vouchers, company))
        checks.append(check_company_vnd_default(company))
    checks.append(check_no_existing_posted(vouchers))
    checks.append(check_supplier_master_present(vouchers))

    block_count = sum(
        1 for c in checks if c["level"] == "block" and not c["passed"]
    )
    warn_count = sum(
        1 for c in checks if c["level"] == "warn" and not c["passed"]
    )
    issue_count = sum(len(c["issues"]) for c in checks)

    if block_count > 0:
        status = "block"
    elif warn_count > 0:
        status = "warn"
    else:
        status = "ok"

    return {
        "status": status,
        "checks": checks,
        "issue_count": issue_count,
        "block_count": block_count,
        "warn_count": warn_count,
    }
