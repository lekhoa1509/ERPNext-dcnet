"""
Sales Velocity and Inventory Days Report.

Calculates stock aging (FIFO-based), sales velocity, and estimated inventory days
for each item based on outgoing Stock Ledger Entries within a given period.
"""

from collections.abc import Iterator
from operator import itemgetter

import frappe
from frappe import _
from frappe.utils import add_days, cint, date_diff, flt, get_datetime, getdate

from frappe.query_builder.functions import Abs, Sum

from erpnext.stock.doctype.serial_no.serial_no import get_serial_nos

Filters = frappe._dict

# Period multipliers: how many days per period unit
PERIOD_DAYS_MAP = {
	"Day": 1,
	"Week": 7,
	"Month": 30,
	"Quarter": 90,
	"Year": 365,
}


def execute(filters: Filters = None) -> tuple:
	"""Main entry point for the report."""
	try:
		filters = frappe._dict(filters or {})
		_validate_filters(filters)

		to_date = filters["to_date"]
		from_date = filters["from_date"]
		period = filters.get("period", "Month")

		columns = get_columns(filters, period)
		item_details = FIFOSlots(filters).generate()

		# Calculate sales velocity from SLE outgoing entries
		sales_data = _get_sales_data(filters, from_date, to_date)
		num_days = max(date_diff(to_date, from_date) + 1, 1)
		period_days = PERIOD_DAYS_MAP.get(period, 30)
		num_periods = max(num_days / period_days, 1)

		data = format_report_data(filters, item_details, to_date, sales_data, num_periods, num_days)
		chart_data = get_chart_data(data, filters, period)
		message = _get_report_message(from_date, to_date, period)

		return columns, data, message, chart_data

	except Exception:
		frappe.log_error(title=_("Sales Velocity and Inventory Days Report Error"))
		raise


def _validate_filters(filters: Filters):
	"""Validate required filters and date ranges."""
	if not filters.get("from_date"):
		filters["from_date"] = str(add_days(getdate(filters.get("to_date")), -30))
	if not filters.get("to_date"):
		filters["to_date"] = str(getdate())
	if getdate(filters["from_date"]) > getdate(filters["to_date"]):
		frappe.throw(_("From Date cannot be after To Date"))


def _get_sales_data(filters: Filters, from_date: str, to_date: str) -> dict:
	"""
	Query total sold qty per item from Stock Ledger Entry (outgoing entries only).
	Returns dict: {item_code: total_sold_qty} or {(item_code, warehouse): total_sold_qty}
	"""
	sle = frappe.qb.DocType("Stock Ledger Entry")

	from_datetime = get_datetime(from_date + " 00:00:00")
	to_datetime = get_datetime(to_date + " 23:59:59")

	query = (
		frappe.qb.from_(sle)
		.select(
			sle.item_code,
			sle.warehouse,
			Sum(Abs(sle.actual_qty)).as_("total_sold_qty"),
		)
		.where(
			(sle.actual_qty < 0)
			& (sle.company == filters.get("company"))
			& (sle.posting_datetime >= from_datetime)
			& (sle.posting_datetime <= to_datetime)
			& (sle.is_cancelled != 1)
		)
		.groupby(sle.item_code, sle.warehouse)
	)

	if filters.get("item_code"):
		query = query.where(sle.item_code == filters.get("item_code"))

	if filters.get("warehouse"):
		warehouse = frappe.qb.DocType("Warehouse")
		lft, rgt = frappe.db.get_value("Warehouse", filters.get("warehouse"), ["lft", "rgt"])
		warehouse_results = (
			frappe.qb.from_(warehouse)
			.select("name")
			.where((warehouse.lft >= lft) & (warehouse.rgt <= rgt))
			.run()
		)
		warehouse_list = [x[0] for x in warehouse_results]
		if warehouse_list:
			query = query.where(sle.warehouse.isin(warehouse_list))

	result = query.run(as_dict=True)

	sales_map = {}
	for row in result:
		if filters.get("show_warehouse_wise_stock"):
			key = (row.item_code, row.warehouse)
		else:
			key = row.item_code

		sales_map[key] = sales_map.get(key, 0) + flt(row.total_sold_qty)

	return sales_map


def format_report_data(
	filters: Filters,
	item_details: dict,
	to_date: str,
	sales_data: dict,
	num_periods: float,
	num_days: int,
) -> list[dict]:
	"""Returns ordered, formatted data with sales velocity metrics."""
	_func = itemgetter(1)
	data = []

	precision = cint(frappe.db.get_single_value("System Settings", "float_precision", cache=True))

	for _item, item_dict in item_details.items():
		if not flt(item_dict.get("total_qty"), precision):
			continue

		details = item_dict["details"]
		fifo_queue = sorted(filter(_func, item_dict["fifo_queue"]), key=_func)

		if not fifo_queue:
			continue

		average_age, age_details = get_average_age(fifo_queue, to_date)
		earliest_age = date_diff(to_date, fifo_queue[0][1])
		latest_age = date_diff(to_date, fifo_queue[-1][1])
		available_qty = flt(item_dict.get("total_qty"), precision)

		# --- Sales velocity calculations ---
		if filters.get("show_warehouse_wise_stock"):
			sales_key = (details.name, details.warehouse)
		else:
			sales_key = details.name

		total_sold_qty = flt(sales_data.get(sales_key, 0), precision)
		avg_sales_per_period = flt(total_sold_qty / num_periods, precision) if num_periods else 0
		avg_daily_sales = flt(total_sold_qty / num_days, precision) if num_days else 0
		inventory_days = flt(available_qty / avg_daily_sales, 2) if avg_daily_sales > 0 else 0

		# --- Build row ---
		row = {
			"item_code": details.name,
			"item_name": details.item_name,
			"uom": details.stock_uom,
			"description": details.description,
			"item_group": details.item_group,
			"brand": details.brand,
			"qty": available_qty,
			"age_details": age_details,
			"average_age": average_age,
			"total_sold_qty": total_sold_qty,
			"avg_sales_per_period": avg_sales_per_period,
			"inventory_days": inventory_days,
		}

		if filters.get("show_warehouse_wise_stock"):
			row["warehouse"] = details.warehouse

		data.append(row)

	return data


def get_average_age(fifo_queue: list, to_date: str) -> tuple[float, str]:
	batch_age = age_qty = total_qty = 0.0
	age_map = {}
	
	for batch in fifo_queue:
		batch_age = date_diff(to_date, batch[1])

		if isinstance(batch[0], int | float):
			qty = batch[0]
		else:
			qty = 1
			
		age_qty += batch_age * qty
		total_qty += qty
		
		age_map[batch_age] = age_map.get(batch_age, 0.0) + float(qty)

	formula = ""
	if total_qty:
		details_list = []
		for age, qty_sum in age_map.items():
			details_list.append(f"{qty_sum:g} sản phẩm tồn trong {age} ngày")
			
		formula = f"Tổng ({' + '.join(details_list)}) trên tổng số lượng {total_qty:g}"
		return flt(age_qty / total_qty, 2), formula
		
	return 0.0, formula


def get_columns(filters: Filters, period: str = "Month") -> list[dict]:
	columns = [
		{
			"label": _("Item Code"),
			"fieldname": "item_code",
			"fieldtype": "Link",
			"options": "Item",
			"width": 100,
		},
		{"label": _("Item Name"), "fieldname": "item_name", "fieldtype": "Data", "width": 100},
		{"label": _("UOM"), "fieldname": "uom", "fieldtype": "Link", "options": "UOM", "width": 100},
		{"label": _("Description"), "fieldname": "description", "fieldtype": "Data", "width": 200},
		{
			"label": _("Item Group"),
			"fieldname": "item_group",
			"fieldtype": "Link",
			"options": "Item Group",
			"width": 100,
		},
		{
			"label": _("Brand"),
			"fieldname": "brand",
			"fieldtype": "Link",
			"options": "Brand",
			"width": 100,
		},
	]

	if filters.get("show_warehouse_wise_stock"):
		columns.append(
			{
				"label": _("Warehouse"),
				"fieldname": "warehouse",
				"fieldtype": "Link",
				"options": "Warehouse",
				"width": 100,
			}
		)

	columns.extend(
		[
			{"label": _("Available Qty"), "fieldname": "qty", "fieldtype": "Float", "width": 100},
			{"label": _("Age Details"), "fieldname": "age_details", "fieldtype": "Data", "width": 250},
			{"label": _("Average Age"), "fieldname": "average_age", "fieldtype": "Float", "width": 100},
			{
				"label": _("Total Sold Qty"),
				"fieldname": "total_sold_qty",
				"fieldtype": "Float",
				"width": 120,
			},
			{
				"label": _("Avg Sales / {0}").format(_(period)),
				"fieldname": "avg_sales_per_period",
				"fieldtype": "Float",
				"width": 140,
			},
			{
				"label": _("Inventory Days"),
				"fieldname": "inventory_days",
				"fieldtype": "Float",
				"width": 120,
			},
		]
	)

	return columns


def get_chart_data(data: list, filters: Filters, period: str = "Month") -> dict:
	if not data:
		return []

	if filters.get("show_warehouse_wise_stock"):
		return {}

	labels, velocity_points, days_points = [], [], []

	sorted_data = sorted(data, key=lambda r: r.get("inventory_days", 0), reverse=True)
	chart_items = sorted_data[:10]

	for row in chart_items:
		labels.append(row.get("item_code"))
		velocity_points.append(row.get("avg_sales_per_period", 0))
		days_points.append(row.get("inventory_days", 0))

	return {
		"data": {
			"labels": labels,
			"datasets": [
				{"name": _("Avg Sales / {0}").format(_(period)), "values": velocity_points},
				{"name": _("Inventory Days"), "values": days_points},
			],
		},
		"type": "bar",
	}


def _get_report_message(from_date: str, to_date: str, period: str) -> str:
	"""Return HTML message explaining the report logic, displayed at bottom of report."""
	return f"""
	<div style="padding: 12px 16px; margin-top: 16px; background: var(--subtle-fg); border-radius: 8px; border-left: 4px solid var(--primary-color); font-size: 13px; line-height: 1.6;">
		<h4 style="margin: 0 0 8px 0; color: var(--heading-color);">
			📊 {_("Report: Sales Velocity and Inventory Days")}
		</h4>
		<p style="margin: 0 0 6px 0; color: var(--text-muted);">
			<strong>{_("Analysis Period")}:</strong> {from_date} → {to_date}
			&nbsp;|&nbsp;
			<strong>{_("Aggregation Unit")}:</strong> {_(period)}
		</p>
		<h5 style="margin: 12px 0 4px 0; color: var(--text-color);">📍 {_("1. Snapshot Metrics (Dependent only on To Date)")}</h5>
		<table style="width: 100%; border-collapse: collapse;">
			<tr>
				<td style="padding: 4px 8px; vertical-align: top; width: 30%; color: var(--text-color);">
					<strong>{_("Available Qty")}</strong>
				</td>
				<td style="padding: 4px 8px; color: var(--text-muted);">
					{_("Stock quantity available exactly at To Date.")}
				</td>
			</tr>
			<tr>
				<td style="padding: 4px 8px; vertical-align: top; color: var(--text-color);">
					<strong>{_("Age Details")}</strong>
				</td>
				<td style="padding: 4px 8px; color: var(--text-muted);">
					{_("Detailed breakdown of batch quantities and their days in stock.")}
				</td>
			</tr>
			<tr>
				<td style="padding: 4px 8px; vertical-align: top; color: var(--text-color);">
					<strong>{_("Average Age")}</strong>
				</td>
				<td style="padding: 4px 8px; color: var(--text-muted);">
					{_("Weighted average age of remaining stock based on FIFO.")}
				</td>
			</tr>
		</table>

		<h5 style="margin: 12px 0 4px 0; color: var(--text-color);">⏳ {_("2. Period Metrics (From Date to To Date)")}</h5>
		<table style="width: 100%; border-collapse: collapse;">
			<tr>
				<td style="padding: 4px 8px; vertical-align: top; width: 30%; color: var(--text-color);">
					<strong>{_("Total Sold Qty")}</strong>
				</td>
				<td style="padding: 4px 8px; color: var(--text-muted);">
					{_("Total outgoing quantity from stock during the timeframe.")}
				</td>
			</tr>
			<tr>
				<td style="padding: 4px 8px; vertical-align: top; color: var(--text-color);">
					<strong>{_("Avg Sales / Period")}</strong>
				</td>
				<td style="padding: 4px 8px; color: var(--text-muted);">
					{_("Total Sold Qty ÷ Number of Periods. Indicates average sales speed during the timeframe.")}
				</td>
			</tr>
			<tr>
				<td style="padding: 4px 8px; vertical-align: top; color: var(--text-color);">
					<strong>{_("Inventory Days")}</strong>
				</td>
				<td style="padding: 4px 8px; color: var(--text-muted);">
					{_("Available Qty ÷ Avg Daily Sales. Estimated number of days the current stock will last.")}
				</td>
			</tr>
		</table>

		<h5 style="margin: 16px 0 4px 0; color: var(--text-color);">💡 {_("3. Metrics Guidance & Analysis")}</h5>
		<p style="margin: 4px 0; font-size: 12px; color: var(--text-color);"><strong>{_("Evaluating Sales Velocity (Inventory Days):")}</strong></p>
		<ul style="margin: 0 0 8px 24px; padding: 0; font-size: 12px; color: var(--text-muted);">
			<li><strong>0 {_("days")}</strong>: {_("No sales recorded, demand stimulation needed.")}</li>
			<li><strong>&lt; 30 {_("days")}</strong>: {_("Fast-moving stock, monitor closely for timely restocking.")}</li>
			<li><strong>30 - 60 {_("days")}</strong>: {_("Stable stock turnover.")}</li>
			<li><strong>&gt; 90 {_("days")}</strong>: {_("High stagnation risk, plan for discount or liquidation.")}</li>
		</ul>

		<p style="margin: 8px 0 4px 0; font-size: 12px; color: var(--text-color);"><strong>{_("Inventory Days x Average Age Matrix:")}</strong></p>
		<ul style="margin: 0 0 12px 24px; padding: 0; font-size: 12px; color: var(--text-muted);">
			<li><strong>{_("Both High")}</strong>: {_("Old stock with slow sales, highest priority for clearance.")}</li>
			<li><strong>{_("Both Low")}</strong>: {_("Fresh stock with fast sales, excellent flagship product.")}</li>
			<li><strong>{_("Low Days, High Age")}</strong>: {_("Selling old stock fast, good sign of effective clearance.")}</li>
			<li><strong>{_("High Days, Low Age")}</strong>: {_("Fresh stock but slow sales, need to review sales plan.")}</li>
		</ul>

		<h5 style="margin: 16px 0 4px 0; color: var(--text-color);">📈 {_("4. Bar Chart Explanation")}</h5>
		<p style="margin: 0; font-size: 12px; color: var(--text-muted);">
			{_("The bar chart highlights the Top 10 items with the highest Inventory Days (highest stagnant risk), cross-referenced with their average sales.")}
		</p>
		
		<p style="margin: 12px 0 0 0; font-size: 12px; color: var(--text-muted); font-style: italic; padding-top: 8px; border-top: 1px dotted var(--border-color);">
			<strong>{_("Note on Stock Aging Algorithm (FIFO):")}</strong>
			<br>
			{_("This report strictly uses the FIFO algorithm to accurately calculate storage days (Age).")}
		</p>
	</div>
	"""


class FIFOSlots:
	"""Returns FIFO computed slots of inwarded stock as per date."""

	def __init__(self, filters: dict | None = None, sle: list | None = None):
		self.item_details = {}
		self.transferred_item_details = {}
		self.serial_no_batch_purchase_details = {}
		self.filters = filters
		self.sle = sle

	def generate(self) -> dict:
		"""
		Returns dict of the foll.g structure:
		Key = Item A / (Item A, Warehouse A)
		Key: {
		        'details' -> Dict: ** item details **,
		        'fifo_queue' -> List: ** list of lists containing entries/slots for existing stock,
		                consumed/updated and maintained via FIFO. **
		}
		"""

		from erpnext.stock.doctype.serial_and_batch_bundle.test_serial_and_batch_bundle import (
			get_serial_nos_from_bundle,
		)

		stock_ledger_entries = self.sle

		bundle_wise_serial_nos = frappe._dict({})
		if stock_ledger_entries is None:
			bundle_wise_serial_nos = self.__get_bundle_wise_serial_nos()

		with frappe.db.unbuffered_cursor():
			if stock_ledger_entries is None:
				stock_ledger_entries = self.__get_stock_ledger_entries()

			for d in stock_ledger_entries:
				key, fifo_queue, transferred_item_key = self.__init_key_stores(d)

				if d.voucher_type == "Stock Reconciliation":
					prev_balance_qty = self.item_details[key].get("qty_after_transaction", 0)
					d.actual_qty = flt(d.qty_after_transaction) - flt(prev_balance_qty)

				serial_nos = get_serial_nos(d.serial_no) if d.serial_no else []
				if d.serial_and_batch_bundle and d.has_serial_no:
					if bundle_wise_serial_nos:
						serial_nos = bundle_wise_serial_nos.get(d.serial_and_batch_bundle) or []
					else:
						serial_nos = get_serial_nos_from_bundle(d.serial_and_batch_bundle) or []

				serial_nos = self.uppercase_serial_nos(serial_nos)
				if d.actual_qty > 0:
					self.__compute_incoming_stock(d, fifo_queue, transferred_item_key, serial_nos)
				else:
					self.__compute_outgoing_stock(d, fifo_queue, transferred_item_key, serial_nos)

				self.__update_balances(d, key)

			del stock_ledger_entries

		if not self.filters.get("show_warehouse_wise_stock"):
			self.item_details = self.__aggregate_details_by_item(self.item_details)

		return self.item_details

	def uppercase_serial_nos(self, serial_nos):
		"""Convert serial nos to uppercase for uniformity."""
		return [sn.upper() for sn in serial_nos]

	def __init_key_stores(self, row: dict) -> tuple:
		"""Initialise keys and FIFO Queue."""
		key = (row.name, row.warehouse)
		self.item_details.setdefault(key, {"details": row, "fifo_queue": []})
		fifo_queue = self.item_details[key]["fifo_queue"]

		transferred_item_key = (row.voucher_no, row.name, row.warehouse)
		self.transferred_item_details.setdefault(transferred_item_key, [])

		return key, fifo_queue, transferred_item_key

	def __compute_incoming_stock(self, row: dict, fifo_queue: list, transfer_key: tuple, serial_nos: list):
		"""Update FIFO Queue on inward stock."""
		transfer_data = self.transferred_item_details.get(transfer_key)
		if transfer_data:
			self.__adjust_incoming_transfer_qty(transfer_data, fifo_queue, row)
		else:
			if not serial_nos and not row.get("has_serial_no"):
				if fifo_queue and flt(fifo_queue[0][0]) <= 0:
					fifo_queue[0][0] += flt(row.actual_qty)
					fifo_queue[0][1] = row.posting_date
					fifo_queue[0][2] += flt(row.stock_value_difference)
				else:
					fifo_queue.append(
						[flt(row.actual_qty), row.posting_date, flt(row.stock_value_difference)]
					)
				return

			valuation = row.stock_value_difference / row.actual_qty
			for serial_no in serial_nos:
				if self.serial_no_batch_purchase_details.get(serial_no):
					fifo_queue.append(
						[serial_no, self.serial_no_batch_purchase_details.get(serial_no), valuation]
					)
				else:
					self.serial_no_batch_purchase_details.setdefault(serial_no, row.posting_date)
					fifo_queue.append([serial_no, row.posting_date, valuation])

	def __compute_outgoing_stock(self, row: dict, fifo_queue: list, transfer_key: tuple, serial_nos: list):
		"""Update FIFO Queue on outward stock."""
		if serial_nos:
			fifo_queue[:] = [serial_no for serial_no in fifo_queue if serial_no[0] not in serial_nos]
			return

		qty_to_pop = abs(row.actual_qty)
		stock_value = abs(row.stock_value_difference)

		while qty_to_pop:
			slot = fifo_queue[0] if fifo_queue else [0, None, 0]
			if 0 < flt(slot[0]) <= qty_to_pop:
				qty_to_pop -= flt(slot[0])
				stock_value -= flt(slot[2])
				self.transferred_item_details[transfer_key].append(fifo_queue.pop(0))
			elif not fifo_queue:
				fifo_queue.append([-(qty_to_pop), row.posting_date, -(stock_value)])
				self.transferred_item_details[transfer_key].append(
					[qty_to_pop, row.posting_date, stock_value]
				)
				qty_to_pop = 0
				stock_value = 0
			else:
				slot[0] = flt(slot[0]) - qty_to_pop
				slot[2] = flt(slot[2]) - stock_value
				self.transferred_item_details[transfer_key].append([qty_to_pop, slot[1], stock_value])
				qty_to_pop = 0
				stock_value = 0

	def __adjust_incoming_transfer_qty(self, transfer_data: dict, fifo_queue: list, row: dict):
		"""Add previously removed stock back to FIFO Queue."""
		transfer_qty_to_pop = flt(row.actual_qty)
		stock_value = flt(row.stock_value_difference)

		def add_to_fifo_queue(slot):
			if fifo_queue and flt(fifo_queue[0][0]) <= 0:
				fifo_queue[0][0] += flt(slot[0])
				fifo_queue[0][1] = slot[1]
				fifo_queue[0][2] += flt(slot[2])
			else:
				fifo_queue.append(slot)

		while transfer_qty_to_pop:
			if transfer_data and 0 < transfer_data[0][0] <= transfer_qty_to_pop:
				transfer_qty_to_pop -= transfer_data[0][0]
				stock_value -= transfer_data[0][2]
				add_to_fifo_queue(transfer_data.pop(0))
			elif not transfer_data:
				add_to_fifo_queue([transfer_qty_to_pop, row.posting_date, stock_value])
				transfer_qty_to_pop = 0
				stock_value = 0
			else:
				transfer_data[0][0] -= transfer_qty_to_pop
				transfer_data[0][2] -= stock_value
				add_to_fifo_queue([transfer_qty_to_pop, transfer_data[0][1], stock_value])
				transfer_qty_to_pop = 0
				stock_value = 0

	def __update_balances(self, row: dict, key: tuple | str):
		self.item_details[key]["qty_after_transaction"] = row.qty_after_transaction

		if "total_qty" not in self.item_details[key]:
			self.item_details[key]["total_qty"] = row.actual_qty
		else:
			self.item_details[key]["total_qty"] += row.actual_qty

		self.item_details[key]["has_serial_no"] = row.has_serial_no
		self.item_details[key]["details"].valuation_rate = row.valuation_rate

	def __aggregate_details_by_item(self, wh_wise_data: dict) -> dict:
		"""Aggregate Item-Wh wise data into single Item entry."""
		item_aggregated_data = {}
		for key, row in wh_wise_data.items():
			item = key[0]
			if not item_aggregated_data.get(item):
				item_aggregated_data.setdefault(
					item,
					{
						"details": frappe._dict(),
						"fifo_queue": [],
						"qty_after_transaction": 0.0,
						"total_qty": 0.0,
					},
				)
			item_row = item_aggregated_data.get(item)
			item_row["details"].update(row["details"])
			item_row["fifo_queue"].extend(row["fifo_queue"])
			item_row["qty_after_transaction"] += flt(row["qty_after_transaction"])
			item_row["total_qty"] += flt(row["total_qty"])
			item_row["has_serial_no"] = row["has_serial_no"]

		return item_aggregated_data

	def __get_stock_ledger_entries(self) -> Iterator[dict]:
		sle = frappe.qb.DocType("Stock Ledger Entry")
		item = self.__get_item_query()
		to_date = get_datetime(self.filters.get("to_date") + " 23:59:59")

		sle_query = (
			frappe.qb.from_(sle)
			.from_(item)
			.select(
				item.name,
				item.item_name,
				item.item_group,
				item.brand,
				item.description,
				item.stock_uom,
				item.has_serial_no,
				item.valuation_method,
				sle.actual_qty,
				sle.stock_value_difference,
				sle.valuation_rate,
				sle.posting_date,
				sle.voucher_type,
				sle.voucher_no,
				sle.serial_no,
				sle.batch_no,
				sle.qty_after_transaction,
				sle.serial_and_batch_bundle,
				sle.warehouse,
			)
			.where(
				(sle.item_code == item.name)
				& (sle.company == self.filters.get("company"))
				& (sle.posting_datetime <= to_date)
				& (sle.is_cancelled != 1)
			)
		)

		if self.filters.get("warehouse"):
			sle_query = self.__get_warehouse_conditions(sle, sle_query)

		sle_query = sle_query.orderby(sle.posting_datetime, sle.creation)

		return sle_query.run(as_dict=True, as_iterator=True)

	def __get_bundle_wise_serial_nos(self) -> dict:
		bundle = frappe.qb.DocType("Serial and Batch Bundle")
		entry = frappe.qb.DocType("Serial and Batch Entry")

		to_date = get_datetime(self.filters.get("to_date") + " 23:59:59")
		query = (
			frappe.qb.from_(bundle)
			.join(entry)
			.on(bundle.name == entry.parent)
			.select(bundle.name, entry.serial_no)
			.where(
				(bundle.docstatus == 1)
				& (entry.serial_no.isnotnull())
				& (bundle.company == self.filters.get("company"))
				& (bundle.posting_datetime <= to_date)
			)
		)

		for field in ["item_code"]:
			if self.filters.get(field):
				query = query.where(bundle[field] == self.filters.get(field))

		if self.filters.get("warehouse"):
			query = self.__get_warehouse_conditions(bundle, query)

		bundle_wise_serial_nos = frappe._dict({})
		for bundle_name, serial_no in query.run():
			bundle_wise_serial_nos.setdefault(bundle_name, []).append(serial_no)

		return bundle_wise_serial_nos

	def __get_item_query(self) -> str:
		item_table = frappe.qb.DocType("Item")

		item = frappe.qb.from_("Item").select(
			"name",
			"item_name",
			"description",
			"stock_uom",
			"brand",
			"item_group",
			"has_serial_no",
			"valuation_method",
		)

		if self.filters.get("item_code"):
			item = item.where(item_table.item_code == self.filters.get("item_code"))

		if self.filters.get("brand"):
			item = item.where(item_table.brand == self.filters.get("brand"))

		return item

	def __get_warehouse_conditions(self, sle, sle_query) -> str:
		warehouse = frappe.qb.DocType("Warehouse")
		lft, rgt = frappe.db.get_value("Warehouse", self.filters.get("warehouse"), ["lft", "rgt"])

		warehouse_results = (
			frappe.qb.from_(warehouse)
			.select("name")
			.where((warehouse.lft >= lft) & (warehouse.rgt <= rgt))
			.run()
		)
		warehouse_results = [x[0] for x in warehouse_results]

		return sle_query.where(sle.warehouse.isin(warehouse_results))
