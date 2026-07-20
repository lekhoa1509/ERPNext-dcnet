from calendar import monthrange
from dataclasses import dataclass, field
from datetime import date, timedelta
from decimal import ROUND_HALF_EVEN, ROUND_HALF_UP, Decimal


@dataclass
class ItemInput:
	item_idx: int  # 0-based contract.items index
	item_label: str
	item_kind: str  # "Setup Fee" | "Recurring Service" | "One-off Goods"
	qty: Decimal
	unit_price: Decimal
	payment_mode: str | None = None  # None = use contract default


@dataclass
class ScheduleInput:
	"""Walk-items mode (v0.2.0). When `items` is set, walk it; otherwise fall back to
	legacy aggregate-by-contract behavior (kept for old data + tests)."""

	contract_type: str
	payment_mode: str
	package_term_months: int | None
	acceptance_date: date
	unit_price_total: Decimal
	setup_fee: Decimal
	rounding_mode: str = "Half-up"
	items: list[ItemInput] = field(default_factory=list)


@dataclass
class ScheduleRow:
	month_index: int
	period_start: date
	period_end: date
	due_date: date
	item_type: str  # "Setup Fee" | "Service" | "One-off Goods"
	amount: Decimal
	is_prorated: bool
	state: str = "Projected"
	item_ref: str = ""  # str of item_idx (or "" for legacy aggregate rows)


def generate_schedule(inp: ScheduleInput) -> list[ScheduleRow]:
	if inp.items:
		return _generate_from_items(inp)
	return _generate_legacy(inp)


def _generate_from_items(inp: ScheduleInput) -> list[ScheduleRow]:
	"""v0.2.0 walk-items mode. Each item generates its own BS row(s)."""
	rounding = ROUND_HALF_UP if inp.rounding_mode == "Half-up" else ROUND_HALF_EVEN
	rows: list[ScheduleRow] = []
	next_idx = 0

	# Group order: Setup Fee → One-off Goods → Recurring Service (so kế toán reads top-down)
	def _kind_order(it: ItemInput) -> int:
		return {"Setup Fee": 0, "One-off Goods": 1, "Recurring Service": 2}.get(it.item_kind, 3)

	for item in sorted(inp.items, key=_kind_order):
		item_amount = Decimal(str(item.qty)) * Decimal(str(item.unit_price))
		if item.item_kind == "Setup Fee":
			rows.append(ScheduleRow(
				month_index=next_idx,
				period_start=inp.acceptance_date,
				period_end=inp.acceptance_date,
				due_date=inp.acceptance_date,
				item_type="Setup Fee",
				amount=item_amount,
				is_prorated=False,
				item_ref=str(item.item_idx),
			))
			next_idx += 1
			continue

		if item.item_kind == "One-off Goods":
			rows.append(ScheduleRow(
				month_index=next_idx,
				period_start=inp.acceptance_date,
				period_end=inp.acceptance_date,
				due_date=inp.acceptance_date,
				item_type="One-off Goods",
				amount=item_amount,
				is_prorated=False,
				item_ref=str(item.item_idx),
			))
			next_idx += 1
			continue

		# Recurring Service
		mode = (item.payment_mode or inp.payment_mode or "Monthly").strip()
		term = inp.package_term_months or 1
		first_start = inp.acceptance_date
		last_end = _add_months(first_start, term) - timedelta(days=1)

		if mode == "Prepay":
			rows.append(ScheduleRow(
				month_index=next_idx,
				period_start=first_start,
				period_end=last_end,
				due_date=first_start,
				item_type="Service",
				amount=item_amount * term,
				is_prorated=False,
				item_ref=str(item.item_idx),
			))
			next_idx += 1
			continue

		# Monthly recurring
		for k in range(1, term + 1):
			p_start, p_end, prorated = _compute_period(k, first_start, term)
			amount = _compute_amount(p_start, p_end, item_amount, rounding)
			rows.append(ScheduleRow(
				month_index=next_idx,
				period_start=p_start,
				period_end=p_end,
				due_date=p_end,
				item_type="Service",
				amount=amount,
				is_prorated=prorated,
				item_ref=str(item.item_idx),
			))
			next_idx += 1

	return rows


def _generate_legacy(inp: ScheduleInput) -> list[ScheduleRow]:
	"""Legacy v0.1.x behavior — aggregate unit_price_total + setup_fee at contract level.
	Kept for old data and tests that don't pass items list."""
	rows: list[ScheduleRow] = []

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
