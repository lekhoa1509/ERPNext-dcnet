"""
Whitelisted API endpoints for EInvoice.

Thin layer: validates permissions, parses input, delegates to services.
All endpoints require System Manager or Accounts Manager role.
"""

import frappe

from einvoice.einvoice.services.issuance import IssuanceService
from einvoice.einvoice.services.sync import SyncService
from einvoice.einvoice.services.state_sync import sync_pending_invoices


def has_app_permission():
    """Permission check for apps screen."""
    return "System Manager" in frappe.get_roles() or "Accounts Manager" in frappe.get_roles()


@frappe.whitelist()
def issue_single_invoice(sales_invoice, provider=None, pattern=None, serial=None,
                         issue_mode=None, send_email=None):
    """Issue a single outward e-invoice from a submitted Sales Invoice."""
    frappe.only_for(["System Manager", "Accounts Manager"])
    return IssuanceService.issue_single(
        sales_invoice, provider, pattern, serial, issue_mode, send_email=send_email
    )


@frappe.whitelist()
def issue_bulk_invoices(sales_invoices, provider=None, pattern=None, serial=None,
                        issue_mode=None, send_email=None):
    """Issue outward e-invoices for multiple Sales Invoices."""
    frappe.only_for(["System Manager", "Accounts Manager"])
    return IssuanceService.issue_bulk(
        sales_invoices, provider, pattern, serial, issue_mode, send_email=send_email
    )


@frappe.whitelist()
def get_providers(company=None):
    """Get list of enabled providers for the dropdown."""
    frappe.only_for(["System Manager", "Accounts Manager"])
    filters = {"enabled": 1}
    if company:
        filters["company"] = company
    return frappe.get_all(
        "EInvoice Provider",
        filters=filters,
        fields=["name", "provider_name", "provider_type",
                "default_invoice_pattern", "default_invoice_serial"],
    )


@frappe.whitelist()
def sync_inward_invoices():
    """Trigger manual sync of inward invoices from all active providers."""
    frappe.only_for(["System Manager", "Accounts Manager"])
    return SyncService.run_sync(sync_type="Manual")


@frappe.whitelist()
def push_to_easyinvoice(sales_invoice, provider=None):
    """Push a submitted Sales Invoice to EasyInvoice as unsigned draft."""
    frappe.only_for(["System Manager", "Accounts Manager"])
    return IssuanceService.push_draft(sales_invoice, provider)


@frappe.whitelist()
def sync_outward_states_now(provider=None):
    """Manually trigger outward invoice state sync (skips enable_auto_sync gate)."""
    frappe.only_for(["System Manager", "Accounts Manager"])
    return sync_pending_invoices(provider_name=provider)


@frappe.whitelist()
def get_easyinvoice_link(sales_invoice):
    """Return the EasyInvoice lookup URL for a pushed/issued SI."""
    frappe.only_for(["System Manager", "Accounts Manager", "Sales User", "Sales Manager"])
    si = frappe.db.get_value(
        "Sales Invoice",
        sales_invoice,
        ["einvoice_ikey", "einvoice_status_text", "einvoice_issued",
         "einvoice_number", "einvoice_lookup_code", "einvoice_link_view",
         "einvoice_pushed"],
        as_dict=True,
    )
    if not si:
        frappe.throw(f"Sales Invoice {sales_invoice} không tồn tại.")
    return si
