"""Historical OpEx projection provider.

Analyzes 12-month GL history for TK 6xx accounts (excluding payroll TK 642x)
to identify recurring expenses and project them forward.
"""
import frappe
from datetime import date
from collections import defaultdict
from statistics import median


def get_opex_forecast(filters):
    company = filters.get("company")
    from_date = filters.get("from_date")
    to_date = filters.get("to_date")
    if not company or not from_date or not to_date:
        return []

    # Query 12-month history for expense accounts (6xx), exclude payroll (642x)
    rows = frappe.db.sql("""
        SELECT account,
               YEAR(posting_date) as yr, MONTH(posting_date) as mn,
               SUM(debit) - SUM(credit) as total
        FROM `tabGL Entry`
        WHERE company = %(company)s
          AND is_cancelled = 0
          AND account LIKE '6%%'
          AND account NOT LIKE '642%%'
          AND posting_date >= DATE_SUB(CURDATE(), INTERVAL 12 MONTH)
        GROUP BY account, yr, mn
        ORDER BY account, yr, mn
    """, {"company": company}, as_dict=True)

    if not rows:
        return []

    # Group by account
    account_data = defaultdict(list)
    account_names = {}
    for r in rows:
        if r.total and float(r.total) > 0:
            account_data[r.account].append({
                "year": r.yr, "month": r.mn,
                "amount": float(r.total),
            })
            account_names[r.account] = r.account

    # Determine history months
    all_months = set()
    for r in rows:
        all_months.add((r.yr, r.mn))
    total_history_months = len(all_months)

    # Minimum recurring threshold
    if total_history_months >= 12:
        min_months = 8
    elif total_history_months >= 6:
        min_months = 4
    else:
        return []  # Not enough history

    entries = []
    for account, monthly_data in account_data.items():
        if len(monthly_data) < min_months:
            continue

        amounts = [m["amount"] for m in monthly_data]
        med = median(amounts)
        cap = med * 2

        # Build month→amount lookup for same-month-last-year
        month_lookup = {}
        for m in monthly_data:
            month_lookup[(m["year"], m["month"])] = m["amount"]

        account_name = account_names.get(account, account)
        entries.extend(
            _project_account(account, account_name, med, cap, month_lookup,
                             from_date, to_date, company)
        )

    return entries


def _project_account(account, account_name, med, cap, month_lookup,
                     from_date, to_date, company):
    """Project a single recurring expense account into future months."""
    entries = []
    current = date.fromisoformat(from_date).replace(day=1)
    end = date.fromisoformat(to_date)
    last_year = date.today().year - 1

    while current <= end:
        # Same-month-last-year if available, else median
        same_month = month_lookup.get((last_year, current.month))
        projected = same_month if same_month else med
        projected = min(projected, cap)  # Cap at 2× median

        if projected <= 0:
            if current.month == 12:
                current = current.replace(year=current.year + 1, month=1)
            else:
                current = current.replace(month=current.month + 1)
            continue

        exp_date = current.replace(day=15)  # Mid-month estimate
        exp_str = str(exp_date)
        if from_date <= exp_str <= to_date:
            entries.append({
                "expected_date": exp_str,
                "amount": projected,
                "direction": "outflow",
                "category": f"Projected OpEx: {account_name}",
                "confidence": "possible",
                "source_doctype": "Account",
                "source_name": account,
                "description": f"{account_name} - T{current.month}/{current.year}",
            })

        if current.month == 12:
            current = current.replace(year=current.year + 1, month=1)
        else:
            current = current.replace(month=current.month + 1)

    return entries
