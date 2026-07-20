"""Treasury forecast provider.

Generates forecast entries from:
- Term Deposits: interest income on interest dates + principal return on maturity
- Bank Loans: repayment outflows (monthly/quarterly) until maturity
"""
import frappe
from datetime import date, timedelta
import calendar


def get_treasury_forecast(filters):
    company = filters.get("company")
    from_date = filters.get("from_date")
    to_date = filters.get("to_date")
    if not company or not from_date or not to_date:
        return []

    entries = []
    entries.extend(_get_term_deposit_entries(company, from_date, to_date))
    entries.extend(_get_bank_loan_entries(company, from_date, to_date))
    return entries


def _get_term_deposit_entries(company, from_date, to_date):
    """Term deposits: interest income + principal return on maturity."""
    deposits = frappe.db.sql("""
        SELECT name, principal_amount, interest_rate, interest_type,
               start_date, maturity_date, total_interest, status
        FROM `tabTerm Deposit`
        WHERE company = %(company)s
          AND docstatus = 1
          AND status IN ('Active', 'active')
          AND maturity_date >= %(from_date)s
    """, {"company": company, "from_date": from_date}, as_dict=True)

    entries = []
    for dep in deposits:
        entries.extend(_deposit_cash_flows(dep, from_date, to_date))
    return entries


def _deposit_cash_flows(dep, from_date, to_date):
    entries = []
    maturity = str(dep.maturity_date)
    principal = float(dep.principal_amount or 0)
    total_interest = float(dep.total_interest or 0)

    # Principal return on maturity
    if from_date <= maturity <= to_date and principal > 0:
        entries.append({
            "expected_date": maturity,
            "amount": principal,
            "direction": "inflow",
            "category": "Term Deposit Maturity",
            "confidence": "committed",
            "source_doctype": "Term Deposit",
            "source_name": dep.name,
            "description": f"Term deposit maturity {dep.name}",
        })

    # Interest income — simple estimate: add on maturity date
    if from_date <= maturity <= to_date and total_interest > 0:
        entries.append({
            "expected_date": maturity,
            "amount": total_interest,
            "direction": "inflow",
            "category": "Interest Income",
            "confidence": "committed",
            "source_doctype": "Term Deposit",
            "source_name": dep.name,
            "description": f"Deposit interest {dep.name}",
        })

    return entries


def _get_bank_loan_entries(company, from_date, to_date):
    """Bank loans: repayment outflows."""
    loans = frappe.db.sql("""
        SELECT name, loan_amount, outstanding_amount, interest_rate,
               repayment_type, repayment_frequency, start_date, maturity_date,
               total_repayment, status
        FROM `tabBank Loan`
        WHERE company = %(company)s
          AND docstatus = 1
          AND status IN ('Active', 'active', 'Disbursed')
          AND maturity_date >= %(from_date)s
    """, {"company": company, "from_date": from_date}, as_dict=True)

    entries = []
    for loan in loans:
        entries.extend(_loan_cash_flows(loan, from_date, to_date))
    return entries


def _loan_cash_flows(loan, from_date, to_date):
    entries = []
    outstanding = float(loan.outstanding_amount or loan.loan_amount or 0)
    if outstanding <= 0:
        return []

    maturity = date.fromisoformat(str(loan.maturity_date))
    start = date.fromisoformat(str(loan.start_date))
    freq = (loan.repayment_frequency or "Monthly").lower()

    # Calculate period increment
    if "quarter" in freq:
        months_step = 3
    elif "annual" in freq or "year" in freq:
        months_step = 12
    else:
        months_step = 1  # Monthly default

    # Determine total periods and monthly payment
    today = date.today()
    total_months = (maturity.year - start.year) * 12 + (maturity.month - start.month)
    total_periods = max(1, total_months // months_step)
    total_repayment = float(loan.total_repayment or outstanding * 1.1)
    per_period = total_repayment / total_periods

    # Generate repayment dates
    current = start
    while current <= maturity:
        # Next repayment on same day of each period
        if months_step == 1:
            if current.month == 12:
                current = current.replace(year=current.year + 1, month=1)
            else:
                current = current.replace(month=current.month + 1)
        else:
            new_month = current.month + months_step
            new_year = current.year + (new_month - 1) // 12
            new_month = ((new_month - 1) % 12) + 1
            current = current.replace(year=new_year, month=new_month)

        if current > maturity:
            break

        exp_str = str(current)
        if from_date <= exp_str <= to_date:
            entries.append({
                "expected_date": exp_str,
                "amount": per_period,
                "direction": "outflow",
                "category": "Loan Repayment",
                "confidence": "committed",
                "source_doctype": "Bank Loan",
                "source_name": loan.name,
                "description": f"Loan repayment {loan.name}",
            })

    return entries
