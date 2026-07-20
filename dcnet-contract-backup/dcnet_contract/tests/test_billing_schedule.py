from datetime import date
from decimal import Decimal

from dcnet_contract.dcnet_contract.utils.billing_schedule import ScheduleInput, generate_schedule


def _inp(**over):
	base = dict(
		contract_type="Recurring",
		payment_mode="Monthly",
		package_term_months=12,
		acceptance_date=date(2026, 1, 1),
		unit_price_total=Decimal("10500"),
		setup_fee=Decimal("0"),
		rounding_mode="Half-up",
	)
	base.update(over)
	return ScheduleInput(**base)


class TestFullMonthStart:
	def test_12_rows_no_proration(self):
		rows = generate_schedule(_inp())
		assert len(rows) == 12
		assert all(r.amount == Decimal("10500") for r in rows)
		assert all(not r.is_prorated for r in rows)

	def test_first_row_dates(self):
		rows = generate_schedule(_inp())
		assert rows[0].month_index == 1
		assert rows[0].period_start == date(2026, 1, 1)
		assert rows[0].period_end == date(2026, 1, 31)
		assert rows[0].item_type == "Service"
		assert rows[0].state == "Projected"

	def test_last_row_dates(self):
		rows = generate_schedule(_inp())
		assert rows[11].month_index == 12
		assert rows[11].period_start == date(2026, 12, 1)
		assert rows[11].period_end == date(2026, 12, 31)


class TestMidMonthProration:
	def test_first_month_prorated(self):
		rows = generate_schedule(_inp(acceptance_date=date(2026, 1, 15)))
		assert rows[0].month_index == 1
		assert rows[0].is_prorated is True
		assert rows[0].amount == Decimal("5763")
		assert rows[0].period_start == date(2026, 1, 15)
		assert rows[0].period_end == date(2026, 1, 31)

	def test_middle_months_full(self):
		rows = generate_schedule(_inp(acceptance_date=date(2026, 1, 15)))
		for r in rows[1:11]:
			assert not r.is_prorated
			assert r.amount == Decimal("10500")

	def test_last_month_prorated(self):
		rows = generate_schedule(_inp(acceptance_date=date(2026, 1, 15)))
		last = rows[11]
		assert last.month_index == 12
		assert last.is_prorated is True
		assert last.period_start == date(2026, 12, 1)
		assert last.period_end == date(2027, 1, 14)

	def test_row_count(self):
		rows = generate_schedule(_inp(acceptance_date=date(2026, 1, 15)))
		assert len(rows) == 12


class TestEndOfMonthStart:
	def test_single_day_first_period(self):
		rows = generate_schedule(_inp(acceptance_date=date(2026, 1, 31)))
		assert rows[0].amount == Decimal("339")
		assert rows[0].is_prorated is True
		assert rows[0].period_start == date(2026, 1, 31)
		assert rows[0].period_end == date(2026, 1, 31)


class TestSetupFee:
	def test_setup_fee_prepended(self):
		rows = generate_schedule(_inp(setup_fee=Decimal("3000")))
		assert rows[0].month_index == 0
		assert rows[0].item_type == "Setup Fee"
		assert rows[0].amount == Decimal("3000")
		assert rows[0].is_prorated is False
		assert rows[1].month_index == 1

	def test_total_rows_with_setup(self):
		rows = generate_schedule(_inp(setup_fee=Decimal("3000")))
		assert len(rows) == 13


class TestPrepay:
	def test_single_row_full_term(self):
		rows = generate_schedule(_inp(payment_mode="Prepay"))
		assert len(rows) == 1
		assert rows[0].amount == Decimal("126000")
		assert not rows[0].is_prorated
		assert rows[0].month_index == 1

	def test_prepay_with_setup_fee(self):
		rows = generate_schedule(_inp(payment_mode="Prepay", setup_fee=Decimal("5000")))
		assert len(rows) == 2
		assert rows[0].item_type == "Setup Fee"
		assert rows[1].amount == Decimal("126000")


class TestLeapYear:
	def test_feb29_add_12_months_clamps(self):
		"""Feb 29 leap year + 12 months → Feb 28 next year (non-leap)."""
		from dcnet_contract.dcnet_contract.utils.billing_schedule import _add_months
		result = _add_months(date(2028, 2, 29), 12)
		assert result == date(2029, 2, 28)

	def test_feb29_add_12_months_to_leap(self):
		"""Feb 29 leap year + 48 months → Feb 29 next leap year."""
		from dcnet_contract.dcnet_contract.utils.billing_schedule import _add_months
		result = _add_months(date(2028, 2, 29), 48)
		assert result == date(2032, 2, 29)


class TestOneMonthTrial:
	def test_one_month_mid_start(self):
		"""1-month contract starting mid-month → exactly 1 prorated row."""
		rows = generate_schedule(_inp(
			package_term_months=1,
			acceptance_date=date(2026, 3, 15),
		))
		assert len(rows) == 1
		assert rows[0].is_prorated is True
		assert rows[0].period_start == date(2026, 3, 15)
		assert rows[0].period_end == date(2026, 3, 31)

	def test_one_month_first_day(self):
		"""1-month contract starting day 1 → exactly 1 full row."""
		rows = generate_schedule(_inp(
			package_term_months=1,
			acceptance_date=date(2026, 3, 1),
		))
		assert len(rows) == 1
		assert rows[0].is_prorated is False
		assert rows[0].amount == Decimal("10500")


class TestZeroAmount:
	def test_zero_price_no_crash(self):
		"""unit_price_total=0 → rows created with amount=0, no crash."""
		rows = generate_schedule(_inp(unit_price_total=Decimal("0")))
		assert len(rows) == 12
		assert all(r.amount == Decimal("0") for r in rows)

	def test_zero_price_mid_month_no_crash(self):
		"""Zero amount + mid-month start → prorated rows with 0 amount."""
		rows = generate_schedule(_inp(
			unit_price_total=Decimal("0"),
			acceptance_date=date(2026, 1, 15),
		))
		assert len(rows) == 12
		assert all(r.amount == Decimal("0") for r in rows)


class TestOneOff:
	def test_single_row(self):
		rows = generate_schedule(_inp(
			contract_type="One-off",
			payment_mode="OneOff",
			package_term_months=None,
			unit_price_total=Decimal("13500"),
		))
		assert len(rows) == 1
		assert rows[0].item_type == "Service"
		assert rows[0].amount == Decimal("13500")
		assert rows[0].month_index == 1
		assert not rows[0].is_prorated
