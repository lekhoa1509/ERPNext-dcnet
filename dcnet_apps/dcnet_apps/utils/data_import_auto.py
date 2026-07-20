"""
Auto-import functionality for Data Import DocType.

Automatically starts import when file is uploaded, bypassing the confirmation button.
"""

import frappe
from frappe import _


@frappe.whitelist()
def auto_start_import(data_import_name):
	"""
	Auto-start import without confirmation button.
	
	This method is called via client script when import_file is set.
	It directly triggers the import process without requiring user confirmation.
	
	Args:
		data_import_name: Name of the Data Import document
		
	Returns:
		Result of start_import() method
	"""
	data_import = frappe.get_doc("Data Import", data_import_name)
	data_import.check_permission("write")
	
	# Directly start the import
	return data_import.start_import()
