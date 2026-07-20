"""Accounting helper for inline posting on Asset Repair / CCDC events.

Provides a uniform pattern: parent doc carries a child table `accounting_entries`
(VN Accounting Entry), pre-filled with TT99/2025 defaults from
`build_default_entries`, edited by accountant if needed, then posted as a
single Journal Entry per event via `post_je_from_entries`.

All account number lookups go through `lookup_account_by_number`. Hardcoded TK
strings are forbidden in JE creation paths.
"""
from __future__ import annotations

from typing import Optional

import frappe
from frappe import _


def _vnd(value) -> float:
    """Round a numeric value to whole VND. Pure Python — safe in unit tests."""
    try:
        return float(round(float(value or 0)))
    except (TypeError, ValueError):
        return 0.0


# --------------------------------------------------------------------------- #
# Account lookups
# --------------------------------------------------------------------------- #

def lookup_account_by_number(company: str, account_number: str) -> str:
    """Return leaf Account name for the given account_number on a company.

    Raises with VN-language message if not found. Always filters is_group=0.
    """
    name = frappe.db.get_value(
        "Account",
        {"company": company, "account_number": account_number, "is_group": 0},
        "name",
    )
    if not name:
        frappe.throw(
            _("Không tìm thấy tài khoản {0} cho công ty {1}. Kiểm tra Hệ thống tài khoản (TT99/2025).").format(
                account_number, company
            )
        )
    return name


def resolve_cost_center(doc, company: str) -> Optional[str]:
    """Resolve cost center via fallback chain: doc.cost_center → doc.project.cost_center → company.cost_center."""
    cc = getattr(doc, "cost_center", None)
    if cc:
        return cc
    project = getattr(doc, "project", None)
    if project:
        proj_cc = frappe.db.get_value("Project", project, "cost_center")
        if proj_cc:
            return proj_cc
    return frappe.db.get_value("Company", company, "cost_center")


# --------------------------------------------------------------------------- #
# Default entry builder — pure function, no DB writes
# --------------------------------------------------------------------------- #

# Mapping per spec §5.1-5.4 (errata-merged)
# Each tuple: (debit_code, credit_code) for the principal row.
# VAT row always: (1331, credit_of_principal_row)
_AR_PRINCIPAL = {
    "Chi phí": ("6427", "111"),
    "Sửa chữa lớn vốn hóa": ("2413", "331"),
    "Nâng cấp cải tạo": ("2412", "331"),
}


def build_default_entries(
    event_type: str,
    classification: Optional[str],
    amount: float,
    has_vat: bool = False,
    vat_rate: float = 10.0,
    company: Optional[str] = None,
    asset_name: Optional[str] = None,
    remaining_242: float = 0,
    remaining_153: float = 0,
    compensation_amount: float = 0,
) -> list[dict]:
    """Return list of dicts shaped {account_debit, account_credit, amount, description, is_vat}.

    event_type ∈ {"Asset Repair", "CCDC Item Purchase", "CCDC Writeoff"}.
    For CCDC Allocation, callers build rows directly from the schedule child
    rows (one JE per period); this builder handles only the lifecycle events.

    Pure function: no DB writes. But DOES read Account names (read-only) when
    `company` is supplied. If `company` is None (test-only), returns rows with
    raw account-number strings — caller must resolve before posting.
    """
    rows: list[dict] = []
    amt = _vnd(amount)

    def _resolve(code: str) -> str:
        if not company:
            return code  # test-shape; caller resolves
        return lookup_account_by_number(company, code)

    if event_type == "Asset Repair":
        if classification not in _AR_PRINCIPAL:
            frappe.throw(_("Phân loại sửa chữa không hợp lệ: {0}").format(classification or ""))
        d_code, c_code = _AR_PRINCIPAL[classification]
        desc_main = _("Sửa chữa TSCĐ {0} ({1})").format(asset_name or "", classification)
        rows.append({
            "account_debit": _resolve(d_code),
            "account_credit": _resolve(c_code),
            "amount": amt,
            "description": desc_main,
            "is_vat": 0,
        })
        if has_vat and amt > 0:
            vat_amt = _vnd(amt * float(vat_rate or 0) / 100)
            rows.append({
                "account_debit": _resolve("1331"),
                "account_credit": _resolve(c_code),
                "amount": vat_amt,
                "description": _("VAT đầu vào {0}%").format(float(vat_rate or 0)),
                "is_vat": 1,
            })

    elif event_type == "CCDC Item Purchase":
        # VAS textbook flow combines purchase + issuance for amortization
        # into a single accounting event for CCDC items recognised at purchase
        # time (typical for ERPNext-tracked CCDC where the item is immediately
        # put into use). Two rows model the two distinct economic facts:
        #   Row 1: Dr 153 / Cr 331 — supplies received from vendor (payable created)
        #   Row 2: Dr 242 / Cr 153 — issued for amortization (cost moved to prepaid)
        # Net effect: TK 153 stays at 0 (transit), TK 242 += cost (asset),
        # TK 331 += cost (payable). Without the first row, TK 153 goes negative,
        # which breaks Mã 140 / Mã 270 on B01.
        rows.append({
            "account_debit": _resolve("153"),
            "account_credit": _resolve("331"),
            "amount": amt,
            "description": _("Mua CCDC nhập kho"),
            "is_vat": 0,
        })
        rows.append({
            "account_debit": _resolve("242"),
            "account_credit": _resolve("153"),
            "amount": amt,
            "description": _("Xuất kho CCDC để phân bổ qua TK 242"),
            "is_vat": 0,
        })
        if has_vat and amt > 0:
            vat_amt = _vnd(amt * float(vat_rate or 0) / 100)
            rows.append({
                "account_debit": _resolve("1331"),
                "account_credit": _resolve("331"),
                "amount": vat_amt,
                "description": _("VAT đầu vào {0}%").format(float(vat_rate or 0)),
                "is_vat": 1,
            })

    elif event_type == "CCDC Writeoff":
        # 1-3 rows: 6423/242 (always if rem_242>0), 632/153 (if rem_153>0), 1388/711 (if compensation>0)
        rem_242 = _vnd(remaining_242)
        rem_153 = _vnd(remaining_153)
        comp = _vnd(compensation_amount)
        if rem_242 > 0:
            rows.append({
                "account_debit": _resolve("6423"),
                "account_credit": _resolve("242"),
                "amount": rem_242,
                "description": _("Ghi giảm CCDC — xóa số dư TK 242"),
                "is_vat": 0,
            })
        if rem_153 > 0:
            rows.append({
                "account_debit": _resolve("632"),
                "account_credit": _resolve("153"),
                "amount": rem_153,
                "description": _("Ghi giảm CCDC — xóa số dư TK 153"),
                "is_vat": 0,
            })
        if comp > 0:
            rows.append({
                "account_debit": _resolve("1388"),
                "account_credit": _resolve("711"),
                "amount": comp,
                "description": _("Bồi thường ghi giảm CCDC"),
                "is_vat": 0,
            })

    else:
        frappe.throw(_("Loại sự kiện không hợp lệ: {0}").format(event_type))

    return rows


# --------------------------------------------------------------------------- #
# JE poster — turns child rows into a Journal Entry
# --------------------------------------------------------------------------- #

def post_je_from_entries(
    entries: list,
    company: str,
    posting_date,
    user_remark: str,
    ref_doctype: str,
    ref_name: str,
    submit: bool = True,
    cost_center: Optional[str] = None,
    source_key: Optional[str] = None,
) -> str:
    """Create a Journal Entry from `entries` rows.

    Each entry produces 2 JE Account rows (debit + credit). Both rows carry
    `reference_type` + `reference_name` so ERPNext "Sổ Cái" filtering by
    `voucher_no = JE.name` returns rows tagged with the source doc.

    Returns the JE name. Validates that sum(debit) == sum(credit).
    """
    if not entries:
        frappe.throw(_("Không có dòng hạch toán nào để ghi sổ"))

    accounts: list[dict] = []
    total_d = 0.0
    total_c = 0.0
    for row in entries:
        # Normalize: support both dict and Document-like row objects
        debit_acc = row.get("account_debit") if isinstance(row, dict) else row.account_debit
        credit_acc = row.get("account_credit") if isinstance(row, dict) else row.account_credit
        amount = _vnd(row.get("amount") if isinstance(row, dict) else row.amount)
        desc = row.get("description") if isinstance(row, dict) else getattr(row, "description", "")
        # Optional per-entry party (needed when credit account is Payable e.g. TK 331)
        party_type = (row.get("party_type") if isinstance(row, dict) else getattr(row, "party_type", None)) or None
        party = (row.get("party") if isinstance(row, dict) else getattr(row, "party", None)) or None

        if amount <= 0:
            frappe.throw(_("Số tiền dòng hạch toán phải > 0"))
        if not debit_acc or not credit_acc:
            frappe.throw(_("Mỗi dòng phải có Tài khoản Nợ và Có"))

        accounts.append({
            "account": debit_acc,
            "debit_in_account_currency": amount,
            "credit_in_account_currency": 0,
            "user_remark": desc or user_remark,
            "reference_type": ref_doctype,
            "reference_name": ref_name,
            **({"cost_center": cost_center} if cost_center else {}),
        })
        credit_row: dict = {
            "account": credit_acc,
            "debit_in_account_currency": 0,
            "credit_in_account_currency": amount,
            "user_remark": desc or user_remark,
            "reference_type": ref_doctype,
            "reference_name": ref_name,
            **({"cost_center": cost_center} if cost_center else {}),
        }
        if party_type and party:
            credit_row["party_type"] = party_type
            credit_row["party"] = party
        accounts.append(credit_row)
        total_d += amount
        total_c += amount

    if abs(total_d - total_c) > 0.01:
        frappe.throw(_("JE không cân: Nợ={0}, Có={1}").format(total_d, total_c))

    je = frappe.get_doc({
        "doctype": "Journal Entry",
        "voucher_type": "Journal Entry",
        "company": company,
        "posting_date": posting_date,
        "user_remark": user_remark,
        "accounts": accounts,
    })
    je.flags.ignore_permissions = True
    je.insert()
    if submit:
        je.submit()

    if source_key:
        from vn_accounting.auto_source import register
        register("Journal Entry", je.name, source_key,
                 registered_by=f"vn_accounting.utils.accounting_posting / {ref_doctype}")

    return je.name
