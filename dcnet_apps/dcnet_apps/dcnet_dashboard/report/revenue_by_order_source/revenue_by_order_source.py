# Copyright (c) 2026, DCNET Cloud and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
    filters = frappe._dict(filters or {})
    columns = get_columns()
    data = get_data(filters)
    chart = get_chart(data)
    return columns, data, None, chart


def get_columns():
    return [
        {
            "fieldname": "order_source",
            "label": _("Order Source"),
            "fieldtype": "Data",
            "width": 200,
        },
        {
            "fieldname": "revenue",
            "label": _("Revenue"),
            "fieldtype": "Currency",
            "width": 150,
        },
    ]


def get_data(filters):
    try:
        from erpnext.accounts.utils import get_fiscal_year
        
        # 1. Set default filters to prevent pulling the entire DB history
        if not filters.get("from_date") or not filters.get("to_date"):
            fiscal_year = get_fiscal_year(frappe.utils.nowdate(), as_dict=True)
            if not filters.get("from_date"):
                filters["from_date"] = fiscal_year.year_start_date
            if not filters.get("to_date"):
                filters["to_date"] = frappe.utils.nowdate()

        conditions = [
            "si.docstatus = 1",
            "si.status NOT IN ('Draft', 'Cancelled', 'Return', 'Credit Note Issued', 'Internal Transfer')"
        ]
        values = {}

        if filters.get("from_date"):
            conditions.append("si.posting_date >= %(from_date)s")
            values["from_date"] = filters.from_date

        if filters.get("to_date"):
            conditions.append("si.posting_date <= %(to_date)s")
            values["to_date"] = filters.to_date

        if filters.get("company"):
            conditions.append("si.company = %(company)s")
            values["company"] = filters.company

        if filters.get("utm_source"):
            conditions.append("so.utm_source = %(utm_source)s")
            values["utm_source"] = filters.utm_source

        data = frappe.db.sql(
            """
            SELECT
                IFNULL(us.name, '{unknown_label}') as order_source,
                SUM(sii.base_amount) as revenue
            FROM `tabSales Invoice Item` sii
            JOIN `tabSales Invoice` si ON sii.parent = si.name
            LEFT JOIN `tabSales Order` so ON sii.sales_order = so.name
            LEFT JOIN `tabUTM Source` us ON so.utm_source = us.name
            WHERE {conditions}
            GROUP BY order_source
            ORDER BY revenue DESC
            """.format(
                conditions=" AND ".join(conditions),
                unknown_label=_("Unknown")
            ),
            values,
            as_dict=1,
        )

        return data
    except Exception as e:
        frappe.log_error(title="Revenue by Order Source Error", message=frappe.get_traceback())
        # Return empty list if it fails, so it doesn't crash the UI
        return []


def get_chart(data):
    if not data:
        return None
    return {
        "data": {
            "labels": [d.order_source for d in data],
            "datasets": [{"name": _("Revenue"), "values": [d.revenue for d in data]}],
        },
        "type": "bar",
    }
