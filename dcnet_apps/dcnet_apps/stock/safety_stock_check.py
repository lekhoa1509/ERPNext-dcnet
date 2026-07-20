import frappe
from frappe import _
from frappe.utils import flt


def check_safety_stock_on_sales_order(doc, method):
	"""
	Hook: Sales Order → on_submit
	Check each item in SO, if actual_qty <= safety_stock → flag for client-side alert.
	The actual dialog is rendered by the client-side JS (sales_order.js)
	which calls get_low_stock_items API after submit.
	"""
	pass  # Logic moved to whitelisted API called from client-side JS


@frappe.whitelist()
def get_low_stock_items(sales_order):
	"""
	Whitelisted API: Check low stock items for a submitted Sales Order.
	Called from client-side JS after submit to show alert dialog.
	Returns dict with low_stock_items and mr_data for Material Request creation.
	"""
	doc = frappe.get_doc("Sales Order", sales_order)
	low_stock_items = []
	ordered_qty_map = {}

	# Aggregate ordered qty per item+warehouse from SO items
	for item in doc.items:
		if not item.item_code:
			continue
		warehouse = item.warehouse or doc.get("set_warehouse")
		if not warehouse:
			continue
		key = (item.item_code, warehouse)
		ordered_qty_map[key] = flt(ordered_qty_map.get(key, 0)) + flt(item.qty)

	checked_items = set()
	for item in doc.items:
		if not item.item_code:
			continue

		warehouse = item.warehouse or doc.get("set_warehouse")
		if not warehouse:
			continue

		key = (item.item_code, warehouse)
		if key in checked_items:
			continue
		checked_items.add(key)

		safety_stock = flt(frappe.db.get_value("Item", item.item_code, "safety_stock"))
		if not safety_stock:
			continue

		# Bin's actual_qty does not change on Sales Order (only on Delivery Note)
		# But 'projected_qty' and 'reserved_qty' do change. 
		# Or we can just calculate manually: resulting_qty = actual_qty - ordered_qty
		actual_qty = flt(
			frappe.db.get_value(
				"Bin",
				{"item_code": item.item_code, "warehouse": warehouse},
				"actual_qty",
			)
		)

		ordered_qty = ordered_qty_map.get(key, 0)
		resulting_qty = actual_qty - ordered_qty

		if resulting_qty < safety_stock:
			stock_uom = frappe.db.get_value("Item", item.item_code, "stock_uom") or ""

			low_stock_items.append(
				{
					"item_code": item.item_code,
					"warehouse": warehouse,
					"stock_uom": stock_uom,
					"ordered_qty": ordered_qty_map.get(key, 0),
					"actual_qty": actual_qty,
					"safety_stock": safety_stock,
				}
			)

	if not low_stock_items:
		return {"items": [], "mr_data": {}}

	mr_data = {
		"material_request_type": "Purchase",
		"schedule_date": frappe.utils.nowdate(),
		"transaction_date": frappe.utils.nowdate(),
		"items": [
			{
				"item_code": item["item_code"],
				"warehouse": item["warehouse"],
				"uom": item["stock_uom"],
				"qty": 0,
				"schedule_date": frappe.utils.nowdate()
			}
			for item in low_stock_items
		]
	}

	return {
		"items": low_stock_items,
		"mr_data": mr_data,
	}