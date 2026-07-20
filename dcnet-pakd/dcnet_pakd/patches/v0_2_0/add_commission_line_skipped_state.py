"""Reload PAKD Commission Line so the new state option + override_rate +
posted_by_cell + skip_reason fields are in meta before any code reads them.
Idempotent — reload_doc is safe to repeat."""

import frappe


def execute():
	frappe.reload_doc("dcnet_pakd", "doctype", "pakd_commission_line", force=True)
