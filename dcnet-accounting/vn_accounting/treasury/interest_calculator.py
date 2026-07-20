"""Pure functions for term deposit interest schedule calculation.

All functions are stateless — no Frappe imports, no DB calls.
Day-count convention: actual/365 (VN banking standard).
"""
from __future__ import annotations

from datetime import date
from dateutil.relativedelta import relativedelta


def build_interest_schedule(
    principal: float,
    rate: float,
    interest_type: str,
    start_date: date,
    term_months: int,
) -> list[dict]:
    """Build interest schedule rows for a term deposit.

    Args:
        principal: Deposit amount (VND).
        rate: Annual interest rate (percent, e.g. 6.0 = 6%).
        interest_type: One of "End of Term", "Monthly", "Quarterly", "Prepaid", "Compound".
        start_date: Deposit start date.
        term_months: Term length in months.

    Returns:
        List of dicts with keys: due_date, interest_amount, principal_at_start.
    """
    maturity_date = start_date + relativedelta(months=term_months)
    builders = {
        "End of Term": _build_end_of_term,
        "Monthly": _build_periodic,
        "Quarterly": _build_periodic,
        "Prepaid": _build_prepaid,
        "Compound": _build_compound,
    }
    builder = builders.get(interest_type)
    if not builder:
        raise ValueError(f"Unknown interest_type: {interest_type}")

    if interest_type == "Monthly":
        return builder(principal, rate, start_date, maturity_date, period_months=1)
    elif interest_type == "Quarterly":
        return builder(principal, rate, start_date, maturity_date, period_months=3)
    else:
        return builder(principal, rate, start_date, maturity_date, term_months=term_months)


def _build_end_of_term(
    principal: float, rate: float, start_date: date, maturity_date: date, **kwargs
) -> list[dict]:
    days = (maturity_date - start_date).days
    interest = principal * (rate / 100) * days / 365
    return [{"due_date": maturity_date, "interest_amount": round(interest, 2), "principal_at_start": principal}]


def _build_periodic(
    principal: float, rate: float, start_date: date, maturity_date: date, period_months: int = 1, **kwargs
) -> list[dict]:
    rows = []
    period_start = start_date
    while True:
        period_end = period_start + relativedelta(months=period_months)
        if period_end > maturity_date:
            period_end = maturity_date
        if period_end <= period_start:
            break
        days = (period_end - period_start).days
        interest = principal * (rate / 100) * days / 365
        rows.append({
            "due_date": period_end,
            "interest_amount": round(interest, 2),
            "principal_at_start": principal,
        })
        if period_end >= maturity_date:
            break
        period_start = period_end
    return rows


def _build_prepaid(
    principal: float, rate: float, start_date: date, maturity_date: date, term_months: int = 0, **kwargs
) -> list[dict]:
    days = (maturity_date - start_date).days
    interest = principal * (rate / 100) * days / 365
    return [{"due_date": start_date, "interest_amount": round(interest, 2), "principal_at_start": principal}]


def _build_compound(
    principal: float, rate: float, start_date: date, maturity_date: date, **kwargs
) -> list[dict]:
    rows = []
    current_principal = principal
    period_start = start_date
    while True:
        period_end = period_start + relativedelta(months=1)
        if period_end > maturity_date:
            period_end = maturity_date
        if period_end <= period_start:
            break
        days = (period_end - period_start).days
        interest = current_principal * (rate / 100) * days / 365
        rows.append({
            "due_date": period_end,
            "interest_amount": round(interest, 2),
            "principal_at_start": round(current_principal, 2),
        })
        current_principal = round(current_principal + interest, 2)
        if period_end >= maturity_date:
            break
        period_start = period_end
    return rows


def calculate_accrued_interest(
    principal: float, rate: float, last_interest_date: date, accrual_date: date
) -> float:
    """Calculate accrued interest from last_interest_date to accrual_date."""
    days = (accrual_date - last_interest_date).days
    if days <= 0:
        return 0.0
    return round(principal * (rate / 100) * days / 365, 2)


def calculate_early_settlement_interest(
    principal: float,
    original_rate: float,
    early_rate: float,
    start_date: date,
    settlement_date: date,
    interest_already_paid: float,
) -> dict:
    """Calculate interest for early settlement of a term deposit.

    Returns dict with:
        interest_entitled: Total interest at early_rate for actual days held.
        adjustment: interest_entitled - interest_already_paid (can be negative).
    """
    days = (settlement_date - start_date).days
    interest_entitled = principal * (early_rate / 100) * days / 365
    return {
        "interest_entitled": round(interest_entitled, 2),
        "adjustment": round(interest_entitled - interest_already_paid, 2),
    }
