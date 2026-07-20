"""Revenue vs Expense — rolling 12 months ending at current month, labels T1..T12."""

from __future__ import annotations

import frappe
from frappe.utils import add_months, get_first_day, get_last_day, getdate, nowdate
from frappe.utils.dashboard import cache_source

from vn_accounting.vn_accounting.report_utils import EXPENSE_PREFIXES, REVENUE_PREFIX


@frappe.whitelist()
@cache_source
def get(
    chart_name=None,
    chart=None,
    no_cache=None,
    filters=None,
    from_date=None,
    to_date=None,
    timespan=None,
    time_interval=None,
    heatmap_year=None,
):
    if chart_name:
        chart = frappe.get_doc("Dashboard Chart", chart_name)
    else:
        chart = frappe._dict(frappe.parse_json(chart))

    filters = frappe.parse_json(filters) or frappe.parse_json(chart.filters_json)
    company = filters.get("company") or frappe.defaults.get_user_default("Company")

    today = getdate(nowdate())
    # Rolling 12 months: from 11 months ago to current month
    months = []
    for i in range(11, -1, -1):
        d = add_months(today, -i)
        months.append((get_first_day(d), get_last_day(d), d.month))

    labels = [f"T{m[2]}" for m in months]
    revenue_vals = []
    expense_vals = []

    for first_day, last_day, _ in months:
        rev = _sum_gl(company, REVENUE_PREFIX, first_day, last_day, credit_minus_debit=True)
        revenue_vals.append(rev)

        exp = _sum_gl_multi(company, EXPENSE_PREFIXES, first_day, last_day)
        expense_vals.append(exp)

    profit_vals = [r - e for r, e in zip(revenue_vals, expense_vals)]

    return {
        "labels": labels,
        "datasets": [
            {"name": "Doanh thu", "values": revenue_vals},
            {"name": "Chi phí", "values": expense_vals},
            {"name": "Lợi nhuận", "values": profit_vals},
        ],
    }


def _sum_gl(company, prefix, from_date, to_date, credit_minus_debit=False):
    result = frappe.db.sql(
        """
        SELECT COALESCE(SUM(credit) - SUM(debit), 0) as total
        FROM `tabGL Entry`
        WHERE account LIKE %(prefix)s
          AND company = %(company)s
          AND is_cancelled = 0
          AND posting_date BETWEEN %(from)s AND %(to)s
        """,
        {"prefix": prefix, "company": company, "from": from_date, "to": to_date},
        as_dict=True,
    )
    val = result[0].total if result else 0
    return val if credit_minus_debit else abs(val)


def _sum_gl_multi(company, prefixes, from_date, to_date):
    like_clauses = " OR ".join(f"account LIKE %(p{i})s" for i in range(len(prefixes)))
    params = {f"p{i}": p for i, p in enumerate(prefixes)}
    params.update({"company": company, "from": from_date, "to": to_date})
    result = frappe.db.sql(
        f"""
        SELECT COALESCE(SUM(debit) - SUM(credit), 0) as total
        FROM `tabGL Entry`
        WHERE ({like_clauses})
          AND company = %(company)s
          AND is_cancelled = 0
          AND posting_date BETWEEN %(from)s AND %(to)s
        """,
        params,
        as_dict=True,
    )
    return result[0].total if result else 0
