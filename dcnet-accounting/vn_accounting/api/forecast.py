"""Forecast API endpoints for the Cash Flow Forecast page and Dashboard v2."""
import frappe
from datetime import date, timedelta
from collections import defaultdict
from datetime import datetime

from vn_accounting.forecast.aggregator import get_all_forecast_entries
from vn_accounting.forecast.payment_delay import clear_delay_cache
from vn_accounting.api.dashboard import _balance_gl


CONFIDENCE_ORDER = {"overdue": 0, "committed": 1, "probable": 2, "possible": 3}


@frappe.whitelist()
def get_forecast_data(company=None, months=12, history_months=0, granularity="monthly"):
    """Summary API — returns aggregated monthly/weekly cells, NO individual entries.

    Individual entries are cached in Redis for the drill-down API.
    Client uses cells to compute chart/table for any combination of source + confidence filters.
    """
    if not company:
        company = frappe.defaults.get_user_default("Company")

    period = int(months)
    history_months = int(history_months)
    today = date.today()
    from_date = today.strftime("%Y-%m-%d")

    if granularity == "weekly":
        to_date = (today + timedelta(days=period * 7)).strftime("%Y-%m-%d")
    else:
        to_date = (today + timedelta(days=period * 30)).strftime("%Y-%m-%d")

    clear_delay_cache()

    entries, errors = get_all_forecast_entries({
        "company": company,
        "from_date": from_date,
        "to_date": to_date,
    })

    # Cache entries for drill-down API (5 min TTL)
    cache_key = f"forecast:{company}:{from_date}:{to_date}"
    frappe.cache.set_value(cache_key, entries, expires_in_sec=300)

    # Aggregate entries into cells: period_key → source → confidence → {inflow, outflow, count}
    cells = {}
    for e in entries:
        if granularity == "weekly":
            d = datetime.strptime(e["expected_date"], "%Y-%m-%d")
            iso_y, iso_w, _ = d.isocalendar()
            pkey = f"{iso_y}-W{iso_w:02d}"
        else:
            pkey = e["expected_date"][:7]

        src = e.get("source_doctype", "Other")
        conf = e.get("confidence", "possible")

        cell = cells.setdefault(pkey, {}).setdefault(src, {}).setdefault(conf, {"inflow": 0, "outflow": 0, "count": 0})
        if e["direction"] == "inflow":
            cell["inflow"] += e["amount"]
        else:
            cell["outflow"] += e["amount"]
        cell["count"] += 1

    # Opening balance: TK 111 + 112 + 113
    opening = (
        _balance_gl(company, "111%")
        + _balance_gl(company, "112%")
        + _balance_gl(company, "113%")
    )

    threshold = frappe.db.get_single_value(
        "VN Accounting Settings", "minimum_cash_threshold"
    ) or 500000000

    sources = sorted(set(e["source_doctype"] for e in entries))

    # Historical actual cash flow from GL
    if history_months > 0:
        if granularity == "weekly":
            historical = _get_historical_weeks(company, history_months)
        else:
            historical = _get_historical_months(company, history_months)
    else:
        historical = []

    return {
        "cells": cells,
        "errors": errors,
        "opening_balance": float(opening),
        "minimum_threshold": float(threshold),
        "sources": sources,
        "historical": historical,
        "granularity": granularity,
        "from_date": from_date,
        "to_date": to_date,
    }



@frappe.whitelist()
def get_forecast_chart(company=None, months=12):
    """Simplified API for Dashboard v2 chart. Committed only, monthly."""
    if not company:
        company = frappe.defaults.get_user_default("Company")

    months = int(months)
    today = date.today()
    from_date = today.strftime("%Y-%m-%d")
    to_date = (today + timedelta(days=months * 30)).strftime("%Y-%m-%d")

    clear_delay_cache()

    entries, _ = get_all_forecast_entries({
        "company": company,
        "from_date": from_date,
        "to_date": to_date,
        "confidence": ["committed"],
    })

    opening = (
        _balance_gl(company, "111%")
        + _balance_gl(company, "112%")
        + _balance_gl(company, "113%")
    )

    monthly = _group_by_month(entries, from_date, to_date, float(opening))

    # Short labels for dashboard (T4 instead of T4/2026) — fits narrow chart container
    short_labels = [m["label"].split("/")[0] for m in monthly]

    return {
        "labels": short_labels,
        "datasets": {
            "inflow": [m["inflow"] for m in monthly],
            "outflow": [m["outflow"] for m in monthly],
            "balance": [m["closing"] for m in monthly],
        },
    }


@frappe.whitelist()
def export_forecast_excel(company=None, months=12, history_months=0):
    """Export forecast summary as XLSX file."""
    from frappe.utils.xlsxutils import make_xlsx

    if not company:
        company = frappe.defaults.get_user_default("Company")

    months = int(months)
    history_months = int(history_months)
    today = date.today()
    from_date = today.strftime("%Y-%m-%d")
    to_date = (today + timedelta(days=months * 30)).strftime("%Y-%m-%d")

    clear_delay_cache()
    entries, _ = get_all_forecast_entries({
        "company": company,
        "from_date": from_date,
        "to_date": to_date,
    })

    opening = float(
        _balance_gl(company, "111%")
        + _balance_gl(company, "112%")
        + _balance_gl(company, "113%")
    )

    forecast_monthly = _group_by_month(entries, from_date, to_date, opening)
    historical = _get_historical_months(company, history_months) if history_months > 0 else []

    headers = ["Period", "Type", "Opening Balance", "Inflow", "Outflow", "Net", "Closing Balance"]
    data = [headers]

    for h in historical:
        month_num = int(h["month"].split("-")[1])
        year = h["month"].split("-")[0]
        net = h["inflow"] - h["outflow"]
        data.append([
            f"T{month_num}/{year}", "Actual",
            h["opening"], h["inflow"], h["outflow"], net, h["closing"],
        ])

    for m in forecast_monthly:
        data.append([
            m["label"], "Forecast",
            m["opening"], m["inflow"], m["outflow"], m["net"], m["closing"],
        ])

    xlsx_file = make_xlsx(data, "Cash Flow Forecast")

    frappe.response["filename"] = "cash_flow_forecast.xlsx"
    frappe.response["filecontent"] = xlsx_file.getvalue()
    frappe.response["type"] = "binary"


def _get_historical_months(company, num_months):
    """Get actual cash flow from GL for the past num_months complete months."""
    if not num_months or num_months <= 0:
        return []

    today = date.today()
    first_of_this_month = today.replace(day=1)

    # Walk back num_months from first_of_this_month
    start = first_of_this_month
    for _ in range(num_months):
        start = (start - timedelta(days=1)).replace(day=1)

    # Opening balance as of day before start
    opening = _balance_gl_at(company, (start - timedelta(days=1)).strftime("%Y-%m-%d"))

    # Monthly debits/credits on cash accounts (TK 111+112+113)
    data = frappe.db.sql("""
        SELECT
            DATE_FORMAT(posting_date, '%%Y-%%m') as month_key,
            SUM(debit) as total_debit,
            SUM(credit) as total_credit
        FROM `tabGL Entry`
        WHERE company = %(company)s
            AND posting_date >= %(start)s
            AND posting_date < %(end)s
            AND (account LIKE '111%%' OR account LIKE '112%%' OR account LIKE '113%%')
            AND is_cancelled = 0
        GROUP BY month_key
        ORDER BY month_key
    """, {
        "company": company,
        "start": start.strftime("%Y-%m-%d"),
        "end": first_of_this_month.strftime("%Y-%m-%d"),
    }, as_dict=True)

    monthly_data = {d.month_key: d for d in data}
    result = []
    balance = float(opening)

    current = start
    while current < first_of_this_month:
        key = current.strftime("%Y-%m")
        d = monthly_data.get(key, frappe._dict(total_debit=0, total_credit=0))
        inflow = float(d.total_debit or 0)
        outflow = float(d.total_credit or 0)
        closing = balance + inflow - outflow
        result.append({
            "month": key,
            "inflow": inflow,
            "outflow": outflow,
            "opening": balance,
            "closing": closing,
        })
        balance = closing
        if current.month == 12:
            current = current.replace(year=current.year + 1, month=1)
        else:
            current = current.replace(month=current.month + 1)

    return result


def _get_historical_weeks(company, num_weeks):
    """Get actual cash flow from GL for the past num_weeks complete weeks (Mon-Sun)."""
    if not num_weeks or num_weeks <= 0:
        return []

    today = date.today()
    # Current week's Monday
    this_monday = today - timedelta(days=today.weekday())

    # Start = num_weeks ago Monday
    start = this_monday - timedelta(weeks=num_weeks)

    opening = _balance_gl_at(company, (start - timedelta(days=1)).strftime("%Y-%m-%d"))

    # Weekly debits/credits on cash accounts, grouped by ISO year-week
    data = frappe.db.sql("""
        SELECT
            CONCAT(YEAR(posting_date), '-W', LPAD(WEEK(posting_date, 3), 2, '0')) as week_key,
            MIN(posting_date) as week_start,
            SUM(debit) as total_debit,
            SUM(credit) as total_credit
        FROM `tabGL Entry`
        WHERE company = %(company)s
            AND posting_date >= %(start)s
            AND posting_date < %(end)s
            AND (account LIKE '111%%' OR account LIKE '112%%' OR account LIKE '113%%')
            AND is_cancelled = 0
        GROUP BY week_key
        ORDER BY week_key
    """, {
        "company": company,
        "start": start.strftime("%Y-%m-%d"),
        "end": this_monday.strftime("%Y-%m-%d"),
    }, as_dict=True)

    weekly_data = {d.week_key: d for d in data}
    result = []
    balance = float(opening)

    current = start
    while current < this_monday:
        iso_year, iso_week, _ = current.isocalendar()
        key = f"{iso_year}-W{iso_week:02d}"
        d = weekly_data.get(key, frappe._dict(total_debit=0, total_credit=0))
        inflow = float(d.total_debit or 0)
        outflow = float(d.total_credit or 0)
        closing = balance + inflow - outflow
        result.append({
            "week": key,
            "week_start": current.strftime("%Y-%m-%d"),
            "inflow": inflow,
            "outflow": outflow,
            "opening": balance,
            "closing": closing,
        })
        balance = closing
        current += timedelta(weeks=1)

    return result


def _balance_gl_at(company, as_of_date):
    """GL balance of TK 111+112+113 as of a specific date."""
    result = frappe.db.sql("""
        SELECT COALESCE(SUM(debit) - SUM(credit), 0)
        FROM `tabGL Entry`
        WHERE company = %s
            AND (account LIKE '111%%' OR account LIKE '112%%' OR account LIKE '113%%')
            AND posting_date <= %s
            AND is_cancelled = 0
    """, (company, as_of_date))
    return float(result[0][0]) if result and result[0][0] else 0.0


def _group_by_month(entries, from_date, to_date, opening):
    """Group entries by YYYY-MM and compute rolling balance."""
    monthly_data = defaultdict(lambda: {"inflow": 0, "outflow": 0})

    for e in entries:
        month_key = e["expected_date"][:7]
        if e["direction"] == "inflow":
            monthly_data[month_key]["inflow"] += e["amount"]
        else:
            monthly_data[month_key]["outflow"] += e["amount"]

    # Build sorted month list
    start = datetime.strptime(from_date, "%Y-%m-%d")
    end = datetime.strptime(to_date, "%Y-%m-%d")
    months = []
    current = start.replace(day=1)
    while current <= end:
        key = current.strftime("%Y-%m")
        months.append(key)
        if current.month == 12:
            current = current.replace(year=current.year + 1, month=1)
        else:
            current = current.replace(month=current.month + 1)

    # Compute rolling balance
    result = []
    balance = opening
    for key in months:
        data = monthly_data.get(key, {"inflow": 0, "outflow": 0})
        net = data["inflow"] - data["outflow"]
        closing = balance + net
        month_num = int(key.split("-")[1])
        year = key.split("-")[0]
        result.append({
            "label": f"T{month_num}/{year}",
            "inflow": data["inflow"],
            "outflow": data["outflow"],
            "net": net,
            "opening": balance,
            "closing": closing,
        })
        balance = closing

    return result


def _filter_entries(entries, *, period_key, granularity, confidences, sources, search):
    """Pure filter: period_key (monthly YYYY-MM or weekly YYYY-Www), confidences, sources, search."""
    out = []
    search_lower = (search or "").strip().lower()
    conf_set = set(confidences) if confidences else None
    src_set = set(sources) if sources else None

    for e in entries:
        if conf_set and e["confidence"] not in conf_set:
            continue
        if src_set and e["source_doctype"] not in src_set:
            continue
        if period_key:
            if "W" in period_key:
                d = datetime.strptime(e["expected_date"], "%Y-%m-%d")
                iso_y, iso_w, _ = d.isocalendar()
                if f"{iso_y}-W{iso_w:02d}" != period_key:
                    continue
            else:
                if e["expected_date"][:7] != period_key:
                    continue
        if search_lower:
            haystack = " ".join([
                str(e.get("description", "")),
                str(e.get("source_name", "")),
                str(e.get("party", "")),
            ]).lower()
            if search_lower not in haystack:
                continue
        out.append(e)
    return out


def _compute_group_totals(entries):
    """Sum inflow/outflow + count by confidence across the FULL filtered set."""
    totals = {c: {"inflow": 0.0, "outflow": 0.0, "count": 0} for c in CONFIDENCE_ORDER}
    for e in entries:
        bucket = totals[e["confidence"]]
        if e["direction"] == "inflow":
            bucket["inflow"] += e["amount"]
        else:
            bucket["outflow"] += e["amount"]
        bucket["count"] += 1
    return totals


def _load_entries_with_cache(company, from_date, to_date):
    """Reuse the same cache key as get_forecast_data (TTL 300s)."""
    cache_key = f"forecast:{company}:{from_date}:{to_date}"
    cached = frappe.cache.get_value(cache_key)
    if cached is not None:
        return cached
    clear_delay_cache()
    entries, _errors = get_all_forecast_entries({
        "company": company,
        "from_date": from_date,
        "to_date": to_date,
    })
    frappe.cache.set_value(cache_key, entries, expires_in_sec=300)
    return entries


@frappe.whitelist()
def get_forecast_entries(
    company,
    from_date,
    to_date,
    granularity="monthly",
    period_key=None,
    confidences=None,
    sources=None,
    search="",
    page=1,
    page_size=20,
):
    """Return paginated forecast entries with confidence-group totals.

    Reuses the existing Redis cache populated by `get_forecast_data`.
    """
    page = int(page)
    page_size = int(page_size)
    if isinstance(confidences, str):
        confidences = frappe.parse_json(confidences) or None
    if isinstance(sources, str):
        sources = frappe.parse_json(sources) or None

    all_entries = _load_entries_with_cache(company, from_date, to_date)
    filtered = _filter_entries(
        all_entries,
        period_key=period_key,
        granularity=granularity,
        confidences=confidences,
        sources=sources,
        search=search or "",
    )
    filtered.sort(key=lambda e: (
        CONFIDENCE_ORDER.get(e["confidence"], 99),
        e["expected_date"],
    ))

    group_totals = _compute_group_totals(filtered)
    total = len(filtered)
    start = (page - 1) * page_size
    page_entries = filtered[start : start + page_size]

    return {
        "entries": page_entries,
        "group_totals": group_totals,
        "total": total,
        "page": page,
        "page_size": page_size,
    }
