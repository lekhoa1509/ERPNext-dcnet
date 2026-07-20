# Copyright (c) 2026, DCNET Cloud and contributors
# For license information, please see license.txt

import frappe
import copy
from frappe.model.document import Document

class BarcodeLabel(Document):
	def db_insert(self, *args, **kwargs):
		"""Append a new barcode to the Item's barcodes child table"""
		if not self.item:
			frappe.throw("Item is required to add a barcode")
		
		# Check if user has write permission on the Item
		if not frappe.has_permission("Item", "write", self.item):
			frappe.throw(f"No permission to edit Item {self.item}", frappe.PermissionError)

		item_doc = frappe.get_doc("Item", self.item)
		
		# Check if barcode already exists for this item
		for row in item_doc.barcodes:
			if row.barcode == self.barcode:
				frappe.throw(f"Barcode {self.barcode} already exists for Item {self.item}")
		
		# Append to child table
		item_doc.append("barcodes", {
			"barcode": self.barcode,
			"barcode_type": self.barcode_type,
			"uom": self.uom
		})
		
		item_doc.save(ignore_permissions=True)
		
		# In virtual doctypes, name is often the name of the underlying record
		# For child tables, we can use the name of the child row
		new_row = item_doc.barcodes[-1]
		self.name = new_row.name

	def load_from_db(self):
		"""Load barcode data from tabItem Barcode"""
		# Finding by name (which is the child row name)
		data = frappe.db.get_value("Item Barcode", self.name, 
			["parent as item", "barcode", "barcode_type", "uom"], as_dict=True)
		
		if not data:
			frappe.throw(f"Barcode Label {self.name} not found")
		
		self.update(data)
		self.barcode_value = self.barcode

	def db_update(self):
		"""Update the barcode entry in the parent Item"""
		barcode_row = frappe.get_doc("Item Barcode", self.name)
		# Check if user has write permission on the Item
		if not frappe.has_permission("Item", "write", barcode_row.parent):
			frappe.throw(f"No permission to edit Item {barcode_row.parent}", frappe.PermissionError)

		item_doc = frappe.get_doc("Item", barcode_row.parent)
		
		for row in item_doc.barcodes:
			if row.name == self.name:
				row.barcode = self.barcode
				row.barcode_type = self.barcode_type
				row.uom = self.uom
				break
		
		item_doc.save(ignore_permissions=True)

	def db_delete(self):
		"""Remove the barcode entry from the parent Item"""
		barcode_row = frappe.get_doc("Item Barcode", self.name)
		# Check if user has write permission on the Item
		if not frappe.has_permission("Item", "write", barcode_row.parent):
			frappe.throw(f"No permission to edit Item {barcode_row.parent}", frappe.PermissionError)

		item_doc = frappe.get_doc("Item", barcode_row.parent)
		
		item_doc.set("barcodes", [d for d in item_doc.barcodes if d.name != self.name])
		item_doc.save(ignore_permissions=True)

	@staticmethod
	def get_list(args):
		"""Fetch list of barcodes from tabItem Barcode using frappe.get_all"""
		filters = copy.deepcopy(args.get("filters") or [])
		
		# Map filters from Barcode Label to Item Barcode schema if needed
		# In Item Barcode child table, 'item' is 'parent'
		if isinstance(filters, list):
			for f in filters:
				if isinstance(f, list) and len(f) > 1 and f[1] == "item":
					f[1] = "parent"
		
		order_by = args.get("order_by") or "modified desc"
		# Remove virtual table name prefix and all backticks to prevent syntax errors
		order_by = order_by.replace("`tabBarcode Label`.", "").replace("`", "")
		
		# Ensure we are not passing complex order_by that might still fail
		if "." in order_by:
			order_by = "modified desc"
		
		# Enforce permissions: Only show barcodes for Items the user can read
		if not (args.get("ignore_permissions") or frappe.session.user == "Administrator"):
			allowed_items = frappe.get_list("Item", pluck="name")
			if isinstance(filters, list):
				filters.append(["parent", "in", allowed_items])
			elif isinstance(filters, dict):
				filters["parent"] = ["in", allowed_items]

		return frappe.get_all("Item Barcode", 
			fields=["name", "parent as item", "barcode", "barcode as barcode_value", "barcode_type", "uom", "modified"],
			filters=filters,
			order_by=order_by,
			limit_start=args.get("limit_start", 0),
			limit_page_length=args.get("limit", 20)
		)

	@staticmethod
	def get_count(args):
		"""Count total barcodes using frappe.db.count"""
		filters = copy.deepcopy(args.get("filters") or [])
		if isinstance(filters, list):
			for f in filters:
				if isinstance(f, list) and len(f) > 1 and f[1] == "item":
					f[1] = "parent"
					
		# Enforce permissions
		if not (args.get("ignore_permissions") or frappe.session.user == "Administrator"):
			allowed_items = frappe.get_list("Item", pluck="name")
			if isinstance(filters, list):
				filters.append(["parent", "in", allowed_items])
			elif isinstance(filters, dict):
				filters["parent"] = ["in", allowed_items]
					
		return frappe.db.count("Item Barcode", filters)

	@staticmethod
	def get_stats(args):
		"""Required for virtual doctypes"""
		return {}

	def normalize_barcode_type(self, barcode_type):
		"""Normalize barcode type for JsBarcode compatibility"""
		type_mapping = {
			"EAN": "EAN-13",
			"UPC": "UPC-A"
		}
		return type_mapping.get(barcode_type, barcode_type)
