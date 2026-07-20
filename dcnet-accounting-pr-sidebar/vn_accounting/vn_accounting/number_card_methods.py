from __future__ import annotations

from typing import Any

import frappe
from frappe.utils import getdate, today

from vn_accounting.vn_accounting.report_utils import (
    AP_PREFIX,
    AR_PREFIX,
    BANK_PREFIX,
    CASH_PREFIX,
    EXPENSE_PREFIXES,
    REVENUE_PREFIX,
)


def _get_fiscal_year_dates() -> tuple[str, str]:
    """Get current fiscal year start/end. Falls back to calendar year."""
    try:
        fy = frappe.db.get_value(
            "Fiscal Year",
            {"year_start_date": ("<=", today()), "year_end_date": (">=", today())},
            ["year_start_date", "year_end_date"],
            as_dict=True,
        )
        if fy:
            return fy.year_start_date, fy.year_end_date
    except Exception:
        pass
    dt = getdate(today())
    return f"{dt.year}-01-01", f"{dt.year}-12-31"


@frappe.whitelist()
def get_total_revenue(company: str | None = None, **kwargs: Any) -> float:
    """Tổng doanh thu năm tài chính hiện tại (TK 511 - ghi Có)."""
    company = company or frappe.defaults.get_user_default("Company")
    fy_start, fy_end = _get_fiscal_year_dates()
    result = frappe.db.sql(
        """
        SELECT COALESCE(SUM(credit) - SUM(debit), 0) as total
        FROM `tabGL Entry`
        WHERE account LIKE %(prefix)s
          AND company = %(company)s
          AND is_cancelled = 0
          AND posting_date BETWEEN %(fy_start)s AND %(fy_end)s
        """,
        {"prefix": REVENUE_PREFIX, "company": company, "fy_start": fy_start, "fy_end": fy_end},
        as_dict=True,
    )
    return {"value": result[0].total if result else 0}


@frappe.whitelist()
def get_total_expenses(company: str | None = None, **kwargs: Any) -> float:
    """Tổng chi phí năm tài chính hiện tại (TK 621-642 - ghi Nợ)."""
    company = company or frappe.defaults.get_user_default("Company")
    fy_start, fy_end = _get_fiscal_year_dates()
    like_clauses = " OR ".join(f"account LIKE %(p{i})s" for i in range(len(EXPENSE_PREFIXES)))
    params = {f"p{i}": p for i, p in enumerate(EXPENSE_PREFIXES)}
    params.update({"company": company, "fy_start": fy_start, "fy_end": fy_end})
    result = frappe.db.sql(
        f"""
        SELECT COALESCE(SUM(debit) - SUM(credit), 0) as total
        FROM `tabGL Entry`
        WHERE ({like_clauses})
          AND company = %(company)s
          AND is_cancelled = 0
          AND posting_date BETWEEN %(fy_start)s AND %(fy_end)s
        """,
        params,
        as_dict=True,
    )
    return {"value": result[0].total if result else 0}


@frappe.whitelist()
def get_accounts_receivable(company: str | None = None, **kwargs: Any) -> float:
    """Công nợ phải thu (số dư Nợ TK 131)."""
    company = company or frappe.defaults.get_user_default("Company")
    result = frappe.db.sql(
        """
        SELECT COALESCE(SUM(debit) - SUM(credit), 0) as total
        FROM `tabGL Entry`
        WHERE account LIKE %(prefix)s
          AND company = %(company)s
          AND is_cancelled = 0
        """,
        {"prefix": AR_PREFIX, "company": company},
        as_dict=True,
    )
    return {"value": result[0].total if result else 0}


@frappe.whitelist()
def get_accounts_payable(company: str | None = None, **kwargs: Any) -> float:
    """Công nợ phải trả (số dư Có TK 331)."""
    company = company or frappe.defaults.get_user_default("Company")
    result = frappe.db.sql(
        """
        SELECT COALESCE(SUM(credit) - SUM(debit), 0) as total
        FROM `tabGL Entry`
        WHERE account LIKE %(prefix)s
          AND company = %(company)s
          AND is_cancelled = 0
        """,
        {"prefix": AP_PREFIX, "company": company},
        as_dict=True,
    )
    return {"value": result[0].total if result else 0}


@frappe.whitelist()
def get_cash_balance(company: str | None = None, **kwargs: Any) -> float:
    """Tồn quỹ (số dư Nợ TK 111 + 112)."""
    company = company or frappe.defaults.get_user_default("Company")
    result = frappe.db.sql(
        """
        SELECT COALESCE(SUM(debit) - SUM(credit), 0) as total
        FROM `tabGL Entry`
        WHERE (account LIKE %(cash)s OR account LIKE %(bank)s)
          AND company = %(company)s
          AND is_cancelled = 0
        """,
        {"cash": CASH_PREFIX, "bank": BANK_PREFIX, "company": company},
        as_dict=True,
    )
    return {"value": result[0].total if result else 0}
