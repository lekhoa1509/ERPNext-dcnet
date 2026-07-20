"""Tests for interest schedule calculator — all 5 interest types.

Run: cd /home/long/long/frappe-bench-dcnet/apps/vn_accounting
     python -m pytest vn_accounting/treasury/test_interest_calculator.py -v
"""
from datetime import date
from vn_accounting.treasury.interest_calculator import build_interest_schedule


def test_end_of_term_single_row():
    """End of Term: 100M VND, 6% p.a., 6 months → 1 row at maturity."""
    rows = build_interest_schedule(
        principal=100_000_000,
        rate=6.0,
        interest_type="End of Term",
        start_date=date(2026, 1, 1),
        term_months=6,
    )
    assert len(rows) == 1
    assert rows[0]["due_date"] == date(2026, 7, 1)
    # interest = 100M * 6/100 * 181/365 = 2,975,342.47 (approx)
    assert abs(rows[0]["interest_amount"] - 2_975_342.47) < 1
    assert rows[0]["principal_at_start"] == 100_000_000


def test_monthly_12_rows():
    """Monthly: 100M, 6%, 12 months → 12 rows, one per month."""
    rows = build_interest_schedule(
        principal=100_000_000,
        rate=6.0,
        interest_type="Monthly",
        start_date=date(2026, 1, 1),
        term_months=12,
    )
    assert len(rows) == 12
    # First row: due 2026-02-01, days=31
    assert rows[0]["due_date"] == date(2026, 2, 1)
    expected_first = 100_000_000 * 0.06 * 31 / 365
    assert abs(rows[0]["interest_amount"] - expected_first) < 1
    # All rows have same principal
    for r in rows:
        assert r["principal_at_start"] == 100_000_000
    # Last row due date = maturity
    assert rows[-1]["due_date"] == date(2027, 1, 1)


def test_quarterly_4_rows():
    """Quarterly: 200M, 7%, 12 months → 4 rows."""
    rows = build_interest_schedule(
        principal=200_000_000,
        rate=7.0,
        interest_type="Quarterly",
        start_date=date(2026, 1, 1),
        term_months=12,
    )
    assert len(rows) == 4
    assert rows[0]["due_date"] == date(2026, 4, 1)
    assert rows[-1]["due_date"] == date(2027, 1, 1)
    for r in rows:
        assert r["principal_at_start"] == 200_000_000


def test_prepaid_single_row_at_start():
    """Prepaid: interest deducted at start_date, 1 row, uses actual/365."""
    rows = build_interest_schedule(
        principal=100_000_000,
        rate=6.0,
        interest_type="Prepaid",
        start_date=date(2026, 1, 1),
        term_months=6,
    )
    assert len(rows) == 1
    assert rows[0]["due_date"] == date(2026, 1, 1)
    # interest = principal * rate/100 * actual_days/365
    maturity = date(2026, 7, 1)
    days = (maturity - date(2026, 1, 1)).days  # 181 days
    expected = 100_000_000 * 0.06 * days / 365
    assert abs(rows[0]["interest_amount"] - expected) < 1
    assert rows[0]["principal_at_start"] == 100_000_000


def test_prepaid_uses_actual_days():
    """Prepaid interest must use actual/365, not term_months/12."""
    rows = build_interest_schedule(
        principal=100_000_000,
        rate=6.0,
        interest_type="Prepaid",
        start_date=date(2026, 1, 1),
        term_months=6,
    )
    # 6 months from Jan 1 → Jul 1 = 181 days
    expected = 100_000_000 * 0.06 * 181 / 365
    assert abs(rows[0]["interest_amount"] - expected) < 1
    # Should NOT equal the old term_months/12 formula
    old_formula = 100_000_000 * 0.06 * 6 / 12
    assert abs(rows[0]["interest_amount"] - old_formula) > 10  # different result


def test_compound_principal_increases():
    """Compound: monthly compounding, principal_at_start increases each period."""
    rows = build_interest_schedule(
        principal=100_000_000,
        rate=6.0,
        interest_type="Compound",
        start_date=date(2026, 1, 1),
        term_months=3,
    )
    assert len(rows) == 3
    assert rows[0]["principal_at_start"] == 100_000_000
    # After period 1: new principal = old + interest (allow 0.01 rounding tolerance)
    assert abs(rows[1]["principal_at_start"] - (rows[0]["principal_at_start"] + rows[0]["interest_amount"])) < 0.01
    assert abs(rows[2]["principal_at_start"] - (rows[1]["principal_at_start"] + rows[1]["interest_amount"])) < 0.01
    # Principal increases each period (compounding effect)
    assert rows[1]["principal_at_start"] > rows[0]["principal_at_start"]
    assert rows[2]["principal_at_start"] > rows[1]["principal_at_start"]


def test_total_interest_sum():
    """Monthly total should approximately equal simple annual interest."""
    rows = build_interest_schedule(
        principal=100_000_000,
        rate=6.0,
        interest_type="Monthly",
        start_date=date(2026, 1, 1),
        term_months=12,
    )
    total = sum(r["interest_amount"] for r in rows)
    # Should be close to 6M (6% of 100M for 1 year)
    assert abs(total - 6_000_000) < 50_000  # within 50K tolerance


def test_accrued_interest():
    """Accrued interest uses actual/365 from last interest date to accrual date."""
    from vn_accounting.treasury.interest_calculator import calculate_accrued_interest
    # 100M at 6%, from Jan 1 to Mar 31 = 89 days
    result = calculate_accrued_interest(
        principal=100_000_000, rate=6.0,
        last_interest_date=date(2026, 1, 1), accrual_date=date(2026, 3, 31),
    )
    expected = 100_000_000 * 0.06 * 89 / 365
    assert abs(result - expected) < 1

    # Zero or negative days → 0
    assert calculate_accrued_interest(100_000_000, 6.0, date(2026, 3, 1), date(2026, 3, 1)) == 0.0
    assert calculate_accrued_interest(100_000_000, 6.0, date(2026, 3, 1), date(2026, 2, 1)) == 0.0


def test_early_settlement_calculation():
    """Early settlement uses early_withdrawal_rate and pro-rata days."""
    from vn_accounting.treasury.interest_calculator import calculate_early_settlement_interest
    result = calculate_early_settlement_interest(
        principal=100_000_000,
        original_rate=6.0,
        early_rate=1.0,
        start_date=date(2026, 1, 1),
        settlement_date=date(2026, 4, 1),
        interest_already_paid=0,
    )
    # 100M * 1% * 90/365 = 246,575.34
    assert abs(result["interest_entitled"] - 246_575.34) < 1
    assert result["adjustment"] == result["interest_entitled"] - 0
