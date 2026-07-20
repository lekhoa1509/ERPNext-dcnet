"""Payroll & Social Insurance forecast providers.

Payroll strategy:
1. If HRMS installed → use last submitted Payroll Entry net_pay, project monthly
2. Fallback → query GL for TK 334 (payroll payable), median of past 3 months

Social Insurance strategy:
- Query GL for TK 3383 (BHXH) + 3384 (BHYT) + 3386 (BHTN) payable accounts
- Use median of past 6 months as projection
- Separate from payroll because insurance has its own payment schedule (20th)
"""
import frappe
from datetime import date
from statistics import median as calc_median


def get_payroll_forecast(filters):
    """Salary payment forecast."""
    company = filters.get("company")
    from_date = filters.get("from_date")
    to_date = filters.get("to_date")
    if not company or not from_date or not to_date:
        return []

    if "hrms" in frappe.get_installed_apps():
        entries = _from_payroll_entry(company, from_date, to_date)
        if entries:
            return entries
    return _from_gl_salary(company, from_date, to_date)


def get_insurance_forecast(filters):
    """Social insurance forecast from GL accounts 3383/3384/3386."""
    company = filters.get("company")
    from_date = filters.get("from_date")
    to_date = filters.get("to_date")
    if not company or not from_date or not to_date:
        return []

    return _from_gl_insurance(company, from_date, to_date)


def _from_payroll_entry(company, from_date, to_date):
    """Project from last submitted Payroll Entry."""
    last_pe = frappe.db.sql("""
        SELECT pe.name, pe.posting_date,
               IFNULL(SUM(ss.net_pay), 0) as total_net_pay
        FROM `tabPayroll Entry` pe
        LEFT JOIN `tabSalary Slip` ss ON ss.payroll_entry = pe.name AND ss.docstatus = 1
        WHERE pe.company = %(company)s AND pe.docstatus = 1
        GROUP BY pe.name, pe.posting_date
        ORDER BY pe.posting_date DESC LIMIT 1
    """, {"company": company}, as_dict=True)

    if not last_pe or float(last_pe[0].total_net_pay) <= 0:
        return []

    monthly_salary = float(last_pe[0].total_net_pay)
    return _project_salary(monthly_salary, from_date, to_date, "probable", company)


def _from_gl_salary(company, from_date, to_date):
    """Project salary from GL TK 334 (payroll payable) only."""
    rows = frappe.db.sql("""
        SELECT YEAR(posting_date) as yr, MONTH(posting_date) as mn,
               SUM(credit) - SUM(debit) as total
        FROM `tabGL Entry`
        WHERE company = %(company)s
          AND is_cancelled = 0
          AND account LIKE '334%%'
          AND posting_date >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
        GROUP BY yr, mn ORDER BY yr, mn
    """, {"company": company}, as_dict=True)

    totals = [float(r.total) for r in rows if r.total and float(r.total) > 0]
    if not totals:
        return []

    monthly_salary = calc_median(totals)
    return _project_salary(monthly_salary, from_date, to_date, "possible", company)


def _from_gl_insurance(company, from_date, to_date):
    """Project insurance from GL TK 3383 + 3384 + 3386."""
    rows = frappe.db.sql("""
        SELECT YEAR(posting_date) as yr, MONTH(posting_date) as mn,
               SUM(credit) - SUM(debit) as total
        FROM `tabGL Entry`
        WHERE company = %(company)s
          AND is_cancelled = 0
          AND (account LIKE '3383%%' OR account LIKE '3384%%'
               OR account LIKE '3386%%')
          AND posting_date >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
        GROUP BY yr, mn ORDER BY yr, mn
    """, {"company": company}, as_dict=True)

    totals = [float(r.total) for r in rows if r.total and float(r.total) > 0]
    if not totals:
        return []

    monthly_insurance = calc_median(totals)
    return _project_insurance(monthly_insurance, from_date, to_date, company)


def _project_salary(monthly_amount, from_date, to_date, confidence, company):
    """Generate monthly salary entries on 5th of each month."""
    entries = []
    current = date.fromisoformat(from_date).replace(day=1)
    end = date.fromisoformat(to_date)

    while current <= end:
        salary_date = current.replace(day=5)
        salary_str = str(salary_date)
        if from_date <= salary_str <= to_date:
            entries.append({
                "expected_date": salary_str,
                "amount": monthly_amount,
                "direction": "outflow",
                "category": "Payroll",
                "confidence": confidence,
                "source_doctype": "Company",
                "source_name": company,
                "description": f"Payroll - {current.strftime('%m/%Y')}",
            })
        current = _next_month(current)

    return entries


def _project_insurance(monthly_amount, from_date, to_date, company):
    """Generate monthly insurance entries on 20th of each month."""
    entries = []
    current = date.fromisoformat(from_date).replace(day=1)
    end = date.fromisoformat(to_date)

    while current <= end:
        ins_date = current.replace(day=20)
        ins_str = str(ins_date)
        if from_date <= ins_str <= to_date:
            entries.append({
                "expected_date": ins_str,
                "amount": monthly_amount,
                "direction": "outflow",
                "category": "Social Insurance",
                "confidence": "possible",
                "source_doctype": "Company",
                "source_name": company,
                "description": f"Insurance - {current.strftime('%m/%Y')}",
            })
        current = _next_month(current)

    return entries


def _next_month(d):
    if d.month == 12:
        return d.replace(year=d.year + 1, month=1)
    return d.replace(month=d.month + 1)
