"""Pure functions for bank loan repayment schedule calculation.

Stateless — no Frappe imports, no DB calls.
Day-count: actual/365 for all calculations (VN banking standard).
"""
from __future__ import annotations

from datetime import date
from dateutil.relativedelta import relativedelta


def build_repayment_schedule(
    loan_amount: float,
    rate: float,
    repayment_type: str,
    frequency: str,
    start_date: date,
    maturity_date: date,
) -> list[dict]:
    """Build repayment schedule for a bank loan.

    Args:
        loan_amount: Total loan amount.
        rate: Annual interest rate (percent).
        repayment_type: "Interest Only" or "EMI".
        frequency: "Monthly" or "Quarterly".
        start_date: Disbursement date.
        maturity_date: Loan maturity date.

    Returns:
        List of dicts: due_date, principal_amount, interest_amount,
        total_amount, outstanding_after.
    """
    period_months = 1 if frequency == "Monthly" else 3

    if repayment_type == "Interest Only":
        return _build_interest_only(loan_amount, rate, start_date, maturity_date, period_months)
    elif repayment_type == "EMI":
        return _build_emi(loan_amount, rate, start_date, maturity_date, period_months)
    else:
        raise ValueError(f"Unknown repayment_type: {repayment_type}")


def _build_interest_only(
    loan_amount: float, rate: float, start_date: date, maturity_date: date, period_months: int
) -> list[dict]:
    rows = []
    outstanding = loan_amount
    period_start = start_date

    periods = []
    while True:
        period_end = period_start + relativedelta(months=period_months)
        if period_end > maturity_date:
            period_end = maturity_date
        if period_end <= period_start:
            break
        periods.append((period_start, period_end))
        if period_end >= maturity_date:
            break
        period_start = period_end

    for i, (p_start, p_end) in enumerate(periods):
        days = (p_end - p_start).days
        interest = outstanding * (rate / 100) * days / 365
        is_last = i == len(periods) - 1
        principal = loan_amount if is_last else 0
        outstanding_after = 0 if is_last else outstanding

        rows.append({
            "due_date": p_end,
            "principal_amount": round(principal, 2),
            "interest_amount": round(interest, 2),
            "total_amount": round(principal + interest, 2),
            "outstanding_after": round(outstanding_after, 2),
        })
    return rows


def _build_emi(
    loan_amount: float, rate: float, start_date: date, maturity_date: date, period_months: int
) -> list[dict]:
    periods = []
    period_start = start_date
    while True:
        period_end = period_start + relativedelta(months=period_months)
        if period_end > maturity_date:
            period_end = maturity_date
        if period_end <= period_start:
            break
        periods.append((period_start, period_end))
        if period_end >= maturity_date:
            break
        period_start = period_end

    n = len(periods)
    if n == 0:
        return []

    # EMI formula uses average periodic rate for stable payment amount
    total_days = (maturity_date - start_date).days
    avg_days = total_days / n
    avg_rate = (rate / 100) * avg_days / 365
    if avg_rate == 0:
        emi = loan_amount / n
    else:
        emi = loan_amount * avg_rate / (1 - (1 + avg_rate) ** (-n))

    rows = []
    outstanding = loan_amount

    for i, (p_start, p_end) in enumerate(periods):
        # Per-period interest uses actual/365 (VN banking standard)
        days = (p_end - p_start).days
        interest = outstanding * (rate / 100) * days / 365
        is_last = i == n - 1

        if is_last:
            principal = outstanding
            total = principal + interest
        else:
            principal = emi - interest
            total = emi

        outstanding -= principal
        rows.append({
            "due_date": p_end,
            "principal_amount": round(principal, 2),
            "interest_amount": round(interest, 2),
            "total_amount": round(total, 2),
            "outstanding_after": round(max(outstanding, 0), 2),
        })

    return rows
