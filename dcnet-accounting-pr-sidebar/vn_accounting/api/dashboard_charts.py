"""VN Accounting Dashboard — chart data functions (8 charts)."""

from __future__ import annotations

import datetime

import frappe
from frappe.utils import add_days, add_months, get_first_day, get_last_day, getdate, nowdate

from vn_accounting.vn_accounting.report_utils import (
    BANK_PREFIX,
    CASH_PREFIX,
    EXPENSE_PREFIXES,
    REVENUE_PREFIX,
)


# ---------------------------------------------------------------------------
# GL helpers
# ---------------------------------------------------------------------------

def _sum_gl(company, prefix, from_date, to_date, credit_minus_debit=False):
    """Sum GL entries for a single account prefix in date range.

    Excludes Period Closing Voucher — it reverses P&L accounts to retained
    earnings at year-end, producing a one-period negative spike that hides the
    real trend.
    """
    result = frappe.db.sql(
        """
        SELECT COALESCE(SUM(credit) - SUM(debit), 0) as total
        FROM `tabGL Entry`
        WHERE account LIKE %(prefix)s
          AND company = %(company)s
          AND is_cancelled = 0
          AND voucher_type != 'Period Closing Voucher'
          AND posting_date BETWEEN %(from_date)s AND %(to_date)s
        """,
        {"prefix": prefix, "company": company, "from_date": from_date, "to_date": to_date},
        as_dict=True,
    )
    val = result[0].total if result else 0
    return val if credit_minus_debit else abs(val)


def _sum_gl_multi(company, prefixes, from_date, to_date):
    """Sum GL entries for multiple account prefixes (debit - credit).

    Excludes Period Closing Voucher (see _sum_gl).
    """
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
          AND voucher_type != 'Period Closing Voucher'
          AND posting_date BETWEEN %(from_date)s AND %(to_date)s
        """,
        params,
        as_dict=True,
    )
    return result[0].total if result else 0


def _balance_gl_prefix(company, prefix, to_date=None):
    """Get balance (debit - credit) for a single account prefix, up to a date."""
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
    return _balance_gl_prefix(company, CASH_PREFIX, to_date) + _balance_gl_prefix(company, BANK_PREFIX, to_date)


def _top_n_donut(data, n=4):
    """Group data into top N + 'Khác' bucket."""
    if not data:
        return {"labels": [], "datasets": [{"values": []}]}

    top = data[:n]
    rest = data[n:]
    labels = [d.name for d in top]
    values = [float(d.total) for d in top]

    if rest:
        labels.append("Khác")
        values.append(sum(float(d.total) for d in rest))

    return {"labels": labels, "datasets": [{"values": values}]}


# ---------------------------------------------------------------------------
# Period builder — granularity-aware
# ---------------------------------------------------------------------------

def _build_periods(to_date, granularity="month"):
    """Build rolling periods ending at to_date.

    Returns list of (from_date, to_date, label) tuples.

    | Granularity | Window | Label examples          |
    |-------------|--------|-------------------------|
    | week        | 12 wks | "7/4", "14/4"           |
    | month       | 12 mo  | "5/25", "6/25", "1", "2"|
    | quarter     | 8 qtrs | "Q1/25", "Q2/25"        |
    | year        | 5 yrs  | "2022", "2023"          |
    """
    end = getdate(to_date)
    periods = []

    if granularity == "week":
        # ISO weekday: Monday=1. Go back to Monday of current week.
        current_monday = end - datetime.timedelta(days=end.weekday())
        for i in range(11, -1, -1):
            monday = current_monday - datetime.timedelta(weeks=i)
            sunday = monday + datetime.timedelta(days=6)
            label = f"{monday.day}/{monday.month}"
            periods.append((monday, sunday, label))

    elif granularity == "quarter":
        # Current quarter
        q = (end.month - 1) // 3
        q_start_month = q * 3 + 1
        current_q_start = datetime.date(end.year, q_start_month, 1)
        for i in range(7, -1, -1):
            q_start = add_months(current_q_start, -i * 3)
            q_start = getdate(q_start)
            q_end = get_last_day(add_months(q_start, 2))
            q_num = (q_start.month - 1) // 3 + 1
            label = f"Q{q_num}/{q_start.year % 100}"
            periods.append((q_start, q_end, label))

    elif granularity == "year":
        for i in range(4, -1, -1):
            y = end.year - i
            y_start = datetime.date(y, 1, 1)
            y_end = datetime.date(y, 12, 31)
            periods.append((y_start, y_end, str(y)))

    else:  # month (default)
        for i in range(11, -1, -1):
            d = add_months(end, -i)
            d = getdate(d)
            first = get_first_day(d)
            last = get_last_day(d)
            label = f"{d.month}" if d.year == end.year else f"{d.month}/{d.year % 100}"
            periods.append((first, last, label))

    return periods


# ---------------------------------------------------------------------------
# Chart 1: Revenue vs Expense (bar stacked)
# ---------------------------------------------------------------------------

def get_revenue_expense_chart(company, from_date, to_date, granularity="month"):
    """Revenue vs Expense bar chart — rolling periods based on granularity."""
    periods = _build_periods(to_date, granularity)

    labels = [p[2] for p in periods]
    rev_vals, exp_vals = [], []

    for first_day, last_day, _ in periods:
        rev_vals.append(_sum_gl(company, REVENUE_PREFIX, first_day, last_day, credit_minus_debit=True))
        exp_vals.append(_sum_gl_multi(company, EXPENSE_PREFIXES, first_day, last_day))

    profit_vals = [r - e for r, e in zip(rev_vals, exp_vals)]

    return {
        "labels": labels,
        "datasets": [
            {"name": "Doanh thu", "values": rev_vals},
            {"name": "Chi phí", "values": exp_vals},
            {"name": "Lợi nhuận", "values": profit_vals},
        ],
    }


# ---------------------------------------------------------------------------
# Chart 2: Cash Timeline (line)
# ---------------------------------------------------------------------------

def get_cash_timeline(company, from_date, to_date, granularity="month"):
    """Cash + bank cumulative balance — rolling periods, separate datasets."""
    periods = _build_periods(to_date, granularity)

    labels = [p[2] for p in periods]
    cash_vals = [_balance_gl_prefix(company, CASH_PREFIX, last_day) for _, last_day, _ in periods]
    bank_vals = [_balance_gl_prefix(company, BANK_PREFIX, last_day) for _, last_day, _ in periods]

    return {
        "labels": labels,
        "datasets": [
            {"name": "Tiền mặt", "values": cash_vals},
            {"name": "Ngân hàng", "values": bank_vals},
        ],
    }


# ---------------------------------------------------------------------------
# Chart 3: AR by Customer (donut)
# ---------------------------------------------------------------------------

def get_ar_donut(company):
    """Top 4 customers by outstanding + Khác."""
    data = frappe.db.sql(
        """
        SELECT customer AS name, SUM(outstanding_amount) AS total
        FROM `tabSales Invoice`
        WHERE docstatus = 1 AND outstanding_amount > 0 AND company = %(company)s
        GROUP BY customer
        ORDER BY total DESC
        """,
        {"company": company},
        as_dict=True,
    )
    return _top_n_donut(data)


# ---------------------------------------------------------------------------
# Chart 4: AP by Supplier (donut)
# ---------------------------------------------------------------------------

def get_ap_donut(company):
    """Top 4 suppliers by outstanding + Khác."""
    data = frappe.db.sql(
        """
        SELECT supplier AS name, SUM(outstanding_amount) AS total
        FROM `tabPurchase Invoice`
        WHERE docstatus = 1 AND outstanding_amount > 0 AND company = %(company)s
        GROUP BY supplier
        ORDER BY total DESC
        """,
        {"company": company},
        as_dict=True,
    )
    return _top_n_donut(data)


# ---------------------------------------------------------------------------
# Chart 5: Revenue by Item Group (donut)
# ---------------------------------------------------------------------------

def get_revenue_by_item_group(company, from_date, to_date):
    """Top 4 item groups by revenue + Khác."""
    data = frappe.db.sql(
        """
        SELECT COALESCE(sii.item_group, 'Không phân loại') AS name, SUM(sii.amount) AS total
        FROM `tabSales Invoice Item` sii
        JOIN `tabSales Invoice` si ON sii.parent = si.name
        WHERE si.docstatus = 1
          AND si.company = %(company)s
          AND si.posting_date BETWEEN %(from_date)s AND %(to_date)s
        GROUP BY COALESCE(sii.item_group, 'Không phân loại')
        ORDER BY total DESC
        """,
        {"company": company, "from_date": from_date, "to_date": to_date},
        as_dict=True,
    )
    return _top_n_donut(data)


# ---------------------------------------------------------------------------
# Chart 6: Expense by Type (donut)
# ---------------------------------------------------------------------------

def get_expense_by_type(company, from_date, to_date):
    """Group GL expenses by account prefix into categories."""
    categories = [
        ("641%", "Chi phí bán hàng"),
        ("642%", "Chi phí quản lý"),
        ("632%", "Giá vốn hàng bán"),
    ]

    results = []
    other_total = 0

    for prefix, label in categories:
        val = _sum_gl_multi(company, (prefix,), from_date, to_date)
        if val:
            results.append({"name": label, "total": val})

    other_prefixes = tuple(p for p in EXPENSE_PREFIXES if p not in ("641%", "642%", "632%"))
    if other_prefixes:
        other_total = _sum_gl_multi(company, other_prefixes, from_date, to_date)

    if not results and not other_total:
        return {"labels": [], "datasets": [{"values": []}]}

    labels = [r["name"] for r in results]
    values = [abs(float(r["total"])) for r in results]

    if other_total:
        labels.append("Khác")
        values.append(abs(float(other_total)))

    return {"labels": labels, "datasets": [{"values": values}]}


# ---------------------------------------------------------------------------
# Chart 7: Top 5 Customers by Revenue (bar)
# ---------------------------------------------------------------------------

def get_top_customers_revenue(company, from_date, to_date):
    """Top 5 customers by revenue in period."""
    data = frappe.db.sql(
        """
        SELECT customer AS name, SUM(grand_total) AS total
        FROM `tabSales Invoice`
        WHERE docstatus = 1
          AND company = %(company)s
          AND posting_date BETWEEN %(from_date)s AND %(to_date)s
        GROUP BY customer
        ORDER BY total DESC
        LIMIT 5
        """,
        {"company": company, "from_date": from_date, "to_date": to_date},
        as_dict=True,
    )
    if not data:
        return {"labels": [], "datasets": [{"name": "Doanh thu", "values": []}]}

    return {
        "labels": [d.name for d in data],
        "datasets": [{"name": "Doanh thu", "values": [float(d.total) for d in data]}],
    }


# ---------------------------------------------------------------------------
# Chart 8: AR Aging (bar)
# ---------------------------------------------------------------------------

def get_ar_aging(company):
    """AR aging buckets from Sales Invoice outstanding."""
    today = getdate(nowdate())
    data = frappe.db.sql(
        """
        SELECT due_date, outstanding_amount
        FROM `tabSales Invoice`
        WHERE docstatus = 1
          AND outstanding_amount > 0
          AND company = %(company)s
        """,
        {"company": company},
        as_dict=True,
    )

    buckets = [0, 0, 0, 0]  # 0-30, 31-60, 61-90, >90
    for row in data:
        if not row.due_date:
            buckets[3] += float(row.outstanding_amount)
            continue
        days = (today - getdate(row.due_date)).days
        if days < 0:
            days = 0
        if days <= 30:
            buckets[0] += float(row.outstanding_amount)
        elif days <= 60:
            buckets[1] += float(row.outstanding_amount)
        elif days <= 90:
            buckets[2] += float(row.outstanding_amount)
        else:
            buckets[3] += float(row.outstanding_amount)

    return {
        "labels": ["0-30 ngày", "31-60 ngày", "61-90 ngày", ">90 ngày"],
        "datasets": [{"name": "Công nợ", "values": buckets}],
    }


def get_cash_flow_forecast_chart(company, months=12):
    """Simplified forecast chart data for Dashboard v2. Committed only."""
    from vn_accounting.api.forecast import get_forecast_chart
    return get_forecast_chart(company=company, months=months)
