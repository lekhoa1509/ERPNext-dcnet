# Copyright (c) 2026, DCNET Cloud and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	"""Return columns and data for Serial No Warranty Status report.

	Replicates the standard 'Serial No Warranty Expiry' Report Builder
	as a Script Report with additional columns and Sales Invoice join.
	"""
	try:
		columns = get_columns()
		data = get_data(filters)
		return columns, data
	except Exception:
		frappe.log_error(title="Serial No Warranty Status Report Error")
		return get_columns(), []


def get_columns():
	"""Return report columns."""
	return [
		{
			"label": _("Serial No"),
			"fieldname": "name",
			"fieldtype": "Link",
			"options": "Serial No",
			"width": 150,
		},
		{
			"label": _("Batch No"),
			"fieldname": "batch_no",
			"fieldtype": "Link",
			"options": "Batch",
			"width": 120,
		},
		{
			"label": _("Status"),
			"fieldname": "status",
			"fieldtype": "Data",
			"width": 100,
		},
		{
			"label": _("Item Code"),
			"fieldname": "item_code",
			"fieldtype": "Link",
			"options": "Item",
			"width": 150,
		},
		{
			"label": _("Item Name"),
			"fieldname": "item_name",
			"fieldtype": "Data",
			"width": 180,
		},
		{
			"label": _("Item Group"),
			"fieldname": "item_group",
			"fieldtype": "Link",
			"options": "Item Group",
			"width": 140,
		},
		{
			"label": _("Brand"),
			"fieldname": "brand",
			"fieldtype": "Link",
			"options": "Brand",
			"width": 120,
		},
		{
			"label": _("Customer"),
			"fieldname": "customer",
			"fieldtype": "Link",
			"options": "Customer",
			"width": 150,
		},
		{
			"label": _("Posting Date"),
			"fieldname": "posting_date",
			"fieldtype": "Date",
			"width": 120,
		},
		{
			"label": _("Warranty Expiry Date"),
			"fieldname": "warranty_expiry_date",
			"fieldtype": "Date",
			"width": 140,
		},
		{
			"label": _("Warranty Period (Days)"),
			"fieldname": "warranty_period",
			"fieldtype": "Int",
			"width": 140,
		},
		{
			"label": _("AMC Expiry Date"),
			"fieldname": "amc_expiry_date",
			"fieldtype": "Date",
			"width": 120,
		},
		{
			"label": _("Maintenance Status"),
			"fieldname": "maintenance_status",
			"fieldtype": "Data",
			"width": 140,
		},
		{
			"label": _("Sales Invoice No"),
			"fieldname": "sales_invoice_no",
			"fieldtype": "Link",
			"options": "Sales Invoice",
			"width": 160,
		},
		{
			"label": _("Warehouse"),
			"fieldname": "warehouse",
			"fieldtype": "Link",
			"options": "Warehouse",
			"width": 150,
		},
		{
			"label": _("Description"),
			"fieldname": "description",
			"fieldtype": "Data",
			"width": 200,
		},
	]


def get_data(filters):
	"""Query Serial No data with Sales Invoice join."""
	conditions = ["sn.warranty_period > 0"]
	values = {}

	if filters and filters.get("item_code"):
		conditions.append("sn.item_code = %(item_code)s")
		values["item_code"] = filters["item_code"]

	if filters and filters.get("item_group"):
		conditions.append("i.item_group = %(item_group)s")
		values["item_group"] = filters["item_group"]

	if filters and filters.get("brand"):
		conditions.append("i.brand = %(brand)s")
		values["brand"] = filters["brand"]

	if filters and filters.get("warehouse"):
		conditions.append("(sbb_out.warehouse = %(warehouse)s OR (sbb_out.warehouse IS NULL AND sn.warehouse = %(warehouse)s))")
		values["warehouse"] = filters["warehouse"]

	if filters and filters.get("maintenance_status"):
		conditions.append("sn.maintenance_status = %(maintenance_status)s")
		values["maintenance_status"] = filters["maintenance_status"]

	if filters and filters.get("status"):
		conditions.append("sn.status = %(status)s")
		values["status"] = filters["status"]

	if filters and filters.get("customer"):
		conditions.append("sn.customer = %(customer)s")
		values["customer"] = filters["customer"]

	if filters and filters.get("batch_no"):
		conditions.append("sn.batch_no = %(batch_no)s")
		values["batch_no"] = filters["batch_no"]

	if filters and filters.get("sales_invoice_no"):
		conditions.append("""(
			(sbb_out.voucher_type = 'Sales Invoice' AND sbb_out.voucher_no = %(sales_invoice_no)s)
			OR (sbb_out.voucher_type = 'Delivery Note' AND dni.against_sales_invoice = %(sales_invoice_no)s)
		)""")
		values["sales_invoice_no"] = filters["sales_invoice_no"]

	where_clause = " AND ".join(conditions)

	data = frappe.db.sql(
		f"""
		SELECT
			sn.name,
			sn.status,
			sn.item_code,
			sn.item_name,
			sn.customer,
			CASE 
				WHEN sbb_out.voucher_type = 'Delivery Note' THEN dn.posting_date
				WHEN sbb_out.voucher_type = 'Sales Invoice' THEN si.posting_date
				ELSE NULL
			END AS posting_date,
			sn.warranty_expiry_date,
			sn.warranty_period,
			sn.amc_expiry_date,
			sn.maintenance_status,
			sn.batch_no,
			CASE 
				WHEN sbb_out.voucher_type = 'Sales Invoice' THEN sbb_out.voucher_no
				WHEN sbb_out.voucher_type = 'Delivery Note' THEN dni.against_sales_invoice
				ELSE NULL
			END AS sales_invoice_no,
			sn.description,
			i.item_group,
			i.brand,
			COALESCE(sbb_out.warehouse, sn.warehouse) AS warehouse
		FROM `tabSerial No` sn
		LEFT JOIN `tabItem` i 
			ON i.name = sn.item_code
			
		-- Lấy Serial and Batch Bundle (Phiếu Xuất)
		LEFT JOIN `tabSerial and Batch Entry` sbe_out
			ON sbe_out.serial_no = sn.name AND sbe_out.is_outward = 1
		LEFT JOIN `tabSerial and Batch Bundle` sbb_out
			ON sbb_out.name = sbe_out.parent AND sbb_out.docstatus = 1
			
		-- Lấy against_sales_invoice thông qua Delivery Note Item
		LEFT JOIN `tabDelivery Note Item` dni
			ON dni.serial_and_batch_bundle = sbb_out.name 
			AND sbb_out.voucher_type = 'Delivery Note'
			
		-- Join trực tiếp với Sales Invoice và Delivery Note để lấy posting_date an toàn cho mọi luồng
		LEFT JOIN `tabSales Invoice` si
			ON (sbb_out.voucher_type = 'Sales Invoice' AND si.name = sbb_out.voucher_no)
			OR (sbb_out.voucher_type = 'Delivery Note' AND si.name = dni.against_sales_invoice)
		LEFT JOIN `tabDelivery Note` dn
			ON sbb_out.voucher_type = 'Delivery Note' AND dn.name = sbb_out.voucher_no
			
		WHERE {where_clause}
		GROUP BY sn.name
		ORDER BY sn.warranty_period ASC
		""",
		values=values,
		as_dict=True,
	)

	# Tối ưu hóa dịch thuật bằng cách cache các giá trị duy nhất
	status_map = {}
	m_status_map = {}

	for row in data:
		if row.status:
			if row.status not in status_map:
				status_map[row.status] = _(row.status)
			row.status = status_map[row.status]

		if row.maintenance_status:
			if row.maintenance_status not in m_status_map:
				m_status_map[row.maintenance_status] = _(row.maintenance_status)
			row.maintenance_status = m_status_map[row.maintenance_status]

	return data
