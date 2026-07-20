# Copyright (c) 2026, DCNET

import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


WORKFLOW_NAME = "Purchase Order Custom Workflow"


# --------------------------------------------------
# MAIN SETUP
# --------------------------------------------------

def setup_purchase_order_workflow():

    print("🚀 Setting up Purchase Order Workflow...")

    create_po_status_field()

    create_workflow_states()

    create_workflow_actions()

    frappe.db.commit()

    create_purchase_order_workflow()

    print("✅ Workflow setup completed")


# --------------------------------------------------
# CUSTOM FIELD
# --------------------------------------------------

def create_po_status_field():

    if frappe.db.exists(
        "Custom Field",
        {"dt": "Purchase Order", "fieldname": "po_workflow_state"}
    ):
        return

    fields = {
        "Purchase Order": [
            {
                "fieldname": "po_workflow_state",
                "label": "PO Workflow State",
                "fieldtype": "Select",
                "options": "\nDraft\nSent to Supplier\nIn Delivery\nTo Receive and Bill\nTo Receive\nTo Bill\nCompleted",
                "default": "Draft",
                "read_only": 1,
                "allow_on_submit": 1,
                "insert_after": "status"
            }
        ]
    }

    create_custom_fields(fields)

    print("Custom field created")


# --------------------------------------------------
# WORKFLOW STATES
# --------------------------------------------------

def create_workflow_states():

    states = [

        ("Sent to Supplier", "Info"),
        ("In Delivery", "Primary"),

        ("To Receive and Bill", "Warning"),
        ("To Receive", "Warning"),
        ("To Bill", "Warning"),

        ("Completed", "Success")

    ]

    for state, style in states:

        if frappe.db.exists("Workflow State", state):

            frappe.db.set_value(
                "Workflow State",
                state,
                "style",
                style
            )

        else:

            doc = frappe.get_doc({
                "doctype": "Workflow State",
                "workflow_state_name": state,
                "style": style
            })

            doc.insert(ignore_permissions=True)


# --------------------------------------------------
# WORKFLOW ACTION
# --------------------------------------------------

def create_workflow_actions():

    actions = [

        "Mark as sent to Supplier",
        "Mark as delivery",
        "Mark as ready to Receive"

    ]

    for action in actions:

        if frappe.db.exists("Workflow Action Master", action):
            continue

        doc = frappe.get_doc({

            "doctype": "Workflow Action Master",
            "workflow_action_name": action

        })

        doc.insert(ignore_permissions=True)


# --------------------------------------------------
# WORKFLOW
# --------------------------------------------------

def create_purchase_order_workflow():

    if frappe.db.exists("Workflow", WORKFLOW_NAME):
        print(f"⚠️ Workflow {WORKFLOW_NAME} already exists, skipping creation")
        return

    workflow = frappe.get_doc({

        "doctype": "Workflow",
        "workflow_name": WORKFLOW_NAME,
        "document_type": "Purchase Order",
        "workflow_state_field": "po_workflow_state",
        "is_active": 1,


        "states": [

            {
                "state": "Draft",
                "doc_status": 0,
                "allow_edit": "Purchase User"
            },

            {
                "state": "Sent to Supplier",
                "doc_status": 1,
                "allow_edit": "Purchase User"
            },

            {
                "state": "In Delivery",
                "doc_status": 1,
                "allow_edit": "Purchase User"
            },

            {
                "state": "To Receive and Bill",
                "doc_status": 1,
                "allow_edit": "Purchase User"
            }

        ],


        "transitions": [

            {
                "state": "Draft",
                "action": "Mark as sent to Supplier",
                "next_state": "Sent to Supplier",
                "allowed": "Purchase User"
            },

            {
                "state": "Sent to Supplier",
                "action": "Mark as delivery",
                "next_state": "In Delivery",
                "allowed": "Purchase User"
            },

            {
                "state": "In Delivery",
                "action": "Mark as ready to Receive",
                "next_state": "To Receive and Bill",
                "allowed": "Purchase User"
            }

        ]

    })

    workflow.insert(ignore_permissions=True)

    frappe.db.commit()

    print("Workflow created")