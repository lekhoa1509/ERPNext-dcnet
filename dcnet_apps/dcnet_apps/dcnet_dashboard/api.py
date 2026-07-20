# Copyright (c) 2026, DCNET Cloud and contributors
# For license information, please see license.txt

import frappe


@frappe.whitelist()
def get_total_revenue():
	return {
		"value": 2847500000,
		"fieldtype": "Currency",
		"route_options": {},
		"route": [],
	}


@frappe.whitelist()
def get_wholesale_revenue():
	return {
		"value": 1923000000,
		"fieldtype": "Currency",
		"route_options": {},
		"route": [],
	}


@frappe.whitelist()
def get_retail_revenue():
	return {
		"value": 924500000,
		"fieldtype": "Currency",
		"route_options": {},
		"route": [],
	}
