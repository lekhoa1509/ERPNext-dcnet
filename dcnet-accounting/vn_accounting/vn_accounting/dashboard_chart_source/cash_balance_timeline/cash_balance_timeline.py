"""Cash + Bank Balance Timeline — combines TK 111 + 112 into a single line."""

from __future__ import annotations

import frappe
from frappe.utils import add_to_date, formatdate, getdate, nowdate
from frappe.utils.dashboard import cache_source
from frappe.utils.dateutils import get_from_date_from_timespan, get_period_ending
from frappe.utils.nestedset import get_descendants_of

from vn_accounting.vn_accounting.report_utils import BANK_PREFIX, CASH_PREFIX


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

    timespan = chart.timespan
    timegrain = chart.time_interval
    filters = frappe.parse_json(filters) or frappe.parse_json(chart.filters_json)
    company = filters.get("company") or frappe.defaults.get_user_default("Company")

    if not to_date:
        to_date = nowdate()
    if not from_date:
        from_date = get_from_date_from_timespan(to_date, timespan)

    dates = _get_dates(from_date, to_date, timegrain)

    # Collect all leaf accounts under 111% and 112%
    accounts = _get_cash_bank_accounts(company)
    if not accounts:
        return {"labels": [], "datasets": []}

    gl_entries = frappe.db.get_all(
        "GL Entry",
        fields=["posting_date", "debit", "credit"],
        filters={
            "posting_date": ("<", get_period_ending(to_date, timegrain)),
            "account": ("in", accounts),
            "is_cancelled": 0,
        },
        order_by="posting_date asc",
    )

    result = _build_result(dates, gl_entries)

    return {
        "labels": [formatdate(r[0].strftime("%Y-%m-%d")) for r in result],
        "datasets": [
            {"name": "Tiền mặt & Ngân hàng", "values": [r[1] for r in result]}
        ],
    }


def _get_cash_bank_accounts(company):
    """Get all leaf accounts matching 111% or 112% for the company."""
    accounts = []
    for prefix in (CASH_PREFIX, BANK_PREFIX):
        rows = frappe.db.get_all(
            "Account",
            filters={"account_number": ("like", prefix), "company": company, "is_group": 0},
            pluck="name",
        )
        accounts.extend(rows)
    # Also include group accounts that have direct GL entries
    for prefix in (CASH_PREFIX, BANK_PREFIX):
        groups = frappe.db.get_all(
            "Account",
            filters={"account_number": ("like", prefix), "company": company, "is_group": 1},
            pluck="name",
        )
        for g in groups:
            descendants = get_descendants_of("Account", g, ignore_permissions=True)
            accounts.extend(descendants)
    return list(set(accounts))


def _build_result(dates, gl_entries):
    """Cumulative balance (Asset-type: debit - credit)."""
    result = [[getdate(d), 0.0] for d in dates]
    idx = 0
    for entry in gl_entries:
        while idx < len(result) - 1 and getdate(entry.posting_date) > result[idx][0]:
            idx += 1
        result[idx][1] += entry.debit - entry.credit

    # Cumulative sum (Balance Sheet accounts)
    for i in range(1, len(result)):
        result[i][1] += result[i - 1][1]
    return result


def _get_dates(from_date, to_date, timegrain):
    months = 1 if timegrain == "Monthly" else 3 if timegrain == "Quarterly" else 0
    days = 1 if timegrain == "Daily" else 7 if timegrain == "Weekly" else 0
    dates = [get_period_ending(from_date, timegrain)]
    while getdate(dates[-1]) < getdate(to_date):
        dates.append(
            get_period_ending(
                add_to_date(dates[-1], months=months, days=days), timegrain
            )
        )
    return dates
