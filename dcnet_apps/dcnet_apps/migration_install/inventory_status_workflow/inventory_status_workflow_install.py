# Copyright (c) 2025, DCNET Cloud
# For license information, please see license.txt

import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


def setup_purchase_receipt_workflow():
    """
    Setup Purchase Receipt approval workflow
    Called during install or migrate
    """

    print("Setting up Purchase Receipt Workflow...")

    create_inventory_status_field()
    create_workflow_states()
    create_workflow_actions()

    frappe.db.commit()

    create_purchase_receipt_workflow()

    print("✅ Successfully set up Purchase Receipt Workflow!")


# ---------------------------------------------------------------------
# Custom Field
# ---------------------------------------------------------------------

def create_inventory_status_field():

    if frappe.db.exists(
        "Custom Field",
        {"dt": "Purchase Receipt", "fieldname": "inventory_status"}):
        return

    fields = {
        "Purchase Receipt": [
            {
                "fieldname": "inventory_status",
                "label": "Inventory Status",
                "fieldtype": "Select",
                "options": "\nDraft\nAwaiting Approval\nReceived into Inventory\nCancelled",
                "default": "Draft",
                "read_only": 1,
                "insert_after": "posting_time"
            }
        ]
    }

    create_custom_fields(fields)

    print("✅ Custom field 'inventory_status' created")


# ---------------------------------------------------------------------
# Workflow States
# NOTE: The states "To Receive", "To Bill", and "Completed" are set automatically
# by update_po_state() when Receipt/Invoice is submitted — bypassing workflow transitions.
# Do not declare them in states[] as they do not have manual transitions.
# ---------------------------------------------------------------------

def create_workflow_states():

    states = [
        ("Draft", "Warning"),
        ("Awaiting Approval", "Info"),
        ("Received into Inventory", "Success"),
        ("Cancelled", "Danger"),
    ]

    for state_name, style in states:

        if frappe.db.exists("Workflow State", state_name):
            continue

        doc = frappe.get_doc({
            "doctype": "Workflow State",
            "workflow_state_name": state_name,
            "style": style
        })

        doc.insert(ignore_permissions=True)
        frappe.db.commit()

        print(f"✅ Workflow State created: {state_name}")


# ---------------------------------------------------------------------
# Workflow Actions
# ---------------------------------------------------------------------

def create_workflow_actions():

    actions = [
        "Submit for Approval",
        "Approve",
        "Cancel"
    ]

    for action in actions:

        if frappe.db.exists("Workflow Action Master", action):
            continue

        doc = frappe.get_doc({
            "doctype": "Workflow Action Master",
            "workflow_action_name": action
        })

        doc.insert(ignore_permissions=True)

        print(f"✅ Workflow Action created: {action}")


# ---------------------------------------------------------------------
# Workflow
# ---------------------------------------------------------------------

def create_purchase_receipt_workflow():

    workflow_name = "Purchase Receipt Approval Workflow"

    if frappe.db.exists("Workflow", workflow_name):
        return

    workflow = frappe.get_doc({
        "doctype": "Workflow",
        "workflow_name": workflow_name,
        "document_type": "Purchase Receipt",
        "workflow_state_field": "inventory_status",
        "is_active": 1,
        "send_email_alert": 0,

        "states": [
            {
                "state": "Draft",
                "doc_status": 0,
                "allow_edit": "Stock User",
                "update_field": "inventory_status",
                "update_value": "Draft"
            },
            {
                "state": "Awaiting Approval",
                "doc_status": 0,
                "allow_edit": "Stock Manager",
                "update_field": "inventory_status",
                "update_value": "Awaiting Approval"
            },
            {
                "state": "Received into Inventory",
                "doc_status": 1,
                "allow_edit": "Stock Manager",
                "update_field": "inventory_status",
                "update_value": "Received into Inventory"
            },
            {
                "state": "Cancelled",
                "doc_status": 2,
                "allow_edit": "Stock Manager",
                "update_field": "inventory_status",
                "update_value": "Cancelled"
            }
        ],

        "transitions": [
            {
                "state": "Draft",
                "action": "Submit for Approval",
                "next_state": "Awaiting Approval",
                "allowed": "Stock User",
                "allow_self_approval": 1
            },
            {
                "state": "Awaiting Approval",
                "action": "Approve",
                "next_state": "Received into Inventory",
                "allowed": "Stock Manager",
                "allow_self_approval": 1
            },
            {
                "state": "Received into Inventory",
                "action": "Cancel",
                "next_state": "Cancelled",
                "allowed": "Stock Manager",
                "allow_self_approval": 1
            }
        ]
    })

    workflow.insert(ignore_permissions=True)

    frappe.db.commit()

    print("✅ Workflow 'Purchase Receipt Approval Workflow' created successfully")
