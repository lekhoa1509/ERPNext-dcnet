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
            "fieldname": "item_code",
            "label": _("Item Code"),
            "fieldtype": "Link",
            "options": "Item",
            "width": 150,
        },
        {
            "fieldname": "item_name",
            "label": _("Item Name"),
            "fieldtype": "Data",
            "width": 250,
        },
        {
            "fieldname": "qty",
            "label": _("Qty"),
            "fieldtype": "Float",
            "width": 100,
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

        if not filters.get("from_date") or not filters.get("to_date"):
            fiscal_year = get_fiscal_year(frappe.utils.nowdate(), as_dict=True)
            if not filters.get("from_date"):
                filters["from_date"] = fiscal_year.year_start_date
            if not filters.get("to_date"):
                filters["to_date"] = frappe.utils.nowdate()

        limit = filters.get("limit", 20)
        conditions = [
            "si.docstatus = 1",
            "si.status NOT IN ('Draft', 'Cancelled', 'Return', 'Credit Note Issued', 'Internal Transfer')"
        ]
        values = {"limit": limit}

        if filters.get("from_date"):
            conditions.append("si.posting_date >= %(from_date)s")
            values["from_date"] = filters.from_date

        if filters.get("to_date"):
            conditions.append("si.posting_date <= %(to_date)s")
            values["to_date"] = filters.to_date

        if filters.get("company"):
            conditions.append("si.company = %(company)s")
            values["company"] = filters.company

        data = frappe.db.sql(
            """
            SELECT
                sii.item_code,
                sii.item_name,
                SUM(sii.qty) as qty,
                SUM(sii.amount) as revenue
            FROM `tabSales Invoice Item` sii
            JOIN `tabSales Invoice` si ON sii.parent = si.name
            WHERE {conditions}
            GROUP BY sii.item_code, sii.item_name
            ORDER BY revenue DESC
            LIMIT %(limit)s
            """.format(conditions=" AND ".join(conditions)),
            values,
            as_dict=1,
        )

        return data
    except Exception as e:
        frappe.log_error(title="Top Products by Revenue Error", message=frappe.get_traceback())
        return []


def get_chart(data):
    if not data:
        return None
    return {
        "data": {
            "labels": [d.item_name for d in data[:10]],
            "datasets": [
                {"name": _("Revenue"), "values": [d.revenue for d in data[:10]]}
            ],
        },
        "type": "bar",
    }
