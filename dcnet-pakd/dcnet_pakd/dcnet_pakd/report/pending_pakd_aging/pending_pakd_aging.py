"""Pending PAKD Aging — PAKDs waiting for approval, bucketed by age."""

import frappe
from frappe import _
from frappe.utils import today, date_diff, getdate


def execute(filters=None):
    columns = get_columns()
    data = get_data()
    return columns, data


def get_columns():
    return [
        {"fieldname": "name", "label": _("PAKD"), "fieldtype": "Link", "options": "Phuong An Kinh Doanh", "width": 150},
        {"fieldname": "customer", "label": _("Customer"), "fieldtype": "Data", "width": 180},
        {"fieldname": "sales_person", "label": _("Sales Person"), "fieldtype": "Link", "options": "Sales Person", "width": 130},
        {"fieldname": "workflow_state", "label": _("Status"), "fieldtype": "Data", "width": 130},
        {"fieldname": "created_on", "label": _("Created Date"), "fieldtype": "Date", "width": 100},
        {"fieldname": "age_days", "label": _("Days Pending"), "fieldtype": "Int", "width": 100},
        {"fieldname": "age_bucket", "label": _("Age Bucket"), "fieldtype": "Data", "width": 90},
        {"fieldname": "contract_value", "label": _("Contract Value"), "fieldtype": "Currency", "width": 120},
    ]


def get_data():
    pending_states = (
        "Pending Sales Director", "Pending General Dept",
        "Pending Branch Director", "Pending Board",
    )
    placeholders = ", ".join(f"'{s}'" for s in pending_states)

    rows = frappe.db.sql(
        f"""
        SELECT
            p.name,
            p.customer,
            p.sales_person,
            p.workflow_state,
            DATE(p.creation) AS created_on,
            COALESCE(p.total_revenue_contract, 0) AS contract_value
        FROM `tabPhuong An Kinh Doanh` p
        WHERE p.workflow_state IN ({placeholders})
        ORDER BY p.creation ASC
        """,
        as_dict=True,
    )

    ref = getdate(today())
    for r in rows:
        age = date_diff(ref, r["created_on"]) if r["created_on"] else 0
        r["age_days"] = age
        if age <= 2:
            r["age_bucket"] = _("0-2 days")
        elif age <= 7:
            r["age_bucket"] = _("3-7 days")
        elif age <= 14:
            r["age_bucket"] = _("8-14 days")
        else:
            r["age_bucket"] = _("> 14 days")

    return rows
