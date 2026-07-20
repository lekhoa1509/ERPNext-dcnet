
import frappe
from frappe import _
from frappe.query_builder.functions import Date, Sum


def execute(filters=None):
	filters = validate_filters(filters)

	columns = get_columns()
	data = get_data(filters)

	return columns, data


def validate_filters(filters):
	from erpnext.accounts.utils import get_fiscal_year

	if not filters:
		# If filters is None, initialize it as a dict
		return frappe._dict({
			"from_date": get_fiscal_year(frappe.utils.nowdate(), True)[1],
			"to_date": frappe.utils.nowdate()
		})

	if not filters.get("from_date"):
		filters["from_date"] = get_fiscal_year(frappe.utils.nowdate(), True)[1]

	if not filters.get("to_date"):
		filters["to_date"] = frappe.utils.nowdate()
		
	return filters

def get_columns():
	return [
		{
			"label": _("Item"),
			"fieldname": "item",
			"fieldtype": "Link",
			"options": "Item",
			"width": 150
		},
		{
			"label": _("Item Name"),
			"fieldname": "item_name",
			"fieldtype": "Data",
			"width": 150
		},
		{
			"label": _("Batch"),
			"fieldname": "batch",
			"fieldtype": "Link",
			"options": "Batch",
			"width": 150
		},
		{
			"label": _("Stock UOM"),
			"fieldname": "stock_uom",
			"fieldtype": "Link",
			"options": "UOM",
			"width": 100
		},
		{
			"label": _("Quantity"),
			"fieldname": "batch_qty",
			"fieldtype": "Float",
			"width": 100
		},
		{
			"label": _("Expires On"),
			"fieldname": "expiry_date",
			"fieldtype": "Date",
			"width": 100
		},
		{
			"label": _("Expiry (In Days)"),
			"fieldname": "expiry_days",
			"fieldtype": "Int",
			"width": 130
		},
	]


def get_data(filters):
	data = []

	# Get filter value, treat None or empty string as 'no filter'
	near_filter_raw = filters.get("near_expiry_days")
	has_filter = near_filter_raw is not None and str(near_filter_raw).strip() != ""
	near_expired_limit = frappe.utils.cint(near_filter_raw) if has_filter else None

	expired_filter = filters.get("expired_filter")

	today = frappe.utils.datetime.date.today()

	for batch in get_batch_details(filters):
		# Calculate real days difference (negative means already expired)
		expiry_days = (batch.expiry_date - today).days if batch.expiry_date else None
		
		# Apply Expired Status filter logically
		if expired_filter == "Exclude Expired":
			if expiry_days is not None and expiry_days <= 0:
				continue
		elif expired_filter == "Expired Only":
			if expiry_days is None or expiry_days > 0:
				continue

		# Apply 'Near Expired (Days)' filter logic
		if has_filter:
			# If filter is set, hide rows with no expiry date or those far into the future
			if expiry_days is None or expiry_days > near_expired_limit:
				continue

		data.append(
			{
				"item": batch.item,
				"item_name": batch.item_name,
				"batch": batch.name,
				"stock_uom": batch.stock_uom,
				"batch_qty": batch.batch_qty,
				"expiry_date": batch.expiry_date,
				"expiry_days": expiry_days,
			}
		)

	return data


def get_batch_details(filters):
	batch = frappe.qb.DocType("Batch")
	query = (
		frappe.qb.from_(batch)
		.select(
			batch.name,
			batch.creation,
			batch.expiry_date,
			batch.item,
			batch.item_name,
			batch.stock_uom,
			batch.batch_qty,
		)
		.where(
			(batch.disabled == 0)
			& (batch.batch_qty > 0)
			& ((Date(batch.creation) >= filters["from_date"]) & (Date(batch.creation) <= filters["to_date"]))
		)
		.orderby(batch.creation)
	)

	if filters.get("item"):
		query = query.where(batch.item == filters["item"])

	return query.run(as_dict=True)
