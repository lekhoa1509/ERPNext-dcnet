from calendar import monthrange
from dataclasses import dataclass
from datetime import date, timedelta
from decimal import ROUND_HALF_EVEN, ROUND_HALF_UP, Decimal


@dataclass
class ScheduleInput:
	contract_type: str  # "Recurring" | "One-off"
	payment_mode: str  # "Prepay" | "Monthly" | "OneOff"
	package_term_months: int | None  # None if One-off
	acceptance_date: date
	unit_price_total: Decimal  # per-period for Recurring, total for One-off
	setup_fee: Decimal  # 0 if none
	rounding_mode: str  # "Half-up" | "Bankers"


@dataclass
class ScheduleRow:
	month_index: int  # 0 = setup fee, 1..N = service periods
	period_start: date
	period_end: date
	due_date: date
	item_type: str  # "Setup Fee" | "Service"
	amount: Decimal
	is_prorated: bool
	state: str = "Projected"


def generate_schedule(inp: ScheduleInput) -> list[ScheduleRow]:
	rows: list[ScheduleRow] = []

	# Setup fee row
	if inp.setup_fee > 0:
		rows.append(ScheduleRow(
			month_index=0,
			period_start=inp.acceptance_date,
			period_end=inp.acceptance_date,
			due_date=inp.acceptance_date,
			item_type="Setup Fee",
			amount=inp.setup_fee,
			is_prorated=False,
		))

	# One-off: single service row
	if inp.contract_type == "One-off":
		rows.append(ScheduleRow(
			month_index=1,
			period_start=inp.acceptance_date,
			period_end=inp.acceptance_date,
			due_date=inp.acceptance_date,
			item_type="Service",
			amount=inp.unit_price_total,
			is_prorated=False,
		))
		return rows

	# Recurring
	first_start = inp.acceptance_date
	last_end = _add_months(first_start, inp.package_term_months) - timedelta(days=1)

	if inp.payment_mode == "Prepay":
		rows.append(ScheduleRow(
			month_index=1,
			period_start=first_start,
			period_end=last_end,
			due_date=first_start,
			item_type="Service",
			amount=inp.unit_price_total * inp.package_term_months,
			is_prorated=False,
		))
		return rows

	# Monthly recurring
	rounding = ROUND_HALF_UP if inp.rounding_mode == "Half-up" else ROUND_HALF_EVEN
	for idx in range(1, inp.package_term_months + 1):
		p_start, p_end, prorated = _compute_period(idx, first_start, inp.package_term_months)
		amount = _compute_amount(p_start, p_end, inp.unit_price_total, rounding)
		rows.append(ScheduleRow(
			month_index=idx,
			period_start=p_start,
			period_end=p_end,
			due_date=p_end,
			item_type="Service",
			amount=amount,
			is_prorated=prorated,
		))

	return rows


def _compute_amount(period_start: date, period_end: date, monthly_price: Decimal, rounding) -> Decimal:
	"""Mau 01 formula: Round(monthly/days_in_month, 0) x actual_days."""
	days_in_month = monthrange(period_start.year, period_start.month)[1]
	actual_days = (period_end - period_start).days + 1
	if actual_days == days_in_month:
		return monthly_price
	daily_rate = (monthly_price / days_in_month).quantize(Decimal("1"), rounding=rounding)
	return daily_rate * actual_days


def _compute_period(idx: int, first_start: date, total_months: int) -> tuple[date, date, bool]:
	"""Return (period_start, period_end, is_prorated) for month idx in [1..total_months]."""
	if idx == 1:
		p_start = first_start
		p_end = _last_day_of_month(first_start)
		return p_start, p_end, (p_start.day != 1)

	p_start = _first_of_month_offset(first_start, idx - 1)
	if idx == total_months:
		p_end = _add_months(first_start, total_months) - timedelta(days=1)
		full_month_end = _last_day_of_month(p_start)
		return p_start, p_end, (p_end != full_month_end)

	p_end = _last_day_of_month(p_start)
	return p_start, p_end, False


def _add_months(d: date, months: int) -> date:
	"""Add N months to a date, preserving the day (clamped to month end)."""
	month = d.month - 1 + months
	year = d.year + month // 12
	month = month % 12 + 1
	day = min(d.day, monthrange(year, month)[1])
	return date(year, month, day)


def _last_day_of_month(d: date) -> date:
	return d.replace(day=monthrange(d.year, d.month)[1])


def _first_of_month_offset(start: date, offset_months: int) -> date:
	"""Return the 1st of the month that is offset_months after start's month."""
	month = start.month - 1 + offset_months
	year = start.year + month // 12
	month = month % 12 + 1
	return date(year, month, 1)
