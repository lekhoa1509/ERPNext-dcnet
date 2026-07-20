"""VN Accounting Dashboard API — single endpoint for KPIs + charts."""

from __future__ import annotations

import frappe
from frappe.utils import add_days, date_diff, get_first_day, get_last_day, getdate, nowdate

from vn_accounting.vn_accounting.report_utils import (
    AP_PREFIX,
    AR_PREFIX,
    BANK_PREFIX,
    CASH_PREFIX,
    EXPENSE_PREFIXES,
    REVENUE_PREFIX,
)

from vn_accounting.api.dashboard_charts import (
    get_ar_aging,
    get_ar_donut,
    get_ap_donut,
    get_cash_timeline,
    get_expense_by_type,
    get_revenue_by_item_group,
    get_revenue_expense_chart,
    get_top_customers_revenue,
)


def _sum_gl(company, prefix, from_date, to_date, credit_minus_debit=False):
    """Sum GL entries for a single account prefix in date range."""
    result = frappe.db.sql(
        """
        SELECT COALESCE(SUM(credit) - SUM(debit), 0) as total
        FROM `tabGL Entry`
        WHERE account LIKE %(prefix)s
          AND company = %(company)s
          AND is_cancelled = 0
          AND posting_date BETWEEN %(from_date)s AND %(to_date)s
        """,
        {"prefix": prefix, "company": company, "from_date": from_date, "to_date": to_date},
        as_dict=True,
    )
    val = result[0].total if result else 0
    return val if credit_minus_debit else abs(val)


def _sum_gl_multi(company, prefixes, from_date, to_date):
    """Sum GL entries for multiple account prefixes (debit - credit)."""
    like_clauses = " OR ".join(f"account LIKE %(p{i})s" for i in range(len(prefixes)))
    params = {f"p{i}": p for i, p in enumerate(prefixes)}
    params.update({"company": company, "from_date": from_date, "to_date": to_date})
    result = frappe.db.sql(
        f"""
        SELECT COALESCE(SUM(debit) - SUM(credit), 0) as total
        FROM `tabGL Entry`
        WHERE ({like_clauses})
          AND company = %(company)s
          AND is_cancelled = 0
          AND posting_date BETWEEN %(from_date)s AND %(to_date)s
        """,
        params,
        as_dict=True,
    )
    return result[0].total if result else 0


def _balance_gl(company, prefix, to_date=None):
    """Get balance (debit - credit) for account prefix, optionally up to a date."""
    date_filter = "AND posting_date <= %(to_date)s" if to_date else ""
    result = frappe.db.sql(
        f"""
        SELECT COALESCE(SUM(debit) - SUM(credit), 0) as total
        FROM `tabGL Entry`
        WHERE account LIKE %(prefix)s
          AND company = %(company)s
          AND is_cancelled = 0
          {date_filter}
        """,
        {"prefix": prefix, "company": company, "to_date": to_date},
        as_dict=True,
    )
    return result[0].total if result else 0


def _balance_gl_cash(company, to_date=None):
    """Get cash + bank balance up to a date."""
    date_filter = "AND posting_date <= %(to_date)s" if to_date else ""
    result = frappe.db.sql(
        f"""
        SELECT COALESCE(SUM(debit) - SUM(credit), 0) as total
        FROM `tabGL Entry`
        WHERE (account LIKE %(cash)s OR account LIKE %(bank)s)
          AND company = %(company)s
          AND is_cancelled = 0
          {date_filter}
        """,
        {"cash": CASH_PREFIX, "bank": BANK_PREFIX, "company": company, "to_date": to_date},
        as_dict=True,
    )
    return result[0].total if result else 0


def _calc_delta(current, previous):
    """Calculate delta percentage. Returns None if previous is 0."""
    if not previous:
        return None
    return round((current - previous) / abs(previous) * 100, 1)


def _get_prev_period(from_date, to_date):
    """Mirror the selected range backwards for delta comparison."""
    diff = date_diff(to_date, from_date)
    prev_from = add_days(from_date, -(diff + 1))
    prev_to = add_days(from_date, -1)
    return prev_from, prev_to


def _get_kpis(company, from_date, to_date):
    """Build 5 KPI items with delta comparison."""
    prev_from, prev_to = _get_prev_period(from_date, to_date)

    rev_cur = _sum_gl(company, REVENUE_PREFIX, from_date, to_date, credit_minus_debit=True)
    rev_prev = _sum_gl(company, REVENUE_PREFIX, prev_from, prev_to, credit_minus_debit=True)

    exp_cur = _sum_gl_multi(company, EXPENSE_PREFIXES, from_date, to_date)
    exp_prev = _sum_gl_multi(company, EXPENSE_PREFIXES, prev_from, prev_to)

    ar_now = _balance_gl(company, AR_PREFIX)
    ar_at_from = _balance_gl(company, AR_PREFIX, add_days(from_date, -1))

    ap_now = -_balance_gl(company, AP_PREFIX)
    ap_at_from = -_balance_gl(company, AP_PREFIX, add_days(from_date, -1))

    cash_now = _balance_gl_cash(company)
    cash_at_from = _balance_gl_cash(company, add_days(from_date, -1))

    return [
        {"title": "Tổng Doanh Thu", "value": rev_cur, "delta": _calc_delta(rev_cur, rev_prev), "color": "#2e7d32"},
        {"title": "Tổng Chi Phí", "value": exp_cur, "delta": _calc_delta(exp_cur, exp_prev), "color": "#e65100"},
        {"title": "Công Nợ Phải Thu", "value": ar_now, "delta": _calc_delta(ar_now, ar_at_from), "color": "#1565c0"},
        {"title": "Công Nợ Phải Trả", "value": ap_now, "delta": _calc_delta(ap_now, ap_at_from), "color": "#c62828"},
        {"title": "Tồn Quỹ", "value": cash_now, "delta": _calc_delta(cash_now, cash_at_from), "color": "#00695c"},
    ]


@frappe.whitelist()
def get_dashboard(from_date=None, to_date=None, company=None, granularity="month"):
    """Main dashboard endpoint — returns KPIs + chart data.

    granularity: "week" | "month" | "quarter" | "year"
    - KPIs use from_date/to_date for the current period value + delta
    - Time-series charts (revenue_expense, cash_timeline) use granularity
      to determine their rolling window and grouping
    - Donut charts and AR aging use from_date/to_date as data filter
    """
    company = company or frappe.defaults.get_user_default("Company")
    if not company:
        frappe.throw("No company selected")

    today = getdate(nowdate())
    if not from_date:
        from_date = get_first_day(today)
    if not to_date:
        to_date = get_last_day(today)

    from_date = getdate(from_date)
    to_date = getdate(to_date)

    return {
        "kpis": _get_kpis(company, from_date, to_date),
        "charts": {
            "revenue_expense": get_revenue_expense_chart(company, from_date, to_date, granularity),
            "cash_timeline": get_cash_timeline(company, from_date, to_date, granularity),
            "ar_by_customer": get_ar_donut(company),
            "ap_by_supplier": get_ap_donut(company),
            "revenue_by_item_group": get_revenue_by_item_group(company, from_date, to_date),
            "expense_by_type": get_expense_by_type(company, from_date, to_date),
            "top_customers_revenue": get_top_customers_revenue(company, from_date, to_date),
            "ar_aging": get_ar_aging(company),
        },
    }
