"""Tax obligations forecast provider.

Projects future tax payments from GL history:
- VAT (TK 33311): monthly, due 20th of following month
- CIT (TK 3334): quarterly, due 30th of Q+1 first month
- PIT (TK 3335): monthly, due 20th of following month
"""
import frappe
from datetime import date


def get_tax_forecast(filters):
    company = filters.get("company")
    from_date = filters.get("from_date")
    to_date = filters.get("to_date")
    if not company or not from_date or not to_date:
        return []

    entries = []
    entries.extend(_project_vat(company, from_date, to_date))
    entries.extend(_project_cit(company, from_date, to_date))
    entries.extend(_project_pit(company, from_date, to_date))
    return entries


def _get_monthly_median(company, account_prefix, months=3):
    """Get median monthly credit balance for a tax account."""
    rows = frappe.db.sql("""
        SELECT YEAR(posting_date) as yr, MONTH(posting_date) as mn,
               SUM(credit) - SUM(debit) as balance
        FROM `tabGL Entry`
        WHERE company = %(company)s
          AND is_cancelled = 0
          AND account LIKE %(prefix)s
          AND posting_date >= DATE_SUB(CURDATE(), INTERVAL %(months)s MONTH)
        GROUP BY yr, mn ORDER BY yr, mn
    """, {"company": company, "prefix": account_prefix, "months": months}, as_dict=True)

    if not rows:
        return 0

    values = sorted([float(r.balance) for r in rows if r.balance and float(r.balance) > 0])
    if not values:
        return 0
    return values[len(values) // 2]


def _project_vat(company, from_date, to_date):
    """VAT: monthly, due 20th of following month."""
    median = _get_monthly_median(company, "33311%")
    if median <= 0:
        return []

    entries = []
    current = date.fromisoformat(from_date).replace(day=1)
    end = date.fromisoformat(to_date)

    while current <= end:
        due = current.replace(day=20)
        due_str = str(due)
        if from_date <= due_str <= to_date:
            entries.append({
                "expected_date": due_str,
                "amount": median,
                "direction": "outflow",
                "category": "VAT Payment",
                "confidence": "possible",
                "source_doctype": "Company",
                "source_name": company,
                "description": f"VAT - T{current.month}/{current.year}",
            })

        if current.month == 12:
            current = current.replace(year=current.year + 1, month=1)
        else:
            current = current.replace(month=current.month + 1)

    return entries


def _project_cit(company, from_date, to_date):
    """CIT: quarterly, due 30th of first month of next quarter."""
    # Last year total from GL
    last_year_total = frappe.db.sql("""
        SELECT COALESCE(SUM(credit) - SUM(debit), 0) as total
        FROM `tabGL Entry`
        WHERE company = %(company)s
          AND is_cancelled = 0
          AND account LIKE '3334%%'
          AND posting_date >= DATE_SUB(CURDATE(), INTERVAL 12 MONTH)
    """, {"company": company}, as_dict=True)

    yearly = float(last_year_total[0].total) if last_year_total else 0
    quarterly = yearly / 4
    if quarterly <= 0:
        return []

    entries = []
    # Quarter end months: 3, 6, 9, 12 → due 30th of next month
    quarter_due_months = {3: 4, 6: 7, 9: 10, 12: 1}
    current = date.fromisoformat(from_date).replace(day=1)
    end = date.fromisoformat(to_date)

    while current <= end:
        if current.month in quarter_due_months:
            due_month = quarter_due_months[current.month]
            due_year = current.year + (1 if current.month == 12 else 0)
            due = date(due_year, due_month, 30)
            due_str = str(due)
            if from_date <= due_str <= to_date:
                entries.append({
                    "expected_date": due_str,
                    "amount": quarterly,
                    "direction": "outflow",
                    "category": "Corporate Income Tax",
                    "confidence": "possible",
                    "source_doctype": "Company",
                    "source_name": company,
                    "description": f"CIT Q{(current.month - 1) // 3 + 1}/{current.year}",
                })

        if current.month == 12:
            current = current.replace(year=current.year + 1, month=1)
        else:
            current = current.replace(month=current.month + 1)

    return entries


def _project_pit(company, from_date, to_date):
    """PIT: monthly, due 20th of following month."""
    median = _get_monthly_median(company, "3335%")
    if median <= 0:
        return []

    entries = []
    current = date.fromisoformat(from_date).replace(day=1)
    end = date.fromisoformat(to_date)

    while current <= end:
        due = current.replace(day=20)
        due_str = str(due)
        if from_date <= due_str <= to_date:
            entries.append({
                "expected_date": due_str,
                "amount": median,
                "direction": "outflow",
                "category": "Personal Income Tax",
                "confidence": "possible",
                "source_doctype": "Company",
                "source_name": company,
                "description": f"PIT - T{current.month}/{current.year}",
            })

        if current.month == 12:
            current = current.replace(year=current.year + 1, month=1)
        else:
            current = current.replace(month=current.month + 1)

    return entries
