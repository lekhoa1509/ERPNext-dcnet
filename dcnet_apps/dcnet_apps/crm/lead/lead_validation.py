# Copyright (c) 2026, DCNET Cloud
# For license information, please see license.txt

"""
Lead Duplicate Validation for DCNET Apps

Validates that email and phone numbers are unique across Lead and Customer
when creating or updating a Lead record.
"""

import frappe
from frappe import _
from frappe.utils import get_link_to_form


def validate_lead_duplicate(doc, method):
    """
    Hook called on Lead validate event to check duplicates.
    
    Checks:
    - Email uniqueness in Lead and Customer
    - Phone uniqueness in Lead and Customer
    
    Args:
        doc: Lead document
        method: Event method name ("validate")
    """
    validate_email_duplicate(doc)
    validate_phone_duplicate(doc)


def validate_email_duplicate(doc):
    """
    Check email uniqueness across Lead and Customer.
    Uses simple indexed queries for better performance with large datasets.
    
    Args:
        doc: Lead document
    """
    if not doc.email_id:
        return
    
    # Check duplicate email in Lead
    duplicate_lead = frappe.db.get_value(
        "Lead",
        filters={
            "email_id": doc.email_id,
            "name": ["!=", doc.name]
        },
        fieldname="name"
    )
    
    if duplicate_lead:
        frappe.throw(
            _("Email Address {0} is already used in Lead {1}").format(
                frappe.bold(doc.email_id),
                get_link_to_form("Lead", duplicate_lead)
            ),
            title=_("Duplicate Contact Found"),
            exc=frappe.DuplicateEntryError
        )
    
    # Check duplicate email in Customer (direct field, indexed)
    duplicate_customer = frappe.db.get_value(
        "Customer",
        filters={"email_id": doc.email_id},
        fieldname="name"
    )
    
    if duplicate_customer:
        frappe.throw(
            _("Email Address {0} is already used in Customer {1}").format(
                frappe.bold(doc.email_id),
                get_link_to_form("Customer", duplicate_customer)
            ),
            title=_("Duplicate Contact Found"),
            exc=frappe.DuplicateEntryError
        )


def validate_phone_duplicate(doc):
    """
    Check phone uniqueness across Lead and Customer.
    Only checks 'phone' field as per requirement (not mobile_no).
    Uses simple indexed queries for better performance with large datasets.
    
    Args:
        doc: Lead document
    """
    if not doc.phone:
        return
    
    # Check duplicate phone in Lead (only check phone field)
    duplicate_lead = frappe.db.get_value(
        "Lead",
        filters={
            "phone": doc.phone,
            "name": ["!=", doc.name]
        },
        fieldname="name"
    )
    
    if duplicate_lead:
        frappe.throw(
            _("Phone Number {0} is already used in Lead {1}").format(
                frappe.bold(doc.phone),
                get_link_to_form("Lead", duplicate_lead)
            ),
            title=_("Duplicate Contact Found"),
            exc=frappe.DuplicateEntryError
        )
    
    # Check duplicate phone in Customer
    # Customer stores phone in 'mobile_no' field (fetched from primary contact)
    duplicate_customer = frappe.db.get_value(
        "Customer",
        filters={"mobile_no": doc.phone},
        fieldname="name"
    )
    
    if duplicate_customer:
        frappe.throw(
            _("Phone Number {0} is already used in Customer {1}").format(
                frappe.bold(doc.phone),
                get_link_to_form("Customer", duplicate_customer)
            ),
            title=_("Duplicate Contact Found"),
            exc=frappe.DuplicateEntryError
        )
