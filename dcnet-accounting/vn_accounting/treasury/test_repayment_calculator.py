"""Tests for loan repayment schedule calculator.

Run: cd /home/long/long/frappe-bench-dcnet/apps/vn_accounting
     python -m pytest vn_accounting/treasury/test_repayment_calculator.py -v
"""
from datetime import date
from vn_accounting.treasury.repayment_calculator import build_repayment_schedule


def test_interest_only_monthly():
    """Interest Only + Monthly: interest each month, full principal last row."""
    rows = build_repayment_schedule(
        loan_amount=500_000_000,
        rate=10.0,
        repayment_type="Interest Only",
        frequency="Monthly",
        start_date=date(2026, 1, 1),
        maturity_date=date(2027, 1, 1),
    )
    assert len(rows) == 12
    # All rows except last: principal=0
    for r in rows[:-1]:
        assert r["principal_amount"] == 0
    # Last row: principal = full loan amount
    assert rows[-1]["principal_amount"] == 500_000_000
    # Outstanding after last row = 0
    assert rows[-1]["outstanding_after"] == 0
    # First row interest: 500M * 10% * 31/365
    expected_first_interest = 500_000_000 * 0.10 * 31 / 365
    assert abs(rows[0]["interest_amount"] - expected_first_interest) < 1


def test_interest_only_quarterly():
    """Interest Only + Quarterly: 4 rows for 12 months."""
    rows = build_repayment_schedule(
        loan_amount=1_000_000_000,
        rate=9.0,
        repayment_type="Interest Only",
        frequency="Quarterly",
        start_date=date(2026, 1, 1),
        maturity_date=date(2027, 1, 1),
    )
    assert len(rows) == 4
    assert rows[-1]["principal_amount"] == 1_000_000_000
    assert rows[-1]["outstanding_after"] == 0


def test_emi_monthly():
    """EMI Monthly: all rows have same total_amount (within rounding)."""
    rows = build_repayment_schedule(
        loan_amount=500_000_000,
        rate=12.0,
        repayment_type="EMI",
        frequency="Monthly",
        start_date=date(2026, 1, 1),
        maturity_date=date(2027, 1, 1),
    )
    assert len(rows) == 12
    # EMI amounts should be approximately equal
    amounts = [r["total_amount"] for r in rows]
    avg = sum(amounts) / len(amounts)
    for a in amounts:
        assert abs(a - avg) < 200_000  # wider tolerance: actual/365 varies by month length
    # Principal decreases over time, interest decreases
    assert rows[0]["interest_amount"] > rows[-1]["interest_amount"]
    assert rows[0]["principal_amount"] < rows[-1]["principal_amount"]
    # Outstanding after last row ≈ 0
    assert abs(rows[-1]["outstanding_after"]) < 100
    # Sum of principal = loan amount
    total_principal = sum(r["principal_amount"] for r in rows)
    assert abs(total_principal - 500_000_000) < 100


def test_emi_quarterly():
    """EMI Quarterly: 4 rows for 12 months."""
    rows = build_repayment_schedule(
        loan_amount=1_000_000_000,
        rate=10.0,
        repayment_type="EMI",
        frequency="Quarterly",
        start_date=date(2026, 1, 1),
        maturity_date=date(2027, 1, 1),
    )
    assert len(rows) == 4
    total_principal = sum(r["principal_amount"] for r in rows)
    assert abs(total_principal - 1_000_000_000) < 100
    assert abs(rows[-1]["outstanding_after"]) < 100


def test_emi_uses_actual_days():
    """EMI interest must use actual/365, not rate/12."""
    rows = build_repayment_schedule(
        loan_amount=500_000_000, rate=12.0,
        repayment_type="EMI", frequency="Monthly",
        start_date=date(2026, 1, 1), maturity_date=date(2027, 1, 1),
    )
    # First period: Jan 1 → Feb 1 = 31 days
    expected_interest_p1 = 500_000_000 * 0.12 * 31 / 365
    assert abs(rows[0]["interest_amount"] - expected_interest_p1) < 1


def test_total_repayment_sum():
    """Total amount for each row = principal + interest."""
    rows = build_repayment_schedule(
        loan_amount=500_000_000,
        rate=12.0,
        repayment_type="EMI",
        frequency="Monthly",
        start_date=date(2026, 1, 1),
        maturity_date=date(2027, 1, 1),
    )
    for r in rows:
        assert abs(r["total_amount"] - (r["principal_amount"] + r["interest_amount"])) < 1
